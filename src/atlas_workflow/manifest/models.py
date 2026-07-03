"""Workflow manifest models for parsing and validation."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from atlas_workflow.common import (
    ManifestMetadata,
    ManifestDependency,
    ManifestParameter,
    ManifestVariable,
    ManifestInput,
    ManifestOutput,
    CapabilityRequirement,
    Permission,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowManifest:
    """Complete workflow manifest containing all declarative metadata.

    Represents the parsed and validated workflow definition before
    graph construction. Per RFC-1005 and RFC-0304.
    """
    metadata: ManifestMetadata
    version: str = "1.0.0"
    dependencies: list[ManifestDependency] = field(default_factory=list)
    capabilities: list[CapabilityRequirement] = field(default_factory=list)
    plugins: list[str] = field(default_factory=list)
    permissions: list[Permission] = field(default_factory=list)
    parameters: list[ManifestParameter] = field(default_factory=list)
    variables: list[ManifestVariable] = field(default_factory=list)
    inputs: list[ManifestInput] = field(default_factory=list)
    outputs: list[ManifestOutput] = field(default_factory=list)
    graph_definition: dict[str, Any] = field(default_factory=dict)
    node_definitions: list[dict[str, Any]] = field(default_factory=list)
    edge_definitions: list[dict[str, Any]] = field(default_factory=list)
    entry_nodes: list[str] = field(default_factory=list)
    exit_nodes: list[str] = field(default_factory=list)
    metadata: ManifestMetadata
