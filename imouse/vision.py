"""
Computer vision: image matching and OCR on iPhone screenshots.

OpenCV (cv2.matchTemplate) — find UI elements by template image.
PaddleOCR — read text from screen (same engine iMouse uses).
"""

from __future__ import annotations

import inspect
import math
import os
from pathlib import Path
from typing import Any, Optional

import cv2
import numpy as np
from PIL import Image, ImageStat, UnidentifiedImageError


# ── Template Matching (Find Image) ───────────────────────────────────────────


def analyze_template_image(
    image: Image.Image,
    *,
    min_width: int = 4,
    min_height: int = 4,
    min_stddev: float = 2.0,
) -> dict:
    """Return a lightweight quality report for a template crop."""
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
    }
    if width < min_width or height < min_height:
        quality.update({"ok": False, "reason": "too_small"})
    elif stddev_luma < min_stddev:
        quality.update({"ok": False, "reason": "low_texture"})
    return quality


def analyze_template_path(
    path: str | Path,
    *,
    min_width: int = 4,
    min_height: int = 4,
    min_stddev: float = 2.0,
) -> dict:
    template_path = Path(path)
    try:
        image = Image.open(template_path)
        image.load()
    except FileNotFoundError:
        return {"ok": False, "reason": "not_found", "path": str(template_path)}
    except (OSError, UnidentifiedImageError) as exc:
        return {"ok": False, "reason": "invalid_image", "path": str(template_path), "error": str(exc)}
    quality = analyze_template_image(
        image,
        min_width=min_width,
        min_height=min_height,
        min_stddev=min_stddev,
    )
    quality["path"] = str(template_path)
    return quality


def find_image(
    screenshot: np.ndarray,
    template_path: str,
    threshold: float = 0.8,
    region: Optional[tuple[int, int, int, int]] = None,
) -> Optional[dict]:
    """Find a template image within a screenshot.

    Args:
        screenshot: BGR numpy array (from OpenCV) of the full screen.
        template_path: Path to the template image file (PNG recommended).
        threshold: Match confidence threshold (0.0–1.0). Higher = stricter.
        region: Optional (x, y, w, h) search region in screenshot coordinates.

    Returns:
        {"x": int, "y": int, "confidence": float, "width": int, "height": int}
        or None if no match above threshold.
    """
    template = cv2.imread(template_path)
    if template is None:
        raise FileNotFoundError(f"Template not found: {template_path}")

    # Ensure screenshot is BGR
    if screenshot.ndim == 2:
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_GRAY2BGR)

    offset_x, offset_y = 0, 0
    search_area = screenshot
    if region is not None:
        x, y, w, h = region
        search_area, offset_x, offset_y = crop_region_with_offset(screenshot, x, y, w, h)
        if search_area.size == 0:
            return None
    if search_area.shape[0] < template.shape[0] or search_area.shape[1] < template.shape[1]:
        return None

    result = cv2.matchTemplate(search_area, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        return None

    h, w = template.shape[:2]
    x, y = max_loc
    return {
        "x": offset_x + x + w // 2,   # center
        "y": offset_y + y + h // 2,
        "confidence": float(max_val),
        "width": w,
        "height": h,
        "region": list(region) if region is not None else None,
    }


def find_all_images(
    screenshot: np.ndarray,
    template_path: str,
    threshold: float = 0.8,
) -> list[dict]:
    """Find all occurrences of a template in a screenshot."""
    template = cv2.imread(template_path)
    if template is None:
        raise FileNotFoundError(f"Template not found: {template_path}")

    if screenshot.ndim == 2:
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_GRAY2BGR)

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    h, w = template.shape[:2]
    locations = np.where(result >= threshold)

    matches = []
    # Non-maximum suppression
    for pt in zip(*locations[::-1]):
        # Check if this point is already covered
        too_close = False
        for m in matches:
            if abs(pt[0] - m["x"] + m["width"] // 2) < w // 2 and \
               abs(pt[1] - m["y"] + m["height"] // 2) < h // 2:
                too_close = True
                break
        if too_close:
            continue
        matches.append({
            "x": int(pt[0]) + w // 2,
            "y": int(pt[1]) + h // 2,
            "confidence": float(result[pt[1], pt[0]]),
            "width": w,
            "height": h,
        })
    return matches


# ── Color Search ─────────────────────────────────────────────────────────────


def find_color(
    screenshot: np.ndarray,
    color: tuple[int, int, int],
    tolerance: int = 5,
    region: Optional[tuple[int, int, int, int]] = None,
) -> Optional[dict]:
    """Find a pixel of a specific color in a screenshot.

    Args:
        screenshot: BGR numpy array.
        color: BGR color tuple to find.
        tolerance: Allowed per-channel deviation.
        region: (x, y, w, h) search region, or None for full image.

    Returns:
        {"x": int, "y": int} or None.
    """
    if region:
        x1, y1, w, h = region
        roi = screenshot[y1 : y1 + h, x1 : x1 + w]
        offset_x, offset_y = x1, y1
    else:
        roi = screenshot
        offset_x, offset_y = 0, 0

    lower = np.array([max(0, c - tolerance) for c in color], dtype=np.uint8)
    upper = np.array([min(255, c + tolerance) for c in color], dtype=np.uint8)

    mask = cv2.inRange(roi, lower, upper)
    points = cv2.findNonZero(mask)

    if points is None or len(points) == 0:
        return None

    # Return center of mass
    cx, cy = points.mean(axis=0).flatten()
    return {"x": int(cx) + offset_x, "y": int(cy) + offset_y}


def _point_offset(point: dict) -> tuple[int, int]:
    x = point.get("dx", point.get("x", 0))
    y = point.get("dy", point.get("y", 0))
    return int(x), int(y)


def _point_color(point: dict) -> tuple[int, int, int]:
    color = point.get("color")
    if not isinstance(color, (list, tuple)) or len(color) != 3:
        raise ValueError("each color point requires a 3-channel color")
    return int(color[0]), int(color[1]), int(color[2])


def _pixel_matches(pixel: np.ndarray, color: tuple[int, int, int], tolerance: int) -> bool:
    values = [int(item) for item in pixel[:3]]
    return all(abs(values[idx] - color[idx]) <= tolerance for idx in range(3))


def find_colors(
    screenshot: np.ndarray,
    points: list[dict],
    tolerance: int = 5,
    region: Optional[tuple[int, int, int, int]] = None,
) -> Optional[dict]:
    """Find a multi-point color pattern on a screenshot.

    Points use offsets relative to a returned anchor: {"dx": 0, "dy": 0,
    "color": [B, G, R]}. The first point is used as the search seed.
    """
    if not points:
        raise ValueError("points must not be empty")
    if screenshot.ndim == 2:
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_GRAY2BGR)

    search_area = screenshot
    offset_x, offset_y = 0, 0
    if region is not None:
        x, y, w, h = region
        search_area, offset_x, offset_y = crop_region_with_offset(screenshot, x, y, w, h)
        if search_area.size == 0:
            return None

    normalized = [
        {"dx": dx, "dy": dy, "color": _point_color(point)}
        for point in points
        for dx, dy in [_point_offset(point)]
    ]
    seed = normalized[0]
    seed_color = seed["color"]
    lower = np.array([max(0, c - tolerance) for c in seed_color], dtype=np.uint8)
    upper = np.array([min(255, c + tolerance) for c in seed_color], dtype=np.uint8)
    seed_mask = cv2.inRange(search_area, lower, upper)
    seed_pixels = cv2.findNonZero(seed_mask)
    if seed_pixels is None:
        return None

    height, width = search_area.shape[:2]
    for item in seed_pixels.reshape(-1, 2):
        anchor_x = int(item[0]) - int(seed["dx"])
        anchor_y = int(item[1]) - int(seed["dy"])
        matched = []
        ok = True
        for point in normalized:
            px = anchor_x + int(point["dx"])
            py = anchor_y + int(point["dy"])
            if px < 0 or py < 0 or px >= width or py >= height:
                ok = False
                break
            if not _pixel_matches(search_area[py, px], point["color"], tolerance):
                ok = False
                break
            matched.append({
                "x": offset_x + px,
                "y": offset_y + py,
                "dx": int(point["dx"]),
                "dy": int(point["dy"]),
                "color": list(point["color"]),
            })
        if ok:
            return {
                "x": offset_x + anchor_x,
                "y": offset_y + anchor_y,
                "tolerance": tolerance,
                "points": matched,
                "region": list(region) if region is not None else None,
            }
    return None


# ── OCR (PaddleOCR) ──────────────────────────────────────────────────────────


_paddle_ocr = None  # Lazy singleton


def _project_cache_dir() -> str:
    """Return a writable project-local cache dir for heavy OCR model files."""
    return str(Path(__file__).resolve().parents[1] / ".cache" / "paddlex")


def _get_ocr():
    global _paddle_ocr
    if _paddle_ocr is None:
        os.environ.setdefault("PADDLE_PDX_CACHE_HOME", _project_cache_dir())
        from paddleocr import PaddleOCR

        # PaddleOCR 3.x renamed the old angle-classifier switches.
        sig = inspect.signature(PaddleOCR)
        if "use_angle_cls" in sig.parameters:
            _paddle_ocr = PaddleOCR(lang="ch", use_angle_cls=False, show_log=False)
        else:
            _paddle_ocr = PaddleOCR(lang="ch", use_textline_orientation=False)
    return _paddle_ocr


def _as_point_list(points: Any) -> list[list[float]]:
    arr = np.asarray(points).reshape(-1, 2)
    return [[float(x), float(y)] for x, y in arr.tolist()]


def _looks_like_paddleocr2_line(line: Any) -> bool:
    return (
        isinstance(line, (list, tuple))
        and len(line) >= 2
        and isinstance(line[1], (list, tuple))
        and len(line[1]) >= 2
        and isinstance(line[1][0], str)
    )


def _normalize_ocr_results(results: Any) -> list[dict]:
    """Normalize PaddleOCR 2.x and 3.x result shapes."""
    if not results:
        return []

    # PaddleOCR 3.x returns dict-like OCRResult objects with rec_* fields.
    if isinstance(results, list) and results and hasattr(results[0], "get"):
        normalized: list[dict] = []
        for page in results:
            texts = page.get("rec_texts") or []
            scores = page.get("rec_scores") or []
            boxes = page.get("rec_polys") or page.get("rec_boxes") or []
            for idx, text in enumerate(texts):
                if not text:
                    continue
                box = boxes[idx] if idx < len(boxes) else [[0, 0], [0, 0], [0, 0], [0, 0]]
                score = scores[idx] if idx < len(scores) else 0.0
                normalized.append({
                    "text": str(text),
                    "confidence": float(score),
                    "bbox": _as_point_list(box),
                })
        return normalized

    # PaddleOCR 2.x commonly returns either [line, ...] or [[line, ...]].
    if isinstance(results, list) and results and _looks_like_paddleocr2_line(results[0]):
        lines = results
    elif (
        isinstance(results, list)
        and results
        and isinstance(results[0], list)
        and results[0]
        and _looks_like_paddleocr2_line(results[0][0])
    ):
        lines = results[0]
    else:
        lines = results

    normalized = []
    for line in lines or []:
        try:
            bbox = line[0]
            text = line[1][0]
            confidence = line[1][1]
        except (IndexError, TypeError):
            continue
        normalized.append({
            "text": text,
            "confidence": float(confidence),
            "bbox": bbox,
        })
    return normalized


def ocr(screenshot: np.ndarray) -> list[dict]:
    """Run OCR on a screenshot.

    Args:
        screenshot: BGR or RGB numpy array.

    Returns:
        List of {text, confidence, bbox: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]}.
    """
    engine = _get_ocr()
    ocr_sig = inspect.signature(engine.ocr)
    if "cls" in ocr_sig.parameters:
        results = engine.ocr(screenshot, cls=False)
    else:
        results = engine.ocr(screenshot)
    return _normalize_ocr_results(results)


def find_text(
    screenshot: np.ndarray,
    target: str,
    case_sensitive: bool = False,
) -> Optional[dict]:
    """Find specific text on screen and return its center position.

    Returns:
        {"x": int, "y": int, "text": str, "confidence": float} or None.
    """
    items = ocr(screenshot)
    search = target if case_sensitive else target.lower()

    for item in items:
        text = item["text"] if case_sensitive else item["text"].lower()
        if search in text:
            bbox = item["bbox"]
            # bbox is [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
            xs = [p[0] for p in bbox]
            ys = [p[1] for p in bbox]
            return {
                "x": int((min(xs) + max(xs)) / 2),
                "y": int((min(ys) + max(ys)) / 2),
                "text": item["text"],
                "confidence": item["confidence"],
            }
    return None


# ── Image Utilities ──────────────────────────────────────────────────────────


def pil_to_cv2(img: Image.Image) -> np.ndarray:
    """Convert PIL Image (RGB) to OpenCV numpy array (BGR)."""
    return np.array(img)[:, :, ::-1].copy()


def cv2_to_pil(img: np.ndarray) -> Image.Image:
    """Convert OpenCV numpy array (BGR) to PIL Image (RGB)."""
    return Image.fromarray(img[:, :, ::-1])


def crop_region(screenshot: np.ndarray,
                x: int, y: int, w: int, h: int) -> np.ndarray:
    """Crop a region from a screenshot, clamped to image bounds."""
    cropped, _offset_x, _offset_y = crop_region_with_offset(screenshot, x, y, w, h)
    return cropped


def crop_region_with_offset(screenshot: np.ndarray,
                            x: int, y: int, w: int, h: int) -> tuple[np.ndarray, int, int]:
    """Crop a region and return the clamped image plus x/y offset."""
    ih, iw = screenshot.shape[:2]
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(iw, x + w)
    y2 = min(ih, y + h)
    return screenshot[y1:y2, x1:x2], x1, y1


def save_debug_image(img: np.ndarray, path: str, mark: Optional[dict] = None) -> None:
    """Save an image with optional debug mark (circle at found position)."""
    out = img.copy()
    if mark:
        cv2.circle(out, (mark["x"], mark["y"]), 10, (0, 255, 0), 2)
        label = f"{mark.get('confidence', 0):.2f}"
        cv2.putText(out, label, (mark["x"] + 15, mark["y"]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(path, out)
