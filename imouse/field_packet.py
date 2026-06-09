"""Generate step-by-step field execution packets for iMouse validation."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path
from typing import Optional

from .doctor import run_doctor
from .readiness import STAGES, evaluate_readiness
from .validation import make_run_id


STAGE_SCRIPTS = {
    "p1": ["scripts/p1_single_device_control_probe.json", "scripts/p1_receiver_capture_probe.json"],
    "p2": ["scripts/p2_single_device_stability.json"],
    "p3": ["scripts/pilot_4_group_smoke.json", "scripts/p3_pilot4_30min_watchdog.json"],
    "p4": ["scripts/stable_10_group_watchdog.json"],
}

STAGE_DEVICE_COUNTS = {
    "p1": 1,
    "p2": 1,
    "p3": 4,
    "p4": 10,
}

STAGE_GOALS = {
    "p1": "Single iPhone: prove screen capture, calibration, click, swipe, type, and evidence.",
    "p2": "Single iPhone stability: prove repeatability over a timed run.",
    "p3": "Four iPhones: prove group dispatch, per-device traceability, and failure isolation.",
    "p4": "Ten iPhones: prove long-run resource and field stability.",
}


def _default_devices(stage: str) -> list[str]:
    count = STAGE_DEVICE_COUNTS[stage]
    return [f"dev_{idx}" for idx in range(1, count + 1)]


def _parse_devices(value: str, stage: str) -> list[str]:
    if not value.strip():
        return _default_devices(stage)
    devices = []
    seen = set()
    for item in value.split(","):
        text = item.strip()
        if not text or text in seen:
            continue
        seen.add(text)
        devices.append(text)
    return devices or _default_devices(stage)


def _evidence_path(run_id: str) -> str:
    return f"evidence/{run_id}.jsonl"


def _route_decision_path(run_id: str) -> str:
    return f"evidence/{run_id}_route_decision.json"


def _doctor_fail_names(report: dict) -> list[str]:
    return [
        str(item.get("name", ""))
        for item in report.get("checks", [])
        if item.get("status") == "fail"
    ]


def _blocker_names(report: dict) -> list[str]:
    return [str(item.get("name", "")) for item in report.get("blockers", [])]


def build_field_packet(
    *,
    stage: str = "p1",
    run_id: str = "",
    devices: Optional[list[str]] = None,
    root: str | Path = ".",
    evidence_jsonl: str | Path | None = None,
    doctor_report: Optional[dict] = None,
    run_doctor_check: bool = True,
) -> dict:
    """Build a field test packet model without claiming field success."""
    normalized_stage = stage.lower().strip()
    if normalized_stage not in STAGES or normalized_stage == "p0":
        raise ValueError(f"Unsupported field stage: {stage}")
    safe_run_id = run_id.strip() or make_run_id(normalized_stage)
    device_ids = devices or _default_devices(normalized_stage)
    evidence_path = str(evidence_jsonl or _evidence_path(safe_run_id))

    if doctor_report is None and run_doctor_check:
        doctor_report = run_doctor(root=root)

    readiness = evaluate_readiness(
        root=root,
        evidence_jsonl=evidence_path if Path(evidence_path).exists() else None,
        target=normalized_stage,
        run_doctor_check=False,
        doctor_report=doctor_report,
    )
    return {
        "stage": normalized_stage,
        "run_id": safe_run_id,
        "devices": device_ids,
        "device_count": len(device_ids),
        "goal": STAGE_GOALS[normalized_stage],
        "scripts": STAGE_SCRIPTS[normalized_stage],
        "evidence_jsonl": evidence_path,
        "route_decision_json": _route_decision_path(safe_run_id),
        "doctor": doctor_report or {},
        "readiness": readiness,
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }


def _metadata_table(devices: list[str]) -> list[str]:
    lines = [
        "| Device | iPhone/iOS | Receiver/Capture | HID/Serial | Hub/Cable | Evidence note |",
        "|---|---|---|---|---|---|",
    ]
    for device_id in devices:
        lines.append(
            f"| {device_id} | model= / ios= | provider= / method= | hid= / serial= | hub= / cable= |  |"
        )
    return lines


def _profile_curl_example(device_id: str) -> str:
    return (
        'curl.exe -X POST http://127.0.0.1:9911/api -H "Content-Type: application/json" '
        f'-d "{{\\"fun\\":\\"/metadata/set\\",\\"data\\":{{\\"id\\":\\"{device_id}\\",'
        '\\"metadata\\":{\\"receiver_provider\\":\\"EDIT_REAL_PROVIDER\\",'
        '\\"capture_method\\":\\"EDIT_REAL_CAPTURE\\",'
        '\\"hid_provider\\":\\"EDIT_REAL_HID\\",'
        '\\"hid_id\\":\\"EDIT_REAL_HID_ID\\",\\"serial_port\\":\\"COM_EDIT_REAL\\",'
        '\\"iphone_id\\":\\"EDIT_REAL_IPHONE\\",\\"ios_version\\":\\"EDIT_REAL_IOS\\"}}}}"'
    )


def write_field_packet_markdown(packet: dict, path: str | Path) -> Path:
    out_path = Path(path)
    stage = packet["stage"]
    run_id = packet["run_id"]
    devices = list(packet["devices"])
    doctor = packet.get("doctor", {})
    readiness = packet.get("readiness", {})
    doctor_overall = doctor.get("overall", "not_run")
    doctor_fails = _doctor_fail_names(doctor)
    blockers = _blocker_names(readiness)
    first_device = devices[0] if devices else "dev_1"

    lines = [
        f"# iMouse Field Execution Packet {stage.upper()}",
        "",
        f"- Generated: `{packet['generated_at']}`",
        f"- Run ID: `{run_id}`",
        f"- Goal: {packet['goal']}",
        f"- Devices: `{', '.join(devices)}`",
        f"- Route Decision JSON: `{packet.get('route_decision_json', _route_decision_path(run_id))}`",
        f"- Evidence JSONL: `{packet['evidence_jsonl']}`",
        f"- Doctor: `{doctor_overall}`",
        f"- Readiness: `{'PASS' if readiness.get('ok') else 'FAIL'}`",
        "",
        "This packet is an execution checklist, not proof of real iOS control. Only evidence plus acceptance/readiness PASS can support a field claim.",
        "",
        "## Current Blockers",
        "",
    ]
    if doctor_fails:
        for name in doctor_fails:
            lines.append(f"- Doctor fail: `{name}`")
    if blockers:
        for name in blockers:
            lines.append(f"- Readiness blocker: `{name}`")
    if not doctor_fails and not blockers:
        lines.append("- None from generated checks. Still verify real iPhone behavior manually.")

    lines.extend([
        "",
        "## Step 0 - XP Parity Context",
        "",
        "Before running hardware, open these and mark the exact XP capability row(s) this run is trying to prove:",
        "",
        "- `docs/mainstream_route_decision.md`",
        "- `docs/xp_parity_matrix.md`",
        "- `docs/imouse_xp_research.md`",
        "- `docs/ios_group_control_sop.md`",
        "- `docs/field_test_matrix.md`",
        "- `docs/operator_worksheet.md`",
        "- `docs/xp_gap_audit.md`",
        "",
        "First choose one receiver route and one HID route. For each selected XP capability row, write down the expected evidence event, device metadata, screenshot artifact, and manual observation that will prove or disprove it.",
        "",
        "Create, edit, then validate this route decision before real hardware actions:",
        "",
        "```powershell",
        f".\\.venv\\Scripts\\python -m imouse.route_decision init --run-id {run_id} --devices {','.join(devices)} --output evidence\\{run_id}_route_decision.json",
        f".\\.venv\\Scripts\\python -m imouse.route_decision validate evidence\\{run_id}_route_decision.json --require-ready --markdown evidence\\{run_id}_route_decision.md --record-evidence evidence\\{run_id}.jsonl",
        f".\\.venv\\Scripts\\python -m imouse.xp_gap_audit --target {stage} --run-id {run_id} --markdown evidence\\{run_id}_{stage}_xp_gap_audit.md",
        "```",
        "",
        "Stop if route decision validation fails. If failure was recorded into evidence, treat this run_id as blocked and start a fresh run_id after fixing blockers. A passing route decision only records component traceability; it does not replace screenshot quality or manual iPhone observations. XP Gap Audit is only a research gap map; it does not write evidence.",
        "",
        "## Step 1 - Local Health",
        "",
        "Run these before touching hardware:",
        "",
        "```powershell",
        "cd D:\\codex-projects\\imouse-clone",
        ".\\.venv\\Scripts\\python -m unittest discover -s tests -v",
        ".\\.venv\\Scripts\\python -m compileall -q imouse tests",
        f".\\.venv\\Scripts\\python -m imouse.doctor --route-decision evidence\\{run_id}_route_decision.json --markdown evidence\\{run_id}_doctor.md",
        "```",
        "",
        "Stop if unit tests or compileall fail. Stop if doctor has an unexplained fail.",
        "",
        "## Step 2 - Component Ledger",
        "",
        "Fill this before running control tests:",
        "",
        *_metadata_table(devices),
        "",
        "Save the same metadata through GUI `Record Metadata` or this API example:",
        "",
        "```powershell",
        _profile_curl_example(first_device),
        "```",
        "",
        "Do not leave `EDIT_REAL_*`, `TODO`, or shared HID/iPhone identities in field evidence.",
        "",
        "## Step 3 - GUI Smoke Path",
        "",
        "1. Start `python -m imouse.gui`.",
        f"2. Set Evidence run id to `{run_id}` and keep `Record` enabled.",
        "3. Start local server, press `Doctor`, press `Ping`.",
        f"4. Generate an operator worksheet: `python -m imouse.operator_worksheet --stage {stage} --run-id {run_id} --devices {','.join(devices)}`.",
        "5. Register each device id, scan serial ports, bind the real HID port.",
        "6. Start AirPlay or the chosen receiver route, then start capture and screenshot.",
        "7. Use screenshot preview to pick safe coordinates, save calibration, and record five-point error.",
        "8. Run click, swipe, type, find image/color/OCR/text; record every real iPhone observation in `Manual`.",
        "",
        "## Step 4 - Script Path",
        "",
        "Dry-run first:",
        "",
        "```powershell",
    ])
    for script in packet["scripts"]:
        lines.append(f".\\.venv\\Scripts\\python -m imouse.script_runner {script} --dry-run --run-id {run_id}")
    lines.extend([
        "```",
        "",
        "Before real run, edit device ids, coordinates, templates, and metadata placeholders to match the field bench.",
        "",
        "Real run:",
        "",
        "```powershell",
    ])
    for script in packet["scripts"]:
        lines.append(f".\\.venv\\Scripts\\python -m imouse.script_runner {script} --run-id {run_id}")
    lines.extend([
        "```",
        "",
        "## Step 5 - Acceptance",
        "",
        "```powershell",
        f".\\.venv\\Scripts\\python -m imouse.evidence_report evidence\\{run_id}.jsonl --markdown evidence\\{run_id}_review.md",
        f".\\.venv\\Scripts\\python -m imouse.acceptance evidence\\{run_id}.jsonl --gate {stage} --markdown evidence\\{run_id}_acceptance.md",
        f".\\.venv\\Scripts\\python -m imouse.readiness --target {stage} --evidence evidence\\{run_id}.jsonl --markdown evidence\\{run_id}_readiness.md",
        "```",
        "",
        "Promotion rule: do not move to the next stage unless acceptance and readiness both PASS and the field operator observed real iPhone behavior.",
        "",
        "## Failure Routing",
        "",
        "| Category | Field action | Evidence required |",
        "|---|---|---|",
        "| airplay_discovery | Check same VLAN, mDNS/Bonjour, firewall, receiver name | receiver logs, network notes |",
        "| airplay_stream | Check black/white/garbled frames, lock screen, codec route | screenshot artifact, receiver version |",
        "| capture | Check window/display/capture-card route and dimensions | screenshot_quality details |",
        "| calibration | Re-run active/target/safe-area mapping | five-point error records |",
        "| hid | Check serial port, firmware, OTG, release state | manual fail, serial/HID id |",
        "| vision_template | Replace low-texture or stale template | template image and threshold |",
        "| group_dispatch | Verify per-device results and single-device isolation | batch result per device |",
        "| performance | Record CPU/memory/network and receiver resource use | metrics samples |",
        "",
    ])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate an iMouse field execution packet")
    parser.add_argument("--stage", choices=("p1", "p2", "p3", "p4"), default="p1")
    parser.add_argument("--run-id", default="", help="Field run id; generated if omitted")
    parser.add_argument("--devices", default="", help="Comma-separated device ids; defaults by stage")
    parser.add_argument("--root", default=".", help="Workspace root")
    parser.add_argument("--evidence", default="", help="Existing evidence JSONL path to audit in the packet")
    parser.add_argument("--skip-doctor", action="store_true", help="Generate packet without running doctor")
    parser.add_argument("--output", default="", help="Markdown output path")
    args = parser.parse_args(argv)

    devices = _parse_devices(args.devices, args.stage)
    run_id = args.run_id.strip() or make_run_id(args.stage)
    output = args.output or f"evidence/{run_id}_field_packet.md"
    packet = build_field_packet(
        stage=args.stage,
        run_id=run_id,
        devices=devices,
        root=args.root,
        evidence_jsonl=args.evidence or None,
        run_doctor_check=not args.skip_doctor,
    )
    out_path = write_field_packet_markdown(packet, output)
    print(f"Wrote field execution packet: {out_path}")
    print(f"Stage {packet['stage'].upper()} readiness: {'PASS' if packet['readiness'].get('ok') else 'FAIL'}")
    if packet["readiness"].get("blockers"):
        print("Blockers:")
        for item in packet["readiness"]["blockers"]:
            print(f"- {item.get('name')}: {item.get('message')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
