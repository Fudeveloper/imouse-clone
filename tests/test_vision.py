import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from imouse.vision import analyze_template_image, analyze_template_path, find_colors, find_image


class VisionQualityTest(unittest.TestCase):
    def test_template_quality_rejects_low_texture_crop(self):
        image = Image.new("RGB", (24, 24), (128, 128, 128))

        quality = analyze_template_image(image)

        self.assertFalse(quality["ok"])
        self.assertEqual(quality["reason"], "low_texture")

    def test_template_quality_accepts_textured_crop(self):
        image = Image.new("RGB", (24, 24), (40, 90, 180))
        for x in range(12):
            for y in range(24):
                image.putpixel((x, y), (220, 230, 240))

        quality = analyze_template_image(image)

        self.assertTrue(quality["ok"])
        self.assertGreater(quality["stddev_luma"], 2.0)

    def test_template_quality_rejects_too_small_crop(self):
        image = Image.new("RGB", (2, 2), (0, 0, 0))

        quality = analyze_template_image(image)

        self.assertFalse(quality["ok"])
        self.assertEqual(quality["reason"], "too_small")

    def test_template_path_reports_missing_and_valid_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = analyze_template_path(Path(tmp) / "missing.png")
            self.assertFalse(missing["ok"])
            self.assertEqual(missing["reason"], "not_found")

            path = Path(tmp) / "ok.png"
            image = Image.new("RGB", (24, 24), (10, 10, 10))
            for x in range(12):
                for y in range(24):
                    image.putpixel((x, y), (240, 240, 240))
            image.save(path)

            valid = analyze_template_path(path)
            self.assertTrue(valid["ok"])
            self.assertEqual(valid["path"], str(path))

    def test_find_image_region_returns_full_screen_coordinates(self):
        with tempfile.TemporaryDirectory() as tmp:
            template = np.zeros((8, 8, 3), dtype=np.uint8)
            template[:, :4] = [0, 255, 0]
            template[:, 4:] = [255, 0, 0]
            template[2:6, 2:6] = [0, 0, 255]
            screenshot = np.zeros((60, 80, 3), dtype=np.uint8)
            screenshot[20:28, 30:38] = template
            path = Path(tmp) / "target.png"
            cv2.imwrite(str(path), template)

            result = find_image(screenshot, str(path), threshold=0.99, region=(25, 15, 20, 20))

            self.assertIsNotNone(result)
            self.assertEqual(result["x"], 34)
            self.assertEqual(result["y"], 24)
            self.assertEqual(result["region"], [25, 15, 20, 20])

    def test_find_image_region_misses_outside_or_too_small_area(self):
        with tempfile.TemporaryDirectory() as tmp:
            template = np.zeros((8, 8, 3), dtype=np.uint8)
            template[:, :4] = [0, 255, 0]
            template[:, 4:] = [255, 0, 0]
            screenshot = np.zeros((60, 80, 3), dtype=np.uint8)
            screenshot[20:28, 30:38] = template
            path = Path(tmp) / "target.png"
            cv2.imwrite(str(path), template)

            self.assertIsNone(find_image(screenshot, str(path), threshold=0.99, region=(0, 0, 20, 20)))
            self.assertIsNone(find_image(screenshot, str(path), threshold=0.99, region=(30, 20, 4, 4)))

    def test_find_colors_matches_relative_color_pattern(self):
        screenshot = np.zeros((60, 80, 3), dtype=np.uint8)
        screenshot[20, 30] = [10, 100, 200]
        screenshot[20, 35] = [20, 110, 210]
        screenshot[27, 30] = [30, 120, 220]
        points = [
            {"dx": 0, "dy": 0, "color": [10, 100, 200]},
            {"dx": 5, "dy": 0, "color": [20, 110, 210]},
            {"dx": 0, "dy": 7, "color": [30, 120, 220]},
        ]

        result = find_colors(screenshot, points, tolerance=0, region=(25, 15, 20, 20))

        self.assertIsNotNone(result)
        self.assertEqual(result["x"], 30)
        self.assertEqual(result["y"], 20)
        self.assertEqual(result["region"], [25, 15, 20, 20])
        self.assertEqual(len(result["points"]), 3)
        self.assertEqual(result["points"][1]["x"], 35)

    def test_find_colors_returns_none_when_pattern_or_region_does_not_match(self):
        screenshot = np.zeros((60, 80, 3), dtype=np.uint8)
        screenshot[20, 30] = [10, 100, 200]
        screenshot[20, 35] = [20, 110, 210]
        points = [
            {"dx": 0, "dy": 0, "color": [10, 100, 200]},
            {"dx": 5, "dy": 0, "color": [20, 110, 211]},
        ]

        self.assertIsNone(find_colors(screenshot, points, tolerance=0))
        self.assertIsNone(find_colors(screenshot, points, tolerance=2, region=(0, 0, 20, 20)))


if __name__ == "__main__":
    unittest.main()
