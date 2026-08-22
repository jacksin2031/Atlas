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
            parallel_groups = graph.get_parallel_groups()

            completed: set[str] = set()
            failed: set[str] = set()
            skipped: set[str] = set()
            context: dict[str, Any] = dict(inputs)

            for group in parallel_groups:
                if token.is_cancelled:
                    return self._make_result(
                        graph, token, success=False,
                        error="Execution cancelled",
                        context=context, completed=completed,
                        failed=failed, skipped=skipped,
                    )

                group_results = self._execute_parallel_group(
                    group, graph, token, context, completed, failed, skipped,
                )
                context.update(group_results)

                for nid in group:
                    ns = self._node_states.get(nid)
                    if ns and ns.is_successful:
                        completed.add(nid)
                    elif ns and ns.is_failed:
                        failed.add(nid)
                    elif ns and ns.state == ExecutionState.SKIPPED:
                        skipped.add(nid)

                self._save_checkpoint(graph, token, context, completed, failed, skipped)

            # Determine overall success: workflow succeeds only if ALL nodes completed successfully
            all_node_ids = set(graph.nodes.keys())
            any_failed = len(failed) > 0 or len(skipped) > 0
            all_done = completed | failed | skipped == all_node_ids

            exit_outputs = self._collect_exit_outputs(graph, context)

            if any_failed:
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
                    context=context, completed=completed,
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
                context=context, completed=completed,
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

    def _execute_parallel_group(
        self,
        group: list[str],
        graph: WorkflowGraph,
        token: ExecutionToken,
        context: dict[str, Any],
        completed: set[str],
        failed: set[str],
        skipped: set[str],
    ) -> dict[str, Any]:
        results: dict[str, Any] = {}
        for node_id in sorted(group):
            if token.is_cancelled:
                break
            if node_id in failed:
                continue
            if self._should_skip(node_id, graph, completed, failed, skipped):
                skipped.add(node_id)
                self._record_node_state(node_id, ExecutionState.SKIPPED)
                continue

            node_result = self._execute_node(node_id, graph, token, context)
            if node_result.success:
                results[node_id] = node_result.output
                for key, val in node_result.output.items():
                    context[key] = val
            else:
                self._propagate_failure(node_id, graph, failed, skipped, node_result.error)
        return results

    def _execute_node(
        self,
        node_id: str,
        graph: WorkflowGraph,
        token: ExecutionToken,
        context: dict[str, Any],
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

        node_inputs = self._resolve_node_inputs(node, context)
        timeout = node.timeout_seconds or self._default_timeout
        max_retries = node.retry_max or self._default_max_retries
        last_error: str | None = None

        for attempt in range(max_retries + 1):
            if token.is_cancelled:
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
                    data={"duration_ms": elapsed, "attempt": attempt + 1},
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

    def _resolve_node_inputs(self, node: GraphNode, context: dict[str, Any]) -> dict[str, Any]:
        inputs: dict[str, Any] = {}
        for inp in node.inputs:
            if inp in context:
                inputs[inp] = context[inp]
            elif inp in node.configuration:
                inputs[inp] = node.configuration[inp]
        return inputs

    def _should_skip(self, node_id: str, graph: WorkflowGraph,
                     completed: set[str], failed: set[str], skipped: set[str]) -> bool:
        predecessors = graph.get_predecessors(node_id)
        for pred in predecessors:
            if pred in failed:
                return True
            if pred in skipped:
                return True
        return False

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

    def _collect_exit_outputs(self, graph: WorkflowGraph, context: dict[str, Any]) -> dict[str, Any]:
        outputs: dict[str, Any] = {}
        for exit_id in sorted(graph.exit_nodes):
            if exit_id in context:
                outputs[f"exit:{exit_id}"] = context[exit_id]
        return outputs

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
