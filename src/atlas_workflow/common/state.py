"""Common state model per RFC-1002."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class WorkflowLifecycleState(str, Enum):
    """Workflow lifecycle states per RFC-0305."""
    CREATED = "Created"
    VALIDATED = "Validated"
    COMPILED = "Compiled"
    SCHEDULED = "Scheduled"
    RUNNING = "Running"
    PAUSED = "Paused"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
    DISPOSED = "Disposed"


class ExecutionState(str, Enum):
    """Node execution state."""
    PENDING = "Pending"
    QUEUED = "Queued"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    SKIPPED = "Skipped"
    CANCELLED = "Cancelled"
    TIMED_OUT = "TimedOut"
    RETRYING = "Retrying"


class HealthState(str, Enum):
    """Health states per RFC-0306."""
    HEALTHY = "Healthy"
    BUSY = "Busy"
    PAUSED = "Paused"
    RECOVERING = "Recovering"
    FAILED = "Failed"


@dataclass(frozen=True, slots=True, kw_only=True)
class ExecutionMetadata:
    """Immutable execution metadata."""
    workflow_id: str = ""
    instance_id: str = ""
    correlation_id: str = ""
    started_at: datetime | None = None
    completed_at: datetime | None = None
    version: str = "1.0.0"


@dataclass(frozen=True, slots=True, kw_only=True)
class NodeState:
    """State of a single node during execution."""
    node_id: str
    state: ExecutionState = ExecutionState.PENDING
    started_at: datetime | None = None
    completed_at: datetime | None = None
    retry_count: int = 0
    max_retries: int = 0
    error: str | None = None
    output: dict[str, Any] | None = None
    inputs: dict[str, Any] = field(default_factory=dict)
    duration_ms: float | None = None

    @property
    def is_terminal(self) -> bool:
        return self.state in (
            ExecutionState.COMPLETED,
            ExecutionState.FAILED,
            ExecutionState.SKIPPED,
            ExecutionState.CANCELLED,
            ExecutionState.TIMED_OUT,
        )

    @property
    def is_successful(self) -> bool:
        return self.state == ExecutionState.COMPLETED

    @property
    def is_failed(self) -> bool:
        return self.state in (ExecutionState.FAILED, ExecutionState.TIMED_OUT)
