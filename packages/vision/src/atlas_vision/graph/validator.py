# Atlas Vision Runtime Graph Validator

"""
Validation for vision execution graphs.
"""
from __future__ import annotations

from atlas_vision.errors import CycleDetectedError, InvalidGraphNodeError
from atlas_vision.graph.graph import VisionGraph


class VisionGraphValidator:
    """Validates vision execution graphs."""

    @staticmethod
    def validate(graph: VisionGraph) -> bool:
        if not graph.get_nodes():
            raise InvalidGraphNodeError("Graph has no nodes")
        try:
            graph.topological_sort()
        except CycleDetectedError:
            raise
        edges = graph.get_edges()
        nodes = {n.node_id for n in graph.get_nodes()}
        for edge in edges:
            if edge.source_node_id not in nodes:
                raise InvalidGraphNodeError(
                    f"Edge references unknown node: {edge.source_node_id}",
                    edge.source_node_id,
                )
            if edge.target_node_id not in nodes:
                raise InvalidGraphNodeError(
                    f"Edge references unknown node: {edge.target_node_id}",
                    edge.target_node_id,
                )
        return True

    @staticmethod
    def has_cycle(graph: VisionGraph) -> bool:
        try:
            graph.topological_sort()
            return False
        except CycleDetectedError:
            return True

    @staticmethod
    def count_nodes(graph: VisionGraph) -> int:
        return len(graph.get_nodes())

    @staticmethod
    def count_edges(graph: VisionGraph) -> int:
        return len(graph.get_edges())
