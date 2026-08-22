# Atlas AI Runtime Scheduler

"""
Scheduling integration for the AI Runtime.

Integrates with Runtime Scheduler.
Supports Immediate, Interval, Workflow Trigger, Vision Trigger,
IPC Trigger, AI Trigger, Cron Trigger.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional


class TriggerType(Enum):
    """Scheduler trigger types."""

    IMMEDIATE = "immediate"
    INTERVAL = "interval"
    WORKFLOW_TRIGGER = "workflow_trigger"
    VISION_TRIGGER = "vision_trigger"
    IPC_TRIGGER = "ipc_trigger"
    AI_TRIGGER = "ai_trigger"
    CRON = "cron"


@dataclass(frozen=True, slots=True, eq=True)
class ScheduleEntry:
    """A scheduled AI task entry."""

    entry_id: str
    trigger_type: TriggerType
    callback: Optional[str] = None
    interval_seconds: Optional[float] = None
    cron_expression: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "trigger_type": self.trigger_type.value,
            "callback": self.callback,
            "interval_seconds": self.interval_seconds,
            "cron_expression": self.cron_expression,
            "enabled": self.enabled,
            "metadata": dict(self.metadata),
        }


class AIScheduler:
    """Deterministic AI task scheduler."""

    def __init__(self) -> None:
        self._entries: dict[str, ScheduleEntry] = {}
        self._callbacks: dict[str, Callable] = {}
        self._running = False

    def schedule(
        self,
        entry: ScheduleEntry,
        callback: Optional[Callable] = None,
    ) -> None:
        self._entries[entry.entry_id] = entry
        if callback is not None:
            self._callbacks[entry.entry_id] = callback

    def unschedule(self, entry_id: str) -> bool:
        if entry_id in self._entries:
            del self._entries[entry_id]
            self._callbacks.pop(entry_id, None)
            return True
        return False

    def get_entry(self, entry_id: str) -> Optional[ScheduleEntry]:
        return self._entries.get(entry_id)

    def list_entries(self) -> list[str]:
        return list(self._entries.keys())

    def enable(self, entry_id: str) -> bool:
        entry = self._entries.get(entry_id)
        if entry:
            self._entries[entry_id] = ScheduleEntry(
                entry_id=entry.entry_id,
                trigger_type=entry.trigger_type,
                callback=entry.callback,
                interval_seconds=entry.interval_seconds,
                cron_expression=entry.cron_expression,
                metadata=dict(entry.metadata),
                enabled=True,
                created_at=entry.created_at,
            )
            return True
        return False

    def disable(self, entry_id: str) -> bool:
        entry = self._entries.get(entry_id)
        if entry:
            self._entries[entry_id] = ScheduleEntry(
                entry_id=entry.entry_id,
                trigger_type=entry.trigger_type,
                callback=entry.callback,
                interval_seconds=entry.interval_seconds,
                cron_expression=entry.cron_expression,
                metadata=dict(entry.metadata),
                enabled=False,
                created_at=entry.created_at,
            )
            return True
        return False

    def execute_pending(self) -> list[str]:
        executed = []
        for entry_id, entry in self._entries.items():
            if not entry.enabled:
                continue
            callback = self._callbacks.get(entry_id)
            if callback is not None:
                try:
                    callback()
                    executed.append(entry_id)
                except Exception:
                    pass
        return executed

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def entry_count(self) -> int:
        return len(self._entries)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entries": {k: v.to_dict() for k, v in self._entries.items()},
            "running": self._running,
            "entry_count": self.entry_count,
        }
