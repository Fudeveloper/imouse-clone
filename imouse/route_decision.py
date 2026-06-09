"""Route decision records for iMouse P1 field validation."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional

from .acceptance import PLACEHOLDER_VALUES
from .validation import ValidationRecorder, make_run_id, now_utc, safe_token


RECEIVER_ROUTES = {"uxplay", "windows_receiver", "wired", "capture_card"}
HID_ROUTES = {"ch9329", "xp_hardware", "self_built", "bluetooth"}

COMMON_REQUIRED_FIELDS = [
    "run_id",
    "target_stage",
    "xp_capability_rows",
    "receiver.route",
    "receiver.name",
    "receiver.version",
    "receiver.path",
    "receiver.capture_method",
    "hid.route",
    "hid.provider",
    "hid.id",
    "hid.firmware",
    "iphone.model",
    "iphone.ios_version",
    "bench.device_id",
    "bench.hub_id",
    "bench.hub_port",
    "bench.cable_id",
    "bench.operator",
    "evidence.expected_jsonl",
    "evidence.expected_doctor_markdown",
    "evidence.expected_readiness_markdown",
    "decision.allowed_to_run_p1",
    "decision.reason",
]

READY_REQUIRED_FIELDS = [
    "receiver.start_command",
    "receiver.airplay_name",
    "hid.serial_port",
    "evidence.plan.screenshot_probe",
    "evidence.plan.reconnect_probe",
    "evidence.plan.manual_observation",
    "evidence.plan.component_metadata",
]

DEFAULT_PLACEHOLDERS = tuple(dict.fromkeys([
    *PLACEHOLDER_VALUES,
    "EDIT_REAL",
    "EDIT_ROUTE",
    "EDIT_VERSION",
    "EDIT_PATH",
    "EDIT_COMMAND",
    "EDIT_DEVICE",
    "EDIT_OPERATOR",
    "unknown",
    "provider_or_choice",
]))


@dataclass
class DecisionCheck:
    name: str
    status: str
    message: str
    details: dict[str, Any] | None = None

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "details": self.details or {},
        }


def decision_template(run_id: str = "", devices: Optional[Iterable[str]] = None) -> dict:
    """Return an editable P1 route decision template."""
    safe_run_id = safe_token(run_id or make_run_id("p1_route"))
    device_ids = [str(item).strip() for item in (devices or ["dev_1"]) if str(item).strip()]
    if not device_ids:
        device_ids = ["dev_1"]
    first_device = device_ids[0]
    return {
        "run_id": safe_run_id,
        "created_at": now_utc(),
        "target_stage": "p1",
        "xp_capability_rows": [
            "产品路线",
            "投屏发现/连接",
            "截图采集",
            "HID 点击/滑动",
            "坐标校准",
        ],
        "receiver": {
            "route": "EDIT_ROUTE_uxplay_or_windows_receiver_or_wired_or_capture_card",
            "name": "EDIT_REAL_RECEIVER_NAME",
            "version": "EDIT_REAL_RECEIVER_VERSION",
            "path": "EDIT_REAL_INSTALL_PATH",
            "start_command": "EDIT_REAL_START_COMMAND",
            "airplay_name": "EDIT_REAL_AIRPLAY_NAME",
            "capture_method": "EDIT_REAL_CAPTURE_METHOD_window_or_display_or_sdk_or_capture_card",
            "window_binding": {
                "title": "EDIT_REAL_WINDOW_TITLE",
                "process": "EDIT_REAL_PROCESS",
                "handle": "EDIT_REAL_HANDLE_OR_EMPTY",
            },
            "license_status": "EDIT_REAL_LICENSE_STATUS",
        },
        "hid": {
            "route": "EDIT_ROUTE_ch9329_or_xp_hardware_or_self_built_or_bluetooth",
            "provider": "EDIT_REAL_HID_PROVIDER",
            "id": "EDIT_REAL_HID_ID",
            "firmware": "EDIT_REAL_FIRMWARE",
            "serial_port": "COM_EDIT_REAL",
            "baudrate": "EDIT_REAL_BAUDRATE",
        },
        "iphone": {
            "id": "EDIT_REAL_IPHONE_ID",
            "model": "EDIT_REAL_IPHONE_MODEL",
            "ios_version": "EDIT_REAL_IOS_VERSION",
            "orientation": "portrait",
            "assistive_touch": "EDIT_REAL_ON_OR_OFF",
            "pointer_speed": "EDIT_REAL_POINTER_SPEED",
        },
        "bench": {
            "device_id": first_device,
            "device_ids": device_ids,
            "hub_id": "EDIT_REAL_HUB_ID",
            "hub_port": "EDIT_REAL_HUB_PORT",
            "cable_id": "EDIT_REAL_CABLE_ID",
            "network": "EDIT_REAL_NETWORK_TOPOLOGY",
            "operator": "EDIT_REAL_OPERATOR",
        },
        "evidence": {
            "expected_jsonl": f"evidence/{safe_run_id}.jsonl",
            "expected_doctor_markdown": f"evidence/{safe_run_id}_doctor.md",
            "expected_readiness_markdown": f"evidence/{safe_run_id}_readiness.md",
            "plan": {
                "screenshot_probe": "100 screenshots, non-black, stable size",
                "reconnect_probe": "5 receiver reconnects with duration",
                "manual_observation": "operator records real iPhone click/swipe/type response",
                "component_metadata": "receiver/capture/HID/iPhone/iOS metadata recorded in evidence",
            },
        },
        "decision": {
            "allowed_to_run_p1": False,
            "reason": "EDIT_REAL_REASON",
            "open_blockers": [
                "EDIT_REAL_BLOCKER_OR_EMPTY_LIST",
            ],
        },
    }


def load_decision(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("Route decision JSON root must be an object")
    return data


def write_decision_template(path: str | Path, *, run_id: str = "", devices: Optional[Iterable[str]] = None) -> Path:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(decision_template(run_id=run_id, devices=devices), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return out_path


def evaluate_decision(data: dict, *, require_ready: bool = False) -> dict:
    checks = [
        _check_required_fields(data, COMMON_REQUIRED_FIELDS, name="required_fields"),
        _check_route_choice(data),
        _check_placeholders(data),
        _check_open_blockers(data),
    ]
    if require_ready:
        checks.append(_check_required_fields(data, READY_REQUIRED_FIELDS, name="ready_fields"))
        checks.append(_check_allowed_to_run(data))
    ready = _is_allowed(data) and not _open_blockers(data)
    fail_checks = [item for item in checks if item.status == "fail"]
    if require_ready:
        ok = not fail_checks and ready
    else:
        ok = not fail_checks
    return {
        "ok": ok,
        "ready": ready,
        "require_ready": require_ready,
        "run_id": str(data.get("run_id", "")),
        "target_stage": str(data.get("target_stage", "")),
        "checks": [item.as_dict() for item in checks],
        "blockers": [item.as_dict() for item in checks if item.status == "fail"],
        "claims": {
            "route_decision_record_valid": not any(item.status == "fail" for item in checks[:3]),
            "allowed_to_run_p1": _is_allowed(data),
            "has_open_blockers": bool(_open_blockers(data)),
            "does_not_verify_real_ios_control": True,
        },
    }


def write_decision_markdown(report: dict, path: str | Path) -> Path:
    out_path = Path(path)
    lines = [
        "# P1 Route Decision Validation",
        "",
        f"- Run ID: `{report.get('run_id', '')}`",
        f"- Target: `{str(report.get('target_stage', '')).upper()}`",
        f"- Result: {'PASS' if report.get('ok') else 'FAIL'}",
        f"- Ready to run P1: `{report.get('ready')}`",
        "- Real iOS control verified: `False`",
        "",
        "## Checks",
        "",
        "| Check | Status | Message |",
        "|---|---|---|",
    ]
    for item in report.get("checks", []):
        lines.append(f"| {item.get('name')} | {item.get('status')} | {item.get('message')} |")
    lines.extend(["", "## Blockers", ""])
    if report.get("blockers"):
        for item in report["blockers"]:
            lines.append(f"- `{item.get('name')}`: {item.get('message')}")
    else:
        lines.append("- None")
    lines.extend([
        "",
        "This validation only checks route-decision completeness. It does not prove AirPlay, HID, screenshot, or real iPhone response.",
        "",
        "If a failed route decision is recorded into evidence, treat that run as blocked. Fix the route decision and start a fresh run_id before claiming P1 pass.",
    ])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def decision_device_ids(data: dict) -> list[str]:
    found, value = _get_path(data, "bench.device_ids")
    if found and isinstance(value, list):
        ids = [str(item).strip() for item in value if str(item).strip()]
        if ids:
            return list(dict.fromkeys(ids))
    found, value = _get_path(data, "bench.device_id")
    if found and str(value).strip():
        return [str(value).strip()]
    return []


def component_metadata_from_decision(data: dict) -> dict:
    """Map a validated route decision to acceptance-readable component metadata."""
    device_ids = decision_device_ids(data)
    receiver = data.get("receiver", {}) if isinstance(data.get("receiver"), dict) else {}
    hid = data.get("hid", {}) if isinstance(data.get("hid"), dict) else {}
    iphone = data.get("iphone", {}) if isinstance(data.get("iphone"), dict) else {}
    bench = data.get("bench", {}) if isinstance(data.get("bench"), dict) else {}
    evidence = data.get("evidence", {}) if isinstance(data.get("evidence"), dict) else {}
    return {
        "manual": False,
        "route_decision": True,
        "does_not_verify_real_ios_control": True,
        "device_id": device_ids[0] if device_ids else str(bench.get("device_id", "")).strip(),
        "device_ids": device_ids,
        "receiver_provider": str(receiver.get("route", "")).strip(),
        "receiver_name": str(receiver.get("name", "")).strip(),
        "receiver_version": str(receiver.get("version", "")).strip(),
        "receiver_path": str(receiver.get("path", "")).strip(),
        "receiver_start_command": str(receiver.get("start_command", "")).strip(),
        "capture_method": str(receiver.get("capture_method", "")).strip(),
        "hid_provider": str(hid.get("provider", hid.get("route", ""))).strip(),
        "hid_route": str(hid.get("route", "")).strip(),
        "hid_id": str(hid.get("id", "")).strip(),
        "serial_port": str(hid.get("serial_port", "")).strip(),
        "hid_firmware": str(hid.get("firmware", "")).strip(),
        "iphone_id": str(iphone.get("id", "")).strip(),
        "iphone_model": str(iphone.get("model", "")).strip(),
        "ios_version": str(iphone.get("ios_version", "")).strip(),
        "hub_id": str(bench.get("hub_id", "")).strip(),
        "hub_port": str(bench.get("hub_port", "")).strip(),
        "cable_id": str(bench.get("cable_id", "")).strip(),
        "expected_jsonl": str(evidence.get("expected_jsonl", "")).strip(),
    }


def append_decision_evidence(data: dict, report: dict, evidence_jsonl: str | Path) -> Path:
    path = Path(evidence_jsonl)
    recorder = ValidationRecorder(path.stem, evidence_dir=path.parent)
    status = "pass" if report.get("ok") else "fail"
    details = component_metadata_from_decision(data)
    details.update({
        "route_decision_report": {
            "ok": report.get("ok"),
            "ready": report.get("ready"),
            "require_ready": report.get("require_ready"),
            "blockers": report.get("blockers", []),
        },
    })
    if status == "fail":
        details["failure_category"] = "route_decision"
    recorder.append(
        "route decision component metadata",
        status,
        device_ids=decision_device_ids(data),
        details=details,
    )
    return recorder.path


def _check_required_fields(data: dict, fields: list[str], *, name: str) -> DecisionCheck:
    missing = []
    for field in fields:
        found, value = _get_path(data, field)
        if not found or _blank(value):
            missing.append(field)
    if missing:
        return DecisionCheck(name, "fail", f"Missing required field(s): {', '.join(missing)}", {"missing": missing})
    return DecisionCheck(name, "pass", f"{len(fields)}/{len(fields)} required field(s) present")


def _check_route_choice(data: dict) -> DecisionCheck:
    receiver = str(_get_path(data, "receiver.route")[1] or "").strip()
    hid = str(_get_path(data, "hid.route")[1] or "").strip()
    failures = []
    if receiver not in RECEIVER_ROUTES:
        failures.append(f"receiver.route={receiver!r} not in {sorted(RECEIVER_ROUTES)}")
    if hid not in HID_ROUTES:
        failures.append(f"hid.route={hid!r} not in {sorted(HID_ROUTES)}")
    if failures:
        return DecisionCheck("route_choice", "fail", "; ".join(failures))
    return DecisionCheck("route_choice", "pass", f"receiver={receiver}, hid={hid}")


def _check_placeholders(data: dict) -> DecisionCheck:
    hits = _placeholder_hits(data, DEFAULT_PLACEHOLDERS)
    if hits:
        formatted = ", ".join(f"{item['path']}={item['value']!r}" for item in hits[:8])
        return DecisionCheck("placeholders", "fail", f"Placeholder value(s) remain: {formatted}", {"hits": hits})
    return DecisionCheck("placeholders", "pass", "No placeholder values found")


def _check_open_blockers(data: dict) -> DecisionCheck:
    blockers = _open_blockers(data)
    if blockers:
        return DecisionCheck("open_blockers", "fail", f"Open blocker(s): {', '.join(blockers)}", {"open_blockers": blockers})
    return DecisionCheck("open_blockers", "pass", "No open blockers recorded")


def _check_allowed_to_run(data: dict) -> DecisionCheck:
    if _is_allowed(data):
        return DecisionCheck("allowed_to_run_p1", "pass", "Decision explicitly allows P1 real run")
    return DecisionCheck("allowed_to_run_p1", "fail", "decision.allowed_to_run_p1 is not true")


def _get_path(data: dict, path: str) -> tuple[bool, Any]:
    current: Any = data
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False, None
    return True, current


def _blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return not value
    return False


def _placeholder_hits(value: Any, placeholders: Iterable[str], path: str = "decision") -> list[dict]:
    hits: list[dict] = []
    if isinstance(value, dict):
        for key, item in value.items():
            hits.extend(_placeholder_hits(item, placeholders, f"{path}.{key}"))
        return hits
    if isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(_placeholder_hits(item, placeholders, f"{path}[{index}]"))
        return hits
    if isinstance(value, str):
        lowered = value.lower()
        for token in placeholders:
            text = str(token).strip()
            if text and text.lower() in lowered:
                hits.append({"path": path, "value": value, "placeholder": text})
                break
    return hits


def _is_allowed(data: dict) -> bool:
    found, value = _get_path(data, "decision.allowed_to_run_p1")
    if not found:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "y", "1", "pass", "allow", "allowed"}
    return False


def _open_blockers(data: dict) -> list[str]:
    found, value = _get_path(data, "decision.open_blockers")
    if not found or value in (None, False):
        return []
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = value
    else:
        return [str(value)]
    blockers = []
    for item in items:
        text = str(item).strip()
        if text:
            blockers.append(text)
    return blockers


def _parse_devices(value: str) -> list[str]:
    devices = []
    seen = set()
    for item in value.split(","):
        text = item.strip()
        if not text or text in seen:
            continue
        seen.add(text)
        devices.append(text)
    return devices or ["dev_1"]


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Create or validate an iMouse P1 route decision record")
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="Write an editable route decision JSON template")
    init_parser.add_argument("--run-id", default="", help="Run id; generated if omitted")
    init_parser.add_argument("--devices", default="dev_1", help="Comma-separated device ids")
    init_parser.add_argument("--output", default="", help="Output JSON path")

    validate_parser = sub.add_parser("validate", help="Validate a route decision JSON file")
    validate_parser.add_argument("path", help="Route decision JSON path")
    validate_parser.add_argument("--require-ready", action="store_true", help="Fail unless the decision explicitly allows P1")
    validate_parser.add_argument("--markdown", default="", help="Optional Markdown report path")
    validate_parser.add_argument(
        "--record-evidence",
        default="",
        help="Optional evidence JSONL path to append route-decision metadata. Failed validation appends a fail event.",
    )
    validate_parser.add_argument("--json", action="store_true", help="Print full JSON report")

    args = parser.parse_args(argv)
    if args.command == "init":
        run_id = safe_token(args.run_id or make_run_id("p1_route"))
        output = args.output or f"evidence/{run_id}_route_decision.json"
        out_path = write_decision_template(output, run_id=run_id, devices=_parse_devices(args.devices))
        print(f"Wrote route decision template: {out_path}")
        return 0

    data = load_decision(args.path)
    report = evaluate_decision(data, require_ready=args.require_ready)
    if args.markdown:
        out_path = write_decision_markdown(report, args.markdown)
        print(f"Wrote route decision report: {out_path}")
    if args.record_evidence:
        evidence_path = append_decision_evidence(data, report, args.record_evidence)
        print(f"Appended route decision evidence: {evidence_path}")
        if not report["ok"]:
            print("Recorded a route decision failure; treat this run_id as blocked and use a fresh run_id after fixing blockers.")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Route decision: {'PASS' if report['ok'] else 'FAIL'}")
        print(f"Ready to run P1: {report['ready']}")
        if report["blockers"]:
            print("Blockers:")
            for item in report["blockers"]:
                print(f"- {item['name']}: {item['message']}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
