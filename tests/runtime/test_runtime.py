"""Tests for workflow runtime."""

from __future__ import annotations
import pytest

from atlas_workflow.common import (
    WorkflowLifecycleState,
    WorkflowEvent,
    EventType,
)
from atlas_workflow.runtime import WorkflowRuntime, WorkflowInstance, WorkflowContext
from atlas_workflow.scheduler import TriggerType


class TestWorkflowContext:
    def test_set_and_get_variable(self):
        ctx = WorkflowContext("wf-1", "inst-1")
        ctx.set_variable("counter", 42)
        assert ctx.get_variable("counter") == 42

    def test_get_missing_variable(self):
        ctx = WorkflowContext("wf-1", "inst-1")
        assert ctx.get_variable("missing") is None

    def test_set_and_get_metadata(self):
        ctx = WorkflowContext("wf-1", "inst-1")
        ctx.set_metadata("key", "value")
        assert ctx.get_metadata("key") == "value"

    def test_get_all_variables(self):
        ctx = WorkflowContext("wf-1", "inst-1")
        ctx.set_variable("a", 1)
        ctx.set_variable("b", 2)
        all_vars = ctx.get_all_variables()
        assert all_vars == {"a": 1, "b": 2}

    def test_properties(self):
        ctx = WorkflowContext("wf-1", "inst-1")
        assert ctx.workflow_id == "wf-1"
        assert ctx.instance_id == "inst-1"


class TestWorkflowInstance:
    def test_create_instance(self, sample_graph):
        inst = WorkflowInstance(
            workflow_id="wf-1",
            workflow_name="Test",
            version="1.0.0",
            graph=sample_graph,
            inputs={"data": "value"},
        )
        assert inst.state == WorkflowLifecycleState.CREATED
        assert inst.workflow_id == "wf-1"
        assert inst.context.get_variable("data") == "value"

    def test_instance_lifecycle_states(self, sample_graph):
        inst = WorkflowInstance(
            workflow_id="wf-1",
            workflow_name="Test",
            version="1.0.0",
            graph=sample_graph,
        )
        for state in WorkflowLifecycleState:
            inst.set_state(state)
            assert inst.state == state

    def test_instance_to_dict(self, sample_graph):
        inst = WorkflowInstance(
            workflow_id="wf-1",
            workflow_name="Test",
            version="1.0.0",
            graph=sample_graph,
            inputs={"key": "val"},
        )
        d = inst.to_dict()
        assert d["workflow_id"] == "wf-1"
        assert d["state"] == "Created"
        assert d["inputs"]["key"] == "val"
        assert "instance_id" in d
        assert "created_at" in d

    def test_instance_with_custom_id(self, sample_graph):
        inst = WorkflowInstance(
            workflow_id="wf-1",
            workflow_name="Test",
            version="1.0.0",
            graph=sample_graph,
            instance_id="custom-id-123",
        )
        assert inst.instance_id == "custom-id-123"


class TestWorkflowRuntime:
    def test_create_and_compile_workflow(self):
        runtime = WorkflowRuntime()
        raw = {
            "metadata": {"name": "test-wf", "version": "1.0.0"},
            "version": "1.0.0",
            "nodes": [
                {"id": "start", "type": "noop", "label": "Start", "ports_out": ["out1"], "ports_in": []},
                {"id": "end", "type": "noop", "label": "End", "ports_in": ["in1"], "ports_out": []},
            ],
            "edges": [
                {"source": "start", "target": "end", "source_port": "out1", "target_port": "in1"},
            ],
            "entry_nodes": ["start"],
            "exit_nodes": ["end"],
        }
        manifest = runtime.create_manifest(raw)
        graph = runtime.compile(manifest)
        assert graph is not None
        assert graph.workflow_id == "test-wf"
        assert len(graph.nodes) == 2

    def test_create_instance(self):
        runtime = WorkflowRuntime()
        raw = {
            "metadata": {"name": "test-wf"},
            "nodes": [
                {"id": "start", "type": "noop", "ports_out": ["out1"], "ports_in": []},
                {"id": "end", "type": "noop", "ports_in": ["in1"], "ports_out": []},
            ],
            "edges": [{"source": "start", "target": "end", "source_port": "out1", "target_port": "in1"}],
            "entry_nodes": ["start"],
            "exit_nodes": ["end"],
        }
        manifest = runtime.create_manifest(raw)
        graph = runtime.compile(manifest)
        inst = runtime.create_instance(graph, inputs={"data": "test"})
        assert inst is not None
        assert inst.state == WorkflowLifecycleState.CREATED

    def test_full_lifecycle(self):
        runtime = WorkflowRuntime()
        raw = {
            "metadata": {"name": "test-wf"},
            "nodes": [
                {"id": "start", "type": "noop", "ports_out": ["out1"], "ports_in": []},
                {"id": "end", "type": "noop", "ports_in": ["in1"], "ports_out": []},
            ],
            "edges": [{"source": "start", "target": "end", "source_port": "out1", "target_port": "in1"}],
            "entry_nodes": ["start"],
            "exit_nodes": ["end"],
        }
        manifest = runtime.create_manifest(raw)
        graph = runtime.compile(manifest)
        inst = runtime.create_instance(graph, inputs={})

        # Schedule
        sched = runtime.schedule_instance(inst, TriggerType.IMMEDIATE)
        assert inst.state == WorkflowLifecycleState.SCHEDULED

        # Register event
        events_received = []
        runtime.event_bus.subscribe_all(lambda e: events_received.append(e))

        # Execute
        result = runtime.execute(inst)
        assert result is not None

        # Check lifecycle states were visited
        assert inst.state in (WorkflowLifecycleState.COMPLETED, WorkflowLifecycleState.FAILED)

    def test_pause_and_resume(self):
        runtime = WorkflowRuntime()
        raw = {
            "metadata": {"name": "test-wf"},
            "nodes": [{"id": "start", "type": "noop", "ports_out": [], "ports_in": []}],
            "edges": [],
            "entry_nodes": ["start"],
            "exit_nodes": ["start"],
        }
        manifest = runtime.create_manifest(raw)
        graph = runtime.compile(manifest)
        inst = runtime.create_instance(graph)
        inst.set_state(WorkflowLifecycleState.RUNNING)

        paused = runtime.pause(inst.instance_id)
        assert paused is True
        assert inst.state == WorkflowLifecycleState.PAUSED

        resumed = runtime.resume(inst.instance_id)
        assert resumed is True
        assert inst.state == WorkflowLifecycleState.RUNNING

    def test_cancel(self):
        runtime = WorkflowRuntime()
        raw = {
            "metadata": {"name": "test-wf"},
            "nodes": [{"id": "start", "type": "noop", "ports_out": [], "ports_in": []}],
            "edges": [],
            "entry_nodes": ["start"],
            "exit_nodes": ["start"],
        }
        manifest = runtime.create_manifest(raw)
        graph = runtime.compile(manifest)
        inst = runtime.create_instance(graph)
        inst.set_state(WorkflowLifecycleState.RUNNING)

        cancelled = runtime.cancel(inst.instance_id)
        assert cancelled is True
        assert inst.state == WorkflowLifecycleState.CANCELLED

    def test_dispose(self):
        runtime = WorkflowRuntime()
        raw = {
            "metadata": {"name": "test-wf"},
            "nodes": [{"id": "start", "type": "noop", "ports_out": [], "ports_in": []}],
            "edges": [],
            "entry_nodes": ["start"],
            "exit_nodes": ["start"],
        }
        manifest = runtime.create_manifest(raw)
        graph = runtime.compile(manifest)
        inst = runtime.create_instance(graph)
        inst_id = inst.instance_id

        disposed = runtime.dispose(inst_id)
        assert disposed is True
        assert inst.state == WorkflowLifecycleState.DISPOSED
        assert runtime.get_instance(inst_id) is None

    def test_recover(self):
        runtime = WorkflowRuntime()
        raw = {
            "metadata": {"name": "test-wf"},
            "nodes": [{"id": "start", "type": "noop", "ports_out": [], "ports_in": []}],
            "edges": [],
            "entry_nodes": ["start"],
            "exit_nodes": ["start"],
        }
        manifest = runtime.create_manifest(raw)
        graph = runtime.compile(manifest)
        inst = runtime.create_instance(graph)
        # Save a snapshot for recovery
        runtime.storage.save_snapshot(inst.instance_id, {"state": "paused"})
        recovered = runtime.recover(inst.instance_id)
        assert recovered is True

    def test_event_bus_receives_lifecycle_events(self):
        runtime = WorkflowRuntime()
        events = []
        runtime.event_bus.subscribe_all(lambda e: events.append(e))

        raw = {
            "metadata": {"name": "test-wf"},
            "nodes": [{"id": "start", "type": "noop", "ports_out": [], "ports_in": []}],
            "edges": [],
            "entry_nodes": ["start"],
            "exit_nodes": ["start"],
        }
        manifest = runtime.create_manifest(raw)
        graph = runtime.compile(manifest)
        inst = runtime.create_instance(graph)

        assert len(events) > 0
        event_types = [e.event_type for e in events]
        assert EventType.WORKFLOW_REGISTERED in event_types

    def test_health_service(self):
        runtime = WorkflowRuntime()
        assert runtime.health.state == "Healthy"
        runtime.health.set_state("Busy")
        assert runtime.health.state == "Busy"

    def test_metrics_collector(self):
        runtime = WorkflowRuntime()
        assert runtime.metrics.execution_count == 0
        raw = {
            "metadata": {"name": "test-wf"},
            "nodes": [{"id": "start", "type": "noop", "ports_out": [], "ports_in": []}],
            "edges": [],
            "entry_nodes": ["start"],
            "exit_nodes": ["start"],
        }
        manifest = runtime.create_manifest(raw)
        graph = runtime.compile(manifest)
        inst = runtime.create_instance(graph)
        result = runtime.execute(inst)
        assert runtime.metrics.execution_count >= 1

    def test_node_registry_accessible(self):
        runtime = WorkflowRuntime()
        reg = runtime.node_registry
        assert reg is not None

    def test_scheduler_accessible(self):
        runtime = WorkflowRuntime()
        sched = runtime.scheduler
        assert sched is not None

    def test_storage_accessible(self):
        runtime = WorkflowRuntime()
        storage = runtime.storage
        assert storage is not None

    def test_plugin_bridge_accessible(self):
        runtime = WorkflowRuntime()
        bridge = runtime.plugin_bridge
        assert bridge is not None

    def test_get_instances(self):
        runtime = WorkflowRuntime()
        raw = {
            "metadata": {"name": "test-wf"},
            "nodes": [{"id": "start", "type": "noop", "ports_out": [], "ports_in": []}],
            "edges": [],
            "entry_nodes": ["start"],
            "exit_nodes": ["start"],
        }
        manifest = runtime.create_manifest(raw)
        graph = runtime.compile(manifest)
        inst = runtime.create_instance(graph)
        instances = runtime.get_instances()
        assert inst.instance_id in instances

    def test_get_instance_by_id(self):
        runtime = WorkflowRuntime()
        raw = {
            "metadata": {"name": "test-wf"},
            "nodes": [{"id": "start", "type": "noop", "ports_out": [], "ports_in": []}],
            "edges": [],
            "entry_nodes": ["start"],
            "exit_nodes": ["start"],
        }
        manifest = runtime.create_manifest(raw)
        graph = runtime.compile(manifest)
        inst = runtime.create_instance(graph)
        fetched = runtime.get_instance(inst.instance_id)
        assert fetched is not None
        assert fetched.instance_id == inst.instance_id

    def test_create_manifest_from_raw(self):
        runtime = WorkflowRuntime()
        raw = {"metadata": {"name": "raw-wf"}}
        manifest = runtime.create_manifest(raw)
        assert manifest.metadata.name == "raw-wf"

    def test_validate_manifest(self):
        runtime = WorkflowRuntime()
        raw = {
            "metadata": {"name": "test-wf"},
            "nodes": [{"id": "start", "type": "noop", "ports_out": [], "ports_in": []}],
            "edges": [],
            "entry_nodes": ["start"],
            "exit_nodes": ["start"],
        }
        manifest = runtime.create_manifest(raw)
        violations = runtime.validate_manifest(manifest)
        assert violations == []
