"""
AirPlay screen-mirroring receiver via UxPlay subprocess.

UxPlay (https://github.com/FDH2/UxPlay) is an open-source AirPlay
mirroring server. We spawn one UxPlay instance per iPhone to receive
its screen stream, then capture frames from the rendered window.

Alternatives: pyairplay (pure Python, less mature), RPiPlay.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class AirPlaySession:
    """Manages one UxPlay instance tied to one iPhone."""

    device_id: str
    display: str = ":99"     # X11 display for this session
    width: int = 0
    height: int = 0
    fps: int = 30
    uxplay_bin: str = "uxplay"

    _process: Optional[subprocess.Popen] = None

    # ── Lifecycle ─────────────────────────────────────────────────────────

    def start(self, device_name: str = "iMouse", pin: str = "") -> None:
        """Launch UxPlay for this session.

        Args:
            device_name: AirPlay server name shown on iPhone.
            pin: Optional PIN for AirPlay pairing (empty = on-screen code).
        """
        if self._process and self._process.poll() is None:
            return  # already running

        cmd = [
            self.uxplay_bin,
            "-n", device_name,
            "-fps", str(self.fps),
        ]
        if pin:
            cmd += ["-pin", pin]
        if self.width > 0 and self.height > 0:
            cmd += ["-s", f"{self.width}x{self.height}"]

        # Set DISPLAY so UxPlay renders to the correct X11 server
        env = os.environ.copy()
        env["DISPLAY"] = self.display

        self._process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # Give it a moment to bind
        time.sleep(0.5)

    def stop(self) -> None:
        """Terminate the UxPlay instance."""
        if self._process:
            try:
                self._process.terminate()
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait()
            self._process = None

    @property
    def is_running(self) -> bool:
        return self._process is not None and self._process.poll() is None

    @property
    def is_connected(self) -> bool:
        """Check if an iPhone is currently mirroring.

        We check UxPlay stderr for the connection log line.
        """
        if not self._process or self._process.poll() is not None:
            return False
        # Read stderr non-blocking and look for connection message
        try:
            import select
            if self._process.stderr:
                ready, _, _ = select.select([self._process.stderr], [], [], 0)
                if ready:
                    line = self._process.stderr.readline()
                    if b"connected" in line.lower():
                        return True
        except Exception:
            pass
        return True  # Assume connected if process is alive


# ── Xvfb Management ──────────────────────────────────────────────────────────


def start_xvfb(display: str = ":99", width: int = 1920, height: int = 1080) -> None:
    """Start a virtual X11 framebuffer for UxPlay to render into."""
    pid = subprocess.Popen(
        ["Xvfb", display, "-screen", "0", f"{width}x{height}x24", "-ac"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.5)
    # Verify
    if pid.poll() is not None:
        raise RuntimeError(f"Xvfb failed to start on {display}")
    # Set DISPLAY for subsequent tools
    os.environ["DISPLAY"] = display


def stop_xvfb(display: str = ":99") -> None:
    """Kill Xvfb on the given display."""
    subprocess.run(["pkill", "-f", f"Xvfb {display}"], capture_output=True)


def find_uxplay() -> Optional[str]:
    """Locate the UxPlay binary on the system."""
    return shutil.which("uxplay")
