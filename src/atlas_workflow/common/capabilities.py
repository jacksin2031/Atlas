"""Common capability model per RFC-1003."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True, kw_only=True)
class CapabilityRequirement:
    """A required capability for a workflow or node."""
    name: str
    version: str = "1.0.0"
    minimum_version: str = "1.0.0"
    description: str = ""

    def satisfies(self, actual_version: str) -> bool:
        """Check if actual_version satisfies this requirement."""
        av_parts = _parse_version(actual_version)
        req_parts = _parse_version(self.minimum_version)
        return av_parts >= req_parts


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


@dataclass(frozen=True, slots=True, kw_only=True)
class Capability:
    """A capability provided by a plugin or the runtime."""
    name: str
    version: str = "1.0.0"
    provider: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def satisfies(self, requirement: CapabilityRequirement) -> bool:
        return self.name == requirement.name and requirement.satisfies(self.version)


@dataclass(frozen=True, slots=True, kw_only=True)
class Permission:
    """A permission for workflow execution."""
    name: str
    resource: str = "*"
    actions: list[str] = field(default_factory=lambda: ["execute"])
    description: str = ""

    def allows(self, action: str, resource: str = "*") -> bool:
        return action in self.actions and (self.resource == "*" or self.resource == resource)
