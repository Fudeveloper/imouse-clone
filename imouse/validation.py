"""Validation evidence recording for field and lab test runs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional


DEFAULT_EVIDENCE_DIR = Path("evidence")
VALID_STATUSES = {"pass", "fail", "info", "skip"}
_SAFE_TOKEN = re.compile(r"[^A-Za-z0-9_.-]+")

FAILURE_CATEGORY_KEYWORDS = {
    "route_decision": ["route decision", "route_decision", "allowed_to_run_p1", "open_blockers"],
    "airplay_discovery": ["airplay discovery", "receiver not found", "bonjour", "mdns", "ap isolation"],
    "airplay_stream": ["uxplay", "airplay", "black screen", "disconnect", "stream", "mirror"],
    "capture": ["screenshot", "capture", "screen size", "black frame"],
    "calibration": ["calibration", "coordinate", "offset", "safe area", "orientation"],
    "vision_template": ["template", "find_image", "find image", "matchtemplate"],
    "vision_color": ["find_color", "find_colors", "find color", "multi color", "rgb", "tolerance"],
    "ocr": ["ocr", "paddleocr", "paddlex"],
    "hid": ["hid", "hardware", "serial", "com", "mouse", "keyboard", "not connected"],
    "group_dispatch": ["group", "batch", "dispatch"],
    "performance": ["cpu", "memory", "disk", "fps", "latency", "timeout"],
    "business_state": ["business", "popup", "login", "page changed"],
}

RECOMMENDATIONS = {
    "route_decision": "Fix receiver/HID/iPhone/bench metadata and clear open blockers. If this failure was recorded, start a fresh run_id before claiming P1 pass.",
    "airplay_discovery": "Check same VLAN, AP isolation, Bonjour/mDNS, firewall, receiver name conflicts.",
    "airplay_stream": "Record receiver component/version, retry with fixed network, and compare UxPlay vs Windows receiver route.",
    "capture": "Verify screenshot dimensions, non-black frames, crop area, and capture component logs.",
    "calibration": "Redo five-point calibration; record active area, target size, orientation, safe area, and pixel error.",
    "vision_template": "Replace low-texture templates, restrict region, record threshold and failure screenshot.",
    "vision_color": "Record RGB/tolerance/region; retest under fixed brightness and theme.",
    "ocr": "Check PaddleOCR import/cache/model download, then retest with cropped OCR region.",
    "hid": "Check HID serial discovery, firmware, baudrate, Hub power, OTG wiring, and iPhone pointer response.",
    "group_dispatch": "Confirm group membership, duplicate devices, per-device results, and single-device failure isolation.",
    "performance": "Compare CPU/memory/disk/network notes against AirPlay disconnects and screenshot/HID failures.",
    "business_state": "Capture the changed page state and update templates/flow guards before rerun.",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_token(value: str, fallback: str = "run") -> str:
    cleaned = _SAFE_TOKEN.sub("_", value.strip()).strip("._-")
    return (cleaned or fallback)[:80]


def make_run_id(prefix: str = "run") -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{safe_token(prefix)}_{stamp}"


def normalize_status(status: str) -> str:
    normalized = status.strip().lower()
    if normalized not in VALID_STATUSES:
        raise ValueError(f"Invalid validation status: {status}")
    return normalized


def normalize_device_ids(device_ids: Optional[str | Iterable[str]]) -> list[str]:
    if device_ids is None:
        return []
    if isinstance(device_ids, str):
        items = [device_ids]
    else:
        items = list(device_ids)
    seen = set()
    out = []
    for item in items:
        cleaned = str(item).strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        out.append(cleaned)
    return out


def json_safe(value: Any, *, string_limit: int = 2000) -> Any:
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        if len(value) > string_limit:
            return f"{value[:string_limit]}...<truncated {len(value) - string_limit} chars>"
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): json_safe(val, string_limit=string_limit) for key, val in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_safe(item, string_limit=string_limit) for item in value]
    return repr(value)


def flatten_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            parts.append(str(key))
            parts.append(flatten_text(item))
        return " ".join(parts)
    if isinstance(value, (list, tuple, set)):
        return " ".join(flatten_text(item) for item in value)
    return str(value)


def failure_category(event: dict) -> str:
    details = event.get("details", {})
    if isinstance(details, dict):
        for key in ("failure_category", "category", "error_type", "type"):
            value = details.get(key)
            if isinstance(value, str) and value.strip():
                return safe_token(value.strip().lower(), fallback="uncategorized")
    primary_text = f"{event.get('step', '')} {flatten_text(details)}".lower()
    for category, keywords in FAILURE_CATEGORY_KEYWORDS.items():
        if any(keyword in primary_text for keyword in keywords):
            return category
    text = f"{primary_text} {' '.join(event.get('artifacts', []))}".lower()
    for category, keywords in FAILURE_CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "uncategorized"


def metric_snapshot(event: dict) -> Optional[dict]:
    details = event.get("details", {})
    if not isinstance(details, dict):
        return None
    if not {"platform", "cpu", "memory", "disk"}.issubset(details.keys()):
        return None
    memory = details.get("memory") if isinstance(details.get("memory"), dict) else {}
    disk = details.get("disk") if isinstance(details.get("disk"), dict) else {}
    return {
        "ts": event.get("ts", ""),
        "step": event.get("step", ""),
        "label": details.get("label", ""),
        "memory_source": memory.get("source", ""),
        "memory_used_percent": memory.get("used_percent"),
        "process_rss_bytes": memory.get("process_rss_bytes"),
        "disk_used_percent": disk.get("used_percent"),
        "extra": details.get("extra", {}),
    }


def is_aggregate_failure(event: dict) -> bool:
    step = str(event.get("step", "")).strip().lower()
    if step == "scenario summary":
        return True
    details = event.get("details", {})
    if not isinstance(details, dict):
        return False
    return bool(details.get("results") or details.get("rounds"))


def _max_number(values: Iterable[Any]) -> Optional[float]:
    numbers = []
    for value in values:
        if isinstance(value, (int, float)):
            numbers.append(float(value))
    return max(numbers) if numbers else None


def summarize_metrics(events: list[dict]) -> dict:
    samples = [snapshot for event in events if (snapshot := metric_snapshot(event))]
    return {
        "count": len(samples),
        "latest": samples[-1] if samples else {},
        "max_memory_used_percent": _max_number(item.get("memory_used_percent") for item in samples),
        "max_disk_used_percent": _max_number(item.get("disk_used_percent") for item in samples),
        "max_process_rss_bytes": _max_number(item.get("process_rss_bytes") for item in samples),
        "samples": samples,
    }


def recommendations_for(summary: dict) -> list[str]:
    recommendations = []
    for category, count in summary.get("by_failure_category", {}).items():
        if count and category in RECOMMENDATIONS:
            recommendations.append(f"{category}: {RECOMMENDATIONS[category]}")
    metrics = summary.get("metrics", {})
    memory = metrics.get("max_memory_used_percent")
    disk = metrics.get("max_disk_used_percent")
    if isinstance(memory, (int, float)) and memory >= 85:
        recommendations.append("performance: Host memory pressure is high; reduce concurrent devices or investigate receiver leaks.")
    if isinstance(disk, (int, float)) and disk >= 90:
        recommendations.append("performance: Disk usage is high; rotate screenshots/evidence before long stability runs.")
    if not recommendations and summary.get("total", 0):
        recommendations.append("No failure category detected; verify real iPhone manual observations before promoting the run.")
    return recommendations


@dataclass
class ValidationRecorder:
    """Append-only evidence recorder.

    Each run writes one JSONL file. This keeps field evidence inspectable even if
    the GUI or server exits in the middle of a longer multi-device test.
    """

    run_id: str
    evidence_dir: Path | str = DEFAULT_EVIDENCE_DIR

    @property
    def safe_run_id(self) -> str:
        return safe_token(self.run_id)

    @property
    def path(self) -> Path:
        return Path(self.evidence_dir) / f"{self.safe_run_id}.jsonl"

    def append(
        self,
        step: str,
        status: str,
        *,
        device_ids: Optional[str | Iterable[str]] = None,
        details: Any = None,
        artifacts: Optional[Iterable[str | Path]] = None,
    ) -> dict:
        event = {
            "ts": now_utc(),
            "run_id": self.safe_run_id,
            "step": step.strip() or "unknown",
            "status": normalize_status(status),
            "device_ids": normalize_device_ids(device_ids),
            "details": json_safe(details or {}),
            "artifacts": [str(item) for item in (artifacts or [])],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False, sort_keys=True))
            fh.write("\n")
        return event

    def load(self) -> list[dict]:
        if not self.path.exists():
            return []
        events = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            events.append(json.loads(line))
        return events

    def summary(self) -> dict:
        events = self.load()
        by_status = {status: 0 for status in sorted(VALID_STATUSES)}
        by_device: dict[str, int] = {}
        by_failure_category: dict[str, int] = {}
        failures = []
        for event in events:
            status = event.get("status", "info")
            by_status[status] = by_status.get(status, 0) + 1
            for device_id in event.get("device_ids", []):
                by_device[device_id] = by_device.get(device_id, 0) + 1
            if status == "fail":
                if not is_aggregate_failure(event):
                    category = failure_category(event)
                    by_failure_category[category] = by_failure_category.get(category, 0) + 1
                failures.append(event)
        summary = {
            "run_id": self.safe_run_id,
            "path": str(self.path),
            "total": len(events),
            "by_status": by_status,
            "by_device": dict(sorted(by_device.items())),
            "by_failure_category": dict(sorted(by_failure_category.items())),
            "metrics": summarize_metrics(events),
            "failures": failures,
        }
        summary["recommendations"] = recommendations_for(summary)
        return summary

    def write_summary_markdown(self, path: Optional[str | Path] = None) -> Path:
        summary = self.summary()
        out_path = Path(path) if path else self.path.with_suffix(".md")
        lines = [
            f"# Validation Run {summary['run_id']}",
            "",
            f"- Evidence file: `{summary['path']}`",
            f"- Total events: {summary['total']}",
            "",
            "## Status Counts",
            "",
        ]
        for status, count in summary["by_status"].items():
            lines.append(f"- {status}: {count}")
        lines.extend(["", "## Device Event Counts", ""])
        if summary["by_device"]:
            for device_id, count in summary["by_device"].items():
                lines.append(f"- {device_id}: {count}")
        else:
            lines.append("- No device ids recorded")
        lines.extend(["", "## Failure Categories", ""])
        if summary["by_failure_category"]:
            for category, count in summary["by_failure_category"].items():
                lines.append(f"- {category}: {count}")
        else:
            lines.append("- No failure categories recorded")
        lines.extend(["", "## Metrics", ""])
        metrics = summary["metrics"]
        lines.append(f"- Samples: {metrics.get('count', 0)}")
        if metrics.get("latest"):
            latest = metrics["latest"]
            lines.append(f"- Latest label: {latest.get('label') or '-'}")
            lines.append(f"- Latest memory source: {latest.get('memory_source') or '-'}")
        for key, label in [
            ("max_memory_used_percent", "Max memory used percent"),
            ("max_disk_used_percent", "Max disk used percent"),
            ("max_process_rss_bytes", "Max process RSS bytes"),
        ]:
            value = metrics.get(key)
            lines.append(f"- {label}: {value if value is not None else '-'}")
        lines.extend(["", "## Failures", ""])
        if summary["failures"]:
            for event in summary["failures"]:
                devices = ", ".join(event.get("device_ids", [])) or "-"
                artifacts = ", ".join(event.get("artifacts", [])) or "-"
                category = failure_category(event)
                detail = event.get("details", {})
                lines.append(
                    f"- {event.get('ts')} | {event.get('step')} | category={category} | devices={devices} | artifacts={artifacts} | details={detail}"
                )
        else:
            lines.append("- No failures recorded")
        lines.extend(["", "## Recommendations", ""])
        if summary["recommendations"]:
            for item in summary["recommendations"]:
                lines.append(f"- {item}")
        else:
            lines.append("- No recommendations")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return out_path
