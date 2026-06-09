"""Preflight checks for iMouse XP-style field validation."""

from __future__ import annotations

import importlib
import json
import platform
import shutil
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional
from urllib import request
from urllib.error import URLError

from .airplay import find_uxplay
from .hardware import list_devices
from .receiver_provider import (
    evaluate_receiver_provider,
    load_receiver_config,
    load_receiver_config_from_route,
)


REQUIRED_MODULES = ["serial", "cv2", "numpy", "PIL", "fastapi", "uvicorn"]
RUNTIME_DIRS = [".cache/paddlex", "evidence", "screenshots", "templates", "state"]


@dataclass
class DoctorCheck:
    name: str
    status: str
    message: str
    details: dict[str, Any] | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def ok(name: str, message: str, details: Optional[dict] = None) -> DoctorCheck:
    return DoctorCheck(name, "ok", message, details or {})


def warn(name: str, message: str, details: Optional[dict] = None) -> DoctorCheck:
    return DoctorCheck(name, "warn", message, details or {})


def fail(name: str, message: str, details: Optional[dict] = None) -> DoctorCheck:
    return DoctorCheck(name, "fail", message, details or {})


def check_python() -> DoctorCheck:
    version = sys.version_info
    version_text = platform.python_version()
    details = {"executable": sys.executable, "version": version_text}
    if version.major == 3 and version.minor == 13:
        return ok("python", f"Python {version_text}", details)
    if version.major == 3 and version.minor >= 14:
        return warn(
            "python",
            f"Python {version_text}; PaddlePaddle wheels may be unavailable, prefer 3.13",
            details,
        )
    return fail("python", f"Python {version_text}; expected Python 3.13", details)


def check_modules(modules: list[str] | None = None) -> list[DoctorCheck]:
    checks = []
    for name in modules or REQUIRED_MODULES:
        try:
            mod = importlib.import_module(name)
        except ImportError as exc:
            checks.append(fail(f"module:{name}", f"Missing Python module {name}", {"error": str(exc)}))
            continue
        version = getattr(mod, "__version__", "")
        message = f"{name} import OK"
        if version:
            message += f" ({version})"
        checks.append(ok(f"module:{name}", message, {"version": version}))
    return checks


def check_binaries(receiver_config: dict | None = None, *, root: str | Path = ".") -> list[DoctorCheck]:
    checks = []
    receiver_report = evaluate_receiver_provider(receiver_config, root=root) if receiver_config else None
    if receiver_report and receiver_report["status"] == "ok":
        checks.append(ok("receiver_provider", receiver_report["message"], receiver_report["details"]))
    elif receiver_report and receiver_report["status"] == "fail":
        checks.append(fail("receiver_provider", receiver_report["message"], receiver_report["details"]))

    route = receiver_report.get("route") if receiver_report else ""
    uxplay = find_uxplay()
    if route in {"windows_receiver", "wired", "capture_card"} and receiver_report["status"] == "ok":
        checks.append(warn(
            "binary:uxplay",
            f"UxPlay not required for selected receiver route: {route}",
            {"receiver_route": route},
        ))
    elif uxplay:
        checks.append(ok("binary:uxplay", f"UxPlay found: {uxplay}", {"path": uxplay}))
    else:
        checks.append(fail("binary:uxplay", "UxPlay not found; AirPlay prototype path cannot be verified"))

    xvfb = shutil.which("Xvfb")
    if xvfb:
        checks.append(ok("binary:xvfb", f"Xvfb found: {xvfb}", {"path": xvfb}))
    else:
        checks.append(warn(
            "binary:xvfb",
            "Xvfb not found; acceptable on Windows native route, but current UxPlay/X11 prototype may need it",
        ))
    return checks


def check_serial_ports() -> DoctorCheck:
    try:
        ports = list_devices()
    except Exception as exc:
        return fail("serial_ports", f"Serial scan failed: {exc}", {"error": str(exc)})
    if not ports:
        return warn("serial_ports", "No serial ports found; HID hardware is not visible", {"ports": []})
    return ok("serial_ports", f"Found {len(ports)} serial port(s)", {"ports": ports})


def check_workspace(root: str | Path = ".") -> list[DoctorCheck]:
    checks = []
    root_path = Path(root)
    try:
        root_path.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", delete=False, dir=root_path, encoding="utf-8") as fh:
            fh.write("doctor")
            temp_path = Path(fh.name)
        temp_path.unlink(missing_ok=True)
        checks.append(ok("workspace:writable", f"Workspace is writable: {root_path.resolve()}"))
    except Exception as exc:
        checks.append(fail("workspace:writable", f"Workspace is not writable: {exc}", {"error": str(exc)}))

    for dirname in RUNTIME_DIRS:
        path = root_path / dirname
        if path.exists():
            checks.append(ok(f"dir:{dirname}", f"{dirname} exists", {"path": str(path)}))
        else:
            checks.append(warn(f"dir:{dirname}", f"{dirname} does not exist yet; it will be created at runtime"))
    return checks


def check_state_files(root: str | Path = ".") -> list[DoctorCheck]:
    root_path = Path(root)
    checks = []
    for relative in ["state/groups.json", "state/calibration.json", "state/device_profiles.json"]:
        path = root_path / relative
        if path.exists():
            checks.append(ok(f"state:{relative}", f"{relative} exists", {"path": str(path)}))
        else:
            checks.append(warn(f"state:{relative}", f"{relative} missing; no persisted state yet"))
    return checks


def check_server(base_url: str) -> DoctorCheck:
    url = f"{base_url.rstrip('/')}/api?fun=/dev/list&msgid=doctor"
    try:
        with request.urlopen(url, timeout=3) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (OSError, URLError, json.JSONDecodeError) as exc:
        return fail("server", f"Server check failed: {exc}", {"url": url, "error": str(exc)})
    if payload.get("status") == 200 and payload.get("fun") == "/device/list":
        return ok("server", f"XP API server OK: {base_url}", {"response": payload})
    return fail("server", "XP API server returned unexpected payload", {"url": url, "response": payload})


def run_doctor(
    root: str | Path = ".",
    server_url: str = "",
    *,
    receiver_config: dict | None = None,
    receiver_config_path: str | Path | None = None,
    route_decision_path: str | Path | None = None,
) -> dict:
    checks: list[DoctorCheck] = []
    resolved_receiver_config = _load_receiver_preflight_config(
        receiver_config=receiver_config,
        receiver_config_path=receiver_config_path,
        route_decision_path=route_decision_path,
    )
    checks.append(check_python())
    checks.extend(check_modules())
    checks.extend(check_binaries(resolved_receiver_config, root=root))
    checks.append(check_serial_ports())
    checks.extend(check_workspace(root))
    checks.extend(check_state_files(root))
    if server_url:
        checks.append(check_server(server_url))

    counts = {"ok": 0, "warn": 0, "fail": 0}
    for check in checks:
        counts[check.status] = counts.get(check.status, 0) + 1
    overall = "fail" if counts.get("fail") else ("warn" if counts.get("warn") else "ok")
    return {
        "overall": overall,
        "counts": counts,
        "checks": [check.to_dict() for check in checks],
    }


def _load_receiver_preflight_config(
    *,
    receiver_config: dict | None = None,
    receiver_config_path: str | Path | None = None,
    route_decision_path: str | Path | None = None,
) -> dict | None:
    if receiver_config:
        return receiver_config
    if receiver_config_path:
        path = Path(receiver_config_path)
        if path.exists():
            return load_receiver_config(path)
    if route_decision_path:
        path = Path(route_decision_path)
        if path.exists():
            return load_receiver_config_from_route(path)
    return None


def write_markdown(report: dict, path: str | Path) -> Path:
    out_path = Path(path)
    lines = [
        "# iMouse Preflight Doctor",
        "",
        f"- Overall: `{report['overall']}`",
        f"- OK: {report['counts'].get('ok', 0)}",
        f"- Warn: {report['counts'].get('warn', 0)}",
        f"- Fail: {report['counts'].get('fail', 0)}",
        "",
        "## Checks",
        "",
    ]
    for check in report["checks"]:
        lines.append(f"- `{check['status']}` **{check['name']}**: {check['message']}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def main(argv: Optional[list[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run iMouse preflight checks")
    parser.add_argument("--server-url", default="", help="Optional XP API server URL to probe")
    parser.add_argument("--receiver-config", default="", help="Optional receiver provider JSON to validate")
    parser.add_argument("--route-decision", default="", help="Optional route decision JSON with receiver fields")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    parser.add_argument("--markdown", default="", help="Write markdown report to this path")
    args = parser.parse_args(argv)

    report = run_doctor(
        server_url=args.server_url,
        receiver_config_path=args.receiver_config or None,
        route_decision_path=args.route_decision or None,
    )
    if args.markdown:
        write_markdown(report, args.markdown)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Overall: {report['overall']}")
        for check in report["checks"]:
            print(f"[{check['status']}] {check['name']}: {check['message']}")
    return 0 if report["overall"] != "fail" else 1


if __name__ == "__main__":
    raise SystemExit(main())
