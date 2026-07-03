"""Tests for event bus."""

from __future__ import annotations
import pytest

from atlas_workflow.common import WorkflowEvent, EventType
from atlas_workflow.events import EventBus


class TestEventBus:
    def test_publish_and_receive(self):
        bus = EventBus()
        received = []
        bus.subscribe(EventType.WORKFLOW_STARTED, lambda e: received.append(e))
        bus.publish(WorkflowEvent(event_type=EventType.WORKFLOW_STARTED, workflow_id="wf-1"))
        assert len(received) == 1
        assert received[0].workflow_id == "wf-1"

    def test_subscribe_all(self):
        bus = EventBus()
        received = []
        bus.subscribe_all(lambda e: received.append(e))
        bus.publish(WorkflowEvent(event_type=EventType.WORKFLOW_COMPLETED))
        bus.publish(WorkflowEvent(event_type=EventType.NODE_STARTED))
        assert len(received) == 2

    def test_unsubscribe(self):
        bus = EventBus()
        received = []
        handler = lambda e: received.append(e)
        bus.subscribe(EventType.WORKFLOW_STARTED, handler)
        bus.unsubscribe(EventType.WORKFLOW_STARTED, handler)
        bus.publish(WorkflowEvent(event_type=EventType.WORKFLOW_STARTED))
        assert len(received) == 0

    def test_publish_workflow_started(self):
        bus = EventBus()
        received = []
        bus.subscribe(EventType.WORKFLOW_STARTED, lambda e: received.append(e))
        bus.publish_workflow_started("wf-1", "inst-1")
        assert len(received) == 1
        assert received[0].workflow_id == "wf-1"
        assert received[0].instance_id == "inst-1"

    def test_publish_all_lifecycle_events(self):
        bus = EventBus()
        received = []
        bus.subscribe_all(lambda e: received.append(e))

        bus.publish_workflow_registered("wf-1")
        bus.publish_workflow_validated("wf-1")
        bus.publish_workflow_compiled("wf-1")
        bus.publish_workflow_started("wf-1", "inst-1")
        bus.publish_workflow_paused("wf-1", "inst-1")
        bus.publish_workflow_resumed("wf-1", "inst-1")
        bus.publish_workflow_completed("wf-1", "inst-1")
        bus.publish_workflow_cancelled("wf-1", "inst-1")
        bus.publish_workflow_failed("wf-1", "inst-1")
        bus.publish_workflow_recovered("wf-1", "inst-1")
        bus.publish_node_started("wf-1", "inst-1", "n1")
        bus.publish_node_completed("wf-1", "inst-1", "n1")
        bus.publish_node_failed("wf-1", "inst-1", "n1")
        bus.publish_node_skipped("wf-1", "inst-1", "n1")

        assert len(received) == 14

    def test_handler_counts(self):
        bus = EventBus()
        bus.subscribe(EventType.WORKFLOW_STARTED, lambda e: None)
        bus.subscribe(EventType.WORKFLOW_STARTED, lambda e: None)
        counts = bus.handler_counts
        assert counts[EventType.WORKFLOW_STARTED] == 2

    def test_all_handler_count(self):
        bus = EventBus()
        bus.subscribe_all(lambda e: None)
        bus.subscribe_all(lambda e: None)
        assert bus.all_handler_count == 2
