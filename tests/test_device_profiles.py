import tempfile
import unittest
from pathlib import Path

from imouse.device_manager import DeviceManager, normalize_device_profile


class DeviceProfileTest(unittest.TestCase):
    def test_normalize_profile_accepts_nested_metadata_and_aliases(self):
        profile = normalize_device_profile({
            "id": "dev_1",
            "manual": True,
            "metadata": {
                "receiver_provider": " uxplay ",
                "capture_method": " window ",
                "hid_provider": "ch9329",
                "port": " COM3 ",
                "iphone_id": " iphone-01 ",
                "ios": "17.7",
                "extra": object(),
            },
        })

        self.assertEqual(profile["receiver_provider"], "uxplay")
        self.assertEqual(profile["capture_method"], "window")
        self.assertEqual(profile["serial_port"], "COM3")
        self.assertEqual(profile["ios_version"], "17.7")
        self.assertIsInstance(profile["extra"], str)
        self.assertNotIn("manual", profile)

    def test_manager_persists_profile_and_applies_to_registered_device(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "device_profiles.json"
            manager = DeviceManager(
                group_store_path=None,
                calibration_store_path=None,
                profile_store_path=str(path),
            )
            manager.set_profile("dev_1", {
                "receiver_provider": "uxplay",
                "capture_method": "window",
                "hid_provider": "ch9329",
                "hid_id": "hid01",
                "serial_port": "COM3",
                "iphone_id": "ip01",
                "ios_version": "17.7",
                "receiver_name": "imouse-dev-01",
            })

            reloaded = DeviceManager(
                group_store_path=None,
                calibration_store_path=None,
                profile_store_path=str(path),
            )
            dev = reloaded.register("dev_1")
            status = reloaded.status_all()[0]

            self.assertEqual(dev.profile["receiver_provider"], "uxplay")
            self.assertEqual(dev.ios_version, "17.7")
            self.assertEqual(reloaded.get_profile("dev_1")["serial_port"], "COM3")
            self.assertEqual(status["component_metadata"]["hid_provider"], "ch9329")
            self.assertEqual(status["iphone_id"], "ip01")
            self.assertEqual(reloaded.list_profiles()[0]["device_id"], "dev_1")


if __name__ == "__main__":
    unittest.main()
