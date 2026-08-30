"""Workflow validator for schema, graph integrity, and requirements.

Validates parsed workflows before execution. Invalid workflows
MUST never reach execution. Per RFC-0317 and RFC-0304.
"""

from __future__ import annotations
from typing import Any

from atlas_workflow.common import (
    ValidationError,
    CapabilityRequirement,
    Capability,
)
from atlas_workflow.graph import WorkflowGraph
from atlas_workflow.parser import ParsedWorkflow
from atlas_workflow.node_registry import NodeRegistry


class WorkflowValidator:
    """Validate workflow definitions before execution.

    Checks schema integrity, graph structure, node references,
    capability requirements, version compatibility, and dependency
    constraints.
    """

    def __init__(self, node_registry: NodeRegistry | None = None) -> None:
        self._registry = node_registry

    def validate(self, parsed: ParsedWorkflow) -> list[str]:
        """Run all validations on a parsed workflow.

        Args:
            parsed: The parsed workflow to validate.

        Returns:
            List of violation messages. Empty means valid.

        Raises:
            ValidationError: If any violations are found.
        """
        violations: list[str] = []

        violations.extend(self._validate_schema(parsed))
        violations.extend(self._validate_graph(parsed))
        violations.extend(self._validate_node_references(parsed))
        violations.extend(self._validate_ports(parsed))
        violations.extend(self._validate_capabilities(parsed))
        violations.extend(self._validate_parameters(parsed))
        violations.extend(self._validate_variables(parsed))
        violations.extend(self._validate_version_compatibility(parsed))

        if violations:
            raise ValidationError(
                "; ".join(violations),
                violations=violations,
            )
        return violations

    def _validate_schema(self, parsed: ParsedWorkflow) -> list[str]:
        violations: list[str] = []
        if not parsed.workflow_id:
            violations.append("Workflow ID is required")
        if not parsed.workflow_name:
            violations.append("Workflow name is required")
        if not parsed.version:
            violations.append("Workflow version is required")
        return violations

    def _validate_graph(self, parsed: ParsedWorkflow) -> list[str]:
        violations: list[str] = []
        node_ids = parsed.node_ids

        if not parsed.entry_nodes:
            violations.append("Workflow must have at least one entry node")

        if not parsed.exit_nodes:
            violations.append("Workflow must have at least one exit node")

        for node_id in parsed.entry_nodes:
            if node_id not in node_ids:
                violations.append(f"Entry node {node_id!r} does not exist")

        for node_id in parsed.exit_nodes:
            if node_id not in node_ids:
                violations.append(f"Exit node {node_id!r} does not exist")

        return violations

    def _validate_node_references(self, parsed: ParsedWorkflow) -> list[str]:
        violations: list[str] = []
        node_ids = parsed.node_ids

        for edge in parsed.edges:
            if edge.source_node_id not in node_ids:
                violations.append(
                    f"Edge references unknown source node: {edge.source_node_id!r}"
                )
            if edge.target_node_id not in node_ids:
                violations.append(
                    f"Edge references unknown target node: {edge.target_node_id!r}"
                )

        return violations

    def _validate_ports(self, parsed: ParsedWorkflow) -> list[str]:
        violations: list[str] = []
        node_map = parsed.node_map

        for edge in parsed.edges:
            source_node = node_map.get(edge.source_node_id)
            target_node = node_map.get(edge.target_node_id)

            if source_node:
                if edge.source_port and edge.source_port not in source_node.ports_out:
                    violations.append(
                        f"Source port {edge.source_port!r} not found on node {edge.source_node_id!r}"
                    )
            if target_node:
                if edge.target_port and edge.target_port not in target_node.ports_in:
                    violations.append(
                        f"Target port {edge.target_port!r} not found on node {edge.target_node_id!r}"
                    )
            if source_node and target_node and edge.source_port and edge.target_port:
                source_types = source_node.metadata.get("output_port_types", {})
                target_types = target_node.metadata.get("input_port_types", {})
                source_type = source_types.get(edge.source_port) if isinstance(source_types, dict) else None
                target_type = target_types.get(edge.target_port) if isinstance(target_types, dict) else None
                if source_type and target_type and not self._types_compatible(str(source_type), str(target_type)):
                    violations.append(
                        f"Port type mismatch: {edge.source_node_id}.{edge.source_port} "
                        f"({source_type}) -> {edge.target_node_id}.{edge.target_port} ({target_type})"
                    )

        return violations

    @staticmethod
    def _types_compatible(source: str, target: str) -> bool:
        if source == target or "any" in {source, target}:
            return True
        if {source, target} <= {"integer", "float", "number"}:
            return True
        reference_types = {"point_reference", "bounds_reference", "region_reference"}
        if target == "target_reference" and source in reference_types:
            return True
        return target == "object" and source in {
            "image", "frame_reference", "knowledge_reference", "ai_response",
            "target_reference", *reference_types,
        }

    def _validate_capabilities(self, parsed: ParsedWorkflow) -> list[str]:
        """Validate capability requirements. Only checks if a registry is available."""
        violations: list[str] = []
        if not self._registry:
            return violations

        for cap_req in parsed.capabilities:
            if not isinstance(cap_req, CapabilityRequirement):
                continue
            available = self._registry.list_capabilities()
            found = False
            for cap_name in available:
                cap_req_copy = CapabilityRequirement(
                    name=cap_req.name,
                    minimum_version=cap_req.minimum_version,
                )
                if cap_name == cap_req.name:
                    found = True
                    break
            if not found:
                violations.append(
                    f"Required capability {cap_req.name!r} (min {cap_req.minimum_version}) not available"
                )
        return violations

    def _validate_parameters(self, parsed: ParsedWorkflow) -> list[str]:
        violations: list[str] = []
        seen_names: set[str] = set()

        for param in parsed.parameters:
            name = getattr(param, "name", None)
            if name and name in seen_names:
                violations.append(f"Duplicate parameter name: {name!r}")
            if name:
                seen_names.add(name)

        return violations

    def _validate_variables(self, parsed: ParsedWorkflow) -> list[str]:
        violations: list[str] = []
        seen_names: set[str] = set()

        for var in parsed.variables:
            name = getattr(var, "name", None)
            if name and name in seen_names:
                violations.append(f"Duplicate variable name: {name!r}")
            if name:
                seen_names.add(name)

        return violations

    def _validate_version_compatibility(self, parsed: ParsedWorkflow) -> list[str]:
        violations: list[str] = []
        version = parsed.version
        if not version:
            violations.append("Version is required")
            return violations
        parts = version.split(".")
        if len(parts) < 2:
            violations.append(f"Invalid version format: {version!r}")
        return violations

    def validate_graph(self, graph: WorkflowGraph) -> list[str]:
        """Validate a WorkflowGraph for integrity."""
        return graph.validate_integrity()
