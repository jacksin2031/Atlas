"""Tests for common event model."""

from __future__ import annotations
import pytest

from atlas_workflow.common.events import WorkflowEvent, EventType


class TestEventType:
    def test_all_workflow_events_exist(self):
        expected = [
            "WorkflowRegistered", "WorkflowValidated", "WorkflowCompiled",
            "WorkflowStarted", "WorkflowPaused", "WorkflowResumed",
            "WorkflowCompleted", "WorkflowCancelled", "WorkflowFailed",
            "WorkflowRecovered",
            "NodeStarted", "NodeCompleted", "NodeFailed", "NodeSkipped",
        ]
        actual = [e.value for e in EventType]
        for exp in expected:
            assert exp in actual, f"Missing event type: {exp}"

    def test_event_type_enum_values(self):
        assert EventType.WORKFLOW_STARTED.value == "WorkflowStarted"
        assert EventType.NODE_COMPLETED.value == "NodeCompleted"


class TestWorkflowEvent:
    def test_event_creation_defaults(self):
        event = WorkflowEvent(
            event_type=EventType.WORKFLOW_STARTED,
            workflow_id="wf-1",
            instance_id="inst-1",
        )
        assert event.workflow_id == "wf-1"
        assert event.instance_id == "inst-1"
        assert event.event_id is not None
        assert event.data == {}

    def test_event_with_data(self):
        event = WorkflowEvent(
            event_type=EventType.NODE_COMPLETED,
            workflow_id="wf-1",
            node_id="node-1",
            data={"duration_ms": 42.0},
        )
        assert event.data["duration_ms"] == 42.0

    def test_event_with_data_method(self):
        event = WorkflowEvent(event_type=EventType.WORKFLOW_STARTED, workflow_id="wf-1")
        updated = event.with_data(extra="value")
        assert updated.data["extra"] == "value"
        assert updated.event_id == event.event_id

    def test_event_to_dict(self):
        event = WorkflowEvent(
            event_type=EventType.NODE_STARTED,
            workflow_id="wf-1",
            instance_id="inst-1",
            node_id="n1",
            data={"key": "val"},
        )
        d = event.to_dict()
        assert d["event_type"] == "NodeStarted"
        assert d["workflow_id"] == "wf-1"
        assert d["node_id"] == "n1"
        assert d["data"]["key"] == "val"
        assert "timestamp" in d

    def test_event_is_frozen(self):
        event = WorkflowEvent(event_type=EventType.WORKFLOW_STARTED, workflow_id="wf-1")
        with pytest.raises(Exception):
            event.workflow_id = "changed"
