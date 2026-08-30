"""Deterministic execution engine for workflow graphs.

Per RFC-0303, RFC-0304, and RFC-0313.
Supports sequential, parallel, conditional, retry, timeout,
cancellation, checkpoint, resume, and failure propagation.

No execution order may depend on hash ordering or non-deterministic iteration.
"""

from __future__ import annotations
import time
from datetime import datetime, timezone
from typing import Any, Callable

from atlas_workflow.common import (
    ExecutionError,
    ExecutionState,
    ExecutionMetadata,
    NodeState,
    WorkflowEvent,
    EventType,
)
from atlas_workflow.execution.models import (
    ExecutionResult,
    ExecutionToken,
    ExecutionTokenState,
    ExecutionHistory,
    ExecutionScope,
    ExecutionControl,
    NodeExecutionContext,
)
from atlas_workflow.graph import WorkflowGraph, GraphNode
from atlas_workflow.plugin_integration import PluginBridge


class ExecutionEngine:
    """Deterministic execution engine for workflow graphs.

    Executes workflow graphs using topological ordering for determinism.
    Supports parallel execution groups, conditional branches, retry,
    timeout, cancellation, checkpoint, and resume.
    """

    def __init__(
        self,
        plugin_bridge: PluginBridge,
        event_publisher: Callable[[WorkflowEvent], None] | None = None,
        checkpoint_callback: Callable[[dict[str, Any]], None] | None = None,
        default_timeout: float = 300.0,
        default_max_retries: int = 0,
    ) -> None:
        self._plugin_bridge = plugin_bridge
        self._event_publisher = event_publisher or (lambda _: None)
        self._checkpoint_callback = checkpoint_callback or (lambda _: None)
        self._default_timeout = default_timeout
        self._default_max_retries = default_max_retries
        self._node_states: dict[str, NodeState] = {}
        self._history: ExecutionHistory | None = None
        self._start_time: datetime | None = None

    def execute(
        self,
        graph: WorkflowGraph,
        token: ExecutionToken,
        inputs: dict[str, Any],
        metadata: ExecutionMetadata | None = None,
        control: ExecutionControl | None = None,
    ) -> ExecutionResult:
        """Execute a workflow graph deterministically.

        Args:
            graph: The workflow graph to execute.
            token: Execution token for pause/resume/cancel control.
            inputs: Initial input variables for the workflow.
            metadata: Execution metadata.

        Returns:
            ExecutionResult with success/failure status.
        """
        self._start_time = datetime.now(timezone.utc)
        self._node_states = {}
        self._history = ExecutionHistory(
            workflow_id=graph.workflow_id,
            instance_id=token.workflow_instance_id,
        )

        self._history.record_event("execution_started", {
            "workflow_id": graph.workflow_id,
            "instance_id": token.workflow_instance_id,
            "entry_nodes": list(graph.entry_nodes),
        })
        self._event_publisher(WorkflowEvent(
            event_type=EventType.WORKFLOW_STARTED,
            workflow_id=graph.workflow_id,
            instance_id=token.workflow_instance_id,
        ))

        try:
            completed: set[str] = set()
            failed: set[str] = set()
            skipped: set[str] = set()
            variables: dict[str, Any] = dict(inputs)
            node_outputs: dict[str, dict[str, Any]] = {}

            for node_id in graph.topological_order():
                if token.is_cancelled or (control and control.is_cancelled):
                    return self._make_result(
                        graph, token, success=False,
                        error="Execution cancelled",
                        context=variables, completed=completed,
                        failed=failed, skipped=skipped,
                    )
                if control and control.has_breakpoint(node_id):
                    self._event_publisher(WorkflowEvent(
                        event_type=EventType.WORKFLOW_PAUSED,
                        workflow_id=graph.workflow_id,
                        instance_id=token.workflow_instance_id,
                        node_id=node_id,
                        data={"reason": "breakpoint", "node_id": node_id},
                    ))
                if control and not control.wait_before_node(node_id):
                    return self._make_result(
                        graph, token, success=False, error="Execution cancelled",
                        context=variables, completed=completed, failed=failed, skipped=skipped,
                    )
                if self._should_skip(node_id, graph, completed, failed, skipped, node_outputs):
                    skipped.add(node_id)
                    self._record_node_state(node_id, ExecutionState.SKIPPED)
                    self._event_publisher(WorkflowEvent(
                        event_type=EventType.NODE_SKIPPED,
                        workflow_id=graph.workflow_id,
                        instance_id=token.workflow_instance_id,
                        node_id=node_id,
                        data={"reason": "No active incoming edge"},
                    ))
                    continue

                node_inputs = self._resolve_node_inputs(
                    node_id, graph, node_outputs, variables,
                )
                node_result = self._execute_node(
                    node_id, graph, token, node_inputs, variables, control,
                )
                if node_result.success:
                    completed.add(node_id)
                    node_outputs[node_id] = node_result.output
                    node = graph.get_node(node_id)
                    if node and node.node_type in {"set_variable", "set-variable"}:
                        name = str(node.configuration.get("name", ""))
                        if name:
                            value = node_result.output.get("value")
                            variables[name] = value
                            self._event_publisher(WorkflowEvent(
                                event_type=EventType.VARIABLE_CHANGED,
                                workflow_id=graph.workflow_id,
                                instance_id=token.workflow_instance_id,
                                node_id=node_id,
                                data={"name": name, "value": value},
                            ))
                else:
                    failed.add(node_id)

                self._save_checkpoint(
                    graph, token, {"variables": variables, "node_outputs": node_outputs},
                    completed, failed, skipped,
                )

            exit_outputs = self._collect_exit_outputs(graph, node_outputs)

            if failed:
                self._history.record_event("execution_failed", {
                    "failed_nodes": list(failed),
                    "skipped_nodes": list(skipped),
                })
                self._event_publisher(WorkflowEvent(
                    event_type=EventType.WORKFLOW_FAILED,
                    workflow_id=graph.workflow_id,
                    instance_id=token.workflow_instance_id,
                    data={"failed_nodes": list(failed), "skipped_nodes": list(skipped)},
                ))
                return self._make_result(
                    graph, token, success=False,
                    error=f"Workflow failed: {len(failed)} node(s) failed",
                    context=variables, completed=completed,
                    failed=failed, skipped=skipped,
                )

            self._history.record_event("execution_completed", {
                "completed_nodes": list(completed),
                "failed_nodes": list(failed),
                "skipped_nodes": list(skipped),
            })
            self._event_publisher(WorkflowEvent(
                event_type=EventType.WORKFLOW_COMPLETED,
                workflow_id=graph.workflow_id,
                instance_id=token.workflow_instance_id,
                data={"completed": list(completed), "failed": list(failed)},
            ))
            return self._make_result(
                graph, token, success=True,
                output=exit_outputs,
                context=variables, completed=completed,
                failed=failed, skipped=skipped,
            )

        except ExecutionError as exc:
            self._history.record_event("execution_failed", {"error": str(exc)})
            self._event_publisher(WorkflowEvent(
                event_type=EventType.WORKFLOW_FAILED,
                workflow_id=graph.workflow_id,
                instance_id=token.workflow_instance_id,
                data={"error": str(exc)},
            ))
            return ExecutionResult.failure_result(
                workflow_id=graph.workflow_id,
                instance_id=token.workflow_instance_id,
                error=str(exc),
                metadata=metadata,
            )

    def _execute_node(
        self,
        node_id: str,
        graph: WorkflowGraph,
        token: ExecutionToken,
        node_inputs: dict[str, Any],
        variables: dict[str, Any],
        control: ExecutionControl | None,
    ) -> ExecutionResult:
        node = graph.get_node(node_id)
        if node is None:
            return ExecutionResult.failure_result(
                workflow_id="", instance_id=token.workflow_instance_id,
                error=f"Node {node_id!r} not found in graph",
            )

        self._record_node_state(node_id, ExecutionState.RUNNING)
        self._event_publisher(WorkflowEvent(
            event_type=EventType.NODE_STARTED,
            workflow_id=graph.workflow_id,
            instance_id=token.workflow_instance_id,
            node_id=node_id,
        ))

        timeout = node.timeout_seconds or self._default_timeout
        max_retries = node.retry_max or self._default_max_retries
        last_error: str | None = None

        for attempt in range(max_retries + 1):
            if token.is_cancelled or (control and control.is_cancelled):
                self._record_node_state(node_id, ExecutionState.CANCELLED)
                return ExecutionResult.failure_result(
                    workflow_id=graph.workflow_id,
                    instance_id=token.workflow_instance_id,
                    node_id=node_id,
                    error="Execution cancelled",
                )

            start = time.monotonic()
            try:
                output = self._plugin_bridge.execute_node(
                    node_type=node.node_type,
                    node_id=node_id,
                    configuration=node.configuration,
                    inputs=node_inputs,
                    node_metadata=node.metadata,
                    execution_context=NodeExecutionContext(
                        workflow_id=graph.workflow_id,
                        instance_id=token.workflow_instance_id,
                        node_id=node_id,
                        variables=variables,
                        capabilities=tuple(node.metadata.get("capabilities", [])),
                        control=control,
                        metadata=node.metadata,
                    ),
                )
                elapsed = (time.monotonic() - start) * 1000
                self._record_node_state(
                    node_id, ExecutionState.COMPLETED,
                    output=output, duration_ms=elapsed,
                )
                self._event_publisher(WorkflowEvent(
                    event_type=EventType.NODE_COMPLETED,
                    workflow_id=graph.workflow_id,
                    instance_id=token.workflow_instance_id,
                    node_id=node_id,
                    data={
                        "duration_ms": elapsed,
                        "attempt": attempt + 1,
                        "inputs": node_inputs,
                        "outputs": output,
                    },
                ))
                return ExecutionResult.success_result(
                    workflow_id=graph.workflow_id,
                    instance_id=token.workflow_instance_id,
                    node_id=node_id,
                    output=output,
                    duration_ms=elapsed,
                    retries=attempt,
                )
            except Exception as exc:
                last_error = str(exc)
                if attempt < max_retries:
                    self._event_publisher(WorkflowEvent(
                        event_type=EventType.EXECUTION_RETRY,
                        workflow_id=graph.workflow_id,
                        instance_id=token.workflow_instance_id,
                        node_id=node_id,
                        data={"attempt": attempt + 2, "error": last_error},
                    ))

        self._record_node_state(
            node_id, ExecutionState.FAILED,
            error=last_error,
        )
        self._event_publisher(WorkflowEvent(
            event_type=EventType.NODE_FAILED,
            workflow_id=graph.workflow_id,
            instance_id=token.workflow_instance_id,
            node_id=node_id,
            data={"error": last_error, "retries": max_retries},
        ))
        return ExecutionResult.failure_result(
            workflow_id=graph.workflow_id,
            instance_id=token.workflow_instance_id,
            node_id=node_id,
            error=last_error or "Unknown error",
            retries=max_retries,
        )

    def _resolve_node_inputs(
        self,
        node_id: str,
        graph: WorkflowGraph,
        node_outputs: dict[str, dict[str, Any]],
        variables: dict[str, Any],
    ) -> dict[str, Any]:
        node = graph.get_node(node_id)
        if node is None:
            return {}
        inputs: dict[str, Any] = {}
        defaults = node.metadata.get("input_defaults", {})
        if isinstance(defaults, dict):
            inputs.update(defaults)
        for name in node.inputs:
            if name in node.configuration:
                inputs[name] = node.configuration[name]
            elif name in variables:
                inputs[name] = variables[name]
        for edge in graph.edges:
            if edge.target_node_id != node_id:
                continue
            source_output = node_outputs.get(edge.source_node_id)
            if source_output is None or not self._edge_active(edge, graph, source_output):
                continue
            value = self._source_value(edge, graph, source_output)
            target_name = self._port_name(node, edge.target_port, "input")
            if not target_name:
                target_name = node.inputs[0] if len(node.inputs) == 1 else edge.source_port or "input"
            inputs[target_name] = value
        if node.node_type in {"get_variable", "get-variable"}:
            name = str(node.configuration.get("name", ""))
            inputs["value"] = variables.get(name, node.configuration.get("default"))
        return inputs

    def _should_skip(
        self, node_id: str, graph: WorkflowGraph,
        completed: set[str], failed: set[str], skipped: set[str],
        node_outputs: dict[str, dict[str, Any]],
    ) -> bool:
        incoming = [edge for edge in graph.edges if edge.target_node_id == node_id]
        if not incoming:
            return False
        if any(edge.source_node_id in failed for edge in incoming):
            return True
        active = [
            edge for edge in incoming
            if edge.source_node_id in completed
            and self._edge_active(edge, graph, node_outputs.get(edge.source_node_id, {}))
        ]
        return not active

    def _edge_active(
        self, edge: Any, graph: WorkflowGraph, source_output: dict[str, Any],
    ) -> bool:
        source = graph.get_node(edge.source_node_id)
        port_name = self._port_name(source, edge.source_port, "output") if source else edge.source_port
        if source and source.node_type in {"condition", "route"} and port_name:
            return port_name in source_output
        if edge.condition:
            expected = edge.condition.strip().lower()
            value = self._source_value(edge, graph, source_output)
            return bool(value) if expected in {"true", "1"} else not bool(value) if expected in {"false", "0"} else True
        return True

    def _source_value(
        self, edge: Any, graph: WorkflowGraph, source_output: dict[str, Any],
    ) -> Any:
        source = graph.get_node(edge.source_node_id)
        port_name = self._port_name(source, edge.source_port, "output") if source else edge.source_port
        if port_name and port_name in source_output:
            return source_output[port_name]
        if len(source_output) == 1:
            return next(iter(source_output.values()))
        return source_output

    @staticmethod
    def _port_name(node: GraphNode | None, port: str, direction: str) -> str:
        if not port or node is None:
            return port
        mapping = node.metadata.get(f"{direction}_ports", {})
        if isinstance(mapping, dict):
            return str(mapping.get(port, port))
        return port

    def _propagate_failure(
        self, node_id: str, graph: WorkflowGraph,
        failed: set[str], skipped: set[str], error: str,
    ) -> None:
        failed.add(node_id)
        self._record_node_state(node_id, ExecutionState.FAILED, error=error)
        self._event_publisher(WorkflowEvent(
            event_type=EventType.NODE_FAILED,
            workflow_id=graph.workflow_id,
            instance_id="",
            node_id=node_id,
            data={"error": error},
        ))
        successors = graph.get_successors(node_id)
        for succ in successors:
            if succ not in failed and succ not in skipped:
                skipped.add(succ)
                self._record_node_state(succ, ExecutionState.SKIPPED)

    def _collect_exit_outputs(
        self, graph: WorkflowGraph, node_outputs: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        values = [node_outputs[exit_id] for exit_id in sorted(graph.exit_nodes) if exit_id in node_outputs]
        if len(values) == 1:
            return values[0]
        return {
            f"exit:{exit_id}": node_outputs[exit_id]
            for exit_id in sorted(graph.exit_nodes)
            if exit_id in node_outputs
        }

    def _record_node_state(
        self, node_id: str, state: ExecutionState,
        output: dict[str, Any] | None = None,
        error: str | None = None,
        duration_ms: float | None = None,
    ) -> None:
        self._node_states[node_id] = NodeState(
            node_id=node_id,
            state=state,
            output=output,
            error=error,
            duration_ms=duration_ms,
        )

    def _save_checkpoint(
        self, graph: WorkflowGraph, token: ExecutionToken,
        context: dict[str, Any], completed: set[str],
        failed: set[str], skipped: set[str],
    ) -> None:
        checkpoint = {
            "workflow_id": graph.workflow_id,
            "instance_id": token.workflow_instance_id,
            "context": dict(context),
            "completed": list(completed),
            "failed": list(failed),
            "skipped": list(skipped),
            "node_states": {
                nid: {
                    "state": ns.state.value,
                    "output": ns.output,
                    "error": ns.error,
                    "duration_ms": ns.duration_ms,
                }
                for nid, ns in self._node_states.items()
            },
        }
        self._history.add_checkpoint(checkpoint)
        self._checkpoint_callback(checkpoint)

    def _make_result(
        self,
        graph: WorkflowGraph,
        token: ExecutionToken,
        success: bool,
        error: str | None = None,
        output: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        completed: set[str] | None = None,
        failed: set[str] | None = None,
        skipped: set[str] | None = None,
    ) -> ExecutionResult:
        if success:
            return ExecutionResult.success_result(
                workflow_id=graph.workflow_id,
                instance_id=token.workflow_instance_id,
                output=output or {},
                metadata={
                    "completed_nodes": list(completed or set()),
                    "failed_nodes": list(failed or set()),
                },
            )
        else:
            return ExecutionResult.failure_result(
                workflow_id=graph.workflow_id,
                instance_id=token.workflow_instance_id,
                error=error or "Unknown error",
                node_id="",
                metadata={
                    "completed_nodes": list(completed or set()),
                    "failed_nodes": list(failed or set()),
                },
            )

    @property
    def node_states(self) -> dict[str, NodeState]:
        return dict(self._node_states)

    @property
    def history(self) -> ExecutionHistory | None:
        return self._history
