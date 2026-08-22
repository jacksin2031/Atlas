# Atlas Vision Runtime Execution Plan

"""
Compiled execution plan from a vision graph.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from atlas_vision.graph.graph import VisionGraph


@dataclass(frozen=True, slots=True, eq=True)
class VisionExecutionPlan:
    """Compiled deterministic execution plan."""

    node_order: tuple[str, ...]
    graph: VisionGraph
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def compile(cls, graph: VisionGraph) -> "VisionExecutionPlan":
        order = graph.topological_sort()
        return cls(node_order=tuple(order), graph=graph)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_order": list(self.node_order),
            "metadata": dict(self.metadata),
        }
