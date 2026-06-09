import json
import tempfile
import unittest
from pathlib import Path

from imouse.acceptance import evaluate_acceptance
from imouse.route_decision import (
    append_decision_evidence,
    component_metadata_from_decision,
    decision_template,
    evaluate_decision,
    load_decision,
    main,
    write_decision_markdown,
)


def ready_decision() -> dict:
    data = decision_template(run_id="p1_ready", devices=["dev_1"])
    data["receiver"].update({
        "route": "uxplay",
        "name": "imouse-dev-01",
        "version": "1.70",
        "path": "C:/tools/uxplay/uxplay.exe",
        "start_command": "uxplay -n imouse-dev-01",
        "airplay_name": "imouse-dev-01",
        "capture_method": "window",
        "license_status": "open-source",
    })
    data["receiver"]["window_binding"] = {
        "title": "imouse-dev-01",
        "process": "uxplay.exe",
        "handle": "0x1234",
    }
    data["hid"].update({
        "route": "ch9329",
        "provider": "ch9329",
        "id": "hid01",
        "firmware": "ch9329-v1",
        "serial_port": "COM3",
        "baudrate": "9600",
    })
    data["iphone"].update({
        "id": "ip01",
        "model": "iPhone 13",
        "ios_version": "17.7",
        "assistive_touch": "on",
        "pointer_speed": "middle",
    })
    data["bench"].update({
        "hub_id": "hub-a",
        "hub_port": "hub-a-01",
        "cable_id": "cable-01",
        "network": "pc-wired-same-vlan",
        "operator": "field-operator",
    })
    data["decision"] = {
        "allowed_to_run_p1": True,
        "reason": "receiver and HID are both selected and traceable",
        "open_blockers": [],
    }
    return data


class RouteDecisionTest(unittest.TestCase):
    def test_template_is_not_ready_until_placeholders_are_filled(self):
        report = evaluate_decision(decision_template(run_id="p1_template"), require_ready=True)

        self.assertFalse(report["ok"])
        blocker_names = [item["name"] for item in report["blockers"]]
        self.assertIn("route_choice", blocker_names)
        self.assertIn("placeholders", blocker_names)
        self.assertIn("allowed_to_run_p1", blocker_names)
        self.assertTrue(report["claims"]["does_not_verify_real_ios_control"])

    def test_ready_decision_passes_require_ready(self):
        report = evaluate_decision(ready_decision(), require_ready=True)

        self.assertTrue(report["ok"])
        self.assertTrue(report["ready"])
        self.assertFalse(report["claims"]["has_open_blockers"])

    def test_component_metadata_maps_to_acceptance_fields(self):
        details = component_metadata_from_decision(ready_decision())

        self.assertEqual(details["receiver_provider"], "uxplay")
        self.assertEqual(details["capture_method"], "window")
        self.assertEqual(details["hid_provider"], "ch9329")
        self.assertEqual(details["hid_id"], "hid01")
        self.assertEqual(details["serial_port"], "COM3")
        self.assertEqual(details["iphone_id"], "ip01")
        self.assertEqual(details["ios_version"], "17.7")
        self.assertFalse(details["manual"])
        self.assertTrue(details["does_not_verify_real_ios_control"])

    def test_append_decision_evidence_satisfies_only_component_traceability(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = ready_decision()
            report = evaluate_decision(data, require_ready=True)
            evidence = Path(tmp) / "p1_ready.jsonl"

            append_decision_evidence(data, report, evidence)
            acceptance = evaluate_acceptance(evidence, gate="p1")

            component = next(item for item in acceptance["checks"] if item["name"] == "component_traceability")
            manual = next(item for item in acceptance["checks"] if item["name"] == "manual_observation")
            screenshot = next(item for item in acceptance["checks"] if item["name"] == "screenshot_quality")
            self.assertEqual(component["status"], "pass")
            self.assertEqual(manual["status"], "fail")
            self.assertEqual(screenshot["status"], "fail")
            self.assertFalse(acceptance["ok"])

    def test_append_failed_decision_evidence_records_fail_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = decision_template(run_id="p1_bad")
            report = evaluate_decision(data, require_ready=True)
            evidence = Path(tmp) / "p1_bad.jsonl"

            append_decision_evidence(data, report, evidence)
            acceptance = evaluate_acceptance(evidence, gate="p1")

            no_fail = next(item for item in acceptance["checks"] if item["name"] == "no_fail_events")
            self.assertEqual(no_fail["status"], "fail")

    def test_open_blockers_fail_even_when_allowed_flag_is_true(self):
        data = ready_decision()
        data["decision"]["open_blockers"] = ["uxplay not installed"]

        report = evaluate_decision(data, require_ready=True)

        self.assertFalse(report["ok"])
        self.assertFalse(report["ready"])
        self.assertIn("open_blockers", [item["name"] for item in report["blockers"]])

    def test_write_decision_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = evaluate_decision(ready_decision(), require_ready=True)
            path = write_decision_markdown(report, Path(tmp) / "route.md")

            text = path.read_text(encoding="utf-8")
            self.assertIn("P1 Route Decision Validation", text)
        self.assertIn("Ready to run P1: `True`", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("fresh run_id", text)

    def test_load_decision_accepts_utf8_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "route_bom.json"
            path.write_text("\ufeff" + json.dumps(ready_decision()), encoding="utf-8")

            data = load_decision(path)

        self.assertEqual(data["run_id"], "p1_ready")

    def test_cli_init_and_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            route_path = Path(tmp) / "route.json"
            markdown_path = Path(tmp) / "route.md"

            init_code = main([
                "init",
                "--run-id", "cli_route",
                "--devices", "dev_1,dev_2",
                "--output", str(route_path),
            ])
            self.assertEqual(init_code, 0)
            self.assertTrue(route_path.exists())
            self.assertIn("dev_2", route_path.read_text(encoding="utf-8"))

            fail_code = main(["validate", str(route_path), "--require-ready"])
            self.assertEqual(fail_code, 1)

            route_path.write_text(
                json.dumps(ready_decision(), ensure_ascii=False),
                encoding="utf-8",
            )
            evidence_path = Path(tmp) / "route_evidence.jsonl"
            pass_code = main([
                "validate",
                str(route_path),
                "--require-ready",
                "--markdown", str(markdown_path),
                "--record-evidence", str(evidence_path),
            ])
            self.assertEqual(pass_code, 0)
            self.assertTrue(markdown_path.exists())
            self.assertTrue(evidence_path.exists())


if __name__ == "__main__":
    unittest.main()
