"""
Device lifecycle manager.

Tracks the full chain:
  hardware_id (CH9329 serial port) → iPhone → AirPlay session

Manages device registration, binding, state transitions, and health checks.
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

from . import hardware as hw
from .airplay import AirPlaySession
from .calibration import CalibrationProfile
from .capture import CaptureEngine

if TYPE_CHECKING:
    from PIL.Image import Image


PROFILE_EXCLUDED_KEYS = {"device_id", "id", "fun", "msgid", "manual"}
PROFILE_STRING_KEYS = {
    "receiver_provider",
    "capture_provider",
    "capture_method",
    "hid_provider",
    "hid_id",
    "serial_port",
    "hardware_id",
    "iphone_id",
    "iphone",
    "iphone_model",
    "iphone_name",
    "ios_version",
    "ios",
    "receiver_name",
    "receiver_version",
    "capture_device",
    "capture_window",
    "capture_display",
    "firmware_version",
    "hub_port",
    "cable_id",
    "notes",
}


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {
            str(key): _jsonable(item)
            for key, item in value.items()
            if str(key).strip()
        }
    return str(value)


def normalize_device_profile(profile_data: dict[str, Any]) -> dict[str, Any]:
    """Return a JSON-safe, stable hardware/iOS traceability profile."""
    if not isinstance(profile_data, dict):
        raise ValueError("profile must be a dict")
    source: dict[str, Any] = dict(profile_data)
    for nested_key in ("profile", "metadata", "component_metadata"):
        nested = source.get(nested_key)
        if isinstance(nested, dict):
            source = dict(nested)
            break

    cleaned: dict[str, Any] = {}
    for key, value in source.items():
        key_text = str(key).strip()
        if not key_text or key_text in PROFILE_EXCLUDED_KEYS:
            continue
        if key_text in PROFILE_STRING_KEYS:
            cleaned[key_text] = "" if value is None else str(value).strip()
        else:
            cleaned[key_text] = _jsonable(value)

    if cleaned.get("ios") and not cleaned.get("ios_version"):
        cleaned["ios_version"] = str(cleaned["ios"]).strip()
    if cleaned.get("port") and not cleaned.get("serial_port"):
        cleaned["serial_port"] = str(cleaned["port"]).strip()
    return cleaned


class DeviceState(Enum):
    OFFLINE = "offline"           # Hardware not connected
    ONLINE = "online"             # Hardware connected, no iPhone
    PHONE_CONNECTED = "phone_connected"   # OTG cable detected
    AIRPLAY_CONNECTED = "airplay_connected"  # iPhone mirroring
    CAPTURING = "capturing"       # Actively taking screenshots
    WORKING = "working"           # Receiving commands
    ERROR = "error"


@dataclass
class Device:
    """One iPhone under control."""

    device_id: str
    hardware_id: str = ""         # CH9329 serial port path
    hardware: Optional[hw.CH9329Device] = None
    airplay: Optional[AirPlaySession] = None
    capture: Optional[CaptureEngine] = None
    state: DeviceState = DeviceState.OFFLINE

    # Screen dimensions (set when AirPlay connects)
    screen_width: int = 0
    screen_height: int = 0
    calibration: CalibrationProfile = field(default_factory=CalibrationProfile)

    # Metadata
    iphone_name: str = ""
    ios_version: str = ""
    profile: dict[str, Any] = field(default_factory=dict)

    # Runtime stats
    _error_count: int = 0
    _last_heartbeat: float = field(default_factory=time.time)

    # ── Lifecycle ─────────────────────────────────────────────────────────

    def bind_hardware(self, port: str, baudrate: int = 9600) -> None:
        """Bind a CH9329 hardware device."""
        self.hardware_id = port
        self.hardware = hw.create_device(port, baudrate)
        self.state = DeviceState.ONLINE

    def unbind_hardware(self) -> None:
        """Release hardware."""
        if self.hardware:
            self.hardware.close()
            self.hardware = None
        self.hardware_id = ""
        self.state = DeviceState.OFFLINE

    def start_airplay(self, display: str = ":99", fps: int = 30) -> None:
        """Start AirPlay receiver."""
        if not self.airplay:
            self.airplay = AirPlaySession(
                device_id=self.device_id,
                display=display,
                fps=fps,
            )
        self.airplay.start(device_name=f"iMouse-{self.device_id}")
        self.state = DeviceState.AIRPLAY_CONNECTED

    def stop_airplay(self) -> None:
        """Stop AirPlay receiver."""
        if self.airplay:
            self.airplay.stop()
        if self.capture:
            self.capture = None
        self.state = DeviceState.PHONE_CONNECTED if self.hardware else DeviceState.ONLINE

    def start_capture(self, display: str = ":99") -> None:
        """Begin screenshot capture loop."""
        if not self.capture:
            self.capture = CaptureEngine(display=display)
        # Take initial frame
        img = self.capture.capture()
        self.screen_width = img.width
        self.screen_height = img.height
        self.state = DeviceState.CAPTURING

    def capture_frame(self) -> "Image":
        """Take a single screenshot. Updates state."""
        if not self.capture:
            raise RuntimeError(f"Device {self.device_id}: capture not started")
        img = self.capture.capture()
        self.state = DeviceState.CAPTURING
        return img

    # ── High-level Operations ──────────────────────────────────────────────

    def click(self, x: int, y: int) -> None:
        """Click at screen coordinates."""
        if not self.hardware or not self.hardware.is_open:
            raise ConnectionError(f"Device {self.device_id} hardware not connected")
        if self.calibration.enabled:
            mapped_x, mapped_y, width, height = self.calibration.map_point(
                x,
                y,
                clamp=True,
            )
        else:
            mapped_x = x
            mapped_y = y
            width = self.screen_width or hw.MAX_COORD
            height = self.screen_height or hw.MAX_COORD
        self.hardware.click_at(mapped_x, mapped_y, width, height)

    def swipe(self, x1: int, y1: int, x2: int, y2: int,
              steps: int = 20, step_delay: float = 0.01) -> None:
        """Swipe gesture."""
        if not self.hardware or not self.hardware.is_open:
            raise ConnectionError(f"Device {self.device_id} hardware not connected")
        if self.calibration.enabled:
            mapped_x1, mapped_y1, width, height = self.calibration.map_point(
                x1,
                y1,
                clamp=True,
            )
            mapped_x2, mapped_y2, width2, height2 = self.calibration.map_point(
                x2,
                y2,
                clamp=True,
            )
            width = max(width, width2)
            height = max(height, height2)
        else:
            mapped_x1, mapped_y1 = x1, y1
            mapped_x2, mapped_y2 = x2, y2
            width = self.screen_width or hw.MAX_COORD
            height = self.screen_height or hw.MAX_COORD
        self.hardware.swipe(mapped_x1, mapped_y1, mapped_x2, mapped_y2,
                            steps, step_delay, width, height)

    def type_text(self, text: str, char_delay: float = 0.02) -> None:
        """Type text via hardware keyboard."""
        if not self.hardware or not self.hardware.is_open:
            raise ConnectionError(f"Device {self.device_id} hardware not connected")
        self.hardware.type_text(text, char_delay)

    def key_tap(self, keycode: int, modifier: int = 0x00) -> None:
        """Tap a specific key."""
        if not self.hardware or not self.hardware.is_open:
            raise ConnectionError(f"Device {self.device_id} hardware not connected")
        self.hardware.key_tap(keycode, modifier)

    def key_combo(self, keys: list[int], modifiers: int = 0x00) -> None:
        """Press key combination."""
        if not self.hardware or not self.hardware.is_open:
            raise ConnectionError(f"Device {self.device_id} hardware not connected")
        self.hardware.combo(keys, modifiers)

    # ── Health ────────────────────────────────────────────────────────────

    def heartbeat(self) -> bool:
        """Check if device is responsive."""
        self._last_heartbeat = time.time()
        if not self.hardware or not self.hardware.is_open:
            self.state = DeviceState.OFFLINE
            return False
        return True

    @property
    def is_ready(self) -> bool:
        return self.state in (DeviceState.CAPTURING, DeviceState.WORKING)

    def apply_profile(self, profile_data: dict[str, Any]) -> None:
        profile = normalize_device_profile(profile_data)
        self.profile = profile
        iphone_name = profile.get("iphone_name") or profile.get("iphone") or profile.get("iphone_id")
        if iphone_name:
            self.iphone_name = str(iphone_name)
        ios_version = profile.get("ios_version") or profile.get("ios")
        if ios_version:
            self.ios_version = str(ios_version)

    def profile_for_status(self) -> dict[str, Any]:
        profile = dict(self.profile)
        if self.hardware_id and not profile.get("serial_port"):
            profile["serial_port"] = self.hardware_id
        if self.iphone_name and not profile.get("iphone_name"):
            profile["iphone_name"] = self.iphone_name
        if self.ios_version and not profile.get("ios_version"):
            profile["ios_version"] = self.ios_version
        return profile


# ── Device Manager ───────────────────────────────────────────────────────────


class DeviceManager:
    """Singleton registry of all controlled devices."""

    def __init__(
        self,
        group_store_path: Optional[str] = "state/groups.json",
        calibration_store_path: Optional[str] = "state/calibration.json",
        profile_store_path: Optional[str] = "state/device_profiles.json",
    ):
        self._devices: dict[str, Device] = {}
        self._groups: dict[str, list[str]] = {}
        self._saved_calibrations: dict[str, CalibrationProfile] = {}
        self._saved_profiles: dict[str, dict[str, Any]] = {}
        self._group_store_path = Path(group_store_path) if group_store_path else None
        self._calibration_store_path = Path(calibration_store_path) if calibration_store_path else None
        self._profile_store_path = Path(profile_store_path) if profile_store_path else None
        self._lock = threading.Lock()
        self._load_groups()
        self._load_calibrations()
        self._load_profiles()

    # ── CRUD ───────────────────────────────────────────────────────────────

    def register(self, device_id: str) -> Device:
        """Create a new device entry."""
        with self._lock:
            if device_id in self._devices:
                raise ValueError(f"Device {device_id} already registered")
            dev = Device(device_id=device_id)
            if device_id in self._saved_calibrations:
                dev.calibration = self._saved_calibrations[device_id]
            if device_id in self._saved_profiles:
                dev.apply_profile(self._saved_profiles[device_id])
            self._devices[device_id] = dev
            return dev

    def get(self, device_id: str) -> Device:
        """Get a device by ID."""
        with self._lock:
            if device_id not in self._devices:
                raise KeyError(f"Device {device_id} not found")
            return self._devices[device_id]

    def list_all(self) -> list[Device]:
        """Return all devices."""
        with self._lock:
            return list(self._devices.values())

    def remove(self, device_id: str) -> None:
        """Remove and shut down a device."""
        with self._lock:
            dev = self._devices.pop(device_id, None)
        if dev:
            dev.unbind_hardware()
            dev.stop_airplay()

    # ── Groups ────────────────────────────────────────────────────────────

    def _load_groups(self) -> None:
        if not self._group_store_path or not self._group_store_path.exists():
            return
        try:
            raw = json.loads(self._group_store_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        groups = raw.get("groups", raw) if isinstance(raw, dict) else {}
        if not isinstance(groups, dict):
            return
        cleaned: dict[str, list[str]] = {}
        for name, ids in groups.items():
            if not isinstance(ids, list):
                continue
            cleaned[str(name)] = self._dedupe_ids([str(item) for item in ids])
        self._groups = cleaned

    def _save_groups(self) -> None:
        if not self._group_store_path:
            return
        self._group_store_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"groups": self._groups}
        self._group_store_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _dedupe_ids(self, device_ids: list[str]) -> list[str]:
        seen = set()
        out = []
        for device_id in device_ids:
            cleaned = str(device_id).strip()
            if not cleaned or cleaned in seen:
                continue
            seen.add(cleaned)
            out.append(cleaned)
        return out

    def list_groups(self) -> list[dict]:
        with self._lock:
            return [
                {"name": name, "device_ids": list(device_ids), "count": len(device_ids)}
                for name, device_ids in sorted(self._groups.items())
            ]

    def get_group(self, name: str) -> list[str]:
        cleaned_name = name.strip()
        with self._lock:
            if cleaned_name not in self._groups:
                raise KeyError(f"Group {cleaned_name} not found")
            return list(self._groups[cleaned_name])

    def set_group(self, name: str, device_ids: list[str]) -> dict:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Group name is required")
        cleaned_ids = self._dedupe_ids(device_ids)
        with self._lock:
            self._groups[cleaned_name] = cleaned_ids
            self._save_groups()
        return {"name": cleaned_name, "device_ids": cleaned_ids, "count": len(cleaned_ids)}

    def remove_group(self, name: str) -> bool:
        cleaned_name = name.strip()
        with self._lock:
            existed = cleaned_name in self._groups
            self._groups.pop(cleaned_name, None)
            if existed:
                self._save_groups()
        return existed

    # ── Calibration ───────────────────────────────────────────────────────

    def _load_calibrations(self) -> None:
        if not self._calibration_store_path or not self._calibration_store_path.exists():
            return
        try:
            raw = json.loads(self._calibration_store_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        entries = raw.get("devices", raw) if isinstance(raw, dict) else {}
        if not isinstance(entries, dict):
            return
        loaded: dict[str, CalibrationProfile] = {}
        for device_id, profile in entries.items():
            if isinstance(profile, dict):
                loaded[str(device_id)] = CalibrationProfile.from_dict(profile)
        self._saved_calibrations = loaded

    def _save_calibrations(self) -> None:
        if not self._calibration_store_path:
            return
        self._calibration_store_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "devices": {
                device_id: profile.to_dict()
                for device_id, profile in sorted(self._saved_calibrations.items())
            }
        }
        self._calibration_store_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def get_calibration(self, device_id: str) -> dict:
        with self._lock:
            if device_id in self._devices:
                return self._devices[device_id].calibration.to_dict()
            if device_id in self._saved_calibrations:
                return self._saved_calibrations[device_id].to_dict()
            raise KeyError(f"Calibration for {device_id} not found")

    def set_calibration(self, device_id: str, profile_data: dict) -> dict:
        profile = CalibrationProfile.from_dict(profile_data)
        with self._lock:
            self._saved_calibrations[device_id] = profile
            if device_id in self._devices:
                self._devices[device_id].calibration = profile
            self._save_calibrations()
        return {"device_id": device_id, "calibration": profile.to_dict()}

    def list_calibrations(self) -> list[dict]:
        with self._lock:
            rows = []
            keys = sorted(set(self._saved_calibrations) | set(self._devices))
            for device_id in keys:
                if device_id in self._devices:
                    profile = self._devices[device_id].calibration
                else:
                    profile = self._saved_calibrations[device_id]
                rows.append({"device_id": device_id, "calibration": profile.to_dict()})
            return rows

    # Device Profiles

    def _load_profiles(self) -> None:
        if not self._profile_store_path or not self._profile_store_path.exists():
            return
        try:
            raw = json.loads(self._profile_store_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        entries = raw.get("devices", raw) if isinstance(raw, dict) else {}
        if not isinstance(entries, dict):
            return
        loaded: dict[str, dict[str, Any]] = {}
        for device_id, profile in entries.items():
            if isinstance(profile, dict):
                loaded[str(device_id)] = normalize_device_profile(profile)
        self._saved_profiles = loaded

    def _save_profiles(self) -> None:
        if not self._profile_store_path:
            return
        self._profile_store_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "devices": {
                device_id: dict(profile)
                for device_id, profile in sorted(self._saved_profiles.items())
            }
        }
        self._profile_store_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def get_profile(self, device_id: str) -> dict[str, Any]:
        with self._lock:
            if device_id in self._devices:
                return self._devices[device_id].profile_for_status()
            if device_id in self._saved_profiles:
                return dict(self._saved_profiles[device_id])
            raise KeyError(f"Profile for {device_id} not found")

    def set_profile(self, device_id: str, profile_data: dict[str, Any],
                    merge: bool = True) -> dict[str, Any]:
        cleaned = normalize_device_profile(profile_data)
        with self._lock:
            current = dict(self._saved_profiles.get(device_id, {})) if merge else {}
            current.update(cleaned)
            self._saved_profiles[device_id] = current
            if device_id in self._devices:
                self._devices[device_id].apply_profile(current)
            self._save_profiles()
        return {"device_id": device_id, "profile": dict(current)}

    def list_profiles(self) -> list[dict[str, Any]]:
        with self._lock:
            rows = []
            keys = sorted(set(self._saved_profiles) | set(self._devices))
            for device_id in keys:
                if device_id in self._devices:
                    profile = self._devices[device_id].profile_for_status()
                else:
                    profile = dict(self._saved_profiles[device_id])
                rows.append({"device_id": device_id, "profile": profile})
            return rows

    # ── Discovery ──────────────────────────────────────────────────────────

    def scan_hardware(self) -> list[dict]:
        """Scan for available CH9329 devices."""
        return hw.list_devices()

    def auto_assign(self, device_id: str) -> Optional[str]:
        """Auto-assign the first available CH9329 to a device."""
        candidates = self.scan_hardware()
        if not candidates:
            return None
        # Pick first unassigned port
        assigned = {d.hardware_id for d in self._devices.values()}
        for c in candidates:
            if c["port"] not in assigned:
                dev = self.get(device_id)
                dev.bind_hardware(c["port"])
                return c["port"]
        return None

    # ── State Dump ─────────────────────────────────────────────────────────

    def status_all(self) -> list[dict]:
        """Return JSON-serializable status for all devices."""
        rows = []
        for d in self._devices.values():
            profile = d.profile_for_status()
            rows.append({
                "device_id": d.device_id,
                "hardware_id": d.hardware_id,
                "state": d.state.value,
                "iphone_name": d.iphone_name or str(profile.get("iphone_id", "")),
                "ios_version": d.ios_version or str(profile.get("ios_version", "")),
                "screen_width": d.screen_width,
                "screen_height": d.screen_height,
                "calibration": d.calibration.to_dict(),
                "profile": profile,
                "component_metadata": profile,
                "receiver_provider": profile.get("receiver_provider", ""),
                "capture_provider": profile.get("capture_provider", ""),
                "capture_method": profile.get("capture_method", ""),
                "hid_provider": profile.get("hid_provider", ""),
                "hid_id": profile.get("hid_id", ""),
                "serial_port": profile.get("serial_port", ""),
                "iphone_id": profile.get("iphone_id", ""),
                "last_heartbeat": d._last_heartbeat,
                "error_count": d._error_count,
            })
        return rows


# ── Global Singleton ─────────────────────────────────────────────────────────

_manager: Optional[DeviceManager] = None


def get_manager() -> DeviceManager:
    global _manager
    if _manager is None:
        _manager = DeviceManager()
    return _manager
