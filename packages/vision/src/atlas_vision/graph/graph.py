# Atlas Vision Runtime Graph

"""
Deterministic directed acyclic graph for vision pipeline execution.

Uses Kahn's algorithm with sorted insertion for deterministic ordering.
"""
from __future__ import annotations

from collections import deque
from typing import Any

from atlas_vision.errors import CycleDetectedError, InvalidGraphNodeError
from atlas_vision.graph.edges import VisionEdge
from atlas_vision.graph.nodes import VisionNode


class VisionGraph:
    """Deterministic DAG for vision pipeline execution."""

    def __init__(self) -> None:
        self._nodes: dict[str, VisionNode] = {}
        self._edges: list[VisionEdge] = []
        self._adjacency: dict[str, list[str]] = {}
        self._reverse_adj: dict[str, list[str]] = {}

    def add_node(self, node: VisionNode) -> None:
        if node.node_id in self._nodes:
            return
        self._nodes[node.node_id] = node
        if node.node_id not in self._adjacency:
            self._adjacency[node.node_id] = []
        if node.node_id not in self._reverse_adj:
            self._reverse_adj[node.node_id] = []

    def add_edge(self, edge: VisionEdge) -> None:
        if edge.source_node_id not in self._nodes:
            raise InvalidGraphNodeError(
                f"Source node not found: {edge.source_node_id}",
                edge.source_node_id,
            )
        if edge.target_node_id not in self._nodes:
            raise InvalidGraphNodeError(
                f"Target node not found: {edge.target_node_id}",
                edge.target_node_id,
            )
        self._edges.append(edge)
        self._adjacency[edge.source_node_id].append(edge.target_node_id)
        if edge.target_node_id not in self._reverse_adj:
            self._reverse_adj[edge.target_node_id] = []
        self._reverse_adj[edge.target_node_id].append(edge.source_node_id)

    def get_nodes(self) -> list[VisionNode]:
        return list(self._nodes.values())

    def get_edges(self) -> list[VisionEdge]:
        return list(self._edges)

    def topological_sort(self) -> list[str]:
        in_degree: dict[str, int] = {n: 0 for n in self._nodes}
        for src, targets in self._adjacency.items():
            for tgt in targets:
                in_degree[tgt] = in_degree.get(tgt, 0) + 1

        queue = sorted([n for n, d in in_degree.items() if d == 0])
        result: list[str] = []

        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbor in sorted(self._adjacency.get(node, [])):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    queue.sort()

        if len(result) != len(self._nodes):
            raise CycleDetectedError("Cycle detected in graph", result)

        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in self._nodes.values()],
            "edges": [e.to_dict() for e in self._edges],
        }
