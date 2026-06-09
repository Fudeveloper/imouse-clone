"""Generate operator worksheets for iMouse field validation."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path
from typing import Optional

from .field_packet import STAGE_DEVICE_COUNTS, STAGE_GOALS, STAGE_SCRIPTS
from .readiness import STAGES
from .validation import make_run_id


FAILURE_TAXONOMY = (
    ("airplay_discovery", "Receiver not visible, mDNS/Bonjour, same VLAN, firewall, name conflict."),
    ("airplay_stream", "Mirror connects but stream is black, white, garbled, delayed, or disconnected."),
    ("capture", "Code cannot capture the real frame, wrong window, wrong dimensions, or stale frame."),
    ("calibration", "Coordinate mapping, active area, orientation, safe area, or point drift."),
    ("hid_discovery", "HID serial/identity cannot be found after plug/unplug."),
    ("hid_bind", "HID port is visible but cannot bind or stays occupied."),
    ("hid_click", "Click has no response, wrong point, or press is not released."),
    ("hid_swipe", "Swipe direction/path/release is wrong."),
    ("hid_keyboard", "Keyboard focus, text, shortcut, language, or IME fails."),
    ("vision_template", "Template too plain, stale, wrong threshold, wrong region, or false positive."),
    ("vision_color", "RGB/tolerance/region/brightness mismatch."),
    ("ocr", "OCR import/cache/model/region/language result fails."),
    ("group_dispatch", "Batch command lacks per-device result or one device blocks the group."),
    ("performance", "CPU, memory, disk, network, receiver, or GUI stability problem."),
    ("business_state", "Business page changed, login, popup, risk control, or unexpected app state."),
)

STAGE_OPERATOR_STEPS = {
    "p1": (
        ("Route decision", "Validate real receiver/HID/iPhone/bench metadata and clear open blockers."),
        ("Doctor", "Run doctor and stop on unexplained fail."),
        ("Register", "Register/select dev_1 in GUI and keep Record enabled."),
        ("Metadata", "Record component metadata for dev_1."),
        ("HID bind", "Scan, plug/unplug, bind the real HID, and record serial/Hub/cable."),
        ("Receiver", "Start receiver/AirPlay/capture and record provider/version/path."),
        ("Screenshot", "Capture non-black, non-white, correct-device screenshot."),
        ("Calibration", "Save calibration and record five-point error observations."),
        ("Click", "Run 10 safe points, 10 repeats each, and record real iPhone response."),
        ("Swipe", "Run up/down/left/right swipe probes and record response."),
        ("Type", "Type English, numbers, and symbols in a safe input field."),
        ("Vision", "Save textured template, find image/color, OCR/find text."),
        ("Script", "Dry-run then real-run P1 scripts with edited real coordinates and metadata."),
        ("Acceptance", "Run Acceptance, Gap, Readiness; only PASS supports promotion."),
    ),
    "p2": (
        ("P1 proof", "Attach the previous P1 PASS evidence and readiness report."),
        ("Stability route", "Keep the same iPhone/HID/receiver unless the change is recorded."),
        ("Metrics", "Record system metrics before, during, and after the 30-minute run."),
        ("Screenshot loop", "Collect repeated screenshot quality samples."),
        ("Input loop", "Repeat click/swipe/type and record drift or release failures."),
        ("Recovery", "Record every disconnect/reconnect and operator decision."),
        ("Acceptance", "Run P2 acceptance/readiness and document remaining blockers."),
    ),
    "p3": (
        ("P1/P2 proof", "Attach single-device PASS evidence before expanding."),
        ("Device ledger", "Record four complete device/component ledgers."),
        ("Groups", "Save/load pilot_4 group and verify membership."),
        ("Group click", "Run group click with per-device observation."),
        ("Group swipe", "Run group swipe with per-device observation."),
        ("Group type", "Run group type with per-device observation."),
        ("Isolation", "Force one device failure and confirm other devices still return results."),
        ("Watchdog", "Run the 30-minute pilot watchdog and record metrics."),
        ("Acceptance", "Run P3 acceptance/readiness and document failed device ids."),
    ),
    "p4": (
        ("P3 proof", "Attach four-device PASS evidence before expanding."),
        ("Ten ledgers", "Record complete ledgers for ten devices."),
        ("Hub/network map", "Record Hub ports, power, cables, AP/VLAN, and receiver resources."),
        ("Stable group", "Save/load stable_10 group and verify membership."),
        ("Watchdog", "Run two-hour watchdog with 30-minute observations."),
        ("Recovery", "Record disconnect, reconnect, stuck HID, and device isolation events."),
        ("Acceptance", "Run P4 acceptance/readiness and list top three blockers."),
    ),
}


def _default_devices(stage: str) -> list[str]:
    return [f"dev_{idx}" for idx in range(1, STAGE_DEVICE_COUNTS[stage] + 1)]


def parse_devices(value: str, stage: str) -> list[str]:
    """Parse comma-separated device ids, falling back to stage defaults."""
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


def build_operator_worksheet(*, stage: str = "p1", run_id: str = "", devices: Optional[list[str]] = None) -> dict:
    """Build an operator worksheet model without reading or writing evidence."""
    normalized_stage = stage.lower().strip()
    if normalized_stage not in STAGES or normalized_stage == "p0":
        raise ValueError(f"Unsupported operator worksheet stage: {stage}")
    safe_run_id = run_id.strip() or make_run_id(normalized_stage)
    device_ids = devices or _default_devices(normalized_stage)
    return {
        "stage": normalized_stage,
        "run_id": safe_run_id,
        "devices": device_ids,
        "device_count": len(device_ids),
        "goal": STAGE_GOALS[normalized_stage],
        "scripts": STAGE_SCRIPTS[normalized_stage],
        "steps": [
            {"name": name, "operator_action": action}
            for name, action in STAGE_OPERATOR_STEPS[normalized_stage]
        ],
        "failure_taxonomy": [
            {"category": category, "meaning": meaning}
            for category, meaning in FAILURE_TAXONOMY
        ],
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }


def _device_ledger_lines(devices: list[str]) -> list[str]:
    lines = [
        "| Device | iPhone model/iOS | Receiver provider/version/path | Capture method/window | HID provider/id/serial | Hub/cable/port | Operator note |",
        "|---|---|---|---|---|---|---|",
    ]
    for device_id in devices:
        lines.append(f"| {device_id} |  |  |  |  |  |  |")
    return lines


def _script_lines(scripts: list[str], run_id: str) -> list[str]:
    lines = []
    for script in scripts:
        lines.append(f"- [ ] Dry-run `{script}`: `python -m imouse.script_runner {script} --dry-run --run-id {run_id}`")
        lines.append(f"- [ ] Real-run `{script}`: `python -m imouse.script_runner {script} --run-id {run_id}`")
    return lines


def write_operator_worksheet_markdown(worksheet: dict, path: str | Path) -> Path:
    """Write an editable Markdown worksheet for field operators."""
    out_path = Path(path)
    stage = str(worksheet["stage"])
    run_id = str(worksheet["run_id"])
    devices = list(worksheet["devices"])
    lines = [
        f"# iMouse Operator Worksheet {stage.upper()}",
        "",
        f"- Generated: `{worksheet['generated_at']}`",
        f"- Run ID: `{run_id}`",
        f"- Goal: {worksheet['goal']}",
        f"- Devices: `{', '.join(devices)}`",
        "- Real iOS control verified: `False`",
        "",
        "This worksheet is a fillable field checklist. It does not write evidence and does not prove iPhone response. Only JSONL evidence plus Acceptance and Readiness PASS can support a field claim.",
        "",
        "## Bench Ledger",
        "",
        *_device_ledger_lines(devices),
        "",
        "## Operator Checklist",
        "",
        "| Done | Step | Operator action | Result | Evidence/artifact | Failure category |",
        "|---|---|---|---|---|---|",
    ]
    for step in worksheet["steps"]:
        action = str(step["operator_action"]).replace("|", "\\|")
        lines.append(f"| [ ] | {step['name']} | {action} | pass/fail/info |  |  |")
    lines.extend([
        "",
        "## Script Commands",
        "",
        *_script_lines(list(worksheet["scripts"]), run_id),
        "",
        "## Acceptance Commands",
        "",
        "```powershell",
        f".\\.venv\\Scripts\\python -m imouse.evidence_report evidence\\{run_id}.jsonl --markdown evidence\\{run_id}_review.md",
        f".\\.venv\\Scripts\\python -m imouse.acceptance evidence\\{run_id}.jsonl --gate {stage} --markdown evidence\\{run_id}_{stage}_acceptance.md --gap-markdown evidence\\{run_id}_{stage}_gap.md",
        f".\\.venv\\Scripts\\python -m imouse.readiness --target {stage} --evidence evidence\\{run_id}.jsonl --markdown evidence\\{run_id}_readiness.md",
        "```",
        "",
        "## Failure Taxonomy",
        "",
        "| Category | Meaning |",
        "|---|---|",
    ])
    for item in worksheet["failure_taxonomy"]:
        meaning = str(item["meaning"]).replace("|", "\\|")
        lines.append(f"| `{item['category']}` | {meaning} |")
    lines.extend([
        "",
        "## Promotion Rule",
        "",
        "Do not promote to the next stage unless every unresolved failure is explained, every target device has component traceability, real iPhone manual observations are recorded, and Acceptance plus Readiness both PASS.",
        "",
    ])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate an iMouse operator worksheet")
    parser.add_argument("--stage", choices=("p1", "p2", "p3", "p4"), default="p1")
    parser.add_argument("--run-id", default="", help="Field run id; generated if omitted")
    parser.add_argument("--devices", default="", help="Comma-separated device ids; defaults by stage")
    parser.add_argument("--output", default="", help="Markdown output path")
    args = parser.parse_args(argv)

    run_id = args.run_id.strip() or make_run_id(args.stage)
    worksheet = build_operator_worksheet(
        stage=args.stage,
        run_id=run_id,
        devices=parse_devices(args.devices, args.stage),
    )
    out_path = write_operator_worksheet_markdown(
        worksheet,
        args.output or f"evidence/{run_id}_{args.stage}_operator_worksheet.md",
    )
    print(f"Wrote operator worksheet: {out_path}")
    print("This worksheet is not evidence and does not prove real iOS control.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

