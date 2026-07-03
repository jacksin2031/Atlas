"""Workflow parser that converts definitions into immutable internal model.

The parser MUST NOT execute workflows. Per RFC-0303.
"""

from __future__ import annotations
from typing import Any

from atlas_workflow.common import ParserError, ManifestError
from atlas_workflow.manifest import WorkflowManifest
from atlas_workflow.parser.models import (
    ParsedNode,
    ParsedEdge,
    ParsedWorkflow,
    RetryPolicy,
)


class WorkflowParser:
    """Convert workflow definitions into an immutable internal model.

    The parser reads a WorkflowManifest and produces a ParsedWorkflow.
    It does NOT execute workflows, validate graph integrity, or
    interact with plugins directly.
    """

    def parse(self, manifest: WorkflowManifest) -> ParsedWorkflow:
        """Parse a WorkflowManifest into a ParsedWorkflow.

        Args:
            manifest: A validated WorkflowManifest.

        Returns:
            An immutable ParsedWorkflow.

        Raises:
            ParserError: If the manifest cannot be parsed.
        """
        nodes = self._parse_nodes(manifest)
        edges = self._parse_edges(manifest)
        entry = tuple(manifest.entry_nodes)
        exit_n = tuple(manifest.exit_nodes)

        return ParsedWorkflow(
            workflow_id=manifest.metadata.name,
            workflow_name=manifest.metadata.name,
            version=manifest.version,
            nodes=tuple(nodes),
            edges=tuple(edges),
            entry_nodes=entry,
            exit_nodes=exit_n,
            parameters=tuple(manifest.parameters),
            variables=tuple(manifest.variables),
            inputs=tuple(manifest.inputs),
            outputs=tuple(manifest.outputs),
            capabilities=tuple(manifest.capabilities),
            dependencies=tuple(manifest.dependencies),
            plugins=tuple(manifest.plugins),
            permissions=tuple(manifest.permissions),
        )

    def _parse_nodes(self, manifest: WorkflowManifest) -> list[ParsedNode]:
        result: list[ParsedNode] = []
        for node_def in manifest.node_definitions:
            if not isinstance(node_def, dict):
                raise ParserError(
                    "Node definition must be a dictionary",
                    details={"node": str(node_def)[:100]},
                )
            node_id = node_def.get("id", node_def.get("node_id", ""))
            if not node_id:
                raise ParserError(
                    "Node definition is missing required field: id",
                    details={"node": str(node_def)[:100]},
                )
            retry = None
            retry_raw = node_def.get("retry_policy")
            if retry_raw and isinstance(retry_raw, dict):
                retry = RetryPolicy(
                    max_retries=int(retry_raw.get("max_retries", 0)),
                    backoff_strategy=str(retry_raw.get("backoff_strategy", "exponential")),
                    initial_delay_seconds=float(retry_raw.get("initial_delay_seconds", 1.0)),
                    max_delay_seconds=float(retry_raw.get("max_delay_seconds", 60.0)),
                    retry_on=list(retry_raw.get("retry_on", ["error"])),
                )
            timeout = node_def.get("timeout_seconds")
            if timeout is not None:
                timeout = float(timeout)
            result.append(ParsedNode(
                node_id=str(node_id),
                node_type=str(node_def.get("type", "default")),
                label=str(node_def.get("label", "")),
                configuration={
                    k: v for k, v in node_def.get("config", node_def.get("configuration", {})).items()
                    if isinstance(k, str)
                },
                inputs=list(node_def.get("inputs", [])),
                outputs=list(node_def.get("outputs", [])),
                ports_in=list(node_def.get("ports_in", [])),
                ports_out=list(node_def.get("ports_out", [])),
                conditions=list(node_def.get("conditions", [])),
                retry_policy=retry,
                timeout_seconds=timeout,
                metadata={
                    k: v for k, v in node_def.get("metadata", {}).items()
                    if isinstance(k, str)
                },
            ))
        return result

    def _parse_edges(self, manifest: WorkflowManifest) -> list[ParsedEdge]:
        result: list[ParsedEdge] = []
        for edge_def in manifest.edge_definitions:
            if not isinstance(edge_def, dict):
                raise ParserError(
                    "Edge definition must be a dictionary",
                )
            source = edge_def.get("source", edge_def.get("source_node_id", ""))
            target = edge_def.get("target", edge_def.get("target_node_id", ""))
            if not source or not target:
                raise ParserError(
                    "Edge definition is missing required fields: source and target",
                    details={"edge": str(edge_def)},
                )
            result.append(ParsedEdge(
                source_node_id=str(source),
                target_node_id=str(target),
                source_port=str(edge_def.get("source_port", "")),
                target_port=str(edge_def.get("target_port", "")),
                condition=str(edge_def.get("condition", "")),
                metadata={
                    k: v for k, v in edge_def.get("metadata", {}).items()
                    if isinstance(k, str)
                },
            ))
        return result
