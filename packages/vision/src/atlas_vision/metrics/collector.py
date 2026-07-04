# Atlas Vision Runtime Metrics Collector

"""
Metrics collection for frames processed, latency, memory, and provider execution.
"""
from __future__ import annotations

import math
import threading
import time
from typing import Any


class Counter:
    """Thread-safe counter."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._value = 0
        self._lock = threading.Lock()

    def increment(self, amount: int = 1) -> None:
        with self._lock:
            self._value += amount

    @property
    def value(self) -> int:
        with self._lock:
            return self._value

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "value": self.value}


class Gauge:
    """Thread-safe gauge."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._value = 0.0
        self._lock = threading.Lock()

    def set(self, value: float) -> None:
        with self._lock:
            self._value = value

    def increment(self, amount: float = 1.0) -> None:
        with self._lock:
            self._value += amount

    def decrement(self, amount: float = 1.0) -> None:
        with self._lock:
            self._value -= amount

    @property
    def value(self) -> float:
        with self._lock:
            return self._value

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "value": self.value}


class Histogram:
    """Thread-safe histogram with percentile calculation."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._values: list[float] = []
        self._lock = threading.Lock()

    def record(self, value: float) -> None:
        with self._lock:
            self._values.append(value)

    def percentile(self, p: float) -> float:
        with self._lock:
            if not self._values:
                return 0.0
            sorted_vals = sorted(self._values)
            idx = int(len(sorted_vals) * p / 100.0)
            idx = min(idx, len(sorted_vals) - 1)
            return sorted_vals[idx]

    @property
    def count(self) -> int:
        with self._lock:
            return len(self._values)

    @property
    def mean(self) -> float:
        with self._lock:
            if not self._values:
                return 0.0
            return sum(self._values) / len(self._values)

    def to_dict(self) -> dict[str, Any]:
        with self._lock:
            vals = list(self._values)
        return {
            "name": self.name,
            "count": len(vals),
            "mean": sum(vals) / len(vals) if vals else 0.0,
            "p50": self.percentile(50),
            "p95": self.percentile(95),
            "p99": self.percentile(99),
        }


class VisionMetricsCollector:
    """Collects and aggregates Vision Runtime metrics."""

    def __init__(self) -> None:
        self._counters: dict[str, Counter] = {}
        self._gauges: dict[str, Gauge] = {}
        self._histograms: dict[str, Histogram] = {}
        self._lock = threading.Lock()

    def _get_counter(self, name: str) -> Counter:
        if name not in self._counters:
            self._counters[name] = Counter(name)
        return self._counters[name]

    def _get_gauge(self, name: str) -> Gauge:
        if name not in self._gauges:
            self._gauges[name] = Gauge(name)
        return self._gauges[name]

    def _get_histogram(self, name: str) -> Histogram:
        if name not in self._histograms:
            self._histograms[name] = Histogram(name)
        return self._histograms[name]

    def increment(self, name: str, amount: int = 1) -> None:
        self._get_counter(name).increment(amount)

    def set_gauge(self, name: str, value: float) -> None:
        self._get_gauge(name).set(value)

    def record_histogram(self, name: str, value: float) -> None:
        self._get_histogram(name).record(value)

    def collect(self) -> dict[str, Any]:
        with self._lock:
            return {
                "counters": {k: v.to_dict() for k, v in self._counters.items()},
                "gauges": {k: v.to_dict() for k, v in self._gauges.items()},
                "histograms": {k: v.to_dict() for k, v in self._histograms.items()},
            }

    def initialize(self) -> None:
        pass
