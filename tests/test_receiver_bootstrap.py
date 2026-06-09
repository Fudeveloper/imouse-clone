import tempfile
import unittest
from pathlib import Path

from imouse.receiver_bootstrap import (
    build_receiver_bootstrap_decision,
    main,
    receiver_bootstrap_report,
    write_bootstrap_markdown,
)
from imouse.receiver_provider import evaluate_receiver_provider, receiver_config_from_decision


class ReceiverBootstrapTest(unittest.TestCase):
    def test_windows_receiver_bootstrap_preflights_receiver_but_keeps_p1_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            receiver = Path(tmp) / "receiverx.exe"
            receiver.write_text("fake", encoding="utf-8")

            decision = build_receiver_bootstrap_decision(
                run_id="p1_rx",
                route="windows_receiver",
                receiver_path=str(receiver),
                receiver_name="ReceiverX",
                version="1.2.3",
                airplay_name="imouse-dev-01",
                window_title="imouse-dev-01",
                window_process="receiverx.exe",
            )
            provider = evaluate_receiver_provider(receiver_config_from_decision(decision))
            report = receiver_bootstrap_report(decision)

        self.assertEqual(provider["status"], "ok")
        self.assertTrue(report["ok_for_receiver_preflight"])
        self.assertFalse(report["ready_for_p1"])
        self.assertFalse(decision["decision"]["allowed_to_run_p1"])
        self.assertTrue(report["claims"]["does_not_verify_real_ios_control"])
        self.assertIn("Fill HID", decision["decision"]["open_blockers"][0])

    def test_bootstrap_markdown_keeps_claim_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            receiver = Path(tmp) / "receiverx.exe"
            receiver.write_text("fake", encoding="utf-8")
            decision = build_receiver_bootstrap_decision(
                run_id="p1_rx",
                route="windows_receiver",
                receiver_path=str(receiver),
                receiver_name="ReceiverX",
            )
            report = receiver_bootstrap_report(decision)
            out = write_bootstrap_markdown(report, Path(tmp) / "bootstrap.md", route_decision_path="route.json")
            text = out.read_text(encoding="utf-8")

        self.assertIn("Receiver Route Bootstrap", text)
        self.assertIn("Ready for P1: `False`", text)
        self.assertIn("does not prove screenshot quality", text)
        self.assertIn("visible click/swipe/type observations", text)

    def test_cli_writes_route_decision_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            receiver = Path(tmp) / "receiverx.exe"
            receiver.write_text("fake", encoding="utf-8")
            route_path = Path(tmp) / "route.json"
            md_path = Path(tmp) / "bootstrap.md"

            code = main([
                "--run-id", "p1_rx",
                "--route", "windows_receiver",
                "--receiver-path", str(receiver),
                "--receiver-name", "ReceiverX",
                "--output", str(route_path),
                "--markdown", str(md_path),
            ])

            self.assertEqual(code, 0)
            self.assertTrue(route_path.exists())
            self.assertTrue(md_path.exists())


if __name__ == "__main__":
    unittest.main()
