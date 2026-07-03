"""Shared test fixtures for Atlas Workflow tests."""

from __future__ import annotations
import pytest

from atlas_workflow.common import (
    ManifestMetadata,
    ManifestParameter,
    ManifestVariable,
    ManifestInput,
    ManifestOutput,
    ManifestDependency,
    CapabilityRequirement,
    Permission,
)
from atlas_workflow.manifest import WorkflowManifest
from atlas_workflow.node_registry import NodeRegistry, NodeDefinition
from atlas_workflow.parser import ParsedWorkflow, ParsedNode, ParsedEdge, RetryPolicy
from atlas_workflow.events import EventBus
from atlas_workflow.graph import WorkflowGraph, GraphNode, GraphEdge
from atlas_workflow.plugin_integration import PluginBridge


@pytest.fixture
def event_bus():
    return EventBus()


@pytest.fixture
def node_registry():
    reg = NodeRegistry()
    reg.register(NodeDefinition(
        node_id="noop-1",
        node_type="noop",
        label="NoOp Node",
        description="A no-operation node",
        capabilities=["basic"],
    ))
    reg.register(NodeDefinition(
        node_id="transform-1",
        node_type="transform",
        label="Transform Node",
        description="A transformation node",
        capabilities=["basic", "transform"],
    ))
    reg.register(NodeDefinition(
        node_id="conditional-1",
        node_type="conditional",
        label="Conditional Node",
        description="A conditional branching node",
        capabilities=["basic", "branching"],
    ))
    return reg


@pytest.fixture
def plugin_bridge():
    def noop_handler(node_id, configuration, inputs, metadata):
        return {"node_id": node_id, "output": "noop_result"}

    def transform_handler(node_id, configuration, inputs, metadata):
        result = {}
        for k, v in inputs.items():
            result[f"transformed_{k}"] = str(v).upper() if isinstance(v, str) else v
        return result

    bridge = PluginBridge(node_handlers={
        "noop": noop_handler,
        "transform": transform_handler,
    })
    bridge._registered_types = {"noop", "transform"}
    return bridge


@pytest.fixture
def sample_manifest():
    return WorkflowManifest(
        metadata=ManifestMetadata(name="test-workflow", version="1.0.0"),
        version="1.0.0",
        dependencies=[ManifestDependency(name="dep1", version=">=1.0.0")],
        capabilities=[CapabilityRequirement(name="basic", minimum_version="1.0.0")],
        plugins=["plugin-a"],
        permissions=[Permission(name="execute", actions=["run"])],
        parameters=[ManifestParameter(name="input_param", type="string", required=True)],
        variables=[ManifestVariable(name="counter", type="int", scope="global", default=0)],
        inputs=[ManifestInput(name="data", type="object", required=True)],
        outputs=[ManifestOutput(name="result", type="object")],
        node_definitions=[
            {"id": "start", "type": "noop", "label": "Start", "ports_out": ["out1"], "ports_in": []},
            {"id": "process", "type": "transform", "label": "Process", "ports_in": ["in1"], "ports_out": ["out1"]},
            {"id": "end", "type": "noop", "label": "End", "ports_in": ["in1"], "ports_out": []},
        ],
        edge_definitions=[
            {"source": "start", "target": "process", "source_port": "out1", "target_port": "in1"},
            {"source": "process", "target": "end", "source_port": "out1", "target_port": "in1"},
        ],
        entry_nodes=["start"],
        exit_nodes=["end"],
    )


@pytest.fixture
def sample_parsed_workflow(sample_manifest):
    from atlas_workflow.parser import WorkflowParser
    parser = WorkflowParser()
    return parser.parse(sample_manifest)


@pytest.fixture
def sample_graph(sample_parsed_workflow):
    from atlas_workflow.graph.models import GraphNode, GraphEdge
    nodes = [GraphNode.from_parsed(n) for n in sample_parsed_workflow.nodes]
    edges = [GraphEdge.from_parsed(e) for e in sample_parsed_workflow.edges]
    return WorkflowGraph(
        nodes=nodes,
        edges=edges,
        entry_nodes=list(sample_parsed_workflow.entry_nodes),
        exit_nodes=list(sample_parsed_workflow.exit_nodes),
        workflow_id=sample_parsed_workflow.workflow_id,
        workflow_name=sample_parsed_workflow.workflow_name,
        version=sample_parsed_workflow.version,
    )


@pytest.fixture
def parallel_graph():
    """Create a graph with parallel execution paths."""
    nodes = [
        GraphNode(node_id="start", node_type="noop", ports_out=["out1"]),
        GraphNode(node_id="branch_a", node_type="noop", ports_in=["in1"], ports_out=["out1"]),
        GraphNode(node_id="branch_b", node_type="noop", ports_in=["in1"], ports_out=["out1"]),
        GraphNode(node_id="branch_c", node_type="noop", ports_in=["in1"], ports_out=["out1"]),
        GraphNode(node_id="merge", node_type="noop", ports_in=["in1", "in2", "in3"]),
        GraphNode(node_id="end", node_type="noop", ports_in=["out1"]),
    ]
    edges = [
        GraphEdge(source_node_id="start", target_node_id="branch_a"),
        GraphEdge(source_node_id="start", target_node_id="branch_b"),
        GraphEdge(source_node_id="start", target_node_id="branch_c"),
        GraphEdge(source_node_id="branch_a", target_node_id="merge"),
        GraphEdge(source_node_id="branch_b", target_node_id="merge"),
        GraphEdge(source_node_id="branch_c", target_node_id="merge"),
        GraphEdge(source_node_id="merge", target_node_id="end"),
    ]
    return WorkflowGraph(
        nodes=nodes,
        edges=edges,
        entry_nodes=["start"],
        exit_nodes=["end"],
        workflow_id="parallel-test",
        workflow_name="Parallel Test Workflow",
    )


@pytest.fixture
def cyclic_graph():
    """Create a graph with a cycle for testing cycle detection."""
    nodes = [
        GraphNode(node_id="a", node_type="noop", ports_out=["out"]),
        GraphNode(node_id="b", node_type="noop", ports_in=["in"], ports_out=["out"]),
        GraphNode(node_id="c", node_type="noop", ports_in=["in"]),
    ]
    edges = [
        GraphEdge(source_node_id="a", target_node_id="b"),
        GraphEdge(source_node_id="b", target_node_id="c"),
        GraphEdge(source_node_id="c", target_node_id="a"),
    ]
    return WorkflowGraph(
        nodes=nodes,
        edges=edges,
        entry_nodes=["a"],
        exit_nodes=["c"],
        workflow_id="cyclic-test",
        workflow_name="Cyclic Test Workflow",
    )
