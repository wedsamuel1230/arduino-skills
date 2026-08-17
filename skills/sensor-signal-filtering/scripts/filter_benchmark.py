#!/usr/bin/env python3
"""Run deterministic, host-side comparisons for common sensor filters.

This helper is a design and TDD aid. It does not replace ADC timing, electrical
measurements, or target-board verification.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from statistics import median
from typing import Iterable, Sequence


FILTER_NAMES = ("moving-average", "median", "ema")


def _validate_samples(samples: Iterable[float]) -> list[float]:
    values = [float(value) for value in samples]
    if any(not math.isfinite(value) for value in values):
        raise ValueError("samples must contain only finite numeric values")
    return values


def _validate_window(window: int, filter_name: str) -> None:
    if window < 1:
        raise ValueError("window must be at least 1")
    if filter_name == "median" and window % 2 == 0:
        raise ValueError("median window must be odd")


def filter_samples(
    samples: Sequence[float],
    filter_name: str,
    *,
    window: int = 3,
    alpha: float = 0.2,
) -> list[float]:
    """Apply one bounded filter with explicit startup behavior.

    Moving-average and median filters use the samples available during
    warm-up; EMA initializes to the first finite sample instead of zero.
    """

    values = _validate_samples(samples)
    if filter_name not in FILTER_NAMES:
        raise ValueError(
            f"filter must be one of: {', '.join(FILTER_NAMES)}"
        )
    _validate_window(window, filter_name)
    if filter_name == "ema" and not 0.0 < alpha <= 1.0:
        raise ValueError("alpha must be greater than 0 and at most 1")

    output: list[float] = []
    history: list[float] = []
    previous: float | None = None
    for value in values:
        if filter_name == "ema":
            if previous is None:
                previous = value
            else:
                previous = alpha * value + (1.0 - alpha) * previous
            output.append(previous)
            continue

        history.append(value)
        if len(history) > window:
            del history[0]
        if filter_name == "median":
            output.append(float(median(history)))
        else:
            output.append(sum(history) / len(history))
    return output


def parse_samples(raw: str) -> list[float]:
    """Parse comma- or whitespace-separated samples without interactive input."""

    tokens = raw.replace(",", " ").split()
    if not tokens:
        raise ValueError("--samples must contain at least one numeric value")
    try:
        return _validate_samples(float(token) for token in tokens)
    except ValueError as exc:
        raise ValueError(f"invalid sample list: {exc}") from exc


def benchmark(
    samples: Sequence[float],
    filter_name: str,
    *,
    window: int = 3,
    alpha: float = 0.2,
) -> dict[str, object]:
    values = _validate_samples(samples)
    filtered = filter_samples(
        values,
        filter_name,
        window=window,
        alpha=alpha,
    )
    return {
        "filter": filter_name,
        "parameters": {"window": window, "alpha": alpha},
        "sample_count": len(values),
        "raw": values,
        "filtered": filtered,
        "metrics": {
            "raw_min": min(values) if values else None,
            "raw_max": max(values) if values else None,
            "filtered_min": min(filtered) if filtered else None,
            "filtered_max": max(filtered) if filtered else None,
        },
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare one deterministic sensor filter against sample data."
    )
    parser.add_argument(
        "--samples",
        required=True,
        help="Comma- or whitespace-separated finite numeric samples.",
    )
    parser.add_argument(
        "--filter",
        dest="filter_name",
        choices=FILTER_NAMES,
        required=True,
        help="Filter under test.",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=3,
        help="Warm-up and history length for moving-average/median (default: 3).",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.2,
        help="EMA weight for the newest sample, in (0, 1] (default: 0.2).",
    )
    parser.add_argument(
        "--format",
        choices=("json", "csv"),
        default="json",
        help="Output format (default: json).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        samples = parse_samples(args.samples)
        payload = benchmark(
            samples,
            args.filter_name,
            window=args.window,
            alpha=args.alpha,
        )
    except ValueError as exc:
        parser.error(str(exc))

    if args.format == "json":
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    writer = csv.writer(sys.stdout)
    writer.writerow(("index", "raw", "filtered"))
    for index, (raw, filtered) in enumerate(
        zip(payload["raw"], payload["filtered"])
    ):
        writer.writerow((index, raw, filtered))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
