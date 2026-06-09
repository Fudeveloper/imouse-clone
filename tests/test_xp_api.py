from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from fastapi.testclient import TestClient
from PIL import Image

from imouse.server import (
    app,
    clear_xp_callback_events,
    clear_xp_runtime_state,
    manager,
    set_xp_runtime_store_path,
)


class FakeCapture:
    def __init__(self, image):
        self.image = image

    def capture(self):
        return self.image


class XPApiTest(unittest.TestCase):
    def setUp(self):
        manager._devices.clear()
        manager._groups.clear()
        manager._saved_calibrations.clear()
        manager._saved_profiles.clear()
        manager._group_store_path = None
        manager._calibration_store_path = None
        manager._profile_store_path = None
        clear_xp_callback_events()
        set_xp_runtime_store_path(None)
        clear_xp_runtime_state()
        self.client = TestClient(app)

    def test_get_device_list_alias(self):
        response = self.client.get("/api", params={"fun": "/dev/list", "msgid": 7})

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["fun"], "/device/list")
        self.assertEqual(body["msgid"], 7)
        self.assertEqual(body["data"]["code"], 0)
        self.assertEqual(body["data"]["devices"], [])

    def test_post_register_accepts_xp_id(self):
        response = self.client.post("/api", json={
            "fun": "/device/register",
            "data": {"id": "xp_1"},
            "msgid": 9,
        })

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["fun"], "/device/register")
        self.assertEqual(body["msgid"], 9)
        self.assertEqual(body["data"]["id"], "xp_1")
        self.assertEqual(body["data"]["device_id"], "xp_1")
        self.assertEqual(body["data"]["state"], "offline")

    def test_post_register_accepts_top_level_fields(self):
        response = self.client.post("/api", json={
            "fun": "/device/register",
            "id": "xp_2",
        })

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["data"]["id"], "xp_2")

    def test_unknown_fun_returns_xp_error(self):
        response = self.client.post("/api", json={"fun": "/not/supported"})

        self.assertEqual(response.status_code, 404)
        body = response.json()
        self.assertEqual(body["fun"], "/not/supported")
        self.assertEqual(body["data"]["code"], 404)
        self.assertIn("Unsupported XP fun", body["message"])

    def test_websocket_accepts_xp_fun_payload(self):
        with self.client.websocket_connect("/ws") as websocket:
            welcome = websocket.receive_json()
            self.assertEqual(welcome["event"], "connected")

            websocket.send_json({"fun": "/dev/list", "msgid": 11})
            body = websocket.receive_json()

        self.assertEqual(body["fun"], "/device/list")
        self.assertEqual(body["msgid"], 11)
        self.assertEqual(body["data"]["devices"], [])

    def test_xp_api_websocket_alias_accepts_fun_and_pushes_callback(self):
        with self.client.websocket_connect("/api") as websocket:
            welcome = websocket.receive_json()
            self.assertEqual(welcome["event"], "connected")
            self.assertEqual(welcome["path"], "/api")

            websocket.send_json({
                "fun": "/device/register",
                "data": {"id": "ws_dev"},
                "msgid": 12,
            })
            first = websocket.receive_json()
            second = websocket.receive_json()

        messages = {item.get("event") or item.get("fun"): item for item in (first, second)}
        self.assertIn("callback", messages)
        self.assertIn("/device/register", messages)
        self.assertEqual(messages["/device/register"]["msgid"], 12)
        self.assertEqual(messages["callback"]["callback"]["event"], "device_registered")
        self.assertEqual(messages["callback"]["callback"]["device_id"], "ws_dev")

    def test_callback_fun_list_push_and_state_events(self):
        pushed = self.client.post("/api", json={
            "fun": "/callback/push",
            "msgid": 21,
            "data": {
                "event": "airplay_log",
                "id": "dev_1",
                "source": "receiver",
                "severity": "warn",
                "data": {"line": "receiver reconnect"},
            },
        })
        self.assertEqual(pushed.status_code, 200)
        event = pushed.json()["data"]["event"]
        self.assertEqual(event["seq"], 1)
        self.assertEqual(event["event"], "airplay_log")
        self.assertEqual(event["device_id"], "dev_1")

        self.client.post("/api", json={
            "fun": "/device/register",
            "data": {"id": "dev_1"},
        })

        listed = self.client.get("/api", params={
            "fun": "/callback/list",
            "after_seq": 0,
            "limit": 10,
        })
        self.assertEqual(listed.status_code, 200)
        events = listed.json()["data"]["events"]
        self.assertEqual([item["event"] for item in events], ["airplay_log", "device_registered"])
        self.assertEqual(listed.json()["data"]["last_seq"], 2)

        polled = self.client.post("/api", json={
            "fun": "/callback/poll",
            "data": {"after_seq": 1},
        })
        self.assertEqual([item["event"] for item in polled.json()["data"]["events"]], ["device_registered"])

    def test_config_user_and_shortcut_runtime_funs(self):
        config = self.client.post("/api", json={
            "fun": "/imconfig/set",
            "msgid": 31,
            "data": {"config": {"receiver_route": "windows_receiver", "theme": "field"}},
        })
        self.assertEqual(config.status_code, 200)
        body = config.json()
        self.assertEqual(body["fun"], "/config/set")
        self.assertEqual(body["msgid"], 31)
        self.assertEqual(body["data"]["config"]["receiver_route"], "windows_receiver")

        one_config = self.client.get("/api", params={"fun": "/config/get", "key": "receiver_route"})
        self.assertTrue(one_config.json()["data"]["exists"])
        self.assertEqual(one_config.json()["data"]["value"], "windows_receiver")

        user = self.client.post("/api", json={
            "fun": "/user/save",
            "data": {"user": {"user_id": "op_1", "role": "operator"}, "active": True},
        })
        self.assertEqual(user.status_code, 200)
        self.assertEqual(user.json()["fun"], "/user/set")
        self.assertEqual(user.json()["data"]["active_user"], "op_1")

        switched = self.client.post("/api", json={
            "fun": "/user/login",
            "data": {"id": "lead_1"},
        })
        self.assertEqual(switched.status_code, 200)
        self.assertEqual(switched.json()["data"]["active_user"], "lead_1")
        self.assertTrue(switched.json()["data"]["user"]["auto_created"])

        shortcut = self.client.post("/api", json={
            "fun": "/shortcut/set",
            "data": {
                "shortcut": {
                    "name": "open_settings",
                    "action": "combo",
                    "keys": [41],
                    "notes": "offline registry only",
                }
            },
        })
        self.assertEqual(shortcut.status_code, 200)
        self.assertEqual(shortcut.json()["fun"], "/shortcut/save")
        self.assertEqual(shortcut.json()["data"]["shortcut"]["name"], "open_settings")

        run = self.client.post("/api", json={
            "fun": "/shortcut/run",
            "data": {"name": "open_settings", "id": "dev_1"},
        })
        self.assertEqual(run.status_code, 200)
        self.assertTrue(run.json()["data"]["dry_run"])
        self.assertFalse(run.json()["data"]["executed"])

        brightness = self.client.post("/api", json={
            "fun": "/shortcut/switch/bril",
            "data": {"id": "dev_1", "value": 60},
        })
        self.assertEqual(brightness.status_code, 200)
        self.assertEqual(brightness.json()["fun"], "/shortcut/brightness")
        self.assertEqual(brightness.json()["data"]["brightness"], 60)

        listed = self.client.get("/api", params={"fun": "/callback/list", "limit": 20})
        event_names = [item["event"] for item in listed.json()["data"]["events"]]
        self.assertIn("config_saved", event_names)
        self.assertIn("user_saved", event_names)
        self.assertIn("user_switched", event_names)
        self.assertIn("shortcut_saved", event_names)
        self.assertIn("shortcut_run", event_names)
        self.assertIn("shortcut_brightness", event_names)

    def test_batch_click_reports_per_device_errors(self):
        self.client.post("/api", json={"fun": "/device/register", "data": {"id": "dev_1"}})
        self.client.post("/api", json={"fun": "/device/register", "data": {"id": "dev_2"}})

        response = self.client.post("/api", json={
            "fun": "/batch/click",
            "data": {"ids": ["dev_1", "dev_2"], "x": 10, "y": 20},
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertFalse(data["ok"])
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["failure_count"], 2)
        self.assertEqual([item["id"] for item in data["results"]], ["dev_1", "dev_2"])
        self.assertIn("hardware not connected", data["results"][0]["error"])

    def test_batch_click_requires_device_ids(self):
        response = self.client.post("/api", json={
            "fun": "/batch/click",
            "data": {"x": 10, "y": 20},
        })

        self.assertEqual(response.status_code, 400)
        body = response.json()
        self.assertEqual(body["fun"], "/batch/click")
        self.assertEqual(body["data"]["code"], 400)

    def test_group_save_list_remove(self):
        response = self.client.post("/api", json={
            "fun": "/group/save",
            "data": {"name": "g1", "ids": ["dev_1", "dev_2", "dev_1"]},
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["group"]["device_ids"], ["dev_1", "dev_2"])

        response = self.client.get("/api", params={"fun": "/group/list"})
        self.assertEqual(response.status_code, 200)
        groups = response.json()["data"]["groups"]
        self.assertEqual(groups, [{"name": "g1", "device_ids": ["dev_1", "dev_2"], "count": 2}])

        response = self.client.post("/api", json={
            "fun": "/group/remove",
            "data": {"name": "g1"},
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["data"]["removed"])

    def test_batch_click_accepts_group_name(self):
        self.client.post("/api", json={"fun": "/device/register", "data": {"id": "dev_1"}})
        self.client.post("/api", json={"fun": "/device/register", "data": {"id": "dev_2"}})
        self.client.post("/api", json={
            "fun": "/group/save",
            "data": {"name": "g1", "ids": ["dev_1", "dev_2"]},
        })

        response = self.client.post("/api", json={
            "fun": "/batch/click",
            "data": {"group": "g1", "x": 10, "y": 20},
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["count"], 2)
        self.assertEqual([item["id"] for item in data["results"]], ["dev_1", "dev_2"])

    def test_batch_click_unknown_group_returns_not_found(self):
        response = self.client.post("/api", json={
            "fun": "/batch/click",
            "data": {"group": "missing", "x": 10, "y": 20},
        })

        self.assertEqual(response.status_code, 404)
        body = response.json()
        self.assertEqual(body["fun"], "/batch/click")
        self.assertEqual(body["data"]["code"], 404)
        self.assertIn("Group missing not found", body["message"])

    def test_calibration_save_get_list(self):
        response = self.client.post("/api", json={
            "fun": "/calibration/set",
            "data": {
                "id": "dev_1",
                "calibration": {
                    "enabled": True,
                    "source_width": 200,
                    "source_height": 300,
                    "active_width": 200,
                    "active_height": 300,
                    "target_width": 1000,
                    "target_height": 2000,
                },
            },
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["calibration"]["target_width"], 1000)

        response = self.client.post("/api", json={
            "fun": "/calibration/get",
            "data": {"id": "dev_1"},
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["data"]["calibration"]["enabled"])

        response = self.client.get("/api", params={"fun": "/calibration/list"})
        self.assertEqual(response.status_code, 200)
        rows = response.json()["data"]["calibrations"]
        self.assertEqual(rows[0]["device_id"], "dev_1")

    def test_profile_save_get_list_and_device_status(self):
        self.client.post("/api", json={"fun": "/device/register", "data": {"id": "dev_1"}})

        response = self.client.post("/api", json={
            "fun": "/metadata/set",
            "data": {
                "id": "dev_1",
                "metadata": {
                    "receiver_provider": "uxplay",
                    "capture_method": "window",
                    "hid_provider": "ch9329",
                    "hid_id": "hid01",
                    "serial_port": "COM3",
                    "iphone_id": "ip01",
                    "ios_version": "17.7",
                },
            },
        })
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["fun"], "/profile/set")
        self.assertEqual(body["data"]["profile"]["receiver_provider"], "uxplay")

        response = self.client.post("/api", json={
            "fun": "/profile/get",
            "data": {"id": "dev_1"},
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["profile"]["ios_version"], "17.7")

        response = self.client.get("/api", params={"fun": "/metadata/list"})
        self.assertEqual(response.status_code, 200)
        rows = response.json()["data"]["profiles"]
        self.assertEqual(rows[0]["device_id"], "dev_1")

        response = self.client.get("/api", params={"fun": "/dev/list"})
        device = response.json()["data"]["devices"][0]
        self.assertEqual(device["component_metadata"]["hid_provider"], "ch9329")
        self.assertEqual(device["iphone_id"], "ip01")

    def test_xp_find_colors_alias_returns_anchor(self):
        dev = manager.register("dev_1")
        image = Image.new("RGB", (80, 60), (0, 0, 0))
        image.putpixel((30, 20), (200, 100, 10))
        image.putpixel((35, 20), (210, 110, 20))
        dev.capture = FakeCapture(image)

        response = self.client.post("/api", json={
            "fun": "/pic/find-colors",
            "data": {
                "id": "dev_1",
                "points": [
                    {"dx": 0, "dy": 0, "color": [200, 100, 10]},
                    {"dx": 5, "dy": 0, "color": [210, 110, 20]},
                ],
                "tolerance": 0,
                "region": [25, 15, 20, 20],
            },
        })

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["fun"], "/pic/find_colors")
        self.assertTrue(body["data"]["found"])
        self.assertEqual(body["data"]["x"], 30)
        self.assertEqual(body["data"]["y"], 20)
        self.assertEqual(body["data"]["points"][0]["color"], [200, 100, 10])

    def test_xp_screenshot_supports_rect_jpg_and_save_path(self):
        dev = manager.register("dev_1")
        image = Image.new("RGB", (20, 12), (10, 20, 30))
        image.putpixel((3, 2), (200, 10, 20))
        dev.capture = FakeCapture(image)

        with TemporaryDirectory(dir=Path.cwd()) as tmp:
            save_path = Path(tmp) / "shot.jpg"
            response = self.client.post("/api", json={
                "fun": "/pic/screenshot",
                "msgid": 31,
                "data": {
                    "id": "dev_1",
                    "rect": [2, 1, 10, 7],
                    "jpg": True,
                    "save_path": str(save_path),
                },
            })

            self.assertEqual(response.status_code, 200)
            body = response.json()
            data = body["data"]
            self.assertEqual(body["fun"], "/pic/screenshot")
            self.assertEqual(body["msgid"], 31)
            self.assertEqual(data["format"], "jpg")
            self.assertEqual(data["width"], 8)
            self.assertEqual(data["height"], 6)
            self.assertEqual(data["source_width"], 20)
            self.assertEqual(data["source_height"], 12)
            self.assertEqual(data["rect"], [2, 1, 10, 7])
            self.assertEqual(data["image"], str(save_path.resolve()))
            self.assertTrue(save_path.exists())
            self.assertTrue(save_path.read_bytes().startswith(b"\xff\xd8"))
            self.assertNotIn("base64", data)

    def test_xp_screenshot_binary_response(self):
        dev = manager.register("dev_1")
        dev.capture = FakeCapture(Image.new("RGB", (8, 6), (1, 2, 3)))

        response = self.client.get("/api", params={
            "fun": "/pic/screenshot",
            "msgid": 32,
            "id": "dev_1",
            "binary": "true",
            "jpg": "true",
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "image/jpeg")
        self.assertEqual(response.headers["x-imouse-fun"], "/pic/screenshot")
        self.assertEqual(response.headers["x-imouse-msgid"], "32")
        self.assertTrue(response.content.startswith(b"\xff\xd8"))

    def test_xp_screenshot_accepts_multipart_form_fields(self):
        dev = manager.register("dev_1")
        dev.capture = FakeCapture(Image.new("RGB", (20, 12), (9, 8, 7)))

        response = self.client.post("/api", files={
            "fun": (None, "/pic/screenshot"),
            "msgid": (None, "33"),
            "id": (None, "dev_1"),
            "region": (None, "1,2,5,4"),
        })

        self.assertEqual(response.status_code, 200)
        body = response.json()
        data = body["data"]
        self.assertEqual(body["msgid"], 33)
        self.assertEqual(data["format"], "png")
        self.assertEqual(data["width"], 5)
        self.assertEqual(data["height"], 4)
        self.assertEqual(data["rect"], [1, 2, 6, 6])
        self.assertIn("base64", data)


if __name__ == "__main__":
    unittest.main()
