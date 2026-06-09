import json
import unittest

from imouse.xp_client import XpApiClient, XpApiError


class FakeResponse:
    def __init__(self, payload, status=200):
        self.payload = payload
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class FakeBinaryResponse:
    def __init__(self, content, status=200, headers=None):
        self.content = content
        self.status = status
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self.content


class XpApiClientTest(unittest.TestCase):
    def test_call_posts_fun_payload(self):
        captured = {}

        def transport(req, timeout):
            captured["url"] = req.full_url
            captured["timeout"] = timeout
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return FakeResponse({
                "status": 200,
                "message": "成功",
                "data": {"code": 0, "devices": []},
                "msgid": captured["body"]["msgid"],
                "fun": captured["body"]["fun"],
            })

        client = XpApiClient("http://127.0.0.1:9911", timeout=3, transport=transport)
        body = client.call("/device/list")

        self.assertEqual(captured["url"], "http://127.0.0.1:9911/api")
        self.assertEqual(captured["timeout"], 3)
        self.assertEqual(captured["body"]["fun"], "/device/list")
        self.assertEqual(body["data"]["devices"], [])

    def test_register_device_helper_uses_xp_id(self):
        captured = {}

        def transport(req, _timeout):
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return FakeResponse({
                "status": 200,
                "message": "成功",
                "data": {"code": 0, "id": "dev_1", "device_id": "dev_1"},
                "msgid": captured["body"]["msgid"],
                "fun": captured["body"]["fun"],
            })

        client = XpApiClient(transport=transport)
        data = client.register_device("dev_1")

        self.assertEqual(captured["body"]["fun"], "/device/register")
        self.assertEqual(captured["body"]["data"]["id"], "dev_1")
        self.assertEqual(data["device_id"], "dev_1")

    def test_error_response_raises(self):
        def transport(_req, _timeout):
            return FakeResponse({
                "status": 404,
                "message": "Unsupported XP fun",
                "data": {"code": 404},
                "msgid": 1,
                "fun": "/bad",
            }, status=404)

        client = XpApiClient(transport=transport)

        with self.assertRaises(XpApiError) as ctx:
            client.call("/bad")

        self.assertEqual(ctx.exception.status, 404)
        self.assertEqual(ctx.exception.fun, "/bad")

    def test_find_image_helper_payload(self):
        captured = {}

        def transport(req, _timeout):
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return FakeResponse({
                "status": 200,
                "message": "成功",
                "data": {"code": 0, "found": True, "x": 10, "y": 20},
                "msgid": captured["body"]["msgid"],
                "fun": captured["body"]["fun"],
            })

        client = XpApiClient(transport=transport)
        data = client.find_image("dev_1", "templates/button.png", 0.85, region=[10, 20, 300, 120])

        self.assertEqual(captured["body"]["fun"], "/pic/find-image")
        self.assertEqual(captured["body"]["data"]["id"], "dev_1")
        self.assertEqual(captured["body"]["data"]["template_path"], "templates/button.png")
        self.assertEqual(captured["body"]["data"]["threshold"], 0.85)
        self.assertEqual(captured["body"]["data"]["region"], [10, 20, 300, 120])
        self.assertTrue(data["found"])

    def test_screenshot_helper_payload(self):
        captured = {}

        def transport(req, _timeout):
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return FakeResponse({
                "status": 200,
                "message": "鎴愬姛",
                "data": {
                    "code": 0,
                    "format": "jpg",
                    "image": "evidence/shot.jpg",
                    "width": 100,
                    "height": 200,
                },
                "msgid": captured["body"]["msgid"],
                "fun": captured["body"]["fun"],
            })

        client = XpApiClient(transport=transport)
        data = client.screenshot(
            "dev_1",
            rect=[1, 2, 101, 202],
            save_path="evidence/shot.jpg",
            jpg=True,
        )

        self.assertEqual(captured["body"]["fun"], "/pic/screenshot")
        self.assertEqual(captured["body"]["data"]["id"], "dev_1")
        self.assertEqual(captured["body"]["data"]["rect"], [1, 2, 101, 202])
        self.assertEqual(captured["body"]["data"]["save_path"], "evidence/shot.jpg")
        self.assertTrue(captured["body"]["data"]["jpg"])
        self.assertNotIn("binary", captured["body"]["data"])
        self.assertEqual(data["format"], "jpg")

    def test_screenshot_bytes_returns_raw_image_payload(self):
        captured = {}
        image = b"\xff\xd8fake-jpeg"

        def transport(req, _timeout):
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return FakeBinaryResponse(
                image,
                headers={"content-type": "image/jpeg"},
            )

        client = XpApiClient(transport=transport)
        data = client.screenshot_bytes(
            "dev_1",
            rect=[1, 2, 101, 202],
            save_path="evidence/shot.jpg",
            jpg=True,
        )

        self.assertEqual(data, image)
        self.assertEqual(captured["body"]["fun"], "/pic/screenshot")
        self.assertEqual(captured["body"]["data"]["id"], "dev_1")
        self.assertEqual(captured["body"]["data"]["rect"], [1, 2, 101, 202])
        self.assertEqual(captured["body"]["data"]["save_path"], "evidence/shot.jpg")
        self.assertTrue(captured["body"]["data"]["jpg"])
        self.assertTrue(captured["body"]["data"]["binary"])

    def test_screenshot_binary_flag_uses_raw_endpoint(self):
        def transport(_req, _timeout):
            return FakeBinaryResponse(b"\x89PNG\r\n")

        client = XpApiClient(transport=transport)
        data = client.screenshot("dev_1", binary=True)

        self.assertEqual(data, b"\x89PNG\r\n")

    def test_screenshot_bytes_http_error_raises_json_payload(self):
        def transport(_req, _timeout):
            return FakeBinaryResponse(json.dumps({
                "status": 404,
                "message": "No such device",
                "data": {"code": 404},
                "msgid": 1,
                "fun": "/pic/screenshot",
            }).encode("utf-8"), status=404)

        client = XpApiClient(transport=transport)

        with self.assertRaises(XpApiError) as ctx:
            client.screenshot_bytes("missing")

        self.assertEqual(ctx.exception.status, 404)
        self.assertEqual(ctx.exception.fun, "/pic/screenshot")
        self.assertEqual(ctx.exception.payload["message"], "No such device")

    def test_find_color_helper_payload(self):
        captured = {}

        def transport(req, _timeout):
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return FakeResponse({
                "status": 200,
                "message": "成功",
                "data": {"code": 0, "found": True, "x": 7, "y": 8},
                "msgid": captured["body"]["msgid"],
                "fun": captured["body"]["fun"],
            })

        client = XpApiClient(transport=transport)
        data = client.find_color("dev_1", [255, 0, 0], tolerance=9, region=[1, 2, 3, 4])

        self.assertEqual(captured["body"]["fun"], "/pic/find_color")
        self.assertEqual(captured["body"]["data"]["color"], [255, 0, 0])
        self.assertEqual(captured["body"]["data"]["tolerance"], 9)
        self.assertEqual(captured["body"]["data"]["region"], [1, 2, 3, 4])
        self.assertTrue(data["found"])

    def test_find_colors_helper_payload(self):
        captured = {}

        def transport(req, _timeout):
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return FakeResponse({
                "status": 200,
                "message": "成功",
                "data": {"code": 0, "found": True, "x": 7, "y": 8},
                "msgid": captured["body"]["msgid"],
                "fun": captured["body"]["fun"],
            })

        points = [
            {"dx": 0, "dy": 0, "color": [255, 0, 0]},
            {"dx": 5, "dy": 0, "color": [0, 255, 0]},
        ]
        client = XpApiClient(transport=transport)
        data = client.find_colors("dev_1", points, tolerance=9, region=[1, 2, 3, 4])

        self.assertEqual(captured["body"]["fun"], "/pic/find_colors")
        self.assertEqual(captured["body"]["data"]["points"], points)
        self.assertEqual(captured["body"]["data"]["tolerance"], 9)
        self.assertEqual(captured["body"]["data"]["region"], [1, 2, 3, 4])
        self.assertTrue(data["found"])

    def test_ocr_and_find_text_helpers(self):
        calls = []

        def transport(req, _timeout):
            body = json.loads(req.data.decode("utf-8"))
            calls.append(body)
            return FakeResponse({
                "status": 200,
                "message": "成功",
                "data": {"code": 0},
                "msgid": body["msgid"],
                "fun": body["fun"],
            })

        client = XpApiClient(transport=transport)
        client.ocr("dev_1")
        client.find_text("dev_1", "设置", case_sensitive=True)

        self.assertEqual(calls[0]["fun"], "/pic/ocr")
        self.assertEqual(calls[1]["fun"], "/pic/find-text")
        self.assertEqual(calls[1]["data"]["text"], "设置")
        self.assertTrue(calls[1]["data"]["case_sensitive"])

    def test_batch_helpers_payload(self):
        calls = []

        def transport(req, _timeout):
            body = json.loads(req.data.decode("utf-8"))
            calls.append(body)
            return FakeResponse({
                "status": 200,
                "message": "成功",
                "data": {"code": 0, "ok": False, "results": []},
                "msgid": body["msgid"],
                "fun": body["fun"],
            })

        client = XpApiClient(transport=transport)
        client.batch_click(["dev_1", "dev_2"], 10, 20)
        client.batch_swipe(["dev_1", "dev_2"], 1, 2, 3, 4)
        client.batch_type_text(["dev_1", "dev_2"], "hello")

        self.assertEqual(calls[0]["fun"], "/batch/click")
        self.assertEqual(calls[0]["data"]["ids"], ["dev_1", "dev_2"])
        self.assertEqual(calls[0]["data"]["x"], 10)
        self.assertEqual(calls[1]["fun"], "/batch/swipe")
        self.assertEqual(calls[2]["fun"], "/batch/type")
        self.assertEqual(calls[2]["data"]["text"], "hello")

    def test_group_helpers_payload(self):
        calls = []

        def transport(req, _timeout):
            body = json.loads(req.data.decode("utf-8"))
            calls.append(body)
            payloads = {
                "/group/list": {"code": 0, "groups": [{"name": "g1"}]},
                "/group/save": {"code": 0, "group": {"name": "g1", "device_ids": ["dev_1"]}},
                "/group/remove": {"code": 0, "removed": True},
                "/batch/click": {"code": 0, "ok": True, "results": []},
                "/batch/swipe": {"code": 0, "ok": True, "results": []},
                "/batch/type": {"code": 0, "ok": True, "results": []},
            }
            return FakeResponse({
                "status": 200,
                "message": "鎴愬姛",
                "data": payloads[body["fun"]],
                "msgid": body["msgid"],
                "fun": body["fun"],
            })

        client = XpApiClient(transport=transport)
        self.assertEqual(client.list_groups(), [{"name": "g1"}])
        self.assertEqual(client.save_group("g1", ["dev_1"])["name"], "g1")
        self.assertTrue(client.remove_group("g1")["removed"])
        client.group_click("g1", 10, 20)
        client.group_swipe("g1", 1, 2, 3, 4, steps=9, step_delay=0.05)
        client.group_type_text("g1", "hello")

        self.assertEqual(calls[0]["fun"], "/group/list")
        self.assertEqual(calls[1]["fun"], "/group/save")
        self.assertEqual(calls[1]["data"], {"name": "g1", "ids": ["dev_1"]})
        self.assertEqual(calls[2]["fun"], "/group/remove")
        self.assertEqual(calls[2]["data"], {"name": "g1"})
        self.assertEqual(calls[3]["fun"], "/batch/click")
        self.assertEqual(calls[3]["data"], {"group": "g1", "x": 10, "y": 20})
        self.assertEqual(calls[4]["fun"], "/batch/swipe")
        self.assertEqual(calls[4]["data"]["group"], "g1")
        self.assertEqual(calls[4]["data"]["steps"], 9)
        self.assertEqual(calls[4]["data"]["step_delay"], 0.05)
        self.assertEqual(calls[5]["fun"], "/batch/type")
        self.assertEqual(calls[5]["data"], {"group": "g1", "text": "hello"})

    def test_callback_helpers_payload(self):
        calls = []

        def transport(req, _timeout):
            body = json.loads(req.data.decode("utf-8"))
            calls.append(body)
            if body["fun"] == "/callback/list":
                payload = {
                    "code": 0,
                    "events": [{"seq": 2, "event": "device_registered"}],
                    "last_seq": 2,
                }
            elif body["fun"] == "/callback/push":
                payload = {
                    "code": 0,
                    "event": {"seq": 3, "event": body["data"]["event"], "device_id": body["data"]["id"]},
                }
            elif body["fun"] == "/callback/clear":
                payload = {
                    "code": 0,
                    "cleared": True,
                    "last_seq": 0,
                }
            else:
                raise AssertionError(body["fun"])
            return FakeResponse({
                "status": 200,
                "message": "ok",
                "data": payload,
                "msgid": body["msgid"],
                "fun": body["fun"],
            })

        client = XpApiClient(transport=transport)
        callbacks = client.list_callbacks(after_seq=1, limit=5)
        pushed = client.push_callback(
            "airplay_log",
            {"line": "connected"},
            device_id="dev_1",
            source="receiver",
            severity="warn",
        )
        cleared = client.clear_callbacks()

        self.assertEqual(callbacks["events"][0]["event"], "device_registered")
        self.assertEqual(pushed["device_id"], "dev_1")
        self.assertTrue(cleared["cleared"])
        self.assertEqual(calls[0]["fun"], "/callback/list")
        self.assertEqual(calls[0]["data"], {"after_seq": 1, "limit": 5})
        self.assertEqual(calls[1]["fun"], "/callback/push")
        self.assertEqual(calls[1]["data"]["source"], "receiver")
        self.assertEqual(calls[1]["data"]["severity"], "warn")
        self.assertEqual(calls[2]["fun"], "/callback/clear")

    def test_config_user_and_shortcut_helpers_payload(self):
        calls = []

        def transport(req, _timeout):
            body = json.loads(req.data.decode("utf-8"))
            calls.append(body)
            payloads = {
                "/config/get": {"code": 0, "config": {"theme": "field"}, "value": "field"},
                "/config/set": {"code": 0, "config": {"theme": "field", "receiver_route": "wired"}},
                "/user/list": {"code": 0, "users": [{"user_id": "op_1"}]},
                "/user/get": {"code": 0, "user": {"user_id": "op_1", "role": "operator"}},
                "/user/set": {"code": 0, "user": {"user_id": "op_1", "role": "operator"}},
                "/user/switch": {"code": 0, "user_id": "op_1", "active_user": "op_1"},
                "/user/remove": {"code": 0, "user_id": "op_1", "removed": True},
                "/shortcut/list": {"code": 0, "shortcuts": [{"name": "home"}]},
                "/shortcut/get": {"code": 0, "shortcut": {"name": "home"}},
                "/shortcut/save": {"code": 0, "shortcut": {"name": "home", "action": "key"}},
                "/shortcut/run": {"code": 0, "name": "home", "dry_run": True, "executed": False},
                "/shortcut/brightness": {"code": 0, "brightness": 55, "dry_run": True},
            }
            return FakeResponse({
                "status": 200,
                "message": "ok",
                "data": payloads[body["fun"]],
                "msgid": body["msgid"],
                "fun": body["fun"],
            })

        client = XpApiClient(transport=transport)
        self.assertEqual(client.get_config("theme")["value"], "field")
        self.assertEqual(client.set_config({"theme": "field"}, receiver_route="wired")["receiver_route"], "wired")
        self.assertEqual(client.list_users()[0]["user_id"], "op_1")
        self.assertEqual(client.get_user("op_1")["role"], "operator")
        self.assertEqual(client.save_user("op_1", {"role": "operator"})["user_id"], "op_1")
        self.assertEqual(client.switch_user("op_1")["active_user"], "op_1")
        self.assertTrue(client.remove_user("op_1")["removed"])
        self.assertEqual(client.list_shortcuts()[0]["name"], "home")
        self.assertEqual(client.get_shortcut("home")["name"], "home")
        self.assertEqual(client.save_shortcut("home", {"action": "key"})["action"], "key")
        self.assertTrue(client.run_shortcut("home", "dev_1")["dry_run"])
        self.assertEqual(client.set_brightness(55, "dev_1")["brightness"], 55)

        self.assertEqual(calls[0]["fun"], "/config/get")
        self.assertEqual(calls[0]["data"]["key"], "theme")
        self.assertEqual(calls[1]["data"]["config"]["receiver_route"], "wired")
        self.assertEqual(calls[4]["data"]["user"]["user_id"], "op_1")
        self.assertFalse(calls[4]["data"]["active"])
        self.assertEqual(calls[10]["data"]["name"], "home")
        self.assertEqual(calls[10]["data"]["id"], "dev_1")
        self.assertEqual(calls[11]["data"]["value"], 55)

    def test_calibration_helpers_payload(self):
        calls = []

        def transport(req, _timeout):
            body = json.loads(req.data.decode("utf-8"))
            calls.append(body)
            payloads = {
                "/calibration/list": {
                    "code": 0,
                    "calibrations": [{"device_id": "dev_1"}],
                },
                "/calibration/get": {
                    "code": 0,
                    "calibration": {"enabled": True, "target_width": 1000},
                },
                "/calibration/set": {
                    "code": 0,
                    "calibration": {"enabled": True, "target_width": 1000},
                },
            }
            return FakeResponse({
                "status": 200,
                "message": "鎴愬姛",
                "data": payloads[body["fun"]],
                "msgid": body["msgid"],
                "fun": body["fun"],
            })

        client = XpApiClient(transport=transport)
        self.assertEqual(client.list_calibrations(), [{"device_id": "dev_1"}])
        self.assertTrue(client.get_calibration("dev_1")["enabled"])
        self.assertEqual(
            client.set_calibration("dev_1", {"enabled": True, "target_width": 1000})["target_width"],
            1000,
        )

        self.assertEqual(calls[0]["fun"], "/calibration/list")
        self.assertEqual(calls[1]["data"], {"id": "dev_1"})
        self.assertEqual(calls[2]["fun"], "/calibration/set")
        self.assertEqual(calls[2]["data"]["id"], "dev_1")
        self.assertEqual(calls[2]["data"]["calibration"]["target_width"], 1000)

    def test_profile_helpers_payload(self):
        calls = []

        def transport(req, _timeout):
            body = json.loads(req.data.decode("utf-8"))
            calls.append(body)
            payloads = {
                "/profile/list": {
                    "code": 0,
                    "profiles": [{"device_id": "dev_1"}],
                },
                "/profile/get": {
                    "code": 0,
                    "profile": {"receiver_provider": "uxplay"},
                },
                "/profile/set": {
                    "code": 0,
                    "profile": {"receiver_provider": "uxplay", "ios_version": "17.7"},
                },
            }
            return FakeResponse({
                "status": 200,
                "message": "ok",
                "data": payloads[body["fun"]],
                "msgid": body["msgid"],
                "fun": body["fun"],
            })

        client = XpApiClient(transport=transport)
        self.assertEqual(client.list_profiles(), [{"device_id": "dev_1"}])
        self.assertEqual(client.get_profile("dev_1")["receiver_provider"], "uxplay")
        self.assertEqual(
            client.set_profile("dev_1", {"receiver_provider": "uxplay", "ios_version": "17.7"})["ios_version"],
            "17.7",
        )

        self.assertEqual(calls[0]["fun"], "/profile/list")
        self.assertEqual(calls[1]["data"], {"id": "dev_1"})
        self.assertEqual(calls[2]["fun"], "/profile/set")
        self.assertEqual(calls[2]["data"]["id"], "dev_1")
        self.assertEqual(calls[2]["data"]["profile"]["receiver_provider"], "uxplay")


if __name__ == "__main__":
    unittest.main()
