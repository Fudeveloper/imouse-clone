import unittest
from pathlib import Path

from imouse.script_runner import ScriptRunner, load_scenario


class ScenarioExamplesTest(unittest.TestCase):
    def test_example_scenarios_load_and_dry_run(self):
        script_dir = Path("scripts")
        paths = sorted(script_dir.glob("*.json"))
        self.assertGreaterEqual(len(paths), 3)

        for path in paths:
            with self.subTest(path=str(path)):
                scenario = load_scenario(path)
                runner = ScriptRunner(dry_run=True, sleep_func=lambda _seconds: None)
                summary = runner.run(scenario)
                self.assertTrue(summary["ok"])
                self.assertEqual(summary["failure_count"], 0)
                self.assertEqual(summary["total"], len(scenario["steps"]))

    def test_p1_control_probe_covers_full_single_device_acceptance_path(self):
        scenario = load_scenario("scripts/p1_single_device_control_probe.json")

        actions = []
        records = []

        def walk(steps):
            for step in steps:
                action = step.get("action")
                actions.append(action)
                if action == "record":
                    records.append(step)
                if action == "repeat":
                    walk(step.get("steps", []))

        walk(scenario["steps"])

        self.assertTrue({"screenshot", "click", "swipe", "type", "metrics", "record"}.issubset(actions))
        self.assertGreaterEqual(actions.count("screenshot"), 1)
        self.assertGreaterEqual(actions.count("record"), 5)
        metadata = records[0]
        self.assertIn("receiver_provider", metadata["required_details"])
        self.assertIn("hid_provider", metadata["required_details"])
        self.assertIn("ios_version", metadata["required_details"])
        self.assertIn("EDIT_ME", metadata["forbid_placeholder_values"])
        final = records[-1]
        self.assertEqual(final["name"], "manual P1 final control decision")
        self.assertIn("click_pass", final["required_details"])
        self.assertIn("swipe_pass", final["required_details"])
        self.assertIn("text_pass", final["required_details"])


if __name__ == "__main__":
    unittest.main()
