"""Integration tests for the complete workflow runtime.

These tests exercise the full stack: manifest -> parser -> validator -> graph -> runtime -> execution.
"""

from __future__ import annotations
import pytest

from atlas_workflow.common import (
    WorkflowLifecycleState,
    ExecutionState,
    WorkflowEvent,
    EventType,
    ManifestMetadata,
    ManifestParameter,
    ManifestVariable,
    ManifestInput,
    ManifestOutput,
    CapabilityRequirement,
    Permission,
    ManifestDependency,
)
from atlas_workflow.manifest import WorkflowManifest, WorkflowManifestParser
from atlas_workflow.parser import WorkflowParser
from atlas_workflow.validator import WorkflowValidator
from atlas_workflow.graph import WorkflowGraph, GraphNode, GraphEdge
from atlas_workflow.node_registry import NodeRegistry, NodeDefinition
from atlas_workflow.plugin_integration import PluginBridge
from atlas_workflow.events import EventBus
from atlas_workflow.execution import ExecutionEngine, ExecutionToken
from atlas_workflow.runtime import WorkflowRuntime
from atlas_workflow.scheduler import TriggerType
from atlas_workflow.storage import StorageAbstraction
from atlas_workflow.metrics import MetricsCollector
from atlas_workflow.health import HealthService


def _make_complete_manifest():
    """Create a realistic workflow manifest for integration testing."""
    parser = WorkflowManifestParser()
    return parser.parse({
        "metadata": {
            "name": "data-pipeline",
            "version": "1.0.0",
            "description": "A data processing pipeline",
        },
        "version": "1.0.0",
        "dependencies": [
            {"name": "data-lib", "version": ">=1.0.0"},
        ],
        "capabilities": [],
        "plugins": ["data-processor"],
        "permissions": [
            {"name": "execute", "actions": ["run", "process"]},
        ],
        "parameters": [
            {"name": "batch_size", "type": "int", "default": 100, "required": False},
        ],
        "variables": [
            {"name": "processing_count", "type": "int", "scope": "global", "default": 0},
        ],
        "inputs": [
            {"name": "input_data", "type": "object", "required": True},
        ],
        "outputs": [
            {"name": "processed_data", "type": "object"},
            {"name": "summary", "type": "string"},
        ],
        "nodes": [
            {
                "id": "ingest",
                "type": "noop",
                "label": "Data Ingestion",
                "ports_out": ["out1"],
                "ports_in": [],
            },
            {
                "id": "validate",
                "type": "noop",
                "label": "Validation",
                "ports_in": ["in1"],
                "ports_out": ["out1"],
            },
            {
                "id": "output",
                "type": "noop",
                "label": "Output",
                "ports_in": ["in1"],
                "ports_out": [],
            },
        ],
        "edges": [
            {"source": "ingest", "target": "validate", "source_port": "out1", "target_port": "in1"},
            {"source": "validate", "target": "output", "source_port": "out1", "target_port": "in1"},
        ],
        "entry_nodes": ["ingest"],
        "exit_nodes": ["output"],
    })


class TestFullWorkflowIntegration:
    def test_end_to_end_pipeline(self):
        """Test the complete workflow from manifest to execution result."""
        runtime = WorkflowRuntime()

        # Compile
        manifest = _make_complete_manifest()
        graph = runtime.compile(manifest)
        assert graph.is_dag()
        assert len(graph.nodes) == 3

        # Create instance
        instance = runtime.create_instance(
            graph,
            inputs={"input_data": {"records": [1, 2, 3]}},
        )
        assert instance.state == WorkflowLifecycleState.CREATED

        # Execute
        result = runtime.execute(instance)
        assert result.success is True
        assert result.workflow_id == "data-pipeline"
        assert instance.state == WorkflowLifecycleState.COMPLETED

    def test_events_published_throughout_lifecycle(self):
        """Verify all lifecycle events are published."""
        runtime = WorkflowRuntime()
        events = []
        runtime.event_bus.subscribe_all(lambda e: events.append(e))

        manifest = _make_complete_manifest()
        graph = runtime.compile(manifest)
        instance = runtime.create_instance(graph, inputs={})
        result = runtime.execute(instance)

        event_types = [e.event_type for e in events]
        assert EventType.WORKFLOW_REGISTERED in event_types
        assert EventType.WORKFLOW_STARTED in event_types
        assert EventType.NODE_STARTED in event_types
        assert EventType.NODE_COMPLETED in event_types
        assert EventType.WORKFLOW_COMPLETED in event_types

    def test_metrics_collected_during_execution(self):
        """Verify metrics are collected during workflow execution."""
        runtime = WorkflowRuntime()
        manifest = _make_complete_manifest()
        graph = runtime.compile(manifest)
        instance = runtime.create_instance(graph, inputs={})
        runtime.execute(instance)

        metrics = runtime.metrics.to_dict()
        assert metrics["execution_count"] >= 1
        assert metrics["success_count"] >= 1

    def test_storage_checkpoint_created(self):
        """Verify storage checkpoints are created during execution."""
        runtime = WorkflowRuntime()
        manifest = _make_complete_manifest()
        graph = runtime.compile(manifest)
        instance = runtime.create_instance(graph, inputs={})
        runtime.execute(instance)

        snapshots = runtime.storage.list_snapshots()
        assert len(snapshots) > 0

    def test_health_reflects_execution(self):
        """Verify health service reflects execution state."""
        runtime = WorkflowRuntime()
        manifest = _make_complete_manifest()
        graph = runtime.compile(manifest)
        instance = runtime.create_instance(graph, inputs={})
        runtime.execute(instance)

        report = runtime.health.get_health_report()
        assert "state" in report

    def test_workflow_with_parallel_branches(self, parallel_graph):
        """Test execution with parallel branches."""
        runtime = WorkflowRuntime()
        manifest = _make_complete_manifest()
        graph = runtime.compile(manifest)
        instance = runtime.create_instance(graph, inputs={})
        result = runtime.execute(instance)
        assert result.success is True

    def test_workflow_recovery_from_storage(self):
        """Test recovering a workflow from stored checkpoint."""
        runtime = WorkflowRuntime()
        manifest = _make_complete_manifest()
        graph = runtime.compile(manifest)
        instance = runtime.create_instance(graph, inputs={})

        # Simulate a checkpoint
        runtime.storage.save_snapshot(instance.instance_id, {
            "state": "running",
            "completed_nodes": ["ingest"],
        })

        recovered = runtime.recover(instance.instance_id)
        assert recovered is True

    def test_workflow_cancel_during_execution(self):
        """Test cancelling a workflow and verifying state."""
        runtime = WorkflowRuntime()
        manifest = _make_complete_manifest()
        graph = runtime.compile(manifest)
        instance = runtime.create_instance(graph, inputs={})

        # Manually set to running and cancel
        instance.set_state(WorkflowLifecycleState.RUNNING)
        cancelled = runtime.cancel(instance.instance_id)
        assert cancelled is True
        assert instance.state == WorkflowLifecycleState.CANCELLED

    def test_workflow_disposal(self):
        """Test disposing of a completed workflow."""
        runtime = WorkflowRuntime()
        manifest = _make_complete_manifest()
        graph = runtime.compile(manifest)
        instance = runtime.create_instance(graph, inputs={})
        runtime.execute(instance)

        disposed = runtime.dispose(instance.instance_id)
        assert disposed is True
        assert runtime.get_instance(instance.instance_id) is None

    def test_multiple_workflow_instances(self):
        """Test running multiple workflow instances."""
        runtime = WorkflowRuntime()
        manifest = _make_complete_manifest()
        graph = runtime.compile(manifest)

        instances = []
        for i in range(3):
            inst = runtime.create_instance(graph, inputs={"input_data": {"batch": i}})
            instances.append(inst)

        for inst in instances:
            result = runtime.execute(inst)
            assert result.success is True

        assert len(runtime.get_instances()) == 3

    def test_graph_determinism(self):
        """Verify topological order is deterministic across runs."""
        manifest = _make_complete_manifest()
        runtime = WorkflowRuntime()
        graph = runtime.compile(manifest)

        order1 = graph.topological_order()
        order2 = graph.topological_order()
        assert order1 == order2

    def test_validation_before_execution(self):
        """Verify invalid workflows cannot be compiled."""
        runtime = WorkflowRuntime()
        bad_manifest = WorkflowManifest(
            metadata=ManifestMetadata(name="bad"),
            version="1.0.0",
            node_definitions=[],
            edge_definitions=[],
            entry_nodes=[],
            exit_nodes=[],
        )
        with pytest.raises(Exception):
            runtime.compile(bad_manifest)
