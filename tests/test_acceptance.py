import tempfile
import unittest
from pathlib import Path

from imouse.acceptance import (
    acceptance_gap_brief,
    acceptance_gap_rows,
    evaluate_acceptance,
    main,
    write_acceptance_gap_markdown,
    write_acceptance_markdown,
)
from imouse.validation import ValidationRecorder


def append_metrics(recorder: ValidationRecorder, online_count: int) -> None:
    recorder.append(
        "system metrics",
        "info",
        details={
            "label": "round-1",
            "platform": {"system": "Windows"},
            "python": {"version": "3.13.9"},
            "cpu": {"count": 8},
            "memory": {"source": "test", "used_percent": 40.0},
            "disk": {"used_percent": 50.0},
            "extra": {"online_count": online_count},
        },
    )


def append_component_metadata(recorder: ValidationRecorder, device_ids: list[str]) -> None:
    recorder.append(
        "component metadata",
        "pass",
        device_ids=device_ids,
        details={
            "device_ids": device_ids,
            "receiver_provider": "uxplay",
            "receiver_name": "imouse-dev-01",
            "receiver_version": "test",
            "capture_method": "window",
            "hid_provider": "ch9329",
            "hid_id": "hid01",
            "serial_port": "COM3",
            "iphone_id": "ip01",
            "ios_version": "17.7",
        },
    )


class AcceptanceTest(unittest.TestCase):
    def test_p1_acceptance_passes_with_manual_and_screenshot_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("p1", evidence_dir=Path(tmp))
            append_component_metadata(recorder, ["dev_1"])
            recorder.append(
                "screenshot",
                "pass",
                device_ids=["dev_1"],
                details={"screenshot_quality": {"ok": True, "reason": "ok"}},
            )
            recorder.append(
                "manual click observation",
                "pass",
                device_ids=["dev_1"],
                details={"manual": True, "note": "iPhone responded"},
            )

            report = evaluate_acceptance(recorder.path, gate="p1")

            self.assertTrue(report["ok"])
            self.assertTrue(all(item["status"] == "pass" for item in report["checks"]))

    def test_p1_acceptance_fails_without_manual_observation(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("p1_missing_manual", evidence_dir=Path(tmp))
            append_component_metadata(recorder, ["dev_1"])
            recorder.append(
                "screenshot",
                "pass",
                device_ids=["dev_1"],
                details={"screenshot_quality": {"ok": True, "reason": "ok"}},
            )

            report = evaluate_acceptance(recorder.path, gate="p1")

            self.assertFalse(report["ok"])
            failed_names = [item["name"] for item in report["checks"] if item["status"] == "fail"]
            self.assertEqual(failed_names, ["manual_observation"])

    def test_p3_acceptance_requires_four_devices_and_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("p3", evidence_dir=Path(tmp))
            append_component_metadata(recorder, ["dev_1", "dev_2", "dev_3", "dev_4"])
            append_metrics(recorder, online_count=4)
            recorder.append(
                "manual group observation",
                "pass",
                device_ids=["dev_1", "dev_2", "dev_3", "dev_4"],
                details={"manual": True, "note": "all four devices responded"},
            )

            report = evaluate_acceptance(recorder.path, gate="p3")

            self.assertTrue(report["ok"])
            self.assertEqual(report["criteria"]["min_devices"], 4)

    def test_p3_acceptance_fails_when_device_traceability_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("p3_missing_devices", evidence_dir=Path(tmp))
            append_component_metadata(recorder, ["dev_1"])
            append_metrics(recorder, online_count=4)
            recorder.append(
                "manual group observation",
                "pass",
                device_ids=["dev_1"],
                details={"manual": True, "note": "only one device id recorded"},
            )

            report = evaluate_acceptance(recorder.path, gate="p3")

            self.assertFalse(report["ok"])
            failed_names = [item["name"] for item in report["checks"] if item["status"] == "fail"]
            self.assertIn("device_traceability", failed_names)

    def test_p1_acceptance_fails_without_component_traceability(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("p1_missing_components", evidence_dir=Path(tmp))
            recorder.append(
                "screenshot",
                "pass",
                device_ids=["dev_1"],
                details={"screenshot_quality": {"ok": True, "reason": "ok"}},
            )
            recorder.append("manual", "pass", device_ids=["dev_1"], details={"manual": True})

            report = evaluate_acceptance(recorder.path, gate="p1")

            self.assertFalse(report["ok"])
            failed_names = [item["name"] for item in report["checks"] if item["status"] == "fail"]
            self.assertIn("component_traceability", failed_names)

    def test_p1_acceptance_rejects_placeholder_component_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("p1_placeholder_components", evidence_dir=Path(tmp))
            append_component_metadata(recorder, ["dev_1"])
            recorder.append(
                "bad receiver metadata",
                "pass",
                device_ids=["dev_1"],
                details={"receiver_provider": "EDIT_ME"},
            )
            recorder.append(
                "screenshot",
                "pass",
                device_ids=["dev_1"],
                details={"screenshot_quality": {"ok": True, "reason": "ok"}},
            )
            recorder.append("manual", "pass", device_ids=["dev_1"], details={"manual": True})

            report = evaluate_acceptance(recorder.path, gate="p1")

            self.assertFalse(report["ok"])
            check = next(item for item in report["checks"] if item["name"] == "component_traceability")
            self.assertTrue(check["details"]["placeholder_hits"])

    def test_main_writes_markdown_and_returns_nonzero_on_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("fail", evidence_dir=Path(tmp))
            recorder.append("manual fail", "fail", details={"manual": True, "category": "hid"})
            out = Path(tmp) / "acceptance.md"

            code = main([str(recorder.path), "--gate", "p1", "--markdown", str(out)])

            self.assertEqual(code, 1)
            self.assertIn("Acceptance Gate P1", out.read_text(encoding="utf-8"))

    def test_acceptance_gap_rows_map_failed_checks_to_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("gap", evidence_dir=Path(tmp))
            recorder.append("manual fail", "fail", details={"manual": True, "category": "hid"})
            report = evaluate_acceptance(recorder.path, gate="p1")

            rows = acceptance_gap_rows(report)
            brief = acceptance_gap_brief(report)

            names = [row["check"] for row in rows]
            self.assertIn("no_fail_events", names)
            self.assertIn("component_traceability", names)
            self.assertIn("Acceptance gap P1", brief)
            self.assertTrue(all(row["gui"] for row in rows))

    def test_write_acceptance_gap_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("gap_doc", evidence_dir=Path(tmp))
            report = evaluate_acceptance(recorder.path, gate="p1")
            out = write_acceptance_gap_markdown(report, Path(tmp) / "gap.md")
            text = out.read_text(encoding="utf-8")

            self.assertIn("Acceptance Evidence Gap P1", text)
            self.assertIn("evidence_exists", text)
            self.assertIn("does not write evidence", text)
            self.assertIn("Real iOS control verified: `False`", text)

    def test_main_writes_gap_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("gap_cli", evidence_dir=Path(tmp))
            out = Path(tmp) / "gap.md"

            code = main([str(recorder.path), "--gate", "p1", "--gap-markdown", str(out)])

            self.assertEqual(code, 1)
            self.assertIn("Acceptance Evidence Gap P1", out.read_text(encoding="utf-8"))

    def test_write_acceptance_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("p1", evidence_dir=Path(tmp))
            append_component_metadata(recorder, ["dev_1"])
            recorder.append(
                "screenshot",
                "pass",
                device_ids=["dev_1"],
                details={"screenshot_quality": {"ok": True}},
            )
            recorder.append("manual", "pass", device_ids=["dev_1"], details={"manual": True})
            report = evaluate_acceptance(recorder.path, gate="p1")
            out = write_acceptance_markdown(report, Path(tmp) / "gate.md")

            text = out.read_text(encoding="utf-8")
            self.assertIn("Result: PASS", text)
            self.assertIn("manual_observation", text)


if __name__ == "__main__":
    unittest.main()
