"""
Computer vision: image matching and OCR on iPhone screenshots.

OpenCV (cv2.matchTemplate) — find UI elements by template image.
PaddleOCR — read text from screen (same engine iMouse uses).
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from PIL import Image


# ── Template Matching (Find Image) ───────────────────────────────────────────


def find_image(
    screenshot: np.ndarray,
    template_path: str,
    threshold: float = 0.8,
) -> Optional[dict]:
    """Find a template image within a screenshot.

    Args:
        screenshot: BGR numpy array (from OpenCV) of the full screen.
        template_path: Path to the template image file (PNG recommended).
        threshold: Match confidence threshold (0.0–1.0). Higher = stricter.

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

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        return None

    h, w = template.shape[:2]
    x, y = max_loc
    return {
        "x": x + w // 2,   # center
        "y": y + h // 2,
        "confidence": float(max_val),
        "width": w,
        "height": h,
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


# ── OCR (PaddleOCR) ──────────────────────────────────────────────────────────


_paddle_ocr = None  # Lazy singleton


def _get_ocr():
    global _paddle_ocr
    if _paddle_ocr is None:
        from paddleocr import PaddleOCR
        # cls=False skips text-orientation classifier (faster for upright phone screens)
        _paddle_ocr = PaddleOCR(lang="ch", use_angle_cls=False, show_log=False)
    return _paddle_ocr


def ocr(screenshot: np.ndarray) -> list[dict]:
    """Run OCR on a screenshot.

    Args:
        screenshot: BGR or RGB numpy array.

    Returns:
        List of {text, confidence, bbox: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]}.
    """
    ocr = _get_ocr()
    results = ocr.ocr(screenshot, cls=False)
    if not results or not results[0]:
        return []

    return [
        {
            "text": line[1][0],
            "confidence": float(line[1][1]),
            "bbox": line[0],
        }
        for line in results[0]
    ]


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
    ih, iw = screenshot.shape[:2]
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(iw, x + w)
    y2 = min(ih, y + h)
    return screenshot[y1:y2, x1:x2]


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
