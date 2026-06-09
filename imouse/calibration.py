"""Coordinate calibration helpers for iOS screen control."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def _now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _positive_int(value: Any, fallback: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return fallback
    return parsed if parsed > 0 else fallback


def _non_negative_int(value: Any, fallback: int = 0) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return fallback
    return parsed if parsed >= 0 else fallback


@dataclass
class CalibrationProfile:
    """Map screenshot coordinates to the HID coordinate space for one device."""

    enabled: bool = False
    source_width: int = 0
    source_height: int = 0
    active_x: int = 0
    active_y: int = 0
    active_width: int = 0
    active_height: int = 0
    target_width: int = 0
    target_height: int = 0
    safe_left: int = 0
    safe_top: int = 0
    safe_right: int = 0
    safe_bottom: int = 0
    orientation: str = "portrait"
    notes: str = ""
    updated_at: str = field(default_factory=_now_utc)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "CalibrationProfile":
        profile = cls(
            enabled=bool(raw.get("enabled", False)),
            source_width=_non_negative_int(raw.get("source_width", 0)),
            source_height=_non_negative_int(raw.get("source_height", 0)),
            active_x=_non_negative_int(raw.get("active_x", 0)),
            active_y=_non_negative_int(raw.get("active_y", 0)),
            active_width=_non_negative_int(raw.get("active_width", 0)),
            active_height=_non_negative_int(raw.get("active_height", 0)),
            target_width=_non_negative_int(raw.get("target_width", 0)),
            target_height=_non_negative_int(raw.get("target_height", 0)),
            safe_left=_non_negative_int(raw.get("safe_left", 0)),
            safe_top=_non_negative_int(raw.get("safe_top", 0)),
            safe_right=_non_negative_int(raw.get("safe_right", 0)),
            safe_bottom=_non_negative_int(raw.get("safe_bottom", 0)),
            orientation=str(raw.get("orientation", "portrait") or "portrait"),
            notes=str(raw.get("notes", "") or ""),
            updated_at=str(raw.get("updated_at", "") or _now_utc()),
        )
        return profile.normalized()

    @classmethod
    def from_screen(cls, width: int, height: int, *, enabled: bool = True) -> "CalibrationProfile":
        width = _positive_int(width, 1)
        height = _positive_int(height, 1)
        return cls(
            enabled=enabled,
            source_width=width,
            source_height=height,
            active_width=width,
            active_height=height,
            target_width=width,
            target_height=height,
            updated_at=_now_utc(),
        )

    def normalized(self) -> "CalibrationProfile":
        source_width = _positive_int(self.source_width, self.active_width or self.target_width or 1)
        source_height = _positive_int(self.source_height, self.active_height or self.target_height or 1)
        active_width = _positive_int(self.active_width, source_width)
        active_height = _positive_int(self.active_height, source_height)
        active_x = max(0, min(_non_negative_int(self.active_x), source_width - 1))
        active_y = max(0, min(_non_negative_int(self.active_y), source_height - 1))
        active_width = min(active_width, max(1, source_width - active_x))
        active_height = min(active_height, max(1, source_height - active_y))
        target_width = _positive_int(self.target_width, active_width)
        target_height = _positive_int(self.target_height, active_height)
        return CalibrationProfile(
            enabled=bool(self.enabled),
            source_width=source_width,
            source_height=source_height,
            active_x=active_x,
            active_y=active_y,
            active_width=active_width,
            active_height=active_height,
            target_width=target_width,
            target_height=target_height,
            safe_left=min(_non_negative_int(self.safe_left), target_width),
            safe_top=min(_non_negative_int(self.safe_top), target_height),
            safe_right=min(_non_negative_int(self.safe_right), target_width),
            safe_bottom=min(_non_negative_int(self.safe_bottom), target_height),
            orientation=str(self.orientation or "portrait"),
            notes=str(self.notes or ""),
            updated_at=str(self.updated_at or _now_utc()),
        )

    def to_dict(self) -> dict:
        return asdict(self.normalized())

    def map_point(self, x: int, y: int, *, clamp: bool = True,
                  safe_area: bool = False) -> tuple[int, int, int, int]:
        """Return mapped x/y plus target width/height for hardware scaling."""
        profile = self.normalized()
        if not profile.enabled:
            width = profile.source_width or profile.target_width
            height = profile.source_height or profile.target_height
            return int(x), int(y), width, height

        local_x = int(x) - profile.active_x
        local_y = int(y) - profile.active_y
        if clamp:
            local_x = max(0, min(profile.active_width, local_x))
            local_y = max(0, min(profile.active_height, local_y))
        elif not (0 <= local_x <= profile.active_width and 0 <= local_y <= profile.active_height):
            raise ValueError(f"Point ({x}, {y}) is outside calibration active area")

        target_x = round(local_x / profile.active_width * profile.target_width)
        target_y = round(local_y / profile.active_height * profile.target_height)

        if safe_area:
            min_x = profile.safe_left
            max_x = max(min_x, profile.target_width - profile.safe_right)
            min_y = profile.safe_top
            max_y = max(min_y, profile.target_height - profile.safe_bottom)
            target_x = max(min_x, min(max_x, target_x))
            target_y = max(min_y, min(max_y, target_y))

        return int(target_x), int(target_y), profile.target_width, profile.target_height
