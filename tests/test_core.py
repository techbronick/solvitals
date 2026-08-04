"""Tests for the pure logic: anomaly detection, history handling, formatting.

Run with: python3 -m unittest discover -s tests -v

Network collectors are not tested here -- they are thin wrappers over third
party APIs, and the behaviour worth pinning down is what happens to their
output once it arrives.
"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solpulse import anomalies, config, store  # noqa: E402


class TestAnomalyThresholds(unittest.TestCase):
    def test_upper_threshold_critical_reports_critical_bound(self):
        found = anomalies._check_thresholds({"delinquent_pct": 12.0})
        self.assertEqual(found[0]["severity"], "critical")
        # The expected bound must be the one actually breached, not the warning.
        self.assertEqual(found[0]["expected"], "< 10.0")

    def test_lower_threshold_critical_reports_critical_bound(self):
        found = anomalies._check_thresholds({"nakamoto_coefficient": 5})
        self.assertEqual(found[0]["severity"], "critical")
        self.assertEqual(found[0]["expected"], "> 10")

    def test_healthy_values_produce_no_findings(self):
        self.assertEqual(anomalies._check_thresholds({
            "delinquent_pct": 1.0, "avg_slot_time_secs": 0.42,
            "tps_non_vote": 2500.0, "nakamoto_coefficient": 18,
        }), [])

    def test_current_nakamoto_does_not_alert(self):
        """Solana's real value sits around 18; alerting on it every run would
        train the reader to ignore alerts."""
        self.assertEqual(anomalies._check_thresholds({"nakamoto_coefficient": 18}), [])

    def test_zero_tps_is_critical_not_ignored(self):
        """A halted chain reports zero non-vote TPS. Treating 0 as missing made
        the halt alert unreachable."""
        found = anomalies._check_thresholds({"tps_non_vote": 0.0})
        self.assertEqual(found[0]["severity"], "critical")

    def test_missing_metrics_are_skipped(self):
        self.assertEqual(anomalies._check_thresholds({"delinquent_pct": None}), [])


class TestAnomalyDeviation(unittest.TestCase):
    def _history(self, values):
        return [{"tvl_usd": v} for v in values]

    def test_flat_baseline_does_not_fire_on_noise(self):
        """A near-flat series has a tiny stdev, so a rounding-level change
        scores hundreds of sigma. It must not alert."""
        history = self._history([1000.0] * 7 + [1000.1])
        found = anomalies._check_deviation({"tvl_usd": 1002.0}, history)
        self.assertEqual(found, [])

    def test_real_move_still_fires(self):
        history = self._history([1000, 1010, 990, 1005, 995, 1000, 1002, 998])
        found = anomalies._check_deviation({"tvl_usd": 1400.0}, history)
        self.assertTrue(found)
        self.assertEqual(found[0]["severity"], "critical")

    def test_insufficient_history_is_silent(self):
        found = anomalies._check_deviation({"tvl_usd": 5000.0}, self._history([1000, 1001]))
        self.assertEqual(found, [])

    def test_stdev_matches_sample_stdev(self):
        import statistics
        values = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        mean = anomalies._mean(values)
        self.assertAlmostEqual(anomalies._stdev(values, mean), statistics.stdev(values), places=10)


class TestFindingOrder(unittest.TestCase):
    def test_critical_sorts_before_warning(self):
        snapshot = {"chain": {"health": {"status": "ok"}}}
        current = {"delinquent_pct": 12.0, "avg_slot_time_secs": 0.7}
        found = anomalies.detect(snapshot, current, [])
        self.assertEqual([f["severity"] for f in found], ["critical", "warning"])

    def test_unhealthy_rpc_is_critical(self):
        found = anomalies.detect({"chain": {"health": {"status": "behind"}}}, {}, [])
        self.assertEqual(found[0]["metric"], "rpc_health")
        self.assertEqual(found[0]["severity"], "critical")


class TestStore(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False)
        self.tmp.close()
        self._original = config.HISTORY_PATH
        config.HISTORY_PATH = self.tmp.name

    def tearDown(self):
        config.HISTORY_PATH = self._original
        os.unlink(self.tmp.name)

    def test_corrupt_lines_are_skipped(self):
        with open(self.tmp.name, "w") as handle:
            handle.write(json.dumps({"captured_at": "a", "price_usd": 1}) + "\n")
            handle.write("{not json\n")
            handle.write("\n")
            handle.write(json.dumps({"captured_at": "b", "price_usd": 2}) + "\n")
        rows = store.load()
        self.assertEqual([r["captured_at"] for r in rows], ["a", "b"])

    def test_flatten_tolerates_errored_sections(self):
        flat = store._flatten({
            "captured_at": "t",
            "chain": {"performance": {"error": "boom"}, "validators": {}},
            "market": {"price": {"error": "boom"}},
        })
        self.assertEqual(flat["captured_at"], "t")
        self.assertIsNone(flat["tps_non_vote"])
        self.assertIsNone(flat["price_usd"])

    def test_append_then_load_roundtrip(self):
        store.append({"captured_at": "t1", "chain": {}, "market": {}})
        self.assertEqual(len(store.load()), 1)

    def test_missing_file_returns_empty(self):
        config.HISTORY_PATH = "/nonexistent/path/history.jsonl"
        self.assertEqual(store.load(), [])


if __name__ == "__main__":
    unittest.main()
