"""Machine-readable iMouse XP core capability gap audit."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable, Optional

from .acceptance import GATE_LEVELS, evaluate_acceptance
from .readiness import evaluate_readiness
from .validation import ValidationRecorder, make_run_id


FIELD_STATUS_ORDER = {
    "pass": 0,
    "partial": 1,
    "blocked": 2,
    "not_started": 3,
}


@dataclass(frozen=True)
class CapabilitySpec:
    key: str
    domain: str
    priority: str
    xp_signal: str
    current_state: str
    gap: str
    required_evidence: str
    implemented_assets: tuple[str, ...] = ()
    blocks_stage: str = "p1"
    field_check: str = ""
    next_action: str = ""


CAPABILITY_SPECS: tuple[CapabilitySpec, ...] = (
    CapabilitySpec(
        key="kernel_api",
        domain="Kernel/API",
        priority="P0",
        xp_signal="Core service plus HTTP/WebSocket API.",
        current_state="FastAPI service, /api+fun compatibility, WebSocket entry.",
        gap="Windows service hardening, permissions, event callbacks, and performance logs remain weak.",
        required_evidence="API tests plus field evidence that GUI/script actions route through the service.",
        implemented_assets=("imouse/server.py", "imouse/xp_client.py", "docs/xp_api_compat.md"),
        blocks_stage="p1",
        field_check="p0_assets",
        next_action="Keep API/GUI/script paths unified; add event callbacks after P1 closes.",
    ),
    CapabilitySpec(
        key="sdk_helper",
        domain="Python SDK",
        priority="P1",
        xp_signal="imouse-py exposes api/helper/device layers.",
        current_state="XpApiClient covers device, group, calibration, metadata, vision, batch helpers.",
        gap="More helpers, callback semantics, config/user/shortcut compatibility, and error-code mapping are incomplete.",
        required_evidence="SDK helper tests and a field script using the same helpers as the GUI.",
        implemented_assets=("imouse/xp_client.py", "tests/test_xp_client.py"),
        blocks_stage="p2",
        field_check="p0_assets",
        next_action="Add helper coverage only after P1 route/HID/capture are verified.",
    ),
    CapabilitySpec(
        key="device_group",
        domain="Device/Group",
        priority="P2",
        xp_signal="Device list, group, user, config, and LAN visibility behaviors.",
        current_state="Local device registry, per-device state, local JSON group management.",
        gap="Cloud groups, subaccounts, LAN visibility, and operator permissions are not implemented.",
        required_evidence="4/10-device group evidence with per-device result isolation.",
        implemented_assets=("imouse/device_manager.py", "tests/test_xp_api.py"),
        blocks_stage="p3",
        field_check="group_evidence",
        next_action="Use local groups for P3; delay cloud/account work until group evidence passes.",
    ),
    CapabilitySpec(
        key="component_metadata",
        domain="Component Ledger",
        priority="P0",
        xp_signal="XP setup depends on receiver, HID, iPhone, iOS, hub, and cable variables.",
        current_state="GUI metadata row, state/device_profiles.json, route decision evidence.",
        gap="Metadata can be filled incorrectly and does not prove real control.",
        required_evidence="Component metadata event for every target device with no placeholders.",
        implemented_assets=("imouse/route_decision.py", "docs/hardware_test_bench_checklist.md"),
        blocks_stage="p1",
        field_check="component_traceability",
        next_action="Record Metadata per device before screenshot/click assertions.",
    ),
    CapabilitySpec(
        key="receiver_capture",
        domain="Receiver/Capture",
        priority="P0",
        xp_signal="AirPlay/wired projection, single service, hardware acceleration, quick reconnect.",
        current_state="UxPlay/X11 prototype entry plus screenshot API and static GUI preview.",
        gap="Windows receiver, wired projection, hardware decoding, window binding, fps and reconnect are not verified.",
        required_evidence="Doctor clean or documented substitute plus non-black screenshot samples.",
        implemented_assets=(
            "imouse/airplay.py",
            "imouse/capture.py",
            "imouse/receiver_provider.py",
            "docs/receiver_capture_selection.md",
        ),
        blocks_stage="p1",
        field_check="screenshot_quality",
        next_action="Choose UxPlay/Windows/wired route, record version/path, then capture real frames.",
    ),
    CapabilitySpec(
        key="hid_control",
        domain="USB/HID",
        priority="P0",
        xp_signal="Dedicated iMouse virtual keyboard/mouse hardware and firmware.",
        current_state="CH9329 serial HID frame prototype and GUI bind/click/swipe/type entries.",
        gap="XP hardware protocol, 4.4 firmware, auto binding, release behavior, and iOS pointer response are unverified.",
        required_evidence="Real iPhone manual observations for click/swipe/type with HID identity.",
        implemented_assets=("imouse/hardware.py", "docs/hid_hardware_protocol_benchmark.md"),
        blocks_stage="p1",
        field_check="manual_observation",
        next_action="Plug one HID route, bind dev_1, run 10 click/swipe/type samples, record Manual.",
    ),
    CapabilitySpec(
        key="calibration",
        domain="Coordinate Calibration",
        priority="P0",
        xp_signal="Adaptive resolution, device configuration, and firmware-aware binding.",
        current_state="Local calibration profile and GUI active/target mapping.",
        gap="Safe area, landscape, Dynamic Island, high resolution, and auto detection need field matrices.",
        required_evidence="Five-point calibration evidence and manual pixel-error notes.",
        implemented_assets=("imouse/calibration.py", "docs/coordinate_calibration.md"),
        blocks_stage="p1",
        field_check="manual_observation",
        next_action="Run five-point calibration before declaring click precision.",
    ),
    CapabilitySpec(
        key="mouse_keyboard",
        domain="Mouse/Keyboard",
        priority="P1",
        xp_signal="Mouse modes, shortcuts, keyboard input, combo keys, Emoji and multilingual input.",
        current_state="Click, swipe, type, key, combo prototype via API/GUI/script.",
        gap="Chinese input, Emoji, focus handling, special mouse modes, and firmware timing are unverified.",
        required_evidence="Input matrix evidence across click, swipe, text, key/combo.",
        implemented_assets=("imouse/server.py", "imouse/script_runner.py"),
        blocks_stage="p2",
        field_check="manual_observation",
        next_action="Keep P1 to safe English/numeric input; expand matrix after receiver/HID are stable.",
    ),
    CapabilitySpec(
        key="vision_color",
        domain="Vision/Image/Color",
        priority="P1",
        xp_signal="Screenshot, OpenCV find image, color, multi-color, OCR and text search.",
        current_state="Find image/color/multi-color, template crop quality, OCR/text compatibility layer.",
        gap="Template asset library, transparent images, threshold policy, region discipline, and replay still need field assets.",
        required_evidence="Template records, thresholds, regions, source screenshots, and failure replay artifacts.",
        implemented_assets=("imouse/vision.py", "docs/validation_evidence.md"),
        blocks_stage="p2",
        field_check="screenshot_quality",
        next_action="Create template naming and failure replay assets from real screenshots.",
    ),
    CapabilitySpec(
        key="ocr",
        domain="OCR",
        priority="P1",
        xp_signal="Baidu PaddleOCR OCR/find-text support.",
        current_state="PaddleOCR 2.x/3.x result parsing with project-local cache defaults.",
        gap="Real model download, cropped OCR performance, language samples, and false-positive handling are unverified.",
        required_evidence="Chinese, English, numeric OCR samples from real screenshots.",
        implemented_assets=("imouse/vision.py", "tests/test_vision.py"),
        blocks_stage="p2",
        field_check="screenshot_quality",
        next_action="Run real cropped OCR only after screenshot route is stable.",
    ),
    CapabilitySpec(
        key="script_runtime",
        domain="Script Runtime",
        priority="P2",
        xp_signal="Python/API automation and batch flows.",
        current_state="JSON runner supports call/wait/repeat/metrics/record/vision/batch plus failure screenshots.",
        gap="Variables, conditionals, business assertions, repeated frame detection, and group-loop watchdogs remain incomplete.",
        required_evidence="Long-running scenario evidence with metrics and operator observations.",
        implemented_assets=("imouse/script_runner.py", "docs/script_runner.md"),
        blocks_stage="p3",
        field_check="metrics",
        next_action="Keep scripts deterministic for P1/P3; add variables/conditionals after core field proof.",
    ),
    CapabilitySpec(
        key="gui_console",
        domain="GUI Console",
        priority="P2",
        xp_signal="Console, multi-window view, debug tools, logs and workflow controls.",
        current_state="Tkinter GUI for API control, SOP reports, Live Probe, Dashboard and Pack.",
        gap="Realtime multi-device video grid, hotkeys, log filters, receiver status columns, and failure replay UI are missing.",
        required_evidence="GUI pilot record showing operator can locate failures within 30 seconds.",
        implemented_assets=("imouse/gui.py", "docs/gui_prototype.md", "docs/gui_live_probe.md"),
        blocks_stage="p3",
        field_check="group_evidence",
        next_action="Add realtime grid only after receiver provider and screenshot window binding are selected.",
    ),
    CapabilitySpec(
        key="observability",
        domain="Observability",
        priority="P1",
        xp_signal="Debug tools, request/response logs, receiver diagnostics and stability traces.",
        current_state="Doctor, evidence JSONL, Review, readiness, acceptance, metrics snapshots.",
        gap="Receiver logs, per-device log filters, fps/latency, reconnect timing, and resource trend UI are incomplete.",
        required_evidence="Doctor, review, metrics, failure category and artifact paths for every failed run.",
        implemented_assets=("imouse/doctor.py", "imouse/evidence_report.py", "imouse/metrics.py"),
        blocks_stage="p2",
        field_check="metrics",
        next_action="Attach receiver/HID logs to evidence during P1/P2 failures.",
    ),
    CapabilitySpec(
        key="commercial_ops",
        domain="Commercial/Ops",
        priority="P3",
        xp_signal="Cloud grouping, subaccounts, LAN visibility, auto update, service operations.",
        current_state="Not implemented beyond local JSON and docs.",
        gap="Accounts, permissions, cloud sync, LAN visibility and update strategy are out of P1 scope.",
        required_evidence="Post-P3 product operations design and pilot records.",
        implemented_assets=("docs/xp_core_backlog.md",),
        blocks_stage="p4",
        field_check="post_p3",
        next_action="Do not build this until P3/P4 field evidence proves core control.",
    ),
)


def build_xp_gap_audit(
    *,
    target_stage: str = "p1",
    run_id: str = "",
    root: str | Path = ".",
    evidence_jsonl: str | Path | None = None,
    readiness_report: Optional[dict] = None,
    doctor_report: Optional[dict] = None,
    run_doctor_check: bool = False,
) -> dict:
    """Build a structured XP parity gap report without claiming field success."""
    normalized_stage = target_stage.lower().strip() or "p1"
    if normalized_stage not in {"p1", "p2", "p3", "p4"}:
        raise ValueError(f"Unsupported target stage: {target_stage}")

    safe_run_id = run_id.strip() or make_run_id(f"{normalized_stage}_gap")
    root_path = Path(root)
    evidence_path = Path(evidence_jsonl) if evidence_jsonl else ValidationRecorder(safe_run_id).path
    evidence_exists = evidence_path.exists()
    acceptance_reports = _acceptance_reports(evidence_path if evidence_exists else None)

    if readiness_report is None:
        readiness_report = evaluate_readiness(
            root=root_path,
            evidence_jsonl=evidence_path if evidence_exists else None,
            target=normalized_stage,
            run_doctor_check=run_doctor_check and doctor_report is None,
            doctor_report=doctor_report,
        )
    rows = [
        _capability_row(
            spec,
            root=root_path,
            target_stage=normalized_stage,
            readiness_report=readiness_report,
            acceptance_reports=acceptance_reports,
            doctor_report=doctor_report,
            evidence_exists=evidence_exists,
        )
        for spec in CAPABILITY_SPECS
    ]
    counts = _status_counts(rows)
    blocking_statuses = {"blocked", "not_started"}
    p0_blockers = [row for row in rows if row["priority"] == "P0" and row["status"] in blocking_statuses]
    target_blockers = [
        row for row in rows
        if _stage_reaches(normalized_stage, row["blocks_stage"]) and row["status"] in blocking_statuses
    ]
    readiness_claims = readiness_report.get("claims", {}) if isinstance(readiness_report, dict) else {}
    return {
        "run_id": safe_run_id,
        "target_stage": normalized_stage,
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "evidence_jsonl": str(evidence_path),
        "summary": {
            "total": len(rows),
            "counts": counts,
            "p0_blockers": len(p0_blockers),
            "target_blockers": len(target_blockers),
            "real_ios_control_verified": bool(readiness_claims.get("real_ios_control_verified")),
            "ios_group_control_verified": bool(readiness_claims.get("ios_group_control_verified")),
        },
        "rows": rows,
        "blockers": target_blockers,
        "claims": {
            "real_ios_control_verified": bool(readiness_claims.get("real_ios_control_verified")),
            "do_not_claim_perfect_ios_control": not bool(readiness_claims.get("real_ios_control_verified")),
            "audit_is_evidence": False,
        },
    }


def xp_gap_audit_brief(audit: dict) -> str:
    summary = audit.get("summary", {})
    counts = summary.get("counts", {})
    return (
        f"XP gap audit {str(audit.get('target_stage', 'p1')).upper()}: "
        f"pass={counts.get('pass', 0)}, partial={counts.get('partial', 0)}, "
        f"blocked={counts.get('blocked', 0)}, not_started={counts.get('not_started', 0)}; "
        f"target_blockers={summary.get('target_blockers', 0)}"
    )


def write_xp_gap_audit_markdown(audit: dict, path: str | Path) -> Path:
    out_path = Path(path)
    summary = audit.get("summary", {})
    lines = [
        f"# iMouse XP Core Gap Audit {str(audit.get('target_stage', 'p1')).upper()}",
        "",
        f"- Generated: `{audit.get('generated_at', '')}`",
        f"- Run ID: `{audit.get('run_id', '')}`",
        f"- Evidence JSONL: `{audit.get('evidence_jsonl', '')}`",
        f"- Real iOS control verified: `{summary.get('real_ios_control_verified', False)}`",
        f"- iOS group control verified: `{summary.get('ios_group_control_verified', False)}`",
        "- This audit is a product gap map. It does not write evidence and does not prove real iPhone response.",
        "",
        "## Summary",
        "",
        f"- Total domains: `{summary.get('total', 0)}`",
        f"- P0 blockers: `{summary.get('p0_blockers', 0)}`",
        f"- Target blockers: `{summary.get('target_blockers', 0)}`",
        "",
        "## Capability Matrix",
        "",
        "| Domain | Priority | Status | Field gate | Current state | Gap | Required evidence | Next action |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in audit.get("rows", []):
        values = [
            row.get("domain", ""),
            row.get("priority", ""),
            row.get("status", ""),
            row.get("field_gate", ""),
            row.get("current_state", ""),
            row.get("gap", ""),
            row.get("required_evidence", ""),
            row.get("next_action", ""),
        ]
        escaped = [str(value).replace("|", "\\|") for value in values]
        lines.append(
            f"| {escaped[0]} | {escaped[1]} | `{escaped[2]}` | {escaped[3]} | "
            f"{escaped[4]} | {escaped[5]} | {escaped[6]} | {escaped[7]} |"
        )
    lines.extend([
        "",
        "## Target Blockers",
        "",
    ])
    blockers = audit.get("blockers", [])
    if blockers:
        for row in blockers:
            lines.append(
                f"- `{row.get('key', '')}` ({row.get('priority', '')}, {row.get('status', '')}): "
                f"{row.get('blocker_reason', row.get('next_action', ''))}"
            )
    else:
        lines.append("- None from this audit. Still verify Acceptance and Readiness before promotion.")
    lines.extend([
        "",
        "## Promotion Rule",
        "",
        "Do not use this audit as proof of XP parity. A domain is field-ready only when the listed evidence exists in JSONL/artifacts and Acceptance plus Readiness pass for the target stage.",
        "",
    ])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def _capability_row(
    spec: CapabilitySpec,
    *,
    root: Path,
    target_stage: str,
    readiness_report: dict,
    acceptance_reports: dict[str, dict],
    doctor_report: dict | None,
    evidence_exists: bool,
) -> dict:
    assets_present = [asset for asset in spec.implemented_assets if (root / asset).exists()]
    asset_status = len(assets_present) == len(spec.implemented_assets)
    status, reason = _field_status(
        spec,
        target_stage=target_stage,
        readiness_report=readiness_report,
        acceptance_reports=acceptance_reports,
        doctor_report=doctor_report,
        evidence_exists=evidence_exists,
        asset_status=asset_status,
    )
    return {
        "key": spec.key,
        "domain": spec.domain,
        "priority": spec.priority,
        "status": status,
        "xp_signal": spec.xp_signal,
        "current_state": spec.current_state,
        "gap": spec.gap,
        "required_evidence": spec.required_evidence,
        "implemented_assets": list(spec.implemented_assets),
        "assets_present": assets_present,
        "blocks_stage": spec.blocks_stage,
        "field_gate": spec.field_check,
        "blocker_reason": reason,
        "next_action": spec.next_action,
    }


def _field_status(
    spec: CapabilitySpec,
    *,
    target_stage: str,
    readiness_report: dict,
    acceptance_reports: dict[str, dict],
    doctor_report: dict | None,
    evidence_exists: bool,
    asset_status: bool,
) -> tuple[str, str]:
    if not asset_status:
        return "blocked", "Required source/doc assets are missing."

    if spec.field_check == "p0_assets":
        p0 = readiness_report.get("stage_status", {}).get("p0", {})
        return ("partial" if p0.get("ok") else "blocked", "P0 assets present; field parity still needs evidence.")

    if spec.field_check == "component_traceability":
        return _acceptance_check_status(acceptance_reports, "p1", "component_traceability")

    if spec.field_check == "screenshot_quality":
        return _acceptance_check_status(acceptance_reports, "p1", "screenshot_quality")

    if spec.field_check == "manual_observation":
        return _acceptance_check_status(acceptance_reports, "p1", "manual_observation")

    if spec.field_check == "metrics":
        gate = "p2" if target_stage in {"p1", "p2"} else target_stage
        return _acceptance_check_status(acceptance_reports, gate, "metrics")

    if spec.field_check == "group_evidence":
        gate = "p3" if target_stage in {"p1", "p2", "p3"} else "p4"
        report = acceptance_reports.get(gate)
        if report and report.get("ok"):
            return "pass", f"{gate.upper()} group evidence passed."
        if evidence_exists:
            return "blocked", f"{gate.upper()} group evidence is incomplete."
        return "not_started", f"{gate.upper()} group evidence has not been recorded."

    if spec.field_check == "post_p3":
        p3_ok = bool(readiness_report.get("stage_status", {}).get("p3", {}).get("ok"))
        if p3_ok:
            return "partial", "P3 evidence exists; commercial operations still need product design."
        return "not_started", "Commercial operations should wait until P3 evidence exists."

    if not evidence_exists:
        return "partial", "Offline assets exist, but field evidence is missing."
    return "partial", "Evidence exists, but this domain has no direct field gate yet."


def _acceptance_check_status(
    acceptance_reports: dict[str, dict],
    gate: str,
    check_name: str,
) -> tuple[str, str]:
    report = acceptance_reports.get(gate)
    if not report:
        return "not_started", f"{gate.upper()} acceptance has no evidence yet."
    for item in report.get("checks", []):
        if item.get("name") != check_name:
            continue
        if item.get("status") == "pass":
            return "pass", str(item.get("message", "pass"))
        return "blocked", str(item.get("message", f"{check_name} failed"))
    return "blocked", f"{gate.upper()} acceptance did not include {check_name}."


def _acceptance_reports(evidence_jsonl: str | Path | None) -> dict[str, dict]:
    if not evidence_jsonl:
        return {}
    path = Path(evidence_jsonl)
    if not path.exists():
        return {}
    reports = {}
    for gate in GATE_LEVELS:
        try:
            reports[gate] = evaluate_acceptance(path, gate=gate)
        except Exception as exc:
            reports[gate] = {
                "gate": gate,
                "ok": False,
                "checks": [{"name": "acceptance_error", "status": "fail", "message": str(exc)}],
            }
    return reports


def _status_counts(rows: Iterable[dict]) -> dict[str, int]:
    counts = {key: 0 for key in FIELD_STATUS_ORDER}
    for row in rows:
        status = str(row.get("status", "not_started"))
        counts[status] = counts.get(status, 0) + 1
    return counts


def _stage_reaches(target_stage: str, blocks_stage: str) -> bool:
    order = {"p1": 1, "p2": 2, "p3": 3, "p4": 4}
    return order.get(target_stage, 1) >= order.get(blocks_stage, 1)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Audit iMouse XP core capability gaps.")
    parser.add_argument("--target", default="p1", choices=("p1", "p2", "p3", "p4"))
    parser.add_argument("--run-id", default="")
    parser.add_argument("--evidence", default="")
    parser.add_argument("--markdown", default="")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--run-doctor", action="store_true")
    args = parser.parse_args(argv)

    audit = build_xp_gap_audit(
        target_stage=args.target,
        run_id=args.run_id,
        evidence_jsonl=args.evidence or None,
        run_doctor_check=args.run_doctor,
    )
    if args.markdown:
        path = write_xp_gap_audit_markdown(audit, args.markdown)
        print(f"Wrote XP gap audit: {path}")
    if args.json or not args.markdown:
        print(json.dumps(audit, ensure_ascii=False, indent=2))
    else:
        print(xp_gap_audit_brief(audit))
    return 0 if not audit.get("summary", {}).get("target_blockers") else 1


if __name__ == "__main__":
    raise SystemExit(main())
