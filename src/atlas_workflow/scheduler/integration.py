"""Scheduler integration for workflow execution.

Per RFC-0312 (Scheduler). Workflow Runtime MUST NOT own scheduling logic.
Supports: Immediate, Scheduled, Interval, Cron, Manual, Event Trigger, AI Trigger.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class TriggerType(str, Enum):
    """Types of workflow triggers."""
    IMMEDIATE = "Immediate"
    SCHEDULED = "Scheduled"
    INTERVAL = "Interval"
    CRON = "Cron"
    MANUAL = "Manual"
    EVENT_TRIGGER = "EventTrigger"
    AI_TRIGGER = "AITrigger"


@dataclass(frozen=False, slots=True, kw_only=True)
class ScheduleConfig:
    """Configuration for scheduling a workflow execution."""
    trigger_type: TriggerType
    scheduled_at: datetime | None = None
    interval_seconds: float | None = None
    cron_expression: str | None = None
    event_filter: dict[str, Any] | None = None
    ai_criteria: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=False, slots=True, kw_only=True)
class ScheduledExecution:
    """A workflow execution scheduled for later."""
    schedule_id: str
    workflow_id: str
    trigger_type: TriggerType
    config: ScheduleConfig
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    executed_at: datetime | None = None
    status: str = "pending"


class SchedulerInterface(ABC):
    """Abstract interface for workflow schedulers.

    The workflow runtime delegates scheduling to an implementation
    of this interface. Per RFC-0312.
    """

    @abstractmethod
    def schedule(
        self,
        workflow_id: str,
        config: ScheduleConfig,
    ) -> ScheduledExecution:
        """Schedule a workflow execution."""
        ...

    @abstractmethod
    def cancel(self, schedule_id: str) -> bool:
        """Cancel a scheduled execution."""
        ...

    @abstractmethod
    def get_scheduled(self, schedule_id: str) -> ScheduledExecution | None:
        """Get a scheduled execution by ID."""
        ...

    @abstractmethod
    def list_all(self) -> list[ScheduledExecution]:
        """List all scheduled executions."""
        ...


class InMemoryScheduler(SchedulerInterface):
    """In-memory scheduler implementation for testing and simple use cases.

    Supports immediate, manual, and event-triggered workflows.
    Scheduled, interval, cron, and AI triggers are recorded but
    not actively fired (would require a background scheduler).
    """

    def __init__(self) -> None:
        self._schedules: dict[str, ScheduledExecution] = {}
        self._next_id = 0

    def schedule(self, workflow_id: str, config: ScheduleConfig) -> ScheduledExecution:
        self._next_id += 1
        schedule_id = f"schedule-{self._next_id:04d}"
        execution = ScheduledExecution(
            schedule_id=schedule_id,
            workflow_id=workflow_id,
            trigger_type=config.trigger_type,
            config=config,
        )
        self._schedules[schedule_id] = execution
        return execution

    def cancel(self, schedule_id: str) -> bool:
        if schedule_id in self._schedules:
            self._schedules[schedule_id].status = "cancelled"
            return True
        return False

    def get_scheduled(self, schedule_id: str) -> ScheduledExecution | None:
        return self._schedules.get(schedule_id)

    def list_all(self) -> list[ScheduledExecution]:
        return list(self._schedules.values())

    def mark_executed(self, schedule_id: str) -> bool:
        if schedule_id in self._schedules:
            self._schedules[schedule_id].status = "executed"
            self._schedules[schedule_id].executed_at = datetime.now(timezone.utc)
            return True
        return False
