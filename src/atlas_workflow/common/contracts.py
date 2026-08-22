"""Common contract model per RFC-1004."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True, kw_only=True)
class InputContract:
    """Defines an input contract for a workflow or node."""
    name: str
    type: str = "any"
    required: bool = False
    default: Any = None
    description: str = ""
    validation: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True, kw_only=True)
class OutputContract:
    """Defines an output contract for a workflow or node."""
    name: str
    type: str = "any"
    description: str = ""
    source: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class VariableDefinition:
    """Defines a workflow or node variable."""
    name: str
    type: str = "any"
    scope: str = "local"
    default: Any = None
    description: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class PortDefinition:
    """Defines a connection port for a workflow node."""
    name: str
    direction: str = "both"
    type: str = "any"
    optional: bool = False
