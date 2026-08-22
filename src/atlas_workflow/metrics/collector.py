"""Metrics collection for workflow execution.

Per RFC-0321 (Observability). Collects:
- Execution duration
- Node duration
- Queue latency
- Retry count
- Failure count
- Success count
- Parallel branch count
"""

from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any


class MetricsCollector:
    """Collects and reports workflow execution metrics.

    All metrics are accumulated in-memory and queryable.
    Thread-safe for single-threaded workflow execution.
    """

    def __init__(self) -> None:
        self._execution_durations: list[float] = []
        self._node_durations: dict[str, list[float]] = defaultdict(list)
        self._queue_latencies: list[float] = []
        self._retry_counts: dict[str, int] = defaultdict(int)
        self._failure_count: int = 0
        self._success_count: int = 0
        self._parallel_branch_counts: list[int] = []
        self._started_at: datetime | None = None
        self._total_executions: int = 0

    def record_execution_started(self) -> None:
        self._started_at = datetime.now(timezone.utc)
        self._total_executions += 1

    def record_execution_completed(self, duration_ms: float) -> None:
        self._execution_durations.append(duration_ms)
        self._success_count += 1

    def record_execution_failed(self, duration_ms: float) -> None:
        self._execution_durations.append(duration_ms)
        self._failure_count += 1

    def record_node_duration(self, node_id: str, duration_ms: float) -> None:
        self._node_durations[node_id].append(duration_ms)

    def record_queue_latency(self, latency_ms: float) -> None:
        self._queue_latencies.append(latency_ms)

    def record_retry(self, node_id: str) -> None:
        self._retry_counts[node_id] += 1

    def record_parallel_branch(self, branch_count: int) -> None:
        self._parallel_branch_counts.append(branch_count)

    @property
    def execution_count(self) -> int:
        return self._total_executions

    @property
    def success_count(self) -> int:
        return self._success_count

    @property
    def failure_count(self) -> int:
        return self._failure_count

    @property
    def retry_counts(self) -> dict[str, int]:
        return dict(self._retry_counts)

    def get_average_execution_duration_ms(self) -> float | None:
        if not self._execution_durations:
            return None
        return sum(self._execution_durations) / len(self._execution_durations)

    def get_node_duration_stats(self, node_id: str) -> dict[str, Any]:
        durations = self._node_durations.get(node_id, [])
        if not durations:
            return {"count": 0, "avg": None, "min": None, "max": None}
        return {
            "count": len(durations),
            "avg": sum(durations) / len(durations),
            "min": min(durations),
            "max": max(durations),
        }

    def get_total_queue_latency_ms(self) -> float:
        return sum(self._queue_latencies)

    def get_average_queue_latency_ms(self) -> float | None:
        if not self._queue_latencies:
            return None
        return sum(self._queue_latencies) / len(self._queue_latencies)

    def get_average_parallel_branch_count(self) -> float | None:
        if not self._parallel_branch_counts:
            return None
        return sum(self._parallel_branch_counts) / len(self._parallel_branch_counts)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_count": self._total_executions,
            "success_count": self._success_count,
            "failure_count": self._failure_count,
            "average_execution_duration_ms": self.get_average_execution_duration_ms(),
            "total_queue_latency_ms": self.get_total_queue_latency_ms(),
            "average_queue_latency_ms": self.get_average_queue_latency_ms(),
            "retry_counts": dict(self._retry_counts),
            "average_parallel_branch_count": self.get_average_parallel_branch_count(),
            "node_durations": {
                nid: self.get_node_duration_stats(nid)
                for nid in sorted(self._node_durations.keys())
            },
        }

    def reset(self) -> None:
        self._execution_durations.clear()
        self._node_durations.clear()
        self._queue_latencies.clear()
        self._retry_counts.clear()
        self._failure_count = 0
        self._success_count = 0
        self._parallel_branch_counts.clear()
        self._started_at = None
        self._total_executions = 0
