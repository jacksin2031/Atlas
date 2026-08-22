# Atlas AI Runtime Metrics

"""
Metrics collection for the AI Runtime.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class Counter:
    """Simple counter metric."""

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self._value = 0

    def increment(self, amount: int = 1) -> None:
        self._value += amount

    @property
    def value(self) -> int:
        return self._value

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "value": self._value}


class Gauge:
    """Simple gauge metric."""

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self._value = 0.0

    def set(self, value: float) -> None:
        self._value = value

    def increment(self, amount: float = 1.0) -> None:
        self._value += amount

    def decrement(self, amount: float = 1.0) -> None:
        self._value -= amount

    @property
    def value(self) -> float:
        return self._value

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "value": self._value}


class Histogram:
    """Simple histogram metric."""

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self._values: list[float] = []
        self._sum = 0.0
        self._count = 0

    @property
    def count(self) -> int:
        return self._count



    def observe(self, value: float) -> None:
        self._values.append(value)
        self._sum += value
        self._count += 1

    @property
    def average(self) -> float:
        return self._sum / self._count if self._count > 0 else 0.0

    @property
    def min_value(self) -> float:
        return min(self._values) if self._values else 0.0

    @property
    def max_value(self) -> float:
        return max(self._values) if self._values else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "count": self._count,
            "sum": self._sum,
            "average": self.average,
            "min": self.min_value,
            "max": self.max_value,
        }


class AIMetricsCollector:
    """Collects AI Runtime metrics."""

    def __init__(self) -> None:
        self._counters: dict[str, Counter] = {}
        self._gauges: dict[str, Gauge] = {}
        self._histograms: dict[str, Histogram] = {}
        self._initialized = False

    def initialize(self) -> None:
        self._setup_defaults()
        self._initialized = True

    def _setup_defaults(self) -> None:
        self._counters["inference_total"] = Counter("inference_total", "Total inference requests")
        self._counters["inference_failed"] = Counter("inference_failed", "Failed inference requests")
        self._counters["prompt_total"] = Counter("prompt_total", "Total prompt executions")
        self._counters["conversation_total"] = Counter("conversation_total", "Total conversations")
        self._counters["agent_executions"] = Counter("agent_executions", "Total agent executions")
        self._counters["memory_items_stored"] = Counter("memory_items_stored", "Total memory items stored")
        self._counters["embedding_generated"] = Counter("embedding_generated", "Total embeddings generated")
        self._gauges["queue_depth"] = Gauge("queue_depth", "Current inference queue depth")
        self._gauges["model_memory_mb"] = Gauge("model_memory_mb", "Total model memory in MB")
        self._gauges["active_conversations"] = Gauge("active_conversations", "Active conversation count")
        self._gauges["active_agents"] = Gauge("active_agents", "Active agent count")
        self._histograms["inference_latency_ms"] = Histogram("inference_latency_ms", "Inference latency in ms")
        self._histograms["prompt_latency_ms"] = Histogram("prompt_latency_ms", "Prompt latency in ms")
        self._histograms["model_load_time_ms"] = Histogram("model_load_time_ms", "Model load time in ms")
        self._histograms["agent_execution_time_ms"] = Histogram("agent_execution_time_ms", "Agent execution time in ms")

    def increment_counter(self, name: str, amount: int = 1) -> None:
        counter = self._counters.get(name)
        if counter:
            counter.increment(amount)

    def set_gauge(self, name: str, value: float) -> None:
        gauge = self._gauges.get(name)
        if gauge:
            gauge.set(value)

    def observe_histogram(self, name: str, value: float) -> None:
        hist = self._histograms.get(name)
        if hist:
            hist.observe(value)

    def collect(self) -> dict[str, Any]:
        return {
            "counters": {k: v.to_dict() for k, v in self._counters.items()},
            "gauges": {k: v.to_dict() for k, v in self._gauges.items()},
            "histograms": {k: v.to_dict() for k, v in self._histograms.items()},
        }

    def reset(self) -> None:
        self._counters.clear()
        self._gauges.clear()
        self._histograms.clear()
        self._initialized = False
