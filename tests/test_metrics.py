import unittest

from imouse.metrics import collect_system_metrics


class MetricsTest(unittest.TestCase):
    def test_collect_system_metrics_returns_stable_shape(self):
        metrics = collect_system_metrics(label="round 1", extra={"online_count": 1})

        self.assertEqual(metrics["label"], "round 1")
        self.assertEqual(metrics["extra"]["online_count"], 1)
        self.assertIn("platform", metrics)
        self.assertIn("python", metrics)
        self.assertIn("cpu", metrics)
        self.assertIn("memory", metrics)
        self.assertIn("disk", metrics)
        self.assertGreater(metrics["disk"]["total_bytes"], 0)
        self.assertIn("source", metrics["memory"])


if __name__ == "__main__":
    unittest.main()
