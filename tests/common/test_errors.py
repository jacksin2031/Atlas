"""Tests for common error types."""

from __future__ import annotations
import pytest

from atlas_workflow.common.errors import (
    WorkflowError,
    ManifestError,
    ParserError,
    ValidationError,
    GraphError,
    ExecutionError,
    SchedulerError,
    StorageError,
    HealthError,
    PluginError,
    SecurityError,
    MetricsError,
)


class TestWorkflowError:
    def test_base_error_message(self):
        err = WorkflowError("test error")
        assert str(err) == "test error"
        assert err.message == "test error"
        assert err.details == {}

    def test_base_error_with_details(self):
        err = WorkflowError("test error", details={"key": "value"})
        assert err.details == {"key": "value"}


class TestManifestError:
    def test_manifest_error_field(self):
        err = ManifestError("invalid field", field="name")
        assert err.field == "name"
        assert err.details["field"] == "name"


class TestParserError:
    def test_parser_error_line(self):
        err = ParserError("parse failed", line=42)
        assert err.line == 42
        assert err.details["line"] == 42


class TestValidationError:
    def test_validation_error_violations(self):
        violations = ["violation1", "violation2"]
        err = ValidationError("validation failed", violations=violations)
        assert err.violations == violations
        assert "violations" in err.details


class TestGraphError:
    def test_graph_error_cycle_nodes(self):
        nodes = ["a", "b", "c"]
        err = GraphError("cycle detected", cycle_nodes=nodes)
        assert err.cycle_nodes == nodes
        assert "cycle_nodes" in err.details


class TestExecutionError:
    def test_execution_error_node_id(self):
        err = ExecutionError("node failed", node_id="node-1")
        assert err.node_id == "node-1"

    def test_execution_error_with_causing_exception(self):
        try:
            raise ValueError("root cause")
        except ValueError as root:
            err = ExecutionError("wrapped", node_id="n1", error=root)
            assert err.node_id == "n1"
            assert err.causing_error is root
            assert "error_type" in err.details
            assert err.details["error_type"] == "ValueError"


class TestSchedulerError:
    def test_scheduler_error_trigger_type(self):
        err = SchedulerError("schedule failed", trigger_type="cron")
        assert err.trigger_type == "cron"


class TestStorageError:
    def test_storage_error_operation(self):
        err = StorageError("save failed", operation="save")
        assert err.operation == "save"


class TestHealthError:
    def test_health_error_component(self):
        err = HealthError("check failed", component="executor")
        assert err.component == "executor"


class TestPluginError:
    def test_plugin_error_plugin_name(self):
        err = PluginError("load failed", plugin_name="my-plugin")
        assert err.plugin_name == "my-plugin"


class TestSecurityError:
    def test_security_error_permission(self):
        err = SecurityError("denied", permission="execute")
        assert err.permission == "execute"


class TestMetricsError:
    def test_metrics_error_metric_name(self):
        err = MetricsError("collection failed", metric_name="duration")
        assert err.metric_name == "duration"
