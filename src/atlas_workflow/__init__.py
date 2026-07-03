"""Atlas Workflow Runtime — Reference Implementation.

This is the Python reference implementation of the Atlas Workflow Runtime.
The architecture is platform-independent; the production implementation
targets Rust.

This reference implementation validates the specification, provides a
testable baseline, and enables rapid iteration on the workflow runtime design.
"""

from __future__ import annotations

__version__ = "1.0.0"
__all__ = [
    "WorkflowRuntime",
    "WorkflowInstance",
    "WorkflowContext",
    "ExecutionContext",
    "ExecutionScope",
    "ExecutionState",
    "ExecutionResult",
    "ExecutionToken",
    "ExecutionHistory",
    "NodeRegistry",
    "WorkflowGraph",
    "WorkflowParser",
    "WorkflowValidator",
    "WorkflowManifest",
    "EventBus",
    "StorageAbstraction",
    "MetricsCollector",
    "HealthService",
    "PluginBridge",
]
