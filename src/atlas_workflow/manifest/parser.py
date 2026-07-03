"""Workflow manifest parser.

Parses raw manifest dictionaries into WorkflowManifest objects.
Per RFC-1005 and RFC-0305.
"""

from __future__ import annotations
from typing import Any

from atlas_workflow.common import (
    ManifestError,
    ManifestMetadata,
    ManifestDependency,
    ManifestParameter,
    ManifestVariable,
    ManifestInput,
    ManifestOutput,
    CapabilityRequirement,
    Permission,
)
from atlas_workflow.manifest.models import WorkflowManifest


_REQUIRED_FIELDS = ("name",)


class WorkflowManifestParser:
    """Parse raw manifest dictionaries into WorkflowManifest objects."""

    def parse(self, raw: dict[str, Any]) -> WorkflowManifest:
        if not isinstance(raw, dict):
            raise ManifestError(
                "Manifest must be a dictionary",
                field="root",
            )

        self._check_required_fields(raw)

        metadata = self._parse_metadata(raw)
        version = str(raw.get("version", "1.0.0"))
        dependencies = self._parse_dependencies(raw)
        capabilities = self._parse_capabilities(raw)
        plugins = self._parse_string_list(raw, "plugins")
        permissions = self._parse_permissions(raw)
        parameters = self._parse_parameters(raw)
        variables = self._parse_variables(raw)
        inputs = self._parse_inputs(raw)
        outputs = self._parse_outputs(raw)
        graph_def = dict(raw.get("graph", {}))
        node_defs = self._parse_node_definitions(raw)
        edge_defs = self._parse_edge_definitions(raw)
        entry = self._parse_string_list(raw, "entry_nodes")
        exit_n = self._parse_string_list(raw, "exit_nodes")

        return WorkflowManifest(
            metadata=metadata,
            version=version,
            dependencies=dependencies,
            capabilities=capabilities,
            plugins=plugins,
            permissions=permissions,
            parameters=parameters,
            variables=variables,
            inputs=inputs,
            outputs=outputs,
            graph_definition=graph_def,
            node_definitions=node_defs,
            edge_definitions=edge_defs,
            entry_nodes=entry,
            exit_nodes=exit_n,
        )

    def parse_metadata(self, raw: dict[str, Any]) -> ManifestMetadata:
        meta_raw = raw.get("metadata", {})
        if not isinstance(meta_raw, dict):
            raise ManifestError(
                "metadata must be a dictionary",
                field="metadata",
            )
        return ManifestMetadata(
            name=str(meta_raw.get("name", raw.get("name", ""))),
            version=str(meta_raw.get("version", "1.0.0")),
            description=str(meta_raw.get("description", "")),
            author=str(meta_raw.get("author", "")),
            tags=self._parse_string_list(meta_raw, "tags"),
        )

    def _check_required_fields(self, raw: dict[str, Any]) -> None:
        meta = raw.get("metadata", {})
        if isinstance(meta, dict):
            name = meta.get("name")
        else:
            name = None
        if not name:
            name = raw.get("name")
        if not name:
            raise ManifestError(
                "Manifest is missing required field: metadata.name",
                field="metadata.name",
            )

    def _parse_metadata(self, raw: dict[str, Any]) -> ManifestMetadata:
        meta_raw = raw.get("metadata", {})
        if not isinstance(meta_raw, dict):
            meta_raw = {"name": raw.get("name", "")}
        return ManifestMetadata(
            name=str(meta_raw.get("name", raw.get("name", ""))),
            version=str(meta_raw.get("version", "1.0.0")),
            description=str(meta_raw.get("description", "")),
            author=str(meta_raw.get("author", "")),
            tags=self._parse_string_list(meta_raw, "tags"),
        )

    def _parse_dependencies(self, raw: dict[str, Any]) -> list[ManifestDependency]:
        deps_raw = raw.get("dependencies", [])
        if not isinstance(deps_raw, list):
            raise ManifestError(
                "dependencies must be a list",
                field="dependencies",
            )
        result: list[ManifestDependency] = []
        for i, dep in enumerate(deps_raw):
            if not isinstance(dep, dict):
                raise ManifestError(
                    f"dependency[{i}] must be a dictionary",
                    field=f"dependencies.{i}",
                )
            if "name" not in dep:
                raise ManifestError(
                    f"dependency[{i}] is missing required field: name",
                    field=f"dependencies.{i}.name",
                )
            result.append(ManifestDependency(
                name=str(dep["name"]),
                version=str(dep.get("version", ">=1.0.0")),
                optional=bool(dep.get("optional", False)),
            ))
        return result

    def _parse_capabilities(self, raw: dict[str, Any]) -> list[CapabilityRequirement]:
        caps_raw = raw.get("capabilities", [])
        if not isinstance(caps_raw, list):
            raise ManifestError(
                "capabilities must be a list",
                field="capabilities",
            )
        result: list[CapabilityRequirement] = []
        for cap in caps_raw:
            if not isinstance(cap, dict):
                raise ManifestError(
                    "capability must be a dictionary",
                    field="capabilities",
                )
            if "name" not in cap:
                raise ManifestError(
                    "capability is missing required field: name",
                    field="capabilities.name",
                )
            result.append(CapabilityRequirement(
                name=str(cap["name"]),
                version=str(cap.get("version", "1.0.0")),
                minimum_version=str(cap.get("minimum_version", "1.0.0")),
                description=str(cap.get("description", "")),
            ))
        return result

    def _parse_permissions(self, raw: dict[str, Any]) -> list[Permission]:
        perms_raw = raw.get("permissions", [])
        if not isinstance(perms_raw, list):
            raise ManifestError(
                "permissions must be a list",
                field="permissions",
            )
        result: list[Permission] = []
        for perm in perms_raw:
            if not isinstance(perm, dict):
                raise ManifestError(
                    "permission must be a dictionary",
                    field="permissions",
                )
            if "name" not in perm:
                raise ManifestError(
                    "permission is missing required field: name",
                    field="permissions.name",
                )
            result.append(Permission(
                name=str(perm["name"]),
                resource=str(perm.get("resource", "*")),
                actions=self._parse_string_list(perm, "actions"),
                description=str(perm.get("description", "")),
            ))
        return result

    def _parse_parameters(self, raw: dict[str, Any]) -> list[ManifestParameter]:
        params_raw = raw.get("parameters", [])
        if not isinstance(params_raw, list):
            raise ManifestError(
                "parameters must be a list",
                field="parameters",
            )
        result: list[ManifestParameter] = []
        for param in params_raw:
            if not isinstance(param, dict):
                raise ManifestError(
                    "parameter must be a dictionary",
                    field="parameters",
                )
            if "name" not in param:
                raise ManifestError(
                    "parameter is missing required field: name",
                    field="parameters.name",
                )
            result.append(ManifestParameter(
                name=str(param["name"]),
                type=str(param.get("type", "string")),
                default=param.get("default"),
                required=bool(param.get("required", False)),
                description=str(param.get("description", "")),
                validation=param.get("validation", {}),
            ))
        return result

    def _parse_variables(self, raw: dict[str, Any]) -> list[ManifestVariable]:
        vars_raw = raw.get("variables", [])
        if not isinstance(vars_raw, list):
            raise ManifestError(
                "variables must be a list",
                field="variables",
            )
        result: list[ManifestVariable] = []
        for var in vars_raw:
            if not isinstance(var, dict):
                raise ManifestError(
                    "variable must be a dictionary",
                    field="variables",
                )
            if "name" not in var:
                raise ManifestError(
                    "variable is missing required field: name",
                    field="variables.name",
                )
            result.append(ManifestVariable(
                name=str(var["name"]),
                type=str(var.get("type", "any")),
                scope=str(var.get("scope", "global")),
                default=var.get("default"),
                description=str(var.get("description", "")),
            ))
        return result

    def _parse_inputs(self, raw: dict[str, Any]) -> list[ManifestInput]:
        inputs_raw = raw.get("inputs", [])
        if not isinstance(inputs_raw, list):
            raise ManifestError(
                "inputs must be a list",
                field="inputs",
            )
        result: list[ManifestInput] = []
        for inp in inputs_raw:
            if not isinstance(inp, dict):
                raise ManifestError(
                    "input must be a dictionary",
                    field="inputs",
                )
            if "name" not in inp:
                raise ManifestError(
                    "input is missing required field: name",
                    field="inputs.name",
                )
            result.append(ManifestInput(
                name=str(inp["name"]),
                type=str(inp.get("type", "any")),
                required=bool(inp.get("required", False)),
                description=str(inp.get("description", "")),
            ))
        return result

    def _parse_outputs(self, raw: dict[str, Any]) -> list[ManifestOutput]:
        outputs_raw = raw.get("outputs", [])
        if not isinstance(outputs_raw, list):
            raise ManifestError(
                "outputs must be a list",
                field="outputs",
            )
        result: list[ManifestOutput] = []
        for out in outputs_raw:
            if not isinstance(out, dict):
                raise ManifestError(
                    "output must be a dictionary",
                    field="outputs",
                )
            if "name" not in out:
                raise ManifestError(
                    "output is missing required field: name",
                    field="outputs.name",
                )
            result.append(ManifestOutput(
                name=str(out["name"]),
                type=str(out.get("type", "any")),
                description=str(out.get("description", "")),
                expression=str(out.get("expression", "")),
            ))
        return result

    def _parse_node_definitions(self, raw: dict[str, Any]) -> list[dict[str, Any]]:
        nodes_raw = raw.get("nodes", [])
        if not isinstance(nodes_raw, list):
            raise ManifestError(
                "nodes must be a list",
                field="nodes",
            )
        result: list[dict[str, Any]] = []
        for i, node in enumerate(nodes_raw):
            if not isinstance(node, dict):
                raise ManifestError(
                    f"nodes[{i}] must be a dictionary",
                    field=f"nodes.{i}",
                )
            result.append(dict(node))
        return result

    def _parse_edge_definitions(self, raw: dict[str, Any]) -> list[dict[str, Any]]:
        edges_raw = raw.get("edges", [])
        if not isinstance(edges_raw, list):
            raise ManifestError(
                "edges must be a list",
                field="edges",
            )
        result: list[dict[str, Any]] = []
        for i, edge in enumerate(edges_raw):
            if not isinstance(edge, dict):
                raise ManifestError(
                    f"edges[{i}] must be a dictionary",
                    field=f"edges.{i}",
                )
            result.append(dict(edge))
        return result

    def _parse_string_list(self, raw: dict[str, Any], key: str) -> list[str]:
        val = raw.get(key, [])
        if not isinstance(val, list):
            return []
        return [str(v) for v in val]
