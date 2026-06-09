"""Receiver provider configuration and preflight validation."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any, Optional

from .airplay import find_uxplay
from .route_decision import DEFAULT_PLACEHOLDERS, RECEIVER_ROUTES, load_decision


ALT_RECEIVER_ROUTES = {"windows_receiver", "wired", "capture_card"}
AIRPLAY_ROUTES = {"uxplay", "windows_receiver"}
CAPTURE_METHODS = {"window", "display", "sdk", "capture_card", "wired", "other"}


def receiver_config_from_decision(data: dict) -> dict:
    """Extract receiver provider fields from a route decision or receiver config."""
    receiver = data.get("receiver", data)
    if not isinstance(receiver, dict):
        receiver = {}
    window_binding = receiver.get("window_binding", {})
    if not isinstance(window_binding, dict):
        window_binding = {}
    return {
        "route": str(receiver.get("route", "") or "").strip(),
        "name": str(receiver.get("name", "") or "").strip(),
        "version": str(receiver.get("version", "") or "").strip(),
        "path": str(receiver.get("path", "") or "").strip(),
        "start_command": str(receiver.get("start_command", "") or "").strip(),
        "airplay_name": str(receiver.get("airplay_name", "") or "").strip(),
        "capture_method": str(receiver.get("capture_method", "") or "").strip(),
        "window_title": str(window_binding.get("title", receiver.get("window_title", "")) or "").strip(),
        "window_process": str(window_binding.get("process", receiver.get("window_process", "")) or "").strip(),
        "window_handle": str(window_binding.get("handle", receiver.get("window_handle", "")) or "").strip(),
        "license_status": str(receiver.get("license_status", "") or "").strip(),
    }


def load_receiver_config(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("Receiver config JSON root must be an object")
    return receiver_config_from_decision(data)


def load_receiver_config_from_route(path: str | Path) -> dict:
    return receiver_config_from_decision(load_decision(path))


def evaluate_receiver_provider(
    config: dict | None = None,
    *,
    root: str | Path = ".",
    uxplay_path: str | None = None,
) -> dict:
    """Evaluate a receiver route without starting it or claiming capture success."""
    if not config:
        return {
            "status": "warn",
            "route": "",
            "message": "No receiver provider config supplied; default UxPlay binary check is required.",
            "details": {},
        }

    normalized = receiver_config_from_decision(config)
    route = normalized["route"]
    missing = _missing_fields(normalized)
    placeholders = _placeholder_fields(normalized)
    path_status = _receiver_path_status(normalized, root=root, uxplay_path=uxplay_path)
    invalid = []
    if route not in RECEIVER_ROUTES:
        invalid.append(f"route={route!r} not in {sorted(RECEIVER_ROUTES)}")
    capture_method = normalized["capture_method"]
    if capture_method and capture_method not in CAPTURE_METHODS:
        invalid.append(f"capture_method={capture_method!r} not in {sorted(CAPTURE_METHODS)}")
    if route == "capture_card" and capture_method and capture_method != "capture_card":
        invalid.append("capture_card route requires capture_method=capture_card")
    if route == "wired" and capture_method and capture_method not in {"wired", "sdk", "display", "other"}:
        invalid.append("wired route expects capture_method wired/sdk/display/other")

    problems = []
    if invalid:
        problems.extend(invalid)
    if missing:
        problems.append(f"missing={', '.join(missing)}")
    if placeholders:
        problems.append(f"placeholder={', '.join(placeholders)}")
    if path_status["status"] == "fail":
        problems.append(path_status["message"])
    if problems:
        return {
            "status": "fail",
            "route": route,
            "message": "; ".join(problems),
            "details": {
                "config": normalized,
                "missing": missing,
                "placeholders": placeholders,
                "path": path_status,
                "invalid": invalid,
            },
        }
    return {
        "status": "ok",
        "route": route,
        "message": f"Receiver provider ready for preflight: {route}",
        "details": {
            "config": normalized,
            "path": path_status,
            "does_not_verify_real_capture": True,
        },
    }


def receiver_provider_brief(report: dict) -> str:
    route = str(report.get("route", "") or "none")
    status = str(report.get("status", "unknown"))
    return f"Receiver provider {route}: {status}; {report.get('message', '')}"


def _missing_fields(config: dict) -> list[str]:
    required = ["route", "name", "version", "path", "start_command", "capture_method"]
    if config.get("route") in AIRPLAY_ROUTES:
        required.append("airplay_name")
    if config.get("capture_method") == "window":
        required.append("window_title")
    return [field for field in required if not str(config.get(field, "")).strip()]


def _placeholder_fields(config: dict) -> list[str]:
    fields = []
    for key, value in config.items():
        text = str(value or "").strip()
        if text and _has_placeholder(text):
            fields.append(key)
    return fields


def _has_placeholder(text: str) -> bool:
    lowered = text.lower()
    return any(token and str(token).lower() in lowered for token in DEFAULT_PLACEHOLDERS)


def _receiver_path_status(config: dict, *, root: str | Path = ".", uxplay_path: str | None = None) -> dict:
    route = config.get("route", "")
    raw_path = str(config.get("path", "") or "").strip()
    if not raw_path:
        return {"status": "fail", "message": "receiver.path is required", "path": raw_path}
    resolved = _resolve_existing_path(raw_path, root=root)
    if resolved:
        return {"status": "ok", "message": f"receiver path exists: {resolved}", "path": str(resolved)}
    if route == "uxplay":
        found = uxplay_path if uxplay_path is not None else find_uxplay()
        if found:
            return {"status": "ok", "message": f"UxPlay found: {found}", "path": str(found)}
        which = shutil.which(raw_path)
        if which:
            return {"status": "ok", "message": f"UxPlay command found: {which}", "path": str(which)}
    return {"status": "fail", "message": f"receiver.path not found: {raw_path}", "path": raw_path}


def _resolve_existing_path(value: str, *, root: str | Path = ".") -> Path | None:
    path = Path(value)
    candidates = [path]
    if not path.is_absolute():
        candidates.append(Path(root) / path)
    for candidate in candidates:
        try:
            if candidate.exists():
                return candidate.resolve()
        except OSError:
            continue
    return None


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an iMouse receiver provider config.")
    parser.add_argument("path", help="Receiver config JSON or route decision JSON")
    parser.add_argument("--route-decision", action="store_true", help="Treat path as a route decision JSON")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    config = load_receiver_config_from_route(args.path) if args.route_decision else load_receiver_config(args.path)
    report = evaluate_receiver_provider(config)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(receiver_provider_brief(report))
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
