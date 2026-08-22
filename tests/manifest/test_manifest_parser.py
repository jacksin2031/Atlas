"""Tests for workflow manifest parser."""

from __future__ import annotations
import pytest

from atlas_workflow.common import ManifestError
from atlas_workflow.manifest import WorkflowManifestParser


class TestWorkflowManifestParser:
    def test_parse_minimal_manifest(self):
        raw = {"metadata": {"name": "test-wf"}}
        parser = WorkflowManifestParser()
        result = parser.parse(raw)
        assert result.metadata.name == "test-wf"
        assert result.version == "1.0.0"
        assert result.dependencies == []
        assert result.capabilities == []
        assert result.plugins == []
        assert result.permissions == []
        assert result.parameters == []
        assert result.variables == []
        assert result.inputs == []
        assert result.outputs == []
        assert result.entry_nodes == []
        assert result.exit_nodes == []

    def test_parse_full_manifest(self):
        raw = {
            "metadata": {"name": "full-wf", "version": "2.0.0", "description": "A full workflow"},
            "version": "2.0.0",
            "dependencies": [{"name": "dep1", "version": ">=1.0.0", "optional": True}],
            "capabilities": [{"name": "basic", "minimum_version": "1.0.0"}],
            "plugins": ["plugin-a", "plugin-b"],
            "permissions": [{"name": "execute", "actions": ["run"]}],
            "parameters": [{"name": "p1", "type": "string", "required": True}],
            "variables": [{"name": "v1", "type": "int", "scope": "global"}],
            "inputs": [{"name": "in1", "type": "object", "required": True}],
            "outputs": [{"name": "out1", "type": "string"}],
            "entry_nodes": ["start"],
            "exit_nodes": ["end"],
            "nodes": [{"id": "start", "type": "noop"}],
            "edges": [{"source": "start", "target": "end"}],
        }
        parser = WorkflowManifestParser()
        result = parser.parse(raw)
        assert result.metadata.name == "full-wf"
        assert len(result.dependencies) == 1
        assert result.dependencies[0].name == "dep1"
        assert len(result.capabilities) == 1
        assert len(result.plugins) == 2
        assert len(result.permissions) == 1
        assert len(result.parameters) == 1
        assert len(result.variables) == 1
        assert len(result.inputs) == 1
        assert len(result.outputs) == 1
        assert result.entry_nodes == ["start"]
        assert result.exit_nodes == ["end"]

    def test_parse_missing_name_raises(self):
        raw = {"metadata": {}}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError, match="missing required field"):
            parser.parse(raw)

    def test_parse_non_dict_raises(self):
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse("not a dict")

    def test_parse_invalid_dependencies_raises(self):
        raw = {"metadata": {"name": "wf"}, "dependencies": "not a list"}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_invalid_capabilities_raises(self):
        raw = {"metadata": {"name": "wf"}, "capabilities": "not a list"}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_invalid_permissions_raises(self):
        raw = {"metadata": {"name": "wf"}, "permissions": "not a list"}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_invalid_parameters_raises(self):
        raw = {"metadata": {"name": "wf"}, "parameters": "not a list"}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_invalid_variables_raises(self):
        raw = {"metadata": {"name": "wf"}, "variables": "not a list"}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_invalid_inputs_raises(self):
        raw = {"metadata": {"name": "wf"}, "inputs": "not a list"}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_invalid_outputs_raises(self):
        raw = {"metadata": {"name": "wf"}, "outputs": "not a list"}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_invalid_nodes_raises(self):
        raw = {"metadata": {"name": "wf"}, "nodes": "not a list"}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_invalid_edges_raises(self):
        raw = {"metadata": {"name": "wf"}, "edges": "not a list"}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_dependency_missing_name_raises(self):
        raw = {"metadata": {"name": "wf"}, "dependencies": [{}]}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_parameter_missing_name_raises(self):
        raw = {"metadata": {"name": "wf"}, "parameters": [{}]}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_variable_missing_name_raises(self):
        raw = {"metadata": {"name": "wf"}, "variables": [{}]}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_input_missing_name_raises(self):
        raw = {"metadata": {"name": "wf"}, "inputs": [{}]}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_output_missing_name_raises(self):
        raw = {"metadata": {"name": "wf"}, "outputs": [{}]}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_permission_missing_name_raises(self):
        raw = {"metadata": {"name": "wf"}, "permissions": [{}]}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_capability_missing_name_raises(self):
        raw = {"metadata": {"name": "wf"}, "capabilities": [{}]}
        parser = WorkflowManifestParser()
        with pytest.raises(ManifestError):
            parser.parse(raw)

    def test_parse_metadata_section(self):
        raw = {
            "metadata": {"name": "test", "version": "1.2.3", "description": "desc", "author": "auth", "tags": ["a", "b"]},
        }
        parser = WorkflowManifestParser()
        result = parser.parse(raw)
        assert result.metadata.name == "test"
        assert result.metadata.version == "1.2.3"
        assert result.metadata.description == "desc"
        assert result.metadata.author == "auth"
        assert result.metadata.tags == ["a", "b"]

    def test_parse_empty_lists(self):
        raw = {"metadata": {"name": "empty"}}
        parser = WorkflowManifestParser()
        result = parser.parse(raw)
        assert result.dependencies == []
        assert result.capabilities == []
        assert result.plugins == []
        assert result.permissions == []
        assert result.parameters == []
        assert result.variables == []
        assert result.inputs == []
        assert result.outputs == []
