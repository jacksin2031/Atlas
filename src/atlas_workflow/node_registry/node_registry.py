"""Node registry for discovering executable node definitions from plugins.

Per RFC-0323 and RFC-0309. The registry supports lookup, registration,
capability filtering, and version filtering.
"""

from __future__ import annotations
from typing import Any

from atlas_workflow.common import PluginError
from atlas_workflow.node_registry.models import NodeDefinition


class NodeRegistry:
    """Registry for discovering and filtering node definitions from plugins.

    The registry is the single source of truth for available node types.
    It supports:
    - Lookup by node ID or type
    - Registration of node definitions
    - Capability filtering
    - Version filtering
    """

    def __init__(self) -> None:
        self._definitions: dict[str, NodeDefinition] = {}
        self._by_type: dict[str, list[str]] = {}
        self._capabilities: dict[str, list[str]] = {}

    @property
    def definitions(self) -> dict[str, NodeDefinition]:
        return dict(self._definitions)

    def register(self, definition: NodeDefinition) -> None:
        """Register a node definition.

        Args:
            definition: The node definition to register.

        Raises:
            PluginError: If a definition with the same ID already exists.
        """
        if definition.node_id in self._definitions:
            raise PluginError(
                f"Node definition already registered: {definition.node_id!r}",
                plugin_name=definition.node_id,
            )
        self._definitions[definition.node_id] = definition
        self._by_type.setdefault(definition.node_type, []).append(definition.node_id)
        for cap in definition.capabilities:
            self._capabilities.setdefault(cap, []).append(definition.node_id)

    def unregister(self, node_id: str) -> bool:
        """Remove a node definition from the registry."""
        if node_id not in self._definitions:
            return False
        defn = self._definitions.pop(node_id)
        type_list = self._by_type.get(defn.node_type, [])
        if node_id in type_list:
            type_list.remove(node_id)
        for cap in defn.capabilities:
            cap_list = self._capabilities.get(cap, [])
            if node_id in cap_list:
                cap_list.remove(node_id)
        return True

    def lookup(self, node_id: str) -> NodeDefinition | None:
        """Look up a node definition by ID."""
        return self._definitions.get(node_id)

    def lookup_by_type(self, node_type: str) -> list[NodeDefinition]:
        """Look up all node definitions of a given type."""
        ids = self._by_type.get(node_type, [])
        return [self._definitions[i] for i in ids if i in self._definitions]

    def list_all(self) -> list[NodeDefinition]:
        """List all registered node definitions."""
        return list(self._definitions.values())

    def list_capabilities(self) -> list[str]:
        """List all registered capability names."""
        return list(self._capabilities.keys())

    def filter_by_capability(self, capability: str) -> list[NodeDefinition]:
        """Filter node definitions by a required capability."""
        ids = self._capabilities.get(capability, [])
        return [self._definitions[i] for i in ids if i in self._definitions]

    def filter_by_version(self, min_version: str) -> list[NodeDefinition]:
        """Filter node definitions by minimum version."""
        return [
            d for d in self._definitions.values()
            if d.satisfies_version(min_version)
        ]

    def filter_by_capabilities(self, capabilities: list[str]) -> list[NodeDefinition]:
        """Filter node definitions that satisfy ALL required capabilities."""
        result: list[NodeDefinition] = []
        for defn in self._definitions.values():
            if defn.satisfies_capabilities(capabilities):
                result.append(defn)
        return result

    def get_available_for_capabilities(self, required_caps: list[str]) -> list[NodeDefinition]:
        """Get node definitions that satisfy the given capability requirements."""
        return self.filter_by_capabilities(required_caps)
