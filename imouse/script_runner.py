"""JSON scenario runner for the XP-compatible iMouse prototype."""

from __future__ import annotations

import base64
import io
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from PIL import Image, ImageStat, UnidentifiedImageError

from .metrics import collect_system_metrics
from .validation import ValidationRecorder, make_run_id, safe_token
from .vision import analyze_template_path
from .xp_client import XpApiClient, XpApiError


class ScriptRunnerError(RuntimeError):
    """Raised when a scenario file or step is invalid."""


@dataclass
class StepResult:
    index: int | str
    name: str
    action: str
    status: str
    device_ids: list[str] = field(default_factory=list)
    result: Any = None
    error: str = ""

    def as_dict(self) -> dict:
        return {
            "index": self.index,
            "name": self.name,
            "action": self.action,
            "status": self.status,
            "device_ids": self.device_ids,
            "result": self.result,
            "error": self.error,
        }


class ScriptRunner:
    """Run simple JSON automation scenarios against the XP-compatible API."""

    def __init__(
        self,
        client: Optional[XpApiClient] = None,
        recorder: Optional[ValidationRecorder] = None,
        *,
        dry_run: bool = False,
        sleep_func: Any = time.sleep,
        auto_failure_screenshot: bool = True,
        failure_artifact_dir: Optional[str | Path] = None,
    ):
        self.client = client or XpApiClient()
        self.recorder = recorder
        self.dry_run = dry_run
        self.sleep_func = sleep_func
        self.auto_failure_screenshot = auto_failure_screenshot
        self.failure_artifact_dir = Path(failure_artifact_dir) if failure_artifact_dir else None

    @classmethod
    def from_file(
        cls,
        path: str | Path,
        *,
        base_url: str = "http://127.0.0.1:9911",
        run_id: Optional[str] = None,
        dry_run: bool = False,
    ) -> tuple["ScriptRunner", dict]:
        scenario = load_scenario(path)
        scenario_run_id = run_id or scenario.get("run_id") or make_run_id(Path(path).stem)
        runner = cls(
            client=XpApiClient(base_url=base_url),
            recorder=ValidationRecorder(scenario_run_id),
            dry_run=dry_run,
        )
        return runner, scenario

    def run(self, scenario: dict) -> dict:
        steps = scenario.get("steps")
        if not isinstance(steps, list):
            raise ScriptRunnerError("Scenario requires a steps list")
        results = []
        stop_on_error = bool(scenario.get("stop_on_error", True))
        for index, step in enumerate(steps, start=1):
            result = self.run_step(step, index)
            results.append(result.as_dict())
            if result.status == "fail" and stop_on_error:
                break
        failures = [item for item in results if item["status"] == "fail"]
        summary = {
            "name": scenario.get("name", ""),
            "total": len(results),
            "success_count": len(results) - len(failures),
            "failure_count": len(failures),
            "ok": not failures,
            "results": results,
        }
        if self.recorder:
            self.recorder.append("scenario summary", "pass" if summary["ok"] else "fail", details=summary)
        return summary

    def run_step(self, step: dict, index: int | str) -> StepResult:
        if not isinstance(step, dict):
            raise ScriptRunnerError(f"Step {index} must be an object")
        action = str(step.get("action", "")).strip()
        if not action:
            raise ScriptRunnerError(f"Step {index} missing action")
        name = str(step.get("name", action)).strip() or action
        device_ids = step_device_ids(step)
        try:
            if action == "repeat":
                data = self.run_repeat(step, index)
            elif self.dry_run:
                data = {"dry_run": True, "step": step}
            else:
                data = self.dispatch(step, action)
            if action == "record":
                status = str(step.get("status", "pass")).lower()
            elif action == "repeat":
                status = "pass" if data.get("ok") else "fail"
            elif action == "screenshot" and not self.dry_run:
                quality = screenshot_quality_from_result(data, step)
                if isinstance(data, dict):
                    data = dict(data)
                    data["screenshot_quality"] = quality
                status = "pass" if quality.get("ok") else "fail"
            else:
                status = "pass"
            error = ""
            if action == "screenshot" and status == "fail" and isinstance(data, dict):
                quality = data.get("screenshot_quality", {})
                error = f"screenshot quality failed: {quality.get('reason', 'unknown')}"
            result = StepResult(index, name, action, status, device_ids, data, error=error)
            self._record_step(result, step)
            return result
        except (XpApiError, ScriptRunnerError, ValueError, KeyError) as exc:
            result = StepResult(index, name, action, "fail", device_ids, error=str(exc))
            self._record_step(result, step)
            return result

    def dispatch(self, step: dict, action: str) -> Any:
        if action == "call":
            fun = required_str(step, "fun")
            data = step.get("data") or {}
            if not isinstance(data, dict):
                raise ScriptRunnerError("call data must be an object")
            return self.client.call(fun, data)["data"]

        if action == "wait":
            seconds = float(step.get("seconds", step.get("ms", 0) / 1000))
            if seconds < 0:
                raise ScriptRunnerError("wait seconds cannot be negative")
            self.sleep_func(seconds)
            return {"seconds": seconds}

        if action == "record":
            details = step.get("details") or {}
            if not isinstance(details, dict):
                raise ScriptRunnerError("record details must be an object")
            validate_record_details(step, details)
            data = {"manual": True, "note": step.get("note", ""), **details}
            for key in ("category", "failure_category", "error_type", "observation"):
                if key in step:
                    data[key] = step[key]
            return data

        if action in {"metrics", "system_metrics"}:
            extra = step.get("extra")
            if extra is not None and not isinstance(extra, dict):
                raise ScriptRunnerError("metrics extra must be an object")
            return collect_system_metrics(label=str(step.get("label", step.get("name", ""))), extra=extra)

        if action == "click":
            return self.client.click(required_str(step, "device_id"), int(step["x"]), int(step["y"]))

        if action == "swipe":
            return self.client.swipe(
                required_str(step, "device_id"),
                int(step["x1"]),
                int(step["y1"]),
                int(step["x2"]),
                int(step["y2"]),
                int(step.get("steps", 20)),
                float(step.get("step_delay", 0.01)),
            )

        if action == "type":
            return self.client.type_text(required_str(step, "device_id"), required_str(step, "text"))

        if action == "group_click":
            return self.client.group_click(required_str(step, "group"), int(step["x"]), int(step["y"]))

        if action == "group_swipe":
            return self.client.group_swipe(
                required_str(step, "group"),
                int(step["x1"]),
                int(step["y1"]),
                int(step["x2"]),
                int(step["y2"]),
                int(step.get("steps", 20)),
                float(step.get("step_delay", 0.01)),
            )

        if action == "group_type":
            return self.client.group_type_text(required_str(step, "group"), required_str(step, "text"))

        if action == "screenshot":
            return self.client.screenshot(required_str(step, "device_id"))

        if action == "find_image":
            template_path = required_str(step, "template_path")
            template_quality = template_quality_from_step(step, template_path)
            if template_quality.get("ok") is False:
                raise ScriptRunnerError(f"template quality failed: {template_quality.get('reason', 'unknown')}")
            result = self.client.find_image(
                required_str(step, "device_id"),
                template_path,
                float(step.get("threshold", 0.8)),
                step.get("region"),
            )
            if isinstance(result, dict):
                return {**result, "template_quality": template_quality}
            return result

        if action == "find_image_then_click":
            device_id = required_str(step, "device_id")
            template_path = required_str(step, "template_path")
            template_quality = template_quality_from_step(step, template_path)
            if template_quality.get("ok") is False:
                raise ScriptRunnerError(f"template quality failed: {template_quality.get('reason', 'unknown')}")
            found = self.client.find_image(
                device_id,
                template_path,
                float(step.get("threshold", 0.8)),
                step.get("region"),
            )
            if not found.get("found"):
                raise ScriptRunnerError("template not found")
            x = int(found.get("x", 0))
            y = int(found.get("y", 0))
            clicked = self.client.click(device_id, x, y)
            return {"template_quality": template_quality, "found": found, "click": clicked}

        if action == "find_color":
            return self.client.find_color(
                required_str(step, "device_id"),
                list(step["color"]),
                int(step.get("tolerance", 5)),
                step.get("region"),
            )

        if action == "find_colors":
            points = step.get("points")
            if not isinstance(points, list) or not points:
                raise ScriptRunnerError("find_colors requires a non-empty points list")
            return self.client.find_colors(
                required_str(step, "device_id"),
                points,
                int(step.get("tolerance", 5)),
                step.get("region"),
            )

        if action == "ocr":
            return self.client.ocr(required_str(step, "device_id"))

        if action == "find_text":
            return self.client.find_text(
                required_str(step, "device_id"),
                required_str(step, "text"),
                bool(step.get("case_sensitive", False)),
            )

        raise ScriptRunnerError(f"Unsupported script action: {action}")

    def run_repeat(self, step: dict, index: int | str) -> dict:
        rounds = int(step.get("count", step.get("rounds", 1)))
        if rounds < 1:
            raise ScriptRunnerError("repeat count must be >= 1")
        steps = step.get("steps")
        if not isinstance(steps, list) or not steps:
            raise ScriptRunnerError("repeat requires a non-empty steps list")
        wait_between = float(step.get(
            "wait_between",
            step.get("wait_between_seconds", step.get("interval_seconds", 0)),
        ))
        if wait_between < 0:
            raise ScriptRunnerError("repeat wait_between cannot be negative")
        stop_on_error = bool(step.get("stop_on_error", True))

        round_summaries = []
        all_results = []
        stopped_early = False
        for round_number in range(1, rounds + 1):
            round_results = []
            for child_index, child in enumerate(steps, start=1):
                result = self.run_step(child, f"{index}.{round_number}.{child_index}")
                result_dict = result.as_dict()
                round_results.append(result_dict)
                all_results.append(result_dict)
                if result.status == "fail" and stop_on_error:
                    stopped_early = True
                    break
            failures = [item for item in round_results if item["status"] == "fail"]
            round_summaries.append({
                "round": round_number,
                "ok": not failures,
                "total": len(round_results),
                "failure_count": len(failures),
                "results": round_results,
            })
            if stopped_early:
                break
            if round_number < rounds and wait_between and not self.dry_run:
                self.sleep_func(wait_between)

        failures = [item for item in all_results if item["status"] == "fail"]
        return {
            "requested_rounds": rounds,
            "completed_rounds": len(round_summaries),
            "wait_between": wait_between,
            "stopped_early": stopped_early,
            "total": len(all_results),
            "success_count": len(all_results) - len(failures),
            "failure_count": len(failures),
            "ok": not failures,
            "rounds": round_summaries,
        }

    def _record_step(self, result: StepResult, step: dict) -> None:
        if not self.recorder:
            return
        artifacts = step_artifacts(step)
        auto_artifacts, screenshot_error = self._capture_failure_screenshot(result, step)
        if result.status == "fail" and result.error and result.action != "screenshot":
            details = {"error": result.error, "step": step}
            if screenshot_error:
                details["failure_screenshot_error"] = screenshot_error
        else:
            details = result.result
        artifacts.extend(auto_artifacts)
        if result.status == "pass" and result.action == "screenshot":
            saved, save_error, byte_count = self._save_screenshot_artifact(result, step)
            artifacts.extend(path for path in saved if path not in artifacts)
            details = screenshot_evidence_details(details, saved, save_error, byte_count)
        elif result.status == "fail" and result.action == "screenshot":
            saved, save_error, byte_count = self._save_screenshot_artifact(result, step)
            artifacts.extend(path for path in saved if path not in artifacts)
            details = screenshot_evidence_details(details, saved, save_error, byte_count)
            if isinstance(details, dict) and result.error:
                details["error"] = result.error
        self.recorder.append(
            f"{result.index}. {result.name}",
            result.status,
            device_ids=result.device_ids,
            details=details,
            artifacts=artifacts,
        )

    def _capture_failure_screenshot(self, result: StepResult, step: dict) -> tuple[list[str], str]:
        if (
            not self.auto_failure_screenshot
            or self.dry_run
            or not self.recorder
            or result.status != "fail"
            or result.action == "screenshot"
            or step.get("failure_screenshot") is False
        ):
            return [], ""
        device_id = failure_screenshot_device_id(result, step)
        if not device_id:
            return [], ""
        try:
            data = self.client.screenshot(device_id)
            encoded = data.get("base64") if isinstance(data, dict) else None
            if not isinstance(encoded, str) or not encoded:
                return [], "failure screenshot returned no base64"
            raw = base64.b64decode(encoded)
            path = self._failure_screenshot_path(result, device_id)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            return [str(path)], ""
        except Exception as exc:
            return [], str(exc)

    def _save_screenshot_artifact(self, result: StepResult, step: dict) -> tuple[list[str], str, int]:
        if self.dry_run or not self.recorder or step.get("save_screenshot") is False:
            return [], "", 0
        data = result.result if isinstance(result.result, dict) else {}
        encoded = data.get("base64")
        if not isinstance(encoded, str) or not encoded:
            return [], "screenshot returned no base64", 0
        try:
            raw = base64.b64decode(encoded)
            path = self._screenshot_artifact_path(result, step)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            return [str(path)], "", len(raw)
        except Exception as exc:
            return [], str(exc), 0

    def _screenshot_artifact_path(self, result: StepResult, step: dict) -> Path:
        explicit = step.get("screenshot_artifact") or step.get("screenshot_path")
        if explicit:
            return Path(str(explicit))
        device_id = screenshot_result_device_id(result, step)
        root = self.failure_artifact_dir
        if root is None:
            root = self.recorder.path.parent / f"{self.recorder.safe_run_id}_artifacts"
        filename = "_".join(
            [
                safe_token(str(result.index)),
                "screenshot",
                safe_token(device_id or "device"),
                "capture.png",
            ]
        )
        return root / filename

    def _failure_screenshot_path(self, result: StepResult, device_id: str) -> Path:
        root = self.failure_artifact_dir
        if root is None:
            root = self.recorder.path.parent / f"{self.recorder.safe_run_id}_artifacts"
        filename = "_".join(
            [
                safe_token(str(result.index)),
                safe_token(result.action),
                safe_token(device_id),
                "failure.png",
            ]
        )
        return root / filename


def step_artifacts(step: dict) -> list[str]:
    artifacts = step.get("artifacts") or []
    if isinstance(artifacts, (str, Path)):
        artifacts = [artifacts]
    return [str(item) for item in artifacts]


def screenshot_evidence_details(details: Any, artifacts: list[str], error: str, byte_count: int) -> Any:
    if not isinstance(details, dict):
        return details
    out = dict(details)
    encoded = out.get("base64")
    if artifacts:
        out["screenshot_artifact"] = artifacts[-1]
        out["base64"] = f"<saved screenshot {byte_count} bytes>"
    elif isinstance(encoded, str):
        out["base64"] = f"<base64 {len(encoded)} chars>"
    if error:
        out["screenshot_artifact_error"] = error
    return out


def template_quality_from_step(step: dict, template_path: str) -> dict:
    if step.get("validate_template") is False:
        return {"ok": True, "reason": "validation_disabled", "path": template_path}
    path = Path(template_path)
    if not path.exists():
        return {"ok": True, "reason": "not_local", "path": template_path}
    return analyze_template_path(
        path,
        min_width=int(step.get("template_min_width", 4)),
        min_height=int(step.get("template_min_height", 4)),
        min_stddev=float(step.get("template_min_stddev", 2.0)),
    )


def screenshot_quality_from_result(data: Any, step: dict) -> dict:
    if step.get("validate_screenshot") is False:
        return {"ok": True, "reason": "validation_disabled"}
    encoded = data.get("base64") if isinstance(data, dict) else None
    return analyze_screenshot_base64(
        encoded,
        min_width=int(step.get("min_width", step.get("screenshot_min_width", 16))),
        min_height=int(step.get("min_height", step.get("screenshot_min_height", 16))),
        min_stddev=float(step.get("min_stddev", step.get("screenshot_min_stddev", 1.0))),
        black_luma=float(step.get("black_luma", 4.0)),
        white_luma=float(step.get("white_luma", 251.0)),
    )


def analyze_screenshot_base64(
    encoded: Any,
    *,
    min_width: int = 16,
    min_height: int = 16,
    min_stddev: float = 1.0,
    black_luma: float = 4.0,
    white_luma: float = 251.0,
) -> dict:
    if not isinstance(encoded, str) or not encoded:
        return {"ok": False, "reason": "missing_base64"}
    try:
        raw = base64.b64decode(encoded)
    except Exception as exc:
        return {"ok": False, "reason": "invalid_base64", "error": str(exc)}
    try:
        image = Image.open(io.BytesIO(raw))
        image.load()
    except (OSError, UnidentifiedImageError) as exc:
        return {"ok": False, "reason": "invalid_image", "bytes": len(raw), "error": str(exc)}
    width, height = image.size
    grayscale = image.convert("L")
    stat = ImageStat.Stat(grayscale)
    mean_luma = float(stat.mean[0]) if stat.mean else 0.0
    stddev_luma = float(stat.stddev[0]) if stat.stddev else 0.0
    quality = {
        "ok": True,
        "reason": "ok",
        "width": width,
        "height": height,
        "mode": image.mode,
        "mean_luma": round(mean_luma, 3),
        "stddev_luma": round(stddev_luma, 3),
        "bytes": len(raw),
    }
    if width < min_width or height < min_height:
        quality.update({"ok": False, "reason": "too_small"})
    elif stddev_luma < min_stddev:
        if mean_luma <= black_luma:
            reason = "black_screen"
        elif mean_luma >= white_luma:
            reason = "white_screen"
        else:
            reason = "blank_screen"
        quality.update({"ok": False, "reason": reason})
    return quality


def validate_record_details(step: dict, details: dict) -> None:
    required = normalize_string_list(step.get("required_details"), "required_details")
    missing = []
    for key in required:
        found, value = get_nested_detail(details, key)
        if not found or is_blank_detail(value):
            missing.append(key)
    if missing:
        raise ScriptRunnerError(f"record details missing required field(s): {', '.join(missing)}")

    placeholders = normalize_placeholder_values(step.get("forbid_placeholder_values"))
    if not placeholders:
        return
    hits = find_placeholder_hits(details, placeholders)
    if hits:
        formatted = ", ".join(f"{hit['path']}={hit['value']!r}" for hit in hits[:5])
        raise ScriptRunnerError(f"record details contain placeholder value(s): {formatted}")


def normalize_string_list(value: Any, field_name: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = value
    else:
        raise ScriptRunnerError(f"{field_name} must be a string or list")
    out = []
    for item in items:
        text = str(item).strip()
        if text:
            out.append(text)
    return out


def normalize_placeholder_values(value: Any) -> list[str]:
    if value is True:
        return ["EDIT_ME", "TODO", "TBD"]
    if value in (None, False):
        return []
    return normalize_string_list(value, "forbid_placeholder_values")


def get_nested_detail(details: dict, path: str) -> tuple[bool, Any]:
    current: Any = details
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
            continue
        return False, None
    return True, current


def is_blank_detail(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def find_placeholder_hits(value: Any, placeholders: list[str], path: str = "details") -> list[dict]:
    hits = []
    if isinstance(value, dict):
        for key, child in value.items():
            hits.extend(find_placeholder_hits(child, placeholders, f"{path}.{key}"))
        return hits
    if isinstance(value, list):
        for index, child in enumerate(value):
            hits.extend(find_placeholder_hits(child, placeholders, f"{path}[{index}]"))
        return hits
    if isinstance(value, str):
        lowered = value.lower()
        for placeholder in placeholders:
            token = placeholder.strip()
            if token and token.lower() in lowered:
                hits.append({"path": path, "value": value, "placeholder": token})
                break
    return hits


def required_str(step: dict, key: str) -> str:
    value = str(step.get(key, "")).strip()
    if not value:
        raise ScriptRunnerError(f"{key} is required")
    return value


def step_device_ids(step: dict) -> list[str]:
    ids = []
    if step.get("device_id"):
        ids.append(str(step["device_id"]))
    for key in ("device_ids", "ids"):
        value = step.get(key)
        if isinstance(value, list):
            ids.extend(str(item) for item in value if item)
    if step.get("action") == "repeat" and isinstance(step.get("steps"), list):
        for child in step["steps"]:
            if isinstance(child, dict):
                ids.extend(step_device_ids(child))
    seen = set()
    unique_ids = []
    for item in ids:
        if item in seen:
            continue
        seen.add(item)
        unique_ids.append(item)
    return unique_ids


def screenshot_result_device_id(result: StepResult, step: dict) -> str:
    data = result.result if isinstance(result.result, dict) else {}
    for value in (data.get("device_id"), data.get("id"), step.get("device_id")):
        text = str(value or "").strip()
        if text:
            return text
    if len(result.device_ids) == 1:
        return result.device_ids[0]
    return ""


def failure_screenshot_device_id(result: StepResult, step: dict) -> str:
    for key in ("failure_screenshot_device_id", "screenshot_device_id"):
        value = str(step.get(key, "")).strip()
        if value:
            return value
    value = str(step.get("device_id", "")).strip()
    if value:
        return value
    if len(result.device_ids) == 1:
        return result.device_ids[0]
    return ""


def load_scenario(path: str | Path) -> dict:
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ScriptRunnerError(f"Scenario file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ScriptRunnerError(f"Scenario JSON is invalid: {exc}") from exc
    if not isinstance(raw, dict):
        raise ScriptRunnerError("Scenario root must be an object")
    return raw


def main(argv: Optional[list[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run an iMouse JSON scenario")
    parser.add_argument("scenario", help="Path to JSON scenario file")
    parser.add_argument("--base-url", default="http://127.0.0.1:9911")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    runner, scenario = ScriptRunner.from_file(
        args.scenario,
        base_url=args.base_url,
        run_id=args.run_id or None,
        dry_run=args.dry_run,
    )
    summary = runner.run(scenario)
    if runner.recorder:
        runner.recorder.write_summary_markdown()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
