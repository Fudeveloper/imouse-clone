import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from imouse.doctor import (
    check_modules,
    check_server,
    run_doctor,
    write_markdown,
)
from imouse.route_decision import decision_template


class FakeResponse:
    status = 200

    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class DoctorTest(unittest.TestCase):
    def test_check_modules_reports_missing_module(self):
        checks = check_modules(["json", "missing_module_for_imouse_doctor"])

        self.assertEqual(checks[0].status, "ok")
        self.assertEqual(checks[1].status, "fail")

    def test_check_server_accepts_xp_device_list(self):
        def fake_urlopen(url, timeout):
            self.assertIn("fun=/dev/list", url)
            self.assertEqual(timeout, 3)
            return FakeResponse({
                "status": 200,
                "fun": "/device/list",
                "data": {"code": 0, "devices": []},
            })

        with patch("imouse.doctor.request.urlopen", fake_urlopen):
            check = check_server("http://127.0.0.1:9911")

        self.assertEqual(check.status, "ok")

    def test_run_doctor_aggregates_failures(self):
        with tempfile.TemporaryDirectory() as tmp, \
             patch("imouse.doctor.find_uxplay", return_value=None), \
             patch("imouse.doctor.shutil.which", return_value=None), \
             patch("imouse.doctor.list_devices", return_value=[]):
            report = run_doctor(root=tmp)

        self.assertEqual(report["overall"], "fail")
        names = {item["name"]: item["status"] for item in report["checks"]}
        self.assertEqual(names["binary:uxplay"], "fail")
        self.assertEqual(names["serial_ports"], "warn")

    def test_route_decision_receiver_provider_avoids_uxplay_hard_fail(self):
        with tempfile.TemporaryDirectory() as tmp, \
             patch("imouse.doctor.find_uxplay", return_value=None), \
             patch("imouse.doctor.shutil.which", return_value=None), \
             patch("imouse.doctor.list_devices", return_value=[]):
            root = Path(tmp)
            receiver_exe = root / "receiverx.exe"
            receiver_exe.write_text("fake", encoding="utf-8")
            decision = decision_template(run_id="p1_receiver", devices=["dev_1"])
            decision["receiver"].update({
                "route": "windows_receiver",
                "name": "ReceiverX",
                "version": "1.2.3",
                "path": str(receiver_exe),
                "start_command": f'"{receiver_exe}" --name imouse-dev-01',
                "airplay_name": "imouse-dev-01",
                "capture_method": "window",
                "window_binding": {
                    "title": "imouse-dev-01",
                    "process": "receiverx.exe",
                    "handle": "",
                },
                "license_status": "trial",
            })
            route_path = root / "route.json"
            route_path.write_text(json.dumps(decision), encoding="utf-8")

            report = run_doctor(root=root, route_decision_path=route_path)

        names = {item["name"]: item["status"] for item in report["checks"]}
        self.assertEqual(names["receiver_provider"], "ok")
        self.assertEqual(names["binary:uxplay"], "warn")
        self.assertNotEqual(report["overall"], "fail")

    def test_write_markdown_report(self):
        report = {
            "overall": "warn",
            "counts": {"ok": 1, "warn": 1, "fail": 0},
            "checks": [
                {"name": "python", "status": "ok", "message": "Python OK", "details": {}},
                {"name": "serial_ports", "status": "warn", "message": "No ports", "details": {}},
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = write_markdown(report, Path(tmp) / "doctor.md")
            text = path.read_text(encoding="utf-8")

        self.assertIn("# iMouse Preflight Doctor", text)
        self.assertIn("serial_ports", text)


if __name__ == "__main__":
    unittest.main()
