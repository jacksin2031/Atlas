# Atlas Vision Runtime Graph Edges

"""
Directed edges connecting vision graph nodes.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, eq=True)
class VisionEdge:
    """Immutable edge between two vision graph nodes."""

    source_node_id: str
    target_node_id: str
    data_type: str = "frame"

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source_node_id,
            "target": self.target_node_id,
            "data_type": self.data_type,
        }
