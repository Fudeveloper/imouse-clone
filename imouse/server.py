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
from typing import Any, Optional
from urllib.parse import parse_qs

import cv2
import numpy as np
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from . import hardware as hw
from .device_manager import DeviceManager, DeviceState, get_manager
from .vision import find_color, find_colors, find_image, find_text, ocr, pil_to_cv2

# ── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(title="iMouse Clone", version="0.1.0")
manager: DeviceManager = get_manager()

# WebSocket connections for real-time callbacks
_ws_clients: dict[str, WebSocket] = {}
_callback_events: list[dict[str, Any]] = []
_callback_seq = 0
_MAX_CALLBACK_EVENTS = 500
_xp_runtime_path: Path | None = Path("state/xp_runtime.json")
_xp_config: dict[str, Any] = {}
_xp_users: dict[str, dict[str, Any]] = {}
_xp_active_user = ""
_xp_shortcuts: dict[str, dict[str, Any]] = {}


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
    region: Optional[list[int]] = None  # [x, y, w, h]

    def get_region(self) -> Optional[tuple[int, int, int, int]]:
        if self.region and len(self.region) == 4:
            return (self.region[0], self.region[1], self.region[2], self.region[3])
        return None


class FindColorRequest(BaseModel):
    device_id: str
    color: list[int]       # [R, G, B] — note: RGB input, converted to BGR
    tolerance: int = 5
    region: Optional[list[int]] = None  # [x, y, w, h]

    def get_region(self) -> Optional[tuple[int, int, int, int]]:
        if self.region and len(self.region) == 4:
            return (self.region[0], self.region[1], self.region[2], self.region[3])
        return None


class FindColorsRequest(BaseModel):
    device_id: str
    points: list[dict] = Field(default_factory=list)
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


class ScreenshotRequest(BaseModel):
    device_id: str
    rect: Optional[list[int]] = None      # XP shape: [x1, y1, x2, y2]
    region: Optional[list[int]] = None    # local shape: [x, y, w, h]
    save_path: str = ""
    binary: bool = False
    jpg: bool = False
    format: str = ""


class BindHardwareRequest(BaseModel):
    device_id: str
    port: str
    baudrate: int = 9600


class DeviceProfileRequest(BaseModel):
    device_id: str
    profile: dict[str, Any] = Field(default_factory=dict)


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


# ── XP-Compatible Unified API ────────────────────────────────────────────────


def xp_ok(fun: str, data: Optional[dict] = None, msgid: int = 0) -> JSONResponse:
    """iMouse XP-style response with top-level fun/msgid fields."""
    return JSONResponse({
        "status": 200,
        "message": "成功",
        "data": {"code": 0, "message": "成功", **(data or {})},
        "msgid": msgid,
        "fun": fun,
    })


def xp_err(fun: str, code: int, message: str,
           status: int = 400, msgid: int = 0) -> JSONResponse:
    return JSONResponse({
        "status": status,
        "message": message,
        "data": {"code": code, "message": message},
        "msgid": msgid,
        "fun": fun,
    }, status_code=status)


def _json_response_body(response: JSONResponse) -> dict:
    return json.loads(response.body.decode("utf-8"))


def _parse_value(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    text = value.strip()
    if not text:
        return value
    if (text.startswith("{") and text.endswith("}")) or \
       (text.startswith("[") and text.endswith("]")):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return value
    if "," in text:
        parts = [p.strip() for p in text.split(",")]
        parsed: list[Any] = []
        for part in parts:
            try:
                parsed.append(int(part))
            except ValueError:
                try:
                    parsed.append(float(part))
                except ValueError:
                    parsed.append(part)
        return parsed
    return value


def _parse_form_fallback(raw: bytes, content_type: str) -> dict[str, Any]:
    """Parse simple form fields when Starlette's optional multipart parser is unavailable."""
    if "application/x-www-form-urlencoded" in content_type:
        parsed = parse_qs(raw.decode("utf-8", errors="replace"), keep_blank_values=True)
        return {key: values[-1] if values else "" for key, values in parsed.items()}
    if "multipart" not in content_type or not raw:
        return {}
    marker = "boundary="
    if marker not in content_type:
        return {}
    boundary = content_type.split(marker, 1)[1].split(";", 1)[0].strip().strip('"')
    if not boundary:
        return {}
    delimiter = ("--" + boundary).encode()
    body: dict[str, Any] = {}
    for part in raw.split(delimiter):
        part = part.strip()
        if not part or part == b"--":
            continue
        if part.endswith(b"--"):
            part = part[:-2].strip()
        if b"\r\n\r\n" not in part:
            continue
        header_blob, value_blob = part.split(b"\r\n\r\n", 1)
        headers = header_blob.decode("utf-8", errors="replace")
        name = ""
        for header in headers.split("\r\n"):
            lower = header.lower()
            if lower.startswith("content-disposition:") and "name=" in lower:
                after = header.split("name=", 1)[1].strip()
                if after.startswith('"'):
                    name = after.split('"', 2)[1]
                else:
                    name = after.split(";", 1)[0].strip()
                break
        if not name:
            continue
        body[name] = value_blob.rstrip(b"\r\n").decode("utf-8", errors="replace")
    return body


def _normalize_xp_data(data: dict[str, Any]) -> dict[str, Any]:
    normalized = {k: _parse_value(v) for k, v in data.items()}
    if "device_id" not in normalized and "id" in normalized:
        normalized["device_id"] = normalized["id"]
    return normalized


def _device_ids_from_data(data: dict[str, Any]) -> list[str]:
    group_name = str(data.get("group", data.get("group_name", "")) or "").strip()
    if group_name:
        return manager.get_group(group_name)
    value = data.get("device_ids", data.get("ids", data.get("device_id", data.get("id", []))))
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        value = [value]
    return [str(item).strip() for item in value if str(item).strip()]


def _calibration_payload_from_data(data: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    device_id = str(data.get("device_id", data.get("id", "")) or "").strip()
    if not device_id:
        raise ValueError("device_id is required")
    nested = data.get("calibration")
    if isinstance(nested, dict):
        profile = dict(nested)
    else:
        profile = {
            key: value for key, value in data.items()
            if key not in {"device_id", "id", "fun", "msgid"}
        }
    return device_id, profile


def _profile_payload_from_data(data: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    device_id = str(data.get("device_id", data.get("id", "")) or "").strip()
    if not device_id:
        raise ValueError("device_id is required")
    for key in ("profile", "metadata", "component_metadata"):
        nested = data.get(key)
        if isinstance(nested, dict):
            return device_id, dict(nested)
    profile = {
        key: value for key, value in data.items()
        if key not in {"device_id", "id", "fun", "msgid"}
    }
    return device_id, profile


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items() if str(key).strip()}
    return str(value)


def _load_xp_runtime_state() -> None:
    if not _xp_runtime_path or not _xp_runtime_path.exists():
        return
    try:
        raw = json.loads(_xp_runtime_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    if not isinstance(raw, dict):
        return
    global _xp_config, _xp_users, _xp_active_user, _xp_shortcuts
    config = raw.get("config", {})
    users = raw.get("users", {})
    shortcuts = raw.get("shortcuts", {})
    _xp_config = dict(config) if isinstance(config, dict) else {}
    _xp_users = {
        str(user_id): dict(user)
        for user_id, user in users.items()
        if str(user_id).strip() and isinstance(user, dict)
    } if isinstance(users, dict) else {}
    _xp_active_user = str(raw.get("active_user", "") or "")
    _xp_shortcuts = {
        str(name): dict(shortcut)
        for name, shortcut in shortcuts.items()
        if str(name).strip() and isinstance(shortcut, dict)
    } if isinstance(shortcuts, dict) else {}


def _save_xp_runtime_state() -> None:
    if not _xp_runtime_path:
        return
    _xp_runtime_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "config": _xp_config,
        "users": _xp_users,
        "active_user": _xp_active_user,
        "shortcuts": _xp_shortcuts,
    }
    _xp_runtime_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def clear_xp_runtime_state() -> None:
    """Clear local XP config/user/shortcut compatibility state for tests."""
    global _xp_config, _xp_users, _xp_active_user, _xp_shortcuts
    _xp_config = {}
    _xp_users = {}
    _xp_active_user = ""
    _xp_shortcuts = {}
    _save_xp_runtime_state()


def set_xp_runtime_store_path(path: str | Path | None) -> None:
    """Set local XP runtime persistence path; pass None for isolated tests."""
    global _xp_runtime_path
    _xp_runtime_path = Path(path) if path else None
    clear_xp_runtime_state()
    _load_xp_runtime_state()


def _config_payload_from_data(data: dict[str, Any]) -> dict[str, Any]:
    nested = data.get("config", data.get("imconfig", None))
    if isinstance(nested, dict):
        return {str(key): _jsonable(value) for key, value in nested.items() if str(key).strip()}
    key = str(data.get("key", data.get("name", "")) or "").strip()
    if key:
        return {key: _jsonable(data.get("value", data.get("val", "")))}
    return {
        str(key): _jsonable(value)
        for key, value in data.items()
        if str(key).strip() and key not in {"fun", "msgid", "device_id", "id"}
    }


def _user_payload_from_data(data: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    nested = data.get("user")
    source = dict(nested) if isinstance(nested, dict) else dict(data)
    user_id = str(
        source.get("user_id", source.get("id", source.get("name", source.get("username", ""))))
        or ""
    ).strip()
    if not user_id:
        raise ValueError("user id is required")
    payload = {
        str(key): _jsonable(value)
        for key, value in source.items()
        if str(key).strip() and key not in {"fun", "msgid"}
    }
    payload.setdefault("user_id", user_id)
    return user_id, payload


def _shortcut_payload_from_data(data: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    nested = data.get("shortcut")
    source = dict(nested) if isinstance(nested, dict) else dict(data)
    name = str(
        source.get("name", source.get("shortcut", source.get("id", source.get("key", ""))))
        or ""
    ).strip()
    if not name:
        raise ValueError("shortcut name is required")
    payload = {
        str(key): _jsonable(value)
        for key, value in source.items()
        if str(key).strip() and key not in {"fun", "msgid"}
    }
    payload.setdefault("name", name)
    return name, payload


_load_xp_runtime_state()


async def _parse_xp_request(request: Request) -> tuple[str, dict[str, Any], int]:
    """Parse iMouse XP GET, JSON POST, and form-style POST requests."""
    query = dict(request.query_params)
    content_type = request.headers.get("content-type", "").lower()
    body: dict[str, Any] = {}

    if "application/json" in content_type:
        try:
            raw = await request.json()
        except json.JSONDecodeError:
            raw = {}
        if isinstance(raw, dict):
            nested = raw.get("data", {})
            body = dict(nested) if isinstance(nested, dict) else {}
            for key, value in raw.items():
                if key not in {"data", "fun", "msgid"}:
                    body.setdefault(key, value)
            body.setdefault("fun", raw.get("fun", ""))
            body.setdefault("msgid", raw.get("msgid", 0))
    elif "form" in content_type or "multipart" in content_type:
        try:
            form = await request.form()
            body = {key: value for key, value in form.items()}
            nested = body.get("data")
            if isinstance(nested, str):
                parsed = _parse_value(nested)
                if isinstance(parsed, dict):
                    body.update(parsed)
        except Exception:
            body = _parse_form_fallback(await request.body(), content_type)
            nested = body.get("data")
            if isinstance(nested, str):
                parsed = _parse_value(nested)
                if isinstance(parsed, dict):
                    body.update(parsed)

    merged = {**query, **body}
    fun = str(merged.pop("fun", "") or "")
    try:
        msgid = int(merged.pop("msgid", 0) or 0)
    except (TypeError, ValueError):
        msgid = 0
    return fun, _normalize_xp_data(merged), msgid


def _ocr_to_xp_list(items: list[dict]) -> list[dict]:
    xp_items = []
    for item in items:
        bbox = item.get("bbox") or []
        xs = [p[0] for p in bbox if len(p) >= 2]
        ys = [p[1] for p in bbox if len(p) >= 2]
        if xs and ys:
            rect = [int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))]
            centre = [int((rect[0] + rect[2]) / 2), int((rect[1] + rect[3]) / 2)]
        else:
            rect = [0, 0, 0, 0]
            centre = [0, 0]
        xp_items.append({
            "text": item.get("text", ""),
            "centre": centre,
            "rect": rect,
            "similarity": float(item.get("confidence", 0.0)),
        })
    return xp_items


def _color_result_to_rgb(result: dict) -> dict:
    out = dict(result)
    converted_points = []
    for point in out.get("points", []):
        converted = dict(point)
        color = converted.get("color")
        if isinstance(color, list) and len(color) == 3:
            converted["color"] = [color[2], color[1], color[0]]
        converted_points.append(converted)
    if converted_points:
        out["points"] = converted_points
    return out


def _screenshot_format(req: ScreenshotRequest) -> tuple[str, str, str]:
    requested = str(req.format or "").strip().lower()
    if req.jpg or requested in {"jpg", "jpeg"}:
        return "JPEG", "jpg", "image/jpeg"
    return "PNG", "png", "image/png"


def _screenshot_crop_box(req: ScreenshotRequest) -> tuple[int, int, int, int] | None:
    if req.rect and len(req.rect) == 4:
        x1, y1, x2, y2 = [int(value) for value in req.rect]
        return x1, y1, x2, y2
    if req.region and len(req.region) == 4:
        x, y, w, h = [int(value) for value in req.region]
        return x, y, x + w, y + h
    return None


def _crop_screenshot_frame(frame: Any, req: ScreenshotRequest) -> tuple[Any, list[int] | None]:
    box = _screenshot_crop_box(req)
    if box is None:
        return frame, None
    x1, y1, x2, y2 = box
    left = max(0, min(frame.width, min(x1, x2)))
    top = max(0, min(frame.height, min(y1, y2)))
    right = max(0, min(frame.width, max(x1, x2)))
    bottom = max(0, min(frame.height, max(y1, y2)))
    if right <= left or bottom <= top:
        raise ValueError(f"invalid screenshot rect: {box}")
    return frame.crop((left, top, right, bottom)), [left, top, right, bottom]


def _safe_screenshot_save_path(path_text: str, ext: str) -> Path:
    raw = str(path_text or "").strip()
    if not raw:
        raise ValueError("save_path is empty")
    root = Path.cwd().resolve()
    out_path = Path(raw)
    if not out_path.is_absolute():
        out_path = root / out_path
    if out_path.exists() and out_path.is_dir():
        out_path = out_path / f"screenshot.{ext}"
    elif not out_path.suffix:
        out_path = out_path.with_suffix(f".{ext}")
    resolved = out_path.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"save_path must stay under workspace: {raw}") from exc
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def _build_screenshot_payload(req: ScreenshotRequest) -> dict[str, Any]:
    dev = manager.get(req.device_id)
    frame = dev.capture_frame()
    source_width = frame.width
    source_height = frame.height
    frame, rect = _crop_screenshot_frame(frame, req)
    pil_format, ext, media_type = _screenshot_format(req)
    if pil_format == "JPEG" and frame.mode not in {"RGB", "L"}:
        frame = frame.convert("RGB")

    buf = io.BytesIO()
    frame.save(buf, format=pil_format)
    raw = buf.getvalue()

    payload: dict[str, Any] = {
        "format": ext,
        "width": frame.width,
        "height": frame.height,
        "source_width": source_width,
        "source_height": source_height,
        "rect": rect,
        "_bytes": raw,
        "_media_type": media_type,
    }
    if req.save_path:
        out_path = _safe_screenshot_save_path(req.save_path, ext)
        out_path.write_bytes(raw)
        payload["save_path"] = str(out_path)
        payload["image"] = str(out_path)
    else:
        b64 = base64.b64encode(raw).decode()
        payload["base64"] = b64
        payload["image"] = b64
    return payload


def _batch_result(device_id: str, ok: bool, **data: Any) -> dict:
    return {"id": device_id, "device_id": device_id, "ok": ok, **data}


def clear_xp_callback_events() -> None:
    """Clear in-memory callback events for tests and fresh offline runs."""
    global _callback_seq
    _callback_events.clear()
    _callback_seq = 0


def _append_xp_callback_event(
    name: str,
    *,
    device_id: str = "",
    data: Optional[dict[str, Any]] = None,
    source: str = "api",
    severity: str = "info",
) -> dict[str, Any]:
    global _callback_seq
    _callback_seq += 1
    event = {
        "seq": _callback_seq,
        "ts": time.time(),
        "event": str(name or "event"),
        "type": str(name or "event"),
        "source": str(source or "api"),
        "severity": str(severity or "info"),
        "device_id": str(device_id or ""),
        "id": str(device_id or ""),
        "data": data or {},
    }
    _callback_events.append(event)
    if len(_callback_events) > _MAX_CALLBACK_EVENTS:
        del _callback_events[:-_MAX_CALLBACK_EVENTS]
    return event


def _callback_event_rows(after_seq: int = 0, limit: int = 50) -> list[dict[str, Any]]:
    bounded_limit = max(1, min(int(limit or 50), 200))
    return [
        dict(event)
        for event in _callback_events
        if int(event.get("seq", 0) or 0) > int(after_seq or 0)
    ][:bounded_limit]


async def _broadcast_xp_callback_event(event: dict[str, Any]) -> None:
    dead_clients = []
    payload = {
        "event": "callback",
        "callback": event,
        "data": event,
    }
    for client_id, ws in list(_ws_clients.items()):
        try:
            await ws.send_json(payload)
        except Exception:
            dead_clients.append(client_id)
    for client_id in dead_clients:
        _ws_clients.pop(client_id, None)


async def _record_xp_callback_event(
    name: str,
    *,
    device_id: str = "",
    data: Optional[dict[str, Any]] = None,
    source: str = "api",
    severity: str = "info",
) -> dict[str, Any]:
    event = _append_xp_callback_event(
        name,
        device_id=device_id,
        data=data,
        source=source,
        severity=severity,
    )
    await _broadcast_xp_callback_event(event)
    return event


def _run_batch(device_ids: list[str], action: Any) -> dict:
    results = []
    for device_id in device_ids:
        try:
            device = manager.get(device_id)
            action(device)
            results.append(_batch_result(device_id, True))
        except Exception as exc:
            results.append(_batch_result(device_id, False, error=str(exc)))
    failures = [item for item in results if not item["ok"]]
    return {
        "ok": not failures,
        "count": len(results),
        "success_count": len(results) - len(failures),
        "failure_count": len(failures),
        "results": results,
    }


async def dispatch_xp_fun(fun: str, data: dict[str, Any],
                          msgid: int = 0) -> JSONResponse:
    """Dispatch the iMouse XP-style fun API to the current local core."""
    aliases = {
        "/dev/list": "/device/list",
        "/devices": "/device/list",
        "/usb/list": "/hardware/scan",
        "/usb/scan": "/hardware/scan",
        "/mouse/down": "/mouse/click",
        "/pic/screen": "/pic/screenshot",
        "/pic/capture": "/pic/screenshot",
        "/pic/find_image": "/pic/find-image",
        "/pic/find-color": "/pic/find_color",
        "/pic/find-colors": "/pic/find_colors",
        "/pic/find_multi_color": "/pic/find_colors",
        "/pic/findtext": "/pic/find-text",
        "/pic/find_text": "/pic/find-text",
        "/mouse/batch-click": "/batch/click",
        "/mouse/batch-swipe": "/batch/swipe",
        "/keyboard/batch-type": "/batch/type",
        "/key/batch-type": "/batch/type",
        "/groups": "/group/list",
        "/group/set": "/group/save",
        "/group/delete": "/group/remove",
        "/device/calibration": "/calibration/get",
        "/calibration/save": "/calibration/set",
        "/device/profile": "/profile/get",
        "/device/profile/get": "/profile/get",
        "/device/profile/set": "/profile/set",
        "/device/metadata": "/profile/get",
        "/device/metadata/get": "/profile/get",
        "/device/metadata/set": "/profile/set",
        "/metadata/list": "/profile/list",
        "/metadata/get": "/profile/get",
        "/metadata/set": "/profile/set",
        "/event/list": "/callback/list",
        "/event/poll": "/callback/poll",
        "/event/push": "/callback/push",
        "/callback/events": "/callback/list",
        "/imconfig/list": "/config/list",
        "/imconfig/get": "/config/get",
        "/imconfig/set": "/config/set",
        "/imconfig/save": "/config/set",
        "/im/config/list": "/config/list",
        "/im/config/get": "/config/get",
        "/im/config/set": "/config/set",
        "/user/save": "/user/set",
        "/user/login": "/user/switch",
        "/user/select": "/user/switch",
        "/user/delete": "/user/remove",
        "/shortcut/set": "/shortcut/save",
        "/shortcut/delete": "/shortcut/remove",
        "/shortcut/call": "/shortcut/run",
        "/shortcuts": "/shortcut/list",
        "/shortcut/switch/bril": "/shortcut/brightness",
    }
    fun = aliases.get(fun, fun)

    try:
        if fun in {"/callback/list", "/callback/poll"}:
            try:
                after_seq = int(data.get("after_seq", data.get("seq", 0)) or 0)
            except (TypeError, ValueError):
                after_seq = 0
            try:
                limit = int(data.get("limit", 50) or 50)
            except (TypeError, ValueError):
                limit = 50
            events = _callback_event_rows(after_seq=after_seq, limit=limit)
            return xp_ok(fun, {
                "events": events,
                "count": len(events),
                "last_seq": _callback_seq,
                "has_more": bool(_callback_event_rows(after_seq=events[-1]["seq"], limit=1)) if events else False,
            }, msgid)

        if fun == "/callback/push":
            event_name = str(data.get("event", data.get("type", "manual")) or "manual")
            device_id = str(data.get("device_id", data.get("id", "")) or "")
            details = data.get("data", data.get("details", {}))
            if not isinstance(details, dict):
                details = {"value": details}
            event = await _record_xp_callback_event(
                event_name,
                device_id=device_id,
                data=details,
                source=str(data.get("source", "manual") or "manual"),
                severity=str(data.get("severity", "info") or "info"),
            )
            return xp_ok(fun, {"event": event}, msgid)

        if fun == "/callback/clear":
            clear_xp_callback_events()
            return xp_ok(fun, {"cleared": True, "last_seq": _callback_seq}, msgid)

        if fun in {"/config/list", "/config/get"}:
            key = str(data.get("key", data.get("name", "")) or "").strip()
            if key:
                return xp_ok(fun, {
                    "key": key,
                    "value": _xp_config.get(key),
                    "exists": key in _xp_config,
                    "config": dict(_xp_config),
                }, msgid)
            return xp_ok(fun, {"config": dict(_xp_config)}, msgid)

        if fun == "/config/set":
            updates = _config_payload_from_data(data)
            _xp_config.update(updates)
            _save_xp_runtime_state()
            await _record_xp_callback_event(
                "config_saved",
                data={"keys": sorted(updates), "config": updates},
                source="xp_config",
            )
            return xp_ok(fun, {"config": dict(_xp_config), "updated": updates}, msgid)

        if fun == "/user/list":
            return xp_ok(fun, {
                "users": [dict(user) for _uid, user in sorted(_xp_users.items())],
                "active_user": _xp_active_user,
            }, msgid)

        if fun in {"/user/get", "/user/current"}:
            user_id = str(
                data.get("user_id", data.get("id", data.get("name", "")))
                or (_xp_active_user if fun == "/user/current" else "")
            ).strip()
            if not user_id:
                return xp_ok(fun, {"user": {}, "active_user": _xp_active_user, "exists": False}, msgid)
            return xp_ok(fun, {
                "user_id": user_id,
                "user": dict(_xp_users.get(user_id, {})),
                "active_user": _xp_active_user,
                "exists": user_id in _xp_users,
            }, msgid)

        if fun == "/user/set":
            user_id, user = _user_payload_from_data(data)
            _xp_users[user_id] = user
            if data.get("active") or not _xp_active_user:
                globals()["_xp_active_user"] = user_id
            _save_xp_runtime_state()
            await _record_xp_callback_event(
                "user_saved",
                data={"user_id": user_id, "active_user": _xp_active_user},
                source="xp_user",
            )
            return xp_ok(fun, {"user_id": user_id, "user": user, "active_user": _xp_active_user}, msgid)

        if fun == "/user/switch":
            user_id = str(data.get("user_id", data.get("id", data.get("name", ""))) or "").strip()
            if not user_id:
                return xp_err(fun, 400, "user id is required", msgid=msgid)
            if user_id not in _xp_users:
                _xp_users[user_id] = {"user_id": user_id, "name": user_id, "auto_created": True}
            globals()["_xp_active_user"] = user_id
            _save_xp_runtime_state()
            await _record_xp_callback_event(
                "user_switched",
                data={"user_id": user_id},
                source="xp_user",
            )
            return xp_ok(fun, {"user_id": user_id, "user": dict(_xp_users[user_id]), "active_user": _xp_active_user}, msgid)

        if fun == "/user/remove":
            user_id = str(data.get("user_id", data.get("id", data.get("name", ""))) or "").strip()
            if not user_id:
                return xp_err(fun, 400, "user id is required", msgid=msgid)
            removed = _xp_users.pop(user_id, None) is not None
            if _xp_active_user == user_id:
                globals()["_xp_active_user"] = ""
            _save_xp_runtime_state()
            await _record_xp_callback_event(
                "user_removed",
                data={"user_id": user_id, "removed": removed},
                source="xp_user",
            )
            return xp_ok(fun, {"user_id": user_id, "removed": removed, "active_user": _xp_active_user}, msgid)

        if fun == "/shortcut/list":
            return xp_ok(fun, {"shortcuts": [dict(row) for _name, row in sorted(_xp_shortcuts.items())]}, msgid)

        if fun == "/shortcut/get":
            name = str(data.get("name", data.get("shortcut", data.get("id", ""))) or "").strip()
            if not name:
                return xp_ok(fun, {"shortcut": {}, "exists": False}, msgid)
            return xp_ok(fun, {
                "name": name,
                "shortcut": dict(_xp_shortcuts.get(name, {})),
                "exists": name in _xp_shortcuts,
            }, msgid)

        if fun == "/shortcut/save":
            name, shortcut = _shortcut_payload_from_data(data)
            _xp_shortcuts[name] = shortcut
            _save_xp_runtime_state()
            await _record_xp_callback_event(
                "shortcut_saved",
                data={"name": name, "shortcut": shortcut},
                source="xp_shortcut",
            )
            return xp_ok(fun, {"name": name, "shortcut": shortcut}, msgid)

        if fun == "/shortcut/remove":
            name = str(data.get("name", data.get("shortcut", data.get("id", ""))) or "").strip()
            if not name:
                return xp_err(fun, 400, "shortcut name is required", msgid=msgid)
            removed = _xp_shortcuts.pop(name, None) is not None
            _save_xp_runtime_state()
            await _record_xp_callback_event(
                "shortcut_removed",
                data={"name": name, "removed": removed},
                source="xp_shortcut",
            )
            return xp_ok(fun, {"name": name, "removed": removed}, msgid)

        if fun == "/shortcut/run":
            name = str(data.get("name", data.get("shortcut", data.get("id", ""))) or "").strip()
            shortcut = dict(_xp_shortcuts.get(name, {})) if name else {}
            await _record_xp_callback_event(
                "shortcut_run",
                device_id=str(data.get("device_id", data.get("id", "")) or ""),
                data={"name": name, "shortcut": shortcut, "dry_run": True},
                source="xp_shortcut",
            )
            return xp_ok(fun, {"name": name, "shortcut": shortcut, "dry_run": True, "executed": False}, msgid)

        if fun == "/shortcut/brightness":
            value = data.get("value", data.get("brightness", data.get("level", "")))
            if value != "":
                _xp_config["brightness"] = _jsonable(value)
                _save_xp_runtime_state()
            await _record_xp_callback_event(
                "shortcut_brightness",
                device_id=str(data.get("device_id", data.get("id", "")) or ""),
                data={"brightness": _xp_config.get("brightness"), "dry_run": True},
                source="xp_shortcut",
            )
            return xp_ok(fun, {"brightness": _xp_config.get("brightness"), "dry_run": True, "executed": False}, msgid)

        if fun == "/device/list":
            return xp_ok(fun, {"devices": manager.status_all()}, msgid)

        if fun == "/device/register":
            dev = manager.register(RegisterRequest(**data).device_id)
            await _record_xp_callback_event(
                "device_registered",
                device_id=dev.device_id,
                data={"state": dev.state.value},
            )
            return xp_ok(fun, {"device_id": dev.device_id, "id": dev.device_id,
                               "state": dev.state.value}, msgid)

        if fun == "/device/remove":
            req = RegisterRequest(**data)
            manager.remove(req.device_id)
            await _record_xp_callback_event(
                "device_removed",
                device_id=req.device_id,
                data={"removed": True},
            )
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               "removed": True}, msgid)

        if fun == "/group/list":
            return xp_ok(fun, {"groups": manager.list_groups()}, msgid)

        if fun == "/group/save":
            name = str(data.get("name", data.get("group", data.get("group_name", ""))) or "")
            device_ids = _device_ids_from_data({
                key: value for key, value in data.items()
                if key not in {"group", "group_name"}
            })
            group = manager.set_group(name, device_ids)
            await _record_xp_callback_event(
                "group_saved",
                data={"name": name, "device_ids": group.get("device_ids", []), "count": group.get("count", 0)},
            )
            return xp_ok(fun, {"group": group}, msgid)

        if fun == "/group/remove":
            name = str(data.get("name", data.get("group", data.get("group_name", ""))) or "")
            removed = manager.remove_group(name)
            await _record_xp_callback_event(
                "group_removed",
                data={"name": name, "removed": removed},
            )
            return xp_ok(fun, {"name": name, "removed": removed}, msgid)

        if fun == "/calibration/list":
            return xp_ok(fun, {"calibrations": manager.list_calibrations()}, msgid)

        if fun == "/calibration/get":
            req = RegisterRequest(**data)
            return xp_ok(fun, {
                "device_id": req.device_id,
                "id": req.device_id,
                "calibration": manager.get_calibration(req.device_id),
            }, msgid)

        if fun == "/calibration/set":
            device_id, profile = _calibration_payload_from_data(data)
            result = manager.set_calibration(device_id, profile)
            await _record_xp_callback_event(
                "calibration_saved",
                device_id=device_id,
                data={"calibration": result.get("calibration", {})},
            )
            return xp_ok(fun, {"id": device_id, **result}, msgid)

        if fun == "/profile/list":
            return xp_ok(fun, {"profiles": manager.list_profiles()}, msgid)

        if fun == "/profile/get":
            req = RegisterRequest(**data)
            return xp_ok(fun, {
                "device_id": req.device_id,
                "id": req.device_id,
                "profile": manager.get_profile(req.device_id),
            }, msgid)

        if fun == "/profile/set":
            device_id, profile = _profile_payload_from_data(data)
            result = manager.set_profile(device_id, profile)
            await _record_xp_callback_event(
                "profile_saved",
                device_id=device_id,
                data={"profile": result.get("profile", {})},
            )
            return xp_ok(fun, {"id": device_id, **result}, msgid)

        if fun == "/hardware/scan":
            return xp_ok(fun, {"devices": manager.scan_hardware()}, msgid)

        if fun in {"/device/bind", "/usb/bind"}:
            req = BindHardwareRequest(**data)
            dev = manager.get(req.device_id)
            dev.bind_hardware(req.port, req.baudrate)
            await _record_xp_callback_event(
                "hardware_bound",
                device_id=req.device_id,
                data={"hardware_id": req.port, "port": req.port, "state": dev.state.value},
            )
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               "hardware_id": req.port, "state": dev.state.value}, msgid)

        if fun == "/device/unbind":
            req = RegisterRequest(**data)
            dev = manager.get(req.device_id)
            dev.unbind_hardware()
            await _record_xp_callback_event(
                "hardware_unbound",
                device_id=req.device_id,
                data={"state": dev.state.value},
            )
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               "state": dev.state.value}, msgid)

        if fun in {"/airplay/connect", "/airplay/start"}:
            req = RegisterRequest(**data)
            dev = manager.get(req.device_id)
            dev.start_airplay()
            await _record_xp_callback_event(
                "airplay_connected",
                device_id=req.device_id,
                data={"state": dev.state.value},
            )
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               "state": dev.state.value}, msgid)

        if fun in {"/airplay/disconnect", "/airplay/stop"}:
            req = RegisterRequest(**data)
            dev = manager.get(req.device_id)
            dev.stop_airplay()
            await _record_xp_callback_event(
                "airplay_disconnected",
                device_id=req.device_id,
                data={"state": dev.state.value},
            )
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               "state": dev.state.value}, msgid)

        if fun == "/capture/start":
            req = RegisterRequest(**data)
            dev = manager.get(req.device_id)
            dev.start_capture()
            await _record_xp_callback_event(
                "capture_started",
                device_id=req.device_id,
                data={"screen_width": dev.screen_width, "screen_height": dev.screen_height},
            )
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               "screen_width": dev.screen_width,
                               "screen_height": dev.screen_height}, msgid)

        if fun == "/mouse/click":
            req = ClickRequest(**data)
            dev = manager.get(req.device_id)
            dev.click(req.x, req.y)
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               "x": req.x, "y": req.y}, msgid)

        if fun == "/mouse/swipe":
            req = SwipeRequest(**data)
            dev = manager.get(req.device_id)
            dev.swipe(req.x1, req.y1, req.x2, req.y2, req.steps, req.step_delay)
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               "x1": req.x1, "y1": req.y1,
                               "x2": req.x2, "y2": req.y2}, msgid)

        if fun in {"/keyboard/type", "/key/type"}:
            req = TypeTextRequest(**data)
            dev = manager.get(req.device_id)
            dev.type_text(req.text, req.char_delay)
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               "text": req.text}, msgid)

        if fun in {"/keyboard/key", "/key/tap"}:
            req = KeyRequest(**data)
            dev = manager.get(req.device_id)
            dev.key_tap(req.keycode, req.modifier)
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               "keycode": req.keycode}, msgid)

        if fun in {"/keyboard/combo", "/key/combo"}:
            req = ComboRequest(**data)
            dev = manager.get(req.device_id)
            dev.key_combo(req.keys, req.modifiers)
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               "keys": req.keys}, msgid)

        if fun == "/batch/click":
            device_ids = _device_ids_from_data(data)
            if not device_ids:
                return xp_err(fun, 400, "No device ids provided", msgid=msgid)
            req = ClickRequest(device_id=device_ids[0], **{
                key: value for key, value in data.items()
                if key in {"x", "y"}
            })
            batch = _run_batch(device_ids, lambda dev: dev.click(req.x, req.y))
            return xp_ok(fun, {"x": req.x, "y": req.y, **batch}, msgid)

        if fun == "/batch/swipe":
            device_ids = _device_ids_from_data(data)
            if not device_ids:
                return xp_err(fun, 400, "No device ids provided", msgid=msgid)
            req = SwipeRequest(device_id=device_ids[0], **{
                key: value for key, value in data.items()
                if key in {"x1", "y1", "x2", "y2", "steps", "step_delay"}
            })
            batch = _run_batch(
                device_ids,
                lambda dev: dev.swipe(req.x1, req.y1, req.x2, req.y2,
                                      req.steps, req.step_delay),
            )
            return xp_ok(fun, {"x1": req.x1, "y1": req.y1,
                               "x2": req.x2, "y2": req.y2, **batch}, msgid)

        if fun in {"/batch/type", "/batch/text"}:
            device_ids = _device_ids_from_data(data)
            if not device_ids:
                return xp_err(fun, 400, "No device ids provided", msgid=msgid)
            req = TypeTextRequest(device_id=device_ids[0], **{
                key: value for key, value in data.items()
                if key in {"text", "char_delay"}
            })
            batch = _run_batch(
                device_ids,
                lambda dev: dev.type_text(req.text, req.char_delay),
            )
            return xp_ok(fun, {"text": req.text, **batch}, msgid)

        if fun == "/pic/screenshot":
            req = ScreenshotRequest(**data)
            payload = _build_screenshot_payload(req)
            raw = payload.pop("_bytes")
            media_type = payload.pop("_media_type")
            if req.binary:
                headers = {
                    "X-iMouse-Fun": fun,
                    "X-iMouse-Msgid": str(msgid),
                    "X-iMouse-Device": req.device_id,
                }
                if payload.get("save_path"):
                    headers["X-iMouse-Save-Path"] = str(payload["save_path"])
                return Response(content=raw, media_type=media_type, headers=headers)
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               **payload}, msgid)

        if fun == "/pic/find-image":
            req = FindImageRequest(**data)
            response = await api_find_image(req)
            payload = _json_response_body(response)
            if payload["data"].get("code") != 0:
                return xp_err(fun, payload["data"].get("code", 6),
                              payload.get("message", "find image failed"), msgid=msgid)
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               **payload["data"]}, msgid)

        if fun == "/pic/find_color":
            req = FindColorRequest(**data)
            response = await api_find_color(req)
            payload = _json_response_body(response)
            if payload["data"].get("code") != 0:
                return xp_err(fun, payload["data"].get("code", 6),
                              payload.get("message", "find color failed"), msgid=msgid)
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               **payload["data"]}, msgid)

        if fun == "/pic/find_colors":
            req = FindColorsRequest(**data)
            response = await api_find_colors(req)
            payload = _json_response_body(response)
            if payload["data"].get("code") != 0:
                return xp_err(fun, payload["data"].get("code", 6),
                              payload.get("message", "find colors failed"), msgid=msgid)
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               **payload["data"]}, msgid)

        if fun == "/pic/ocr":
            req = RegisterRequest(**data)
            dev = manager.get(req.device_id)
            frame = dev.capture_frame()
            screenshot = pil_to_cv2(frame)
            items = ocr(screenshot)
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               "list": _ocr_to_xp_list(items), "texts": items}, msgid)

        if fun == "/pic/find-text":
            req = FindTextRequest(**data)
            response = await api_find_text(req)
            payload = _json_response_body(response)
            if payload["data"].get("code") != 0:
                return xp_err(fun, payload["data"].get("code", 6),
                              payload.get("message", "find text failed"), msgid=msgid)
            return xp_ok(fun, {"device_id": req.device_id, "id": req.device_id,
                               **payload["data"]}, msgid)

    except ValueError as exc:
        return xp_err(fun, 400, str(exc), msgid=msgid)
    except KeyError as exc:
        return xp_err(fun, 404, str(exc), status=404, msgid=msgid)
    except Exception as exc:
        return xp_err(fun, 500, str(exc), msgid=msgid)

    return xp_err(fun, 404, f"Unsupported XP fun: {fun}", status=404, msgid=msgid)


@app.get("/api")
async def xp_api_get(request: Request):
    fun, data, msgid = await _parse_xp_request(request)
    if not fun:
        return xp_err("", 400, "Missing fun")
    return await dispatch_xp_fun(fun, data, msgid)


@app.post("/api")
async def xp_api_post(request: Request):
    fun, data, msgid = await _parse_xp_request(request)
    if not fun:
        return xp_err("", 400, "Missing fun")
    if data.get("_parse_error"):
        return xp_err(fun, 400, f"Failed to parse request body: {data['_parse_error']}",
                      msgid=msgid)
    return await dispatch_xp_fun(fun, data, msgid)


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


@app.get("/api/device/profiles")
async def list_device_profiles():
    """List persisted component profiles for field traceability."""
    return ok({"profiles": manager.list_profiles()})


@app.get("/api/device/profile/{device_id}")
async def get_device_profile(device_id: str):
    """Get a device component profile."""
    try:
        return ok({"device_id": device_id, "profile": manager.get_profile(device_id)})
    except Exception as e:
        return err(15, str(e), status=404)


@app.post("/api/device/profile")
async def set_device_profile(req: DeviceProfileRequest):
    """Persist receiver/capture/HID/iPhone/iOS traceability metadata."""
    try:
        result = manager.set_profile(req.device_id, req.profile)
        return ok(result)
    except Exception as e:
        return err(15, str(e))


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
        result = find_image(screenshot, req.template_path, req.threshold, req.get_region())

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


@app.post("/api/find_colors")
async def api_find_colors(req: FindColorsRequest):
    """Find a multi-point color pattern on the device screen."""
    try:
        dev = manager.get(req.device_id)
        frame = dev.capture_frame()
        screenshot = pil_to_cv2(frame)
        bgr_points = []
        for point in req.points:
            color = point.get("color")
            if not isinstance(color, list) or len(color) != 3:
                raise ValueError("each point requires RGB color")
            bgr_points.append({
                **point,
                "color": [color[2], color[1], color[0]],
            })
        result = find_colors(screenshot, bgr_points, req.tolerance, req.get_region())

        if result is None:
            return ok({"found": False})
        return ok({"found": True, **_color_result_to_rgb(result)})
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
async def api_screenshot(req: ScreenshotRequest):
    """Take a screenshot and return it as base64 or binary."""
    try:
        payload = _build_screenshot_payload(req)
        raw = payload.pop("_bytes")
        media_type = payload.pop("_media_type")
        if req.binary:
            return Response(content=raw, media_type=media_type)
        return ok(payload)
    except Exception as e:
        return err(26, str(e))


# ── WebSocket (iMouse Callbacks) ─────────────────────────────────────────────


async def _xp_websocket_loop(ws: WebSocket, *, path: str) -> None:
    """Shared XP-style WebSocket loop for /ws and /api."""
    await ws.accept()
    client_id = str(id(ws))
    _ws_clients[client_id] = ws

    # Send welcome
    await ws.send_json({
        "event": "connected",
        "client_id": client_id,
        "path": path,
        "last_seq": _callback_seq,
    })

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

            if msg.get("fun"):
                nested = msg.get("data", {})
                payload = dict(nested) if isinstance(nested, dict) else {}
                for key, value in msg.items():
                    if key not in {"data", "fun", "msgid"}:
                        payload.setdefault(key, value)
                fun = str(msg.get("fun", ""))
                try:
                    msgid = int(msg.get("msgid", 0) or 0)
                except (TypeError, ValueError):
                    msgid = 0
                response = await dispatch_xp_fun(
                    fun,
                    _normalize_xp_data(payload),
                    msgid,
                )
                await ws.send_json(_json_response_body(response))

            elif action == "subscribe":
                await ws.send_json({
                    "event": "subscribed",
                    "device_id": device_id,
                    "devices": manager.status_all(),
                    "last_seq": _callback_seq,
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


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """WebSocket for real-time device events (iMouse callback equivalent)."""
    await _xp_websocket_loop(ws, path="/ws")


@app.websocket("/api")
async def xp_api_websocket(ws: WebSocket):
    """XP-compatible WebSocket endpoint using the same /api path as HTTP."""
    await _xp_websocket_loop(ws, path="/api")
