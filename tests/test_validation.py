import json
import tempfile
import unittest
from pathlib import Path

from imouse.validation import (
    ValidationRecorder,
    failure_category,
    json_safe,
    normalize_device_ids,
    safe_token,
)


class ValidationRecorderTest(unittest.TestCase):
    def test_safe_token_and_device_ids(self):
        self.assertEqual(safe_token(" pilot 4 "), "pilot_4")
        self.assertEqual(safe_token(""), "run")
        self.assertEqual(
            normalize_device_ids(["dev_1", "dev_1", " ", "dev_2"]),
            ["dev_1", "dev_2"],
        )

    def test_json_safe_truncates_long_strings(self):
        value = json_safe({"base64": "x" * 12}, string_limit=5)

        self.assertEqual(value["base64"], "xxxxx...<truncated 7 chars>")

    def test_append_load_summary_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder(" run:1 ", evidence_dir=Path(tmp))
            event = recorder.append(
                "Click",
                "pass",
                device_ids=["dev_1", "dev_1"],
                details={"x": 10, "y": 20},
            )
            recorder.append(
                "Swipe",
                "fail",
                device_ids=["dev_2"],
                details={"error": "hardware not connected"},
                artifacts=["screenshots/dev_2_fail.png"],
            )

            self.assertEqual(event["run_id"], "run_1")
            self.assertEqual(event["device_ids"], ["dev_1"])
            lines = recorder.path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[0])["step"], "Click")

            summary = recorder.summary()
            self.assertEqual(summary["total"], 2)
            self.assertEqual(summary["by_status"]["pass"], 1)
            self.assertEqual(summary["by_status"]["fail"], 1)
            self.assertEqual(summary["by_device"], {"dev_1": 1, "dev_2": 1})
            self.assertEqual(summary["by_failure_category"], {"hid": 1})
            self.assertEqual(summary["failures"][0]["step"], "Swipe")

            report = recorder.write_summary_markdown()
            text = report.read_text(encoding="utf-8")
            self.assertIn("# Validation Run run_1", text)
            self.assertIn("Swipe", text)
            self.assertIn("category=hid", text)
            self.assertIn("screenshots/dev_2_fail.png", text)
            self.assertIn("## Recommendations", text)

    def test_failure_category_prefers_explicit_category(self):
        event = {"step": "Click", "details": {"category": "airplay_stream", "error": "hid text ignored"}}

        self.assertEqual(failure_category(event), "airplay_stream")

    def test_summary_includes_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("metrics", evidence_dir=Path(tmp))
            recorder.append(
                "system metrics",
                "info",
                details={
                    "label": "round-1",
                    "platform": {"system": "Windows"},
                    "python": {"version": "3.13.9"},
                    "cpu": {"count": 8},
                    "memory": {"source": "test", "used_percent": 86.5, "process_rss_bytes": 123},
                    "disk": {"used_percent": 91.0},
                    "extra": {"online_count": 4},
                },
            )

            summary = recorder.summary()
            self.assertEqual(summary["metrics"]["count"], 1)
            self.assertEqual(summary["metrics"]["latest"]["label"], "round-1")
            self.assertEqual(summary["metrics"]["max_memory_used_percent"], 86.5)
            self.assertTrue(any("Host memory pressure" in item for item in summary["recommendations"]))

    def test_route_decision_failure_has_specific_recommendation(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("route_fail", evidence_dir=Path(tmp))
            recorder.append(
                "route decision component metadata",
                "fail",
                device_ids=["dev_1"],
                details={"failure_category": "route_decision", "open_blockers": ["uxplay missing"]},
            )

            summary = recorder.summary()

            self.assertEqual(summary["by_failure_category"], {"route_decision": 1})
            self.assertTrue(any("fresh run_id" in item for item in summary["recommendations"]))


if __name__ == "__main__":
    unittest.main()
