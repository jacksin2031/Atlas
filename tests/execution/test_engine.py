"""Tests for execution engine."""

from __future__ import annotations
import pytest

from atlas_workflow.common import (
    ExecutionState,
    ExecutionMetadata,
    WorkflowEvent,
    EventType,
)
from atlas_workflow.execution import ExecutionEngine, ExecutionToken, ExecutionResult
from atlas_workflow.graph import WorkflowGraph, GraphNode, GraphEdge
from atlas_workflow.plugin_integration import PluginBridge


def _make_graph_with_nodes(types_list, edges_list):
    """Helper to create a simple graph from node types and edges."""
    nodes = []
    for i, ntype in enumerate(types_list):
        pid = f"in{i}" if i > 0 else ""
        pod = f"out{i}" if i < len(types_list) - 1 else ""
        nodes.append(GraphNode(node_id=f"n{i}", node_type=ntype, ports_in=[pid] if pid else [], ports_out=[pod] if pod else []))
    edge_objs = []
    for src, tgt in edges_list:
        edge_objs.append(GraphEdge(source_node_id=f"n{src}", target_node_id=f"n{tgt}"))
    entry = [f"n{edges_list[0][0]}"] if edges_list else [f"n0"]
    exit_n = [f"n{edges_list[-1][1]}"] if edges_list else [f"n{len(types_list)-1}"]
    return WorkflowGraph(
        nodes=nodes, edges=edge_objs,
        entry_nodes=entry,
        exit_nodes=exit_n,
        workflow_id="test-wf",
        workflow_name="Test Workflow",
    )


class TestExecutionEngine:
    def test_sequential_execution(self, plugin_bridge):
        engine = ExecutionEngine(
            plugin_bridge=plugin_bridge,
            event_publisher=lambda e: None,
            checkpoint_callback=lambda c: None,
        )
        graph = _make_graph_with_nodes(["noop", "transform", "noop"], [(0, 1), (1, 2)])
        token = ExecutionToken(token_id="t1", workflow_instance_id="i1")
        result = engine.execute(graph, token, {"data": "hello"})
        assert result.success is True
        assert result.workflow_id == "test-wf"
        assert result.instance_id == "i1"

    def test_execution_records_node_states(self, plugin_bridge):
        engine = ExecutionEngine(
            plugin_bridge=plugin_bridge,
            event_publisher=lambda e: None,
            checkpoint_callback=lambda c: None,
        )
        graph = _make_graph_with_nodes(["noop", "noop"], [(0, 1)])
        token = ExecutionToken(token_id="t2", workflow_instance_id="i2")
        engine.execute(graph, token, {})
        states = engine.node_states
        assert len(states) == 2
        for nid, ns in states.items():
            assert ns.state == ExecutionState.COMPLETED

    def test_execution_failure_propagation(self):
        def failing_handler(node_id, configuration, inputs, metadata):
            raise RuntimeError("intentional failure")

        bridge = PluginBridge(node_handlers={"fail": failing_handler})
        bridge._registered_types = {"fail"}

        engine = ExecutionEngine(
            plugin_bridge=bridge,
            event_publisher=lambda e: None,
            checkpoint_callback=lambda c: None,
            default_max_retries=0,
        )
        graph = _make_graph_with_nodes(["fail"], [])
        token = ExecutionToken(token_id="t3", workflow_instance_id="i3")
        result = engine.execute(graph, token, {})
        assert result.success is False
        assert result.error is not None
        assert "failed" in result.error.lower()

    def test_parallel_execution(self, plugin_bridge, parallel_graph):
        engine = ExecutionEngine(
            plugin_bridge=plugin_bridge,
            event_publisher=lambda e: None,
            checkpoint_callback=lambda c: None,
        )
        token = ExecutionToken(token_id="t4", workflow_instance_id="i4")
        result = engine.execute(parallel_graph, token, {})
        assert result.success is True

    def test_execution_history(self, plugin_bridge):
        engine = ExecutionEngine(
            plugin_bridge=plugin_bridge,
            event_publisher=lambda e: None,
            checkpoint_callback=lambda c: None,
        )
        graph = _make_graph_with_nodes(["noop", "noop"], [(0, 1)])
        token = ExecutionToken(token_id="t5", workflow_instance_id="i5")
        engine.execute(graph, token, {})
        hist = engine.history
        assert hist is not None
        assert hist.event_count > 0
        assert hist.checkpoint_count > 0

    def test_execution_with_metadata(self, plugin_bridge):
        engine = ExecutionEngine(
            plugin_bridge=plugin_bridge,
            event_publisher=lambda e: None,
            checkpoint_callback=lambda c: None,
        )
        graph = _make_graph_with_nodes(["noop"], [])
        token = ExecutionToken(token_id="t6", workflow_instance_id="i6")
        meta = ExecutionMetadata(workflow_id="wf-1", instance_id="i6")
        result = engine.execute(graph, token, {}, metadata=meta)
        assert result.success is True

    def test_execution_result_success_result(self):
        r = ExecutionResult.success_result(
            workflow_id="wf-1",
            instance_id="i1",
            output={"key": "val"},
            duration_ms=42.0,
        )
        assert r.success is True
        assert r.output["key"] == "val"
        assert r.duration_ms == 42.0

    def test_execution_result_failure_result(self):
        r = ExecutionResult.failure_result(
            workflow_id="wf-1",
            instance_id="i1",
            error="something broke",
            node_id="n1",
        )
        assert r.success is False
        assert r.error == "something broke"
        assert r.node_id == "n1"
