"""Immutable workflow graph with DAG validation.

Per RFC-0304 and RFC-0317. Graphs are deterministic and immutable.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from atlas_workflow.common import GraphError


@dataclass(frozen=True, slots=True, kw_only=True)
class GraphNode:
    """A node in the workflow graph."""
    node_id: str
    node_type: str
    label: str = ""
    configuration: dict[str, Any] = field(default_factory=dict)
    inputs: tuple[str, ...] = field(default_factory=tuple)
    outputs: tuple[str, ...] = field(default_factory=tuple)
    ports_in: tuple[str, ...] = field(default_factory=tuple)
    ports_out: tuple[str, ...] = field(default_factory=tuple)
    conditions: tuple[str, ...] = field(default_factory=tuple)
    retry_max: int = 0
    timeout_seconds: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_parsed(cls, parsed: Any) -> GraphNode:
        """Construct from a ParsedNode."""
        return cls(
            node_id=parsed.node_id,
            node_type=parsed.node_type,
            label=parsed.label,
            configuration=parsed.configuration,
            inputs=tuple(parsed.inputs),
            outputs=tuple(parsed.outputs),
            ports_in=tuple(parsed.ports_in),
            ports_out=tuple(parsed.ports_out),
            conditions=tuple(parsed.conditions),
            retry_max=parsed.retry_policy.max_retries if parsed.retry_policy else 0,
            timeout_seconds=parsed.timeout_seconds,
            metadata=parsed.metadata,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class GraphEdge:
    """An edge in the workflow graph."""
    source_node_id: str
    target_node_id: str
    source_port: str = ""
    target_port: str = ""
    condition: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_parsed(cls, parsed: Any) -> GraphEdge:
        """Construct from a ParsedEdge."""
        return cls(
            source_node_id=parsed.source_node_id,
            target_node_id=parsed.target_node_id,
            source_port=parsed.source_port,
            target_port=parsed.target_port,
            condition=parsed.condition,
            metadata=parsed.metadata,
        )


class WorkflowGraph:
    """Immutable directed acyclic workflow graph.

    Provides deterministic traversal, cycle detection, topological
    ordering, and sub-graph extraction. Per RFC-0304.
    """

    def __init__(
        self,
        nodes: list[GraphNode],
        edges: list[GraphEdge],
        entry_nodes: list[str],
        exit_nodes: list[str],
        workflow_id: str = "",
        workflow_name: str = "",
        version: str = "1.0.0",
    ) -> None:
        self._workflow_id = workflow_id
        self._workflow_name = workflow_name
        self._version = version
        self._nodes: dict[str, GraphNode] = {n.node_id: n for n in nodes}
        self._edges: list[GraphEdge] = list(edges)
        self._entry_nodes = tuple(entry_nodes)
        self._exit_nodes = tuple(exit_nodes)
        self._build_adjacency()

    def _build_adjacency(self) -> None:
        self._adjacency: dict[str, list[str]] = {n.node_id: [] for n in self._nodes.values()}
        self._reverse_adjacency: dict[str, list[str]] = {n.node_id: [] for n in self._nodes.values()}
        for edge in self._edges:
            if edge.source_node_id in self._adjacency:
                self._adjacency[edge.source_node_id].append(edge.target_node_id)
            if edge.target_node_id in self._reverse_adjacency:
                self._reverse_adjacency[edge.target_node_id].append(edge.source_node_id)

    @property
    def workflow_id(self) -> str:
        return self._workflow_id

    @property
    def workflow_name(self) -> str:
        return self._workflow_name

    @property
    def version(self) -> str:
        return self._version

    @property
    def nodes(self) -> dict[str, GraphNode]:
        return dict(self._nodes)

    @property
    def edges(self) -> list[GraphEdge]:
        return list(self._edges)

    @property
    def entry_nodes(self) -> tuple[str, ...]:
        return self._entry_nodes

    @property
    def exit_nodes(self) -> tuple[str, ...]:
        return self._exit_nodes

    @property
    def adjacency(self) -> dict[str, list[str]]:
        return {k: list(v) for k, v in self._adjacency.items()}

    def get_node(self, node_id: str) -> GraphNode | None:
        return self._nodes.get(node_id)

    def get_successors(self, node_id: str) -> list[str]:
        return list(self._adjacency.get(node_id, []))

    def get_predecessors(self, node_id: str) -> list[str]:
        return list(self._reverse_adjacency.get(node_id, []))

    def has_node(self, node_id: str) -> bool:
        return node_id in self._nodes

    def has_edge(self, source: str, target: str) -> bool:
        for edge in self._edges:
            if edge.source_node_id == source and edge.target_node_id == target:
                return True
        return False

    def topological_order(self) -> list[str]:
        """Return deterministic topological ordering using Kahn algorithm.

        Uses sorted insertion for determinism (no hash-order dependence).
        """
        in_degree: dict[str, int] = {nid: 0 for nid in self._nodes}
        for edge in self._edges:
            tid = edge.target_node_id
            if tid in in_degree:
                in_degree[tid] += 1

        queue = sorted(nid for nid, deg in in_degree.items() if deg == 0)
        order: list[str] = []

        while queue:
            current = queue.pop(0)
            order.append(current)
            for successor in sorted(self._adjacency.get(current, [])):
                in_degree[successor] -= 1
                if in_degree[successor] == 0:
                    queue.append(successor)
                    queue.sort()

        if len(order) != len(self._nodes):
            raise GraphError(
                "Cycle detected in workflow graph",
                cycle_nodes=[n for n in self._nodes if n not in order],
            )
        return order

    def detect_cycles(self) -> list[list[str]]:
        """Detect all cycles in the graph. Returns empty list if DAG."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {nid: WHITE for nid in self._nodes}
        cycles: list[list[str]] = []
        path: list[str] = []

        def dfs(node: str) -> None:
            color[node] = GRAY
            path.append(node)
            for neighbor in sorted(self._adjacency.get(node, [])):
                if neighbor not in color:
                    continue
                if color[neighbor] == GRAY:
                    idx = path.index(neighbor)
                    cycles.append(list(path[idx:] + [neighbor]))
                elif color[neighbor] == WHITE:
                    dfs(neighbor)
            path.pop()
            color[node] = BLACK

        for node in sorted(self._nodes):
            if color[node] == WHITE:
                dfs(node)
        return cycles

    def is_dag(self) -> bool:
        return len(self.detect_cycles()) == 0

    def get_parallel_groups(self) -> list[list[str]]:
        """Group nodes that can execute in parallel (same topological level)."""
        in_degree: dict[str, int] = {nid: 0 for nid in self._nodes}
        for edge in self._edges:
            tid = edge.target_node_id
            if tid in in_degree:
                in_degree[tid] += 1

        current_level = sorted(nid for nid, deg in in_degree.items() if deg == 0)
        groups: list[list[str]] = []

        while current_level:
            groups.append(current_level)
            next_level: list[str] = []
            for node in current_level:
                for succ in self._adjacency.get(node, []):
                    in_degree[succ] -= 1
                    if in_degree[succ] == 0:
                        next_level.append(succ)
            current_level = sorted(set(next_level))

        return groups

    def get_subgraph(self, node_ids: list[str]) -> WorkflowGraph:
        """Extract a subgraph containing only the specified nodes and their connecting edges."""
        id_set = set(node_ids)
        sub_nodes = [n for n in self._nodes.values() if n.node_id in id_set]
        sub_edges = [
            e for e in self._edges
            if e.source_node_id in id_set and e.target_node_id in id_set
        ]
        return WorkflowGraph(
            nodes=sub_nodes,
            edges=sub_edges,
            entry_nodes=[n for n in self._entry_nodes if n in id_set],
            exit_nodes=[n for n in self._exit_nodes if n in id_set],
            workflow_id=self._workflow_id,
            workflow_name=self._workflow_name,
            version=self._version,
        )

    def validate_integrity(self) -> list[str]:
        """Validate graph integrity. Returns list of violation messages."""
        violations: list[str] = []
        node_ids = set(self._nodes.keys())

        for edge in self._edges:
            if edge.source_node_id not in node_ids:
                violations.append(
                    f"Edge references unknown source node: {edge.source_node_id!r}"
                )
            if edge.target_node_id not in node_ids:
                violations.append(
                    f"Edge references unknown target node: {edge.target_node_id!r}"
                )

        for node_id in self._entry_nodes:
            if node_id not in node_ids:
                violations.append(f"Entry node {node_id!r} does not exist")

        for node_id in self._exit_nodes:
            if node_id not in node_ids:
                violations.append(f"Exit node {node_id!r} does not exist")

        if not self.is_dag():
            cycles = self.detect_cycles()
            for cycle in cycles:
                violations.append(f"Cycle detected: {' -> '.join(cycle)}")

        return violations

    def __repr__(self) -> str:
        return (
            f"WorkflowGraph(workflow={self._workflow_name!r}, "
            f"nodes={len(self._nodes)}, edges={len(self._edges)}, "
            f"dag={self.is_dag()})"
        )
