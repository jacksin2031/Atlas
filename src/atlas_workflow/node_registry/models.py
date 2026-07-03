"""Node registry models for plugin-discovered node definitions."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True, kw_only=True)
class NodeDefinition:
    """A discoverable node definition from a plugin.

    Per RFC-0323 (Plugin Integration) and RFC-0309 (Actions).
    """
    node_id: str
    node_type: str
    label: str = ""
    description: str = ""
    version: str = "1.0.0"
    capabilities: list[str] = field(default_factory=list)
    required_plugins: list[str] = field(default_factory=list)
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    configuration_schema: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def satisfies_capabilities(self, required: list[str]) -> bool:
        """Check if this node definition satisfies the required capabilities."""
        return all(cap in self.capabilities for cap in required)

    def satisfies_version(self, min_version: str) -> bool:
        """Check if version meets minimum requirement."""
        return _compare_version(self.version, min_version) >= 0


def _compare_version(v1: str, v2: str) -> int:
    p1 = _parse_version(v1)
    p2 = _parse_version(v2)
    if p1 < p2:
        return -1
    if p1 > p2:
        return 1
    return 0


def _parse_version(version_str: str) -> tuple[int, ...]:
    parts: list[int] = []
    for seg in version_str.split("."):
        try:
            parts.append(int(seg))
        except ValueError:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)
