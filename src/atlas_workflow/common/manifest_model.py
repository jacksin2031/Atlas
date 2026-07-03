"""Common manifest model per RFC-1005."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True, kw_only=True)
class ManifestMetadata:
    """Metadata for a workflow manifest."""
    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True, kw_only=True)
class ManifestDependency:
    """A dependency declaration for a workflow."""
    name: str
    version: str = ">=1.0.0"
    optional: bool = False


@dataclass(frozen=True, slots=True, kw_only=True)
class ManifestParameter:
    """A workflow or node parameter."""
    name: str
    type: str = "string"
    default: Any = None
    required: bool = False
    description: str = ""
    validation: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True, kw_only=True)
class ManifestVariable:
    """A workflow or node variable definition."""
    name: str
    type: str = "any"
    scope: str = "global"
    default: Any = None
    description: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class ManifestInput:
    """An input definition for a workflow."""
    name: str
    type: str = "any"
    required: bool = False
    description: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class ManifestOutput:
    """An output definition for a workflow."""
    name: str
    type: str = "any"
    description: str = ""
    expression: str = ""
