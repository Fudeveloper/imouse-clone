"""
CH9329 HID Keyboard & Mouse Controller.

CH9329 is a USB-HID chip from Nanjing Qinheng (沁恒) that emulates
a keyboard + absolute mouse over serial (UART).

Protocol frame:
    57 AB  ADDR  CMD  LEN  DATA...  SUM

ADDR: default 0x00
CMD:  0x02 = keyboard, 0x04 = absolute mouse, 0x05 = relative mouse + buttons
SUM:  (ADDR + CMD + LEN + sum(DATA)) & 0xFF
"""

from __future__ import annotations

import struct
import time
from dataclasses import dataclass, field
from typing import Optional

import serial
import serial.tools.list_ports

# ── Protocol Constants ──────────────────────────────────────────────────────

HEADER = bytes([0x57, 0xAB])
DEFAULT_ADDR = 0x00

CMD_KEYBOARD = 0x02
CMD_MOUSE_ABS = 0x04
CMD_MOUSE_REL = 0x05

# Screen coordinate range for absolute mouse
MAX_COORD = 4095

# ── USB HID Keyboard Code Map ────────────────────────────────────────────────

# Maps ASCII chars to (keycode, needs_shift)
_KEY_MAP: dict[str, tuple[int, bool]] = {
    # Lowercase letters
    "a": (0x04, False), "b": (0x05, False), "c": (0x06, False),
    "d": (0x07, False), "e": (0x08, False), "f": (0x09, False),
    "g": (0x0A, False), "h": (0x0B, False), "i": (0x0C, False),
    "j": (0x0D, False), "k": (0x0E, False), "l": (0x0F, False),
    "m": (0x10, False), "n": (0x11, False), "o": (0x12, False),
    "p": (0x13, False), "q": (0x14, False), "r": (0x15, False),
    "s": (0x16, False), "t": (0x17, False), "u": (0x18, False),
    "v": (0x19, False), "w": (0x1A, False), "x": (0x1B, False),
    "y": (0x1C, False), "z": (0x1D, False),
    # Numbers (unshifted)
    "1": (0x1E, False), "2": (0x1F, False), "3": (0x20, False),
    "4": (0x21, False), "5": (0x22, False), "6": (0x23, False),
    "7": (0x24, False), "8": (0x25, False), "9": (0x26, False),
    "0": (0x27, False),
    # Special chars (unshifted)
    " ": (0x2C, False), "-": (0x2D, False), "=": (0x2E, False),
    "[": (0x2F, False), "]": (0x30, False), "\\": (0x31, False),
    ";": (0x33, False), "'": (0x34, False), ",": (0x36, False),
    ".": (0x37, False), "/": (0x38, False), "`": (0x35, False),
    # Special chars (shifted)
    "!": (0x1E, True), "@": (0x1F, True), "#": (0x20, True),
    "$": (0x21, True), "%": (0x22, True), "^": (0x23, True),
    "&": (0x24, True), "*": (0x25, True), "(": (0x26, True),
    ")": (0x27, True), "_": (0x2D, True), "+": (0x2E, True),
    "{": (0x2F, True), "}": (0x30, True), "|": (0x31, True),
    ":": (0x33, True), '"': (0x34, True), "<": (0x36, True),
    ">": (0x37, True), "?": (0x38, True), "~": (0x35, True),
    # Control characters
    "\n": (0x28, False),  # Enter
    "\t": (0x2B, False),  # Tab
    "\b": (0x2A, False),  # Backspace
    "\x1b": (0x29, False),  # Escape
}

# Named keycodes
KEY_ENTER = 0x28
KEY_ESC = 0x29
KEY_BACKSPACE = 0x2A
KEY_TAB = 0x2B
KEY_SPACE = 0x2C
KEY_CAPS = 0x39
KEY_UP = 0x52
KEY_DOWN = 0x51
KEY_LEFT = 0x50
KEY_RIGHT = 0x4F
KEY_HOME = 0x4A
KEY_END = 0x4D
KEY_PAGEUP = 0x4B
KEY_PAGEDOWN = 0x4E
KEY_DELETE = 0x4C
KEY_INSERT = 0x49

# ── Modifier masks ───────────────────────────────────────────────────────────

MOD_LCTRL = 0x01
MOD_LSHIFT = 0x02
MOD_LALT = 0x04
MOD_LWIN = 0x08
MOD_RCTRL = 0x10
MOD_RSHIFT = 0x20
MOD_RALT = 0x40
MOD_RWIN = 0x80


def _checksum(data: bytes) -> int:
    """Compute CH9329 checksum: sum of all payload bytes, lower 8 bits."""
    return sum(data) & 0xFF


def _build_frame(addr: int, cmd: int, data: bytes) -> bytes:
    """Build a complete CH9329 frame."""
    payload = bytes([addr, cmd, len(data)]) + data
    return HEADER + payload + bytes([_checksum(payload)])


# ── Keyboard Helpers ─────────────────────────────────────────────────────────


def _char_to_key(c: str) -> tuple[int, int]:
    """Convert a character to (keycode, modifier). Raises KeyError if unmapped."""
    entry = _KEY_MAP.get(c)
    if entry is None:
        # Try uppercase by lowercasing + shift
        if c.isalpha() and c.isupper():
            lower = _KEY_MAP.get(c.lower())
            if lower:
                return (lower[0], MOD_LSHIFT)
        raise KeyError(f"No HID mapping for character: {c!r}")
    keycode, needs_shift = entry
    return (keycode, MOD_LSHIFT if needs_shift else 0x00)


# ── CH9329 Device Class ──────────────────────────────────────────────────────


@dataclass
class CH9329Device:
    """Represents one CH9329 chip connected via serial port."""

    port: str
    baudrate: int = 9600
    timeout: float = 0.5
    hardware_id: str = ""

    _ser: Optional[serial.Serial] = field(default=None, repr=False, init=False)

    # ── Lifecycle ─────────────────────────────────────────────────────────

    def open(self) -> None:
        """Open the serial connection."""
        if self._ser and self._ser.is_open:
            return
        self._ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )
        # Hardware ID defaults to serial port path
        if not self.hardware_id:
            self.hardware_id = self.port

    def close(self) -> None:
        """Close the serial connection."""
        if self._ser and self._ser.is_open:
            self._ser.close()
        self._ser = None

    @property
    def is_open(self) -> bool:
        return self._ser is not None and self._ser.is_open

    def _send(self, frame: bytes) -> None:
        """Send a raw frame to the device."""
        if not self._ser or not self._ser.is_open:
            raise ConnectionError(f"CH9329 on {self.port} is not open")
        self._ser.write(frame)
        self._ser.flush()

    # ── Keyboard operations ───────────────────────────────────────────────

    def key_press(self, keycode: int, modifier: int = 0x00) -> None:
        """Press a single key (with optional modifier)."""
        data = bytes([modifier, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00])
        self._send(_build_frame(DEFAULT_ADDR, CMD_KEYBOARD, data))

    def key_release(self) -> None:
        """Release all keys."""
        data = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self._send(_build_frame(DEFAULT_ADDR, CMD_KEYBOARD, data))

    def key_tap(self, keycode: int, modifier: int = 0x00, delay: float = 0.05) -> None:
        """Press and release a single key."""
        self.key_press(keycode, modifier)
        time.sleep(delay)
        self.key_release()
        time.sleep(delay)

    def combo(self, keys: list[int], modifiers: int = 0x00, delay: float = 0.05) -> None:
        """Press a combination of keys simultaneously (e.g. Ctrl+C)."""
        padded = (keys + [0x00] * 6)[:6]
        data = bytes([modifiers, 0x00]) + bytes(padded)
        self._send(_build_frame(DEFAULT_ADDR, CMD_KEYBOARD, data))
        time.sleep(delay)
        # Release
        self._send(_build_frame(DEFAULT_ADDR, CMD_KEYBOARD, bytes(8)))

    def type_text(self, text: str, char_delay: float = 0.02) -> None:
        """Type a string character by character."""
        for c in text:
            if c.isalpha() and c.isupper():
                # Send as shift + lowercase
                lower = _KEY_MAP[c.lower()]
                self.key_tap(lower[0], MOD_LSHIFT, char_delay)
            else:
                keycode, modifier = _char_to_key(c)
                self.key_tap(keycode, modifier, char_delay)

    # ── Mouse operations ──────────────────────────────────────────────────

    def mouse_move_abs(self, x: int, y: int, width: int = MAX_COORD,
                       height: int = MAX_COORD) -> None:
        """Move mouse to absolute coordinates. (x, y) in pixel space,
        mapped to the CH9329 0-4095 coordinate range."""
        chip_x = int(x / width * MAX_COORD) if width > 0 else 0
        chip_y = int(y / height * MAX_COORD) if height > 0 else 0
        chip_x = max(0, min(MAX_COORD, chip_x))
        chip_y = max(0, min(MAX_COORD, chip_y))

        data = bytes([
            0x02,                       # Absolute mouse mode
            chip_x & 0xFF,              # X low
            (chip_x >> 8) & 0xFF,       # X high
            chip_y & 0xFF,              # Y low
            (chip_y >> 8) & 0xFF,       # Y high
            0x00,                       # Wheel
            0x00,                       # Reserved
        ])
        self._send(_build_frame(DEFAULT_ADDR, CMD_MOUSE_ABS, data))

    def mouse_click(self, button: int = 0x01, delay: float = 0.05) -> None:
        """Click a mouse button. 0x01=left, 0x02=right, 0x04=middle."""
        # Press
        self._send(_build_frame(DEFAULT_ADDR, CMD_MOUSE_REL,
                                bytes([button, 0x00, 0x00, 0x00, 0x00])))
        time.sleep(delay)
        # Release
        self._send(_build_frame(DEFAULT_ADDR, CMD_MOUSE_REL,
                                bytes([0x00, 0x00, 0x00, 0x00, 0x00])))
        time.sleep(delay)

    def mouse_down(self, button: int = 0x01) -> None:
        """Press and hold a mouse button."""
        self._send(_build_frame(DEFAULT_ADDR, CMD_MOUSE_REL,
                                bytes([button, 0x00, 0x00, 0x00, 0x00])))

    def mouse_up(self) -> None:
        """Release all mouse buttons."""
        self._send(_build_frame(DEFAULT_ADDR, CMD_MOUSE_REL,
                                bytes([0x00, 0x00, 0x00, 0x00, 0x00])))

    def mouse_scroll(self, amount: int) -> None:
        """Scroll. Positive = up, negative = down."""
        wheel = max(0x01, min(0x7F, amount)) if amount > 0 else \
                max(0x81, min(0xFF, 0x100 + amount))
        self._send(_build_frame(DEFAULT_ADDR, CMD_MOUSE_REL,
                                bytes([0x00, 0x00, 0x00, wheel, 0x00])))

    def swipe(self, x1: int, y1: int, x2: int, y2: int,
              steps: int = 20, step_delay: float = 0.01,
              width: int = MAX_COORD, height: int = MAX_COORD) -> None:
        """Swipe gesture from (x1, y1) to (x2, y2)."""
        self.mouse_down(0x01)
        for i in range(steps + 1):
            t = i / steps
            x = int(x1 + (x2 - x1) * t)
            y = int(y1 + (y2 - y1) * t)
            self.mouse_move_abs(x, y, width, height)
            time.sleep(step_delay)
        self.mouse_up()

    def click_at(self, x: int, y: int, width: int = MAX_COORD,
                 height: int = MAX_COORD, delay: float = 0.05) -> None:
        """Move to (x, y) and left-click."""
        self.mouse_move_abs(x, y, width, height)
        time.sleep(delay)
        self.mouse_click(0x01, delay)


# ── Device Discovery ─────────────────────────────────────────────────────────


def list_devices() -> list[dict]:
    """Scan serial ports for potential CH9329 devices.

    CH9329 typically appears as a USB CDC-ACM device.
    Returns list of {port, description, hwid} for each candidate.
    """
    candidates = []
    for port in serial.tools.list_ports.comports():
        # CH9329 uses USB VID: 0x1A86 (Qinheng)
        # But the VID may vary; include all CDC devices
        candidates.append({
            "port": port.device,
            "description": port.description,
            "hwid": port.hwid,
        })
    return candidates


def create_device(port: str, baudrate: int = 9600) -> CH9329Device:
    """Factory: create and open a CH9329 device."""
    dev = CH9329Device(port=port, baudrate=baudrate)
    dev.open()
    return dev
