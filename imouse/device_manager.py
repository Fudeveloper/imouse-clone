"""
Device lifecycle manager.

Tracks the full chain:
  hardware_id (CH9329 serial port) → iPhone → AirPlay session

Manages device registration, binding, state transitions, and health checks.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Optional

from . import hardware as hw
from .airplay import AirPlaySession
from .capture import CaptureEngine

if TYPE_CHECKING:
    from PIL.Image import Image


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

    # Metadata
    iphone_name: str = ""
    ios_version: str = ""

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
        self.hardware.click_at(x, y, self.screen_width or hw.MAX_COORD,
                               self.screen_height or hw.MAX_COORD)

    def swipe(self, x1: int, y1: int, x2: int, y2: int,
              steps: int = 20, step_delay: float = 0.01) -> None:
        """Swipe gesture."""
        if not self.hardware or not self.hardware.is_open:
            raise ConnectionError(f"Device {self.device_id} hardware not connected")
        self.hardware.swipe(x1, y1, x2, y2, steps, step_delay,
                            self.screen_width or hw.MAX_COORD,
                            self.screen_height or hw.MAX_COORD)

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


# ── Device Manager ───────────────────────────────────────────────────────────


class DeviceManager:
    """Singleton registry of all controlled devices."""

    def __init__(self):
        self._devices: dict[str, Device] = {}
        self._lock = threading.Lock()

    # ── CRUD ───────────────────────────────────────────────────────────────

    def register(self, device_id: str) -> Device:
        """Create a new device entry."""
        with self._lock:
            if device_id in self._devices:
                raise ValueError(f"Device {device_id} already registered")
            dev = Device(device_id=device_id)
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
        return [
            {
                "device_id": d.device_id,
                "hardware_id": d.hardware_id,
                "state": d.state.value,
                "iphone_name": d.iphone_name,
                "screen_width": d.screen_width,
                "screen_height": d.screen_height,
                "last_heartbeat": d._last_heartbeat,
                "error_count": d._error_count,
            }
            for d in self._devices.values()
        ]


# ── Global Singleton ─────────────────────────────────────────────────────────

_manager: Optional[DeviceManager] = None


def get_manager() -> DeviceManager:
    global _manager
    if _manager is None:
        _manager = DeviceManager()
    return _manager
