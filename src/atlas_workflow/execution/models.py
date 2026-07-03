"""Execution models for the workflow runtime.

Per RFC-0304 (Workflow Runtime) and RFC-0303 (Execution).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from atlas_workflow.common import (
    ExecutionState,
    ExecutionMetadata,
    NodeState,
    WorkflowLifecycleState,
)


class ExecutionScope(str, Enum):
    """Scope of an execution unit."""
    SINGLE_NODE = "SingleNode"
    PARALLEL_BRANCH = "ParallelBranch"
    SUB_WORKFLOW = "SubWorkflow"
    FULL_WORKFLOW = "FullWorkflow"


class ExecutionTokenState(str, Enum):
    """State of an execution token."""
    ACTIVE = "Active"
    PAUSED = "Paused"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


@dataclass(frozen=True, slots=True, kw_only=True)
class ExecutionToken:
    """Token for tracking execution state and enabling pause/resume/cancel.

    Per RFC-0304. Provides deterministic execution control.
    """
    token_id: str
    workflow_instance_id: str
    state: ExecutionTokenState = ExecutionTokenState.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    paused_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def pause(self) -> ExecutionToken:
        return ExecutionToken(
            token_id=self.token_id,
            workflow_instance_id=self.workflow_instance_id,
            state=ExecutionTokenState.PAUSED,
            created_at=self.created_at,
            paused_at=datetime.now(timezone.utc),
            metadata=dict(self.metadata),
        )

    def resume(self) -> ExecutionToken:
        return ExecutionToken(
            token_id=self.token_id,
            workflow_instance_id=self.workflow_instance_id,
            state=ExecutionTokenState.ACTIVE,
            created_at=self.created_at,
            paused_at=None,
            metadata=dict(self.metadata),
        )

    def cancel(self) -> ExecutionToken:
        return ExecutionToken(
            token_id=self.token_id,
            workflow_instance_id=self.workflow_instance_id,
            state=ExecutionTokenState.CANCELLED,
            created_at=self.created_at,
            paused_at=self.paused_at,
            metadata=dict(self.metadata),
        )

    @property
    def is_cancelled(self) -> bool:
        return self.state == ExecutionTokenState.CANCELLED

    @property
    def is_paused(self) -> bool:
        return self.state == ExecutionTokenState.PAUSED


@dataclass(frozen=True, slots=True, kw_only=True)
class ExecutionResult:
    """Result of a workflow or node execution."""
    success: bool
    workflow_id: str = ""
    instance_id: str = ""
    node_id: str = ""
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    duration_ms: float | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    retries: int = 0
    state: ExecutionState = ExecutionState.PENDING
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def success_result(
        cls,
        workflow_id: str,
        instance_id: str,
        output: dict[str, Any],
        duration_ms: float | None = None,
        **kwargs: Any,
    ) -> ExecutionResult:
        return cls(
            success=True,
            workflow_id=workflow_id,
            instance_id=instance_id,
            output=output,
            duration_ms=duration_ms,
            state=ExecutionState.COMPLETED,
            **kwargs,
        )

    @classmethod
    def failure_result(
        cls,
        workflow_id: str,
        instance_id: str,
        error: str,
        node_id: str = "",
        duration_ms: float | None = None,
        **kwargs: Any,
    ) -> ExecutionResult:
        return cls(
            success=False,
            workflow_id=workflow_id,
            instance_id=instance_id,
            node_id=node_id,
            error=error,
            duration_ms=duration_ms,
            state=ExecutionState.FAILED,
            **kwargs,
        )


@dataclass
class ExecutionHistory:
    """Append-only history of execution events for a workflow instance.

    Per RFC-0304. Supports recovery and audit.
    """
    workflow_id: str
    instance_id: str
    entries: list[dict[str, Any]] = field(default_factory=list)
    checkpoints: list[dict[str, Any]] = field(default_factory=list)

    def record_event(self, event_type: str, data: dict[str, Any] | None = None) -> None:
        entry = {
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data or {},
        }
        self.entries.append(entry)

    def add_checkpoint(self, checkpoint_data: dict[str, Any]) -> None:
        checkpoint = {
            "checkpoint_id": str(len(self.checkpoints) + 1),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": checkpoint_data,
        }
        self.checkpoints.append(checkpoint)

    def get_last_checkpoint(self) -> dict[str, Any] | None:
        return self.checkpoints[-1] if self.checkpoints else None

    def get_history_since(self, since_index: int) -> list[dict[str, Any]]:
        return list(self.entries[since_index:])

    @property
    def event_count(self) -> int:
        return len(self.entries)

    @property
    def checkpoint_count(self) -> int:
        return len(self.checkpoints)
