#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: Copyright 2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
from dataclasses import dataclass
from typing import Any
from typing import Literal

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit(
        "error: numpy is required. Run with a Python environment that has numpy installed, "
        "for example: uv run --with numpy python compare_outputs.py <reference> <actual>"
    ) from exc

MetricDirection = Literal["lower", "higher"]
MetricLevel = Literal["green", "yellow", "red"]

_DTYPE_BY_NAME = {
    "float16": np.float16,
    "float32": np.float32,
    "float64": np.float64,
    "int8": np.int8,
    "uint8": np.uint8,
    "int16": np.int16,
    "uint16": np.uint16,
    "int32": np.int32,
    "uint32": np.uint32,
    "int64": np.int64,
    "uint64": np.uint64,
}


@dataclass(frozen=True)
class MetricThreshold:
    """Green/yellow bands for a single metric."""

    direction: MetricDirection
    green: float
    yellow: float

    def classify(self, value: float) -> MetricLevel:
        if not math.isfinite(value):
            level: MetricLevel = "red"
        elif self.direction == "lower" and value <= self.green:
            level = "green"
        elif self.direction == "lower" and value <= self.yellow:
            level = "yellow"
        elif self.direction == "higher" and value >= self.green:
            level = "green"
        elif self.direction == "higher" and value >= self.yellow:
            level = "yellow"
        else:
            level = "red"
        return level

    def describe(self) -> str:
        operator = "<=" if self.direction == "lower" else ">="
        return f"green {operator} {self.green:.6g}, yellow {operator} {self.yellow:.6g}"


@dataclass(frozen=True)
class MetricResult:
    """Computed metric value and threshold classification."""

    name: str
    value: float
    level: MetricLevel
    threshold: MetricThreshold

    @property
    def passed(self) -> bool:
        return self.level != "red"

    def to_json(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "level": self.level,
            "passed": self.passed,
            "threshold": {
                "direction": self.threshold.direction,
                "green": self.threshold.green,
                "yellow": self.threshold.yellow,
            },
        }


_DEFAULT_FP32_THRESHOLDS = {
    "rel_l2": MetricThreshold(direction="lower", green=3e-6, yellow=1.5e-5),
    "cosine": MetricThreshold(direction="higher", green=0.999999, yellow=0.999995),
    "scale_error": MetricThreshold(direction="lower", green=2e-6, yellow=1e-5),
    "wasserstein_rel": MetricThreshold(direction="lower", green=2e-7, yellow=1e-6),
    "atol_p999": MetricThreshold(direction="lower", green=3e-6, yellow=1e-5),
}

_THRESHOLD_PROFILES = {
    "default-fp32": _DEFAULT_FP32_THRESHOLDS,
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare a reference tensor against an actual tensor using diagnostics metrics. "
            "Supports .npy files and raw .bin files."
        )
    )
    parser.add_argument(
        "reference", type=pathlib.Path, help="Reference/golden tensor file."
    )
    parser.add_argument("actual", type=pathlib.Path, help="Actual output tensor file.")
    parser.add_argument(
        "--bin-dtype",
        choices=sorted(_DTYPE_BY_NAME),
        default="float32",
        help="Data type used for raw .bin files. Default: float32.",
    )
    parser.add_argument(
        "--shape",
        type=_parse_shape,
        help="Shape for raw .bin files, for example 1,1000 or 1x3x224x224. If omitted, .bin files are compared flat.",
    )
    parser.add_argument(
        "--profile",
        choices=sorted(_THRESHOLD_PROFILES),
        default="default-fp32",
        help="Threshold profile used to classify metric levels. Default: default-fp32.",
    )
    parser.add_argument(
        "--eps",
        type=float,
        default=1e-12,
        help="Small denominator guard used by normalized metrics. Default: 1e-12.",
    )
    parser.add_argument(
        "--atol-rtol",
        type=float,
        default=1e-5,
        help="Relative term subtracted before computing atol_p999. Default: 1e-5.",
    )
    parser.add_argument(
        "--require-green",
        action="store_true",
        help="Return failure unless every thresholded metric is green.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of a text table.",
    )
    return parser.parse_args()


def _parse_shape(value: str) -> tuple[int, ...]:
    parts = value.replace("x", ",").split(",")
    try:
        shape = tuple(int(part.strip()) for part in parts if part.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid shape: {value!r}") from exc
    if not shape or any(dim <= 0 for dim in shape):
        raise argparse.ArgumentTypeError(
            f"shape must contain positive dimensions: {value!r}"
        )
    return shape


def _load_tensor(
    path: pathlib.Path, *, bin_dtype: str, shape: tuple[int, ...] | None
) -> np.ndarray:
    if not path.is_file():
        raise FileNotFoundError(f"Tensor file does not exist: {path}")

    if path.suffix == ".npy":
        return np.load(path, allow_pickle=False)

    if path.suffix == ".bin":
        tensor = np.fromfile(path, dtype=_DTYPE_BY_NAME[bin_dtype])
        if shape is None:
            return tensor
        expected_size = math.prod(shape)
        if tensor.size != expected_size:
            raise ValueError(
                f"{path}: raw element count {tensor.size} does not match shape {shape} "
                f"which requires {expected_size} elements."
            )
        return tensor.reshape(shape)

    raise ValueError(
        f"{path}: unsupported suffix {path.suffix!r}; expected .npy or .bin"
    )


def _as_metric_vector(tensor: np.ndarray, *, name: str) -> np.ndarray:
    values = np.asarray(tensor, dtype=np.float64).reshape(-1)
    if values.size == 0:
        raise ValueError(f"{name} tensor is empty.")
    if not np.all(np.isfinite(values)):
        nonfinite_count = int(values.size - np.count_nonzero(np.isfinite(values)))
        raise ValueError(
            f"{name} tensor contains {nonfinite_count} non-finite value(s)."
        )
    return values


def _compute_metric_values(
    reference: np.ndarray, actual: np.ndarray, *, eps: float, atol_rtol: float
) -> dict[str, float]:
    ref = _as_metric_vector(reference, name="reference")
    test = _as_metric_vector(actual, name="actual")
    diff = test - ref

    ref_norm = float(np.linalg.norm(ref))
    test_norm = float(np.linalg.norm(test))
    dot = float(np.dot(ref, test))
    ref_dot = float(np.dot(ref, ref))
    ref_range = float(np.max(ref) - np.min(ref))

    if ref_norm == 0.0 and test_norm == 0.0:
        cosine = 1.0
    else:
        cosine = dot / ((ref_norm * test_norm) + eps)
        cosine = float(np.clip(cosine, -1.0, 1.0))

    if ref_dot == 0.0:
        scale_error = 0.0 if test_norm == 0.0 else 1.0
    else:
        alpha = dot / ref_dot
        scale_error = float(abs(alpha - 1.0))
    adjusted_abs_error = np.maximum(0.0, np.abs(diff) - (atol_rtol * np.abs(ref)))

    return {
        "rel_l2": float(np.linalg.norm(diff) / (ref_norm + eps)),
        "cosine": cosine,
        "scale_error": scale_error,
        "wasserstein_rel": float(
            np.mean(np.abs(np.sort(ref) - np.sort(test))) / (ref_range + eps)
        ),
        "atol_p999": float(np.quantile(adjusted_abs_error, 0.999)),
    }


def _evaluate_metrics(
    values: dict[str, float], thresholds: dict[str, MetricThreshold]
) -> list[MetricResult]:
    return [
        MetricResult(
            name=name,
            value=value,
            level=thresholds[name].classify(value),
            threshold=thresholds[name],
        )
        for name, value in values.items()
    ]


def _summary_stats(reference: np.ndarray, actual: np.ndarray) -> dict[str, float]:
    ref = _as_metric_vector(reference, name="reference")
    test = _as_metric_vector(actual, name="actual")
    abs_diff = np.abs(test - ref)
    return {
        "max_abs_diff": float(np.max(abs_diff)),
        "mean_abs_diff": float(np.mean(abs_diff)),
        "p99_abs_diff": float(np.quantile(abs_diff, 0.99)),
    }


def _build_report(args: argparse.Namespace) -> dict[str, Any]:
    reference = _load_tensor(
        args.reference,
        bin_dtype=args.bin_dtype,
        shape=args.shape,
    )
    actual = _load_tensor(
        args.actual,
        bin_dtype=args.bin_dtype,
        shape=args.shape,
    )
    if reference.shape != actual.shape:
        raise ValueError(
            f"Shape mismatch: reference shape {reference.shape} != actual shape {actual.shape}"
        )

    metric_values = _compute_metric_values(
        reference, actual, eps=args.eps, atol_rtol=args.atol_rtol
    )
    metrics = _evaluate_metrics(metric_values, _THRESHOLD_PROFILES[args.profile])
    passed = (
        all(result.level == "green" for result in metrics)
        if args.require_green
        else all(result.passed for result in metrics)
    )

    return {
        "status": "PASS" if passed else "FAIL",
        "passed": passed,
        "reference": str(args.reference),
        "actual": str(args.actual),
        "shape": list(reference.shape),
        "profile": args.profile,
        "metrics": [result.to_json() for result in metrics],
        "statistics": _summary_stats(reference, actual),
    }


def _format_value(value: float) -> str:
    return f"{value:.8e}"


def _print_text(report: dict[str, Any]) -> None:
    lines = [
        f"status: {report['status']}",
        f"reference: {report['reference']}",
        f"actual: {report['actual']}",
        f"shape: {report['shape']}  profile: {report['profile']}",
        "",
        "metric           value          level   threshold",
        "---------------  -------------  ------  -----------------------------------",
    ]
    for metric in report["metrics"]:
        threshold = MetricThreshold(**metric["threshold"])
        lines.append(
            f"{metric['name']:<15}  {_format_value(metric['value']):>13}  {metric['level']:<6}  {threshold.describe()}"
        )
    lines.extend(
        [
            "",
            "statistic        value",
            "---------------  -------------",
        ]
    )
    for name, value in report["statistics"].items():
        lines.append(f"{name:<15}  {_format_value(value):>13}")
    sys.stdout.write("\n".join(lines) + "\n")


def main() -> int:
    args = _parse_args()
    try:
        report = _build_report(args)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"error: {exc}\n")
        return 2

    if args.json:
        sys.stdout.write(json.dumps(report, indent=2) + "\n")
    else:
        _print_text(report)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
