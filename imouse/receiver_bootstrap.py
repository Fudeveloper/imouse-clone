"""Bootstrap a receiver route decision for P1 preflight.

The bootstrap fills the receiver/capture lane so Doctor can validate an
alternate receiver route. It intentionally keeps P1 blocked until HID, iPhone,
bench, screenshot, and manual-observation evidence are supplied.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .receiver_provider import evaluate_receiver_provider, receiver_config_from_decision
from .route_decision import RECEIVER_ROUTES, decision_template, evaluate_decision
from .validation import safe_token


DEFAULT_CAPTURE_BY_ROUTE = {
    "uxplay": "window",
    "windows_receiver": "window",
    "wired": "wired",
    "capture_card": "capture_card",
}


def build_receiver_bootstrap_decision(
    *,
    run_id: str,
    route: str,
    receiver_path: str,
    receiver_name: str = "",
    version: str = "",
    start_command: str = "",
    airplay_name: str = "",
    capture_method: str = "",
    window_title: str = "",
    window_process: str = "",
    device_id: str = "dev_1",
) -> dict[str, Any]:
    normalized_route = str(route or "").strip()
    safe_run_id = safe_token(run_id or "p1_receiver_bootstrap")
    data = decision_template(run_id=safe_run_id, devices=[device_id or "dev_1"])
    receiver_label = receiver_name or f"{normalized_route}_receiver"
    capture = capture_method or DEFAULT_CAPTURE_BY_ROUTE.get(normalized_route, "window")
    command = start_command or f'"{receiver_path}"'
    title = window_title or (receiver_label if capture == "window" else "")
    process = window_process or Path(receiver_path).name
    data["receiver"].update({
        "route": normalized_route,
        "name": receiver_label,
        "version": version or "unverified",
        "path": receiver_path,
        "start_command": command,
        "airplay_name": airplay_name or receiver_label,
        "capture_method": capture,
        "window_binding": {
            "title": title,
            "process": process,
            "handle": "",
        },
        "license_status": "unverified",
    })
    data["decision"] = {
        "allowed_to_run_p1": False,
        "reason": "Receiver route bootstrap only. Complete HID, iPhone settings, bench ledger, screenshot quality, manual observation, Acceptance, and Readiness before P1.",
        "open_blockers": [
            "Fill HID route/provider/id/firmware/serial fields with real hardware values.",
            "Fill iPhone id/model/iOS/settings and bench Hub/cable/operator fields.",
            "Run Doctor with this route decision, then run Screenshot/Shot Bench and P1 Trial on a real iPhone.",
        ],
    }
    return data


def receiver_bootstrap_report(data: dict[str, Any], *, root: str | Path = ".") -> dict[str, Any]:
    provider = evaluate_receiver_provider(receiver_config_from_decision(data), root=root)
    decision = evaluate_decision(data, require_ready=True)
    return {
        "ok_for_receiver_preflight": provider.get("status") == "ok",
        "ready_for_p1": False,
        "receiver_provider": provider,
        "route_decision": decision,
        "claims": {
            "does_not_verify_screenshot_quality": True,
            "does_not_verify_real_ios_control": True,
            "does_not_verify_xp_parity": True,
        },
        "next_commands": [
            "python -m imouse.doctor --route-decision <route_decision.json> --markdown evidence/<run_id>_doctor.md",
            "python -m imouse.route_decision validate <route_decision.json> --require-ready",
            "python -m imouse.readiness --target p1 --evidence evidence/<run_id>.jsonl",
        ],
    }


def write_bootstrap_decision(data: dict[str, Any], path: str | Path) -> Path:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out_path


def write_bootstrap_markdown(report: dict[str, Any], path: str | Path, *, route_decision_path: str | Path = "") -> Path:
    out_path = Path(path)
    provider = report.get("receiver_provider", {})
    decision = report.get("route_decision", {})
    lines = [
        "# Receiver Route Bootstrap",
        "",
        f"- Receiver preflight OK: `{report.get('ok_for_receiver_preflight')}`",
        f"- Ready for P1: `{report.get('ready_for_p1')}`",
        f"- Route decision: `{route_decision_path}`",
        "- Real iOS control verified: `False`",
        "- This bootstrap only fills the receiver lane. It does not prove screenshot quality, real iPhone response, or XP parity.",
        "",
        "## Receiver Provider",
        "",
        f"- Status: `{provider.get('status', '')}`",
        f"- Route: `{provider.get('route', '')}`",
        f"- Message: {provider.get('message', '')}",
        "",
        "## Route Decision",
        "",
        f"- Valid and ready: `{decision.get('ok')}`",
        f"- Ready flag: `{decision.get('ready')}`",
        "",
        "## Blockers",
        "",
    ]
    blockers = decision.get("blockers", []) if isinstance(decision, dict) else []
    if blockers:
        for item in blockers:
            lines.append(f"- `{item.get('name', '')}`: {item.get('message', '')}")
    else:
        lines.append("- None")
    lines.extend([
        "",
        "## Next Commands",
        "",
    ])
    for command in report.get("next_commands", []) or []:
        lines.append(f"- `{command}`")
    lines.extend([
        "",
        "## Stop Rule",
        "",
        "Do not use this bootstrap as a pass. It can remove the default UxPlay hard blocker only when the receiver path is real. P1 still requires current screenshots, visible click/swipe/type observations on the physical iPhone, JSONL evidence, Acceptance PASS, and Readiness PASS.",
        "",
    ])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a receiver route bootstrap decision")
    parser.add_argument("--run-id", default="p1_receiver_bootstrap")
    parser.add_argument("--route", choices=sorted(RECEIVER_ROUTES), default="windows_receiver")
    parser.add_argument("--receiver-path", required=True)
    parser.add_argument("--receiver-name", default="")
    parser.add_argument("--version", default="")
    parser.add_argument("--start-command", default="")
    parser.add_argument("--airplay-name", default="")
    parser.add_argument("--capture-method", default="")
    parser.add_argument("--window-title", default="")
    parser.add_argument("--window-process", default="")
    parser.add_argument("--device-id", default="dev_1")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    data = build_receiver_bootstrap_decision(
        run_id=args.run_id,
        route=args.route,
        receiver_path=args.receiver_path,
        receiver_name=args.receiver_name,
        version=args.version,
        start_command=args.start_command,
        airplay_name=args.airplay_name,
        capture_method=args.capture_method,
        window_title=args.window_title,
        window_process=args.window_process,
        device_id=args.device_id,
    )
    output = args.output or f"evidence/{safe_token(args.run_id)}_route_decision.json"
    decision_path = write_bootstrap_decision(data, output)
    report = receiver_bootstrap_report(data)
    if args.markdown:
        write_bootstrap_markdown(report, args.markdown, route_decision_path=decision_path)
    if args.json:
        print(json.dumps({"route_decision": str(decision_path), "report": report}, ensure_ascii=False, indent=2))
    else:
        print(f"Wrote receiver route decision bootstrap: {decision_path}")
        print(f"Receiver preflight OK: {report['ok_for_receiver_preflight']}")
        print("Ready for P1: False")
    return 0 if report["ok_for_receiver_preflight"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
