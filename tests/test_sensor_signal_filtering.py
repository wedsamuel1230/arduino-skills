#!/usr/bin/env python3
"""Behavior-first tests for the sensor-signal-filtering host helper."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/sensor-signal-filtering/scripts/filter_benchmark.py"
sys.path.insert(0, str(SCRIPT.parent))

from filter_benchmark import filter_samples  # noqa: E402


class SensorSignalFilteringTests(unittest.TestCase):
    def test_ema_initializes_from_first_sample_without_zero_bias(self) -> None:
        result = filter_samples([100.0, 100.0, 100.0], "ema", alpha=0.2)

        self.assertEqual(result, [100.0, 100.0, 100.0])

    def test_median_rejects_one_impulsive_adc_spike(self) -> None:
        result = filter_samples([10.0, 10.0, 100.0, 10.0], "median", window=3)

        self.assertEqual(result, [10.0, 10.0, 10.0, 10.0])

    def test_moving_average_has_explicit_warmup_window(self) -> None:
        result = filter_samples([10.0, 20.0, 30.0], "moving-average", window=3)

        self.assertEqual(result, [10.0, 15.0, 20.0])

    def test_ema_step_response_is_bounded_and_monotonic(self) -> None:
        result = filter_samples([0.0, 0.0, 100.0, 100.0], "ema", alpha=0.5)

        self.assertEqual(result, [0.0, 0.0, 50.0, 75.0])
        self.assertTrue(all(0.0 <= value <= 100.0 for value in result))

    def test_invalid_filter_parameters_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            filter_samples([1.0, 2.0], "median", window=2)
        with self.assertRaises(ValueError):
            filter_samples([1.0, 2.0], "ema", alpha=0.0)
        with self.assertRaises(ValueError):
            filter_samples([1.0, 2.0], "unknown")
        with self.assertRaises(ValueError):
            filter_samples([1.0, float("nan")], "ema")
        with self.assertRaises(ValueError):
            filter_samples([1.0, float("inf")], "ema")

    def test_cli_rejects_malformed_samples_with_nonzero_status(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--samples",
                "10,not-a-number",
                "--filter",
                "ema",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("invalid sample list", completed.stderr)

    def test_cli_emits_structured_json_for_agent_and_ci_consumers(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--samples",
                "10,20,30",
                "--filter",
                "median",
                "--window",
                "3",
                "--format",
                "json",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertEqual(payload["filter"], "median")
        self.assertEqual(payload["sample_count"], 3)
        self.assertEqual(payload["filtered"], [10.0, 15.0, 20.0])
        self.assertIn("raw_min", payload["metrics"])


if __name__ == "__main__":
    unittest.main()
