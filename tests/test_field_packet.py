import tempfile
import unittest
from pathlib import Path

from imouse.field_packet import (
    build_field_packet,
    main,
    write_field_packet_markdown,
)


FAKE_DOCTOR_OK = {
    "overall": "ok",
    "counts": {"ok": 1, "warn": 0, "fail": 0},
    "checks": [{"name": "python", "status": "ok", "message": "ok", "details": {}}],
}


class FieldPacketTest(unittest.TestCase):
    def test_build_packet_defaults_p3_devices_and_scripts(self):
        packet = build_field_packet(
            stage="p3",
            run_id="pilot_4_test",
            doctor_report=FAKE_DOCTOR_OK,
            run_doctor_check=False,
        )

        self.assertEqual(packet["devices"], ["dev_1", "dev_2", "dev_3", "dev_4"])
        self.assertIn("scripts/p3_pilot4_30min_watchdog.json", packet["scripts"])
        self.assertFalse(packet["readiness"]["ok"])
        blocker_names = [item["name"] for item in packet["readiness"]["blockers"]]
        self.assertIn("field_evidence", blocker_names)

    def test_write_markdown_includes_commands_and_no_success_claim(self):
        packet = build_field_packet(
            stage="p1",
            run_id="p1_test",
            devices=["dev_9"],
            doctor_report=FAKE_DOCTOR_OK,
            run_doctor_check=False,
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            write_field_packet_markdown(packet, path)
            text = path.read_text(encoding="utf-8")

        self.assertIn("# iMouse Field Execution Packet P1", text)
        self.assertIn("scripts/p1_single_device_control_probe.json", text)
        self.assertIn("scripts/p1_receiver_capture_probe.json", text)
        self.assertIn("docs/mainstream_route_decision.md", text)
        self.assertIn("docs/operator_worksheet.md", text)
        self.assertIn("docs/xp_gap_audit.md", text)
        self.assertIn("imouse.operator_worksheet --stage p1 --run-id p1_test --devices dev_9", text)
        self.assertIn("imouse.route_decision validate evidence\\p1_test_route_decision.json --require-ready", text)
        self.assertIn("imouse.xp_gap_audit --target p1 --run-id p1_test", text)
        self.assertIn("imouse.doctor --route-decision evidence\\p1_test_route_decision.json", text)
        self.assertIn("--record-evidence evidence\\p1_test.jsonl", text)
        self.assertIn("docs/xp_parity_matrix.md", text)
        self.assertIn("imouse.acceptance evidence\\p1_test.jsonl --gate p1", text)
        self.assertIn("This packet is an execution checklist, not proof of real iOS control.", text)
        self.assertIn("dev_9", text)

    def test_main_writes_output_without_running_doctor(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            code = main([
                "--stage", "p1",
                "--run-id", "cli_test",
                "--devices", "dev_1,dev_2,dev_1",
                "--skip-doctor",
                "--output", str(path),
            ])

            self.assertEqual(code, 0)
            text = path.read_text(encoding="utf-8")
            self.assertIn("Run ID: `cli_test`", text)
            self.assertIn("Devices: `dev_1, dev_2`", text)


if __name__ == "__main__":
    unittest.main()
