from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image

from imouse.gui import (
    ImouseGui,
    acceptance_brief,
    acceptance_proof_map_brief,
    acceptance_proof_map_rows,
    apply_route_decision_form_values,
    build_command_queue_scenario,
    build_gui_session_snapshot,
    canvas_rect_to_image_rect,
    canvas_to_image_point,
    callback_event_brief,
    callback_event_rows,
    callback_log_evidence_details,
    callback_log_evidence_status,
    callback_log_brief,
    callback_log_events_from_text,
    claim_scope_brief,
    claim_scope_rows,
    command_queue_brief,
    command_queue_rows,
    component_metadata_details,
    capture_quality_bench_brief,
    capture_quality_bench_rows,
    capture_quality_bench_status,
    control_evidence_ledger_brief,
    control_evidence_ledger_rows,
    control_response_bench_brief,
    control_response_bench_rows,
    device_evidence_matrix_brief,
    device_evidence_matrix_rows,
    device_ios_compatibility_brief,
    device_ios_compatibility_rows,
    doctor_brief,
    evidence_review_brief,
    evidence_timeline_brief,
    evidence_timeline_rows,
    field_evidence_wizard_brief,
    field_evidence_wizard_rows,
    field_evidence_runner_brief,
    field_evidence_runner_rows,
    field_kit_gate_brief,
    field_kit_gate_rows,
    first_run_packet_brief,
    first_run_packet_rows,
    field_packet_brief,
    field_runbook_brief,
    field_runbook_rows,
    fit_image_to_canvas,
    gui_control_center_brief,
    gui_control_center_rows,
    gui_goal_gate_brief,
    gui_goal_gate_rows,
    gui_knowledge_center_brief,
    gui_knowledge_center_rows,
    industry_current_snapshot_brief,
    industry_current_snapshot_rows,
    industry_route_procurement_brief,
    industry_route_procurement_rows,
    industry_sop_radar_brief,
    industry_sop_radar_rows,
    ios_field_sop_brief,
    ios_field_sop_rows,
    live_probe_brief,
    live_probe_rows,
    local_verification_brief,
    local_verification_rows,
    mainstream_route_matrix_brief,
    mainstream_route_matrix_rows,
    manual_observation_details,
    operator_home_brief,
    operator_home_rows,
    operator_worksheet_brief,
    p1_field_transcript_brief,
    p1_field_transcript_rows,
    p1_transcript_manual_prefill,
    p1_trial_brief,
    p1_trial_rows,
    p1_test_coach_brief,
    p1_test_coach_rows,
    pitfall_library_brief,
    pitfall_library_rows,
    readiness_brief,
    real_run_guard_brief,
    real_run_guard_report,
    recovery_drill_brief,
    recovery_observation_details,
    recovery_drill_rows,
    receiver_candidate_scorecard_brief,
    receiver_candidate_scorecard_rows,
    receiver_evidence_checklist_brief,
    receiver_evidence_checklist_rows,
    receiver_route_gate_brief,
    receiver_route_gate_rows,
    receiver_setup_wizard_brief,
    receiver_setup_wizard_rows,
    rerun_playbook_brief,
    rerun_playbook_rows,
    route_decision_brief,
    route_decision_issue_brief,
    route_decision_issue_rows,
    route_decision_form_values,
    route_decision_form_issues,
    route_decision_metadata_prefill_values,
    scenario_brief,
    script_coverage_board_brief,
    script_coverage_board_rows,
    scenario_library_brief,
    scenario_library_rows,
    sop_problem_ledger_brief,
    sop_problem_ledger_rows,
    stage_sop_brief,
    stage_sop_next_command,
    stage_sop_rows,
    stage_dashboard_brief,
    stage_dashboard_rows,
    standard_probe_script,
    template_asset_brief,
    template_asset_rows,
    verification_walkthrough_brief,
    verification_walkthrough_rows,
    xp_public_source_ledger_brief,
    xp_public_source_ledger_rows,
    xp_source_refresh_brief,
    xp_source_refresh_rows,
    xp_public_source_action_map_brief,
    xp_public_source_action_map_rows,
    xp_package_namespace_guard_brief,
    xp_package_namespace_guard_rows,
    xp_api_coverage_board_brief,
    xp_api_coverage_board_rows,
    xp_core_function_matrix_brief,
    xp_core_function_matrix_rows,
    xp_event_error_contract_brief,
    xp_event_error_contract_rows,
    xp_architecture_map_brief,
    xp_architecture_map_rows,
    xp_hardware_lab_brief,
    xp_hardware_lab_rows,
    xp_iteration_drill_brief,
    xp_iteration_drill_rows,
    xp_iteration_radar_brief,
    xp_iteration_radar_rows,
    xp_iteration_timeline_brief,
    xp_iteration_timeline_rows,
    xp_roadmap_brief,
    xp_roadmap_rows,
    gui_evidence_pack_brief,
    gui_evidence_pack_rows,
    gui_session_snapshot_brief,
    hardware_bench_brief,
    hardware_bench_rows,
    issue_triage_brief,
    issue_triage_rows,
    write_acceptance_proof_map_markdown,
    write_command_queue_scenario,
    write_capture_quality_bench_markdown,
    write_callback_events_markdown,
    write_callback_log_markdown,
    write_claim_scope_markdown,
    write_control_evidence_ledger_markdown,
    write_control_response_bench_markdown,
    write_device_evidence_matrix_markdown,
    write_device_ios_compatibility_markdown,
    write_evidence_timeline_markdown,
    write_field_evidence_wizard_markdown,
    write_field_evidence_runner_markdown,
    write_field_kit_gate_markdown,
    write_first_run_packet_markdown,
    write_field_runbook_markdown,
    write_gui_control_center_markdown,
    write_gui_evidence_pack_markdown,
    write_gui_goal_gate_markdown,
    write_gui_knowledge_center_markdown,
    write_industry_current_snapshot_markdown,
    write_industry_route_procurement_markdown,
    write_industry_sop_radar_markdown,
    write_ios_field_sop_markdown,
    write_gui_session_snapshot_markdown,
    write_hardware_bench_markdown,
    write_issue_triage_markdown,
    write_live_probe_markdown,
    write_local_verification_markdown,
    write_mainstream_route_matrix_markdown,
    write_operator_home_markdown,
    write_p1_field_transcript_markdown,
    write_p1_trial_markdown,
    write_p1_test_coach_markdown,
    write_pitfall_library_markdown,
    write_real_run_guard_markdown,
    write_receiver_candidate_scorecard_markdown,
    write_receiver_evidence_checklist_markdown,
    write_receiver_route_gate_markdown,
    write_receiver_setup_wizard_markdown,
    write_recovery_drill_markdown,
    write_rerun_playbook_markdown,
    write_route_decision_issue_markdown,
    write_scenario_library_markdown,
    write_script_coverage_board_markdown,
    write_sop_problem_ledger_markdown,
    write_stage_dashboard_markdown,
    write_stage_sop_markdown,
    write_template_asset_index_markdown,
    write_verification_walkthrough_markdown,
    write_xp_public_source_ledger_markdown,
    write_xp_source_refresh_markdown,
    write_xp_public_source_action_map_markdown,
    write_xp_package_namespace_guard_markdown,
    write_xp_api_coverage_board_markdown,
    write_xp_core_function_matrix_markdown,
    write_xp_event_error_contract_markdown,
    write_xp_architecture_map_markdown,
    write_xp_hardware_lab_markdown,
    write_xp_iteration_drill_markdown,
    write_xp_iteration_radar_markdown,
    write_xp_iteration_timeline_markdown,
    write_xp_roadmap_markdown,
)
from imouse.route_decision import decision_template


class GuiHelperTest(unittest.TestCase):
    def test_fit_image_to_canvas_centers_portrait_image(self):
        scale, width, height, offset_x, offset_y = fit_image_to_canvas(100, 200, 300, 300)

        self.assertEqual(scale, 1.5)
        self.assertEqual(width, 150)
        self.assertEqual(height, 300)
        self.assertEqual(offset_x, 75)
        self.assertEqual(offset_y, 0)

    def test_canvas_to_image_point_maps_center(self):
        point = canvas_to_image_point(150, 150, 100, 200, 300, 300)

        self.assertEqual(point, (50, 100))

    def test_canvas_to_image_point_rejects_letterbox_area(self):
        point = canvas_to_image_point(10, 150, 100, 200, 300, 300)

        self.assertIsNone(point)

    def test_canvas_to_image_point_clamps_bottom_right(self):
        point = canvas_to_image_point(224, 299, 100, 200, 300, 300)

        self.assertEqual(point, (99, 199))

    def test_canvas_rect_to_image_rect_maps_selection(self):
        rect = canvas_rect_to_image_rect(90, 30, 210, 270, 100, 200, 300, 300)

        self.assertEqual(rect, (10, 20, 81, 161))

    def test_canvas_rect_to_image_rect_rejects_tiny_selection(self):
        rect = canvas_rect_to_image_rect(150, 150, 151, 151, 100, 200, 300, 300)

        self.assertIsNone(rect)

    def test_doctor_brief_includes_status_counts(self):
        report = {"overall": "fail", "counts": {"ok": 11, "warn": 6, "fail": 1}}

        self.assertEqual(doctor_brief(report), "Doctor fail: ok=11, warn=6, fail=1")

    def test_doctor_brief_tolerates_missing_counts(self):
        self.assertEqual(doctor_brief({}), "Doctor unknown: ok=0, warn=0, fail=0")

    def test_scenario_brief_includes_status_counts(self):
        summary = {"ok": True, "total": 3, "success_count": 3, "failure_count": 0}

        self.assertEqual(scenario_brief(summary), "Scenario ok: total=3, pass=3, fail=0")

    def test_scenario_brief_reports_failure(self):
        summary = {"ok": False, "total": 2, "success_count": 1, "failure_count": 1}

        self.assertEqual(scenario_brief(summary), "Scenario fail: total=2, pass=1, fail=1")

    def test_evidence_review_brief_includes_failure_categories_and_metrics(self):
        summary = {
            "total": 9,
            "by_status": {"fail": 2},
            "by_failure_category": {"hid": 1, "airplay_stream": 1},
            "metrics": {"count": 3},
        }

        self.assertEqual(
            evidence_review_brief(summary),
            "Evidence review: total=9, fail=2, categories=airplay_stream=1, hid=1, metrics=3",
        )

    def test_evidence_review_brief_handles_no_categories(self):
        summary = {"total": 1, "by_status": {}, "by_failure_category": {}, "metrics": {}}

        self.assertEqual(
            evidence_review_brief(summary),
            "Evidence review: total=1, fail=0, categories=none, metrics=0",
        )

    def test_evidence_timeline_rows_and_brief_include_failure_category(self):
        rows = evidence_timeline_rows([
            {
                "ts": "2026-06-09T10:00:00Z",
                "step": "Click",
                "status": "pass",
                "device_ids": ["dev_1"],
                "details": {"x": 10, "y": 20},
                "artifacts": [],
            },
            {
                "ts": "2026-06-09T10:01:00Z",
                "step": "Manual observation",
                "status": "fail",
                "device_ids": ["dev_1"],
                "details": {"category": "hid", "note": "phone did not move"},
                "artifacts": ["evidence/dev_1_fail.png"],
            },
        ])
        brief = evidence_timeline_brief(rows)

        self.assertEqual(rows[0]["category"], "-")
        self.assertEqual(rows[1]["category"], "hid")
        self.assertEqual(rows[1]["devices"], "dev_1")
        self.assertIn("phone did not move", rows[1]["detail"])
        self.assertIn("events=2", brief)
        self.assertIn("hid=1", brief)

    def test_write_evidence_timeline_markdown(self):
        rows = evidence_timeline_rows([
            {
                "ts": "2026-06-09T10:01:00Z",
                "step": "Screenshot",
                "status": "fail",
                "device_ids": ["dev_1"],
                "details": {"screenshot_quality": {"ok": False, "reason": "black_screen"}},
                "artifacts": ["evidence/dev_1_screen.png"],
            }
        ])
        with TemporaryDirectory() as tmp:
            out = write_evidence_timeline_markdown(
                rows,
                Path(tmp) / "timeline.md",
                run_id="p1_timeline",
                evidence_path="evidence/p1_timeline.jsonl",
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Evidence Timeline p1_timeline", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("black_screen", text)

    def test_callback_event_rows_and_brief(self):
        rows = callback_event_rows([
            {
                "seq": 1,
                "ts": 1780963200.0,
                "event": "device_registered",
                "device_id": "dev_1",
                "source": "api",
                "severity": "info",
                "data": {"state": "offline"},
            },
            {
                "seq": 2,
                "event": "airplay_log",
                "id": "dev_1",
                "source": "receiver",
                "severity": "warn",
                "data": {"line": "receiver reconnect"},
            },
        ])
        brief = callback_event_brief(rows)

        self.assertEqual(rows[0]["seq"], "1")
        self.assertEqual(rows[0]["device_id"], "dev_1")
        self.assertIn("offline", rows[0]["detail"])
        self.assertEqual(rows[1]["device_id"], "dev_1")
        self.assertIn("events=2", brief)
        self.assertIn("warn=1", brief)
        self.assertIn("airplay_log=1", brief)

    def test_write_callback_events_markdown(self):
        rows = callback_event_rows([
            {
                "seq": 7,
                "event": "hardware_bound",
                "device_id": "dev_1",
                "source": "api",
                "severity": "info",
                "data": {"port": "COM7"},
            }
        ])
        with TemporaryDirectory() as tmp:
            out = write_callback_events_markdown(
                rows,
                Path(tmp) / "callbacks.md",
                run_id="p1_callbacks",
                server_url="http://127.0.0.1:9911",
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Callback Monitor", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("hardware_bound", text)

    def test_callback_log_events_classify_receiver_and_hid_lines(self):
        events = callback_log_events_from_text(
            """
            AirPlay receiver reconnect warning
            CH9329 serial COM7 mouse click failed
            screenshot black screen no frame
            """,
            device_id="dev_1",
            source="log:receiver.log",
        )
        brief = callback_log_brief(events, pushed=2)

        self.assertEqual(len(events), 3)
        self.assertEqual(events[0]["event"], "airplay_log")
        self.assertEqual(events[0]["severity"], "warn")
        self.assertEqual(events[1]["event"], "hid_log")
        self.assertEqual(events[1]["severity"], "fail")
        self.assertEqual(events[1]["data"]["category"], "hid")
        self.assertEqual(events[2]["event"], "capture_log")
        self.assertIn("pushed=2", brief)
        self.assertIn("hid_log=1", brief)

    def test_callback_log_events_cap_lines_and_skip_blank(self):
        events = callback_log_events_from_text("\nline one\n\nline two\nline three", max_lines=2)

        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["data"]["line_no"], 2)
        self.assertEqual(events[1]["data"]["line_no"], 4)
        self.assertEqual(callback_log_events_from_text("line", max_lines=0), [])

    def test_callback_log_evidence_details_classify_fail_without_manual_claim(self):
        events = callback_log_events_from_text(
            """
            AirPlay receiver reconnect warning
            CH9329 serial COM7 mouse click failed
            screenshot black screen no frame
            """,
            device_id="dev_1",
            source="log:receiver.log",
        )

        status = callback_log_evidence_status(events)
        details = callback_log_evidence_details(
            events,
            source_path="receiver.log",
            pushed=2,
            push_error="",
        )

        self.assertEqual(status, "fail")
        self.assertTrue(details["log_triage"])
        self.assertFalse(details["manual_observation"])
        self.assertNotIn("manual", details)
        self.assertEqual(details["category"], "hid")
        self.assertEqual(details["by_category"]["hid"], 1)
        self.assertEqual(details["by_category"]["capture"], 1)
        self.assertEqual(details["devices"], ["dev_1"])
        self.assertEqual(details["pushed"], 2)
        self.assertIn("not prove real iPhone control", details["claim_boundary"])

    def test_callback_log_evidence_status_warn_info_and_empty_logs(self):
        warn_events = callback_log_events_from_text("receiver reconnect warning")
        info_events = callback_log_events_from_text("receiver started")

        self.assertEqual(callback_log_evidence_status(warn_events), "info")
        self.assertEqual(callback_log_evidence_status(info_events), "info")
        self.assertEqual(callback_log_evidence_status([]), "skip")

    def test_write_callback_log_markdown(self):
        events = callback_log_events_from_text(
            "worker error timeout\n",
            device_id="dev_1",
            source="log:receiver.log",
        )
        with TemporaryDirectory() as tmp:
            out = write_callback_log_markdown(
                events,
                Path(tmp) / "callback_log.md",
                run_id="p1_log",
                source_path="receiver.log",
                server_url="http://127.0.0.1:9911",
                pushed=1,
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Callback Log Attach", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("receiver_error", text)

    def test_issue_triage_rows_group_failed_events(self):
        rows = issue_triage_rows([
            {
                "ts": "2026-06-09T10:00:00Z",
                "step": "Click",
                "status": "fail",
                "device_ids": ["dev_1"],
                "details": {"category": "hid", "note": "phone did not move"},
                "artifacts": ["evidence/dev_1_hid.png"],
            },
            {
                "ts": "2026-06-09T10:01:00Z",
                "step": "Scenario summary",
                "status": "fail",
                "details": {"results": [{"status": "fail"}]},
            },
            {
                "ts": "2026-06-09T10:02:00Z",
                "step": "Screenshot",
                "status": "fail",
                "device_ids": ["dev_2"],
                "details": {"screenshot_quality": {"ok": False, "reason": "black_screen"}},
            },
        ])
        by_category = {row["category"]: row for row in rows}
        brief = issue_triage_brief(rows)

        self.assertEqual(by_category["hid"]["count"], "1")
        self.assertEqual(by_category["hid"]["devices"], "dev_1")
        self.assertIn("Scan hardware", by_category["hid"]["next_action"])
        self.assertEqual(by_category["capture"]["count"], "1")
        self.assertNotIn("uncategorized", by_category)
        self.assertIn("categories=2", brief)

    def test_write_issue_triage_markdown(self):
        rows = issue_triage_rows([
            {
                "ts": "2026-06-09T10:00:00Z",
                "step": "Find image",
                "status": "fail",
                "device_ids": ["dev_1"],
                "details": {"category": "vision_template"},
                "artifacts": ["evidence/template_miss.png"],
            }
        ])
        with TemporaryDirectory() as tmp:
            out = write_issue_triage_markdown(
                rows,
                Path(tmp) / "triage.md",
                run_id="p1_triage",
                evidence_path="evidence/p1_triage.jsonl",
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Issue Triage p1_triage", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("vision_template", text)

    def test_rerun_playbook_rows_turn_failures_into_smallest_rerun(self):
        issue_rows = issue_triage_rows([
            {
                "ts": "2026-06-09T10:00:00Z",
                "step": "Click",
                "status": "fail",
                "device_ids": ["dev_1"],
                "details": {"category": "hid", "note": "phone did not move"},
                "artifacts": ["evidence/dev_1_hid.png"],
            },
            {
                "ts": "2026-06-09T10:01:00Z",
                "step": "Route Decision",
                "status": "fail",
                "device_ids": ["dev_1"],
                "details": {"category": "route_decision", "note": "receiver not confirmed"},
            },
        ])
        rows = rerun_playbook_rows(
            issue_rows,
            stage="p1",
            route_report={"ok": False, "ready": False, "issues": ["receiver missing"]},
            doctor_report={"overall": "fail", "counts": {"ok": 5, "warn": 1, "fail": 1}},
            acceptance_report={"ok": False, "checks": [{"key": "manual_observation", "status": "fail"}]},
            readiness_report={"ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 4, "by_status": {"fail": 2}},
        )
        by_category = {row["category"]: row for row in rows}
        brief = rerun_playbook_brief(rows, stage="p1")

        self.assertEqual(by_category["route_decision"]["fresh_run_id"], "yes")
        self.assertEqual(by_category["route_decision"]["gui_action"], "Edit Route")
        self.assertIn("fresh run_id", by_category["route_decision"]["rerun_rule"])
        self.assertEqual(by_category["hid"]["gui_action"], "Open Control Bench")
        self.assertIn("Hardware scan", by_category["hid"]["evidence"])
        self.assertIn("HID id", by_category["hid"]["evidence"])
        self.assertEqual(by_category["doctor"]["status"], "fail")
        self.assertEqual(by_category["acceptance"]["status"], "fail")
        self.assertEqual(by_category["readiness"]["status"], "fail")
        self.assertIn("first_action=hid", brief)

    def test_rerun_playbook_rows_keep_clean_evidence_as_warn_until_real_ios_verified(self):
        rows = rerun_playbook_rows(
            [],
            stage="p1",
            route_report={"ok": True, "ready": True},
            doctor_report={"overall": "ok", "counts": {"ok": 8, "warn": 0, "fail": 0}},
            acceptance_report={"ok": True},
            readiness_report={"ok": True, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 3, "by_status": {"pass": 3}},
        )
        by_category = {row["category"]: row for row in rows}

        self.assertNotIn("no_open_rerun", by_category)
        self.assertEqual(by_category["readiness"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_category["readiness"]["current"])

    def test_write_rerun_playbook_markdown(self):
        rows = rerun_playbook_rows(
            issue_triage_rows([
                {
                    "ts": "2026-06-09T10:00:00Z",
                    "step": "Screenshot",
                    "status": "fail",
                    "device_ids": ["dev_1"],
                    "details": {"category": "capture", "note": "black frame"},
                }
            ]),
            stage="p1",
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report=None,
            evidence_exists=True,
            evidence_summary={"total": 1, "by_status": {"fail": 1}},
        )
        with TemporaryDirectory() as tmp:
            out = write_rerun_playbook_markdown(
                rows,
                Path(tmp) / "rerun.md",
                run_id="p1_rerun",
                stage="p1",
                evidence_path="evidence/p1_rerun.jsonl",
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Rerun Playbook P1", text)
        self.assertIn("capture", text)
        self.assertIn("Fresh run_id", text)
        self.assertIn("does not write evidence", text)

    def test_recovery_drill_rows_turn_failures_into_recovery_lanes(self):
        issue_rows = issue_triage_rows([
            {
                "ts": "2026-06-09T10:00:00Z",
                "step": "Screenshot",
                "status": "fail",
                "device_ids": ["dev_1"],
                "details": {"category": "capture", "note": "black frame"},
                "artifacts": ["evidence/dev_1_black.png"],
            },
            {
                "ts": "2026-06-09T10:01:00Z",
                "step": "Click",
                "status": "fail",
                "device_ids": ["dev_1"],
                "details": {"category": "hid", "note": "phone did not move"},
            },
            {
                "ts": "2026-06-09T10:02:00Z",
                "step": "Metrics",
                "status": "fail",
                "details": {"category": "performance", "note": "memory pressure"},
            },
        ])
        rows = recovery_drill_rows(
            issue_rows,
            stage="p3",
            route_report={"ok": True, "ready": True},
            doctor_report={"overall": "ok", "counts": {"ok": 8, "warn": 0, "fail": 0}},
            acceptance_report={"ok": False, "checks": [{"key": "screenshot_quality", "status": "fail"}]},
            readiness_report={"ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 8, "by_status": {"fail": 3}, "metrics": {"count": 1}},
        )
        by_key = {row["key"]: row for row in rows}
        brief = recovery_drill_brief(rows, stage="p3")

        self.assertEqual(by_key["receiver_capture_recovery"]["status"], "fail")
        self.assertEqual(by_key["receiver_capture_recovery"]["gui_action"], "Run Shot Bench")
        self.assertIn("Receiver log", by_key["receiver_capture_recovery"]["evidence"])
        self.assertEqual(by_key["hid_control_recovery"]["status"], "fail")
        self.assertEqual(by_key["hid_control_recovery"]["gui_action"], "Open Control Bench")
        self.assertEqual(by_key["performance_watchdog_recovery"]["status"], "fail")
        self.assertEqual(by_key["performance_watchdog_recovery"]["gui_action"], "Open Dashboard")
        self.assertIn("first_action=receiver_capture_recovery", brief)

    def test_recovery_drill_rows_warn_when_gates_clean_but_real_ios_unverified(self):
        rows = recovery_drill_rows(
            [],
            stage="p1",
            route_report={"ok": True, "ready": True},
            doctor_report={"overall": "ok", "counts": {"ok": 8, "warn": 0, "fail": 0}},
            acceptance_report={
                "ok": True,
                "checks": [
                    {"key": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    {"key": "manual_observation", "status": "pass", "message": "1 manual pass"},
                ],
            },
            readiness_report={"ok": True, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 3, "by_status": {"pass": 3}, "metrics": {"count": 0}},
        )
        by_key = {row["key"]: row for row in rows}

        self.assertEqual(by_key["route_doctor_recovery"]["status"], "ready")
        self.assertEqual(by_key["receiver_capture_recovery"]["status"], "ready")
        self.assertEqual(by_key["hid_control_recovery"]["status"], "ready")
        self.assertEqual(by_key["handoff_claim_recovery"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_key["handoff_claim_recovery"]["current"])

    def test_recovery_observation_details_keeps_execution_evidence_separate_from_manual_pass(self):
        row = {
            "key": "receiver_capture_recovery",
            "status": "fail",
            "category_count": "2",
            "categories": "airplay_stream, capture",
            "trigger": "black frame",
            "current": "screenshot failed",
            "recovery": "Restart receiver and capture",
            "verify": "Run Shot Bench",
            "evidence": "Receiver log and screenshot",
            "stop_rule": "Stop HID until screenshot passes",
            "gui_action": "Run Shot Bench",
            "method": "run_capture_quality_bench_from_gui",
        }

        details = recovery_observation_details(
            row=row,
            status="pass",
            note="receiver restarted and screenshot recovered",
            selected_device="dev_1",
            click_x=100,
            click_y=200,
        )

        self.assertTrue(details["recovery_drill"])
        self.assertNotIn("manual", details)
        self.assertEqual(details["operator_result"], "pass")
        self.assertEqual(details["recovery_key"], "receiver_capture_recovery")
        self.assertEqual(details["category"], "airplay_stream")
        self.assertEqual(details["categories"], ["airplay_stream", "capture"])
        self.assertEqual(details["selected_device"], "dev_1")
        self.assertEqual(details["click"], {"x": 100, "y": 200})
        self.assertIn("Shot Bench", details["verify_step"])

    def test_write_recovery_drill_markdown(self):
        rows = recovery_drill_rows(
            issue_triage_rows([
                {
                    "ts": "2026-06-09T10:00:00Z",
                    "step": "AirPlay",
                    "status": "fail",
                    "device_ids": ["dev_1"],
                    "details": {"category": "airplay_stream", "note": "stale frame"},
                }
            ]),
            stage="p1",
            route_report={"ok": False, "ready": False},
            doctor_report={"overall": "fail", "counts": {"ok": 5, "warn": 0, "fail": 1}},
            acceptance_report=None,
            readiness_report=None,
            evidence_exists=True,
            evidence_summary={"total": 1, "by_status": {"fail": 1}, "metrics": {}},
        )
        with TemporaryDirectory() as tmp:
            out = write_recovery_drill_markdown(
                rows,
                Path(tmp) / "recovery.md",
                run_id="p1_recovery",
                stage="p1",
                evidence_path="evidence/p1_recovery.jsonl",
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Recovery Drill P1", text)
        self.assertIn("receiver_capture_recovery", text)
        self.assertIn("Recovery step", text)
        self.assertIn("Record Pass/Fail buttons can write recovery execution evidence", text)
        self.assertIn("not a substitute for Manual/P1 Trial", text)

    def test_pitfall_library_rows_surface_existing_failure_categories(self):
        issue_rows = issue_triage_rows([
            {
                "ts": "2026-06-09T10:00:00Z",
                "step": "Click",
                "status": "fail",
                "device_ids": ["dev_1"],
                "details": {"category": "hid", "note": "phone did not move"},
                "artifacts": ["evidence/dev_1_hid.png"],
            },
            {
                "ts": "2026-06-09T10:01:00Z",
                "step": "Screenshot",
                "status": "fail",
                "device_ids": ["dev_1"],
                "details": {"screenshot_quality": {"ok": False, "reason": "black_screen"}},
            },
        ])
        rows = pitfall_library_rows(
            stage="p1",
            docs_root=".",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            acceptance_report={
                "gate": "p1",
                "ok": False,
                "checks": [
                    {"name": "manual_observation", "status": "fail", "message": "0 manual pass"},
                    {"name": "screenshot_quality", "status": "fail", "message": "black screen"},
                ],
            },
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 2, "by_status": {"fail": 2}},
            issue_rows_data=issue_rows,
        )
        by_key = {row["key"]: row for row in rows}
        brief = pitfall_library_brief(rows, stage="p1")

        self.assertEqual(by_key["hid_no_response"]["status"], "fail")
        self.assertEqual(by_key["receiver_stream_capture"]["status"], "fail")
        self.assertIn("category_failures=1", by_key["hid_no_response"]["current"])
        self.assertIn("first_focus=", brief)

    def test_pitfall_library_rows_keep_xp_hardware_parity_warn_on_ch9329(self):
        route = decision_template(run_id="pitfall_xp", devices=["dev_1"])
        apply_route_decision_form_values(route, {
            "hid.route": "ch9329",
            "hid.provider": "ch9329",
            "hid.id": "hid01",
            "hid.firmware": "ch9329-v1",
            "hid.serial_port": "COM3",
            "decision.allowed_to_run_p1": "true",
            "decision.open_blockers": "",
        })
        rows = pitfall_library_rows(
            stage="p1",
            docs_root=".",
            device_ids=["dev_1"],
            route_decision=route,
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            issue_rows_data=[],
        )
        by_key = {row["key"]: row for row in rows}

        self.assertEqual(by_key["xp_hardware_parity"]["status"], "warn")
        self.assertIn("generic P1 may continue", by_key["xp_hardware_parity"]["current"])
        self.assertEqual(by_key["receiver_discovery"]["status"], "ready")

    def test_write_pitfall_library_markdown(self):
        rows = pitfall_library_rows(
            stage="p1",
            docs_root=".",
            device_ids=[],
            route_report=None,
            doctor_report=None,
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_pitfall_library_markdown(
                rows,
                Path(tmp) / "pitfalls.md",
                run_id="p1_pitfalls",
                stage="p1",
                evidence_path="evidence/p1_pitfalls.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Pitfall Library P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)

    def test_sop_problem_ledger_rows_merge_pitfalls_issues_and_rerun_rules(self):
        events = [
            {
                "ts": "2026-06-09T10:00:00Z",
                "step": "Click",
                "status": "fail",
                "device_ids": ["dev_1"],
                "details": {"category": "hid", "note": "phone did not move"},
                "artifacts": ["evidence/dev_1_hid.png"],
            },
            {
                "ts": "2026-06-09T10:01:00Z",
                "step": "Screenshot",
                "status": "fail",
                "device_ids": ["dev_1"],
                "details": {"screenshot_quality": {"ok": False, "reason": "black_screen"}},
            },
        ]
        issue_rows = issue_triage_rows(events)
        pitfall_rows = pitfall_library_rows(
            stage="p1",
            docs_root=".",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            acceptance_report={
                "gate": "p1",
                "ok": False,
                "checks": [
                    {"name": "manual_observation", "status": "fail", "message": "0 manual pass"},
                    {"name": "screenshot_quality", "status": "fail", "message": "black screen"},
                ],
            },
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 2, "by_status": {"fail": 2}},
            issue_rows_data=issue_rows,
        )
        rerun_rows = rerun_playbook_rows(
            issue_rows,
            stage="p1",
            route_report={"ok": True, "ready": True},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            acceptance_report={"ok": False},
            readiness_report={"ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 2, "by_status": {"fail": 2}},
        )

        rows = sop_problem_ledger_rows(
            stage="p1",
            pitfall_rows_data=pitfall_rows,
            issue_rows_data=issue_rows,
            rerun_rows_data=rerun_rows,
            evidence_exists=True,
            evidence_summary={"total": 2, "by_status": {"fail": 2}},
            readiness_report={"claims": {"real_ios_control_verified": False}},
        )
        by_problem = {row["problem"]: row for row in rows}
        hid = by_problem["HID command success but iPhone does not respond"]
        capture = by_problem["Black screen, stale frame, or wrong capture window"]
        brief = sop_problem_ledger_brief(rows, stage="p1")

        self.assertEqual(hid["status"], "fail")
        self.assertEqual(hid["count"], "1")
        self.assertEqual(hid["ledger_type"], "field_failure")
        self.assertIn("Scan hardware", hid["rerun_rule"])
        self.assertIn("Hardware scan", hid["evidence"])
        self.assertEqual(hid["gui_action"], "Open Control Bench")
        self.assertEqual(capture["status"], "fail")
        self.assertIn("field_failures=2", brief)

    def test_write_sop_problem_ledger_markdown(self):
        rows = sop_problem_ledger_rows(
            stage="p1",
            pitfall_rows_data=[{
                "pitfall": "HID command success but iPhone does not respond",
                "status": "fail",
                "categories": "hid",
                "current": "category_failures=1",
                "sop_check": "Scan/bind HID and record Manual pass/fail.",
                "first_probe": "Open Control Bench.",
                "stop_rule": "Stop if the iPhone does not visibly respond.",
                "gui_action": "Open Control Bench",
                "method": "show_control_response_bench_from_gui",
            }],
            issue_rows_data=[{"category": "hid", "count": "1", "devices": "dev_1", "steps": "Click"}],
            rerun_rows_data=[],
            evidence_exists=True,
            evidence_summary={"total": 1, "by_status": {"fail": 1}},
            readiness_report={"claims": {"real_ios_control_verified": False}},
        )
        with TemporaryDirectory() as tmp:
            out = write_sop_problem_ledger_markdown(
                rows,
                Path(tmp) / "problems.md",
                run_id="p1_problems",
                stage="p1",
                evidence_path="evidence/p1_problems.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI SOP Problem Ledger P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("HID command success", text)

    def test_device_evidence_matrix_rows_show_per_device_gaps(self):
        rows = device_evidence_matrix_rows(
            device_rows=[
                {
                    "device_id": "dev_1",
                    "state": "capturing",
                    "hardware_id": "COM3",
                    "profile": {
                        "receiver_provider": "uxplay",
                        "capture_method": "window",
                        "hid_provider": "ch9329",
                        "serial_port": "COM3",
                        "iphone_id": "iphone_1",
                        "ios_version": "17.7",
                    },
                },
                {"device_id": "dev_2", "state": "offline", "profile": {}},
            ],
            selected_device_ids=["dev_1", "dev_2"],
            events=[
                {
                    "ts": "2026-06-09T10:00:00Z",
                    "step": "Screenshot",
                    "status": "pass",
                    "device_ids": ["dev_1"],
                    "details": {"screenshot_quality": {"ok": True}},
                },
                {
                    "ts": "2026-06-09T10:01:00Z",
                    "step": "Manual observation",
                    "status": "pass",
                    "device_ids": ["dev_1"],
                    "details": {"manual": True},
                },
                {
                    "ts": "2026-06-09T10:02:00Z",
                    "step": "Click",
                    "status": "fail",
                    "device_ids": [],
                    "details": {"category": "hid"},
                },
            ],
        )
        by_device = {row["device_id"]: row for row in rows}
        brief = device_evidence_matrix_brief(rows)

        self.assertEqual(by_device["dev_1"]["status"], "pass")
        self.assertEqual(by_device["dev_2"]["status"], "pending")
        self.assertIn("no_events", by_device["dev_2"]["gaps"])
        self.assertEqual(by_device["unassigned"]["status"], "fail")
        self.assertIn("missing_device_id", by_device["unassigned"]["gaps"])
        self.assertIn("devices=3", brief)
        self.assertIn("pass=1", brief)

    def test_write_device_evidence_matrix_markdown(self):
        rows = device_evidence_matrix_rows(
            device_rows=[{"device_id": "dev_1", "state": "offline", "profile": {}}],
            selected_device_ids=["dev_1"],
            events=[],
        )
        with TemporaryDirectory() as tmp:
            out = write_device_evidence_matrix_markdown(
                rows,
                Path(tmp) / "matrix.md",
                run_id="p3_matrix",
                evidence_path="evidence/p3_matrix.jsonl",
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Device Evidence Matrix p3_matrix", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("component_metadata", text)

    def test_device_ios_compatibility_rows_group_model_and_ios_coverage(self):
        rows = device_ios_compatibility_rows(
            device_rows=[
                {
                    "device_id": "dev_1",
                    "state": "capturing",
                    "hardware_id": "COM3",
                    "profile": {
                        "receiver_provider": "uxplay",
                        "capture_method": "window",
                        "hid_provider": "ch9329",
                        "serial_port": "COM3",
                        "iphone_id": "iphone_13_a",
                        "iphone_model": "iPhone 13",
                        "ios_version": "17.7",
                    },
                },
                {
                    "device_id": "dev_2",
                    "state": "offline",
                    "profile": {
                        "receiver_provider": "uxplay",
                        "capture_method": "window",
                        "hid_provider": "ch9329",
                        "serial_port": "COM4",
                        "iphone_id": "iphone_16_b",
                        "iphone_model": "iPhone 16 Pro",
                        "ios_version": "18.5",
                    },
                },
            ],
            selected_device_ids=["dev_1", "dev_2"],
            events=[
                {
                    "ts": "2026-06-09T10:00:00Z",
                    "step": "Screenshot",
                    "status": "pass",
                    "device_ids": ["dev_1"],
                    "details": {"screenshot_quality": {"ok": True}},
                },
                {
                    "ts": "2026-06-09T10:01:00Z",
                    "step": "Manual observation",
                    "status": "pass",
                    "device_ids": ["dev_1"],
                    "details": {"manual": True},
                },
            ],
            target_stage="p1",
        )
        by_pair = {(row["model"], row["ios_version"]): row for row in rows}
        brief = device_ios_compatibility_brief(rows, stage="p1")

        self.assertEqual(by_pair[("iPhone 13", "17.7")]["status"], "pass")
        self.assertEqual(by_pair[("iPhone 13", "17.7")]["claim"], "covered_for_p1")
        self.assertEqual(by_pair[("iPhone 16 Pro", "18.5")]["status"], "pending")
        self.assertEqual(by_pair[("iPhone 16 Pro", "18.5")]["claim"], "not_covered")
        self.assertIn("manual_observation", by_pair[("iPhone 16 Pro", "18.5")]["gaps"])
        self.assertIn("covered=1", brief)
        self.assertIn("first_gap=iPhone 16 Pro/18.5", brief)

    def test_write_device_ios_compatibility_markdown(self):
        rows = device_ios_compatibility_rows(
            device_rows=[{"device_id": "dev_1", "state": "offline", "profile": {}}],
            selected_device_ids=["dev_1"],
            events=[],
            target_stage="p1",
        )
        with TemporaryDirectory() as tmp:
            out = write_device_ios_compatibility_markdown(
                rows,
                Path(tmp) / "compat.md",
                run_id="p1_compat",
                stage="p1",
                evidence_path="evidence/p1_compat.jsonl",
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("Device iOS Compatibility Matrix P1", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("does not prove broad compatibility", text)
        self.assertIn("unknown_model", text)

    def test_real_run_guard_report_blocks_without_route_and_doctor(self):
        report = real_run_guard_report(
            stage="p1",
            device_ids=["dev_1"],
            route_report=None,
            doctor_report=None,
        )
        brief = real_run_guard_brief(report)

        self.assertFalse(report["ok"])
        self.assertEqual([item["name"] for item in report["blockers"]], ["route_decision", "doctor"])
        self.assertIn("blocked", brief)

    def test_real_run_guard_report_allows_ready_route_and_ok_doctor(self):
        report = real_run_guard_report(
            stage="p1",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
        )

        self.assertTrue(report["ok"])
        self.assertEqual(real_run_guard_brief(report), "Real-run guard P1 allow: blockers=none")

    def test_real_run_guard_report_allows_route_aware_doctor_warn_without_fail(self):
        report = real_run_guard_report(
            stage="p1",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "warn", "counts": {"ok": 12, "warn": 1, "fail": 0}},
        )

        self.assertTrue(report["ok"])
        self.assertEqual([item["name"] for item in report["blockers"]], [])
        self.assertIn("warn=1", report["checks"][2]["message"])

    def test_real_run_guard_report_blocks_doctor_warn_with_fail_count(self):
        report = real_run_guard_report(
            stage="p1",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "warn", "counts": {"ok": 12, "warn": 1, "fail": 1}},
        )

        self.assertFalse(report["ok"])
        self.assertEqual([item["name"] for item in report["blockers"]], ["doctor"])

    def test_write_real_run_guard_markdown(self):
        report = real_run_guard_report(
            stage="p1",
            device_ids=[],
            route_report={"ok": False, "ready": False, "blockers": [{"name": "route"}]},
            doctor_report={"overall": "fail", "counts": {"ok": 0, "warn": 0, "fail": 1}},
        )
        with TemporaryDirectory() as tmp:
            out = write_real_run_guard_markdown(
                report,
                Path(tmp) / "guard.md",
                run_id="p1_guard",
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Real-run Guard P1", text)
        self.assertIn("Allowed: `False`", text)
        self.assertIn("does not prove real iPhone response", text)
        self.assertIn("Next Actions", text)
        self.assertIn("Open Route Edit / Receiver / Rx Setup", text)
        self.assertIn("Do not bypass this guard", text)

    def test_readiness_brief_includes_stages_and_blockers(self):
        report = {
            "target": "p1",
            "ok": False,
            "stage_status": {
                "p0": {"ok": True},
                "p1": {"ok": False},
            },
            "blockers": [{"name": "doctor"}, {"name": "field_evidence"}],
        }

        self.assertEqual(
            readiness_brief(report),
            "Readiness P1 fail: P0=pass, P1=fail; blockers=doctor, field_evidence",
        )

    def test_route_decision_brief_includes_ready_and_blockers(self):
        report = {
            "target_stage": "p1",
            "ok": False,
            "ready": False,
            "blockers": [{"name": "route_choice"}, {"name": "placeholders"}],
        }

        self.assertEqual(
            route_decision_brief(report),
            "Route decision P1 fail: ready=False; blockers=route_choice, placeholders",
        )

    def test_field_packet_brief_includes_doctor_and_readiness(self):
        packet = {
            "stage": "p1",
            "device_count": 1,
            "doctor": {"overall": "fail"},
            "readiness": {"ok": False, "blockers": [{"name": "acceptance:p1"}]},
        }

        self.assertEqual(
            field_packet_brief(packet),
            "Field packet P1: devices=1, doctor=fail, readiness=fail; blockers=acceptance:p1",
        )

    def test_operator_worksheet_brief_includes_counts(self):
        worksheet = {
            "stage": "p3",
            "device_count": 4,
            "steps": [{"name": "one"}, {"name": "two"}],
            "scripts": ["a.json"],
        }

        self.assertEqual(
            operator_worksheet_brief(worksheet),
            "Operator worksheet P3: devices=4, steps=2, scripts=1",
        )

    def test_acceptance_brief_summarizes_failed_checks(self):
        report = {
            "gate": "p1",
            "ok": False,
            "checks": [
                {"name": "evidence_exists", "status": "pass"},
                {"name": "manual_observation", "status": "fail"},
                {"name": "screenshot_quality", "status": "fail"},
            ],
        }

        self.assertEqual(
            acceptance_brief(report),
            "Acceptance P1 fail: checks=1/3; failed=manual_observation, screenshot_quality",
        )

    def test_standard_probe_script_maps_stage(self):
        self.assertEqual(standard_probe_script("p1"), "scripts/p1_single_device_control_probe.json")
        self.assertEqual(standard_probe_script("p3"), "scripts/pilot_4_group_smoke.json")
        self.assertEqual(standard_probe_script("unknown"), "scripts/p1_single_device_control_probe.json")

    def test_scenario_library_rows_scan_scripts_and_fail_bad_json(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "scripts"
            root.mkdir()
            (root / "p3_demo.json").write_text(
                """
{
  "name": "p3 demo",
  "steps": [
    {"action": "click", "device_id": "dev_1", "x": 1, "y": 2},
    {"action": "repeat", "count": 2, "steps": [
      {"action": "screenshot", "device_id": "dev_2"}
    ]}
  ]
}
""".strip(),
                encoding="utf-8",
            )
            (root / "bad.json").write_text("{", encoding="utf-8")

            rows = scenario_library_rows(root)
            by_name = {row["name"]: row for row in rows}
            brief = scenario_library_brief(rows)

        self.assertEqual(by_name["p3 demo"]["stage"], "p3")
        self.assertEqual(by_name["p3 demo"]["steps"], "3")
        self.assertIn("click=1", by_name["p3 demo"]["actions"])
        self.assertIn("screenshot=1", by_name["p3 demo"]["actions"])
        self.assertIn("dev_1", by_name["p3 demo"]["devices"])
        self.assertEqual(by_name["bad"]["status"], "fail")
        self.assertIn("fail=1", brief)

    def test_write_scenario_library_markdown(self):
        rows = [
            {
                "stage": "p1",
                "name": "p1 smoke",
                "status": "ok",
                "steps": "2",
                "actions": "click=1, screenshot=1",
                "devices": "dev_1",
                "groups": "-",
                "dry_run": "required_first",
                "path": "scripts/p1.json",
                "note": "Dry-run first",
            }
        ]
        with TemporaryDirectory() as tmp:
            out = write_scenario_library_markdown(rows, Path(tmp) / "library.md", run_id="p1_lib")
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Scenario Library", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("scripts/p1.json", text)

    def test_live_probe_rows_keep_missing_evidence_blocked(self):
        acceptance = {
            "gate": "p1",
            "ok": False,
            "checks": [
                {"name": "component_traceability", "status": "fail", "message": "0 component metadata"},
                {"name": "screenshot_quality", "status": "fail", "message": "0 screenshot quality"},
                {"name": "manual_observation", "status": "fail", "message": "0 manual pass"},
                {"name": "metrics", "status": "pass", "message": "0 metrics sample(s), required >= 0"},
            ],
        }
        readiness = {
            "target": "p1",
            "ok": False,
            "stage_status": {"p0": {"ok": True}, "p1": {"ok": False}},
            "blockers": [{"name": "field_evidence"}],
        }

        rows = live_probe_rows(
            stage="p1",
            device_ids=[],
            acceptance_report=acceptance,
            readiness_report=readiness,
            evidence_exists=False,
            evidence_summary=None,
        )
        by_key = {row["key"]: row for row in rows}
        brief = live_probe_brief(rows, stage="p1")

        self.assertEqual(by_key["devices"]["status"], "fail")
        self.assertEqual(by_key["evidence"]["status"], "fail")
        self.assertEqual(by_key["component_traceability"]["status"], "fail")
        self.assertEqual(by_key["metrics"]["status"], "pass")
        self.assertIn("Live probe P1", brief)
        self.assertIn("blockers=devices", brief)

    def test_live_probe_rows_can_pass_clean_p1_snapshot(self):
        route = {"target_stage": "p1", "ok": True, "ready": True, "blockers": []}
        doctor = {"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}}
        scenario = {"ok": True, "total": 2, "success_count": 2, "failure_count": 0}
        acceptance = {
            "gate": "p1",
            "ok": True,
            "checks": [
                {"name": "component_traceability", "status": "pass", "message": "1 component metadata"},
                {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot quality"},
                {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                {"name": "metrics", "status": "pass", "message": "0 metrics sample(s), required >= 0"},
            ],
        }
        readiness = {
            "target": "p1",
            "ok": True,
            "stage_status": {"p0": {"ok": True}, "p1": {"ok": True}},
            "blockers": [],
        }

        rows = live_probe_rows(
            stage="p1",
            device_ids=["dev_1"],
            route_report=route,
            doctor_report=doctor,
            scenario_summary=scenario,
            acceptance_report=acceptance,
            readiness_report=readiness,
            evidence_exists=True,
            evidence_summary={"total": 4},
        )

        self.assertTrue(all(row["status"] == "pass" for row in rows))
        self.assertIn("blockers=none", live_probe_brief(rows, stage="p1"))

    def test_write_live_probe_markdown(self):
        rows = live_probe_rows(
            stage="p1",
            device_ids=["dev_1"],
            acceptance_report={"gate": "p1", "ok": False, "checks": []},
            readiness_report={"ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_live_probe_markdown(
                rows,
                Path(tmp) / "probe.md",
                stage="p1",
                run_id="p1_live",
                evidence_path="evidence/p1_live.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Live Probe P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)

    def test_stage_dashboard_rows_surface_current_stage_blockers(self):
        readiness = {
            "target": "p1",
            "ok": False,
            "stage_status": {
                "p0": {"ok": True},
                "p1": {"ok": False},
                "p2": {"ok": False},
                "p3": {"ok": False},
                "p4": {"ok": False},
            },
            "blockers": [{"name": "doctor"}, {"name": "field_evidence"}, {"name": "acceptance:p1"}],
            "claims": {"real_ios_control_verified": False},
        }
        acceptance = {
            "p1": {
                "gate": "p1",
                "ok": False,
                "checks": [
                    {"name": "manual_observation", "status": "fail"},
                    {"name": "screenshot_quality", "status": "fail"},
                ],
            }
        }

        rows = stage_dashboard_rows(
            target_stage="p1",
            device_ids=[],
            readiness_report=readiness,
            acceptance_reports=acceptance,
            route_report={"ok": False},
            doctor_report={"overall": "fail"},
            evidence_exists=False,
        )
        by_stage = {row["stage"]: row for row in rows}
        brief = stage_dashboard_brief(rows, target_stage="p1")

        self.assertEqual(by_stage["p0"]["status"], "pass")
        self.assertEqual(by_stage["p1"]["status"], "fail")
        self.assertIn("devices", by_stage["p1"]["blockers"])
        self.assertIn("route_decision", by_stage["p1"]["blockers"])
        self.assertIn("Stage dashboard P1", brief)
        self.assertIn("current=P1 fail", brief)

    def test_write_stage_dashboard_markdown(self):
        rows = stage_dashboard_rows(
            target_stage="p1",
            device_ids=["dev_1"],
            readiness_report={
                "stage_status": {"p0": {"ok": True}, "p1": {"ok": False}},
                "blockers": [{"name": "field_evidence"}],
                "claims": {"real_ios_control_verified": False, "ios_group_control_verified": False},
            },
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_stage_dashboard_markdown(
                rows,
                Path(tmp) / "dashboard.md",
                target_stage="p1",
                run_id="p1_dash",
                evidence_path="evidence/p1_dash.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Stage Dashboard P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)

    def test_stage_sop_rows_surface_stage_blockers(self):
        rows = stage_sop_rows(
            stage="p1",
            device_ids=[],
            route_report={"ok": False, "ready": False, "blockers": [{"name": "route"}]},
            doctor_report={"overall": "fail", "counts": {"ok": 1, "warn": 0, "fail": 1}},
            evidence_exists=False,
            command_queue_items=[{"action": "click", "device_ids": ["dev_1"], "x": 10, "y": 20}],
            template_asset_rows_data=[
                {"name": "flat.png", "status": "fail", "reason": "low_texture", "size": "24x24", "path": "templates/flat.png"},
            ],
            acceptance_report={"gate": "p1", "ok": False, "checks": [{"name": "manual_observation", "status": "fail"}]},
            readiness_report={"target": "p1", "ok": False, "stage_status": {"p1": {"ok": False}}, "blockers": [{"name": "field_evidence"}]},
        )
        by_stream = {row["workstream"]: row for row in rows}
        brief = stage_sop_brief(rows, stage="p1")

        self.assertEqual(by_stream["Device scope"]["status"], "fail")
        self.assertEqual(by_stream["Route decision"]["status"], "fail")
        self.assertEqual(by_stream["Probe script"]["status"], "ready")
        self.assertEqual(by_stream["Vision assets"]["status"], "fail")
        self.assertIn("SOP board P1", brief)
        self.assertIn("Device scope", brief)

    def test_stage_sop_next_command_maps_rows_to_gui_methods(self):
        self.assertEqual(
            stage_sop_next_command({"workstream": "Route decision"})["method"],
            "edit_route_decision_from_gui",
        )
        self.assertEqual(
            stage_sop_next_command({"workstream": "Probe script", "status": "pending"})["method"],
            "load_probe_script_from_gui",
        )
        queue_command = stage_sop_next_command(
            {"workstream": "Probe script", "status": "pending"},
            queue_has_items=True,
        )
        self.assertEqual(queue_command["label"], "Run Queue")
        self.assertEqual(queue_command["method"], "run_command_queue_from_gui")
        self.assertEqual(
            stage_sop_next_command({"workstream": "Promotion review", "status": "pass"})["method"],
            "write_gui_session_snapshot_from_gui",
        )

    def test_write_stage_sop_markdown(self):
        rows = stage_sop_rows(
            stage="p1",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            scenario_summary={"ok": True, "total": 1, "success_count": 1, "failure_count": 0},
            evidence_exists=True,
            evidence_summary={"total": 2, "by_status": {"pass": 2, "fail": 0, "info": 0, "skip": 0}},
            template_asset_rows_data=[
                {"name": "ok.png", "status": "ok", "reason": "ok", "size": "32x32", "path": "templates/ok.png"},
            ],
            acceptance_report={"gate": "p1", "ok": True, "checks": []},
            readiness_report={"target": "p1", "ok": True, "stage_status": {"p1": {"ok": True}}, "blockers": []},
        )
        with TemporaryDirectory() as tmp:
            out = write_stage_sop_markdown(
                rows,
                Path(tmp) / "sop.md",
                run_id="p1_sop",
                stage="p1",
                evidence_path="evidence/p1_sop.jsonl",
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI SOP Board P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("Primary GUI command", text)
        self.assertIn("Capture/control evidence", text)

    def test_field_runbook_rows_surface_operator_stop_rules(self):
        rows = field_runbook_rows(
            stage="p3",
            device_ids=["dev_1", "dev_2"],
            route_report={"ok": True, "ready": True, "target_stage": "p3", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            scenario_summary={"ok": True, "total": 2, "success_count": 2, "failure_count": 0},
            acceptance_report={
                "gate": "p3",
                "ok": False,
                "checks": [
                    {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                    {"name": "screenshot_quality", "status": "pass", "message": "optional for p3"},
                    {"name": "metrics", "status": "fail", "message": "0 metrics sample(s), required >= 1"},
                ],
            },
            readiness_report={"target": "p3", "ok": False, "stage_status": {"p3": {"ok": False}}},
            evidence_exists=True,
            evidence_summary={"total": 5, "by_status": {"pass": 5, "fail": 0}, "metrics": {"count": 0}},
            template_asset_rows_data=[
                {"name": "flat.png", "status": "fail", "reason": "low_texture", "size": "24x24", "path": "templates/flat.png"},
            ],
        )
        by_phase = {row["phase"]: row for row in rows}
        brief = field_runbook_brief(rows, stage="p3")

        self.assertEqual(by_phase["Bench scope"]["status"], "fail")
        self.assertEqual(by_phase["Route ledger"]["status"], "pass")
        self.assertEqual(by_phase["Receiver/capture"]["status"], "pass")
        self.assertEqual(by_phase["Vision assets"]["status"], "fail")
        self.assertEqual(by_phase["Real-run guard"]["status"], "fail")
        self.assertEqual(by_phase["Stability metrics"]["status"], "fail")
        self.assertIn("first_stop=Bench scope", brief)

    def test_write_field_runbook_markdown(self):
        rows = field_runbook_rows(
            stage="p1",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            acceptance_report={
                "gate": "p1",
                "ok": True,
                "checks": [
                    {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                    {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    {"name": "metrics", "status": "pass", "message": "0 metrics sample(s), required >= 0"},
                ],
            },
            readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 3, "by_status": {"pass": 3, "fail": 0}, "metrics": {"count": 0}},
            template_asset_rows_data=[
                {"name": "ok.png", "status": "ok", "reason": "ok", "size": "32x32", "path": "templates/ok.png"},
            ],
        )
        with TemporaryDirectory() as tmp:
            out = write_field_runbook_markdown(
                rows,
                Path(tmp) / "runbook.md",
                run_id="p1_runbook",
                stage="p1",
                evidence_path="evidence/p1_runbook.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Field Runbook P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("operator guide", text)
        self.assertIn("Promotion requires clean JSONL evidence", text)

    def test_p1_trial_rows_surface_real_device_stop_rules(self):
        rows = p1_trial_rows(
            device_ids=[],
            route_report={"ok": False, "ready": False, "blockers": [{"name": "route"}]},
            doctor_report={"overall": "fail", "counts": {"ok": 1, "warn": 0, "fail": 1}},
            acceptance_report={
                "gate": "p1",
                "ok": False,
                "checks": [
                    {"name": "manual_observation", "status": "fail", "message": "0 manual pass"},
                    {"name": "screenshot_quality", "status": "fail", "message": "0 screenshot pass"},
                ],
            },
            readiness_report={"target": "p1", "ok": False, "stage_status": {"p1": {"ok": False}}},
            evidence_exists=False,
            callback_rows_data=[],
        )
        by_lane = {row["lane"]: row for row in rows}
        brief = p1_trial_brief(rows)

        self.assertEqual(by_lane["Bench ledger"]["status"], "fail")
        self.assertEqual(by_lane["Route gate"]["status"], "fail")
        self.assertEqual(by_lane["Preflight"]["status"], "fail")
        self.assertEqual(by_lane["Receiver/capture"]["status"], "fail")
        self.assertEqual(by_lane["Log triage"]["status"], "pending")
        self.assertIn("first_stop=Bench ledger", brief)

    def test_write_p1_trial_markdown(self):
        rows = p1_trial_rows(
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            acceptance_report={
                "gate": "p1",
                "ok": True,
                "checks": [
                    {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                    {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                ],
            },
            readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 4, "by_status": {"pass": 4, "fail": 0}},
            callback_rows_data=[
                {"event": "device_registered", "severity": "info"},
                {"event": "hardware_bound", "severity": "info"},
            ],
        )
        with TemporaryDirectory() as tmp:
            out = write_p1_trial_markdown(
                rows,
                Path(tmp) / "p1_trial.md",
                run_id="p1_trial",
                evidence_path="evidence/p1_trial.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        by_lane = {row["lane"]: row for row in rows}
        self.assertEqual(by_lane["Bench ledger"]["status"], "pass")
        self.assertEqual(by_lane["HID swipe"]["status"], "ready")
        self.assertEqual(by_lane["Log triage"]["status"], "pass")
        self.assertIn("GUI P1 Trial", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("operator checklist", text)

    def test_p1_test_coach_keeps_readiness_boundary_after_manual_lanes_pass(self):
        control_rows = control_response_bench_rows([
            {
                "status": "pass",
                "step": "P1 trial - HID click",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "tap opened target"},
            },
            {
                "status": "pass",
                "step": "P1 trial - HID swipe",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "list moved"},
            },
            {
                "status": "pass",
                "step": "P1 trial - Keyboard input",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "imouse-smoke visible"},
            },
        ])
        rows = p1_test_coach_rows(
            run_id="p1_coach",
            stage="p1",
            device_ids=["dev_1"],
            action_map_rows=[{"key": "source_to_evidence_boundary", "status": "warn"}],
            local_rows=[{"check": "unit tests", "status": "ready"}],
            kit_rows=[{"gate": "kit", "status": "pass"}],
            ios_sop_rows=[{"check": "ios", "status": "pass"}],
            control_bench_rows_data=control_rows,
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            scenario_summary={"ok": True, "steps": [{"status": "pass"}]},
            acceptance_report={
                "gate": "p1",
                "ok": True,
                "checks": [
                    {"name": "manual_observation", "status": "pass", "message": "3 manual pass"},
                    {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                ],
            },
            readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}},
        )
        by_focus = {row["focus"]: row for row in rows}
        brief = p1_test_coach_brief(rows, stage="p1")

        self.assertEqual(by_focus["Run identity and device scope"]["status"], "pass")
        self.assertEqual(by_focus["HID click"]["status"], "pass")
        self.assertEqual(by_focus["HID swipe"]["status"], "pass")
        self.assertEqual(by_focus["Keyboard input"]["status"], "pass")
        self.assertEqual(by_focus["Readiness and handoff"]["status"], "fail")
        self.assertIn("real_ios_verified=False", by_focus["Readiness and handoff"]["current"])
        self.assertIn("first_focus=Source-derived SOP gates", brief)

    def test_write_p1_test_coach_markdown(self):
        rows = p1_test_coach_rows(
            run_id="p1_coach_missing",
            stage="p1",
            device_ids=[],
            route_report=None,
            doctor_report={"overall": "fail", "counts": {"ok": 11, "warn": 7, "fail": 1}},
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_p1_test_coach_markdown(
                rows,
                Path(tmp) / "coach.md",
                run_id="p1_coach_missing",
                stage="p1",
                evidence_path="evidence/p1_coach_missing.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        by_focus = {row["focus"]: row for row in rows}
        self.assertEqual(by_focus["Run identity and device scope"]["status"], "fail")
        self.assertEqual(by_focus["Preflight Doctor"]["status"], "fail")
        self.assertIn("GUI P1 Test Coach P1", text)
        self.assertIn("step-by-step operator guide", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("API/HID command success without visible iPhone response is not a pass", text)
        self.assertIn("python -m imouse.acceptance evidence\\p1_coach_missing.jsonl --gate p1", text)
        self.assertIn("python -m imouse.readiness --target p1 --evidence evidence\\p1_coach_missing.jsonl", text)
        self.assertNotIn("python -m imouse.acceptance --gate p1 --evidence", text)
        self.assertNotIn("--evidence-jsonl", text)

    def test_p1_field_transcript_rows_include_receiver_setup_and_signoff(self):
        coach_rows = p1_test_coach_rows(
            run_id="p1_transcript",
            stage="p1",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            acceptance_report={
                "gate": "p1",
                "ok": False,
                "checks": [
                    {"name": "manual_observation", "status": "pending", "message": "manual missing"},
                    {"name": "screenshot_quality", "status": "pass", "message": "screenshot ok"},
                ],
            },
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 3, "by_status": {"pass": 3, "fail": 0}},
        )
        receiver_rows = [
            {
                "step": "3. Lock one receiver lane",
                "status": "pass",
                "route": "windows_receiver",
            },
            {
                "step": "8. iPhone to receiver binding",
                "status": "pending",
                "route": "windows_receiver",
            },
        ]

        rows = p1_field_transcript_rows(
            run_id="p1_transcript",
            stage="p1",
            coach_rows=coach_rows,
            receiver_setup_rows=receiver_rows,
            evidence_exists=True,
            evidence_summary={"total": 3, "by_status": {"pass": 3, "fail": 0}},
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
        )
        by_checkpoint = {row["checkpoint"]: row for row in rows}
        brief = p1_field_transcript_brief(rows, stage="p1")

        self.assertEqual(by_checkpoint["Transcript header"]["status"], "pass")
        self.assertEqual(by_checkpoint["Receiver setup split"]["status"], "pending")
        self.assertEqual(by_checkpoint["HID click"]["failure_categories"], "hid, calibration, business_state")
        self.assertIn("physical iPhone", by_checkpoint["HID click"]["observation_prompt"])
        self.assertEqual(by_checkpoint["Operator sign-off"]["status"], "pending")
        self.assertIn("first_checkpoint=Receiver setup split", brief)

    def test_write_p1_field_transcript_markdown_keeps_manual_boundary(self):
        coach_rows = p1_test_coach_rows(
            run_id="p1_transcript_missing",
            stage="p1",
            device_ids=[],
            route_report=None,
            doctor_report={"overall": "fail", "counts": {"ok": 11, "warn": 7, "fail": 1}},
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        rows = p1_field_transcript_rows(
            run_id="p1_transcript_missing",
            stage="p1",
            coach_rows=coach_rows,
            receiver_setup_rows=[],
            evidence_exists=False,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
        )
        with TemporaryDirectory() as tmp:
            out = write_p1_field_transcript_markdown(
                rows,
                Path(tmp) / "transcript.md",
                run_id="p1_transcript_missing",
                stage="p1",
                evidence_path="evidence/p1_transcript_missing.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("P1 Field Transcript P1", text)
        self.assertIn("fillable operator log", text)
        self.assertIn("does not record Manual pass by itself", text)
        self.assertIn("Record what the physical iPhone did", text)
        self.assertIn("--evidence evidence\\p1_transcript_missing.jsonl", text)
        self.assertNotIn("--evidence-jsonl", text)

    def test_p1_transcript_manual_prefill_only_passes_control_rows(self):
        control = p1_transcript_manual_prefill(
            {
                "checkpoint": "HID click",
                "current": "manual pending",
                "observation_prompt": "watch physical iPhone",
                "expected": "tap opens target",
                "failure_categories": "hid, calibration",
                "artifact": "screenshots/p1_click.png",
            },
            requested_status="pass",
        )
        setup = p1_transcript_manual_prefill(
            {
                "checkpoint": "Route Decision",
                "current": "route ready",
                "observation_prompt": "record command output",
                "expected": "route is ready",
                "failure_categories": "route_decision, binding",
                "artifact": "evidence/p1_route_decision.md",
            },
            requested_status="pass",
        )
        fail = p1_transcript_manual_prefill(
            {
                "checkpoint": "HID swipe",
                "current": "swipe failed",
                "observation_prompt": "watch physical iPhone",
                "expected": "content moves",
                "failure_categories": "hid, calibration",
                "artifact": "logs/hid.log",
            },
            requested_status="fail",
        )

        self.assertEqual(control["status"], "pass")
        self.assertEqual(control["category"], "")
        self.assertEqual(control["artifact"], "screenshots/p1_click.png")
        self.assertEqual(control["control_checkpoint"], "true")
        self.assertEqual(setup["status"], "info")
        self.assertEqual(setup["control_checkpoint"], "false")
        self.assertIn("not click/swipe/text control", setup["note"])
        self.assertEqual(fail["status"], "fail")
        self.assertEqual(fail["category"], "hid")
        self.assertEqual(fail["artifact"], "logs/hid.log")

    def test_gui_control_center_rows_surface_first_blocker(self):
        rows = gui_control_center_rows(
            stage="p1",
            device_ids=[],
            route_report={"ok": False, "ready": False, "blockers": [{"name": "route"}]},
            doctor_report={"overall": "fail", "counts": {"ok": 1, "warn": 0, "fail": 1}},
            acceptance_report={
                "gate": "p1",
                "ok": False,
                "checks": [
                    {"name": "manual_observation", "status": "fail", "message": "0 manual pass"},
                    {"name": "screenshot_quality", "status": "fail", "message": "0 screenshot pass"},
                ],
            },
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "missing"},
                {"name": "Doctor Report", "requirement": "required", "status": "missing"},
            ],
            callback_rows_data=[],
            live_probe_rows_data=[{"status": "fail"}],
            sop_rows_data=[{"status": "pending"}],
        )
        by_domain = {row["domain"]: row for row in rows}
        brief = gui_control_center_brief(rows, stage="p1")

        self.assertEqual(by_domain["Stage and device scope"]["status"], "fail")
        self.assertEqual(by_domain["Route and hardware gate"]["status"], "fail")
        self.assertEqual(by_domain["Live iPhone evidence"]["status"], "fail")
        self.assertEqual(by_domain["Evidence pack and SOP docs"]["status"], "fail")
        self.assertIn("first_blocker=Stage and device scope", brief)

    def test_write_gui_control_center_markdown(self):
        rows = gui_control_center_rows(
            stage="p1",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            scenario_summary={"ok": True, "steps": 2, "failed": 0},
            acceptance_report={
                "gate": "p1",
                "ok": True,
                "checks": [
                    {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                    {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                ],
            },
            readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}},
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "present"},
                {"name": "Doctor Report", "requirement": "required", "status": "present"},
                {"name": "GUI Control Center", "requirement": "recommended", "status": "missing"},
            ],
            callback_rows_data=[{"event": "hid_ack", "severity": "info"}],
            live_probe_rows_data=[{"status": "pass"}],
            sop_rows_data=[{"status": "pass"}],
            template_asset_rows_data=[{"status": "ok"}],
        )
        with TemporaryDirectory() as tmp:
            out = write_gui_control_center_markdown(
                rows,
                Path(tmp) / "center.md",
                run_id="p1_center",
                stage="p1",
                evidence_path="evidence/p1_center.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        by_domain = {row["domain"]: row for row in rows}
        self.assertEqual(by_domain["Promotion claim boundary"]["status"], "warn")
        self.assertIn("GUI Control Center P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("operator dashboard", text)

    def test_gui_knowledge_center_rows_surface_missing_docs_and_route(self):
        with TemporaryDirectory() as tmp:
            rows = gui_knowledge_center_rows(
                stage="p1",
                docs_root=tmp,
                route_report=None,
                doctor_report=None,
                acceptance_report=None,
                readiness_report=None,
                evidence_exists=False,
                xp_gap_audit=None,
            )

        by_topic = {row["topic"]: row for row in rows}
        brief = gui_knowledge_center_brief(rows, stage="p1")

        self.assertEqual(by_topic["XP public product model"]["status"], "fail")
        self.assertEqual(by_topic["P1 receiver/HID decision"]["status"], "fail")
        self.assertEqual(by_topic["Claim boundary"]["status"], "fail")
        self.assertIn("first_blocker=XP public product model", brief)

    def test_write_gui_knowledge_center_markdown(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/imouse_xp_research.md",
                "docs/industry_landscape_2026.md",
                "docs/mainstream_route_decision.md",
                "docs/ios_group_control_sop.md",
                "docs/hardware_test_bench_checklist.md",
                "docs/xp_api_compat.md",
                "docs/imouse_xp_iteration_lessons.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = gui_knowledge_center_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={"gate": "p1", "ok": True, "checks": []},
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}},
                xp_gap_audit={"rows": [{"domain": "Receiver/Capture", "status": "blocked"}]},
            )
            out = write_gui_knowledge_center_markdown(
                rows,
                root / "knowledge.md",
                run_id="p1_knowledge",
                stage="p1",
                evidence_path="evidence/p1_knowledge.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        by_topic = {row["topic"]: row for row in rows}
        self.assertEqual(by_topic["XP API and helper parity"]["status"], "warn")
        self.assertEqual(by_topic["Claim boundary"]["status"], "warn")
        self.assertIn("GUI Knowledge Center P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)

    def test_industry_current_snapshot_rows_keep_offline_status_unproven(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/industry_current_state_snapshot_2026.md",
                "docs/mainstream_route_decision.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/ios_field_settings_sop.md",
                "docs/xp_event_error_contract.md",
                "docs/script_runner.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = industry_current_snapshot_rows(
                stage="p1",
                docs_root=root,
                route_report=None,
                doctor_report=None,
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                evidence_summary={},
            )
            brief = industry_current_snapshot_brief(rows, stage="p1")

        by_area = {row["area"]: row for row in rows}
        self.assertEqual(by_area["Current public-source snapshot"]["status"], "ready")
        self.assertIn("public claim to test", by_area["Current public-source snapshot"]["current_signal"])
        self.assertIn("not local coverage", by_area["Current public-source snapshot"]["current_signal"])
        self.assertEqual(by_area["Mainstream route choice"]["status"], "pending")
        self.assertEqual(by_area["Receiver/capture barrier"]["status"], "pending")
        self.assertEqual(by_area["HID and hardware barrier"]["status"], "pending")
        self.assertEqual(by_area["Group failure isolation"]["status"], "pending")
        self.assertEqual(by_area["Claim boundary"]["status"], "fail")
        self.assertIn("first_focus=Mainstream route choice", brief)

    def test_industry_current_snapshot_keeps_claim_boundary_when_real_ios_missing(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/industry_current_state_snapshot_2026.md",
                "docs/mainstream_route_decision.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/ios_field_settings_sop.md",
                "docs/xp_event_error_contract.md",
                "docs/script_runner.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = industry_current_snapshot_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                        {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}, "metrics": {"count": 1}},
            )

        by_area = {row["area"]: row for row in rows}
        self.assertEqual(by_area["Mainstream route choice"]["status"], "ready")
        self.assertEqual(by_area["Receiver/capture barrier"]["status"], "ready")
        self.assertEqual(by_area["HID and hardware barrier"]["status"], "warn")
        self.assertEqual(by_area["Vision/OCR asset replay"]["status"], "ready")
        self.assertEqual(by_area["Claim boundary"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_area["Claim boundary"]["current"])

    def test_write_industry_current_snapshot_markdown_keeps_boundary(self):
        rows = industry_current_snapshot_rows(
            stage="p1",
            docs_root=".",
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_industry_current_snapshot_markdown(
                rows,
                Path(tmp) / "snapshot.md",
                run_id="p1_snapshot",
                stage="p1",
                evidence_path="evidence/p1_snapshot.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Industry Current Snapshot P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("does not prove real iPhone response", text)
        self.assertIn("Use Snapshot before Routes", text)

    def test_industry_sop_radar_rows_keep_current_state_separate_from_proof(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/industry_sop_radar.md",
                "docs/xp_public_source_refresh.md",
                "docs/ios_group_control_sop.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/xp_api_compat.md",
                "docs/script_runner.md",
                "docs/validation_evidence.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = industry_sop_radar_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                        {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}},
                xp_gap_audit={
                    "rows": [
                        {"domain": "Kernel/API", "status": "pass"},
                        {"domain": "Python SDK", "status": "pass"},
                        {"domain": "Receiver/Capture", "status": "pass"},
                        {"domain": "USB/HID", "status": "pass"},
                    ]
                },
                route_matrix_rows=[{"lane": "XP-style black-box route", "status": "ready"}],
                core_rows=[{"domain": "USB/HID control", "status": "warn"}],
            )
            brief = industry_sop_radar_brief(rows, stage="p1")

        by_topic = {row["topic"]: row for row in rows}
        self.assertEqual(by_topic["Mainstream route boundary"]["status"], "ready")
        self.assertEqual(by_topic["iMouse XP product boundary"]["status"], "warn")
        self.assertEqual(by_topic["Receiver/capture product lane"]["status"], "ready")
        self.assertEqual(by_topic["HID hardware and firmware lane"]["status"], "warn")
        self.assertEqual(by_topic["API and SDK compatibility lane"]["status"], "ready")
        self.assertEqual(by_topic["Claim and compliance boundary"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_topic["HID hardware and firmware lane"]["current"])
        self.assertIn("first_focus=iMouse XP product boundary", brief)

    def test_industry_sop_radar_blocks_receiver_and_hid_when_doctor_fails(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/industry_sop_radar.md",
                "docs/xp_public_source_refresh.md",
                "docs/ios_group_control_sop.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/xp_api_compat.md",
                "docs/script_runner.md",
                "docs/validation_evidence.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = industry_sop_radar_rows(
                stage="p1",
                docs_root=root,
                route_report=None,
                doctor_report={"overall": "fail", "counts": {"ok": 11, "warn": 7, "fail": 1}},
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                xp_gap_audit={"rows": [{"domain": "Kernel/API", "status": "pass"}]},
            )

        by_topic = {row["topic"]: row for row in rows}
        self.assertEqual(by_topic["Receiver/capture product lane"]["status"], "fail")
        self.assertEqual(by_topic["HID hardware and firmware lane"]["status"], "fail")
        self.assertEqual(by_topic["API and SDK compatibility lane"]["status"], "ready")
        self.assertIn("doctor=fail", by_topic["Receiver/capture product lane"]["current"])

    def test_write_industry_sop_radar_markdown(self):
        rows = industry_sop_radar_rows(
            stage="p1",
            docs_root=".",
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_industry_sop_radar_markdown(
                rows,
                Path(tmp) / "industry.md",
                run_id="p1_industry",
                stage="p1",
                evidence_path="evidence/p1_industry.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Industry SOP Radar P1", text)
        self.assertIn("Mainstream route boundary", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("does not prove iOS control", text)

    def test_industry_route_procurement_blocks_missing_route_and_buying(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/mainstream_route_decision.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/gui_xp_hardware_lab.md",
                "docs/ios_field_settings_sop.md",
                "docs/hardware_test_bench_checklist.md",
                "docs/xp_public_source_refresh.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = industry_route_procurement_rows(
                stage="p1",
                docs_root=root,
                device_ids=[],
                route_decision=None,
                route_report=None,
                doctor_report=None,
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                evidence_summary={},
                route_matrix_rows=[],
                xp_lab_rows=[],
            )
            brief = industry_route_procurement_brief(rows, stage="p1")

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["route_lock"]["status"], "pending")
        self.assertEqual(by_key["receiver_procurement"]["status"], "pending")
        self.assertEqual(by_key["hid_procurement"]["status"], "pending")
        self.assertEqual(by_key["xp_parity_purchase"]["status"], "pending")
        self.assertEqual(by_key["source_refresh_contract"]["status"], "ready")
        self.assertIn("Route Decision not loaded", by_key["route_lock"]["current"])
        self.assertIn("first_focus=Mainstream route lock", brief)

    def test_industry_route_procurement_keeps_generic_hid_from_xp_parity(self):
        route = decision_template(run_id="procure_ch9329", devices=["dev_1"])
        route["receiver"].update({
            "route": "windows_receiver",
            "name": "WinReceiver",
            "version": "1.2.3",
            "path": "C:/receiver",
            "start_command": "receiver.exe --name LabRX",
            "airplay_name": "LabRX",
            "capture_method": "window",
        })
        route["hid"].update({
            "route": "ch9329",
            "provider": "CH9329",
            "id": "hid-001",
            "firmware": "fw-1",
            "serial_port": "COM5",
            "baudrate": 9600,
        })
        route["iphone"].update({
            "id": "ip01",
            "model": "iPhone 15",
            "ios_version": "17.7",
            "orientation": "portrait",
            "assistive_touch": "on",
            "pointer_speed": "medium",
        })
        route["bench"].update({
            "device_id": "dev_1",
            "hub_id": "hub-1",
            "hub_port": "port-1",
            "cable_id": "cable-1",
            "network": "lab-wifi",
            "operator": "op-1",
        })
        route["decision"].update({"allowed_to_run_p1": True, "open_blockers": []})
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/mainstream_route_decision.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/gui_xp_hardware_lab.md",
                "docs/ios_field_settings_sop.md",
                "docs/hardware_test_bench_checklist.md",
                "docs/xp_public_source_refresh.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = industry_route_procurement_rows(
                stage="p1",
                docs_root=root,
                device_ids=["dev_1"],
                route_decision=route,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "manual ok"},
                        {"name": "screenshot_quality", "status": "pass", "message": "shot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}, "metrics": {"count": 1}},
                route_matrix_rows=[{"lane": "XP-style black-box route", "status": "ready", "selected": "yes"}],
                xp_lab_rows=[{"lane": "XP dedicated hardware parity", "status": "pending"}],
            )

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["route_lock"]["status"], "ready")
        self.assertEqual(by_key["receiver_procurement"]["status"], "ready")
        self.assertEqual(by_key["hid_procurement"]["status"], "warn")
        self.assertEqual(by_key["xp_parity_purchase"]["status"], "warn")
        self.assertEqual(by_key["iphone_fixture_matrix"]["status"], "ready")
        self.assertEqual(by_key["claim_and_scale_stop"]["status"], "warn")
        self.assertIn("generic HID route", by_key["xp_parity_purchase"]["current"])
        self.assertIn("real_ios_verified=False", by_key["claim_and_scale_stop"]["current"])

    def test_write_industry_route_procurement_markdown_keeps_claim_boundary(self):
        rows = industry_route_procurement_rows(
            stage="p1",
            docs_root=".",
            route_decision=None,
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_industry_route_procurement_markdown(
                rows,
                Path(tmp) / "procure.md",
                run_id="p1_procure",
                stage="p1",
                evidence_path="evidence/p1_procure.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Route Procurement SOP P1", text)
        self.assertIn("Vendor questions", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("does not prove real iPhone response", text)

    def test_mainstream_route_matrix_rows_surface_route_decision_gap(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/industry_sop_playbook.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")

            rows = mainstream_route_matrix_rows(
                stage="p1",
                docs_root=root,
                route_decision=None,
                route_report=None,
                doctor_report=None,
                acceptance_report=None,
                readiness_report=None,
                evidence_exists=False,
            )

        by_lane = {row["lane"]: row for row in rows}
        brief = mainstream_route_matrix_brief(rows, stage="p1")

        self.assertEqual(by_lane["XP-style black-box route"]["status"], "pending")
        self.assertEqual(by_lane["WDA/Appium/XCUITest"]["status"], "warn")
        self.assertEqual(by_lane["MDM/Configurator/Shortcuts"]["status"], "warn")
        self.assertIn("selected=none", brief)
        self.assertIn("first_focus=XP-style black-box route", brief)

    def test_mainstream_route_matrix_keeps_generic_hid_separate_from_xp_hardware(self):
        route = decision_template(run_id="route_matrix", devices=["dev_1"])
        apply_route_decision_form_values(route, {
            "receiver.route": "windows_receiver",
            "receiver.name": "WinReceiver",
            "receiver.capture_method": "window",
            "hid.route": "ch9329",
            "hid.serial_or_device": "COM5",
            "decision.allowed_to_run_p1": "true",
            "decision.open_blockers": "",
        })
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/industry_sop_playbook.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = mainstream_route_matrix_rows(
                stage="p1",
                docs_root=root,
                route_decision=route,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                        {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}},
            )
            out = write_mainstream_route_matrix_markdown(
                rows,
                root / "routes.md",
                run_id="route_matrix",
                stage="p1",
                evidence_path="evidence/route_matrix.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        by_lane = {row["lane"]: row for row in rows}
        self.assertEqual(by_lane["XP-style black-box route"]["status"], "ready")
        self.assertEqual(by_lane["Windows receiver/window capture"]["status"], "pass")
        self.assertEqual(by_lane["CH9329/general USB HID"]["status"], "pass")
        self.assertEqual(by_lane["XP dedicated hardware"]["status"], "warn")
        self.assertIn("GUI Mainstream Route Matrix P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("WDA/Appium/XCUITest", text)

    def test_mainstream_route_matrix_xp_hardware_requires_side_by_side_evidence(self):
        route = decision_template(run_id="xp_hw_matrix", devices=["dev_1"])
        apply_route_decision_form_values(route, {
            "receiver.route": "wired",
            "receiver.name": "VendorWired",
            "receiver.capture_method": "sdk",
            "hid.route": "xp_hardware",
            "hid.serial_or_device": "XP-HW-001",
            "decision.allowed_to_run_p1": "true",
            "decision.open_blockers": "",
        })
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/industry_sop_playbook.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = mainstream_route_matrix_rows(
                stage="p1",
                docs_root=root,
                route_decision=route,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                        {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}},
            )

        by_lane = {row["lane"]: row for row in rows}
        self.assertEqual(by_lane["Wired projection/vendor SDK"]["status"], "pass")
        self.assertEqual(by_lane["XP dedicated hardware"]["status"], "ready")
        self.assertIn("side_by_side_xp_parity_evidence=missing", by_lane["XP dedicated hardware"]["current"])
        self.assertNotEqual(by_lane["XP dedicated hardware"]["status"], "pass")

    def test_xp_core_function_matrix_keeps_api_ready_but_control_unverified(self):
        route = decision_template(run_id="core_matrix", devices=["dev_1"])
        apply_route_decision_form_values(route, {
            "receiver.route": "windows_receiver",
            "receiver.name": "WinReceiver",
            "receiver.capture_method": "window",
            "hid.route": "ch9329",
            "hid.serial_or_device": "COM5",
            "decision.allowed_to_run_p1": "true",
            "decision.open_blockers": "",
        })
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/xp_parity_matrix.md",
                "docs/xp_api_compat.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/coordinate_calibration.md",
                "docs/validation_evidence.md",
                "docs/script_runner.md",
                "docs/gui_prototype.md",
                "docs/xp_core_backlog.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_core_function_matrix_rows(
                stage="p1",
                docs_root=root,
                route_decision=route,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                        {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}},
                xp_gap_audit={
                    "rows": [
                        {"domain": "Kernel/API", "status": "pass"},
                        {"domain": "Python SDK", "status": "pass"},
                        {"domain": "Receiver/Capture", "status": "pass"},
                        {"domain": "USB/HID", "status": "pass"},
                        {"domain": "Mouse/Keyboard", "status": "pass"},
                        {"domain": "Coordinate Calibration", "status": "pass"},
                        {"domain": "Vision/Image/Color", "status": "pass"},
                        {"domain": "OCR", "status": "pass"},
                        {"domain": "Script Runtime", "status": "pass"},
                        {"domain": "GUI Console", "status": "pass"},
                        {"domain": "Observability", "status": "pass"},
                        {"domain": "Commercial/Ops", "status": "not_started"},
                    ]
                },
            )
            brief = xp_core_function_matrix_brief(rows, stage="p1")

        by_domain = {row["domain"]: row for row in rows}
        self.assertEqual(by_domain["Kernel/API and WebSocket"]["status"], "ready")
        self.assertEqual(by_domain["Python SDK/helper"]["status"], "ready")
        self.assertEqual(by_domain["Screenshot acquisition"]["status"], "pass")
        self.assertEqual(by_domain["USB/HID control"]["status"], "warn")
        self.assertEqual(by_domain["Mouse/keyboard input"]["status"], "warn")
        self.assertEqual(by_domain["Config/user/shortcut compatibility"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_domain["USB/HID control"]["current_gate"])
        self.assertIn("first_focus=XP-style product route", brief)

    def test_xp_core_function_matrix_blocks_receiver_and_hid_when_doctor_fails(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/xp_parity_matrix.md",
                "docs/xp_api_compat.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/coordinate_calibration.md",
                "docs/validation_evidence.md",
                "docs/script_runner.md",
                "docs/gui_prototype.md",
                "docs/xp_core_backlog.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_core_function_matrix_rows(
                stage="p1",
                docs_root=root,
                route_decision=None,
                route_report=None,
                doctor_report={"overall": "fail", "counts": {"ok": 11, "warn": 7, "fail": 1}},
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                xp_gap_audit={
                    "rows": [
                        {"domain": "Receiver/Capture", "status": "pass"},
                        {"domain": "USB/HID", "status": "pass"},
                        {"domain": "Mouse/Keyboard", "status": "pass"},
                    ]
                },
            )

        by_domain = {row["domain"]: row for row in rows}
        self.assertEqual(by_domain["Receiver/capture route"]["status"], "fail")
        self.assertEqual(by_domain["USB/HID control"]["status"], "fail")
        self.assertEqual(by_domain["Mouse/keyboard input"]["status"], "fail")
        self.assertIn("doctor=fail", by_domain["Receiver/capture route"]["current_gate"])

    def test_write_xp_core_function_matrix_markdown(self):
        rows = xp_core_function_matrix_rows(
            stage="p1",
            docs_root=".",
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            xp_gap_audit={"rows": [{"domain": "Kernel/API", "status": "pass"}]},
        )
        with TemporaryDirectory() as tmp:
            out = write_xp_core_function_matrix_markdown(
                rows,
                Path(tmp) / "core.md",
                run_id="p1_core",
                stage="p1",
                evidence_path="evidence/p1_core.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("XP Core Function Matrix P1", text)
        self.assertIn("Kernel/API and WebSocket", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("does not prove XP parity", text)

    def test_xp_api_coverage_board_keeps_local_api_p0_only(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/xp_api_compat.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/xp_event_error_contract.md",
                "docs/xp_core_backlog.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_api_coverage_board_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "generic manual pass"},
                        {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}},
                callback_rows_data=[],
                xp_gap_audit={
                    "rows": [
                        {"domain": "Kernel/API", "status": "pass"},
                        {"domain": "Receiver/Capture", "status": "pass"},
                        {"domain": "USB/HID", "status": "pass"},
                        {"domain": "Mouse/Keyboard", "status": "pass"},
                        {"domain": "Vision/Image/Color", "status": "pass"},
                        {"domain": "OCR", "status": "pass"},
                        {"domain": "Device/Group", "status": "pass"},
                        {"domain": "Script Runtime", "status": "pass"},
                        {"domain": "Observability", "status": "pass"},
                        {"domain": "Commercial/Ops", "status": "not_started"},
                    ]
                },
            )
            brief = xp_api_coverage_board_brief(rows, stage="p1")

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["api_envelope"]["status"], "ready")
        self.assertEqual(by_key["api_envelope"]["support_state"], "p0_api_covered")
        self.assertIn("P0 API compatibility", by_key["api_envelope"]["current"])
        self.assertEqual(by_key["receiver_airplay_capture"]["status"], "ready")
        self.assertEqual(by_key["usb_hid_binding"]["status"], "warn")
        self.assertEqual(by_key["mouse_control"]["status"], "warn")
        self.assertEqual(by_key["keyboard_text"]["status"], "warn")
        self.assertEqual(by_key["mouse_control"]["support_state"], "lane_manual_required")
        self.assertIn("Local CH9329", by_key["usb_hid_binding"]["claim_boundary"])
        self.assertIn("first_focus=USB/HID binding", brief)

    def test_xp_api_coverage_board_marks_scaffolding_and_backlog(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/xp_api_compat.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/xp_event_error_contract.md",
                "docs/xp_core_backlog.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_api_coverage_board_rows(
                stage="p1",
                docs_root=root,
                route_report=None,
                doctor_report=None,
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                callback_rows_data=[],
                xp_gap_audit={"rows": [{"domain": "Commercial/Ops", "status": "not_started"}]},
            )

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["config_user_shortcut"]["status"], "warn")
        self.assertEqual(by_key["config_user_shortcut"]["support_state"], "scaffolding_only")
        self.assertIn("no XP cloud", by_key["config_user_shortcut"]["current"])
        self.assertEqual(by_key["cloud_ops"]["status"], "pending")
        self.assertEqual(by_key["cloud_ops"]["support_state"], "backlog_only")
        self.assertIn("deferred backlog", by_key["cloud_ops"]["current"])

    def test_xp_api_coverage_board_surfaces_callbacks_without_control_proof(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in ("docs/xp_api_compat.md", "docs/xp_event_error_contract.md"):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_api_coverage_board_rows(
                stage="p1",
                docs_root=root,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                callback_rows_data=[
                    {"event": "receiver_error", "source": "attach_log", "severity": "error", "detail": "black frame"}
                ],
                xp_gap_audit={"rows": [{"domain": "Observability", "status": "pass"}]},
            )

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["callback_event"]["status"], "warn")
        self.assertEqual(by_key["logs_triage"]["status"], "warn")
        self.assertIn("not control proof", by_key["callback_event"]["current"])
        self.assertIn("attach_log_seen=True", by_key["logs_triage"]["current"])

    def test_write_xp_api_coverage_board_markdown(self):
        rows = xp_api_coverage_board_rows(
            stage="p1",
            docs_root=".",
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            callback_rows_data=[],
            xp_gap_audit={"rows": [{"domain": "Kernel/API", "status": "pass"}]},
        )
        with TemporaryDirectory() as tmp:
            out = write_xp_api_coverage_board_markdown(
                rows,
                Path(tmp) / "api_coverage.md",
                run_id="p1_api",
                stage="p1",
                evidence_path="evidence/p1_api.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("XP API Coverage Board P1", text)
        self.assertIn("API envelope and transport", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("A local helper test can close only a P0 compatibility row", text)

    def test_script_coverage_board_keeps_dry_run_p0_only(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/script_runner.md",
                "docs/verification_plan.md",
                "docs/validation_evidence.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/sop_problem_ledger.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = script_coverage_board_rows(
                stage="p1",
                docs_root=root,
                scenario_rows_data=[
                    {
                        "name": "P1 probe",
                        "stage": "p1",
                        "path": "scripts/p1_single_device_control_probe.json",
                        "status": "ok",
                        "actions": "call=2, click=1, metrics=2, record=5, repeat=1, screenshot=1, swipe=1, type=1, wait=3",
                    },
                    {
                        "name": "P3 group",
                        "stage": "p3",
                        "path": "scripts/pilot_4_group_smoke.json",
                        "status": "ok",
                        "actions": "call=5, group_click=1, group_swipe=1, group_type=1, record=1",
                    },
                ],
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                scenario_summary={"ok": True, "total": 12, "success_count": 12, "failure_count": 0},
                guard_report={"stage": "p1", "ok": True, "blockers": [], "checks": []},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "generic manual pass"},
                        {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                        {"name": "metrics", "status": "pass", "message": "1 metrics sample"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}, "metrics": {"count": 1}},
            )

        by_key = {row["key"]: row for row in rows}
        brief = script_coverage_board_brief(rows, stage="p1")

        self.assertEqual(by_key["scenario_inventory"]["status"], "ready")
        self.assertEqual(by_key["dry_run_contract"]["status"], "ready")
        self.assertEqual(by_key["real_run_guard"]["status"], "ready")
        self.assertEqual(by_key["receiver_screenshot"]["status"], "ready")
        self.assertEqual(by_key["hid_control_lanes"]["status"], "warn")
        self.assertEqual(by_key["hid_control_lanes"]["support_state"], "readiness_boundary_open")
        self.assertIn("real_ios_verified=False", by_key["hid_control_lanes"]["current"])
        self.assertEqual(by_key["claim_boundary"]["status"], "warn")
        self.assertIn("dry_run_or_script_success_is_not_control_proof", by_key["claim_boundary"]["current"])
        self.assertIn("Script coverage P1", brief)

    def test_script_coverage_board_blocks_real_run_when_guard_fails(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/script_runner.md",
                "docs/verification_plan.md",
                "docs/validation_evidence.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/sop_problem_ledger.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = script_coverage_board_rows(
                stage="p1",
                docs_root=root,
                scenario_rows_data=[{
                    "name": "P1 probe",
                    "stage": "p1",
                    "path": "scripts/p1_single_device_control_probe.json",
                    "status": "ok",
                    "actions": "click=1, record=1, repeat=1, screenshot=1, swipe=1, type=1",
                }],
                scenario_summary=None,
                guard_report={
                    "stage": "p1",
                    "ok": False,
                    "blockers": [{"name": "route_decision"}, {"name": "doctor"}],
                    "checks": [],
                },
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
            )

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["dry_run_contract"]["status"], "pending")
        self.assertEqual(by_key["real_run_guard"]["status"], "fail")
        self.assertEqual(by_key["real_run_guard"]["support_state"], "guard_blocked")
        self.assertIn("blockers=2", by_key["real_run_guard"]["current"])
        self.assertEqual(by_key["claim_boundary"]["status"], "warn")

    def test_write_script_coverage_board_markdown(self):
        rows = script_coverage_board_rows(
            stage="p1",
            docs_root=".",
            scenario_rows_data=[{
                "name": "P1 probe",
                "stage": "p1",
                "path": "scripts/p1_single_device_control_probe.json",
                "status": "ok",
                "actions": "click=1, record=1, repeat=1, screenshot=1, swipe=1, type=1",
            }],
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_script_coverage_board_markdown(
                rows,
                Path(tmp) / "script_coverage.md",
                run_id="p1_script",
                stage="p1",
                evidence_path="evidence/p1_script.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Script Coverage Board P1", text)
        self.assertIn("Scenario inventory and stage defaults", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not run scripts, write JSONL evidence", text)
        self.assertIn("A dry-run, scenario summary, API success, or GUI queue can close only script readiness", text)

    def test_acceptance_proof_map_links_failed_checks_to_gui_actions(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/follow_along_test_method.md",
                "docs/receiver_capture_selection.md",
                "docs/validation_evidence.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/gui_control_evidence_ledger.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/readiness_audit.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = acceptance_proof_map_rows(
                run_id="proof_missing",
                stage="p1",
                docs_root=root,
                device_ids=[],
                route_report=None,
                doctor_report={"overall": "fail", "counts": {"ok": 1, "warn": 0, "fail": 1}},
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                evidence_summary={},
            )

        by_key = {row["key"]: row for row in rows}
        brief = acceptance_proof_map_brief(rows, stage="p1")

        self.assertEqual(by_key["run_scope"]["status"], "fail")
        self.assertEqual(by_key["route_doctor"]["status"], "fail")
        self.assertEqual(by_key["evidence_exists"]["status"], "fail")
        self.assertEqual(by_key["readiness_gate"]["status"], "fail")
        self.assertIn("Open Runner", by_key["evidence_exists"]["gui_action"])
        self.assertIn("imouse.acceptance", by_key["manual_observation"]["next_command"])
        self.assertIn("first_focus=run_scope", brief)

    def test_acceptance_proof_map_keeps_lane_passes_inside_claim_boundary(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/follow_along_test_method.md",
                "docs/receiver_capture_selection.md",
                "docs/validation_evidence.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/gui_control_evidence_ledger.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/readiness_audit.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = acceptance_proof_map_rows(
                run_id="proof_lanes",
                stage="p1",
                docs_root=root,
                device_ids=["dev_1"],
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "evidence_exists", "status": "pass", "message": "events loaded"},
                        {"name": "no_fail_events", "status": "pass", "message": "0 fail event(s)"},
                        {"name": "device_traceability", "status": "pass", "message": "1 device"},
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "manual ok"},
                        {"name": "screenshot_quality", "status": "pass", "message": "shot ok"},
                        {"name": "metrics", "status": "pass", "message": "0 metrics sample(s)"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}, "metrics": {"count": 0}},
                control_ledger_rows_data=[
                    {"lane": "HID click", "status": "pass"},
                    {"lane": "HID swipe", "status": "pass"},
                    {"lane": "Keyboard input", "status": "pass"},
                ],
            )

        by_key = {row["key"]: row for row in rows}

        self.assertEqual(by_key["run_scope"]["status"], "pass")
        self.assertEqual(by_key["route_doctor"]["status"], "pass")
        self.assertEqual(by_key["lane_separation"]["status"], "warn")
        self.assertEqual(by_key["readiness_gate"]["status"], "warn")
        self.assertEqual(by_key["claim_boundary"]["status"], "warn")
        self.assertIn("lane_pass=3/3", by_key["lane_separation"]["current"])
        self.assertIn("real_ios_verified=False", by_key["claim_boundary"]["current"])

    def test_write_acceptance_proof_map_markdown(self):
        rows = acceptance_proof_map_rows(
            run_id="proof_md",
            stage="p1",
            docs_root=".",
            device_ids=["dev_1"],
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_acceptance_proof_map_markdown(
                rows,
                Path(tmp) / "proof_map.md",
                run_id="proof_md",
                stage="p1",
                evidence_path="evidence/proof_md.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Acceptance Proof Map P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not run scripts, write JSONL evidence", text)
        self.assertIn("lane-separated Manual click/swipe/text observations", text)
        self.assertIn("imouse.readiness --target p1", text)

    def test_claim_scope_limits_offline_assets_to_p0_wording(self):
        rows = claim_scope_rows(
            run_id="claim_p0",
            stage="p1",
            device_ids=[],
            route_report=None,
            doctor_report={"overall": "fail", "counts": {"ok": 1, "warn": 0, "fail": 1}},
            acceptance_report=None,
            readiness_report={
                "target": "p1",
                "ok": False,
                "claims": {
                    "offline_assets_ready": True,
                    "real_ios_control_verified": False,
                    "ios_group_control_verified": False,
                },
            },
            evidence_exists=False,
            evidence_summary={},
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "missing"},
                {"name": "Doctor Report", "requirement": "required", "status": "missing"},
            ],
        )
        by_area = {row["claim_area"]: row for row in rows}
        brief = claim_scope_brief(rows, stage="p1")

        self.assertEqual(by_area["P0 offline assets"]["status"], "pass")
        self.assertEqual(by_area["P1 single-iPhone control"]["status"], "fail")
        self.assertEqual(by_area["P3/P4 iOS group control"]["status"], "pending")
        self.assertEqual(by_area["XP hardware, wired, firmware and decode parity"]["status"], "fail")
        self.assertEqual(by_area["Docs and SOP handoff wording"]["status"], "fail")
        self.assertIn("not a field-control claim", by_area["P0 offline assets"]["handoff_text"])
        self.assertIn("iOS perfect control", by_area["P1 single-iPhone control"]["forbidden_claim"])
        self.assertIn("strongest=P0 offline assets", brief)

    def test_claim_scope_keeps_p1_blocked_when_gates_pass_without_real_ios_claim(self):
        rows = claim_scope_rows(
            run_id="claim_boundary",
            stage="p1",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            acceptance_report={
                "gate": "p1",
                "ok": True,
                "checks": [
                    {"name": "manual_observation", "status": "pass", "message": "manual ok"},
                    {"name": "screenshot_quality", "status": "pass", "message": "shot ok"},
                    {"name": "component_traceability", "status": "pass", "message": "component ok"},
                ],
            },
            readiness_report={
                "target": "p1",
                "ok": True,
                "claims": {
                    "offline_assets_ready": True,
                    "real_ios_control_verified": False,
                    "ios_group_control_verified": False,
                },
                "stage_status": {
                    "p1": {"ok": True},
                    "p2": {"ok": False},
                    "p3": {"ok": False},
                    "p4": {"ok": False},
                },
            },
            evidence_exists=True,
            evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}, "metrics": {"count": 0}},
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "present"},
                {"name": "Doctor Report", "requirement": "required", "status": "present"},
                {"name": "Acceptance Report", "requirement": "required", "status": "present"},
                {"name": "Readiness Report", "requirement": "required", "status": "present"},
            ],
            proof_map_rows=[{"key": "claim_boundary", "status": "warn"}],
            core_rows=[{"domain": "USB/HID control", "status": "pass"}],
            api_coverage_rows=[{"domain": "Mouse/key/touch actions", "status": "pass"}],
            compatibility_rows=[{"coverage_key": "iPhone 13 / 17.7", "status": "pass"}],
        )
        by_area = {row["claim_area"]: row for row in rows}
        brief = claim_scope_brief(rows, stage="p1")

        self.assertEqual(by_area["P1 single-iPhone control"]["status"], "warn")
        self.assertNotEqual(by_area["P1 single-iPhone control"]["status"], "pass")
        self.assertEqual(by_area["XP API/SDK compatibility"]["status"], "ready")
        self.assertEqual(by_area["Docs and SOP handoff wording"]["status"], "ready")
        self.assertIn("real_ios_verified=False", by_area["P1 single-iPhone control"]["current_scope"])
        self.assertIn("unverified field control", by_area["P1 single-iPhone control"]["allowed_claim"])
        self.assertIn("XP-equivalent control", by_area["P1 single-iPhone control"]["forbidden_claim"])
        self.assertIn("first_focus=P1 single-iPhone control", brief)

    def test_write_claim_scope_markdown(self):
        rows = claim_scope_rows(
            run_id="claim_md",
            stage="p1",
            device_ids=["dev_1"],
            readiness_report={
                "target": "p1",
                "ok": False,
                "claims": {"real_ios_control_verified": False, "ios_group_control_verified": False},
            },
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_claim_scope_markdown(
                rows,
                Path(tmp) / "claim_scope.md",
                run_id="claim_md",
                stage="p1",
                evidence_path="evidence/claim_md.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False, "ios_group_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Claim Scope P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("iOS group control verified: `False`", text)
        self.assertIn("writes claim wording guidance only", text)
        self.assertIn("does not write JSONL evidence and does not prove real iPhone response", text)
        self.assertIn("iOS perfect control", text)

    def test_xp_event_error_contract_rows_surface_callbacks_and_error_boundaries(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/xp_api_compat.md",
                "docs/xp_event_error_contract.md",
                "docs/sop_problem_ledger.md",
                "docs/script_runner.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_event_error_contract_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={"gate": "p1", "ok": True, "checks": []},
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={
                    "total": 4,
                    "by_status": {"pass": 3, "fail": 1},
                    "by_failure_category": {"hid": 1},
                },
                callback_rows_data=[{
                    "seq": "1",
                    "event": "hid_error",
                    "source": "attach_log",
                    "severity": "error",
                    "detail": "no response",
                }],
                xp_gap_audit={
                    "rows": [
                        {"domain": "Kernel/API", "status": "pass"},
                        {"domain": "USB/HID", "status": "pass"},
                        {"domain": "Observability", "status": "partial"},
                    ]
                },
            )

        by_key = {row["key"]: row for row in rows}
        brief = xp_event_error_contract_brief(rows, stage="p1")

        self.assertEqual(by_key["api_envelope"]["status"], "ready")
        self.assertEqual(by_key["callback_lifecycle"]["status"], "warn")
        self.assertEqual(by_key["receiver_hid_capture_errors"]["status"], "warn")
        self.assertEqual(by_key["field_log_ingestion"]["status"], "warn")
        self.assertEqual(by_key["config_user_shortcut_boundary"]["status"], "warn")
        self.assertEqual(by_key["claim_boundary"]["status"], "warn")
        self.assertIn("first_focus=Callback/event lifecycle", brief)
        self.assertIn("callbacks=1", by_key["callback_lifecycle"]["current"])
        self.assertIn("related_failures=1", by_key["receiver_hid_capture_errors"]["current"])

    def test_write_xp_event_error_contract_markdown(self):
        rows = xp_event_error_contract_rows(
            stage="p1",
            docs_root=".",
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            callback_rows_data=[],
            xp_gap_audit={"rows": [{"domain": "Kernel/API", "status": "pass"}]},
        )
        with TemporaryDirectory() as tmp:
            out = write_xp_event_error_contract_markdown(
                rows,
                Path(tmp) / "events.md",
                run_id="p1_events",
                stage="p1",
                evidence_path="evidence/p1_events.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("XP Event/Error Contract P1", text)
        self.assertIn("Callback/event lifecycle", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("does not prove XP parity", text)

    def test_verification_walkthrough_rows_surface_step_by_step_blockers(self):
        rows = verification_walkthrough_rows(
            run_id="verify_missing",
            stage="p1",
            device_ids=[],
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "missing"},
                {"name": "Doctor Report", "requirement": "required", "status": "missing"},
            ],
            core_rows=[],
            route_matrix_rows=[],
        )
        by_key = {row["key"]: row for row in rows}
        brief = verification_walkthrough_brief(rows, stage="p1")

        self.assertEqual(by_key["offline_self_check"]["status"], "ready")
        self.assertEqual(by_key["run_identity"]["status"], "fail")
        self.assertEqual(by_key["route_decision"]["status"], "pending")
        self.assertEqual(by_key["handoff_pack"]["status"], "fail")
        self.assertIn("first_focus=Run identity and device scope", brief)
        self.assertIn("--target p1", by_key["acceptance_readiness"]["command"])

    def test_verification_walkthrough_keeps_real_ios_boundary_when_gates_look_clean(self):
        rows = verification_walkthrough_rows(
            run_id="verify_cleanish",
            stage="p1",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            acceptance_report={
                "gate": "p1",
                "ok": True,
                "checks": [
                    {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                    {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                    {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                ],
            },
            readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}},
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "present"},
                {"name": "Doctor Report", "requirement": "required", "status": "present"},
                {"name": "Verification Walkthrough", "requirement": "recommended", "status": "missing"},
            ],
            core_rows=[{"domain": "USB/HID control", "status": "warn"}],
            route_matrix_rows=[{"lane": "XP-style black-box route", "status": "ready"}],
        )
        by_key = {row["key"]: row for row in rows}

        self.assertEqual(by_key["receiver_capture"]["status"], "pass")
        self.assertEqual(by_key["hid_manual_control"]["status"], "warn")
        self.assertEqual(by_key["acceptance_readiness"]["status"], "warn")
        self.assertEqual(by_key["xp_parity_review"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_key["hid_manual_control"]["current"])

    def test_write_verification_walkthrough_markdown(self):
        rows = verification_walkthrough_rows(
            run_id="verify_md",
            stage="p1",
            device_ids=[],
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_verification_walkthrough_markdown(
                rows,
                Path(tmp) / "verify.md",
                run_id="verify_md",
                stage="p1",
                evidence_path="evidence/verify_md.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Verification Walkthrough P1", text)
        self.assertIn("python -m unittest discover -s tests -v", text)
        self.assertIn("python -m imouse.readiness --target p1 --evidence evidence\\verify_md.jsonl", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("does not prove real iPhone response", text)

    def test_local_verification_rows_surface_command_by_command_blockers(self):
        rows = local_verification_rows(
            run_id="local_missing",
            stage="p1",
            route_report=None,
            doctor_report={
                "overall": "fail",
                "counts": {"ok": 11, "warn": 7, "fail": 1},
                "checks": [
                    {
                        "name": "binary:uxplay",
                        "status": "fail",
                        "message": "uxplay MISSING",
                    }
                ],
            },
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            evidence_summary={"total": 0, "by_status": {}},
        )
        by_key = {row["key"]: row for row in rows}
        brief = local_verification_brief(rows, stage="p1")

        self.assertEqual(by_key["unit_tests"]["status"], "ready")
        self.assertEqual(by_key["compileall"]["status"], "ready")
        self.assertEqual(by_key["dependency_check"]["status"], "warn")
        self.assertIn("uxplay MISSING", by_key["dependency_check"]["current"])
        self.assertEqual(by_key["doctor_default"]["status"], "fail")
        self.assertEqual(by_key["doctor_route"]["status"], "pending")
        self.assertEqual(by_key["readiness_p1"]["status"], "fail")
        self.assertIn("first_focus=Dependency check", brief)

    def test_local_verification_rows_include_route_aware_doctor_command(self):
        rows = local_verification_rows(
            run_id="local_route",
            stage="p1",
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={
                "overall": "warn",
                "counts": {"ok": 1, "warn": 1, "fail": 0},
                "checks": [
                    {
                        "name": "receiver_provider",
                        "status": "ok",
                        "message": "Receiver provider ready for preflight: windows_receiver",
                    },
                    {
                        "name": "binary:uxplay",
                        "status": "warn",
                        "message": "UxPlay not required for selected receiver route: windows_receiver",
                    },
                ],
            },
            scenario_summary={"ok": True, "steps": [{"ok": True}]},
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            route_decision_path="evidence\\local_route_route_decision.json",
        )
        by_key = {row["key"]: row for row in rows}

        self.assertEqual(by_key["doctor_route"]["status"], "warn")
        self.assertIn("--route-decision evidence\\local_route_route_decision.json", by_key["doctor_route"]["command"])
        self.assertIn("--dry-run --run-id local_route", by_key["scenario_dry_run"]["command"])
        self.assertIn("--target p1 --evidence evidence\\local_route.jsonl", by_key["readiness_p1"]["command"])
        self.assertEqual(by_key["scenario_dry_run"]["status"], "pass")
        self.assertIn("Open Receiver", by_key["doctor_route"]["gui_action"])

    def test_write_local_verification_markdown_keeps_claim_boundary(self):
        rows = local_verification_rows(
            run_id="local_md",
            stage="p1",
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
        )
        with TemporaryDirectory() as tmp:
            out = write_local_verification_markdown(
                rows,
                Path(tmp) / "local.md",
                run_id="local_md",
                stage="p1",
                evidence_path="evidence/local_md.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Local Verification P1", text)
        self.assertIn("python -m unittest discover -s tests -v", text)
        self.assertIn("python -m imouse.doctor --route-decision", text)
        self.assertIn("python -m imouse.readiness --target p1 --evidence evidence\\local_md.jsonl", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("does not prove real iOS control", text)

    def test_xp_public_source_ledger_rows_keep_public_claims_as_unverified(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/imouse_xp_research.md",
                "docs/xp_public_source_refresh.md",
                "docs/xp_api_compat.md",
                "docs/xp_parity_matrix.md",
                "docs/imouse_xp_iteration_lessons.md",
                "docs/ios_field_settings_sop.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_public_source_ledger_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={"gate": "p1", "ok": True, "checks": []},
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}},
                xp_gap_audit={"rows": [{"domain": "Receiver/Capture", "status": "blocked"}]},
            )
            out = write_xp_public_source_ledger_markdown(
                rows,
                root / "sources.md",
                run_id="p1_sources",
                stage="p1",
                evidence_path="evidence/p1_sources.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        by_key = {row["key"]: row for row in rows}
        brief = xp_public_source_ledger_brief(rows, stage="p1")

        self.assertEqual(by_key["official_current_support_claim"]["status"], "warn")
        self.assertEqual(by_key["python_xp_helper"]["status"], "fail")
        self.assertEqual(by_key["pypi_imouse_py_release"]["status"], "warn")
        self.assertIn("package exists", by_key["pypi_imouse_py_release"]["verification_gap"])
        self.assertEqual(by_key["official_first_config_mouse_params"]["status"], "warn")
        self.assertEqual(by_key["claim_boundary"]["status"], "warn")
        self.assertIn("first_focus=official_product_model", brief)
        self.assertIn("XP Public Source Ledger P1", text)
        self.assertIn("https://www.imouse.cc/", text)
        self.assertIn("https://pypi.org/project/imouse-py/", text)
        self.assertIn("official_first_config_mouse_params", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("does not prove XP parity", text)

    def test_xp_source_refresh_rows_keep_source_freshness_separate_from_evidence(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/imouse_xp_research.md",
                "docs/xp_api_compat.md",
                "docs/imouse_xp_iteration_lessons.md",
                "docs/xp_public_source_action_map.md",
                "docs/ios_field_settings_sop.md",
                "docs/industry_sop_radar.md",
                "docs/xp_public_source_refresh.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_source_refresh_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={"gate": "p1", "ok": True, "checks": []},
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 4, "by_status": {"pass": 4, "fail": 0}},
                xp_gap_audit={"rows": [{"domain": "Receiver/Capture", "status": "blocked"}]},
            )
            out = write_xp_source_refresh_markdown(
                rows,
                root / "source_refresh.md",
                run_id="p1_refresh",
                stage="p1",
                evidence_path="evidence/p1_refresh.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        by_key = {row["key"]: row for row in rows}
        brief = xp_source_refresh_brief(rows, stage="p1")

        self.assertEqual(by_key["official_homepage_refresh"]["status"], "warn")
        self.assertEqual(by_key["official_api_refresh"]["status"], "warn")
        self.assertEqual(by_key["package_registry_refresh"]["status"], "warn")
        self.assertEqual(by_key["source_to_sop_commit"]["status"], "ready")
        self.assertEqual(by_key["source_claim_boundary_refresh"]["status"], "fail")
        self.assertIn("first_focus=official_homepage_refresh", brief)
        self.assertIn("XP Source Refresh Board P1", text)
        self.assertIn("does not browse automatically", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("does not prove XP parity", text)
        self.assertIn("Package Namespace Guard", text)
        self.assertIn("https://pypi.org/project/imouse-xp/", text)
        self.assertIn("https://pypi.org/project/py-imouse-xp/", text)
        self.assertIn("dependency-confusion", text)
        self.assertIn("do not install lookalike packages", text)

    def test_xp_package_namespace_guard_rows_keep_package_ok_as_warn(self):
        report = {
            "overall": "ok",
            "rows": [
                {
                    "key": "pypi_imouse_py",
                    "status": "ok",
                    "url": "https://pypi.org/pypi/imouse-py/json",
                    "version": "0.0.4",
                    "summary": "imouse xp client-server helper",
                    "project_urls": "Homepage=https://www.imouse.cc/",
                    "claim_boundary": "Package metadata is supply-chain intelligence.",
                },
                {
                    "key": "pypi_imouse_xp",
                    "status": "ok",
                    "url": "https://pypi.org/pypi/imouse-xp/json",
                    "version": "0.0.7",
                    "summary": "similar package namespace",
                    "project_urls": "",
                    "claim_boundary": "Do not adopt similar package names without review.",
                },
                {
                    "key": "pypi_py_imouse_xp",
                    "status": "pending",
                    "url": "https://pypi.org/pypi/py-imouse-xp/json",
                    "version": "",
                    "summary": "",
                    "project_urls": "",
                    "claim_boundary": "Do not adopt similar package names without review.",
                },
            ],
        }
        rows = xp_package_namespace_guard_rows(report)
        by_package = {row["package"]: row for row in rows}
        brief = xp_package_namespace_guard_brief(rows, stage="p1")

        self.assertEqual(by_package["imouse-py"]["status"], "warn")
        self.assertEqual(by_package["imouse-py"]["source_status"], "ok")
        self.assertEqual(by_package["imouse-xp"]["status"], "warn")
        self.assertEqual(by_package["py-imouse-xp"]["status"], "pending")
        self.assertIn("official Python XP install target", by_package["imouse-py"]["identity"])
        self.assertIn("dependency-confusion", by_package["imouse-xp"]["identity"])
        self.assertIn("never write JSONL evidence", by_package["imouse-py"]["claim_boundary"])
        self.assertIn("first_focus=imouse-py", brief)

    def test_write_xp_package_namespace_guard_markdown(self):
        rows = xp_package_namespace_guard_rows({
            "overall": "warn",
            "rows": [
                {
                    "key": "pypi_imouse_py",
                    "status": "ok",
                    "url": "https://pypi.org/pypi/imouse-py/json",
                    "version": "0.0.4",
                    "summary": "imouse xp client-server helper",
                    "project_urls": "Homepage=https://www.imouse.cc/",
                    "claim_boundary": "Package metadata is supply-chain intelligence.",
                },
                {
                    "key": "pypi_imouse_xp",
                    "status": "ok",
                    "url": "https://pypi.org/pypi/imouse-xp/json",
                    "version": "0.0.7",
                    "summary": "similar package namespace",
                    "project_urls": "",
                    "claim_boundary": "Do not adopt similar package names without review.",
                },
                {
                    "key": "pypi_py_imouse_xp",
                    "status": "ok",
                    "url": "https://pypi.org/pypi/py-imouse-xp/json",
                    "version": "1.0.1",
                    "summary": "similar package namespace",
                    "project_urls": "",
                    "claim_boundary": "Treat as third-party until reviewed.",
                },
            ],
        })
        with TemporaryDirectory() as tmp:
            out = write_xp_package_namespace_guard_markdown(
                rows,
                Path(tmp) / "package_guard.md",
                run_id="p1_pkg",
                stage="p1",
                source_audit_overall="warn",
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("XP Package Namespace Guard P1", text)
        self.assertIn("imouse-py", text)
        self.assertIn("imouse-xp", text)
        self.assertIn("py-imouse-xp", text)
        self.assertIn("does not install packages", text)
        self.assertIn("Package import success is never screenshot freshness", text)

    def test_xp_public_source_action_map_rows_turn_sources_into_sop_gates(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            action_doc = root / "docs/xp_public_source_action_map.md"
            action_doc.parent.mkdir(parents=True, exist_ok=True)
            action_doc.write_text("ok", encoding="utf-8")
            rows = xp_public_source_action_map_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": False, "ready": False, "target_stage": "p1", "blockers": ["receiver"]},
                doctor_report={"overall": "fail", "counts": {"ok": 11, "warn": 7, "fail": 1}},
                acceptance_report={"gate": "p1", "ok": False, "checks": []},
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                evidence_summary={},
                xp_gap_audit={"rows": [{"domain": "Receiver/Capture", "status": "blocked"}]},
            )
            out = write_xp_public_source_action_map_markdown(
                rows,
                root / "action_map.md",
                run_id="p1_action",
                stage="p1",
                evidence_path="evidence/p1_action.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        by_key = {row["key"]: row for row in rows}
        brief = xp_public_source_action_map_brief(rows, stage="p1")

        self.assertEqual(by_key["xp_product_model"]["status"], "fail")
        self.assertEqual(by_key["receiver_capture_route"]["status"], "fail")
        self.assertEqual(by_key["python_sdk_hardware_boundary"]["status"], "fail")
        self.assertEqual(by_key["package_registry_boundary"]["status"], "warn")
        self.assertEqual(by_key["group_ops_productization"]["status"], "pending")
        self.assertEqual(by_key["source_to_evidence_boundary"]["status"], "fail")
        self.assertIn("Stop perfect-control", by_key["xp_product_model"]["stop_rule"])
        self.assertIn("Open Receiver", by_key["receiver_capture_route"]["gui_owner"])
        self.assertIn("first_focus=xp_product_model", brief)
        self.assertIn("XP Public Source Action Map P1", text)
        self.assertIn("R&D decision", text)
        self.assertIn("SOP gate", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("does not prove real iPhone control", text)

    def test_xp_iteration_radar_rows_prioritize_field_proof(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/imouse_xp_iteration_lessons.md",
                "docs/xp_api_compat.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/xp_core_backlog.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_iteration_radar_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={"gate": "p1", "ok": True, "checks": []},
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 5, "by_status": {"pass": 5, "fail": 0}},
                xp_gap_audit={
                    "rows": [
                        {"domain": "Kernel/API", "status": "pass"},
                        {"domain": "Python SDK", "status": "partial"},
                        {"domain": "Receiver/Capture", "status": "partial"},
                        {"domain": "USB/HID", "status": "blocked"},
                        {"domain": "Vision/Image/Color", "status": "partial"},
                        {"domain": "Script Runtime", "status": "partial"},
                        {"domain": "Observability", "status": "partial"},
                    ]
                },
            )
            brief = xp_iteration_radar_brief(rows, stage="p1")

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["p1_black_box_control"]["status"], "warn")
        self.assertEqual(by_key["receiver_capture_evolution"]["status"], "warn")
        self.assertEqual(by_key["xp_hardware_binding"]["status"], "fail")
        self.assertEqual(by_key["claim_boundary"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_key["xp_hardware_binding"]["current_gap"])
        self.assertIn("first_focus=P1 black-box control", brief)

    def test_write_xp_iteration_radar_markdown(self):
        rows = xp_iteration_radar_rows(
            stage="p1",
            docs_root=".",
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            xp_gap_audit={"rows": [{"domain": "USB/HID", "status": "blocked"}]},
        )
        with TemporaryDirectory() as tmp:
            out = write_xp_iteration_radar_markdown(
                rows,
                Path(tmp) / "iteration_radar.md",
                run_id="p1_radar",
                stage="p1",
                evidence_path="evidence/p1_radar.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("XP Iteration Radar P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("Do not turn public XP iteration claims into product claims", text)

    def test_xp_iteration_timeline_rows_keep_offline_evolution_unproven(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/imouse_xp_iteration_lessons.md",
                "docs/xp_api_compat.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/script_runner.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_iteration_timeline_rows(
                stage="p1",
                docs_root=root,
                route_report=None,
                doctor_report=None,
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                evidence_summary={},
                xp_gap_audit={"rows": [{"domain": "Kernel/API", "status": "pass"}]},
            )
            brief = xp_iteration_timeline_brief(rows, stage="p1")

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["black_box_product_model"]["status"], "pending")
        self.assertEqual(by_key["kernel_console_api_split"]["status"], "warn")
        self.assertEqual(by_key["receiver_projection_productization"]["status"], "pending")
        self.assertEqual(by_key["firmware_wired_binding"]["status"], "pending")
        self.assertEqual(by_key["ops_logs_group_scale"]["status"], "pending")
        self.assertIn("first_focus=No-app black-box control", brief)

    def test_xp_iteration_timeline_keeps_claim_boundary_when_real_ios_missing(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/imouse_xp_iteration_lessons.md",
                "docs/xp_api_compat.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/script_runner.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_iteration_timeline_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "manual_observation", "status": "pass", "message": "manual ok"},
                        {"name": "screenshot_quality", "status": "pass", "message": "shot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}, "metrics": {"count": 1}},
                xp_gap_audit={
                    "rows": [
                        {"domain": "Kernel/API", "status": "pass"},
                        {"domain": "Python SDK", "status": "pass"},
                        {"domain": "Receiver/Capture", "status": "pass"},
                        {"domain": "USB/HID", "status": "pass"},
                        {"domain": "Mouse/Keyboard", "status": "pass"},
                        {"domain": "Vision/Image/Color", "status": "pass"},
                        {"domain": "Script Runtime", "status": "pass"},
                        {"domain": "Observability", "status": "pass"},
                    ]
                },
            )

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["black_box_product_model"]["status"], "warn")
        self.assertEqual(by_key["receiver_projection_productization"]["status"], "ready")
        self.assertEqual(by_key["firmware_wired_binding"]["status"], "fail")
        self.assertEqual(by_key["vision_script_assets"]["status"], "ready")
        self.assertEqual(by_key["source_claim_governance"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_key["source_claim_governance"]["current"])
        self.assertIn("side-by-side XP hardware", by_key["firmware_wired_binding"]["stop_rule"])

    def test_write_xp_iteration_timeline_markdown_keeps_boundary(self):
        rows = xp_iteration_timeline_rows(
            stage="p1",
            docs_root=".",
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            evidence_summary={},
        )
        with TemporaryDirectory() as tmp:
            out = write_xp_iteration_timeline_markdown(
                rows,
                Path(tmp) / "timeline.md",
                run_id="p1_xp_timeline",
                stage="p1",
                evidence_path="evidence/p1_xp_timeline.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("XP Iteration Timeline P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("does not prove XP parity", text)
        self.assertIn("Timeline Rows", text)

    def test_xp_architecture_map_rows_keep_offline_layers_unproven(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/imouse_xp_architecture_map.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/receiver_capture_selection.md",
                "docs/script_runner.md",
                "docs/xp_api_compat.md",
                "docs/gui_prototype.md",
                "docs/validation_evidence.md",
                "docs/p2_p3_stability_runbook.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_architecture_map_rows(
                stage="p1",
                docs_root=root,
                route_report=None,
                doctor_report=None,
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                evidence_summary={},
                xp_gap_audit={"rows": [{"domain": "Kernel/API", "status": "pass"}]},
            )
            brief = xp_architecture_map_brief(rows, stage="p1")

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["kernel_api"]["status"], "ready")
        self.assertEqual(by_key["hardware_usb_hid"]["status"], "fail")
        self.assertEqual(by_key["projection_receiver"]["status"], "pending")
        self.assertEqual(by_key["capture_vision"]["status"], "pending")
        self.assertEqual(by_key["evidence_readiness"]["status"], "fail")
        self.assertIn("real_ios_verified=False", by_key["hardware_usb_hid"]["current"])
        self.assertIn("first_focus=Product boundary", brief)

    def test_xp_architecture_map_keeps_xp_parity_separate_after_local_api_ready(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/imouse_xp_architecture_map.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/receiver_capture_selection.md",
                "docs/script_runner.md",
                "docs/xp_api_compat.md",
                "docs/gui_prototype.md",
                "docs/validation_evidence.md",
                "docs/p2_p3_stability_runbook.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_architecture_map_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "manual ok"},
                        {"name": "screenshot_quality", "status": "pass", "message": "shot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}, "metrics": {"count": 0}},
                xp_gap_audit={
                    "rows": [
                        {"domain": "Kernel/API", "status": "pass"},
                        {"domain": "Python SDK", "status": "pass"},
                        {"domain": "Receiver/Capture", "status": "pass"},
                        {"domain": "USB/HID", "status": "pass"},
                        {"domain": "Mouse/Keyboard", "status": "pass"},
                        {"domain": "Vision/Image/Color", "status": "partial"},
                        {"domain": "Observability", "status": "pass"},
                    ]
                },
            )

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["kernel_api"]["status"], "ready")
        self.assertEqual(by_key["python_sdk"]["status"], "ready")
        self.assertEqual(by_key["projection_receiver"]["status"], "ready")
        self.assertEqual(by_key["hardware_usb_hid"]["status"], "fail")
        self.assertEqual(by_key["evidence_readiness"]["status"], "warn")
        self.assertIn("XP hardware/4.4/auto-binding unverified", by_key["hardware_usb_hid"]["current"])

    def test_write_xp_architecture_map_markdown_keeps_claim_boundary(self):
        rows = xp_architecture_map_rows(
            stage="p1",
            docs_root=".",
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            evidence_summary={},
            xp_gap_audit={"rows": [{"domain": "Kernel/API", "status": "pass"}]},
        )
        with TemporaryDirectory() as tmp:
            out = write_xp_architecture_map_markdown(
                rows,
                Path(tmp) / "xp_architecture.md",
                run_id="p1_arch",
                stage="p1",
                evidence_path="evidence/p1_arch.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("XP Architecture Map P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not prove real iPhone response", text)
        self.assertIn("does not prove XP parity", text)
        self.assertIn("Architecture Layers", text)

    def test_xp_hardware_lab_rows_keep_missing_route_blocked(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/mainstream_route_decision.md",
                "docs/receiver_capture_selection.md",
                "docs/imouse_xp_iteration_lessons.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/ios_field_settings_sop.md",
                "docs/hardware_test_bench_checklist.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/xp_event_error_contract.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_hardware_lab_rows(
                stage="p1",
                docs_root=root,
                route_decision=None,
                route_report=None,
                doctor_report=None,
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                evidence_summary={},
            )
            brief = xp_hardware_lab_brief(rows, stage="p1")

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["route_procurement_ledger"]["status"], "pending")
        self.assertEqual(by_key["receiver_capture_rig"]["status"], "pending")
        self.assertEqual(by_key["hid_controller_rig"]["status"], "pending")
        self.assertEqual(by_key["xp_dedicated_hardware_parity"]["status"], "pending")
        self.assertIn("Route Decision is not loaded", by_key["route_procurement_ledger"]["current"])
        self.assertIn("first_focus=Route and procurement ledger", brief)

    def test_xp_hardware_lab_keeps_ch9329_separate_from_xp_hardware(self):
        route = decision_template(run_id="xp_lab_ch9329", devices=["dev_1"])
        route["receiver"].update({
            "route": "windows_receiver",
            "name": "WinReceiver",
            "version": "1.2.3",
            "path": "C:/receiver",
            "start_command": "receiver.exe --name LabRX",
            "airplay_name": "LabRX",
            "capture_method": "window",
            "window_binding": {"title": "LabRX", "process": "receiver.exe", "handle": ""},
        })
        route["hid"].update({
            "route": "ch9329",
            "provider": "CH9329",
            "id": "hid-001",
            "firmware": "fw-1",
            "serial_port": "COM5",
        })
        route["iphone"].update({
            "id": "ip01",
            "model": "iPhone 15",
            "ios_version": "17.7",
            "assistive_touch": "on",
            "pointer_speed": "medium",
        })
        route["bench"].update({
            "device_id": "dev_1",
            "hub_id": "hub-1",
            "hub_port": "port-1",
            "cable_id": "cable-1",
            "operator": "op-1",
        })
        route["decision"].update({"allowed_to_run_p1": True, "open_blockers": []})
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/mainstream_route_decision.md",
                "docs/receiver_capture_selection.md",
                "docs/imouse_xp_iteration_lessons.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/ios_field_settings_sop.md",
                "docs/hardware_test_bench_checklist.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/xp_event_error_contract.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_hardware_lab_rows(
                stage="p1",
                docs_root=root,
                device_ids=["dev_1"],
                route_decision=route,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "manual ok"},
                        {"name": "screenshot_quality", "status": "pass", "message": "shot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}, "metrics": {"count": 1}},
            )

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["receiver_capture_rig"]["status"], "ready")
        self.assertEqual(by_key["hid_controller_rig"]["status"], "warn")
        self.assertEqual(by_key["xp_dedicated_hardware_parity"]["status"], "pending")
        self.assertIn("generic or unset", by_key["xp_dedicated_hardware_parity"]["current"])
        self.assertNotEqual(by_key["xp_dedicated_hardware_parity"]["status"], "pass")

    def test_xp_hardware_lab_xp_hardware_still_needs_side_by_side(self):
        route = decision_template(run_id="xp_lab_xp_hw", devices=["dev_1"])
        route["receiver"].update({
            "route": "wired",
            "name": "VendorWired",
            "version": "2.0",
            "path": "C:/wired",
            "start_command": "wired.exe",
            "airplay_name": "WiredRX",
            "capture_method": "sdk",
        })
        route["hid"].update({
            "route": "xp_hardware",
            "provider": "XP hardware",
            "id": "xp-hw-001",
            "firmware": "4.4",
            "serial_port": "COM6",
        })
        route["iphone"].update({
            "id": "ip01",
            "model": "iPhone 15",
            "ios_version": "17.7",
            "assistive_touch": "on",
            "pointer_speed": "medium",
        })
        route["bench"].update({
            "device_id": "dev_1",
            "hub_id": "hub-1",
            "hub_port": "port-1",
            "cable_id": "cable-1",
            "operator": "op-1",
        })
        route["decision"].update({"allowed_to_run_p1": True, "open_blockers": []})
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/mainstream_route_decision.md",
                "docs/receiver_capture_selection.md",
                "docs/imouse_xp_iteration_lessons.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/ios_field_settings_sop.md",
                "docs/hardware_test_bench_checklist.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/xp_event_error_contract.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_hardware_lab_rows(
                stage="p1",
                docs_root=root,
                device_ids=["dev_1"],
                route_decision=route,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "manual ok"},
                        {"name": "screenshot_quality", "status": "pass", "message": "shot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": True}},
                evidence_exists=True,
                evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}, "metrics": {"count": 1}},
            )

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["hid_controller_rig"]["status"], "ready")
        self.assertEqual(by_key["xp_dedicated_hardware_parity"]["status"], "warn")
        self.assertIn("side-by-side parity is still open", by_key["xp_dedicated_hardware_parity"]["current"])
        self.assertNotEqual(by_key["xp_dedicated_hardware_parity"]["status"], "pass")

    def test_write_xp_hardware_lab_markdown_keeps_claim_boundary(self):
        rows = xp_hardware_lab_rows(
            stage="p1",
            docs_root=".",
            route_decision=None,
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            evidence_summary={},
        )
        with TemporaryDirectory() as tmp:
            out = write_xp_hardware_lab_markdown(
                rows,
                Path(tmp) / "xp_hardware_lab.md",
                run_id="p1_lab",
                stage="p1",
                evidence_path="evidence/p1_lab.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("XP Hardware Lab P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not prove real iPhone response", text)
        self.assertIn("does not prove XP dedicated-hardware parity", text)
        self.assertIn("procurement", text.lower())

    def test_xp_iteration_drill_rows_keep_offline_drills_blocked(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/xp_api_compat.md",
                "docs/ios_field_settings_sop.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/xp_public_source_action_map.md",
                "docs/validation_evidence.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_iteration_drill_rows(
                stage="p1",
                docs_root=root,
                route_report=None,
                doctor_report=None,
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                evidence_summary={},
                xp_gap_audit={"rows": [{"domain": "USB/HID", "status": "blocked"}]},
            )
            brief = xp_iteration_drill_brief(rows, stage="p1")

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["ios_settings_mouse_profile"]["status"], "pending")
        self.assertEqual(by_key["receiver_projection_binding"]["status"], "pending")
        self.assertEqual(by_key["xp_hardware_44_wired_binding"]["status"], "fail")
        self.assertEqual(by_key["restart_projection_logs"]["status"], "pending")
        self.assertEqual(by_key["multi_device_10_projection"]["status"], "pending")
        self.assertNotEqual(by_key["claim_boundary_drill"]["status"], "pass")
        self.assertIn("real_ios_verified=False", by_key["xp_hardware_44_wired_binding"]["current_gap"])
        self.assertIn("first_focus=windows_service_console_split", brief)

    def test_xp_iteration_drill_keeps_claim_boundary_when_real_ios_missing(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/xp_api_compat.md",
                "docs/ios_field_settings_sop.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/xp_public_source_action_map.md",
                "docs/validation_evidence.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_iteration_drill_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "manual ok"},
                        {"name": "screenshot_quality", "status": "pass", "message": "shot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 5, "by_status": {"pass": 5, "fail": 0}, "metrics": {"count": 1}},
                xp_gap_audit={
                    "rows": [
                        {"domain": "Kernel/API", "status": "pass"},
                        {"domain": "Python SDK", "status": "pass"},
                        {"domain": "Receiver/Capture", "status": "pass"},
                        {"domain": "USB/HID", "status": "pass"},
                        {"domain": "Mouse/Keyboard", "status": "pass"},
                        {"domain": "Coordinate Calibration", "status": "pass"},
                        {"domain": "Observability", "status": "pass"},
                    ]
                },
            )

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["windows_service_console_split"]["status"], "ready")
        self.assertEqual(by_key["receiver_projection_binding"]["status"], "ready")
        self.assertEqual(by_key["ios_settings_mouse_profile"]["status"], "warn")
        self.assertEqual(by_key["xp_hardware_44_wired_binding"]["status"], "fail")
        self.assertEqual(by_key["claim_boundary_drill"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_key["claim_boundary_drill"]["current_gap"])
        self.assertIn("side-by-side XP hardware", by_key["xp_hardware_44_wired_binding"]["stop_rule"])

    def test_write_xp_iteration_drill_markdown_keeps_evidence_boundary(self):
        rows = xp_iteration_drill_rows(
            stage="p1",
            docs_root=".",
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            evidence_summary={},
            xp_gap_audit={"rows": [{"domain": "USB/HID", "status": "blocked"}]},
        )
        with TemporaryDirectory() as tmp:
            out = write_xp_iteration_drill_markdown(
                rows,
                Path(tmp) / "iteration_drill.md",
                run_id="p1_drill",
                stage="p1",
                evidence_path="evidence/p1_drill.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("XP Iteration Drill Board P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("does not prove XP parity", text)
        self.assertIn("Failure category", text)

    def test_xp_roadmap_rows_keep_api_ready_but_field_control_unverified(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/xp_api_compat.md",
                "docs/mainstream_route_decision.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/coordinate_calibration.md",
                "docs/xp_public_source_refresh.md",
                "docs/script_runner.md",
                "docs/validation_evidence.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_roadmap_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                        {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}},
                xp_gap_audit={
                    "rows": [
                        {"domain": "Kernel/API", "status": "pass"},
                        {"domain": "Python SDK", "status": "pass"},
                        {"domain": "Receiver/Capture", "status": "pass"},
                        {"domain": "USB/HID", "status": "pass"},
                        {"domain": "Mouse/Keyboard", "status": "pass"},
                        {"domain": "Coordinate Calibration", "status": "pass"},
                        {"domain": "Vision/Image/Color", "status": "partial"},
                        {"domain": "Script Runtime", "status": "partial"},
                        {"domain": "Observability", "status": "pass"},
                    ]
                },
                route_matrix_rows=[{"lane": "XP dedicated hardware", "status": "ready"}],
                core_rows=[{"domain": "USB/HID control", "status": "warn"}],
                industry_rows=[{"topic": "iMouse XP product boundary", "status": "warn"}],
                verification_rows=[{"phase": "HID click/swipe/text proof", "status": "warn"}],
            )
            brief = xp_roadmap_brief(rows, stage="p1")

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["p0_offline_base"]["status"], "ready")
        self.assertEqual(by_key["p1_route_bench"]["status"], "ready")
        self.assertEqual(by_key["p1_receiver_capture"]["status"], "ready")
        self.assertEqual(by_key["p1_hid_control"]["status"], "warn")
        self.assertEqual(by_key["p1_calibration_input"]["status"], "warn")
        self.assertEqual(by_key["xp_hardware_wired_parity"]["status"], "fail")
        self.assertEqual(by_key["claim_documentation"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_key["p1_hid_control"]["current"])
        self.assertIn("first_focus=P1 HID click/swipe/type proof", brief)

    def test_xp_roadmap_blocks_receiver_and_hid_when_doctor_fails(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/xp_api_compat.md",
                "docs/mainstream_route_decision.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/coordinate_calibration.md",
                "docs/xp_public_source_refresh.md",
                "docs/script_runner.md",
                "docs/validation_evidence.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_roadmap_rows(
                stage="p1",
                docs_root=root,
                route_report=None,
                doctor_report={"overall": "fail", "counts": {"ok": 11, "warn": 7, "fail": 1}},
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                xp_gap_audit={"rows": [{"domain": "Kernel/API", "status": "pass"}]},
            )

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["p0_offline_base"]["status"], "ready")
        self.assertEqual(by_key["p1_route_bench"]["status"], "fail")
        self.assertEqual(by_key["p1_receiver_capture"]["status"], "fail")
        self.assertEqual(by_key["p1_hid_control"]["status"], "fail")
        self.assertIn("doctor=fail", by_key["p1_receiver_capture"]["current"])

    def test_xp_roadmap_keeps_xp_hardware_parity_separate_after_real_ios_pass(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/xp_api_compat.md",
                "docs/mainstream_route_decision.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
                "docs/coordinate_calibration.md",
                "docs/xp_public_source_refresh.md",
                "docs/script_runner.md",
                "docs/validation_evidence.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = xp_roadmap_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                        {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": True}},
                evidence_exists=True,
                evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}},
                xp_gap_audit={"rows": [{"domain": "USB/HID", "status": "pass"}]},
                route_matrix_rows=[
                    {"lane": "XP dedicated hardware", "status": "ready"},
                    {"lane": "Wired projection/vendor SDK", "status": "pass"},
                ],
            )

        by_key = {row["key"]: row for row in rows}
        self.assertEqual(by_key["p1_hid_control"]["status"], "ready")
        self.assertEqual(by_key["xp_hardware_wired_parity"]["status"], "warn")
        self.assertNotEqual(by_key["xp_hardware_wired_parity"]["status"], "pass")
        self.assertIn("XP hardware/wired/4.4/hard-decode proof is separate", by_key["xp_hardware_wired_parity"]["current"])

    def test_write_xp_roadmap_markdown(self):
        rows = xp_roadmap_rows(
            stage="p1",
            docs_root=".",
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            xp_gap_audit={"rows": [{"domain": "Kernel/API", "status": "pass"}]},
        )
        with TemporaryDirectory() as tmp:
            out = write_xp_roadmap_markdown(
                rows,
                Path(tmp) / "roadmap.md",
                run_id="p1_roadmap",
                stage="p1",
                evidence_path="evidence/p1_roadmap.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("XP Roadmap P1", text)
        self.assertIn("P1 HID click/swipe/type proof", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("does not prove XP parity", text)

    def test_gui_goal_gate_rows_map_user_acceptance_goals(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for sources in (
                "docs/p1_single_device_runbook.md",
                "docs/verification_plan.md",
                "docs/validation_evidence.md",
                "docs/ios_group_control_sop.md",
                "docs/industry_sop_playbook.md",
                "docs/field_test_matrix.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/hardware_test_bench_checklist.md",
                "docs/xp_api_compat.md",
                "docs/xp_core_backlog.md",
                "docs/xp_parity_matrix.md",
                "docs/gui_prototype.md",
                "docs/script_runner.md",
                "docs/imouse_xp_iteration_lessons.md",
                "docs/xp_public_source_refresh.md",
                "docs/industry_landscape_2026.md",
                "docs/mainstream_route_decision.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
            ):
                path = root / sources
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = gui_goal_gate_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                        {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}},
                xp_gap_audit={"rows": [{"domain": "Receiver/Capture", "status": "blocked"}]},
                artifact_rows=[
                    {"name": "Field Runbook", "requirement": "recommended", "status": "present"},
                    {"name": "Operator Worksheet", "requirement": "recommended", "status": "present"},
                    {"name": "GUI SOP Board", "requirement": "recommended", "status": "present"},
                    {"name": "Issue Triage", "requirement": "recommended", "status": "present"},
                    {"name": "Rerun Playbook", "requirement": "recommended", "status": "present"},
                    {"name": "Recovery Drill", "requirement": "recommended", "status": "present"},
                    {"name": "Device Evidence Matrix", "requirement": "recommended", "status": "present"},
                    {"name": "Acceptance Gap", "requirement": "recommended", "status": "present"},
                ],
            )

        by_goal = {row["goal"]: row for row in rows}
        brief = gui_goal_gate_brief(rows, stage="p1")

        self.assertEqual(by_goal["1. iOS perfect control"]["status"], "warn")
        self.assertEqual(by_goal["2. iOS group-control SOP and issue log"]["status"], "pass")
        self.assertEqual(by_goal["3. iMouse XP core functions and docs"]["status"], "fail")
        self.assertEqual(by_goal["4. XP iteration lessons and pitfalls"]["status"], "pass")
        self.assertIn("first_blocker=3. iMouse XP core functions and docs", brief)

    def test_gui_goal_gate_uses_claim_scope_before_acceptance_completion(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for sources in (
                "docs/p1_single_device_runbook.md",
                "docs/verification_plan.md",
                "docs/validation_evidence.md",
                "docs/ios_group_control_sop.md",
                "docs/industry_sop_playbook.md",
                "docs/field_test_matrix.md",
                "docs/p2_p3_stability_runbook.md",
                "docs/hardware_test_bench_checklist.md",
                "docs/xp_api_compat.md",
                "docs/xp_core_backlog.md",
                "docs/xp_parity_matrix.md",
                "docs/gui_prototype.md",
                "docs/script_runner.md",
                "docs/imouse_xp_iteration_lessons.md",
                "docs/xp_public_source_refresh.md",
                "docs/industry_landscape_2026.md",
                "docs/mainstream_route_decision.md",
                "docs/receiver_capture_selection.md",
                "docs/hid_hardware_protocol_benchmark.md",
            ):
                path = root / sources
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = gui_goal_gate_rows(
                stage="p1",
                docs_root=root,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                        {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": True}},
                evidence_exists=True,
                evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}},
                xp_gap_audit={"rows": [{"domain": "Receiver/Capture", "status": "pass"}]},
                artifact_rows=[
                    {"name": "Field Runbook", "requirement": "recommended", "status": "present"},
                    {"name": "Operator Worksheet", "requirement": "recommended", "status": "present"},
                    {"name": "GUI SOP Board", "requirement": "recommended", "status": "present"},
                    {"name": "Issue Triage", "requirement": "recommended", "status": "present"},
                    {"name": "Rerun Playbook", "requirement": "recommended", "status": "present"},
                    {"name": "Recovery Drill", "requirement": "recommended", "status": "present"},
                    {"name": "Device Evidence Matrix", "requirement": "recommended", "status": "present"},
                    {"name": "Acceptance Gap", "requirement": "recommended", "status": "present"},
                ],
                proof_map_rows=[{"key": "claim_boundary", "status": "pass"}],
                claim_scope_rows_data=[{"claim_area": "P1 single-iPhone control", "status": "warn"}],
            )

        by_goal = {row["goal"]: row for row in rows}

        self.assertEqual(by_goal["1. iOS perfect control"]["status"], "warn")
        self.assertEqual(by_goal["1. iOS perfect control"]["gui_action"], "Open Claim Scope")
        self.assertEqual(by_goal["2. iOS group-control SOP and issue log"]["status"], "warn")
        self.assertIn("Claim scope P1", by_goal["1. iOS perfect control"]["current_evidence"])
        self.assertIn("Proof Map and Claim Scope", by_goal["1. iOS perfect control"]["next_action"])

    def test_write_gui_goal_gate_markdown(self):
        rows = gui_goal_gate_rows(
            stage="p1",
            docs_root=".",
            acceptance_report=None,
            readiness_report=None,
            evidence_exists=False,
            xp_gap_audit=None,
        )
        with TemporaryDirectory() as tmp:
            out = write_gui_goal_gate_markdown(
                rows,
                Path(tmp) / "goals.md",
                run_id="p1_goals",
                stage="p1",
                evidence_path="evidence/p1_goals.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Goal Gate P1", text)
        self.assertIn("1. iOS perfect control", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("Proof Map closure, Claim Scope pass wording", text)

    def test_field_kit_gate_rows_stop_on_placeholders_and_missing_scope(self):
        route = decision_template(run_id="kit_missing", devices=["dev_1"])
        rows = field_kit_gate_rows(
            stage="p1",
            docs_root=".",
            device_ids=[],
            route_decision=route,
            route_report=None,
            doctor_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        by_gate = {row["gate"]: row for row in rows}
        brief = field_kit_gate_brief(rows, stage="p1")

        self.assertEqual(by_gate["Run identity and device scope"]["status"], "fail")
        self.assertEqual(by_gate["Receiver procurement and capture route"]["status"], "fail")
        self.assertEqual(by_gate["HID procurement, firmware, and serial binding"]["status"], "fail")
        self.assertEqual(by_gate["Open P1 stop line"]["status"], "fail")
        self.assertIn("first_stop=", brief)
        self.assertIn("Run identity and device scope", brief)

    def test_field_kit_gate_rows_allow_generic_p1_but_warn_xp_parity(self):
        route = decision_template(run_id="kit_ready", devices=["dev_1"])
        apply_route_decision_form_values(route, {
            "receiver.route": "uxplay",
            "receiver.name": "imouse-dev-01",
            "receiver.version": "1.0",
            "receiver.path": "C:/tools/uxplay.exe",
            "receiver.start_command": "uxplay -n imouse-dev-01",
            "receiver.airplay_name": "imouse-dev-01",
            "receiver.capture_method": "window",
            "receiver.window_binding.title": "iMouse dev 01",
            "receiver.window_binding.process": "uxplay.exe",
            "receiver.window_binding.handle": "",
            "receiver.license_status": "open-source local build",
            "hid.route": "ch9329",
            "hid.provider": "ch9329",
            "hid.id": "hid01",
            "hid.firmware": "ch9329-v1",
            "hid.serial_port": "COM3",
            "hid.baudrate": "9600",
            "iphone.id": "ip01",
            "iphone.model": "iPhone 13",
            "iphone.ios_version": "17.7",
            "iphone.orientation": "portrait",
            "iphone.assistive_touch": "on",
            "iphone.pointer_speed": "default",
            "bench.device_id": "dev_1",
            "bench.device_ids": "dev_1",
            "bench.hub_id": "hub-a",
            "bench.hub_port": "hub-a-01",
            "bench.cable_id": "cable-01",
            "bench.network": "pc wired, same vlan",
            "bench.operator": "tester",
            "decision.allowed_to_run_p1": "true",
            "decision.reason": "kit ready",
            "decision.open_blockers": "",
        })
        rows = field_kit_gate_rows(
            stage="p1",
            docs_root=".",
            device_ids=["dev_1"],
            route_decision=route,
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            evidence_summary={"total": 0, "by_status": {}},
            hardware_scan_rows=[{"port": "COM3", "description": "CH9329 hid01"}],
        )
        by_gate = {row["gate"]: row for row in rows}
        brief = field_kit_gate_brief(rows, stage="p1")

        self.assertEqual(by_gate["Run identity and device scope"]["status"], "pass")
        self.assertEqual(by_gate["Receiver procurement and capture route"]["status"], "pass")
        self.assertEqual(by_gate["HID procurement, firmware, and serial binding"]["status"], "pass")
        self.assertEqual(by_gate["Evidence plan and artifact ledger"]["status"], "pass")
        self.assertEqual(by_gate["Open P1 stop line"]["status"], "pass")
        self.assertEqual(by_gate["XP hardware comparison question"]["status"], "warn")
        self.assertIn("first_stop=none", brief)

    def test_write_field_kit_gate_markdown(self):
        rows = field_kit_gate_rows(
            stage="p1",
            docs_root=".",
            device_ids=[],
            route_decision=decision_template(run_id="kit_doc", devices=["dev_1"]),
            route_report=None,
            doctor_report=None,
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_field_kit_gate_markdown(
                rows,
                Path(tmp) / "kit_gate.md",
                run_id="p1_kit",
                stage="p1",
                evidence_path="evidence/p1_kit.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Field Kit Gate P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("pre-run procurement/material/readiness gate", text)
        self.assertIn("does not write evidence", text)

    def test_ios_field_sop_rows_surface_missing_phone_settings(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/ios_field_settings_sop.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = ios_field_sop_rows(
                stage="p1",
                docs_root=root,
                device_ids=[],
                route_decision=None,
                route_report=None,
                doctor_report=None,
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
            )
            brief = ios_field_sop_brief(rows, stage="p1")

        by_check = {row["check"]: row for row in rows}
        self.assertEqual(by_check["Device identity and iOS version"]["status"], "fail")
        self.assertEqual(by_check["AssistiveTouch and pointer profile"]["status"], "pending")
        self.assertEqual(by_check["Rotation lock and AssistiveTouch menu"]["status"], "pending")
        self.assertEqual(by_check["Full Keyboard Access and mouse settings"]["status"], "pending")
        self.assertEqual(by_check["Mouse parameter profile and calibration library"]["status"], "pending")
        self.assertEqual(by_check["Settings claim boundary"]["status"], "fail")
        self.assertIn("first_stop=Device identity and iOS version", brief)

    def test_ios_field_sop_rows_keep_settings_ready_separate_from_real_control(self):
        route = decision_template(run_id="ios_sop_ready", devices=["dev_1"])
        apply_route_decision_form_values(route, {
            "receiver.route": "uxplay",
            "receiver.name": "imouse-dev-01",
            "receiver.version": "1.0",
            "receiver.path": "C:/tools/uxplay.exe",
            "receiver.start_command": "uxplay -n imouse-dev-01",
            "receiver.airplay_name": "imouse-dev-01",
            "receiver.capture_method": "window",
            "receiver.window_binding.title": "iMouse dev 01",
            "hid.route": "ch9329",
            "hid.provider": "ch9329",
            "hid.id": "hid01",
            "hid.firmware": "ch9329-v1",
            "hid.serial_port": "COM3",
            "iphone.id": "ip01",
            "iphone.model": "iPhone 13",
            "iphone.ios_version": "17.7",
            "iphone.orientation": "portrait",
            "iphone.assistive_touch": "on",
            "iphone.rotation_lock": "on",
            "iphone.assistive_touch_menu": "hidden",
            "iphone.full_keyboard_access": "on",
            "iphone.trackpad_mouse": "on",
            "iphone.pointer_speed": "default",
            "iphone.mouse_parameter_profile": "iphone13-ios17-portrait-default",
            "iphone.qr_scan_policy": "disconnect_airplay_before_scan",
            "iphone.auto_lock": "never",
            "iphone.brightness": "80%",
            "iphone.focus_mode": "off",
            "bench.device_id": "dev_1",
            "bench.device_ids": "dev_1",
            "bench.hub_id": "hub-a",
            "bench.hub_port": "hub-a-01",
            "bench.cable_id": "cable-01",
            "bench.network": "same vlan",
            "bench.operator": "tester",
            "decision.allowed_to_run_p1": "true",
            "decision.open_blockers": "",
        })
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in (
                "docs/ios_field_settings_sop.md",
                "docs/verification_plan.md",
            ):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("ok", encoding="utf-8")
            rows = ios_field_sop_rows(
                stage="p1",
                docs_root=root,
                device_ids=["dev_1"],
                route_decision=route,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
                acceptance_report={
                    "gate": "p1",
                    "ok": True,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                        {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                    ],
                },
                readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}},
            )

        by_check = {row["check"]: row for row in rows}
        self.assertEqual(by_check["Device identity and iOS version"]["status"], "ready")
        self.assertEqual(by_check["AssistiveTouch and pointer profile"]["status"], "ready")
        self.assertEqual(by_check["Rotation lock and AssistiveTouch menu"]["status"], "ready")
        self.assertEqual(by_check["Full Keyboard Access and mouse settings"]["status"], "ready")
        self.assertEqual(by_check["Mouse parameter profile and calibration library"]["status"], "ready")
        self.assertEqual(by_check["Screen lock, brightness, and interruptions"]["status"], "ready")
        self.assertEqual(by_check["Baseline screenshot and manual observation"]["status"], "warn")
        self.assertEqual(by_check["Settings claim boundary"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_check["Baseline screenshot and manual observation"]["current"])

    def test_write_ios_field_sop_markdown(self):
        rows = ios_field_sop_rows(
            stage="p1",
            docs_root=".",
            device_ids=[],
            route_decision=None,
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_ios_field_sop_markdown(
                rows,
                Path(tmp) / "ios_sop.md",
                run_id="p1_ios_sop",
                stage="p1",
                evidence_path="evidence/p1_ios_sop.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("iOS Field Settings SOP P1", text)
        self.assertIn("AssistiveTouch and pointer profile", text)
        self.assertIn("Mouse parameter profile and calibration library", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)

    def test_hardware_bench_rows_surface_route_and_real_device_gates(self):
        route = decision_template(run_id="bench_ready", devices=["dev_1"])
        apply_route_decision_form_values(route, {
            "receiver.route": "uxplay",
            "receiver.name": "imouse-dev-01",
            "receiver.version": "1.0",
            "receiver.path": "C:/tools/uxplay.exe",
            "receiver.start_command": "uxplay -n imouse-dev-01",
            "receiver.airplay_name": "imouse-dev-01",
            "receiver.capture_method": "window",
            "hid.route": "ch9329",
            "hid.provider": "ch9329",
            "hid.id": "hid01",
            "hid.firmware": "ch9329-v1",
            "hid.serial_port": "COM3",
            "iphone.id": "ip01",
            "iphone.model": "iPhone 13",
            "iphone.ios_version": "17.7",
            "iphone.orientation": "portrait",
            "iphone.assistive_touch": "on",
            "iphone.pointer_speed": "default",
            "bench.device_id": "dev_1",
            "bench.device_ids": "dev_1",
            "bench.hub_id": "hub-a",
            "bench.hub_port": "hub-a-01",
            "bench.cable_id": "cable-01",
            "bench.network": "pc wired, same vlan",
            "bench.operator": "tester",
            "decision.allowed_to_run_p1": "true",
            "decision.reason": "bench ready",
            "decision.open_blockers": "",
        })
        rows = hardware_bench_rows(
            stage="p1",
            device_ids=["dev_1"],
            route_decision=route,
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            acceptance_report={
                "gate": "p1",
                "ok": True,
                "checks": [
                    {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                    {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                ],
            },
            readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}},
            callback_rows_data=[{"event": "hid_ack", "severity": "info"}],
        )
        by_check = {row["check"]: row for row in rows}
        brief = hardware_bench_brief(rows, stage="p1")

        self.assertEqual(by_check["Bench ledger and labels"]["status"], "pass")
        self.assertEqual(by_check["Receiver/capture route"]["status"], "pass")
        self.assertEqual(by_check["HID binding and iPhone response"]["status"], "pass")
        self.assertEqual(by_check["Screenshot and control evidence"]["status"], "pass")
        self.assertEqual(by_check["XP hardware comparison"]["status"], "pending")
        self.assertIn("first_blocker=XP hardware comparison", brief)

    def test_write_hardware_bench_markdown(self):
        rows = hardware_bench_rows(
            stage="p1",
            device_ids=[],
            route_decision=decision_template(run_id="bench_missing", devices=["dev_1"]),
            route_report={"ok": False, "ready": False, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "fail", "counts": {"ok": 1, "warn": 0, "fail": 1}},
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_hardware_bench_markdown(
                rows,
                Path(tmp) / "bench.md",
                run_id="p1_bench",
                stage="p1",
                evidence_path="evidence/p1_bench.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        by_check = {row["check"]: row for row in rows}
        self.assertEqual(by_check["Bench ledger and labels"]["status"], "fail")
        self.assertIn("GUI Hardware Bench P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)

    def test_capture_quality_bench_rows_detect_failures_and_size_drift(self):
        rows = capture_quality_bench_rows(
            [
                {
                    "sample": 1,
                    "device_id": "dev_1",
                    "elapsed_ms": 31.2,
                    "artifact": "evidence/p1_artifacts/001.png",
                    "screenshot_quality": {
                        "ok": True,
                        "reason": "ok",
                        "width": 1170,
                        "height": 2532,
                        "mean_luma": 121.4,
                        "stddev_luma": 32.1,
                        "bytes": 12345,
                    },
                },
                {
                    "sample": 2,
                    "device_id": "dev_1",
                    "elapsed_ms": 33.0,
                    "artifact": "evidence/p1_artifacts/002.png",
                    "screenshot_quality": {
                        "ok": True,
                        "reason": "ok",
                        "width": 1170,
                        "height": 2530,
                        "mean_luma": 120.0,
                        "stddev_luma": 31.8,
                        "bytes": 12000,
                    },
                },
                {
                    "sample": 3,
                    "device_id": "dev_1",
                    "elapsed_ms": 30.0,
                    "screenshot_quality": {
                        "ok": False,
                        "reason": "black_screen",
                        "width": 1170,
                        "height": 2532,
                        "mean_luma": 0.0,
                        "stddev_luma": 0.0,
                        "bytes": 9000,
                    },
                },
            ],
            device_id="dev_1",
        )
        brief = capture_quality_bench_brief(rows, stage="p1", sample_goal=3)

        self.assertEqual(rows[0]["status"], "pass")
        self.assertEqual(rows[0]["size"], "1170x2532")
        self.assertEqual(rows[2]["status"], "fail")
        self.assertEqual(rows[2]["reason"], "black_screen")
        self.assertEqual(capture_quality_bench_status(rows, sample_goal=3), "fail")
        self.assertIn("size_variants=2", brief)
        self.assertIn("first_failure=3: black_screen", brief)

    def test_capture_quality_bench_status_warns_on_size_drift(self):
        rows = capture_quality_bench_rows([
            {
                "sample": 1,
                "device_id": "dev_1",
                "screenshot_quality": {"ok": True, "reason": "ok", "width": 1170, "height": 2532},
            },
            {
                "sample": 2,
                "device_id": "dev_1",
                "screenshot_quality": {"ok": True, "reason": "ok", "width": 1170, "height": 2530},
            },
        ])

        self.assertEqual(capture_quality_bench_status(rows, sample_goal=2), "warn")

    def test_write_capture_quality_bench_markdown(self):
        rows = capture_quality_bench_rows([
            {
                "sample": 1,
                "device_id": "dev_1",
                "artifact": "evidence/p1_artifacts/001.png",
                "screenshot_quality": {"ok": True, "reason": "ok", "width": 1170, "height": 2532},
            }
        ])
        with TemporaryDirectory() as tmp:
            out = write_capture_quality_bench_markdown(
                rows,
                Path(tmp) / "capture_bench.md",
                run_id="p1_capture",
                stage="p1",
                device_id="dev_1",
                sample_goal=1,
                evidence_path="evidence/p1_capture.jsonl",
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Capture Quality Bench P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not prove click, swipe, text input", text)
        self.assertIn("100-screenshot stability run", text)

    def test_control_response_bench_rows_keep_api_success_in_ready(self):
        rows = control_response_bench_rows(
            [
                {
                    "status": "pass",
                    "step": "api hid click",
                    "device_ids": ["dev_1"],
                    "details": {"action": "click", "x": 120, "y": 300},
                }
            ],
            device_ids=["dev_1"],
        )
        by_label = {row["label"]: row for row in rows}
        brief = control_response_bench_brief(rows, stage="p1")

        self.assertEqual(by_label["HID click"]["status"], "ready")
        self.assertIn("commands=1", by_label["HID click"]["current"])
        self.assertIn("manual_pass=0", by_label["HID click"]["current"])
        self.assertEqual(by_label["HID swipe"]["status"], "pending")
        self.assertIn("ready=1", brief)

    def test_control_response_bench_rows_pass_with_manual_observations(self):
        rows = control_response_bench_rows([
            {
                "status": "pass",
                "step": "P1 trial - HID click",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "tap opened target page"},
            },
            {
                "status": "pass",
                "step": "P1 trial - HID swipe",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "list moved and released"},
            },
            {
                "status": "pass",
                "step": "P1 trial - Keyboard input",
                "device_ids": ["dev_1"],
                "details": {"observation": {"manual": True, "note": "abc visible in field"}},
            },
        ])
        by_label = {row["label"]: row for row in rows}
        brief = control_response_bench_brief(rows, stage="p1")

        self.assertEqual(by_label["HID click"]["status"], "pass")
        self.assertEqual(by_label["HID swipe"]["status"], "pass")
        self.assertEqual(by_label["Keyboard input"]["status"], "pass")
        self.assertIn("pass=3", brief)
        self.assertIn("abc visible", by_label["Keyboard input"]["note"])

    def test_control_response_bench_rows_preserve_fail_context(self):
        rows = control_response_bench_rows([
            {
                "status": "fail",
                "step": "P1 trial - HID swipe",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "category": "calibration", "note": "swipe went upward"},
                "artifacts": ["evidence/p1_artifacts/swipe_fail.png"],
            },
            {
                "status": "fail",
                "step": "api keyboard type",
                "device_ids": ["dev_1"],
                "details": {"error": "keyboard not connected"},
            },
        ])
        by_label = {row["label"]: row for row in rows}

        self.assertEqual(by_label["HID swipe"]["status"], "fail")
        self.assertEqual(by_label["HID swipe"]["categories"], "calibration")
        self.assertIn("swipe_fail.png", by_label["HID swipe"]["artifacts"])
        self.assertIn("manual_fail=1", by_label["HID swipe"]["current"])
        self.assertEqual(by_label["Keyboard input"]["status"], "fail")
        self.assertEqual(by_label["Keyboard input"]["categories"], "hid")
        self.assertIn("command_fail=1", by_label["Keyboard input"]["current"])

    def test_write_control_response_bench_markdown(self):
        rows = control_response_bench_rows([
            {
                "status": "pass",
                "step": "P1 trial - HID click",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "button opened"},
            }
        ])
        with TemporaryDirectory() as tmp:
            out = write_control_response_bench_markdown(
                rows,
                Path(tmp) / "control_bench.md",
                run_id="p1_control",
                stage="p1",
                evidence_path="evidence/p1_control.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Control Response Bench P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("API/HID command success is not enough", text)
        self.assertIn("Manual pass recorded after the operator sees the real iPhone respond", text)

    def test_control_evidence_ledger_quarantines_generic_manual_observation(self):
        events = [
            {
                "status": "pass",
                "step": "Manual observation",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "operator says the control smoke looked ok"},
            }
        ]
        rows = control_evidence_ledger_rows(
            events,
            run_id="p1_generic",
            stage="p1",
            device_ids=["dev_1"],
            evidence_exists=True,
            evidence_summary={"total": 1, "by_status": {"pass": 1}},
        )
        by_lane = {row["lane"]: row for row in rows}
        brief = control_evidence_ledger_brief(rows, stage="p1")

        self.assertEqual(by_lane["HID click"]["status"], "pending")
        self.assertEqual(by_lane["HID swipe"]["status"], "pending")
        self.assertEqual(by_lane["Keyboard input"]["status"], "pending")
        self.assertEqual(by_lane["Generic Manual quarantine"]["status"], "fail")
        self.assertIn("generic=1", by_lane["Generic Manual quarantine"]["current"])
        self.assertIn("lane_pass=0/3", by_lane["Claim boundary"]["current"])
        self.assertIn("fail=", brief)

    def test_control_evidence_ledger_requires_separate_lane_passes(self):
        events = [
            {
                "status": "pass",
                "step": "Control ledger - HID click",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "button opened on physical iPhone"},
            },
            {
                "status": "pass",
                "step": "Control ledger - HID swipe",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "list moved down and released"},
            },
            {
                "status": "pass",
                "step": "Control ledger - Keyboard input",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "imouse-smoke visible in focused field"},
            },
        ]
        readiness = {"ok": True, "claims": {"real_ios_control_verified": True}}
        acceptance = {"gate": "p1", "ok": True, "checks": []}
        rows = control_evidence_ledger_rows(
            events,
            run_id="p1_lanes",
            stage="p1",
            device_ids=["dev_1"],
            evidence_exists=True,
            evidence_summary={"total": 3, "by_status": {"pass": 3}},
            acceptance_report=acceptance,
            readiness_report=readiness,
        )
        by_lane = {row["lane"]: row for row in rows}

        self.assertEqual(by_lane["HID click"]["status"], "pass")
        self.assertEqual(by_lane["HID swipe"]["status"], "pass")
        self.assertEqual(by_lane["Keyboard input"]["status"], "pass")
        self.assertEqual(by_lane["Generic Manual quarantine"]["status"], "pass")
        self.assertEqual(by_lane["Claim boundary"]["status"], "pass")

    def test_control_evidence_ledger_broad_manual_text_does_not_close_all_lanes(self):
        rows = control_evidence_ledger_rows(
            [
                {
                    "status": "pass",
                    "step": "Manual observation",
                    "device_ids": ["dev_1"],
                    "details": {"manual": True, "note": "click swipe type all looked ok"},
                }
            ],
            run_id="p1_broad",
            stage="p1",
            device_ids=["dev_1"],
            evidence_exists=True,
            evidence_summary={"total": 1, "by_status": {"pass": 1}},
        )
        by_lane = {row["lane"]: row for row in rows}

        self.assertEqual(by_lane["HID click"]["status"], "pending")
        self.assertEqual(by_lane["HID swipe"]["status"], "pending")
        self.assertEqual(by_lane["Keyboard input"]["status"], "pending")
        self.assertEqual(by_lane["Generic Manual quarantine"]["status"], "fail")

    def test_write_control_evidence_ledger_markdown(self):
        rows = control_evidence_ledger_rows(
            [],
            run_id="p1_ledger",
            stage="p1",
            device_ids=["dev_1"],
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_control_evidence_ledger_markdown(
                rows,
                Path(tmp) / "control_ledger.md",
                run_id="p1_ledger",
                stage="p1",
                evidence_path="evidence/p1_ledger.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Control Evidence Ledger P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("Lane Separation Rule", text)
        self.assertIn("A generic Manual pass is not enough", text)

    def test_field_evidence_wizard_rows_keep_claim_boundary_visible(self):
        route = decision_template(run_id="wizard_ready", devices=["dev_1"])
        apply_route_decision_form_values(route, {
            "receiver.route": "uxplay",
            "receiver.name": "imouse-dev-01",
            "receiver.version": "1.0",
            "receiver.path": "C:/tools/uxplay.exe",
            "receiver.start_command": "uxplay -n imouse-dev-01",
            "receiver.airplay_name": "imouse-dev-01",
            "receiver.capture_method": "window",
            "hid.route": "ch9329",
            "hid.provider": "ch9329",
            "hid.id": "hid01",
            "hid.firmware": "ch9329-v1",
            "hid.serial_port": "COM3",
            "iphone.id": "ip01",
            "iphone.model": "iPhone 13",
            "iphone.ios_version": "17.7",
            "iphone.orientation": "portrait",
            "iphone.assistive_touch": "on",
            "iphone.pointer_speed": "default",
            "bench.device_id": "dev_1",
            "bench.device_ids": "dev_1",
            "bench.hub_id": "hub-a",
            "bench.hub_port": "hub-a-01",
            "bench.cable_id": "cable-01",
            "bench.network": "pc wired, same vlan",
            "bench.operator": "tester",
            "decision.allowed_to_run_p1": "true",
            "decision.reason": "bench ready",
            "decision.open_blockers": "",
        })
        rows = field_evidence_wizard_rows(
            run_id="wizard_ready",
            stage="p1",
            device_ids=["dev_1"],
            route_decision=route,
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            scenario_summary={"ok": True, "steps": [{"status": "pass"}]},
            acceptance_report={
                "gate": "p1",
                "ok": True,
                "checks": [
                    {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                    {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                ],
            },
            readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}},
            callback_rows_data=[{"event": "hid_ack", "severity": "info"}],
            template_asset_rows_data=[{"path": "templates/button.png", "status": "ok"}],
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "present"},
                {"name": "Doctor Report", "requirement": "required", "status": "present"},
                {"name": "Acceptance Report", "requirement": "required", "status": "present"},
                {"name": "Readiness Report", "requirement": "required", "status": "present"},
            ],
        )
        by_lane = {row["lane"]: row for row in rows}
        brief = field_evidence_wizard_brief(rows, stage="p1")

        self.assertEqual(by_lane["Physical ledger"]["status"], "pass")
        self.assertEqual(by_lane["Receiver screenshot"]["status"], "pass")
        self.assertEqual(by_lane["HID click, swipe, and text"]["status"], "pass")
        self.assertEqual(by_lane["Readiness and handoff"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_lane["Readiness and handoff"]["current"])
        self.assertIn("first_focus=Readiness and handoff", brief)

    def test_write_field_evidence_wizard_markdown(self):
        rows = field_evidence_wizard_rows(
            run_id="wizard_missing",
            stage="p1",
            device_ids=[],
            route_decision=None,
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_field_evidence_wizard_markdown(
                rows,
                Path(tmp) / "wizard.md",
                run_id="wizard_missing",
                stage="p1",
                evidence_path="evidence/wizard_missing.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        by_lane = {row["lane"]: row for row in rows}
        self.assertEqual(by_lane["Run identity and device scope"]["status"], "fail")
        self.assertIn("Field Evidence Wizard P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)

    def test_field_evidence_runner_requires_each_control_lane(self):
        rows = field_evidence_runner_rows(
            run_id="p1_runner",
            stage="p1",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            acceptance_report={
                "gate": "p1",
                "ok": True,
                "checks": [
                    {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                    {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                ],
            },
            readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": True}},
            evidence_exists=True,
            evidence_summary={"total": 4, "by_status": {"pass": 4, "fail": 0}},
            events=[
                {
                    "status": "pass",
                    "step": "P1 trial - HID click",
                    "device_ids": ["dev_1"],
                    "details": {"manual": True, "note": "button opened"},
                }
            ],
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "present"},
                {"name": "Doctor Report", "requirement": "required", "status": "present"},
                {"name": "Acceptance Report", "requirement": "required", "status": "present"},
                {"name": "Readiness Report", "requirement": "required", "status": "present"},
            ],
            evidence_path="evidence/p1_runner.jsonl",
            route_decision_path="evidence/p1_runner_route_decision.json",
        )
        by_gate = {row["gate"]: row for row in rows}
        brief = field_evidence_runner_brief(rows, stage="p1")

        self.assertEqual(by_gate["HID click"]["status"], "pass")
        self.assertEqual(by_gate["HID swipe"]["status"], "pending")
        self.assertEqual(by_gate["Keyboard input"]["status"], "pending")
        self.assertEqual(by_gate["Claim boundary"]["status"], "fail")
        self.assertIn("first_focus=Screenshot quality", brief)

    def test_field_evidence_runner_keeps_readiness_claim_boundary(self):
        events = [
            {
                "status": "pass",
                "step": "P1 trial - HID click",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "tap visible"},
            },
            {
                "status": "pass",
                "step": "P1 trial - HID swipe",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "release visible"},
            },
            {
                "status": "pass",
                "step": "P1 trial - Keyboard input",
                "device_ids": ["dev_1"],
                "details": {"manual": True, "note": "text visible"},
            },
        ]
        rows = field_evidence_runner_rows(
            run_id="p1_runner_ready",
            stage="p1",
            device_ids=["dev_1"],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "warn", "counts": {"ok": 12, "warn": 1, "fail": 0}},
            acceptance_report={
                "gate": "p1",
                "ok": True,
                "checks": [
                    {"name": "manual_observation", "status": "pass", "message": "3 manual pass"},
                    {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                ],
            },
            readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}},
            events=events,
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "present"},
                {"name": "Doctor Report", "requirement": "required", "status": "present"},
                {"name": "Capture Quality Bench", "requirement": "recommended", "status": "present", "path": "capture.md"},
                {"name": "Acceptance Report", "requirement": "required", "status": "present"},
                {"name": "Readiness Report", "requirement": "required", "status": "present"},
            ],
            evidence_path="evidence/p1_runner_ready.jsonl",
            route_decision_path="evidence/p1_runner_ready_route_decision.json",
        )
        by_gate = {row["gate"]: row for row in rows}

        self.assertEqual(by_gate["Route-aware doctor"]["status"], "warn")
        self.assertEqual(by_gate["HID click"]["status"], "pass")
        self.assertEqual(by_gate["HID swipe"]["status"], "pass")
        self.assertEqual(by_gate["Keyboard input"]["status"], "pass")
        self.assertEqual(by_gate["Readiness report"]["status"], "warn")
        self.assertEqual(by_gate["Claim boundary"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_gate["Readiness report"]["current"])

    def test_write_field_evidence_runner_markdown_commands(self):
        rows = field_evidence_runner_rows(
            run_id="p1_runner_md",
            stage="p1",
            device_ids=[],
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            evidence_path="evidence/p1_runner_md.jsonl",
            route_decision_path="evidence/p1_runner_md_route_decision.json",
        )
        with TemporaryDirectory() as tmp:
            out = write_field_evidence_runner_markdown(
                rows,
                Path(tmp) / "runner.md",
                run_id="p1_runner_md",
                stage="p1",
                evidence_path="evidence/p1_runner_md.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("Field Evidence Runner P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("python -m imouse.route_decision validate evidence/p1_runner_md_route_decision.json --require-ready --markdown evidence\\p1_runner_md_p1_route_decision.md --record-evidence evidence/p1_runner_md.jsonl", text)
        self.assertIn("python -m imouse.doctor --route-decision evidence/p1_runner_md_route_decision.json --markdown evidence\\p1_runner_md_p1_doctor.md", text)
        self.assertIn("python -m imouse.acceptance evidence/p1_runner_md.jsonl --gate p1 --markdown evidence\\p1_runner_md_p1_acceptance.md", text)
        self.assertIn("python -m imouse.acceptance evidence/p1_runner_md.jsonl --gate p1 --gap-markdown evidence\\p1_runner_md_p1_gap.md", text)
        self.assertIn("python -m imouse.readiness --target p1 --evidence evidence/p1_runner_md.jsonl --markdown evidence\\p1_runner_md_readiness.md", text)
        self.assertNotIn("--evidence-jsonl", text)

    def test_first_run_packet_rows_surface_start_blockers(self):
        rows = first_run_packet_rows(
            run_id="p1_start",
            stage="p1",
            device_ids=[],
            source_rows=[],
            compatibility_rows=[],
            goal_rows=[],
            kit_gate_rows=[{"gate": "Open P1 stop line", "status": "fail"}],
            bench_rows=[{"check": "Receiver/capture route", "status": "fail"}],
            wizard_rows=[{"lane": "Run identity and device scope", "status": "fail"}],
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "missing"},
                {"name": "Doctor Report", "requirement": "required", "status": "missing"},
            ],
            route_report=None,
            doctor_report=None,
            acceptance_report=None,
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        by_section = {row["section"]: row for row in rows}
        brief = first_run_packet_brief(rows, stage="p1")

        self.assertEqual(by_section["Run identity and device scope"]["status"], "fail")
        self.assertEqual(by_section["Step-by-step verification method"]["status"], "pending")
        self.assertEqual(by_section["Local command verification"]["status"], "pending")
        self.assertEqual(by_section["XP roadmap and R&D closure"]["status"], "pending")
        self.assertEqual(by_section["XP core function coverage"]["status"], "pending")
        self.assertEqual(by_section["XP API/SDK coverage boundary"]["status"], "pending")
        self.assertEqual(by_section["Scenario/script coverage guard"]["status"], "pending")
        self.assertEqual(by_section["Claim scope and handoff wording"]["status"], "pending")
        self.assertIn("Open Claim Scope", by_section["Claim scope and handoff wording"]["gui_action"])
        self.assertEqual(by_section["XP event/error contract"]["status"], "pending")
        self.assertEqual(by_section["Mainstream route matrix"]["status"], "pending")
        self.assertEqual(by_section["Receiver lane scorecard"]["status"], "pending")
        self.assertEqual(by_section["Receiver route bootstrap draft"]["status"], "pending")
        self.assertEqual(by_section["Receiver setup and binding split"]["status"], "pending")
        self.assertEqual(by_section["Device/iOS coverage"]["status"], "pending")
        self.assertEqual(by_section["Field kit gate"]["status"], "fail")
        self.assertEqual(by_section["iPhone settings SOP"]["status"], "pending")
        self.assertEqual(by_section["Route, doctor, and hardware bench"]["status"], "fail")
        self.assertEqual(by_section["Real iPhone control proof"]["status"], "fail")
        self.assertEqual(by_section["Evidence pack exports"]["status"], "fail")
        self.assertIn("first_focus=Run identity and device scope", brief)

    def test_first_run_packet_keeps_real_ios_boundary_when_gates_look_clean(self):
        rows = first_run_packet_rows(
            run_id="p1_start",
            stage="p1",
            device_ids=["dev_1"],
            source_rows=[{"status": "warn"}],
            industry_rows=[{"topic": "iMouse XP product boundary", "status": "warn"}],
            roadmap_rows=[{"lane": "P1 HID click/swipe/type proof", "status": "warn"}],
            verification_rows=[{"phase": "HID click/swipe/text proof", "status": "warn"}],
            local_rows=[{"check": "Dependency check", "status": "warn"}],
            core_rows=[{"domain": "USB/HID control", "status": "warn"}],
            api_coverage_rows=[{"domain": "USB/HID binding", "status": "warn"}],
            script_coverage_rows=[{"domain": "HID click, swipe and text lanes", "status": "warn"}],
            proof_map_rows=[{"key": "claim_boundary", "status": "warn"}],
            claim_scope_rows_data=[{"claim_area": "P1 single-iPhone control", "status": "warn"}],
            event_contract_rows=[{"contract": "Callback/event lifecycle", "status": "warn"}],
            route_matrix_rows=[{"lane": "XP-style black-box route", "status": "ready", "selected": "yes"}],
            compatibility_rows=[{"coverage_key": "iPhone 13 / 17.7", "status": "pass"}],
            goal_rows=[{"status": "warn"}],
            kit_gate_rows=[
                {"gate": "Open P1 stop line", "status": "pass"},
                {"gate": "XP hardware comparison question", "status": "warn"},
            ],
            ios_sop_rows=[{"check": "Settings claim boundary", "status": "warn"}],
            bench_rows=[{"check": "Screenshot and control evidence", "status": "pass"}],
            wizard_rows=[{"lane": "Readiness and handoff", "status": "warn"}],
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "present"},
                {"name": "Doctor Report", "requirement": "required", "status": "present"},
                {"name": "Receiver Candidate Scorecard", "requirement": "recommended", "status": "present", "path": "rx_score.md"},
                {"name": "Receiver Route Bootstrap", "requirement": "recommended", "status": "present", "path": "rx_bootstrap.md"},
                {"name": "Receiver Setup Wizard", "requirement": "recommended", "status": "present", "path": "rx_setup.md"},
                {"name": "First Run Packet", "requirement": "recommended", "status": "missing"},
            ],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            scenario_summary={"ok": True, "total": 2, "success_count": 2, "failure_count": 0},
            acceptance_report={
                "gate": "p1",
                "ok": True,
                "checks": [
                    {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                    {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                ],
            },
            readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 6, "by_status": {"pass": 6, "fail": 0}},
        )
        by_section = {row["section"]: row for row in rows}

        self.assertEqual(by_section["Run identity and device scope"]["status"], "pass")
        self.assertEqual(by_section["XP public sources, industry radar, and goal boundary"]["status"], "ready")
        self.assertEqual(by_section["XP roadmap and R&D closure"]["status"], "warn")
        self.assertEqual(by_section["Step-by-step verification method"]["status"], "warn")
        self.assertEqual(by_section["Local command verification"]["status"], "warn")
        self.assertEqual(by_section["XP core function coverage"]["status"], "warn")
        self.assertEqual(by_section["XP API/SDK coverage boundary"]["status"], "warn")
        self.assertIn("XP API coverage P1", by_section["XP API/SDK coverage boundary"]["current"])
        self.assertEqual(by_section["Scenario/script coverage guard"]["status"], "warn")
        self.assertIn("Script coverage P1", by_section["Scenario/script coverage guard"]["current"])
        self.assertEqual(by_section["Acceptance proof map"]["status"], "warn")
        self.assertIn("Proof map P1", by_section["Acceptance proof map"]["current"])
        self.assertEqual(by_section["Claim scope and handoff wording"]["status"], "warn")
        self.assertIn("Claim scope P1", by_section["Claim scope and handoff wording"]["current"])
        self.assertEqual(by_section["XP event/error contract"]["status"], "warn")
        self.assertEqual(by_section["Mainstream route matrix"]["status"], "ready")
        self.assertEqual(by_section["Receiver lane scorecard"]["status"], "ready")
        self.assertEqual(by_section["Receiver route bootstrap draft"]["status"], "ready")
        self.assertEqual(by_section["Receiver setup and binding split"]["status"], "ready")
        self.assertEqual(by_section["Field kit gate"]["status"], "warn")
        self.assertEqual(by_section["iPhone settings SOP"]["status"], "warn")
        self.assertEqual(by_section["Real iPhone control proof"]["status"], "warn")
        self.assertEqual(by_section["Acceptance, readiness, and handoff"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_section["Acceptance, readiness, and handoff"]["current"])

    def test_write_first_run_packet_markdown(self):
        rows = first_run_packet_rows(
            run_id="p1_start",
            stage="p1",
            device_ids=[],
            route_report=None,
            doctor_report=None,
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_first_run_packet_markdown(
                rows,
                Path(tmp) / "start.md",
                run_id="p1_start",
                stage="p1",
                evidence_path="evidence/p1_start.jsonl",
                route_decision_path="evidence/p1_start_route_decision.json",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI First Run Packet P1", text)
        self.assertIn("XP API/SDK coverage boundary", text)
        self.assertIn("Open API Cov", text)
        self.assertIn("Scenario/script coverage guard", text)
        self.assertIn("Open Script Cov", text)
        self.assertIn("Acceptance proof map", text)
        self.assertIn("Open Proof Map", text)
        self.assertIn("Claim scope and handoff wording", text)
        self.assertIn("Open Claim Scope", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("operator guide", text)
        self.assertIn("does not write evidence", text)
        self.assertIn(".\\.venv\\Scripts\\python -m imouse.gui", text)
        self.assertIn("python -m unittest discover -s tests -v", text)
        self.assertIn("python -m compileall -q imouse tests", text)
        self.assertIn("python -m imouse.main --check", text)
        self.assertIn("python -m imouse.receiver_bootstrap", text)
        self.assertIn("--markdown evidence\\p1_start_p1_receiver_bootstrap.md", text)
        self.assertIn("python -m imouse.doctor --route-decision evidence/p1_start_route_decision.json --json", text)
        self.assertIn("python -m imouse.readiness --target p1 --evidence evidence/p1_start.jsonl", text)
        self.assertIn("--dry-run --run-id p1_start", text)

    def test_operator_home_rows_surface_offline_first_blocker(self):
        rows = operator_home_rows(
            run_id="home_p1",
            stage="p1",
            device_ids=[],
            route_report=None,
            doctor_report={"overall": "fail", "counts": {"ok": 11, "warn": 7, "fail": 1}},
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
            evidence_summary={},
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "missing"},
                {"name": "Doctor Report", "requirement": "required", "status": "missing"},
            ],
        )
        by_phase = {row["phase"]: row for row in rows}
        brief = operator_home_brief(rows, stage="p1")

        self.assertEqual(by_phase["Operator intake"]["status"], "fail")
        self.assertEqual(by_phase["Route, kit, and iPhone settings"]["status"], "fail")
        self.assertEqual(by_phase["Receiver screenshot proof"]["status"], "fail")
        self.assertEqual(by_phase["HID click, swipe, and text proof"]["status"], "fail")
        self.assertEqual(by_phase["Claim scope and handoff wording"]["status"], "pending")
        self.assertIn("Open Claim Scope", by_phase["Claim scope and handoff wording"]["gui_action"])
        self.assertEqual(by_phase["Evidence pack, acceptance, and handoff"]["status"], "fail")
        self.assertIn("first_focus=Operator intake", brief)
        self.assertIn("Open Ctrl Ledger", by_phase["HID click, swipe, and text proof"]["gui_action"])

    def test_operator_home_keeps_real_ios_boundary_visible_when_checks_pass(self):
        rows = operator_home_rows(
            run_id="home_ready",
            stage="p1",
            device_ids=["dev_1"],
            source_rows=[{"status": "pass"}],
            industry_rows=[{"status": "pass"}],
            roadmap_rows=[{"status": "pass"}],
            local_rows=[{"status": "pass"}],
            core_rows=[{"status": "pass"}],
            proof_map_rows=[{"key": "claim_boundary", "status": "warn"}],
            claim_scope_rows_data=[{"claim_area": "P1 single-iPhone control", "status": "warn"}],
            event_contract_rows=[{"status": "pass"}],
            route_matrix_rows=[{"status": "pass"}],
            goal_rows=[{"status": "pass"}],
            pitfall_rows=[{"status": "pass"}],
            kit_gate_rows=[{"status": "pass"}],
            ios_sop_rows=[{"status": "pass"}],
            bench_rows=[{"check": "Screenshot and control evidence", "status": "pass"}],
            wizard_rows=[{"lane": "Readiness and handoff", "status": "pass"}],
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={"overall": "ok", "counts": {"ok": 3, "warn": 0, "fail": 0}},
            scenario_summary={"ok": True, "total": 2, "success_count": 2, "failure_count": 0},
            acceptance_report={
                "gate": "p1",
                "ok": True,
                "checks": [
                    {"name": "manual_observation", "status": "pass", "message": "1 manual pass"},
                    {"name": "screenshot_quality", "status": "pass", "message": "1 screenshot ok"},
                ],
            },
            readiness_report={"target": "p1", "ok": True, "claims": {"real_ios_control_verified": False}},
            evidence_exists=True,
            evidence_summary={"total": 8, "by_status": {"pass": 8, "fail": 0}},
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "present"},
                {"name": "Doctor Report", "requirement": "required", "status": "present"},
                {"name": "Acceptance Report", "requirement": "required", "status": "present"},
                {"name": "Readiness Report", "requirement": "required", "status": "present"},
            ],
        )
        by_phase = {row["phase"]: row for row in rows}

        self.assertEqual(by_phase["Operator intake"]["status"], "pass")
        self.assertEqual(by_phase["Knowledge and acceptance boundary"]["status"], "pass")
        self.assertEqual(by_phase["Route, kit, and iPhone settings"]["status"], "pass")
        self.assertEqual(by_phase["Receiver screenshot proof"]["status"], "pass")
        self.assertEqual(by_phase["HID click, swipe, and text proof"]["status"], "warn")
        self.assertEqual(by_phase["Acceptance proof map"]["status"], "warn")
        self.assertEqual(by_phase["Claim scope and handoff wording"]["status"], "warn")
        self.assertIn("Claim scope P1", by_phase["Claim scope and handoff wording"]["current"])
        self.assertEqual(by_phase["Evidence pack, acceptance, and handoff"]["status"], "warn")
        self.assertIn("real_ios_verified=False", by_phase["HID click, swipe, and text proof"]["current"])
        self.assertIn("real_ios_verified=False", by_phase["Evidence pack, acceptance, and handoff"]["current"])

    def test_write_operator_home_markdown(self):
        rows = operator_home_rows(
            run_id="home_md",
            stage="p1",
            device_ids=[],
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )
        with TemporaryDirectory() as tmp:
            out = write_operator_home_markdown(
                rows,
                Path(tmp) / "home.md",
                run_id="home_md",
                stage="p1",
                evidence_path="evidence/home_md.jsonl",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Operator Home P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("Home, Pack, Dashboard, Start Pack, Events, Core, and Roadmap", text)

    def test_gui_evidence_pack_rows_mark_required_missing(self):
        with TemporaryDirectory() as tmp:
            base = Path(tmp) / "evidence"
            base.mkdir()
            (base / "p1_pack.jsonl").write_text("{}", encoding="utf-8")
            rows = gui_evidence_pack_rows(run_id="p1_pack", stage="p1", base_dir=base)
            brief = gui_evidence_pack_brief(rows, stage="p1")

        by_name = {row["name"]: row for row in rows}
        self.assertEqual(by_name["Evidence JSONL"]["status"], "present")
        self.assertEqual(by_name["Doctor Report"]["status"], "missing")
        self.assertEqual(by_name["XP Gap Audit"]["status"], "missing")
        self.assertEqual(by_name["Evidence Timeline"]["requirement"], "recommended")
        self.assertEqual(by_name["Device Evidence Matrix"]["requirement"], "recommended")
        self.assertEqual(by_name["Issue Triage"]["requirement"], "recommended")
        self.assertEqual(by_name["SOP Problem Ledger"]["requirement"], "recommended")
        self.assertEqual(by_name["Rerun Playbook"]["requirement"], "recommended")
        self.assertEqual(by_name["Recovery Drill"]["requirement"], "recommended")
        self.assertEqual(by_name["Real-run Guard"]["requirement"], "recommended")
        self.assertEqual(by_name["Callback Monitor"]["requirement"], "recommended")
        self.assertEqual(by_name["XP Event/Error Contract"]["requirement"], "recommended")
        self.assertEqual(by_name["Scenario Library"]["requirement"], "recommended")
        self.assertEqual(by_name["Field Runbook"]["requirement"], "recommended")
        self.assertEqual(by_name["GUI Operator Home"]["requirement"], "recommended")
        self.assertEqual(by_name["GUI Control Center"]["requirement"], "recommended")
        self.assertEqual(by_name["GUI Knowledge Center"]["requirement"], "recommended")
        self.assertEqual(by_name["GUI Industry SOP Radar"]["requirement"], "recommended")
        self.assertEqual(by_name["GUI Industry Current Snapshot"]["requirement"], "recommended")
        self.assertIn("industry_current_snapshot.md", by_name["GUI Industry Current Snapshot"]["path"])
        self.assertEqual(by_name["GUI Route Procurement SOP"]["requirement"], "recommended")
        self.assertIn("route_procurement_sop.md", by_name["GUI Route Procurement SOP"]["path"])
        self.assertEqual(by_name["Industry Current Snapshot"]["requirement"], "recommended")
        self.assertEqual(by_name["Industry Current Snapshot"]["status"], "present")
        self.assertIn("industry_current_state_snapshot_2026.md", by_name["Industry Current Snapshot"]["path"])
        self.assertEqual(by_name["GUI Mainstream Route Matrix"]["requirement"], "recommended")
        self.assertEqual(by_name["GUI Local Verification"]["requirement"], "recommended")
        self.assertEqual(by_name["GUI Verification Walkthrough"]["requirement"], "recommended")
        self.assertEqual(by_name["XP Core Function Matrix"]["requirement"], "recommended")
        self.assertEqual(by_name["XP API Coverage Board"]["requirement"], "recommended")
        self.assertIn("xp_api_coverage.md", by_name["XP API Coverage Board"]["path"])
        self.assertEqual(by_name["GUI Script Coverage Board"]["requirement"], "recommended")
        self.assertIn("script_coverage.md", by_name["GUI Script Coverage Board"]["path"])
        self.assertEqual(by_name["Acceptance Proof Map"]["requirement"], "recommended")
        self.assertIn("proof_map.md", by_name["Acceptance Proof Map"]["path"])
        self.assertEqual(by_name["Claim Scope Board"]["requirement"], "recommended")
        self.assertIn("claim_scope.md", by_name["Claim Scope Board"]["path"])
        self.assertEqual(by_name["GUI Pitfall Library"]["requirement"], "recommended")
        self.assertEqual(by_name["XP Public Source Ledger"]["requirement"], "recommended")
        self.assertEqual(by_name["XP Source Refresh Board"]["requirement"], "recommended")
        self.assertIn("xp_source_refresh.md", by_name["XP Source Refresh Board"]["path"])
        self.assertEqual(by_name["XP Public Source Audit"]["requirement"], "recommended")
        self.assertIn("xp_public_source_audit.md", by_name["XP Public Source Audit"]["path"])
        self.assertEqual(by_name["XP Package Namespace Guard"]["requirement"], "recommended")
        self.assertIn("xp_package_namespace_guard.md", by_name["XP Package Namespace Guard"]["path"])
        self.assertEqual(by_name["XP Public Source Action Map"]["requirement"], "recommended")
        self.assertEqual(by_name["XP Public Source Action Map"]["status"], "missing")
        self.assertIn("xp_source_action_map.md", by_name["XP Public Source Action Map"]["path"])
        self.assertEqual(by_name["XP Iteration Radar"]["requirement"], "recommended")
        self.assertEqual(by_name["XP Iteration Timeline"]["requirement"], "recommended")
        self.assertIn("xp_iteration_timeline.md", by_name["XP Iteration Timeline"]["path"])
        self.assertEqual(by_name["XP Iteration Drill Board"]["requirement"], "recommended")
        self.assertIn("xp_iteration_drill.md", by_name["XP Iteration Drill Board"]["path"])
        self.assertEqual(by_name["XP Architecture Map"]["requirement"], "recommended")
        self.assertIn("xp_architecture.md", by_name["XP Architecture Map"]["path"])
        self.assertEqual(by_name["XP Hardware Lab"]["requirement"], "recommended")
        self.assertIn("xp_hardware_lab.md", by_name["XP Hardware Lab"]["path"])
        self.assertEqual(by_name["XP Roadmap"]["requirement"], "recommended")
        self.assertEqual(by_name["Device iOS Compatibility Matrix"]["requirement"], "recommended")
        self.assertEqual(by_name["GUI Goal Gate"]["requirement"], "recommended")
        self.assertEqual(by_name["GUI Field Kit Gate"]["requirement"], "recommended")
        self.assertEqual(by_name["iOS Field Settings SOP"]["requirement"], "recommended")
        self.assertEqual(by_name["GUI Hardware Bench"]["requirement"], "recommended")
        self.assertEqual(by_name["Capture Quality Bench"]["requirement"], "recommended")
        self.assertEqual(by_name["Control Response Bench"]["requirement"], "recommended")
        self.assertEqual(by_name["Control Evidence Ledger"]["requirement"], "recommended")
        self.assertIn("control_ledger.md", by_name["Control Evidence Ledger"]["path"])
        self.assertEqual(by_name["Field Evidence Wizard"]["requirement"], "recommended")
        self.assertEqual(by_name["First Run Packet"]["requirement"], "recommended")
        self.assertEqual(by_name["Receiver Candidate Scorecard"]["requirement"], "recommended")
        self.assertIn("receiver_candidate_scorecard.md", by_name["Receiver Candidate Scorecard"]["path"])
        self.assertEqual(by_name["Receiver Route Bootstrap"]["requirement"], "recommended")
        self.assertIn("receiver_bootstrap.md", by_name["Receiver Route Bootstrap"]["path"])
        self.assertEqual(by_name["Receiver Setup Wizard"]["requirement"], "recommended")
        self.assertIn("receiver_setup_wizard.md", by_name["Receiver Setup Wizard"]["path"])
        self.assertEqual(by_name["Receiver Evidence Checklist"]["requirement"], "recommended")
        self.assertIn("receiver_evidence_checklist.md", by_name["Receiver Evidence Checklist"]["path"])
        self.assertEqual(by_name["P1 Trial Board"]["requirement"], "recommended")
        self.assertEqual(by_name["P1 Test Coach"]["requirement"], "recommended")
        self.assertIn("p1_test_coach.md", by_name["P1 Test Coach"]["path"])
        self.assertEqual(by_name["P1 Field Transcript"]["requirement"], "recommended")
        self.assertIn("p1_field_transcript.md", by_name["P1 Field Transcript"]["path"])
        self.assertEqual(by_name["GUI Session Snapshot"]["requirement"], "recommended")
        self.assertEqual(by_name["GUI SOP Board"]["requirement"], "recommended")
        self.assertEqual(by_name["GUI Queue Scenario"]["requirement"], "recommended")
        self.assertEqual(by_name["Template Asset Index"]["requirement"], "recommended")
        self.assertIn("required_missing=", brief)
        self.assertIn("Doctor Report", brief)

    def test_write_gui_evidence_pack_markdown(self):
        rows = [
            {
                "name": "Evidence JSONL",
                "requirement": "required",
                "status": "missing",
                "path": "evidence/p1_pack.jsonl",
                "action": "Record GUI/API/script field events.",
            }
        ]
        with TemporaryDirectory() as tmp:
            out = write_gui_evidence_pack_markdown(
                rows,
                Path(tmp) / "pack.md",
                run_id="p1_pack",
                stage="p1",
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI Evidence Pack P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("artifact index", text)

    def test_gui_evidence_pack_includes_industry_current_snapshot_doc(self):
        rows = gui_evidence_pack_rows(run_id="p1_pack", stage="p1", base_dir="evidence")
        by_name = {row["name"]: row for row in rows}

        self.assertEqual(by_name["Industry Current Snapshot"]["requirement"], "recommended")
        self.assertEqual(by_name["Industry Current Snapshot"]["status"], "present")
        self.assertIn(
            "docs\\industry_current_state_snapshot_2026.md",
            by_name["Industry Current Snapshot"]["path"].replace("/", "\\"),
        )

    def test_route_decision_form_values_formats_lists_and_booleans(self):
        data = decision_template(run_id="p1_form", devices=["dev_1", "dev_2"])
        data["decision"]["allowed_to_run_p1"] = True
        data["decision"]["open_blockers"] = ["uxplay missing", "hid not flashed"]

        values = route_decision_form_values(data)

        self.assertEqual(values["bench.device_ids"], "dev_1, dev_2")
        self.assertEqual(values["decision.allowed_to_run_p1"], "true")
        self.assertEqual(values["decision.open_blockers"], "uxplay missing; hid not flashed")

    def test_apply_route_decision_form_values_normalizes_special_fields(self):
        data = decision_template(run_id="p1_form", devices=["dev_1"])

        updated = apply_route_decision_form_values(
            data,
            {
                "receiver.route": "uxplay",
                "bench.device_ids": "dev_1, dev_2",
                "decision.allowed_to_run_p1": "allowed",
                "decision.open_blockers": "",
            },
        )

        self.assertEqual(updated["receiver"]["route"], "uxplay")
        self.assertEqual(updated["bench"]["device_ids"], ["dev_1", "dev_2"])
        self.assertTrue(updated["decision"]["allowed_to_run_p1"])
        self.assertEqual(updated["decision"]["open_blockers"], [])

    def test_route_decision_form_issues_flags_placeholders_and_not_allowed(self):
        data = decision_template(run_id="p1_form", devices=["dev_1"])

        issues = route_decision_form_issues(data)

        self.assertEqual(issues["receiver.route"], "placeholder")
        self.assertEqual(issues["hid.serial_port"], "placeholder")
        self.assertEqual(issues["decision.allowed_to_run_p1"], "not allowed")
        self.assertEqual(issues["decision.open_blockers"], "placeholder")

    def test_route_decision_issue_rows_include_actions(self):
        data = decision_template(run_id="p1_form", devices=["dev_1"])

        rows = route_decision_issue_rows(data)
        brief = route_decision_issue_brief(data)

        receiver = next(row for row in rows if row["path"] == "receiver.route")
        self.assertEqual(receiver["issue"], "placeholder")
        self.assertIn("Replace placeholder", receiver["action"])
        self.assertIn("issues=", brief)
        self.assertIn("placeholder=", brief)

    def test_write_route_decision_issue_markdown(self):
        data = decision_template(run_id="p1_form", devices=["dev_1"])

        with TemporaryDirectory() as tmp:
            out = write_route_decision_issue_markdown(data, Path(tmp) / "checklist.md")
            text = out.read_text(encoding="utf-8")

        self.assertIn("Route Decision Fill Checklist", text)
        self.assertIn("receiver.route", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)

    def test_receiver_route_gate_rows_block_missing_route_source(self):
        rows = receiver_route_gate_rows(
            stage="p1",
            route_decision=None,
            route_report=None,
            doctor_report=None,
            evidence_exists=False,
        )
        by_lane = {row["lane"]: row for row in rows}
        brief = receiver_route_gate_brief(rows, stage="p1")

        self.assertEqual(by_lane["Route decision source"]["status"], "fail")
        self.assertEqual(by_lane["Route validation and open blockers"]["status"], "pending")
        self.assertEqual(by_lane["Receiver provider config"]["status"], "warn")
        self.assertIn("Edit Route", by_lane["Route decision source"]["gui_action"])
        self.assertIn("first_gap=Route decision source", brief)

    def test_receiver_route_gate_accepts_valid_windows_receiver_without_uxplay_fail(self):
        with TemporaryDirectory() as tmp:
            exe = Path(tmp) / "receiverx.exe"
            exe.write_text("fake", encoding="utf-8")
            route = decision_template(run_id="p1_receiver", devices=["dev_1"])
            apply_route_decision_form_values(route, {
                "receiver.route": "windows_receiver",
                "receiver.name": "ReceiverX",
                "receiver.version": "1.2.3",
                "receiver.path": str(exe),
                "receiver.start_command": f'"{exe}" --name imouse-dev-01',
                "receiver.airplay_name": "imouse-dev-01",
                "receiver.capture_method": "window",
                "receiver.window_binding.title": "imouse-dev-01",
                "receiver.window_binding.process": "receiverx.exe",
                "receiver.window_binding.handle": "",
                "receiver.license_status": "trial",
                "decision.allowed_to_run_p1": "true",
                "decision.open_blockers": "",
            })
            rows = receiver_route_gate_rows(
                stage="p1",
                route_decision=route,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={
                    "overall": "warn",
                    "counts": {"ok": 1, "warn": 1, "fail": 0},
                    "checks": [
                        {
                            "name": "receiver_provider",
                            "status": "ok",
                            "message": "Receiver provider ready for preflight: windows_receiver",
                        },
                        {
                            "name": "binary:uxplay",
                            "status": "warn",
                            "message": "UxPlay not required for selected receiver route: windows_receiver",
                        },
                    ],
                },
                acceptance_report=None,
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=False,
                route_decision_path=Path(tmp) / "route.json",
            )

        by_lane = {row["lane"]: row for row in rows}
        self.assertEqual(by_lane["Receiver provider config"]["status"], "pass")
        self.assertEqual(by_lane["UxPlay dependency and alternate route"]["status"], "pass")
        self.assertIn("binary:uxplay=warn", by_lane["UxPlay dependency and alternate route"]["current"])
        self.assertEqual(by_lane["Capture binding fields"]["status"], "pass")
        self.assertEqual(by_lane["Screenshot proof boundary"]["status"], "pending")
        self.assertEqual(by_lane["Claim boundary"]["status"], "pending")

    def test_write_receiver_route_gate_markdown_keeps_claim_boundary(self):
        rows = receiver_route_gate_rows(stage="p1", route_decision=None, doctor_report=None)
        with TemporaryDirectory() as tmp:
            out = write_receiver_route_gate_markdown(
                rows,
                Path(tmp) / "receiver_gate.md",
                run_id="p1_receiver",
                stage="p1",
                evidence_path="evidence/p1_receiver.jsonl",
                route_decision_path="evidence/p1_receiver_route_decision.json",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("Receiver Route Gate P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("does not prove real iOS control", text)

    def test_receiver_setup_wizard_blocks_selected_uxplay_when_binary_missing(self):
        route = decision_template(run_id="p1_receiver_setup", devices=["dev_1"])
        apply_route_decision_form_values(route, {
            "receiver.route": "uxplay",
            "receiver.name": "UxPlay",
            "receiver.version": "1.0",
            "receiver.path": "C:/tools/uxplay.exe",
            "receiver.start_command": "uxplay -n imouse-dev-01",
            "receiver.airplay_name": "imouse-dev-01",
            "receiver.capture_method": "window",
            "receiver.window_binding.title": "imouse-dev-01",
            "receiver.window_binding.process": "uxplay.exe",
            "decision.allowed_to_run_p1": "true",
            "decision.open_blockers": "",
        })

        rows = receiver_setup_wizard_rows(
            stage="p1",
            route_decision=route,
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={
                "overall": "fail",
                "counts": {"ok": 0, "warn": 0, "fail": 1},
                "checks": [
                    {"name": "binary:uxplay", "status": "fail", "message": "uxplay MISSING"},
                ],
            },
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )

        by_step = {row["step"]: row for row in rows}
        self.assertEqual(by_step["4. UxPlay install lane"]["status"], "fail")
        self.assertIn("binary:uxplay=fail", by_step["4. UxPlay install lane"]["current"])
        self.assertEqual(by_step["9. Screenshot bench before HID"]["status"], "pending")
        self.assertIn("first_gap=4. UxPlay install lane", receiver_setup_wizard_brief(rows, stage="p1"))

    def test_receiver_setup_wizard_windows_receiver_downgrades_uxplay_dependency(self):
        with TemporaryDirectory() as tmp:
            exe = Path(tmp) / "receiverx.exe"
            exe.write_text("fake", encoding="utf-8")
            route = decision_template(run_id="p1_receiver_setup_win", devices=["dev_1"])
            apply_route_decision_form_values(route, {
                "receiver.route": "windows_receiver",
                "receiver.name": "ReceiverX",
                "receiver.version": "1.2.3",
                "receiver.path": str(exe),
                "receiver.start_command": f'"{exe}" --name imouse-dev-01',
                "receiver.airplay_name": "imouse-dev-01",
                "receiver.capture_method": "window",
                "receiver.window_binding.title": "imouse-dev-01",
                "receiver.window_binding.process": "receiverx.exe",
                "receiver.window_binding.handle": "",
                "receiver.license_status": "trial",
                "decision.allowed_to_run_p1": "true",
                "decision.open_blockers": "",
            })

            rows = receiver_setup_wizard_rows(
                stage="p1",
                route_decision=route,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={
                    "overall": "warn",
                    "counts": {"ok": 1, "warn": 1, "fail": 0},
                    "checks": [
                        {
                            "name": "receiver_provider",
                            "status": "ok",
                            "message": "Receiver provider ready for preflight: windows_receiver",
                        },
                        {
                            "name": "binary:uxplay",
                            "status": "warn",
                            "message": "UxPlay not required for selected receiver route: windows_receiver",
                        },
                    ],
                },
                acceptance_report={
                    "gate": "p1",
                    "ok": False,
                    "checks": [
                        {
                            "name": "screenshot_quality",
                            "status": "pass",
                            "message": "visible screenshot",
                        },
                        {
                            "name": "manual_observation",
                            "status": "pending",
                            "message": "manual missing",
                        },
                    ],
                },
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                route_decision_path=Path(tmp) / "route.json",
            )

        by_step = {row["step"]: row for row in rows}
        self.assertEqual(by_step["4. UxPlay install lane"]["status"], "pass")
        self.assertIn("uxplay not required", by_step["4. UxPlay install lane"]["current"])
        self.assertEqual(by_step["5. Windows receiver lane"]["status"], "pass")
        self.assertEqual(by_step["7. Capture binding"]["status"], "pass")
        self.assertEqual(by_step["8. iPhone to receiver binding"]["status"], "pass")
        self.assertEqual(by_step["11. Handoff and claim boundary"]["status"], "warn")

    def test_write_receiver_setup_wizard_markdown_keeps_claim_boundary(self):
        rows = receiver_setup_wizard_rows(stage="p1", route_decision=None, doctor_report=None)
        with TemporaryDirectory() as tmp:
            out = write_receiver_setup_wizard_markdown(
                rows,
                Path(tmp) / "receiver_setup.md",
                run_id="p1_receiver_setup",
                stage="p1",
                evidence_path="evidence/p1_receiver_setup.jsonl",
                route_decision_path="evidence/p1_receiver_setup_route_decision.json",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("Receiver Setup Wizard P1", text)
        self.assertIn("Copy-Ready Commands", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not install software", text)
        self.assertIn("does not prove real iPhone response", text)

    def test_receiver_evidence_checklist_blocks_missing_route_source(self):
        rows = receiver_evidence_checklist_rows(
            stage="p1",
            route_decision=None,
            route_report=None,
            doctor_report=None,
            evidence_exists=False,
        )
        by_checkpoint = {row["checkpoint"]: row for row in rows}
        brief = receiver_evidence_checklist_brief(rows, stage="p1")

        self.assertEqual(by_checkpoint["1. Lock one receiver route"]["status"], "fail")
        self.assertEqual(by_checkpoint["3. Route-aware Doctor"]["status"], "pending")
        self.assertEqual(by_checkpoint["5. Baseline screenshot proof"]["status"], "fail")
        self.assertIn("first_stop=1. Lock one receiver route", brief)

    def test_receiver_evidence_checklist_windows_route_moves_to_capture_before_hid(self):
        with TemporaryDirectory() as tmp:
            exe = Path(tmp) / "receiverx.exe"
            exe.write_text("fake", encoding="utf-8")
            route = decision_template(run_id="p1_receiver_evidence_win", devices=["dev_1"])
            apply_route_decision_form_values(route, {
                "receiver.route": "windows_receiver",
                "receiver.name": "ReceiverX",
                "receiver.version": "1.2.3",
                "receiver.path": str(exe),
                "receiver.start_command": f'"{exe}" --name imouse-dev-01',
                "receiver.airplay_name": "imouse-dev-01",
                "receiver.capture_method": "window",
                "receiver.window_binding.title": "imouse-dev-01",
                "receiver.window_binding.process": "receiverx.exe",
                "receiver.window_binding.handle": "",
                "receiver.license_status": "paid lab license",
                "hid.route": "self_built",
                "hid.provider": "lab_hid",
                "hid.id": "hid-01",
                "hid.firmware": "1.0",
                "hid.serial_port": "COM7",
                "iphone.model": "iPhone 15",
                "iphone.ios_version": "18.5",
                "decision.allowed_to_run_p1": "true",
                "decision.open_blockers": "",
            })

            rows = receiver_evidence_checklist_rows(
                stage="p1",
                route_decision=route,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={
                    "overall": "warn",
                    "counts": {"ok": 1, "warn": 1, "fail": 0},
                    "checks": [
                        {
                            "name": "receiver_provider",
                            "status": "ok",
                            "message": "Receiver provider ready for preflight: windows_receiver",
                        },
                        {
                            "name": "binary:uxplay",
                            "status": "warn",
                            "message": "UxPlay not required for selected receiver route: windows_receiver",
                        },
                    ],
                },
                acceptance_report={
                    "gate": "p1",
                    "ok": False,
                    "checks": [
                        {"name": "component_traceability", "status": "pass", "message": "metadata ok"},
                        {"name": "screenshot_quality", "status": "pass", "message": "visible screenshot"},
                        {"name": "manual_observation", "status": "pending", "message": "manual missing"},
                    ],
                },
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                evidence_summary={"total": 14, "by_status": {"pass": 14, "fail": 0}, "metrics": {"count": 2}},
                route_decision_path=Path(tmp) / "route.json",
                evidence_path=Path(tmp) / "p1_receiver_evidence_win.jsonl",
            )

        by_checkpoint = {row["checkpoint"]: row for row in rows}
        self.assertEqual(by_checkpoint["1. Lock one receiver route"]["status"], "pass")
        self.assertEqual(by_checkpoint["2. Receiver provider preflight"]["status"], "pass")
        self.assertEqual(by_checkpoint["3. Route-aware Doctor"]["status"], "pass")
        self.assertIn("binary:uxplay=warn", by_checkpoint["3. Route-aware Doctor"]["current"])
        self.assertEqual(by_checkpoint["4. Bind receiver identity to device"]["status"], "pass")
        self.assertEqual(by_checkpoint["5. Baseline screenshot proof"]["status"], "pass")
        self.assertEqual(by_checkpoint["6. Receiver capture probe set"]["status"], "ready")
        self.assertEqual(by_checkpoint["8. HID handoff stop line"]["status"], "pending")
        self.assertEqual(by_checkpoint["9. Acceptance and claim closure"]["status"], "fail")

    def test_write_receiver_evidence_checklist_markdown_keeps_claim_boundary_and_commands(self):
        rows = receiver_evidence_checklist_rows(stage="p1", route_decision=None, doctor_report=None)
        with TemporaryDirectory() as tmp:
            out = write_receiver_evidence_checklist_markdown(
                rows,
                Path(tmp) / "receiver_evidence.md",
                run_id="p1_receiver_evidence",
                stage="p1",
                evidence_path="evidence/p1_receiver_evidence.jsonl",
                route_decision_path="evidence/p1_receiver_evidence_route_decision.json",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("Receiver Evidence Checklist P1", text)
        self.assertIn("Copy-Ready Commands", text)
        self.assertIn("p1_receiver_capture_probe.json", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("does not prove real iPhone response", text)

    def test_receiver_candidate_scorecard_blocks_uxplay_when_binary_missing(self):
        route = decision_template(run_id="p1_receiver_score", devices=["dev_1"])
        apply_route_decision_form_values(route, {
            "receiver.route": "uxplay",
            "receiver.name": "UxPlay",
            "receiver.version": "1.0",
            "receiver.path": "C:/tools/uxplay.exe",
            "receiver.start_command": "uxplay -n imouse-dev-01",
            "receiver.airplay_name": "imouse-dev-01",
            "receiver.capture_method": "window",
            "receiver.window_binding.title": "imouse-dev-01",
            "receiver.window_binding.process": "uxplay.exe",
            "decision.allowed_to_run_p1": "true",
            "decision.open_blockers": "",
        })

        rows = receiver_candidate_scorecard_rows(
            stage="p1",
            route_decision=route,
            route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
            doctor_report={
                "overall": "fail",
                "counts": {"ok": 0, "warn": 0, "fail": 1},
                "checks": [
                    {"name": "binary:uxplay", "status": "fail", "message": "uxplay MISSING"},
                ],
            },
            readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
            evidence_exists=False,
        )

        by_candidate = {row["candidate"]: row for row in rows}
        uxplay = by_candidate["UxPlay open receiver"]
        self.assertEqual(uxplay["status"], "fail")
        self.assertEqual(uxplay["recommendation"], "blocked")
        self.assertIn("binary:uxplay=fail", uxplay["current"])
        self.assertIn("binary:uxplay=fail", uxplay["gaps"])
        self.assertIn("first_gap=UxPlay open receiver", receiver_candidate_scorecard_brief(rows, stage="p1"))

    def test_receiver_candidate_scorecard_recommends_valid_windows_receiver_without_claim(self):
        with TemporaryDirectory() as tmp:
            exe = Path(tmp) / "receiverx.exe"
            exe.write_text("fake", encoding="utf-8")
            route = decision_template(run_id="p1_receiver_score_win", devices=["dev_1"])
            apply_route_decision_form_values(route, {
                "receiver.route": "windows_receiver",
                "receiver.name": "ReceiverX",
                "receiver.version": "1.2.3",
                "receiver.path": str(exe),
                "receiver.start_command": f'"{exe}" --name imouse-dev-01',
                "receiver.airplay_name": "imouse-dev-01",
                "receiver.capture_method": "window",
                "receiver.window_binding.title": "imouse-dev-01",
                "receiver.window_binding.process": "receiverx.exe",
                "receiver.window_binding.handle": "",
                "receiver.license_status": "paid lab license",
                "decision.allowed_to_run_p1": "true",
                "decision.open_blockers": "",
            })

            rows = receiver_candidate_scorecard_rows(
                stage="p1",
                route_decision=route,
                route_report={"ok": True, "ready": True, "target_stage": "p1", "blockers": []},
                doctor_report={
                    "overall": "warn",
                    "counts": {"ok": 1, "warn": 1, "fail": 0},
                    "checks": [
                        {
                            "name": "receiver_provider",
                            "status": "ok",
                            "message": "Receiver provider ready for preflight: windows_receiver",
                        },
                        {
                            "name": "binary:uxplay",
                            "status": "warn",
                            "message": "UxPlay not required for selected receiver route: windows_receiver",
                        },
                    ],
                },
                acceptance_report={
                    "gate": "p1",
                    "ok": False,
                    "checks": [
                        {
                            "name": "screenshot_quality",
                            "status": "pass",
                            "message": "visible screenshot",
                        },
                        {
                            "name": "manual_observation",
                            "status": "pending",
                            "message": "manual missing",
                        },
                    ],
                },
                readiness_report={"target": "p1", "ok": False, "claims": {"real_ios_control_verified": False}},
                evidence_exists=True,
                route_decision_path=Path(tmp) / "route.json",
            )

        by_candidate = {row["candidate"]: row for row in rows}
        windows = by_candidate["Windows AirPlay receiver"]
        uxplay = by_candidate["UxPlay open receiver"]
        self.assertEqual(windows["status"], "ready")
        self.assertEqual(windows["recommendation"], "recommended")
        self.assertEqual(windows["selected"], "yes")
        self.assertIn("binary:uxplay=warn", windows["current"])
        self.assertIn("recommended=Windows AirPlay receiver", receiver_candidate_scorecard_brief(rows, stage="p1"))
        self.assertNotEqual(uxplay["recommendation"], "recommended")
        self.assertLess(int(uxplay["score"]), int(windows["score"]))

    def test_write_receiver_candidate_scorecard_markdown_keeps_claim_boundary(self):
        rows = receiver_candidate_scorecard_rows(
            stage="p1",
            route_decision=None,
            doctor_report={
                "overall": "fail",
                "counts": {"ok": 0, "warn": 0, "fail": 1},
                "checks": [
                    {"name": "binary:uxplay", "status": "fail", "message": "uxplay MISSING"},
                ],
            },
        )
        with TemporaryDirectory() as tmp:
            out = write_receiver_candidate_scorecard_markdown(
                rows,
                Path(tmp) / "receiver_scorecard.md",
                run_id="p1_receiver_score",
                stage="p1",
                evidence_path="evidence/p1_receiver_score.jsonl",
                route_decision_path="evidence/p1_receiver_score_route_decision.json",
                readiness_report={"claims": {"real_ios_control_verified": False}},
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("Receiver Candidate Scorecard P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write JSONL evidence", text)
        self.assertIn("prove real iPhone response", text)
        self.assertIn("prove iOS perfect control", text)
        self.assertIn("prove XP parity", text)

    def test_route_decision_metadata_prefill_values_maps_gui_metadata(self):
        values = route_decision_metadata_prefill_values(
            device_ids=["dev_1", "dev_2"],
            receiver_provider="wired_capture",
            capture_method="window",
            hid_provider="self_hid",
            hid_id="hid-01",
            serial_port="COM7",
            iphone_id="iphone-01",
            ios_version="17.7",
            receiver_name="imouse-dev-01",
            receiver_version="1.2.3",
        )

        self.assertEqual(values["receiver.route"], "wired")
        self.assertEqual(values["receiver.capture_method"], "window")
        self.assertEqual(values["hid.route"], "self_built")
        self.assertEqual(values["hid.serial_port"], "COM7")
        self.assertEqual(values["bench.device_id"], "dev_1")
        self.assertEqual(values["bench.device_ids"], "dev_1, dev_2")
        self.assertEqual(values["iphone.ios_version"], "17.7")

    def test_command_queue_rows_and_brief(self):
        items = [
            {"action": "click", "device_ids": ["dev_1", "dev_2"], "x": 10, "y": 20},
            {"action": "type", "device_ids": ["dev_1"], "text": "hello"},
        ]

        rows = command_queue_rows(items)
        brief = command_queue_brief(items)

        self.assertEqual(rows[0]["devices"], "dev_1, dev_2")
        self.assertEqual(rows[0]["payload"], "x=10, y=20")
        self.assertIn("click=1", brief)
        self.assertIn("type=1", brief)

    def test_build_command_queue_scenario_expands_devices_and_repeat(self):
        scenario = build_command_queue_scenario(
            [
                {"action": "click", "device_ids": ["dev_1", "dev_2"], "x": 10, "y": 20},
                {"action": "screenshot", "device_ids": ["dev_1"]},
                {
                    "action": "find_image_then_click",
                    "device_ids": ["dev_1"],
                    "template_path": "templates/ok.png",
                    "threshold": 0.91,
                    "region": [1, 2, 3, 4],
                },
            ],
            repeat=2,
            wait_between=0.5,
            name="queue",
        )

        repeat = scenario["steps"][0]
        steps = repeat["steps"]
        self.assertEqual(repeat["action"], "repeat")
        self.assertEqual(repeat["count"], 2)
        self.assertEqual(steps[0]["device_id"], "dev_1")
        self.assertEqual(steps[1]["device_id"], "dev_2")
        self.assertEqual(steps[2]["action"], "screenshot")
        self.assertEqual(steps[3]["action"], "find_image_then_click")
        self.assertEqual(steps[3]["region"], [1, 2, 3, 4])

    def test_write_command_queue_scenario(self):
        with TemporaryDirectory() as tmp:
            out = write_command_queue_scenario(
                [{"action": "type", "device_ids": ["dev_1"], "text": "hello"}],
                Path(tmp) / "queue.json",
                repeat=1,
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("GUI command queue", text)
        self.assertIn("\"action\": \"type\"", text)

    def test_template_asset_rows_and_markdown(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "templates"
            root.mkdir()
            ok_path = root / "ok.png"
            image = Image.new("RGB", (24, 24), (40, 90, 180))
            for x in range(12):
                for y in range(24):
                    image.putpixel((x, y), (220, 230, 240))
            image.save(ok_path)
            Image.new("RGB", (24, 24), (128, 128, 128)).save(root / "flat.png")

            rows = template_asset_rows(root)
            brief = template_asset_brief(rows)
            out = write_template_asset_index_markdown(rows, Path(tmp) / "assets.md")
            text = out.read_text(encoding="utf-8")

        by_name = {row["name"]: row for row in rows}
        self.assertEqual(by_name["ok.png"]["status"], "ok")
        self.assertEqual(by_name["flat.png"]["reason"], "low_texture")
        self.assertIn("total=2", brief)
        self.assertIn("GUI Template Asset Index", text)
        self.assertIn("Real iOS control verified: `False`", text)

    def test_write_gui_session_snapshot_markdown(self):
        snapshot = build_gui_session_snapshot(
            run_id="p1_session",
            stage="p1",
            server_url="http://127.0.0.1:9911",
            device_ids=["dev_1"],
            evidence_path="evidence/p1_session.jsonl",
            evidence_summary={"total": 2, "by_status": {"pass": 1, "fail": 1, "info": 0, "skip": 0}},
            route_decision_path="evidence/p1_session_route_decision.json",
            route_report={"target_stage": "p1", "ok": False, "ready": False, "blockers": [{"name": "route"}]},
            doctor_report={"overall": "fail", "counts": {"ok": 1, "warn": 0, "fail": 1}},
            readiness_report={
                "target": "p1",
                "ok": False,
                "stage_status": {"p0": {"ok": True}, "p1": {"ok": False}},
                "blockers": [{"name": "field_evidence"}],
            },
            live_probe_rows_data=[
                {"label": "Route decision", "status": "fail", "message": "not ready", "action": "Validate"},
            ],
            sop_rows_data=[
                {"step": "1", "workstream": "Route decision", "status": "fail", "current": "not ready", "next_action": "Validate", "evidence": "Route report"},
            ],
            command_queue_rows_data=[
                {"index": "1", "action": "click", "devices": "dev_1", "payload": "x=10, y=20"},
            ],
            template_asset_rows_data=[
                {"name": "flat.png", "status": "fail", "reason": "low_texture", "size": "24x24", "path": "templates/flat.png"},
            ],
            artifact_rows=[
                {"name": "Evidence JSONL", "requirement": "required", "status": "present", "path": "evidence/p1_session.jsonl", "action": "Record evidence"},
            ],
        )
        with TemporaryDirectory() as tmp:
            out = write_gui_session_snapshot_markdown(snapshot, Path(tmp) / "session.md")
            text = out.read_text(encoding="utf-8")

        brief = gui_session_snapshot_brief(snapshot)
        self.assertIn("GUI Session Snapshot P1", text)
        self.assertIn("Snapshot verifies real iOS control: `False`", text)
        self.assertIn("Route decision", text)
        self.assertIn("SOP Board", text)
        self.assertIn("Primary command", text)
        self.assertIn("Edit Route", text)
        self.assertIn("flat.png", text)
        self.assertIn("live_fail=1", brief)
        self.assertIn("sop_blockers=1", brief)
        self.assertIn("template_fail=1", brief)

    def test_manual_observation_details_includes_category_when_set(self):
        details = manual_observation_details(
            note="dev_1 did not move",
            selected_device="dev_1",
            click_x=100,
            click_y=200,
            category="hid",
        )

        self.assertTrue(details["manual"])
        self.assertEqual(details["category"], "hid")
        self.assertEqual(details["click"], {"x": 100, "y": 200})

    def test_manual_observation_details_omits_empty_category(self):
        details = manual_observation_details(
            note="observed",
            selected_device="dev_1",
            click_x=100,
            click_y=200,
        )

        self.assertNotIn("category", details)

    def test_component_metadata_details_contains_acceptance_fields(self):
        details = component_metadata_details(
            device_id="dev_1",
            receiver_provider="uxplay",
            capture_method="window",
            hid_provider="ch9329",
            hid_id="hid01",
            serial_port="COM3",
            iphone_id="ip01",
            ios_version="17.7",
            receiver_name="imouse-dev-01",
            receiver_version="1.0",
        )

        self.assertTrue(details["manual"])
        self.assertEqual(details["device_id"], "dev_1")
        self.assertEqual(details["receiver_provider"], "uxplay")
        self.assertEqual(details["capture_method"], "window")
        self.assertEqual(details["hid_provider"], "ch9329")
        self.assertEqual(details["hid_id"], "hid01")
        self.assertEqual(details["serial_port"], "COM3")
        self.assertEqual(details["iphone_id"], "ip01")
        self.assertEqual(details["ios_version"], "17.7")

    def test_component_metadata_details_requires_hid_or_serial_and_ios(self):
        with self.assertRaisesRegex(ValueError, "hid_id_or_serial_port"):
            component_metadata_details(
                device_id="dev_1",
                receiver_provider="uxplay",
                capture_method="window",
                hid_provider="ch9329",
                hid_id="",
                serial_port="",
                iphone_id="ip01",
                ios_version="17.7",
            )

        with self.assertRaisesRegex(ValueError, "ios_version"):
            component_metadata_details(
                device_id="dev_1",
                receiver_provider="uxplay",
                capture_method="window",
                hid_provider="ch9329",
                hid_id="hid01",
                serial_port="COM3",
                iphone_id="ip01",
                ios_version="",
            )

    def test_gui_success_evidence_status_for_doctor(self):
        app = ImouseGui.__new__(ImouseGui)

        self.assertEqual(
            app._success_evidence_status("Preflight doctor", {"report": {"overall": "fail"}}),
            "fail",
        )
        self.assertEqual(
            app._success_evidence_status("Preflight doctor", {"report": {"overall": "warn"}}),
            "info",
        )
        self.assertEqual(
            app._success_evidence_status("Preflight doctor", {"report": {"overall": "ok"}}),
            "pass",
        )

    def test_gui_success_evidence_status_for_failed_scenario_summary(self):
        app = ImouseGui.__new__(ImouseGui)

        self.assertEqual(
            app._success_evidence_status("Scenario run", {"summary": {"ok": False}}),
            "fail",
        )

    def test_gui_success_evidence_status_for_failed_screenshot_quality(self):
        app = ImouseGui.__new__(ImouseGui)

        self.assertEqual(
            app._success_evidence_status("Screenshot", {"screenshot_quality": {"ok": False, "reason": "black_screen"}}),
            "fail",
        )
        self.assertEqual(
            app._success_evidence_status("Screenshot", {"screenshot_quality": {"ok": True, "reason": "ok"}}),
            "pass",
        )

    def test_gui_success_evidence_status_for_capture_bench(self):
        app = ImouseGui.__new__(ImouseGui)

        self.assertEqual(
            app._success_evidence_status("Capture quality bench", {"ok": False, "bench_status": "fail"}),
            "fail",
        )
        self.assertEqual(
            app._success_evidence_status("Capture quality bench", {"ok": True, "bench_status": "pass"}),
            "pass",
        )

    def test_gui_success_evidence_status_for_failed_readiness(self):
        app = ImouseGui.__new__(ImouseGui)

        self.assertEqual(
            app._success_evidence_status("Readiness audit", {"report": {"ok": False}}),
            "fail",
        )

    def test_readiness_audit_does_not_default_to_selected_device_id(self):
        class DummyTree:
            def selection(self):
                return []

        app = ImouseGui.__new__(ImouseGui)
        app.device_tree = DummyTree()
        app.selected_device = type("Var", (), {"get": lambda self: ""})()
        app.device_id = type("Var", (), {"get": lambda self: "dev_1"})()

        self.assertEqual(app._evidence_device_ids("Readiness audit", {"ok": False}), [])


if __name__ == "__main__":
    unittest.main()
