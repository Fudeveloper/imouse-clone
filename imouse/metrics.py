"""Lightweight system metrics for field stability evidence."""

from __future__ import annotations

import os
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


def _now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_percent(used: int, total: int) -> Optional[float]:
    if total <= 0:
        return None
    return round((used / total) * 100, 2)


def _memory_from_psutil() -> dict[str, Any] | None:
    try:
        import psutil  # type: ignore
    except Exception:
        return None
    vm = psutil.virtual_memory()
    proc = psutil.Process(os.getpid())
    info = proc.memory_info()
    return {
        "source": "psutil",
        "total_bytes": int(vm.total),
        "available_bytes": int(vm.available),
        "used_percent": float(vm.percent),
        "process_rss_bytes": int(info.rss),
    }


def _memory_from_windows() -> dict[str, Any] | None:
    if platform.system().lower() != "windows":
        return None
    try:
        import ctypes
        from ctypes import wintypes

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", wintypes.DWORD),
                ("dwMemoryLoad", wintypes.DWORD),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
            return None
    except Exception:
        return None
    return {
        "source": "GlobalMemoryStatusEx",
        "total_bytes": int(stat.ullTotalPhys),
        "available_bytes": int(stat.ullAvailPhys),
        "used_percent": float(stat.dwMemoryLoad),
    }


def _memory_from_proc() -> dict[str, Any] | None:
    path = Path("/proc/meminfo")
    if not path.exists():
        return None
    values: dict[str, int] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) < 2:
                continue
            key = parts[0].rstrip(":")
            values[key] = int(parts[1]) * 1024
    except Exception:
        return None
    total = values.get("MemTotal")
    available = values.get("MemAvailable")
    if not total or available is None:
        return None
    used = total - available
    return {
        "source": "/proc/meminfo",
        "total_bytes": total,
        "available_bytes": available,
        "used_percent": _safe_percent(used, total),
    }


def collect_system_metrics(*, label: str = "", extra: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """Collect best-effort host metrics without requiring extra dependencies."""

    disk = shutil.disk_usage(".")
    memory = _memory_from_psutil() or _memory_from_windows() or _memory_from_proc() or {"source": "unavailable"}
    payload: dict[str, Any] = {
        "ts": _now_utc(),
        "label": label,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
        },
        "python": {
            "version": platform.python_version(),
            "executable": sys.executable,
        },
        "process": {
            "pid": os.getpid(),
        },
        "cpu": {
            "count": os.cpu_count(),
        },
        "memory": memory,
        "disk": {
            "path": str(Path(".").resolve()),
            "total_bytes": int(disk.total),
            "used_bytes": int(disk.used),
            "free_bytes": int(disk.free),
            "used_percent": _safe_percent(int(disk.used), int(disk.total)),
        },
    }
    if extra:
        payload["extra"] = extra
    return payload

