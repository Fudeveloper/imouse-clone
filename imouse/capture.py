"""
Screen capture from AirPlay mirroring window / display.

Two backends:
  - mss (fast, cross-platform, recommended)
  - PIL ImageGrab (fallback)

Each AirPlay session renders to its own X11 display (or window on Windows/macOS).
We capture the full screen of that display at the iPhone's native resolution.
"""

from __future__ import annotations

import io
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image


# ── Screenshot backends ──────────────────────────────────────────────────────


def _capture_mss(display: str = ":99", monitor: int = 0) -> Image.Image:
    """Capture using mss (fast, works on X11/Wayland/Windows/macOS)."""
    import mss
    with mss.mss(display=display.encode() if display else None) as sct:
        monitor = sct.monitors[monitor]
        img_data = sct.grab(monitor)
        return Image.frombytes("RGB", img_data.size, img_data.rgb)


def _capture_pil() -> Image.Image:
    """Capture using PIL ImageGrab (fallback)."""
    from PIL import ImageGrab
    return ImageGrab.grab()


def _capture_x11_import(display: str = ":99") -> Image.Image:
    """Capture using ImageMagick `import` command (X11 only)."""
    import subprocess
    env = os.environ.copy()
    env["DISPLAY"] = display
    proc = subprocess.run(
        ["import", "-window", "root", "png:-"],
        env=env, capture_output=True, timeout=5,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"import failed: {proc.stderr.decode()}")
    return Image.open(io.BytesIO(proc.stdout))


def screenshot(display: str = ":99", backend: str = "mss") -> Image.Image:
    """Take a screenshot of the given X11 display.

    Args:
        display: X11 display string (e.g., ":99").
        backend: "mss" (default), "pil", or "x11".

    Returns:
        PIL Image in RGB mode.
    """
    if backend == "mss":
        try:
            return _capture_mss(display)
        except ImportError:
            pass
    if backend == "pil":
        try:
            return _capture_pil()
        except Exception:
            pass
    # Fallback to X11 import
    return _capture_x11_import(display)


# ── Capture Engine ───────────────────────────────────────────────────────────


class CaptureEngine:
    """Periodically captures screenshots from an AirPlay display.

    Maintains a ring of recent frames for vision operations.
    """

    def __init__(self, display: str = ":99", save_dir: Optional[str] = None):
        self.display = display
        self.save_dir = Path(save_dir) if save_dir else Path("screenshots")
        self._last_frame: Optional[Image.Image] = None
        self._last_time: float = 0.0
        self._frame_count: int = 0

    def capture(self, save: bool = False, label: str = "") -> Image.Image:
        """Take one screenshot.

        Returns:
            PIL Image in RGB (also stored as self._last_frame).
        """
        img = screenshot(self.display)
        self._last_frame = img
        self._last_time = time.time()
        self._frame_count += 1

        if save:
            self.save_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            name = f"{label}_{ts}" if label else ts
            img.save(self.save_dir / f"{name}.png")

        return img

    @property
    def last_frame(self) -> Optional[Image.Image]:
        return self._last_frame

    @property
    def last_frame_np(self) -> Optional[np.ndarray]:
        """Return last frame as a numpy BGR array (OpenCV format)."""
        if self._last_frame is None:
            return None
        return np.array(self._last_frame)[:, :, ::-1].copy()  # RGB → BGR

    def capture_np(self) -> np.ndarray:
        """Capture and return as numpy BGR array (OpenCV format)."""
        img = self.capture()
        return np.array(img)[:, :, ::-1].copy()
