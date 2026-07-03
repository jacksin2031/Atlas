"""Common error types for Atlas Workflow."""

from __future__ import annotations
import traceback
from typing import Any


class WorkflowError(Exception):
    """Base exception for all workflow errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ManifestError(WorkflowError):
    """Raised when a workflow manifest is invalid."""

    def __init__(self, message: str, field: str | None = None, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, details or {})
        self.field = field
        if field:
            self.details["field"] = field


class ParserError(WorkflowError):
    """Raised when a workflow definition cannot be parsed."""

    def __init__(self, message: str, line: int | None = None, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, details or {})
        self.line = line
        if line is not None:
            self.details["line"] = line


class ValidationError(WorkflowError):
    """Raised when workflow validation fails."""

    def __init__(self, message: str, violations: list[str] | None = None, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, details or {})
        self.violations = violations or []
        self.details["violations"] = self.violations


class GraphError(WorkflowError):
    """Raised when a workflow graph is invalid."""

    def __init__(self, message: str, cycle_nodes: list[str] | None = None, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, details or {})
        self.cycle_nodes = cycle_nodes or []
        if cycle_nodes:
            self.details["cycle_nodes"] = cycle_nodes


class ExecutionError(WorkflowError):
    """Raised when workflow execution fails."""

    def __init__(self, message: str, node_id: str | None = None, error: Exception | None = None, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, details or {})
        self.node_id = node_id
        self.causing_error = error
        if node_id:
            self.details["node_id"] = node_id
        if error:
            self.details["error_type"] = type(error).__name__
            self.details["error_message"] = str(error)
            self.details["error_traceback"] = traceback.format_exception(type(error), error, error.__traceback__)


class SchedulerError(WorkflowError):
    """Raised when scheduling fails."""

    def __init__(self, message: str, trigger_type: str | None = None, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, details or {})
        self.trigger_type = trigger_type
        if trigger_type:
            self.details["trigger_type"] = trigger_type


class StorageError(WorkflowError):
    """Raised when storage operations fail."""

    def __init__(self, message: str, operation: str | None = None, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, details or {})
        self.operation = operation
        if operation:
            self.details["operation"] = operation


class HealthError(WorkflowError):
    """Raised when health checks fail."""

    def __init__(self, message: str, component: str | None = None, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, details or {})
        self.component = component
        if component:
            self.details["component"] = component


class PluginError(WorkflowError):
    """Raised when plugin operations fail."""

    def __init__(self, message: str, plugin_name: str | None = None, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, details or {})
        self.plugin_name = plugin_name
        if plugin_name:
            self.details["plugin_name"] = plugin_name


class SecurityError(WorkflowError):
    """Raised when security checks fail."""

    def __init__(self, message: str, permission: str | None = None, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, details or {})
        self.permission = permission
        if permission:
            self.details["permission"] = permission


class MetricsError(WorkflowError):
    """Raised when metrics operations fail."""

    def __init__(self, message: str, metric_name: str | None = None, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, details or {})
        self.metric_name = metric_name
        if metric_name:
            self.details["metric_name"] = metric_name
