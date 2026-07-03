"""Tests for common state model."""

from __future__ import annotations
import pytest

from atlas_workflow.common.state import (
    WorkflowLifecycleState,
    ExecutionState,
    HealthState,
    NodeState,
)


class TestWorkflowLifecycleState:
    def test_all_states_present(self):
        expected = [
            "Created", "Validated", "Compiled", "Scheduled",
            "Running", "Paused", "Completed", "Failed",
            "Cancelled", "Disposed",
        ]
        actual = [s.value for s in WorkflowLifecycleState]
        for exp in expected:
            assert exp in actual

    def test_state_values(self):
        assert WorkflowLifecycleState.CREATED.value == "Created"
        assert WorkflowLifecycleState.COMPLETED.value == "Completed"
        assert WorkflowLifecycleState.FAILED.value == "Failed"


class TestExecutionState:
    def test_all_states_present(self):
        expected = [
            "Pending", "Queued", "Running", "Completed",
            "Failed", "Skipped", "Cancelled", "TimedOut", "Retrying",
        ]
        actual = [s.value for s in ExecutionState]
        for exp in expected:
            assert exp in actual


class TestHealthState:
    def test_all_states_present(self):
        expected = ["Healthy", "Busy", "Paused", "Recovering", "Failed"]
        actual = [s.value for s in HealthState]
        for exp in expected:
            assert exp in actual


class TestNodeState:
    def test_pending_node_not_terminal(self):
        ns = NodeState(node_id="n1")
        assert ns.state == ExecutionState.PENDING
        assert not ns.is_terminal
        assert not ns.is_successful
        assert not ns.is_failed

    def test_completed_node_is_terminal_and_successful(self):
        ns = NodeState(node_id="n1", state=ExecutionState.COMPLETED)
        assert ns.is_terminal
        assert ns.is_successful
        assert not ns.is_failed

    def test_failed_node_is_terminal_and_failed(self):
        ns = NodeState(node_id="n1", state=ExecutionState.FAILED, error="boom")
        assert ns.is_terminal
        assert not ns.is_successful
        assert ns.is_failed
        assert ns.error == "boom"

    def test_skipped_node_is_terminal(self):
        ns = NodeState(node_id="n1", state=ExecutionState.SKIPPED)
        assert ns.is_terminal
        assert not ns.is_successful

    def test_timed_out_node_is_failed(self):
        ns = NodeState(node_id="n1", state=ExecutionState.TIMED_OUT)
        assert ns.is_terminal
        assert ns.is_failed

    def test_node_with_output(self):
        ns = NodeState(
            node_id="n1",
            state=ExecutionState.COMPLETED,
            output={"result": 42},
            duration_ms=123.4,
        )
        assert ns.output["result"] == 42
        assert ns.duration_ms == 123.4

    def test_node_with_retry_info(self):
        ns = NodeState(
            node_id="n1",
            state=ExecutionState.RETRYING,
            retry_count=2,
            max_retries=3,
        )
        assert ns.retry_count == 2
        assert ns.max_retries == 3
