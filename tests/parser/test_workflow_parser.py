"""Tests for workflow parser."""

from __future__ import annotations
import pytest

from atlas_workflow.common import ParserError, ManifestError
from atlas_workflow.manifest import WorkflowManifest, WorkflowManifestParser
from atlas_workflow.parser import WorkflowParser, ParsedWorkflow, RetryPolicy


class TestWorkflowParser:
    def test_parse_minimal_manifest(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({"metadata": {"name": "test"}})
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert parsed.workflow_id == "test"
        assert parsed.workflow_name == "test"
        assert parsed.nodes == ()
        assert parsed.edges == ()

    def test_parse_manifest_with_nodes(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "nodes": [
                {"id": "n1", "type": "noop", "label": "Node 1"},
                {"id": "n2", "type": "transform", "config": {"key": "val"}},
            ],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert len(parsed.nodes) == 2
        assert parsed.nodes[0].node_id == "n1"
        assert parsed.nodes[0].node_type == "noop"
        assert parsed.nodes[0].label == "Node 1"
        assert parsed.nodes[1].node_type == "transform"
        assert parsed.nodes[1].configuration["key"] == "val"

    def test_parse_manifest_with_edges(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "nodes": [
                {"id": "n1", "type": "noop", "ports_out": ["out1"]},
                {"id": "n2", "type": "noop", "ports_in": ["in1"]},
            ],
            "edges": [
                {"source": "n1", "target": "n2", "source_port": "out1", "target_port": "in1"},
            ],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert len(parsed.edges) == 1
        assert parsed.edges[0].source_node_id == "n1"
        assert parsed.edges[0].target_node_id == "n2"
        assert parsed.edges[0].source_port == "out1"
        assert parsed.edges[0].target_port == "in1"

    def test_parse_manifest_with_retry_policy(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "nodes": [
                {
                    "id": "n1", "type": "noop",
                    "retry_policy": {
                        "max_retries": 3,
                        "backoff_strategy": "linear",
                        "initial_delay_seconds": 0.5,
                        "max_delay_seconds": 30,
                        "retry_on": ["timeout", "error"],
                    },
                },
            ],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert parsed.nodes[0].retry_policy is not None
        assert parsed.nodes[0].retry_policy.max_retries == 3
        assert parsed.nodes[0].retry_policy.backoff_strategy == "linear"

    def test_parse_manifest_with_timeout(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "nodes": [{"id": "n1", "type": "noop", "timeout_seconds": 60}],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert parsed.nodes[0].timeout_seconds == 60.0

    def test_parse_manifest_with_entry_exit_nodes(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "entry_nodes": ["start"],
            "exit_nodes": ["end"],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert parsed.entry_nodes == ("start",)
        assert parsed.exit_nodes == ("end",)

    def test_parse_manifest_with_parameters(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "parameters": [{"name": "p1", "type": "int", "required": True, "default": 42}],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert len(parsed.parameters) == 1
        assert parsed.parameters[0].name == "p1"
        assert parsed.parameters[0].type == "int"
        assert parsed.parameters[0].default == 42

    def test_parse_manifest_with_variables(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "variables": [{"name": "v1", "type": "string", "scope": "global"}],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert len(parsed.variables) == 1
        assert parsed.variables[0].name == "v1"

    def test_parse_manifest_with_capabilities(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "capabilities": [{"name": "basic", "minimum_version": "1.0.0"}],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert len(parsed.capabilities) == 1
        assert parsed.capabilities[0].name == "basic"

    def test_parse_manifest_with_plugins(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "plugins": ["plugin-a", "plugin-b"],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert parsed.plugins == ("plugin-a", "plugin-b")

    def test_parse_manifest_with_permissions(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "permissions": [{"name": "execute", "actions": ["run"]}],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert len(parsed.permissions) == 1

    def test_parse_manifest_with_inputs(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "inputs": [{"name": "data", "type": "object", "required": True}],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert len(parsed.inputs) == 1
        assert parsed.inputs[0].name == "data"

    def test_parse_manifest_with_outputs(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "outputs": [{"name": "result", "type": "string"}],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert len(parsed.outputs) == 1
        assert parsed.outputs[0].name == "result"

    def test_parsed_workflow_node_map(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "nodes": [{"id": "n1", "type": "a"}, {"id": "n2", "type": "b"}],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert parsed.node_map["n1"].node_type == "a"
        assert parsed.node_map["n2"].node_type == "b"
        assert parsed.get_node("n1") is not None
        assert parsed.get_node("nonexistent") is None

    def test_parsed_workflow_node_ids(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "nodes": [{"id": "n1", "type": "a"}, {"id": "n2", "type": "b"}],
        })
        parser = WorkflowParser()
        parsed = parser.parse(manifest)
        assert parsed.node_ids == frozenset({"n1", "n2"})

    def test_parse_missing_node_id_raises(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "nodes": [{"type": "noop"}],
        })
        parser = WorkflowParser()
        with pytest.raises(ParserError, match="missing required field"):
            parser.parse(manifest)

    def test_parse_missing_edge_fields_raises(self):
        manifest_parser = WorkflowManifestParser()
        manifest = manifest_parser.parse({
            "metadata": {"name": "test"},
            "edges": [{"source": "n1"}],
        })
        parser = WorkflowParser()
        with pytest.raises(ParserError, match="missing required fields"):
            parser.parse(manifest)

    def test_parse_node_definition_as_string_raises(self):
        manifest_parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            manifest_parser.parse({
                "metadata": {"name": "test"},
                "nodes": ["not a dict"],
            })

    def test_parse_edge_definition_as_string_raises(self):
        manifest_parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            manifest_parser.parse({
                "metadata": {"name": "test"},
                "edges": ["not a dict"],
            })
