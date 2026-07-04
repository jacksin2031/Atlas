# Atlas Vision Runtime Graph Nodes

"""
Directed graph nodes for vision pipeline execution.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True, eq=True)
class VisionNode:
    """Immutable node in the vision execution graph."""

    node_id: str
    stage_name: str
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "stage_name": self.stage_name,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "metadata": dict(self.metadata),
        }
