import json
import tempfile
import unittest
from pathlib import Path

from imouse.receiver_provider import (
    evaluate_receiver_provider,
    load_receiver_config,
    receiver_provider_brief,
)


def windows_receiver_config(path: Path) -> dict:
    return {
        "route": "windows_receiver",
        "name": "ReceiverX",
        "version": "1.2.3",
        "path": str(path),
        "start_command": f'"{path}" --name imouse-dev-01',
        "airplay_name": "imouse-dev-01",
        "capture_method": "window",
        "window_title": "imouse-dev-01",
        "window_process": "receiverx.exe",
        "license_status": "trial",
    }


class ReceiverProviderTest(unittest.TestCase):
    def test_windows_receiver_config_passes_when_path_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "receiverx.exe"
            exe.write_text("fake", encoding="utf-8")

            report = evaluate_receiver_provider(windows_receiver_config(exe))

        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["route"], "windows_receiver")
        self.assertIn("Receiver provider windows_receiver: ok", receiver_provider_brief(report))

    def test_placeholder_or_missing_path_fails(self):
        report = evaluate_receiver_provider({
            "route": "EDIT_ROUTE_windows_receiver",
            "name": "EDIT_REAL_RECEIVER",
            "version": "1.0",
            "path": "missing.exe",
            "start_command": "missing.exe",
            "airplay_name": "imouse-dev-01",
            "capture_method": "window",
            "window_title": "imouse-dev-01",
        })

        self.assertEqual(report["status"], "fail")
        self.assertIn("placeholder", report["message"])

    def test_load_receiver_config_accepts_receiver_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "receiverx.exe"
            exe.write_text("fake", encoding="utf-8")
            path = Path(tmp) / "receiver.json"
            path.write_text(
                """
{
  "receiver": {
    "route": "windows_receiver",
    "name": "ReceiverX",
    "version": "1.2.3",
    "path": "%s",
    "start_command": "run",
    "airplay_name": "imouse-dev-01",
    "capture_method": "window",
    "window_binding": {"title": "imouse-dev-01"}
  }
}
""" % str(exe).replace("\\", "\\\\"),
                encoding="utf-8",
            )

            config = load_receiver_config(path)

        self.assertEqual(config["route"], "windows_receiver")
        self.assertEqual(config["window_title"], "imouse-dev-01")

    def test_load_receiver_config_accepts_utf8_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "receiverx.exe"
            exe.write_text("fake", encoding="utf-8")
            path = Path(tmp) / "receiver_bom.json"
            payload = {
                "receiver": windows_receiver_config(exe),
            }
            path.write_text("\ufeff" + json.dumps(payload), encoding="utf-8")

            config = load_receiver_config(path)

        self.assertEqual(config["route"], "windows_receiver")


if __name__ == "__main__":
    unittest.main()
