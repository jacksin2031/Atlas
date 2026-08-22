# Atlas Vision Runtime IPC Bridge

"""
Abstract IPC bridge for Vision Runtime event forwarding.

Supports Frame Events, Pipeline Events, Provider Events,
Capture Events, Health Events, and Metrics Events.
"""
from __future__ import annotations

from typing import Any, Callable, Optional

from atlas_vision.events import Event, EventType


class IPCVisionBridge:
    """Abstract IPC bridge for Vision Runtime events."""

    def __init__(self) -> None:
        self._handlers: dict[EventType, list[Callable[[Event], None]]] = {}
        self._dispatched_count = 0

    def register_handler(
        self, event_type: EventType, handler: Callable[[Event], None]
    ) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def dispatch(self, event: Event) -> None:
        handlers = self._handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                pass
        self._dispatched_count += 1

    def dispatch_frame_event(self, event: Event) -> None:
        self.dispatch(event)

    def dispatch_pipeline_event(self, event: Event) -> None:
        self.dispatch(event)

    def dispatch_provider_event(self, event: Event) -> None:
        self.dispatch(event)

    def dispatch_capture_event(self, event: Event) -> None:
        self.dispatch(event)

    def dispatch_health_event(self, event: Event) -> None:
        self.dispatch(event)

    def dispatch_metrics_event(self, event: Event) -> None:
        self.dispatch(event)

    def get_dispatched_count(self) -> int:
        return self._dispatched_count

    def list_event_types(self) -> list[str]:
        return [et.value for et in EventType]
