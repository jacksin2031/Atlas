"""Internal immutable model produced by the workflow parser.

The parser converts workflow definitions into this immutable model.
It MUST NOT execute workflows. Per RFC-0303 and RFC-0304.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True, kw_only=True)
class ParsedNode:
    """An immutable node in the parsed workflow graph."""
    node_id: str
    node_type: str
    label: str = ""
    configuration: dict[str, Any] = field(default_factory=dict)
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    ports_in: list[str] = field(default_factory=list)
    ports_out: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    retry_policy: RetryPolicy | None = None
    timeout_seconds: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True, kw_only=True)
class RetryPolicy:
    """Retry configuration for a node."""
    max_retries: int = 0
    backoff_strategy: str = "exponential"
    initial_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    retry_on: list[str] = field(default_factory=lambda: ["error"])


@dataclass(frozen=True, slots=True, kw_only=True)
class ParsedEdge:
    """An immutable edge connecting two nodes."""
    source_node_id: str
    target_node_id: str
    source_port: str = ""
    target_port: str = ""
    condition: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True, kw_only=True)
class ParsedWorkflow:
    """The complete parsed workflow as an immutable internal model.

    This is the output of the parser and input to the validator.
    """
    workflow_id: str
    workflow_name: str
    version: str = "1.0.0"
    nodes: tuple[ParsedNode, ...] = field(default_factory=tuple)
    edges: tuple[ParsedEdge, ...] = field(default_factory=tuple)
    entry_nodes: tuple[str, ...] = field(default_factory=tuple)
    exit_nodes: tuple[str, ...] = field(default_factory=tuple)
    parameters: tuple[Any, ...] = field(default_factory=tuple)
    variables: tuple[Any, ...] = field(default_factory=tuple)
    inputs: tuple[Any, ...] = field(default_factory=tuple)
    outputs: tuple[Any, ...] = field(default_factory=tuple)
    capabilities: tuple[Any, ...] = field(default_factory=tuple)
    dependencies: tuple[Any, ...] = field(default_factory=tuple)
    plugins: tuple[str, ...] = field(default_factory=tuple)
    permissions: tuple[Any, ...] = field(default_factory=tuple)

    @property
    def node_map(self) -> dict[str, ParsedNode]:
        return {n.node_id: n for n in self.nodes}

    @property
    def node_ids(self) -> frozenset[str]:
        return frozenset(n.node_id for n in self.nodes)

    def get_node(self, node_id: str) -> ParsedNode | None:
        return self.node_map.get(node_id)
