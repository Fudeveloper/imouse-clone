"""
HTTP + WebSocket API server (port 9911).

API mirrors iMouse structure:
  - Device management
  - Mouse/keyboard control
  - Image recognition (find image, find color)
  - OCR (text recognition)
  - Screenshot capture
  - WebSocket for real-time event push
"""

from __future__ import annotations

import base64
import io
import json
import time
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from . import hardware as hw
from .device_manager import DeviceManager, DeviceState, get_manager
from .vision import find_color, find_image, find_text, ocr, pil_to_cv2

# ── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(title="iMouse Clone", version="0.1.0")
manager: DeviceManager = get_manager()

# WebSocket connections for real-time callbacks
_ws_clients: dict[str, WebSocket] = {}


# ── Pydantic Models ──────────────────────────────────────────────────────────


class ClickRequest(BaseModel):
    device_id: str
    x: int
    y: int


class SwipeRequest(BaseModel):
    device_id: str
    x1: int
    y1: int
    x2: int
    y2: int
    steps: int = 20
    step_delay: float = 0.01


class TypeTextRequest(BaseModel):
    device_id: str
    text: str
    char_delay: float = 0.02


class KeyRequest(BaseModel):
    device_id: str
    keycode: int
    modifier: int = 0x00


class ComboRequest(BaseModel):
    device_id: str
    keys: list[int]
    modifiers: int = 0x00


class FindImageRequest(BaseModel):
    device_id: str
    template_path: str
    threshold: float = 0.8


class FindColorRequest(BaseModel):
    device_id: str
    color: list[int]       # [R, G, B] — note: RGB input, converted to BGR
    tolerance: int = 5
    region: Optional[list[int]] = None  # [x, y, w, h]

    def get_region(self) -> Optional[tuple[int, int, int, int]]:
        if self.region and len(self.region) == 4:
            return (self.region[0], self.region[1], self.region[2], self.region[3])
        return None


class FindTextRequest(BaseModel):
    device_id: str
    text: str
    case_sensitive: bool = False


class RegisterRequest(BaseModel):
    device_id: str


class BindHardwareRequest(BaseModel):
    device_id: str
    port: str
    baudrate: int = 9600


# ── Unified Response Helper ──────────────────────────────────────────────────


def ok(data: Optional[dict] = None) -> JSONResponse:
    """Standard iMouse-style response."""
    return JSONResponse({
        "status": 200,
        "message": "成功",
        "data": {"code": 0, **(data or {})},
    })


def err(code: int, message: str, status: int = 400) -> JSONResponse:
    return JSONResponse({
        "status": status,
        "message": message,
        "data": {"code": code},
    }, status_code=status)


# ── Device Endpoints ─────────────────────────────────────────────────────────


@app.get("/api/devices")
async def list_devices():
    """List all registered devices and their states."""
    return ok({"devices": manager.status_all()})


@app.post("/api/device/register")
async def register_device(req: RegisterRequest):
    """Register a new device."""
    try:
        dev = manager.register(req.device_id)
        return ok({"device_id": dev.device_id, "state": dev.state.value})
    except ValueError as e:
        return err(1, str(e))


@app.post("/api/device/remove")
async def remove_device(req: RegisterRequest):
    """Remove and shutdown a device."""
    try:
        manager.remove(req.device_id)
        return ok({"device_id": req.device_id, "removed": True})
    except Exception as e:
        return err(2, str(e))


@app.post("/api/device/bind")
async def bind_hardware(req: BindHardwareRequest):
    """Bind CH9329 hardware to a device."""
    try:
        dev = manager.get(req.device_id)
        dev.bind_hardware(req.port, req.baudrate)
        return ok({"device_id": req.device_id, "hardware_id": req.port,
                   "state": dev.state.value})
    except Exception as e:
        return err(3, str(e))


@app.post("/api/device/unbind")
async def unbind_hardware(req: RegisterRequest):
    """Unbind hardware from a device."""
    try:
        dev = manager.get(req.device_id)
        dev.unbind_hardware()
        return ok({"device_id": req.device_id, "state": dev.state.value})
    except Exception as e:
        return err(3, str(e))


@app.get("/api/hardware/scan")
async def scan_hardware():
    """Scan serial ports for available CH9329 devices."""
    devices = manager.scan_hardware()
    return ok({"devices": devices})


@app.post("/api/device/airplay/start")
async def start_airplay(req: RegisterRequest):
    """Start AirPlay receiver for a device."""
    try:
        dev = manager.get(req.device_id)
        dev.start_airplay()
        return ok({"device_id": req.device_id, "state": dev.state.value})
    except Exception as e:
        return err(4, str(e))


@app.post("/api/device/airplay/stop")
async def stop_airplay(req: RegisterRequest):
    """Stop AirPlay receiver."""
    try:
        dev = manager.get(req.device_id)
        dev.stop_airplay()
        return ok({"device_id": req.device_id, "state": dev.state.value})
    except Exception as e:
        return err(4, str(e))


@app.post("/api/device/capture/start")
async def start_capture(req: RegisterRequest):
    """Begin capturing screenshots."""
    try:
        dev = manager.get(req.device_id)
        dev.start_capture()
        return ok({"device_id": req.device_id,
                   "screen_width": dev.screen_width,
                   "screen_height": dev.screen_height})
    except Exception as e:
        return err(5, str(e))


# ── Mouse/Keyboard Endpoints ─────────────────────────────────────────────────


@app.post("/api/click")
async def api_click(req: ClickRequest):
    """Click at screen coordinates."""
    try:
        dev = manager.get(req.device_id)
        dev.click(req.x, req.y)
        return ok({"x": req.x, "y": req.y})
    except Exception as e:
        return err(14, str(e))


@app.post("/api/swipe")
async def api_swipe(req: SwipeRequest):
    """Swipe gesture."""
    try:
        dev = manager.get(req.device_id)
        dev.swipe(req.x1, req.y1, req.x2, req.y2, req.steps, req.step_delay)
        return ok({"x1": req.x1, "y1": req.y1, "x2": req.x2, "y2": req.y2})
    except Exception as e:
        return err(14, str(e))


@app.post("/api/type")
async def api_type_text(req: TypeTextRequest):
    """Type text."""
    try:
        dev = manager.get(req.device_id)
        dev.type_text(req.text, req.char_delay)
        return ok({"text": req.text})
    except Exception as e:
        return err(14, str(e))


@app.post("/api/key")
async def api_key_tap(req: KeyRequest):
    """Tap a single key."""
    try:
        dev = manager.get(req.device_id)
        dev.key_tap(req.keycode, req.modifier)
        return ok({"keycode": req.keycode})
    except Exception as e:
        return err(14, str(e))


@app.post("/api/combo")
async def api_combo(req: ComboRequest):
    """Press key combination (e.g. Cmd+Tab)."""
    try:
        dev = manager.get(req.device_id)
        dev.key_combo(req.keys, req.modifiers)
        return ok({"keys": req.keys})
    except Exception as e:
        return err(14, str(e))


# ── Image Recognition Endpoints ──────────────────────────────────────────────


@app.post("/api/find_image")
async def api_find_image(req: FindImageRequest):
    """Find a template image on the device screen."""
    try:
        dev = manager.get(req.device_id)
        frame = dev.capture_frame()
        screenshot = pil_to_cv2(frame)
        result = find_image(screenshot, req.template_path, req.threshold)

        if result is None:
            return ok({"found": False})
        return ok({"found": True, **result})
    except Exception as e:
        return err(6, str(e))


@app.post("/api/find_color")
async def api_find_color(req: FindColorRequest):
    """Find a color on the device screen."""
    try:
        dev = manager.get(req.device_id)
        frame = dev.capture_frame()
        screenshot = pil_to_cv2(frame)

        # Input is RGB; convert to BGR for OpenCV
        bgr_color = (req.color[2], req.color[1], req.color[0])

        region = req.get_region()
        result = find_color(screenshot, bgr_color, req.tolerance, region)

        if result is None:
            return ok({"found": False})
        return ok({"found": True, **result})
    except Exception as e:
        return err(6, str(e))


@app.post("/api/ocr")
async def api_ocr(req: RegisterRequest):
    """Run OCR on device screen."""
    try:
        dev = manager.get(req.device_id)
        frame = dev.capture_frame()
        screenshot = pil_to_cv2(frame)
        results = ocr(screenshot)
        return ok({"texts": results})
    except Exception as e:
        return err(6, str(e))


@app.post("/api/find_text")
async def api_find_text(req: FindTextRequest):
    """Find specific text on device screen."""
    try:
        dev = manager.get(req.device_id)
        frame = dev.capture_frame()
        screenshot = pil_to_cv2(frame)
        result = find_text(screenshot, req.text, req.case_sensitive)

        if result is None:
            return ok({"found": False})
        return ok({"found": True, **result})
    except Exception as e:
        return err(6, str(e))


# ── Screenshot Endpoints ─────────────────────────────────────────────────────


@app.post("/api/screenshot")
async def api_screenshot(req: RegisterRequest):
    """Take a screenshot and return it as base64."""
    try:
        dev = manager.get(req.device_id)
        frame = dev.capture_frame()

        buf = io.BytesIO()
        frame.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()

        return ok({
            "format": "png",
            "base64": b64,
            "width": frame.width,
            "height": frame.height,
        })
    except Exception as e:
        return err(26, str(e))


# ── WebSocket (iMouse Callbacks) ─────────────────────────────────────────────


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """WebSocket for real-time device events (iMouse callback equivalent).

    Client sends JSON commands; server pushes state updates and event notifications.
    """
    await ws.accept()
    client_id = str(id(ws))
    _ws_clients[client_id] = ws

    # Send welcome
    await ws.send_json({"event": "connected", "client_id": client_id})

    try:
        while True:
            data = await ws.receive_text()
            try:
                msg = json.loads(data)
            except json.JSONDecodeError:
                await ws.send_json({"event": "error", "message": "Invalid JSON"})
                continue

            action = msg.get("action", "")
            device_id = msg.get("device_id", "")

            if action == "subscribe":
                await ws.send_json({
                    "event": "subscribed",
                    "device_id": device_id,
                    "devices": manager.status_all(),
                })

            elif action == "ping":
                await ws.send_json({"event": "pong", "time": time.time()})

            else:
                await ws.send_json({
                    "event": "unknown_action",
                    "message": f"Unknown action: {action}",
                })

    except WebSocketDisconnect:
        pass
    finally:
        _ws_clients.pop(client_id, None)
