import base64
import io
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from imouse.script_runner import (
    ScriptRunner,
    ScriptRunnerError,
    StepResult,
    analyze_screenshot_base64,
    failure_screenshot_device_id,
    load_scenario,
    screenshot_evidence_details,
    template_quality_from_step,
)
from imouse.validation import ValidationRecorder
from imouse.xp_client import XpApiError


def png_base64(color=(40, 90, 180), *, stripe=True):
    image = Image.new("RGB", (24, 24), color)
    if stripe:
        for x in range(12):
            for y in range(24):
                image.putpixel((x, y), (220, 230, 240))
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


class FakeClient:
    def __init__(self):
        self.calls = []

    def call(self, fun, data=None):
        self.calls.append(("call", fun, data or {}))
        return {"data": {"code": 0, "fun": fun}}

    def click(self, device_id, x, y):
        self.calls.append(("click", device_id, x, y))
        return {"device_id": device_id, "x": x, "y": y}

    def swipe(self, device_id, x1, y1, x2, y2, steps=20, step_delay=0.01):
        self.calls.append(("swipe", device_id, x1, y1, x2, y2, steps, step_delay))
        return {"device_id": device_id}

    def type_text(self, device_id, text):
        self.calls.append(("type", device_id, text))
        return {"device_id": device_id, "text": text}

    def group_click(self, group, x, y):
        self.calls.append(("group_click", group, x, y))
        return {"group": group, "x": x, "y": y}

    def group_swipe(self, group, x1, y1, x2, y2, steps=20, step_delay=0.01):
        self.calls.append(("group_swipe", group, x1, y1, x2, y2, steps, step_delay))
        return {"group": group}

    def group_type_text(self, group, text):
        self.calls.append(("group_type", group, text))
        return {"group": group, "text": text}

    def find_image(self, device_id, template_path, threshold=0.8, region=None):
        self.calls.append(("find_image", device_id, template_path, threshold, region))
        if template_path == "missing.png":
            return {"found": False}
        return {"found": True, "x": 11, "y": 22}

    def find_color(self, device_id, color, tolerance=5, region=None):
        self.calls.append(("find_color", device_id, color, tolerance, region))
        return {"found": True, "x": 1, "y": 2}

    def find_colors(self, device_id, points, tolerance=5, region=None):
        self.calls.append(("find_colors", device_id, points, tolerance, region))
        return {"found": True, "x": 3, "y": 4}

    def screenshot(self, device_id):
        self.calls.append(("screenshot", device_id))
        return {"device_id": device_id, "base64": png_base64()}

    def ocr(self, device_id):
        self.calls.append(("ocr", device_id))
        return {"list": []}

    def find_text(self, device_id, text, case_sensitive=False):
        self.calls.append(("find_text", device_id, text, case_sensitive))
        return {"found": True, "x": 3, "y": 4}


class FailingClient(FakeClient):
    def click(self, device_id, x, y):
        raise XpApiError("hardware not connected", status=500, fun="/mouse/click")


class ScreenshotAlsoFailingClient(FailingClient):
    def screenshot(self, device_id):
        self.calls.append(("screenshot", device_id))
        raise XpApiError("capture unavailable", status=500, fun="/pic/screenshot")


class BlackScreenshotClient(FakeClient):
    def screenshot(self, device_id):
        self.calls.append(("screenshot", device_id))
        return {"device_id": device_id, "base64": png_base64((0, 0, 0), stripe=False)}


class ScriptRunnerTest(unittest.TestCase):
    def test_run_dispatches_steps_and_records_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = FakeClient()
            recorder = ValidationRecorder("scenario", evidence_dir=Path(tmp))
            runner = ScriptRunner(client=client, recorder=recorder, sleep_func=lambda _seconds: None)
            summary = runner.run({
                "name": "smoke",
                "steps": [
                    {"action": "call", "fun": "/device/list"},
                    {"action": "click", "device_id": "dev_1", "x": 10, "y": 20},
                    {"action": "find_image_then_click", "device_id": "dev_1", "template_path": "ok.png"},
                    {"action": "group_type", "group": "pilot_4", "text": "hello"},
                    {"action": "wait", "seconds": 0.01},
                    {"action": "record", "name": "manual pass", "status": "pass", "note": "observed"},
                ],
            })

            self.assertTrue(summary["ok"])
            self.assertEqual(summary["total"], 6)
            self.assertIn(("click", "dev_1", 11, 22), client.calls)
            events = recorder.load()
            self.assertEqual(events[0]["step"], "1. call")
            self.assertEqual(events[-1]["step"], "scenario summary")
            self.assertEqual(events[-1]["status"], "pass")

    def test_run_stops_on_failure_by_default(self):
        runner = ScriptRunner(client=FailingClient(), sleep_func=lambda _seconds: None)
        summary = runner.run({
            "steps": [
                {"action": "click", "device_id": "dev_1", "x": 10, "y": 20},
                {"action": "type", "device_id": "dev_1", "text": "never"},
            ],
        })

        self.assertFalse(summary["ok"])
        self.assertEqual(summary["total"], 1)
        self.assertIn("hardware not connected", summary["results"][0]["error"])

    def test_failure_auto_saves_screenshot_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = FailingClient()
            recorder = ValidationRecorder("fail_capture", evidence_dir=Path(tmp))
            runner = ScriptRunner(
                client=client,
                recorder=recorder,
                sleep_func=lambda _seconds: None,
            )
            summary = runner.run({
                "steps": [
                    {"action": "click", "device_id": "dev_1", "x": 10, "y": 20},
                ],
            })

            self.assertFalse(summary["ok"])
            event = recorder.load()[0]
            self.assertEqual(event["status"], "fail")
            self.assertEqual(event["artifacts"], [str(Path(tmp) / "fail_capture_artifacts" / "1_click_dev_1_failure.png")])
            self.assertGreater(Path(event["artifacts"][0]).stat().st_size, 0)
            self.assertIn(("screenshot", "dev_1"), client.calls)

    def test_failure_screenshot_error_is_recorded_without_hiding_original_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("fail_capture_error", evidence_dir=Path(tmp))
            runner = ScriptRunner(
                client=ScreenshotAlsoFailingClient(),
                recorder=recorder,
                sleep_func=lambda _seconds: None,
            )
            runner.run({
                "steps": [
                    {"action": "click", "device_id": "dev_1", "x": 10, "y": 20},
                ],
            })

            event = recorder.load()[0]
            self.assertIn("hardware not connected", event["details"]["error"])
            self.assertIn("capture unavailable", event["details"]["failure_screenshot_error"])
            self.assertEqual(event["artifacts"], [])

    def test_failure_screenshot_device_id_prefers_explicit_override(self):
        step_result = StepResult(1, "group click", "group_click", "fail", ["dev_1", "dev_2"])

        self.assertEqual(
            failure_screenshot_device_id(step_result, {"failure_screenshot_device_id": "dev_2"}),
            "dev_2",
        )
        self.assertEqual(failure_screenshot_device_id(step_result, {}), "")

    def test_screenshot_step_auto_saves_artifact_and_compacts_base64(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("screen_capture", evidence_dir=Path(tmp))
            runner = ScriptRunner(
                client=FakeClient(),
                recorder=recorder,
                sleep_func=lambda _seconds: None,
            )
            summary = runner.run({
                "steps": [
                    {"action": "screenshot", "device_id": "dev_1"},
                ],
            })

            self.assertTrue(summary["ok"])
            event = recorder.load()[0]
            expected = Path(tmp) / "screen_capture_artifacts" / "1_screenshot_dev_1_capture.png"
            self.assertEqual(event["artifacts"], [str(expected)])
            self.assertGreater(expected.stat().st_size, 0)
            self.assertRegex(event["details"]["base64"], r"^<saved screenshot \d+ bytes>$")
            self.assertEqual(event["details"]["screenshot_artifact"], str(expected))
            self.assertTrue(event["details"]["screenshot_quality"]["ok"])

    def test_screenshot_step_fails_on_black_screen_but_keeps_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("black_screen", evidence_dir=Path(tmp))
            runner = ScriptRunner(
                client=BlackScreenshotClient(),
                recorder=recorder,
                sleep_func=lambda _seconds: None,
            )
            summary = runner.run({
                "steps": [
                    {"action": "screenshot", "device_id": "dev_1"},
                ],
            })

            self.assertFalse(summary["ok"])
            self.assertEqual(summary["results"][0]["error"], "screenshot quality failed: black_screen")
            event = recorder.load()[0]
            self.assertEqual(event["status"], "fail")
            self.assertEqual(event["details"]["screenshot_quality"]["reason"], "black_screen")
            self.assertTrue(Path(event["artifacts"][0]).exists())

    def test_screenshot_evidence_details_records_save_error(self):
        details = screenshot_evidence_details(
            {"base64": "abc", "device_id": "dev_1"},
            [],
            "disk full",
            0,
        )

        self.assertEqual(details["base64"], "<base64 3 chars>")
        self.assertEqual(details["screenshot_artifact_error"], "disk full")

    def test_analyze_screenshot_base64_reports_invalid_and_valid_images(self):
        self.assertEqual(analyze_screenshot_base64("")["reason"], "missing_base64")
        valid = analyze_screenshot_base64(png_base64())

        self.assertTrue(valid["ok"])
        self.assertEqual(valid["width"], 24)
        self.assertGreater(valid["stddev_luma"], 1.0)

    def test_find_image_then_click_fails_when_template_missing(self):
        runner = ScriptRunner(client=FakeClient(), sleep_func=lambda _seconds: None)
        result = runner.run_step(
            {"action": "find_image_then_click", "device_id": "dev_1", "template_path": "missing.png"},
            1,
        )

        self.assertEqual(result.status, "fail")
        self.assertIn("template not found", result.error)

    def test_find_image_then_click_passes_region_to_client(self):
        client = FakeClient()
        runner = ScriptRunner(client=client, sleep_func=lambda _seconds: None)
        result = runner.run_step(
            {
                "action": "find_image_then_click",
                "device_id": "dev_1",
                "template_path": "ok.png",
                "threshold": 0.91,
                "region": [10, 20, 300, 120],
            },
            1,
        )

        self.assertEqual(result.status, "pass")
        self.assertIn(("find_image", "dev_1", "ok.png", 0.91, [10, 20, 300, 120]), client.calls)
        self.assertIn(("click", "dev_1", 11, 22), client.calls)

    def test_find_image_rejects_local_low_texture_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "flat.png"
            Image.new("RGB", (24, 24), (128, 128, 128)).save(path)
            runner = ScriptRunner(client=FakeClient(), sleep_func=lambda _seconds: None)

            result = runner.run_step(
                {"action": "find_image", "device_id": "dev_1", "template_path": str(path)},
                1,
            )

            self.assertEqual(result.status, "fail")
            self.assertIn("template quality failed: low_texture", result.error)

    def test_find_colors_passes_points_to_client(self):
        client = FakeClient()
        runner = ScriptRunner(client=client, sleep_func=lambda _seconds: None)
        points = [
            {"dx": 0, "dy": 0, "color": [255, 0, 0]},
            {"dx": 5, "dy": 0, "color": [0, 255, 0]},
        ]

        result = runner.run_step(
            {
                "action": "find_colors",
                "device_id": "dev_1",
                "points": points,
                "tolerance": 7,
                "region": [10, 20, 300, 120],
            },
            1,
        )

        self.assertEqual(result.status, "pass")
        self.assertIn(("find_colors", "dev_1", points, 7, [10, 20, 300, 120]), client.calls)

    def test_find_colors_requires_points(self):
        runner = ScriptRunner(client=FakeClient(), sleep_func=lambda _seconds: None)

        result = runner.run_step({"action": "find_colors", "device_id": "dev_1"}, 1)

        self.assertEqual(result.status, "fail")
        self.assertIn("find_colors requires a non-empty points list", result.error)

    def test_template_quality_from_step_skips_nonlocal_paths(self):
        quality = template_quality_from_step({"template_path": "missing.png"}, "missing.png")

        self.assertTrue(quality["ok"])
        self.assertEqual(quality["reason"], "not_local")

    def test_dry_run_does_not_call_client(self):
        client = FakeClient()
        runner = ScriptRunner(client=client, dry_run=True)
        summary = runner.run({"steps": [{"action": "click", "device_id": "dev_1", "x": 1, "y": 2}]})

        self.assertTrue(summary["ok"])
        self.assertEqual(client.calls, [])
        self.assertTrue(summary["results"][0]["result"]["dry_run"])

    def test_repeat_runs_nested_steps_and_waits_between_rounds(self):
        sleeps = []
        client = FakeClient()
        runner = ScriptRunner(client=client, sleep_func=sleeps.append)
        summary = runner.run({
            "steps": [
                {
                    "action": "repeat",
                    "name": "two rounds",
                    "count": 2,
                    "wait_between": 0.5,
                    "steps": [
                        {"action": "click", "device_id": "dev_1", "x": 1, "y": 2},
                        {"action": "type", "device_id": "dev_1", "text": "ok"},
                    ],
                }
            ],
        })

        self.assertTrue(summary["ok"])
        self.assertEqual(summary["total"], 1)
        repeat_result = summary["results"][0]["result"]
        self.assertEqual(repeat_result["completed_rounds"], 2)
        self.assertEqual(repeat_result["total"], 4)
        self.assertEqual(sleeps, [0.5])
        self.assertEqual(
            client.calls,
            [
                ("click", "dev_1", 1, 2),
                ("type", "dev_1", "ok"),
                ("click", "dev_1", 1, 2),
                ("type", "dev_1", "ok"),
            ],
        )

    def test_repeat_failure_stops_nested_steps_by_default(self):
        runner = ScriptRunner(client=FailingClient(), sleep_func=lambda _seconds: None)
        summary = runner.run({
            "steps": [
                {
                    "action": "repeat",
                    "count": 2,
                    "steps": [
                        {"action": "click", "device_id": "dev_1", "x": 1, "y": 2},
                        {"action": "type", "device_id": "dev_1", "text": "never"},
                    ],
                }
            ],
        })

        self.assertFalse(summary["ok"])
        repeat_result = summary["results"][0]["result"]
        self.assertTrue(repeat_result["stopped_early"])
        self.assertEqual(repeat_result["completed_rounds"], 1)
        self.assertEqual(repeat_result["failure_count"], 1)
        self.assertIn("hardware not connected", repeat_result["rounds"][0]["results"][0]["error"])

    def test_repeat_records_nested_steps(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("repeat", evidence_dir=Path(tmp))
            runner = ScriptRunner(
                client=FakeClient(),
                recorder=recorder,
                sleep_func=lambda _seconds: None,
            )
            summary = runner.run({
                "steps": [
                    {
                        "action": "repeat",
                        "name": "repeat smoke",
                        "count": 2,
                        "steps": [
                            {"action": "click", "device_id": "dev_1", "x": 1, "y": 2},
                        ],
                    }
                ],
            })

            self.assertTrue(summary["ok"])
            steps = [event["step"] for event in recorder.load()]
            self.assertIn("1.1.1. click", steps)
            self.assertIn("1.2.1. click", steps)
            self.assertIn("1. repeat smoke", steps)

    def test_metrics_step_records_system_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("metrics", evidence_dir=Path(tmp))
            runner = ScriptRunner(
                client=FakeClient(),
                recorder=recorder,
                sleep_func=lambda _seconds: None,
            )
            summary = runner.run({
                "steps": [
                    {
                        "action": "metrics",
                        "name": "round metrics",
                        "label": "round-1",
                        "extra": {"online_count": 1},
                    }
                ],
            })

            self.assertTrue(summary["ok"])
            result = summary["results"][0]["result"]
            self.assertEqual(result["label"], "round-1")
            self.assertEqual(result["extra"]["online_count"], 1)
            self.assertIn("disk", result)
            event = recorder.load()[0]
            self.assertEqual(event["step"], "1. round metrics")
            self.assertEqual(event["details"]["label"], "round-1")

    def test_record_failure_keeps_manual_category_and_details(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("manual_fail", evidence_dir=Path(tmp))
            runner = ScriptRunner(
                client=FakeClient(),
                recorder=recorder,
                sleep_func=lambda _seconds: None,
            )
            summary = runner.run({
                "steps": [
                    {
                        "action": "record",
                        "name": "manual HID failure",
                        "status": "fail",
                        "category": "hid",
                        "note": "dev_1 did not move",
                        "details": {"port": "COM3"},
                    }
                ],
            })

            self.assertFalse(summary["ok"])
            event = recorder.load()[0]
            self.assertEqual(event["status"], "fail")
            self.assertEqual(event["details"]["category"], "hid")
            self.assertEqual(event["details"]["port"], "COM3")
            self.assertEqual(recorder.summary()["by_failure_category"], {"hid": 1})

    def test_record_requires_named_details(self):
        runner = ScriptRunner(client=FakeClient(), sleep_func=lambda _seconds: None)

        result = runner.run_step(
            {
                "action": "record",
                "name": "receiver metadata",
                "status": "pass",
                "required_details": ["receiver_provider", "receiver.version"],
                "details": {
                    "receiver_provider": "uxplay",
                    "receiver": {"version": ""},
                },
            },
            1,
        )

        self.assertEqual(result.status, "fail")
        self.assertIn("receiver.version", result.error)

    def test_record_rejects_placeholder_details(self):
        runner = ScriptRunner(client=FakeClient(), sleep_func=lambda _seconds: None)

        result = runner.run_step(
            {
                "action": "record",
                "name": "receiver metadata",
                "status": "pass",
                "forbid_placeholder_values": ["EDIT_ME", "provider_or_choice"],
                "details": {
                    "receiver_name": "EDIT_ME",
                    "receiver_provider": "provider_or_choice",
                },
            },
            1,
        )

        self.assertEqual(result.status, "fail")
        self.assertIn("placeholder value", result.error)
        self.assertIn("receiver_name", result.error)

    def test_record_accepts_required_details_without_placeholders(self):
        runner = ScriptRunner(client=FakeClient(), sleep_func=lambda _seconds: None)

        result = runner.run_step(
            {
                "action": "record",
                "name": "receiver metadata",
                "status": "pass",
                "required_details": ["receiver_provider", "receiver_name"],
                "forbid_placeholder_values": ["EDIT_ME"],
                "details": {
                    "receiver_provider": "uxplay",
                    "receiver_name": "imouse-dev-01",
                },
            },
            1,
        )

        self.assertEqual(result.status, "pass")

    def test_load_scenario_validates_json_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text("[]", encoding="utf-8")

            with self.assertRaises(ScriptRunnerError):
                load_scenario(path)


if __name__ == "__main__":
    unittest.main()
