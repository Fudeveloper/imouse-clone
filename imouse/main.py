"""
iMouse Clone — iOS群控免越狱方案

Entry point. Starts:
  1. Xvfb (virtual framebuffer for AirPlay rendering)
  2. FastAPI server (port 9911)
  3. Device manager

Usage:
    python -m imouse.main
    python -m imouse.main --port 9911 --display :99
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import signal
import sys

import uvicorn

from .airplay import find_uxplay, start_xvfb, stop_xvfb
from .device_manager import get_manager
from .hardware import list_devices

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("imouse")


def check_deps() -> dict:
    """Check runtime dependencies and return status."""
    status = {}

    # Python deps
    for mod in ["serial", "cv2", "numpy", "PIL", "fastapi", "uvicorn"]:
        try:
            __import__(mod)
            status[mod] = "OK"
        except ImportError:
            status[mod] = "MISSING: not installed"

    # System deps
    uxplay = find_uxplay()
    status["uxplay"] = f"OK: {uxplay}" if uxplay else "MISSING: not found (install UxPlay)"

    return status


def print_banner():
    print(r"""
     ___ __  __  ___  _   _ ____  _____
    |_ _|  \/  |/ _ \| | | / ___|| ____|
     | || |\/| | | | | | | \___ \|  _|
     | || |  | | |_| | |_| |___) | |___
    |___|_|  |_|\___/ \___/|____/|_____|
          iOS Group Control - No Jailbreak Required

       Architecture: AirPlay + CH9329 + OpenCV + PaddleOCR
    """)
    print("-" * 60)


def main():
    parser = argparse.ArgumentParser(description="iMouse Clone Server")
    parser.add_argument("--port", type=int, default=9911,
                        help="HTTP/WS server port (default: 9911)")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                        help="Bind address (default: 0.0.0.0)")
    parser.add_argument("--display", type=str, default=":99",
                        help="X11 display for AirPlay (default: :99)")
    parser.add_argument("--no-xvfb", action="store_true",
                        help="Don't start Xvfb (use existing display)")
    parser.add_argument("--check", action="store_true",
                        help="Check dependencies and exit")
    args = parser.parse_args()

    print_banner()

    if args.check:
        print("Dependency Check:")
        for dep, status in check_deps().items():
            print(f"  {dep:12s}  {status}")
        return 0

    log.info(f"Starting iMouse Clone on port {args.port}")

    # 1. Start Xvfb if needed
    if not args.no_xvfb:
        try:
            start_xvfb(args.display)
            log.info(f"Xvfb started on {args.display}")
        except Exception as e:
            log.warning(f"Xvfb failed ({e}) — continuing without virtual display")

    # 2. Scan for hardware
    hw_devices = list_devices()
    if hw_devices:
        log.info(f"Found {len(hw_devices)} serial device(s):")
        for d in hw_devices:
            log.info(f"  {d['port']:15s}  {d.get('description', '')}")
    else:
        log.info("No serial devices found (CH9329 not connected?)")

    # 3. Start FastAPI server
    os.environ["DISPLAY"] = args.display

    uvicorn.run(
        "imouse.server:app",
        host=args.host,
        port=args.port,
        log_level="info",
        reload=False,
    )


if __name__ == "__main__":
    sys.exit(main())
