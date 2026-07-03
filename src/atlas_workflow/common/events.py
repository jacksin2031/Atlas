"""Common event model per RFC-1001."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
import uuid


class EventType(str, Enum):
    """Standard event types for workflow lifecycle."""
    # Workflow events
    WORKFLOW_REGISTERED = "WorkflowRegistered"
    WORKFLOW_VALIDATED = "WorkflowValidated"
    WORKFLOW_COMPILED = "WorkflowCompiled"
    WORKFLOW_STARTED = "WorkflowStarted"
    WORKFLOW_PAUSED = "WorkflowPaused"
    WORKFLOW_RESUMED = "WorkflowResumed"
    WORKFLOW_COMPLETED = "WorkflowCompleted"
    WORKFLOW_CANCELLED = "WorkflowCancelled"
    WORKFLOW_FAILED = "WorkflowFailed"
    WORKFLOW_RECOVERED = "WorkflowRecovered"
    # Node events
    NODE_STARTED = "NodeStarted"
    NODE_COMPLETED = "NodeCompleted"
    NODE_FAILED = "NodeFailed"
    NODE_SKIPPED = "NodeSkipped"
    # Execution events
    EXECUTION_CHECKPOINT = "ExecutionCheckpoint"
    EXECUTION_RETRY = "ExecutionRetry"
    EXECUTION_TIMEOUT = "ExecutionTimeout"
    EXECUTION_CANCELLATION_REQUESTED = "ExecutionCancellationRequested"


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowEvent:
    """Immutable event emitted by the workflow runtime."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = EventType.WORKFLOW_STARTED
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    workflow_id: str = ""
    instance_id: str = ""
    node_id: str = ""
    correlation_id: str = ""
    data: dict[str, Any] = field(default_factory=dict)

    def with_data(self, **kwargs: Any) -> WorkflowEvent:
        """Return a copy with additional data fields merged."""
        merged = dict(self.data)
        merged.update(kwargs)
        return WorkflowEvent(
            event_id=self.event_id,
            event_type=self.event_type,
            timestamp=self.timestamp,
            workflow_id=self.workflow_id,
            instance_id=self.instance_id,
            node_id=self.node_id,
            correlation_id=self.correlation_id,
            data=merged,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "workflow_id": self.workflow_id,
            "instance_id": self.instance_id,
            "node_id": self.node_id,
            "correlation_id": self.correlation_id,
            "data": dict(self.data),
        }
