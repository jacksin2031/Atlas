"""Event bus integration for workflow lifecycle events.

Per RFC-0005 (Runtime Event Bus) and RFC-1001 (Common Event Model).
Publishes all workflow and node lifecycle events.
"""

from __future__ import annotations
from typing import Any, Callable

from atlas_workflow.common import WorkflowEvent, EventType


EventHandler = Callable[[WorkflowEvent], None]


class EventBus:
    """Event bus for publishing workflow lifecycle events.

    Supports subscribing handlers for specific event types or all events.
    All events defined in the mission spec are published:
    WorkflowRegistered, WorkflowValidated, WorkflowCompiled,
    WorkflowStarted, WorkflowPaused, WorkflowResumed,
    WorkflowCompleted, WorkflowCancelled, WorkflowFailed,
    WorkflowRecovered, NodeStarted, NodeCompleted, NodeFailed, NodeSkipped.
    """

    def __init__(self) -> None:
        self._handlers: dict[EventType, list[EventHandler]] = {
            et: [] for et in EventType
        }
        self._all_handlers: list[EventHandler] = []

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Subscribe a handler to a specific event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def subscribe_all(self, handler: EventHandler) -> None:
        """Subscribe a handler to all event types."""
        self._all_handlers.append(handler)

    def unsubscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Unsubscribe a handler from a specific event type."""
        handlers = self._handlers.get(event_type, [])
        if handler in handlers:
            handlers.remove(handler)

    def publish(self, event: WorkflowEvent) -> None:
        """Publish an event to all subscribed handlers."""
        for handler in self._handlers.get(event.event_type, []):
            handler(event)
        for handler in self._all_handlers:
            handler(event)

    def publish_event_type(self, event_type: EventType, **kwargs: Any) -> WorkflowEvent:
        """Convenience method to publish a typed event with data."""
        event = WorkflowEvent(event_type=event_type, **kwargs)
        self.publish(event)
        return event

    def publish_workflow_registered(self, workflow_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.WORKFLOW_REGISTERED, workflow_id=workflow_id, **kwargs)

    def publish_workflow_validated(self, workflow_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.WORKFLOW_VALIDATED, workflow_id=workflow_id, **kwargs)

    def publish_workflow_compiled(self, workflow_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.WORKFLOW_COMPILED, workflow_id=workflow_id, **kwargs)

    def publish_workflow_started(self, workflow_id: str, instance_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.WORKFLOW_STARTED, workflow_id=workflow_id, instance_id=instance_id, **kwargs)

    def publish_workflow_paused(self, workflow_id: str, instance_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.WORKFLOW_PAUSED, workflow_id=workflow_id, instance_id=instance_id, **kwargs)

    def publish_workflow_resumed(self, workflow_id: str, instance_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.WORKFLOW_RESUMED, workflow_id=workflow_id, instance_id=instance_id, **kwargs)

    def publish_workflow_completed(self, workflow_id: str, instance_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.WORKFLOW_COMPLETED, workflow_id=workflow_id, instance_id=instance_id, **kwargs)

    def publish_workflow_cancelled(self, workflow_id: str, instance_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.WORKFLOW_CANCELLED, workflow_id=workflow_id, instance_id=instance_id, **kwargs)

    def publish_workflow_failed(self, workflow_id: str, instance_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.WORKFLOW_FAILED, workflow_id=workflow_id, instance_id=instance_id, **kwargs)

    def publish_workflow_recovered(self, workflow_id: str, instance_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.WORKFLOW_RECOVERED, workflow_id=workflow_id, instance_id=instance_id, **kwargs)

    def publish_node_started(self, workflow_id: str, instance_id: str, node_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.NODE_STARTED, workflow_id=workflow_id, instance_id=instance_id, node_id=node_id, **kwargs)

    def publish_node_completed(self, workflow_id: str, instance_id: str, node_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.NODE_COMPLETED, workflow_id=workflow_id, instance_id=instance_id, node_id=node_id, **kwargs)

    def publish_node_failed(self, workflow_id: str, instance_id: str, node_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.NODE_FAILED, workflow_id=workflow_id, instance_id=instance_id, node_id=node_id, **kwargs)

    def publish_node_skipped(self, workflow_id: str, instance_id: str, node_id: str, **kwargs: Any) -> WorkflowEvent:
        return self.publish_event_type(EventType.NODE_SKIPPED, workflow_id=workflow_id, instance_id=instance_id, node_id=node_id, **kwargs)

    @property
    def handler_counts(self) -> dict[EventType, int]:
        return {et: len(h) for et, h in self._handlers.items()}

    @property
    def all_handler_count(self) -> int:
        return len(self._all_handlers)
