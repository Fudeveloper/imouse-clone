"""Small Python client for the local iMouse XP-compatible API."""

from __future__ import annotations

import json
import itertools
from typing import Any, Callable, Optional
from urllib import request
from urllib.error import HTTPError, URLError


Transport = Callable[[request.Request, float], Any]


class XpApiError(RuntimeError):
    """Raised when the XP-compatible API returns an error response."""

    def __init__(self, message: str, *, status: int = 0,
                 fun: str = "", payload: Optional[dict] = None):
        super().__init__(message)
        self.status = status
        self.fun = fun
        self.payload = payload or {}


class XpApiClient:
    """HTTP JSON client for the XP-style `/api` + `fun` endpoint."""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:9911",
        timeout: float = 5.0,
        transport: Optional[Transport] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._transport = transport
        self._msgids = itertools.count(1)

    def call(self, fun: str, data: Optional[dict] = None,
             msgid: Optional[int] = None) -> dict:
        """Call a XP-style fun and return the decoded JSON response."""
        return self._send(self._build_request(fun, data, msgid))

    def _build_request(
        self,
        fun: str,
        data: Optional[dict] = None,
        msgid: Optional[int] = None,
    ) -> request.Request:
        payload = {
            "fun": fun,
            "msgid": next(self._msgids) if msgid is None else msgid,
            "data": data or {},
        }
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = request.Request(
            f"{self.base_url}/api",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        return req

    def _send(self, req: request.Request) -> dict:
        try:
            if self._transport is None:
                resp = request.urlopen(req, timeout=self.timeout)
            else:
                resp = self._transport(req, self.timeout)
            with resp:
                status = getattr(resp, "status", getattr(resp, "code", 0))
                payload = json.loads(resp.read().decode("utf-8"))
        except HTTPError as exc:
            status = exc.code
            try:
                payload = json.loads(exc.read().decode("utf-8"))
            except Exception:
                payload = {"message": str(exc), "fun": "", "data": {"code": status}}
        except URLError as exc:
            raise XpApiError(f"Cannot connect to {self.base_url}: {exc}") from exc
        except OSError as exc:
            raise XpApiError(f"API request failed: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise XpApiError(f"API returned invalid JSON: {exc}") from exc

        code = payload.get("data", {}).get("code", 0)
        if status >= 400 or code not in (0, None):
            raise XpApiError(
                payload.get("message", f"API error {code}"),
                status=status,
                fun=payload.get("fun", ""),
                payload=payload,
            )
        return payload

    @staticmethod
    def _error_from_raw(status: int, raw: bytes, fun: str,
                        fallback: str) -> XpApiError:
        try:
            payload = json.loads(raw.decode("utf-8"))
            if not isinstance(payload, dict):
                payload = {}
        except Exception:
            payload = {}

        data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
        code = data.get("code", status)
        message = payload.get("message") or fallback
        response_fun = payload.get("fun") or fun
        if not payload:
            payload = {
                "message": message,
                "fun": response_fun,
                "data": {"code": code},
            }
        return XpApiError(
            message,
            status=status,
            fun=response_fun,
            payload=payload,
        )

    def _send_bytes(self, req: request.Request, fun: str) -> bytes:
        try:
            if self._transport is None:
                resp = request.urlopen(req, timeout=self.timeout)
            else:
                resp = self._transport(req, self.timeout)
            with resp:
                status = getattr(resp, "status", getattr(resp, "code", 0))
                raw = resp.read()
        except HTTPError as exc:
            raw = exc.read()
            if isinstance(raw, str):
                raw = raw.encode("utf-8")
            raise self._error_from_raw(
                exc.code,
                raw,
                fun,
                str(exc),
            ) from exc
        except URLError as exc:
            raise XpApiError(f"Cannot connect to {self.base_url}: {exc}") from exc
        except OSError as exc:
            raise XpApiError(f"API request failed: {exc}") from exc

        if isinstance(raw, str):
            raw = raw.encode("utf-8")
        if status >= 400:
            raise self._error_from_raw(status, raw, fun, f"API error {status}")
        return raw

    def list_devices(self) -> list[dict]:
        return self.call("/device/list")["data"].get("devices", [])

    def register_device(self, device_id: str) -> dict:
        return self.call("/device/register", {"id": device_id})["data"]

    def remove_device(self, device_id: str) -> dict:
        return self.call("/device/remove", {"id": device_id})["data"]

    def scan_hardware(self) -> list[dict]:
        return self.call("/hardware/scan")["data"].get("devices", [])

    def list_groups(self) -> list[dict]:
        return self.call("/group/list")["data"].get("groups", [])

    def save_group(self, name: str, device_ids: list[str]) -> dict:
        return self.call("/group/save", {"name": name, "ids": device_ids})["data"]["group"]

    def remove_group(self, name: str) -> dict:
        return self.call("/group/remove", {"name": name})["data"]

    def list_callbacks(self, after_seq: int = 0, limit: int = 50) -> dict:
        return self.call("/callback/list", {"after_seq": after_seq, "limit": limit})["data"]

    def push_callback(
        self,
        event: str,
        data: Optional[dict] = None,
        *,
        device_id: str = "",
        source: str = "client",
        severity: str = "info",
    ) -> dict:
        return self.call("/callback/push", {
            "event": event,
            "id": device_id,
            "source": source,
            "severity": severity,
            "data": data or {},
        })["data"]["event"]

    def clear_callbacks(self) -> dict:
        return self.call("/callback/clear")["data"]

    def get_config(self, key: str = "") -> dict:
        data = {"key": key} if key else {}
        return self.call("/config/get", data)["data"]

    def set_config(self, config: dict | None = None, **values: Any) -> dict:
        payload = dict(config or {})
        payload.update(values)
        return self.call("/config/set", {"config": payload})["data"]["config"]

    def list_users(self) -> list[dict]:
        return self.call("/user/list")["data"].get("users", [])

    def get_user(self, user_id: str = "") -> dict:
        data = {"id": user_id} if user_id else {}
        return self.call("/user/get", data)["data"].get("user", {})

    def save_user(self, user_id: str, user: dict | None = None, *, active: bool = False) -> dict:
        payload = dict(user or {})
        payload.setdefault("user_id", user_id)
        return self.call("/user/set", {"user": payload, "active": active})["data"]["user"]

    def switch_user(self, user_id: str) -> dict:
        return self.call("/user/switch", {"id": user_id})["data"]

    def remove_user(self, user_id: str) -> dict:
        return self.call("/user/remove", {"id": user_id})["data"]

    def list_shortcuts(self) -> list[dict]:
        return self.call("/shortcut/list")["data"].get("shortcuts", [])

    def get_shortcut(self, name: str) -> dict:
        return self.call("/shortcut/get", {"name": name})["data"].get("shortcut", {})

    def save_shortcut(self, name: str, shortcut: dict | None = None) -> dict:
        payload = dict(shortcut or {})
        payload.setdefault("name", name)
        return self.call("/shortcut/save", {"shortcut": payload})["data"]["shortcut"]

    def run_shortcut(self, name: str, device_id: str = "") -> dict:
        data = {"name": name}
        if device_id:
            data["id"] = device_id
        return self.call("/shortcut/run", data)["data"]

    def set_brightness(self, value: int | float, device_id: str = "") -> dict:
        data: dict[str, Any] = {"value": value}
        if device_id:
            data["id"] = device_id
        return self.call("/shortcut/brightness", data)["data"]

    def list_calibrations(self) -> list[dict]:
        return self.call("/calibration/list")["data"].get("calibrations", [])

    def get_calibration(self, device_id: str) -> dict:
        return self.call("/calibration/get", {"id": device_id})["data"]["calibration"]

    def set_calibration(self, device_id: str, calibration: dict) -> dict:
        return self.call("/calibration/set", {
            "id": device_id,
            "calibration": calibration,
        })["data"]["calibration"]

    def list_profiles(self) -> list[dict]:
        return self.call("/profile/list")["data"].get("profiles", [])

    def get_profile(self, device_id: str) -> dict:
        return self.call("/profile/get", {"id": device_id})["data"]["profile"]

    def set_profile(self, device_id: str, profile: dict) -> dict:
        return self.call("/profile/set", {
            "id": device_id,
            "profile": profile,
        })["data"]["profile"]

    def bind_hardware(self, device_id: str, port: str,
                      baudrate: int = 9600) -> dict:
        return self.call("/device/bind", {
            "id": device_id,
            "port": port,
            "baudrate": baudrate,
        })["data"]

    def unbind_hardware(self, device_id: str) -> dict:
        return self.call("/device/unbind", {"id": device_id})["data"]

    def start_airplay(self, device_id: str) -> dict:
        return self.call("/airplay/connect", {"id": device_id})["data"]

    def stop_airplay(self, device_id: str) -> dict:
        return self.call("/airplay/disconnect", {"id": device_id})["data"]

    def start_capture(self, device_id: str) -> dict:
        return self.call("/capture/start", {"id": device_id})["data"]

    @staticmethod
    def _screenshot_data(
        device_id: str,
        *,
        rect: Optional[list[int]] = None,
        region: Optional[list[int]] = None,
        save_path: str = "",
        jpg: bool = False,
        binary: bool = False,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {"id": device_id}
        if rect is not None:
            data["rect"] = rect
        if region is not None:
            data["region"] = region
        if save_path:
            data["save_path"] = save_path
        if jpg:
            data["jpg"] = True
        if binary:
            data["binary"] = True
        return data

    def screenshot(
        self,
        device_id: str,
        *,
        rect: Optional[list[int]] = None,
        region: Optional[list[int]] = None,
        save_path: str = "",
        jpg: bool = False,
        binary: bool = False,
    ) -> dict | bytes:
        if binary:
            return self.screenshot_bytes(
                device_id,
                rect=rect,
                region=region,
                save_path=save_path,
                jpg=jpg,
            )
        data = self._screenshot_data(
            device_id,
            rect=rect,
            region=region,
            save_path=save_path,
            jpg=jpg,
        )
        return self.call("/pic/screenshot", data)["data"]

    def screenshot_bytes(
        self,
        device_id: str,
        *,
        rect: Optional[list[int]] = None,
        region: Optional[list[int]] = None,
        save_path: str = "",
        jpg: bool = False,
    ) -> bytes:
        data = self._screenshot_data(
            device_id,
            rect=rect,
            region=region,
            save_path=save_path,
            jpg=jpg,
            binary=True,
        )
        req = self._build_request("/pic/screenshot", data)
        return self._send_bytes(req, "/pic/screenshot")

    def click(self, device_id: str, x: int, y: int) -> dict:
        return self.call("/mouse/click", {"id": device_id, "x": x, "y": y})["data"]

    def swipe(self, device_id: str, x1: int, y1: int, x2: int, y2: int,
              steps: int = 20, step_delay: float = 0.01) -> dict:
        return self.call("/mouse/swipe", {
            "id": device_id,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "steps": steps,
            "step_delay": step_delay,
        })["data"]

    def type_text(self, device_id: str, text: str) -> dict:
        return self.call("/keyboard/type", {"id": device_id, "text": text})["data"]

    def batch_click(self, device_ids: list[str], x: int, y: int) -> dict:
        return self.call("/batch/click", {"ids": device_ids, "x": x, "y": y})["data"]

    def group_click(self, group: str, x: int, y: int) -> dict:
        return self.call("/batch/click", {"group": group, "x": x, "y": y})["data"]

    def batch_swipe(self, device_ids: list[str], x1: int, y1: int,
                    x2: int, y2: int, steps: int = 20,
                    step_delay: float = 0.01) -> dict:
        return self.call("/batch/swipe", {
            "ids": device_ids,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "steps": steps,
            "step_delay": step_delay,
        })["data"]

    def group_swipe(self, group: str, x1: int, y1: int,
                    x2: int, y2: int, steps: int = 20,
                    step_delay: float = 0.01) -> dict:
        return self.call("/batch/swipe", {
            "group": group,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "steps": steps,
            "step_delay": step_delay,
        })["data"]

    def batch_type_text(self, device_ids: list[str], text: str) -> dict:
        return self.call("/batch/type", {"ids": device_ids, "text": text})["data"]

    def group_type_text(self, group: str, text: str) -> dict:
        return self.call("/batch/type", {"group": group, "text": text})["data"]

    def find_image(self, device_id: str, template_path: str,
                   threshold: float = 0.8,
                   region: Optional[list[int]] = None) -> dict:
        data: dict[str, Any] = {
            "id": device_id,
            "template_path": template_path,
            "threshold": threshold,
        }
        if region is not None:
            data["region"] = region
        return self.call("/pic/find-image", data)["data"]

    def find_color(self, device_id: str, color: list[int],
                   tolerance: int = 5,
                   region: Optional[list[int]] = None) -> dict:
        data: dict[str, Any] = {
            "id": device_id,
            "color": color,
            "tolerance": tolerance,
        }
        if region is not None:
            data["region"] = region
        return self.call("/pic/find_color", data)["data"]

    def find_colors(self, device_id: str, points: list[dict],
                    tolerance: int = 5,
                    region: Optional[list[int]] = None) -> dict:
        data: dict[str, Any] = {
            "id": device_id,
            "points": points,
            "tolerance": tolerance,
        }
        if region is not None:
            data["region"] = region
        return self.call("/pic/find_colors", data)["data"]

    def ocr(self, device_id: str) -> dict:
        return self.call("/pic/ocr", {"id": device_id})["data"]

    def find_text(self, device_id: str, text: str,
                  case_sensitive: bool = False) -> dict:
        return self.call("/pic/find-text", {
            "id": device_id,
            "text": text,
            "case_sensitive": case_sensitive,
        })["data"]
