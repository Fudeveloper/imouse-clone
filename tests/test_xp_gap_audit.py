from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from imouse.validation import ValidationRecorder
from imouse.xp_gap_audit import (
    CAPABILITY_SPECS,
    build_xp_gap_audit,
    write_xp_gap_audit_markdown,
    xp_gap_audit_brief,
)


P0_READY = {
    "target": "p1",
    "ok": False,
    "stage_status": {
        "p0": {"ok": True},
        "p1": {"ok": False},
        "p2": {"ok": False},
        "p3": {"ok": False},
        "p4": {"ok": False},
    },
    "blockers": [{"name": "field_evidence"}],
    "claims": {"real_ios_control_verified": False, "ios_group_control_verified": False},
}

P1_READY = {
    "target": "p1",
    "ok": True,
    "stage_status": {
        "p0": {"ok": True},
        "p1": {"ok": True},
        "p2": {"ok": False},
        "p3": {"ok": False},
        "p4": {"ok": False},
    },
    "blockers": [],
    "claims": {"real_ios_control_verified": True, "ios_group_control_verified": False},
}


def create_declared_assets(root: Path) -> None:
    assets = set()
    for spec in CAPABILITY_SPECS:
        assets.update(spec.implemented_assets)
    for relative in assets:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("ok", encoding="utf-8")


def append_p1_evidence(recorder: ValidationRecorder) -> None:
    recorder.append(
        "Component metadata",
        "pass",
        device_ids=["dev_1"],
        details={
            "device_id": "dev_1",
            "receiver_provider": "uxplay",
            "capture_method": "window",
            "hid_provider": "ch9329",
            "hid_id": "hid01",
            "serial_port": "COM3",
            "iphone_id": "iphone01",
            "ios_version": "17.7",
        },
    )
    recorder.append(
        "Screenshot",
        "pass",
        device_ids=["dev_1"],
        details={"screenshot_quality": {"ok": True}},
    )
    recorder.append(
        "Manual observation",
        "pass",
        device_ids=["dev_1"],
        details={"manual": True, "note": "real iPhone responded"},
    )


class XpGapAuditTest(unittest.TestCase):
    def test_audit_without_evidence_keeps_p1_blocked(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_declared_assets(root)

            audit = build_xp_gap_audit(
                target_stage="p1",
                run_id="p1_gap",
                root=root,
                readiness_report=P0_READY,
            )

        by_key = {row["key"]: row for row in audit["rows"]}
        self.assertFalse(audit["claims"]["real_ios_control_verified"])
        self.assertFalse(audit["claims"]["audit_is_evidence"])
        self.assertEqual(by_key["receiver_capture"]["status"], "not_started")
        self.assertEqual(by_key["hid_control"]["status"], "not_started")
        self.assertGreaterEqual(audit["summary"]["target_blockers"], 1)
        self.assertIn("XP gap audit P1", xp_gap_audit_brief(audit))

    def test_audit_marks_p1_receiver_hid_and_metadata_pass_with_field_evidence(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_declared_assets(root)
            recorder = ValidationRecorder("p1_gap", evidence_dir=root / "evidence")
            append_p1_evidence(recorder)

            audit = build_xp_gap_audit(
                target_stage="p1",
                run_id="p1_gap",
                root=root,
                evidence_jsonl=recorder.path,
                readiness_report=P1_READY,
            )

        by_key = {row["key"]: row for row in audit["rows"]}
        self.assertTrue(audit["claims"]["real_ios_control_verified"])
        self.assertEqual(by_key["component_metadata"]["status"], "pass")
        self.assertEqual(by_key["receiver_capture"]["status"], "pass")
        self.assertEqual(by_key["hid_control"]["status"], "pass")

    def test_write_xp_gap_audit_markdown(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_declared_assets(root)
            audit = build_xp_gap_audit(
                target_stage="p1",
                run_id="p1_gap",
                root=root,
                readiness_report=P0_READY,
            )
            out = write_xp_gap_audit_markdown(audit, root / "audit.md")
            text = out.read_text(encoding="utf-8")

        self.assertIn("iMouse XP Core Gap Audit P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)


if __name__ == "__main__":
    unittest.main()
