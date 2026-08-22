"""Tests for workflow validator."""

from __future__ import annotations
import pytest

from atlas_workflow.common import ValidationError
from atlas_workflow.parser import ParsedWorkflow, ParsedNode, ParsedEdge
from atlas_workflow.validator import WorkflowValidator


def _make_parsed(**overrides):
    defaults = {
        "workflow_id": "wf-1",
        "workflow_name": "Test Workflow",
        "version": "1.0.0",
        "nodes": (ParsedNode(node_id="start", node_type="noop", ports_out=["out1"]),
                  ParsedNode(node_id="end", node_type="noop", ports_in=["in1"])),
        "edges": (ParsedEdge(source_node_id="start", target_node_id="end"),),
        "entry_nodes": ("start",),
        "exit_nodes": ("end",),
        "parameters": (),
        "variables": (),
        "inputs": (),
        "outputs": (),
        "capabilities": (),
        "dependencies": (),
        "plugins": (),
        "permissions": (),
    }
    defaults.update(overrides)
    return ParsedWorkflow(**defaults)


class TestWorkflowValidator:
    def test_valid_workflow_passes(self):
        validator = WorkflowValidator()
        parsed = _make_parsed()
        violations = validator.validate(parsed)
        assert violations == []

    def test_missing_workflow_id_raises(self):
        validator = WorkflowValidator()
        parsed = _make_parsed(workflow_id="")
        with pytest.raises(ValidationError, match="Workflow ID is required"):
            validator.validate(parsed)

    def test_missing_workflow_name_raises(self):
        validator = WorkflowValidator()
        parsed = _make_parsed(workflow_name="")
        with pytest.raises(ValidationError, match="Workflow name is required"):
            validator.validate(parsed)

    def test_missing_version_raises(self):
        validator = WorkflowValidator()
        parsed = _make_parsed(version="")
        with pytest.raises(ValidationError, match="Version is required"):
            validator.validate(parsed)

    def test_missing_entry_node_raises(self):
        validator = WorkflowValidator()
        parsed = _make_parsed(entry_nodes=())
        with pytest.raises(ValidationError, match="at least one entry node"):
            validator.validate(parsed)

    def test_missing_exit_node_raises(self):
        validator = WorkflowValidator()
        parsed = _make_parsed(exit_nodes=())
        with pytest.raises(ValidationError, match="at least one exit node"):
            validator.validate(parsed)

    def test_missing_entry_node_id_raises(self):
        validator = WorkflowValidator()
        parsed = _make_parsed(entry_nodes=("nonexistent",))
        with pytest.raises(ValidationError, match="does not exist"):
            validator.validate(parsed)

    def test_missing_exit_node_id_raises(self):
        validator = WorkflowValidator()
        parsed = _make_parsed(exit_nodes=("nonexistent",))
        with pytest.raises(ValidationError, match="does not exist"):
            validator.validate(parsed)

    def test_missing_edge_source_raises(self):
        validator = WorkflowValidator()
        parsed = _make_parsed(edges=(ParsedEdge(source_node_id="missing", target_node_id="end"),))
        with pytest.raises(ValidationError):
            validator.validate(parsed)

    def test_missing_edge_target_raises(self):
        validator = WorkflowValidator()
        parsed = _make_parsed(edges=(ParsedEdge(source_node_id="start", target_node_id="missing"),))
        with pytest.raises(ValidationError):
            validator.validate(parsed)

    def test_duplicate_parameter_raises(self):
        from atlas_workflow.common import ManifestParameter
        validator = WorkflowValidator()
        parsed = _make_parsed(parameters=(
            ManifestParameter(name="dup"),
            ManifestParameter(name="dup"),
        ))
        with pytest.raises(ValidationError, match="Duplicate parameter"):
            validator.validate(parsed)

    def test_duplicate_variable_raises(self):
        from atlas_workflow.common import ManifestVariable
        validator = WorkflowValidator()
        parsed = _make_parsed(variables=(
            ManifestVariable(name="dup"),
            ManifestVariable(name="dup"),
        ))
        with pytest.raises(ValidationError, match="Duplicate variable"):
            validator.validate(parsed)

    def test_invalid_version_format_raises(self):
        validator = WorkflowValidator()
        parsed = _make_parsed(version="abc")
        with pytest.raises(ValidationError, match="Invalid version"):
            validator.validate(parsed)

    def test_validate_graph(self, sample_graph):
        validator = WorkflowValidator()
        violations = validator.validate_graph(sample_graph)
        assert violations == []

    def test_validate_invalid_graph(self, cyclic_graph):
        validator = WorkflowValidator()
        violations = validator.validate_graph(cyclic_graph)
        assert len(violations) > 0
        assert any("Cycle" in v for v in violations)
