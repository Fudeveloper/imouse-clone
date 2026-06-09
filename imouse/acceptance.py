"""Acceptance gate checks for iMouse field evidence."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from .evidence_report import recorder_from_jsonl


GATE_LEVELS = ("p1", "p2", "p3", "p4")


@dataclass(frozen=True)
class GateCriteria:
    min_devices: int
    min_manual_pass: int
    min_screenshot_ok: int
    min_metrics: int
    require_component_traceability: bool = True


DEFAULT_CRITERIA = {
    "p1": GateCriteria(min_devices=1, min_manual_pass=1, min_screenshot_ok=1, min_metrics=0),
    "p2": GateCriteria(min_devices=1, min_manual_pass=2, min_screenshot_ok=2, min_metrics=1),
    "p3": GateCriteria(min_devices=4, min_manual_pass=1, min_screenshot_ok=0, min_metrics=1),
    "p4": GateCriteria(min_devices=10, min_manual_pass=2, min_screenshot_ok=0, min_metrics=1),
}

COMPONENT_REQUIREMENTS = {
    "receiver_provider": ("receiver_provider", "capture_provider"),
    "capture_method": ("capture_method",),
    "hid_provider": ("hid_provider",),
    "hid_identity": ("hid_id", "serial_port", "hardware_id", "port"),
    "iphone_identity": ("iphone_id", "iphone", "iphone_model"),
    "ios_version": ("ios_version", "ios"),
}

PLACEHOLDER_VALUES = (
    "EDIT_ME",
    "TODO",
    "TBD",
    "COM_EDIT_ME",
    "uxplay_or_windows_receiver_or_wired_capture",
    "window_or_display_or_sdk_or_capture_card",
    "ch9329_or_xp_hardware",
)


def _flatten_details(value: Any) -> list[dict]:
    found = []
    if isinstance(value, dict):
        found.append(value)
        for item in value.values():
            found.extend(_flatten_details(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(_flatten_details(item))
    return found


def _manual_pass_count(events: list[dict]) -> int:
    count = 0
    for event in events:
        if event.get("status") != "pass":
            continue
        if any(details.get("manual") is True for details in _flatten_details(event.get("details", {}))):
            count += 1
    return count


def _screenshot_ok_count(events: list[dict]) -> int:
    count = 0
    for event in events:
        for details in _flatten_details(event.get("details", {})):
            quality = details.get("screenshot_quality")
            if isinstance(quality, dict) and quality.get("ok") is True:
                count += 1
                break
    return count


def _unique_devices(events: list[dict]) -> set[str]:
    devices = set()
    for event in events:
        for device_id in event.get("device_ids", []):
            text = str(device_id).strip()
            if text:
                devices.add(text)
    return devices


def _detail_device_ids(value: Any) -> set[str]:
    ids = set()
    if isinstance(value, dict):
        for key in ("device_id", "id"):
            text = str(value.get(key, "")).strip()
            if text:
                ids.add(text)
        for key in ("device_ids", "ids"):
            items = value.get(key)
            if isinstance(items, list):
                ids.update(str(item).strip() for item in items if str(item).strip())
        for item in value.values():
            ids.update(_detail_device_ids(item))
    elif isinstance(value, list):
        for item in value:
            ids.update(_detail_device_ids(item))
    return ids


def _clean_component_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    return ""


def _is_placeholder(value: str) -> bool:
    lowered = value.lower()
    return any(token.lower() in lowered for token in PLACEHOLDER_VALUES)


def _component_groups(details: dict) -> tuple[set[str], list[dict]]:
    groups = set()
    placeholders = []
    for details_item in _flatten_details(details):
        for group, keys in COMPONENT_REQUIREMENTS.items():
            for key in keys:
                value = _clean_component_value(details_item.get(key))
                if not value:
                    continue
                if _is_placeholder(value):
                    placeholders.append({"group": group, "key": key, "value": value})
                    continue
                groups.add(group)
                break
    return groups, placeholders


def _component_traceability(events: list[dict], required_devices: int) -> dict:
    by_device: dict[str, set[str]] = {}
    placeholder_hits = []
    for event in events:
        details = event.get("details", {})
        event_devices = set(str(item).strip() for item in event.get("device_ids", []) if str(item).strip())
        event_devices.update(_detail_device_ids(details))
        if not event_devices:
            continue
        groups, placeholders = _component_groups(details if isinstance(details, dict) else {})
        placeholder_hits.extend(placeholders)
        if not groups:
            continue
        for device_id in event_devices:
            by_device.setdefault(device_id, set()).update(groups)

    complete_devices = []
    missing_by_device = {}
    required_groups = set(COMPONENT_REQUIREMENTS)
    for device_id, groups in sorted(by_device.items()):
        missing = sorted(required_groups - groups)
        if missing:
            missing_by_device[device_id] = missing
        else:
            complete_devices.append(device_id)
    ok = len(complete_devices) >= required_devices and not placeholder_hits
    return {
        "ok": ok,
        "complete_devices": complete_devices,
        "required_devices": required_devices,
        "required_groups": sorted(required_groups),
        "missing_by_device": missing_by_device,
        "placeholder_hits": placeholder_hits,
    }


def _check(name: str, ok: bool, message: str, details: Optional[dict] = None) -> dict:
    return {
        "name": name,
        "status": "pass" if ok else "fail",
        "message": message,
        "details": details or {},
    }


def evaluate_acceptance(
    evidence_jsonl: str | Path,
    *,
    gate: str = "p1",
    min_devices: Optional[int] = None,
) -> dict:
    """Evaluate whether an evidence JSONL file passes a field gate."""
    normalized_gate = gate.lower().strip()
    if normalized_gate not in DEFAULT_CRITERIA:
        raise ValueError(f"Unsupported gate: {gate}")

    path = Path(evidence_jsonl)
    recorder = recorder_from_jsonl(path)
    events = recorder.load()
    summary = recorder.summary()
    criteria = DEFAULT_CRITERIA[normalized_gate]
    required_devices = criteria.min_devices if min_devices is None else int(min_devices)
    devices = _unique_devices(events)
    manual_pass = _manual_pass_count(events)
    screenshot_ok = _screenshot_ok_count(events)
    metrics_count = int(summary.get("metrics", {}).get("count", 0) or 0)
    failures = int(summary.get("by_status", {}).get("fail", 0) or 0)
    component_traceability = _component_traceability(events, required_devices)

    checks = [
        _check(
            "evidence_exists",
            path.exists() and bool(events),
            f"{len(events)} evidence event(s) loaded",
            {"path": str(path)},
        ),
        _check(
            "no_fail_events",
            failures == 0,
            f"{failures} fail event(s) recorded",
        ),
        _check(
            "device_traceability",
            len(devices) >= required_devices,
            f"{len(devices)} unique device id(s), required >= {required_devices}",
            {"devices": sorted(devices)},
        ),
        _check(
            "component_traceability",
            (not criteria.require_component_traceability) or component_traceability["ok"],
            (
                f"{len(component_traceability['complete_devices'])} device(s) with receiver/capture/HID/iOS "
                f"component metadata, required >= {required_devices}"
            ),
            component_traceability,
        ),
        _check(
            "manual_observation",
            manual_pass >= criteria.min_manual_pass,
            f"{manual_pass} manual pass observation(s), required >= {criteria.min_manual_pass}",
        ),
        _check(
            "screenshot_quality",
            screenshot_ok >= criteria.min_screenshot_ok,
            f"{screenshot_ok} screenshot quality pass sample(s), required >= {criteria.min_screenshot_ok}",
        ),
        _check(
            "metrics",
            metrics_count >= criteria.min_metrics,
            f"{metrics_count} metrics sample(s), required >= {criteria.min_metrics}",
        ),
    ]
    ok = all(item["status"] == "pass" for item in checks)
    return {
        "ok": ok,
        "gate": normalized_gate,
        "criteria": {
            "min_devices": required_devices,
            "min_manual_pass": criteria.min_manual_pass,
            "min_screenshot_ok": criteria.min_screenshot_ok,
            "min_metrics": criteria.min_metrics,
            "require_component_traceability": criteria.require_component_traceability,
        },
        "checks": checks,
        "summary": summary,
    }


GAP_ACTIONS = {
    "evidence_exists": {
        "action": "Start the GUI with Record enabled or run a real script so evidence JSONL contains field events.",
        "gui": "Set Evidence run_id, keep Record checked, then run Doctor, Metadata, Screenshot, Manual, and Scenario steps.",
        "evidence": "At least one JSONL event from the current run.",
    },
    "no_fail_events": {
        "action": "Review fail events, fix the root cause, and rerun with a fresh run_id if the failure blocks the field claim.",
        "gui": "Use Review, inspect failure category, then repeat the failed receiver/HID/capture/manual step.",
        "evidence": "A fresh run with zero unresolved fail events.",
    },
    "device_traceability": {
        "action": "Record every target device id on metadata, screenshot, manual, script, or group events.",
        "gui": "Select devices in the device table before running commands; use groups for P3/P4.",
        "evidence": "Unique device ids matching the gate requirement.",
    },
    "component_traceability": {
        "action": "Record receiver, capture, HID, serial or HID id, iPhone identity, and iOS version per device.",
        "gui": "Fill Metadata, click Record Metadata, or validate a complete Route Decision.",
        "evidence": "Component metadata event(s) with no placeholders.",
    },
    "manual_observation": {
        "action": "Record real iPhone response observed by the operator after click/swipe/type or group actions.",
        "gui": "Use Manual with status=pass only after the iPhone visibly responded.",
        "evidence": "Manual pass observation event(s).",
    },
    "screenshot_quality": {
        "action": "Capture real screenshots and keep only non-black, non-white, correctly bound frames.",
        "gui": "Start Capture, click Screenshot, verify preview quality, then save artifacts when useful.",
        "evidence": "Screenshot event(s) with screenshot_quality.ok=true.",
    },
    "metrics": {
        "action": "Record system metrics during stability or multi-device runs.",
        "gui": "Run the P2/P3/P4 watchdog scenario or a script metrics step.",
        "evidence": "Metrics sample event(s).",
    },
}


def acceptance_gap_rows(report: dict) -> list[dict[str, str]]:
    """Return actionable rows for failed acceptance checks."""
    rows = []
    for check in report.get("checks", []):
        if not isinstance(check, dict) or check.get("status") == "pass":
            continue
        name = str(check.get("name", "") or "unknown")
        action = GAP_ACTIONS.get(name, {})
        rows.append({
            "check": name,
            "message": str(check.get("message", "") or ""),
            "action": action.get("action", "Review this failed acceptance check and add stronger field evidence."),
            "gui": action.get("gui", "Use the GUI evidence controls or script runner to add field evidence."),
            "evidence": action.get("evidence", "Field evidence that makes this check pass."),
        })
    return rows


def acceptance_gap_brief(report: dict) -> str:
    gate = str(report.get("gate", "p1") or "p1").upper()
    rows = acceptance_gap_rows(report)
    names = ", ".join(row["check"] for row in rows[:3]) if rows else "none"
    return f"Acceptance gap {gate}: items={len(rows)}; failed={names}"


def write_acceptance_gap_markdown(report: dict, path: str | Path) -> Path:
    out_path = Path(path)
    rows = acceptance_gap_rows(report)
    lines = [
        f"# Acceptance Evidence Gap {str(report.get('gate', 'p1')).upper()}",
        "",
        f"- Acceptance result: `{'PASS' if report.get('ok') else 'FAIL'}`",
        f"- Evidence: `{report.get('summary', {}).get('path', '')}`",
        f"- Gap items: `{len(rows)}`",
        "- Real iOS control verified: `False`",
        "",
        "This gap report is a fill checklist. It does not write evidence and does not prove AirPlay, HID, screenshots, or real iPhone response.",
        "",
        "## Gap Items",
        "",
        "| Check | Current message | GUI action | Evidence needed |",
        "|---|---|---|---|",
    ]
    if rows:
        for row in rows:
            message = row["message"].replace("|", "\\|")
            gui = row["gui"].replace("|", "\\|")
            evidence = row["evidence"].replace("|", "\\|")
            lines.append(f"| `{row['check']}` | {message} | {gui} | {evidence} |")
    else:
        lines.append("| None | No failed acceptance checks | Still run readiness and verify real iPhone behavior. | Acceptance alone is not the full delivery claim. |")
    lines.extend([
        "",
        "## Next Step",
        "",
        "Use the listed GUI actions to add real evidence, then rerun Acceptance and Readiness. If a route decision failure was recorded, start a fresh run_id after fixing it.",
        "",
    ])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def write_acceptance_markdown(report: dict, path: str | Path) -> Path:
    out_path = Path(path)
    lines = [
        f"# Acceptance Gate {report['gate'].upper()}",
        "",
        f"- Result: {'PASS' if report['ok'] else 'FAIL'}",
        f"- Evidence: `{report['summary'].get('path', '')}`",
        "",
        "## Checks",
        "",
        "| Check | Status | Message |",
        "|---|---|---|",
    ]
    for item in report["checks"]:
        lines.append(f"| {item['name']} | {item['status']} | {item['message']} |")
    lines.extend(["", "## Failure Categories", ""])
    categories = report["summary"].get("by_failure_category", {})
    if categories:
        for category, count in categories.items():
            lines.append(f"- {category}: {count}")
    else:
        lines.append("- None")
    lines.extend(["", "## Recommendations", ""])
    for item in report["summary"].get("recommendations", []):
        lines.append(f"- {item}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate iMouse evidence against a field acceptance gate")
    parser.add_argument("evidence_jsonl", help="Path to evidence/<run_id>.jsonl")
    parser.add_argument("--gate", choices=GATE_LEVELS, default="p1", help="Acceptance gate to evaluate")
    parser.add_argument("--min-devices", type=int, default=None, help="Override required unique device count")
    parser.add_argument("--markdown", default="", help="Optional output Markdown path")
    parser.add_argument("--gap-markdown", default="", help="Optional evidence gap Markdown path")
    parser.add_argument("--json", action="store_true", help="Print full JSON report")
    args = parser.parse_args(argv)

    report = evaluate_acceptance(args.evidence_jsonl, gate=args.gate, min_devices=args.min_devices)
    if args.markdown:
        out_path = write_acceptance_markdown(report, args.markdown)
        print(f"Wrote acceptance report: {out_path}")
    if args.gap_markdown:
        out_path = write_acceptance_gap_markdown(report, args.gap_markdown)
        print(f"Wrote acceptance gap report: {out_path}")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Acceptance {args.gate.upper()}: {'PASS' if report['ok'] else 'FAIL'}")
        for item in report["checks"]:
            print(f"- {item['status']}: {item['name']} - {item['message']}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
