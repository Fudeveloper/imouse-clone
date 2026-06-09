import tempfile
import unittest
from pathlib import Path

from imouse.operator_worksheet import (
    build_operator_worksheet,
    main,
    parse_devices,
    write_operator_worksheet_markdown,
)


class OperatorWorksheetTest(unittest.TestCase):
    def test_parse_devices_defaults_by_stage(self):
        self.assertEqual(parse_devices("", "p1"), ["dev_1"])
        self.assertEqual(parse_devices("", "p3"), ["dev_1", "dev_2", "dev_3", "dev_4"])

    def test_parse_devices_dedupes_explicit_ids(self):
        self.assertEqual(parse_devices("dev_1, dev_2, dev_1", "p1"), ["dev_1", "dev_2"])

    def test_build_p1_worksheet_shape(self):
        worksheet = build_operator_worksheet(stage="p1", run_id="p1_live", devices=["dev_1"])

        self.assertEqual(worksheet["stage"], "p1")
        self.assertEqual(worksheet["run_id"], "p1_live")
        self.assertEqual(worksheet["device_count"], 1)
        self.assertTrue(worksheet["steps"])
        self.assertIn("scripts/p1_single_device_control_probe.json", worksheet["scripts"])
        self.assertIn("scripts/p1_receiver_capture_probe.json", worksheet["scripts"])
        self.assertTrue(any(item["category"] == "hid_click" for item in worksheet["failure_taxonomy"]))

    def test_write_operator_worksheet_markdown(self):
        worksheet = build_operator_worksheet(stage="p1", run_id="p1_doc", devices=["dev_1"])
        with tempfile.TemporaryDirectory() as tmp:
            out = write_operator_worksheet_markdown(worksheet, Path(tmp) / "worksheet.md")
            text = out.read_text(encoding="utf-8")

        self.assertIn("iMouse Operator Worksheet P1", text)
        self.assertIn("Real iOS control verified: `False`", text)
        self.assertIn("does not write evidence", text)
        self.assertIn("hid_click", text)
        self.assertIn("imouse.acceptance", text)

    def test_main_writes_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "operator.md"

            code = main([
                "--stage",
                "p3",
                "--run-id",
                "pilot4",
                "--devices",
                "dev_1,dev_2,dev_3,dev_4",
                "--output",
                str(out),
            ])

            self.assertEqual(code, 0)
            text = out.read_text(encoding="utf-8")
            self.assertIn("iMouse Operator Worksheet P3", text)
            self.assertIn("pilot4", text)


if __name__ == "__main__":
    unittest.main()
