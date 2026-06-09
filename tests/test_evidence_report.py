import tempfile
import unittest
from pathlib import Path

from imouse.evidence_report import main, recorder_from_jsonl
from imouse.validation import ValidationRecorder


class EvidenceReportTest(unittest.TestCase):
    def test_recorder_from_jsonl_uses_parent_and_stem(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "pilot_4.jsonl"
            recorder = recorder_from_jsonl(path)

            self.assertEqual(recorder.safe_run_id, "pilot_4")
            self.assertEqual(recorder.path, path)

    def test_main_writes_markdown_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = ValidationRecorder("run_1", evidence_dir=Path(tmp))
            recorder.append("click", "fail", details={"category": "hid", "error": "hardware not connected"})
            out_path = Path(tmp) / "report.md"

            code = main([str(recorder.path), "--markdown", str(out_path)])

            self.assertEqual(code, 0)
            text = out_path.read_text(encoding="utf-8")
            self.assertIn("# Validation Run run_1", text)
            self.assertIn("hid: 1", text)


if __name__ == "__main__":
    unittest.main()
