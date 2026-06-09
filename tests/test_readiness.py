import tempfile
import unittest
from pathlib import Path

from imouse.readiness import REQUIRED_DOCS, REQUIRED_MODULES, evaluate_readiness, write_readiness_markdown
from imouse.validation import ValidationRecorder


OK_DOCTOR = {"overall": "ok", "counts": {"ok": 1, "warn": 0, "fail": 0}, "checks": []}
FAIL_DOCTOR = {
    "overall": "fail",
    "counts": {"ok": 1, "warn": 0, "fail": 1},
    "checks": [{"name": "binary:uxplay", "status": "fail", "message": "UxPlay missing"}],
}


def append_component_metadata(recorder: ValidationRecorder) -> None:
    recorder.append(
        "component metadata",
        "pass",
        device_ids=["dev_1"],
        details={
            "device_id": "dev_1",
            "receiver_provider": "uxplay",
            "capture_method": "window",
            "hid_provider": "ch9329",
            "hid_id": "hid01",
            "serial_port": "COM3",
            "iphone_id": "ip01",
            "ios_version": "17.7",
        },
    )


class ReadinessTest(unittest.TestCase):
    def test_mainstream_route_decision_is_required_p0_asset(self):
        self.assertIn("docs/mainstream_route_decision.md", REQUIRED_DOCS)

    def test_imouse_xp_architecture_map_is_required_p0_asset(self):
        self.assertIn("docs/imouse_xp_architecture_map.md", REQUIRED_DOCS)

    def test_xp_parity_matrix_is_required_p0_asset(self):
        self.assertIn("docs/xp_parity_matrix.md", REQUIRED_DOCS)

    def test_industry_sop_playbook_is_required_p0_asset(self):
        self.assertIn("docs/industry_sop_playbook.md", REQUIRED_DOCS)

    def test_industry_current_state_snapshot_is_required_p0_asset(self):
        self.assertIn("docs/industry_current_state_snapshot_2026.md", REQUIRED_DOCS)

    def test_gui_live_probe_is_required_p0_asset(self):
        self.assertIn("docs/gui_live_probe.md", REQUIRED_DOCS)

    def test_gui_verification_walkthrough_is_required_p0_asset(self):
        self.assertIn("docs/gui_verification_walkthrough.md", REQUIRED_DOCS)

    def test_gui_field_evidence_runner_is_required_p0_asset(self):
        self.assertIn("docs/gui_field_evidence_runner.md", REQUIRED_DOCS)

    def test_gui_route_procurement_sop_is_required_p0_asset(self):
        self.assertIn("docs/gui_route_procurement_sop.md", REQUIRED_DOCS)

    def test_gui_industry_current_snapshot_is_required_p0_asset(self):
        self.assertIn("docs/gui_industry_current_snapshot.md", REQUIRED_DOCS)

    def test_gui_control_evidence_ledger_is_required_p0_asset(self):
        self.assertIn("docs/gui_control_evidence_ledger.md", REQUIRED_DOCS)

    def test_gui_p1_test_coach_is_required_p0_asset(self):
        self.assertIn("docs/gui_p1_test_coach.md", REQUIRED_DOCS)

    def test_gui_receiver_candidate_scorecard_is_required_p0_asset(self):
        self.assertIn("docs/gui_receiver_candidate_scorecard.md", REQUIRED_DOCS)

    def test_gui_receiver_setup_wizard_is_required_p0_asset(self):
        self.assertIn("docs/gui_receiver_setup_wizard.md", REQUIRED_DOCS)

    def test_gui_receiver_evidence_checklist_is_required_p0_asset(self):
        self.assertIn("docs/gui_receiver_evidence_checklist.md", REQUIRED_DOCS)

    def test_gui_p1_field_transcript_is_required_p0_asset(self):
        self.assertIn("docs/gui_p1_field_transcript.md", REQUIRED_DOCS)

    def test_gui_xp_source_refresh_board_is_required_p0_asset(self):
        self.assertIn("docs/gui_xp_source_refresh_board.md", REQUIRED_DOCS)

    def test_gui_xp_iteration_timeline_is_required_p0_asset(self):
        self.assertIn("docs/gui_xp_iteration_timeline.md", REQUIRED_DOCS)

    def test_gui_xp_iteration_drill_board_is_required_p0_asset(self):
        self.assertIn("docs/gui_xp_iteration_drill_board.md", REQUIRED_DOCS)

    def test_gui_xp_hardware_lab_is_required_p0_asset(self):
        self.assertIn("docs/gui_xp_hardware_lab.md", REQUIRED_DOCS)

    def test_gui_xp_api_coverage_board_is_required_p0_asset(self):
        self.assertIn("docs/gui_xp_api_coverage_board.md", REQUIRED_DOCS)

    def test_gui_script_coverage_board_is_required_p0_asset(self):
        self.assertIn("docs/gui_script_coverage_board.md", REQUIRED_DOCS)

    def test_gui_real_run_guard_is_required_p0_asset(self):
        self.assertIn("docs/gui_real_run_guard.md", REQUIRED_DOCS)

    def test_gui_acceptance_proof_map_is_required_p0_asset(self):
        self.assertIn("docs/gui_acceptance_proof_map.md", REQUIRED_DOCS)

    def test_gui_claim_scope_is_required_p0_asset(self):
        self.assertIn("docs/gui_claim_scope.md", REQUIRED_DOCS)

    def test_gui_goal_gate_is_required_p0_asset(self):
        self.assertIn("docs/gui_goal_gate.md", REQUIRED_DOCS)

    def test_follow_along_test_method_is_required_p0_asset(self):
        self.assertIn("docs/follow_along_test_method.md", REQUIRED_DOCS)

    def test_operator_worksheet_assets_are_required_p0_assets(self):
        self.assertIn("docs/operator_worksheet.md", REQUIRED_DOCS)
        self.assertIn("imouse/operator_worksheet.py", REQUIRED_MODULES)

    def test_xp_gap_audit_assets_are_required_p0_assets(self):
        self.assertIn("docs/xp_gap_audit.md", REQUIRED_DOCS)
        self.assertIn("imouse/xp_gap_audit.py", REQUIRED_MODULES)

    def test_xp_public_source_action_map_is_required_p0_asset(self):
        self.assertIn("docs/xp_public_source_action_map.md", REQUIRED_DOCS)

    def test_xp_public_source_audit_assets_are_required_p0_assets(self):
        self.assertIn("docs/xp_public_source_audit.md", REQUIRED_DOCS)
        self.assertIn("imouse/source_audit.py", REQUIRED_MODULES)

    def test_gui_xp_package_namespace_guard_is_required_p0_asset(self):
        self.assertIn("docs/gui_xp_package_namespace_guard.md", REQUIRED_DOCS)

    def test_receiver_provider_module_is_required_p0_asset(self):
        self.assertIn("imouse/receiver_provider.py", REQUIRED_MODULES)

    def test_receiver_bootstrap_assets_are_required_p0_assets(self):
        self.assertIn("docs/receiver_route_bootstrap.md", REQUIRED_DOCS)
        self.assertIn("imouse/receiver_bootstrap.py", REQUIRED_MODULES)

    def test_p0_assets_do_not_imply_p1_real_ios_control(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            required_docs = ["docs/a.md"]
            required_scripts = ["scripts/a.json"]
            required_modules = ["imouse/a.py"]
            for relative in [*required_docs, *required_scripts, *required_modules]:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")

            report = evaluate_readiness(
                root=root,
                target="p1",
                run_doctor_check=False,
                required_docs=required_docs,
                required_scripts=required_scripts,
                required_modules=required_modules,
                gates=["p1"],
            )

            self.assertFalse(report["ok"])
            self.assertTrue(report["stage_status"]["p0"]["ok"])
            self.assertFalse(report["stage_status"]["p1"]["ok"])
            self.assertTrue(report["claims"]["do_not_claim_perfect_ios_control"])
            blocker_names = [item["name"] for item in report["blockers"]]
            self.assertIn("field_evidence", blocker_names)

    def test_p1_pass_requires_acceptance_and_doctor_without_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            recorder = ValidationRecorder("p1", evidence_dir=root / "evidence")
            append_component_metadata(recorder)
            recorder.append(
                "screenshot",
                "pass",
                device_ids=["dev_1"],
                details={"screenshot_quality": {"ok": True}},
            )
            recorder.append(
                "manual observation",
                "pass",
                device_ids=["dev_1"],
                details={"manual": True, "note": "iPhone responded"},
            )

            report = evaluate_readiness(
                root=root,
                evidence_jsonl=recorder.path,
                target="p1",
                doctor_report=OK_DOCTOR,
                required_docs=[],
                required_scripts=[],
                required_modules=[],
                gates=["p1"],
            )

            self.assertTrue(report["ok"])
            self.assertTrue(report["stage_status"]["p1"]["ok"])
            self.assertFalse(report["claims"]["do_not_claim_perfect_ios_control"])

            failed_doctor_report = evaluate_readiness(
                root=root,
                evidence_jsonl=recorder.path,
                target="p1",
                doctor_report=FAIL_DOCTOR,
                required_docs=[],
                required_scripts=[],
                required_modules=[],
                gates=["p1"],
            )
            self.assertFalse(failed_doctor_report["ok"])
            self.assertFalse(failed_doctor_report["stage_status"]["p1"]["ok"])

    def test_write_readiness_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = evaluate_readiness(
                root=Path(tmp),
                target="p0",
                run_doctor_check=False,
                required_docs=[],
                required_scripts=[],
                required_modules=[],
                gates=["p1"],
            )
            out = write_readiness_markdown(report, Path(tmp) / "readiness.md")

            text = out.read_text(encoding="utf-8")
            self.assertIn("iMouse Readiness Audit", text)
            self.assertIn("Real iOS control verified", text)


if __name__ == "__main__":
    unittest.main()
