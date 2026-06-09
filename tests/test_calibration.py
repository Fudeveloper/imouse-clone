import tempfile
import unittest
from pathlib import Path

from imouse.calibration import CalibrationProfile
from imouse.device_manager import Device, DeviceManager


class FakeHardware:
    is_open = True

    def __init__(self):
        self.clicks = []
        self.swipes = []

    def click_at(self, x, y, width, height):
        self.clicks.append((x, y, width, height))

    def swipe(self, x1, y1, x2, y2, steps, step_delay, width, height):
        self.swipes.append((x1, y1, x2, y2, steps, step_delay, width, height))


class CalibrationTest(unittest.TestCase):
    def test_profile_maps_active_area_to_target_space(self):
        profile = CalibrationProfile.from_dict({
            "enabled": True,
            "source_width": 200,
            "source_height": 300,
            "active_x": 10,
            "active_y": 20,
            "active_width": 100,
            "active_height": 200,
            "target_width": 1000,
            "target_height": 2000,
        })

        self.assertEqual(profile.map_point(60, 120), (500, 1000, 1000, 2000))
        self.assertEqual(profile.map_point(-100, 999), (0, 2000, 1000, 2000))

    def test_device_click_and_swipe_use_calibration(self):
        hardware = FakeHardware()
        device = Device(device_id="dev_1", hardware=hardware)
        device.calibration = CalibrationProfile.from_dict({
            "enabled": True,
            "source_width": 200,
            "source_height": 300,
            "active_x": 10,
            "active_y": 20,
            "active_width": 100,
            "active_height": 200,
            "target_width": 1000,
            "target_height": 2000,
        })

        device.click(60, 120)
        device.swipe(10, 20, 110, 220, steps=5, step_delay=0.02)

        self.assertEqual(hardware.clicks[0], (500, 1000, 1000, 2000))
        self.assertEqual(hardware.swipes[0], (0, 0, 1000, 2000, 5, 0.02, 1000, 2000))

    def test_device_without_calibration_keeps_screen_dimensions(self):
        hardware = FakeHardware()
        device = Device(device_id="dev_1", hardware=hardware, screen_width=1170, screen_height=2532)

        device.click(100, 200)

        self.assertEqual(hardware.clicks[0], (100, 200, 1170, 2532))

    def test_manager_persists_calibration(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "calibration.json"
            manager = DeviceManager(group_store_path=None, calibration_store_path=str(path))
            manager.set_calibration("dev_1", {
                "enabled": True,
                "source_width": 200,
                "source_height": 300,
                "active_width": 200,
                "active_height": 300,
                "target_width": 1000,
                "target_height": 2000,
            })

            reloaded = DeviceManager(group_store_path=None, calibration_store_path=str(path))
            dev = reloaded.register("dev_1")

            self.assertTrue(dev.calibration.enabled)
            self.assertEqual(dev.calibration.target_width, 1000)
            self.assertEqual(reloaded.get_calibration("dev_1")["target_height"], 2000)


if __name__ == "__main__":
    unittest.main()
