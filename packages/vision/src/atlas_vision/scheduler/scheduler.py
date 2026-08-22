# Atlas Vision Runtime Scheduler

"""
Vision scheduler supporting 7 trigger types.

Integrates with the Runtime Scheduler for deterministic execution.
"""
from __future__ import annotations

import threading
import time
from enum import Enum
from typing import Any, Callable, Optional


class TriggerType(Enum):
    """Scheduler trigger types."""

    IMMEDIATE = "immediate"
    INTERVAL = "interval"
    FRAME_TRIGGER = "frame_trigger"
    WORKFLOW_TRIGGER = "workflow_trigger"
    AI_TRIGGER = "ai_trigger"
    EVENT_TRIGGER = "event_trigger"
    CRON_TRIGGER = "cron_trigger"


class ScheduleEntry:
    """Immutable schedule entry."""

    def __init__(
        self,
        task_id: str,
        trigger_type: TriggerType,
        callback: Callable[..., Any],
        interval_ms: float = 0,
        cron_expression: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.task_id = task_id
        self.trigger_type = trigger_type
        self.callback = callback
        self.interval_ms = interval_ms
        self.cron_expression = cron_expression
        self.metadata = metadata or {}
        self._running = False
        self._thread: Optional[threading.Thread] = None

    @property
    def is_running(self) -> bool:
        return self._running

    def start(self) -> None:
        if self.trigger_type == TriggerType.IMMEDIATE:
            self._running = True
            self.callback()
            self._running = False
        elif self.trigger_type == TriggerType.INTERVAL:
            self._running = True
            self._thread = threading.Thread(
                target=self._interval_loop, daemon=True
            )
            self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=5.0)
            self._thread = None

    def _interval_loop(self) -> None:
        while self._running:
            try:
                self.callback()
            except Exception:
                pass
            time.sleep(self.interval_ms / 1000.0)


class VisionScheduler:
    """Deterministic vision task scheduler."""

    def __init__(self, metrics: Any = None) -> None:
        self._entries: dict[str, ScheduleEntry] = {}
        self._metrics = metrics
        self._lock = threading.Lock()
        self._running = False

    def schedule(
        self,
        task_id: str,
        trigger_type: TriggerType,
        callback: Callable[..., Any],
        interval_ms: float = 0,
        cron_expression: str = "",
    ) -> None:
        entry = ScheduleEntry(
            task_id=task_id,
            trigger_type=trigger_type,
            callback=callback,
            interval_ms=interval_ms,
            cron_expression=cron_expression,
        )
        with self._lock:
            self._entries[task_id] = entry

    def execute(self, task_id: str) -> None:
        entry = self._entries.get(task_id)
        if entry is None:
            return
        entry.start()

    def stop_task(self, task_id: str) -> None:
        entry = self._entries.get(task_id)
        if entry is not None:
            entry.stop()

    def list_tasks(self) -> list[str]:
        return list(self._entries.keys())

    def stop(self) -> None:
        with self._lock:
            for entry in self._entries.values():
                entry.stop()
            self._entries.clear()

    def health_check(self) -> dict[str, Any]:
        return {
            "total_tasks": len(self._entries),
            "running_tasks": sum(
                1 for e in self._entries.values() if e.is_running
            ),
        }
