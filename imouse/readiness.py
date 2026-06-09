"""Project readiness audit for the iMouse XP benchmark prototype."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable, Optional

from .acceptance import GATE_LEVELS, evaluate_acceptance
from .doctor import run_doctor


STAGES = ("p0", "p1", "p2", "p3", "p4")

REQUIRED_DOCS = [
    "docs/imouse_xp_research.md",
    "docs/imouse_xp_architecture_map.md",
    "docs/imouse_xp_iteration_lessons.md",
    "docs/industry_current_state_snapshot_2026.md",
    "docs/industry_landscape_2026.md",
    "docs/industry_sop_playbook.md",
    "docs/mainstream_route_decision.md",
    "docs/ios_group_control_sop.md",
    "docs/xp_parity_matrix.md",
    "docs/field_test_matrix.md",
    "docs/hardware_test_bench_checklist.md",
    "docs/receiver_capture_selection.md",
    "docs/hid_hardware_protocol_benchmark.md",
    "docs/p1_single_device_runbook.md",
    "docs/p2_p3_stability_runbook.md",
    "docs/follow_along_test_method.md",
    "docs/xp_core_backlog.md",
    "docs/verification_plan.md",
    "docs/gui_prototype.md",
    "docs/gui_live_probe.md",
    "docs/gui_verification_walkthrough.md",
    "docs/gui_field_evidence_runner.md",
    "docs/gui_route_procurement_sop.md",
    "docs/gui_operator_home.md",
    "docs/gui_industry_current_snapshot.md",
    "docs/gui_control_evidence_ledger.md",
    "docs/gui_p1_test_coach.md",
    "docs/gui_receiver_candidate_scorecard.md",
    "docs/gui_receiver_setup_wizard.md",
    "docs/gui_receiver_evidence_checklist.md",
    "docs/receiver_route_bootstrap.md",
    "docs/gui_p1_field_transcript.md",
    "docs/gui_xp_source_refresh_board.md",
    "docs/gui_xp_iteration_timeline.md",
    "docs/gui_xp_iteration_drill_board.md",
    "docs/gui_xp_hardware_lab.md",
    "docs/gui_xp_api_coverage_board.md",
    "docs/gui_script_coverage_board.md",
    "docs/gui_real_run_guard.md",
    "docs/gui_acceptance_proof_map.md",
    "docs/gui_claim_scope.md",
    "docs/gui_goal_gate.md",
    "docs/xp_public_source_audit.md",
    "docs/gui_xp_package_namespace_guard.md",
    "docs/xp_public_source_action_map.md",
    "docs/xp_gap_audit.md",
    "docs/operator_worksheet.md",
    "docs/sop_problem_ledger.md",
    "docs/xp_event_error_contract.md",
    "docs/script_runner.md",
    "docs/validation_evidence.md",
    "docs/preflight_doctor.md",
    "docs/xp_api_compat.md",
]

REQUIRED_SCRIPTS = [
    "scripts/p1_single_device_control_probe.json",
    "scripts/single_device_smoke.json",
    "scripts/p1_receiver_capture_probe.json",
    "scripts/p2_single_device_stability.json",
    "scripts/pilot_4_group_smoke.json",
    "scripts/p3_pilot4_30min_watchdog.json",
    "scripts/stable_10_group_watchdog.json",
]

REQUIRED_MODULES = [
    "imouse/server.py",
    "imouse/gui.py",
    "imouse/xp_client.py",
    "imouse/script_runner.py",
    "imouse/validation.py",
    "imouse/acceptance.py",
    "imouse/doctor.py",
    "imouse/receiver_provider.py",
    "imouse/receiver_bootstrap.py",
    "imouse/field_packet.py",
    "imouse/operator_worksheet.py",
    "imouse/xp_gap_audit.py",
    "imouse/source_audit.py",
    "imouse/route_decision.py",
    "imouse/calibration.py",
    "imouse/metrics.py",
    "imouse/vision.py",
    "imouse/hardware.py",
]


def _check(name: str, status: str, message: str, details: Optional[dict] = None) -> dict:
    return {
        "name": name,
        "status": status,
        "message": message,
        "details": details or {},
    }


def _path_group_check(root: Path, name: str, paths: Iterable[str]) -> dict:
    expected = list(paths)
    present = []
    missing = []
    for relative in expected:
        path = root / relative
        if path.exists():
            present.append(relative)
        else:
            missing.append(relative)
    return _check(
        name,
        "pass" if not missing else "fail",
        f"{len(present)}/{len(expected)} required path(s) present",
        {"present": present, "missing": missing},
    )


def _doctor_check(report: dict) -> dict:
    overall = str(report.get("overall", "unknown"))
    if overall == "ok":
        status = "pass"
    elif overall == "warn":
        status = "warn"
    else:
        status = "fail"
    fail_names = [
        item.get("name", "")
        for item in report.get("checks", [])
        if item.get("status") == "fail"
    ]
    return _check(
        "doctor",
        status,
        f"doctor overall={overall}",
        {
            "counts": report.get("counts", {}),
            "fail_checks": fail_names,
        },
    )


def _acceptance_checks(evidence_jsonl: str | Path | None, gates: Iterable[str]) -> tuple[list[dict], dict]:
    checks = []
    gate_reports: dict[str, dict] = {}
    if not evidence_jsonl:
        checks.append(_check(
            "field_evidence",
            "fail",
            "No evidence JSONL supplied; real iPhone control is unverified",
        ))
        return checks, gate_reports

    path = Path(evidence_jsonl)
    if not path.exists():
        checks.append(_check(
            "field_evidence",
            "fail",
            f"Evidence JSONL not found: {path}",
            {"path": str(path)},
        ))
        return checks, gate_reports

    checks.append(_check("field_evidence", "pass", f"Evidence JSONL found: {path}", {"path": str(path)}))
    for gate in gates:
        gate_name = gate.lower().strip()
        if gate_name not in GATE_LEVELS:
            checks.append(_check("acceptance", "fail", f"Unsupported gate: {gate}"))
            continue
        try:
            report = evaluate_acceptance(path, gate=gate_name)
        except Exception as exc:
            checks.append(_check(f"acceptance:{gate_name}", "fail", str(exc), {"path": str(path)}))
            continue
        gate_reports[gate_name] = report
        failed = [item for item in report.get("checks", []) if item.get("status") != "pass"]
        checks.append(_check(
            f"acceptance:{gate_name}",
            "pass" if report.get("ok") else "fail",
            f"{gate_name.upper()} {'PASS' if report.get('ok') else 'FAIL'}",
            {
                "criteria": report.get("criteria", {}),
                "failed_checks": failed,
            },
        ))
    return checks, gate_reports


def _stage_status(
    *,
    asset_ok: bool,
    doctor_ok: bool,
    gate_reports: dict[str, dict],
) -> dict:
    p1_ok = bool(gate_reports.get("p1", {}).get("ok")) and doctor_ok
    p2_ok = bool(gate_reports.get("p2", {}).get("ok")) and doctor_ok
    p3_ok = bool(gate_reports.get("p3", {}).get("ok")) and doctor_ok
    p4_ok = bool(gate_reports.get("p4", {}).get("ok")) and doctor_ok
    return {
        "p0": {
            "ok": asset_ok,
            "claim": "Offline docs, scripts, API/GUI/evidence source files are present.",
        },
        "p1": {
            "ok": p1_ok,
            "claim": "Single iPhone real-device control evidence passes P1 and doctor has no fail.",
        },
        "p2": {
            "ok": p2_ok,
            "claim": "Single-device stability evidence passes P2 and doctor has no fail.",
        },
        "p3": {
            "ok": p3_ok,
            "claim": "Four-device group-control evidence passes P3 and doctor has no fail.",
        },
        "p4": {
            "ok": p4_ok,
            "claim": "Ten-device stability evidence passes P4 and doctor has no fail.",
        },
    }


def evaluate_readiness(
    *,
    root: str | Path = ".",
    evidence_jsonl: str | Path | None = None,
    target: str = "p1",
    run_doctor_check: bool = True,
    doctor_report: Optional[dict] = None,
    required_docs: Optional[list[str]] = None,
    required_scripts: Optional[list[str]] = None,
    required_modules: Optional[list[str]] = None,
    gates: Iterable[str] = GATE_LEVELS,
) -> dict:
    """Evaluate current project readiness without redefining real-device success."""
    root_path = Path(root)
    normalized_target = target.lower().strip()
    if normalized_target not in STAGES:
        raise ValueError(f"Unsupported target stage: {target}")

    doc_paths = REQUIRED_DOCS if required_docs is None else required_docs
    script_paths = REQUIRED_SCRIPTS if required_scripts is None else required_scripts
    module_paths = REQUIRED_MODULES if required_modules is None else required_modules
    checks = [
        _path_group_check(root_path, "docs", doc_paths),
        _path_group_check(root_path, "scripts", script_paths),
        _path_group_check(root_path, "modules", module_paths),
    ]
    if doctor_report is None and run_doctor_check:
        doctor_report = run_doctor(root=root_path)
    if doctor_report is None:
        checks.append(_check("doctor", "warn", "Doctor not run; environment readiness is unverified"))
        doctor_ok = False
    else:
        doctor_item = _doctor_check(doctor_report)
        checks.append(doctor_item)
        doctor_ok = doctor_item["status"] != "fail"

    acceptance_items, gate_reports = _acceptance_checks(evidence_jsonl, gates)
    checks.extend(acceptance_items)

    asset_ok = all(
        item["status"] == "pass"
        for item in checks
        if item["name"] in {"docs", "scripts", "modules"}
    )
    stages = _stage_status(asset_ok=asset_ok, doctor_ok=doctor_ok, gate_reports=gate_reports)
    target_ok = bool(stages[normalized_target]["ok"])
    blockers = [item for item in checks if item["status"] == "fail"]
    return {
        "ok": target_ok,
        "target": normalized_target,
        "stage_status": stages,
        "checks": checks,
        "blockers": blockers,
        "claims": {
            "offline_assets_ready": stages["p0"]["ok"],
            "real_ios_control_verified": stages["p1"]["ok"],
            "ios_group_control_verified": stages["p3"]["ok"] or stages["p4"]["ok"],
            "do_not_claim_perfect_ios_control": not stages["p1"]["ok"],
        },
    }


def write_readiness_markdown(report: dict, path: str | Path) -> Path:
    out_path = Path(path)
    lines = [
        "# iMouse Readiness Audit",
        "",
        f"- Target: `{report['target'].upper()}`",
        f"- Result: {'PASS' if report['ok'] else 'FAIL'}",
        f"- Real iOS control verified: `{report['claims']['real_ios_control_verified']}`",
        f"- iOS group control verified: `{report['claims']['ios_group_control_verified']}`",
        "",
        "## Stage Status",
        "",
        "| Stage | Status | Claim |",
        "|---|---|---|",
    ]
    for stage, item in report["stage_status"].items():
        lines.append(f"| {stage.upper()} | {'PASS' if item['ok'] else 'FAIL'} | {item['claim']} |")
    lines.extend(["", "## Checks", "", "| Check | Status | Message |", "|---|---|---|"])
    for item in report["checks"]:
        lines.append(f"| {item['name']} | {item['status']} | {item['message']} |")
    lines.extend(["", "## Blockers", ""])
    if report["blockers"]:
        for item in report["blockers"]:
            lines.append(f"- `{item['name']}`: {item['message']}")
    else:
        lines.append("- None")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Audit iMouse XP prototype readiness")
    parser.add_argument("--root", default=".", help="Workspace root")
    parser.add_argument("--evidence", default="", help="Optional evidence/<run_id>.jsonl to evaluate")
    parser.add_argument("--target", choices=STAGES, default="p1", help="Target readiness stage")
    parser.add_argument("--skip-doctor", action="store_true", help="Do not run doctor checks")
    parser.add_argument("--markdown", default="", help="Optional output Markdown path")
    parser.add_argument("--json", action="store_true", help="Print full JSON report")
    args = parser.parse_args(argv)

    report = evaluate_readiness(
        root=args.root,
        evidence_jsonl=args.evidence or None,
        target=args.target,
        run_doctor_check=not args.skip_doctor,
    )
    if args.markdown:
        out_path = write_readiness_markdown(report, args.markdown)
        print(f"Wrote readiness report: {out_path}")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Readiness {args.target.upper()}: {'PASS' if report['ok'] else 'FAIL'}")
        for stage, item in report["stage_status"].items():
            print(f"- {stage.upper()}: {'PASS' if item['ok'] else 'FAIL'} - {item['claim']}")
        if report["blockers"]:
            print("Blockers:")
            for item in report["blockers"]:
                print(f"- {item['name']}: {item['message']}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
