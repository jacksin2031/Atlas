"""Tests for workflow graph."""

from __future__ import annotations
import pytest

from atlas_workflow.common import GraphError
from atlas_workflow.graph import WorkflowGraph, GraphNode, GraphEdge


class TestWorkflowGraphBasics:
    def test_create_simple_graph(self):
        nodes = [
            GraphNode(node_id="start", node_type="noop", ports_out=["out1"]),
            GraphNode(node_id="end", node_type="noop", ports_in=["in1"]),
        ]
        edges = [GraphEdge(source_node_id="start", target_node_id="end")]
        graph = WorkflowGraph(nodes, edges, ["start"], ["end"])
        assert len(graph.nodes) == 2
        assert len(graph.edges) == 1
        assert graph.entry_nodes == ("start",)
        assert graph.exit_nodes == ("end",)

    def test_get_node(self):
        nodes = [GraphNode(node_id="n1", node_type="noop")]
        graph = WorkflowGraph(nodes, [], [], [])
        node = graph.get_node("n1")
        assert node is not None
        assert node.node_id == "n1"
        assert graph.get_node("missing") is None

    def test_has_node(self):
        nodes = [GraphNode(node_id="n1", node_type="noop")]
        graph = WorkflowGraph(nodes, [], [], [])
        assert graph.has_node("n1")
        assert not graph.has_node("missing")

    def test_has_edge(self):
        nodes = [
            GraphNode(node_id="a", node_type="noop"),
            GraphNode(node_id="b", node_type="noop"),
        ]
        edges = [GraphEdge(source_node_id="a", target_node_id="b")]
        graph = WorkflowGraph(nodes, edges, ["a"], ["b"])
        assert graph.has_edge("a", "b")
        assert not graph.has_edge("b", "a")
        assert not graph.has_edge("a", "a")


class TestGraphTraversal:
    def test_successors(self):
        nodes = [
            GraphNode(node_id="a", node_type="noop"),
            GraphNode(node_id="b", node_type="noop"),
            GraphNode(node_id="c", node_type="noop"),
        ]
        edges = [
            GraphEdge(source_node_id="a", target_node_id="b"),
            GraphEdge(source_node_id="a", target_node_id="c"),
        ]
        graph = WorkflowGraph(nodes, edges, ["a"], ["b", "c"])
        assert sorted(graph.get_successors("a")) == ["b", "c"]
        assert graph.get_successors("b") == []

    def test_predecessors(self):
        nodes = [
            GraphNode(node_id="a", node_type="noop"),
            GraphNode(node_id="b", node_type="noop"),
            GraphNode(node_id="c", node_type="noop"),
        ]
        edges = [
            GraphEdge(source_node_id="a", target_node_id="b"),
            GraphEdge(source_node_id="b", target_node_id="c"),
        ]
        graph = WorkflowGraph(nodes, edges, ["a"], ["c"])
        assert graph.get_predecessors("c") == ["b"]
        assert graph.get_predecessors("a") == []


class TestTopologicalOrder:
    def test_linear_topological_order(self):
        nodes = [
            GraphNode(node_id="a", node_type="noop"),
            GraphNode(node_id="b", node_type="noop"),
            GraphNode(node_id="c", node_type="noop"),
        ]
        edges = [
            GraphEdge(source_node_id="a", target_node_id="b"),
            GraphEdge(source_node_id="b", target_node_id="c"),
        ]
        graph = WorkflowGraph(nodes, edges, ["a"], ["c"])
        order = graph.topological_order()
        assert order == ["a", "b", "c"]

    def test_diamond_topological_order(self):
        nodes = [
            GraphNode(node_id="start", node_type="noop"),
            GraphNode(node_id="left", node_type="noop"),
            GraphNode(node_id="right", node_type="noop"),
            GraphNode(node_id="end", node_type="noop"),
        ]
        edges = [
            GraphEdge(source_node_id="start", target_node_id="left"),
            GraphEdge(source_node_id="start", target_node_id="right"),
            GraphEdge(source_node_id="left", target_node_id="end"),
            GraphEdge(source_node_id="right", target_node_id="end"),
        ]
        graph = WorkflowGraph(nodes, edges, ["start"], ["end"])
        order = graph.topological_order()
        assert order[0] == "start"
        assert order[-1] == "end"
        assert len(order) == 4

    def test_cycle_raises_graph_error(self, cyclic_graph):
        with pytest.raises(GraphError, match="Cycle detected"):
            cyclic_graph.topological_order()

    def test_topological_order_is_deterministic(self):
        nodes = [
            GraphNode(node_id="z", node_type="noop"),
            GraphNode(node_id="a", node_type="noop"),
            GraphNode(node_id="m", node_type="noop"),
        ]
        edges = [
            GraphEdge(source_node_id="z", target_node_id="m"),
            GraphEdge(source_node_id="a", target_node_id="m"),
        ]
        graph = WorkflowGraph(nodes, edges, ["z", "a"], ["m"])
        order1 = graph.topological_order()
        order2 = graph.topological_order()
        assert order1 == order2


class TestCycleDetection:
    def test_dag_has_no_cycles(self, sample_graph):
        cycles = sample_graph.detect_cycles()
        assert cycles == []

    def test_cyclic_graph_detects_cycles(self, cyclic_graph):
        cycles = cyclic_graph.detect_cycles()
        assert len(cycles) > 0

    def test_is_dag_true(self, sample_graph):
        assert sample_graph.is_dag() is True

    def test_is_dag_false(self, cyclic_graph):
        assert cyclic_graph.is_dag() is False


class TestParallelGroups:
    def test_linear_has_one_node_per_group(self):
        nodes = [
            GraphNode(node_id="a", node_type="noop"),
            GraphNode(node_id="b", node_type="noop"),
            GraphNode(node_id="c", node_type="noop"),
        ]
        edges = [
            GraphEdge(source_node_id="a", target_node_id="b"),
            GraphEdge(source_node_id="b", target_node_id="c"),
        ]
        graph = WorkflowGraph(nodes, edges, ["a"], ["c"])
        groups = graph.get_parallel_groups()
        assert len(groups) == 3
        assert groups[0] == ["a"]
        assert groups[1] == ["b"]
        assert groups[2] == ["c"]

    def test_diamond_has_two_parallel_nodes(self):
        nodes = [
            GraphNode(node_id="start", node_type="noop"),
            GraphNode(node_id="left", node_type="noop"),
            GraphNode(node_id="right", node_type="noop"),
            GraphNode(node_id="end", node_type="noop"),
        ]
        edges = [
            GraphEdge(source_node_id="start", target_node_id="left"),
            GraphEdge(source_node_id="start", target_node_id="right"),
            GraphEdge(source_node_id="left", target_node_id="end"),
            GraphEdge(source_node_id="right", target_node_id="end"),
        ]
        graph = WorkflowGraph(nodes, edges, ["start"], ["end"])
        groups = graph.get_parallel_groups()
        assert len(groups) == 3
        assert set(groups[1]) == {"left", "right"}

    def test_parallel_graph_groups(self, parallel_graph):
        groups = parallel_graph.get_parallel_groups()
        assert len(groups) == 4
        assert groups[0] == ["start"]
        assert set(groups[1]) == {"branch_a", "branch_b", "branch_c"}
        assert groups[2] == ["merge"]
        assert groups[3] == ["end"]


class TestGraphIntegrity:
    def test_valid_graph_has_no_violations(self, sample_graph):
        violations = sample_graph.validate_integrity()
        assert violations == []

    def test_missing_edge_source(self):
        nodes = [GraphNode(node_id="b", node_type="noop")]
        edges = [GraphEdge(source_node_id="missing", target_node_id="b")]
        graph = WorkflowGraph(nodes, edges, ["missing"], ["b"])
        violations = graph.validate_integrity()
        assert any("unknown source" in v for v in violations)

    def test_missing_edge_target(self):
        nodes = [GraphNode(node_id="a", node_type="noop")]
        edges = [GraphEdge(source_node_id="a", target_node_id="missing")]
        graph = WorkflowGraph(nodes, edges, ["a"], ["a"])
        violations = graph.validate_integrity()
        assert any("unknown target" in v for v in violations)

    def test_missing_entry_node(self):
        nodes = [GraphNode(node_id="a", node_type="noop")]
        edges = []
        graph = WorkflowGraph(nodes, edges, ["missing_entry"], ["a"])
        violations = graph.validate_integrity()
        assert any("Entry node" in v for v in violations)

    def test_missing_exit_node(self):
        nodes = [GraphNode(node_id="a", node_type="noop")]
        edges = []
        graph = WorkflowGraph(nodes, edges, ["a"], ["missing_exit"])
        violations = graph.validate_integrity()
        assert any("Exit node" in v for v in violations)

    def test_cycle_is_violation(self, cyclic_graph):
        violations = cyclic_graph.validate_integrity()
        assert any("Cycle" in v for v in violations)


class TestSubgraph:
    def test_extract_subgraph(self):
        nodes = [
            GraphNode(node_id="a", node_type="noop"),
            GraphNode(node_id="b", node_type="noop"),
            GraphNode(node_id="c", node_type="noop"),
        ]
        edges = [
            GraphEdge(source_node_id="a", target_node_id="b"),
            GraphEdge(source_node_id="b", target_node_id="c"),
        ]
        graph = WorkflowGraph(nodes, edges, ["a"], ["c"])
        sub = graph.get_subgraph(["a", "b"])
        assert len(sub.nodes) == 2
        assert len(sub.edges) == 1
        assert sub.has_node("a")
        assert sub.has_node("b")
        assert not sub.has_node("c")


class TestGraphNode:
    def test_from_parsed(self):
        from atlas_workflow.parser import ParsedNode, RetryPolicy
        parsed = ParsedNode(
            node_id="n1", node_type="noop",
            retry_policy=RetryPolicy(max_retries=3),
            timeout_seconds=60.0,
            ports_in=["in1"], ports_out=["out1"],
        )
        node = GraphNode.from_parsed(parsed)
        assert node.node_id == "n1"
        assert node.retry_max == 3
        assert node.timeout_seconds == 60.0
        assert node.inputs == ()
        assert node.outputs == ()
        assert node.ports_in == ("in1",)
        assert node.ports_out == ("out1",)
