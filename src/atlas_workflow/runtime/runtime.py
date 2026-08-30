"""Workflow Runtime, Instance, and Context.

Per RFC-0304 (Workflow Runtime) and RFC-0305 (Lifecycle).
"""

from __future__ import annotations
import uuid
from dataclasses import replace
from datetime import datetime, timezone
from typing import Any

from atlas_workflow.common import (
    WorkflowError,
    ManifestError,
    ValidationError,
    WorkflowEvent,
    EventType,
    WorkflowLifecycleState,
    ExecutionState,
    ExecutionMetadata,
    SecurityError,
)
from atlas_workflow.events import EventBus
from atlas_workflow.execution import ExecutionControl, ExecutionEngine, ExecutionToken, ExecutionResult
from atlas_workflow.graph import WorkflowGraph, GraphNode, GraphEdge
from atlas_workflow.health import HealthService
from atlas_workflow.metrics import MetricsCollector
from atlas_workflow.node_registry import NodeRegistry
from atlas_workflow.parser import ParsedWorkflow, WorkflowParser
from atlas_workflow.plugin_integration import PluginBridge
from atlas_workflow.scheduler import ScheduleConfig, SchedulerInterface, InMemoryScheduler, TriggerType
from atlas_workflow.storage import StorageAbstraction
from atlas_workflow.validator import WorkflowValidator
from atlas_workflow.manifest import WorkflowManifest, WorkflowManifestParser


def _default_noop_handler(node_id, configuration, inputs, metadata):
    """Default handler for unknown node types - returns inputs as output."""
    return {"node_id": node_id, "output": "noop_result", **inputs}


class WorkflowContext:
    """Context for a single workflow execution."""

    def __init__(
        self,
        workflow_id: str,
        instance_id: str,
        variables: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self._workflow_id = workflow_id
        self._instance_id = instance_id
        self._variables: dict[str, Any] = variables or {}
        self._metadata: dict[str, Any] = metadata or {}

    @property
    def workflow_id(self) -> str:
        return self._workflow_id

    @property
    def instance_id(self) -> str:
        return self._instance_id

    def get_variable(self, name: str) -> Any:
        return self._variables.get(name)

    def set_variable(self, name: str, value: Any) -> None:
        self._variables[name] = value

    def get_metadata(self, key: str) -> Any:
        return self._metadata.get(key)

    def set_metadata(self, key: str, value: Any) -> None:
        self._metadata[key] = value

    def get_all_variables(self) -> dict[str, Any]:
        return dict(self._variables)

    def get_all_metadata(self) -> dict[str, Any]:
        return dict(self._metadata)


class WorkflowInstance:
    """A single execution instance of a workflow."""

    def __init__(
        self,
        workflow_id: str,
        workflow_name: str,
        version: str,
        graph: WorkflowGraph,
        instance_id: str | None = None,
        inputs: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        breakpoints: set[str] | None = None,
    ) -> None:
        self._instance_id = instance_id or str(uuid.uuid4())
        self._workflow_id = workflow_id
        self._workflow_name = workflow_name
        self._version = version
        self._graph = graph
        self._state = WorkflowLifecycleState.CREATED
        self._inputs = inputs or {}
        self._context = WorkflowContext(
            workflow_id=workflow_id,
            instance_id=self._instance_id,
            variables=dict(inputs) if inputs else {},
            metadata=metadata or {},
        )
        self._created_at = datetime.now(timezone.utc)
        self._started_at: datetime | None = None
        self._completed_at: datetime | None = None
        self._result: ExecutionResult | None = None
        self._token: ExecutionToken | None = None
        self._control = ExecutionControl(breakpoints)

    @property
    def instance_id(self) -> str:
        return self._instance_id

    @property
    def workflow_id(self) -> str:
        return self._workflow_id

    @property
    def workflow_name(self) -> str:
        return self._workflow_name

    @property
    def version(self) -> str:
        return self._version

    @property
    def state(self) -> WorkflowLifecycleState:
        return self._state

    @property
    def graph(self) -> WorkflowGraph:
        return self._graph

    @property
    def context(self) -> WorkflowContext:
        return self._context

    @property
    def result(self) -> ExecutionResult | None:
        return self._result

    @property
    def token(self) -> ExecutionToken | None:
        return self._token

    @property
    def control(self) -> ExecutionControl:
        return self._control

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def started_at(self) -> datetime | None:
        return self._started_at

    @property
    def completed_at(self) -> datetime | None:
        return self._completed_at

    def set_state(self, state: WorkflowLifecycleState) -> None:
        self._state = state

    def with_result(self, result: ExecutionResult) -> None:
        self._result = result
        self._completed_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self._instance_id,
            "workflow_id": self._workflow_id,
            "workflow_name": self._workflow_name,
            "version": self._version,
            "state": self._state.value,
            "inputs": dict(self._inputs),
            "created_at": self._created_at.isoformat(),
            "started_at": self._started_at.isoformat() if self._started_at else None,
            "completed_at": self._completed_at.isoformat() if self._completed_at else None,
            "result": self._result.to_dict() if self._result else None,
        }


class WorkflowRuntime:
    """Main workflow runtime orchestrator."""

    def __init__(
        self,
        event_bus: EventBus | None = None,
        node_registry: NodeRegistry | None = None,
        plugin_bridge: PluginBridge | None = None,
        scheduler: SchedulerInterface | None = None,
        storage: StorageAbstraction | None = None,
        metrics: MetricsCollector | None = None,
        health: HealthService | None = None,
        default_timeout: float = 300.0,
        default_max_retries: int = 0,
    ) -> None:
        self._event_bus = event_bus or EventBus()
        self._node_registry = node_registry or NodeRegistry()
        self._plugin_bridge = plugin_bridge or PluginBridge()
        # Register default noop handler so workflows can execute without explicit plugin setup
        self._plugin_bridge.register_handler("noop", _default_noop_handler)
        self._scheduler = scheduler or InMemoryScheduler()
        self._storage = storage or StorageAbstraction()
        self._metrics = metrics or MetricsCollector()
        self._health = health or HealthService()
        self._parser = WorkflowParser()
        self._validator = WorkflowValidator(self._node_registry)
        self._engine: ExecutionEngine | None = None
        self._instances: dict[str, WorkflowInstance] = {}
        self._default_timeout = default_timeout
        self._default_max_retries = default_max_retries

    def _ensure_engine(self) -> ExecutionEngine:
        if self._engine is None:
            self._engine = ExecutionEngine(
                plugin_bridge=self._plugin_bridge,
                event_publisher=self._event_bus.publish,
                checkpoint_callback=self._on_checkpoint,
                default_timeout=self._default_timeout,
                default_max_retries=self._default_max_retries,
            )
        return self._engine

    def create_manifest(self, raw: dict[str, Any]) -> WorkflowManifest:
        parser = WorkflowManifestParser()
        return parser.parse(raw)

    def validate_manifest(self, manifest: WorkflowManifest) -> list[str]:
        parsed = self._parser.parse(manifest)
        return self._validator.validate(parsed)

    def compile(self, manifest: WorkflowManifest) -> WorkflowGraph:
        parsed = self._parser.parse(manifest)
        self._validator.validate(parsed)

        self._event_bus.publish_event_type(
            EventType.WORKFLOW_VALIDATED,
            workflow_id=parsed.workflow_id,
        )
        self._event_bus.publish_event_type(
            EventType.WORKFLOW_COMPILED,
            workflow_id=parsed.workflow_id,
        )

        nodes = [GraphNode.from_parsed(n) for n in parsed.nodes]
        edges = [GraphEdge.from_parsed(e) for e in parsed.edges]

        graph = WorkflowGraph(
            nodes=nodes,
            edges=edges,
            entry_nodes=list(parsed.entry_nodes),
            exit_nodes=list(parsed.exit_nodes),
            workflow_id=parsed.workflow_id,
            workflow_name=parsed.workflow_name,
            version=parsed.version,
        )

        violations = graph.validate_integrity()
        if violations:
            raise ValidationError(
                f"Graph validation failed: {len(violations)} violation(s)",
                violations=violations,
            )

        return graph

    def create_instance(
        self,
        graph: WorkflowGraph,
        inputs: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        instance_id: str | None = None,
        breakpoints: set[str] | None = None,
    ) -> WorkflowInstance:
        instance = WorkflowInstance(
            workflow_id=graph.workflow_id,
            workflow_name=graph.workflow_name,
            version=graph.version,
            graph=graph,
            inputs=inputs,
            metadata=metadata,
            instance_id=instance_id,
            breakpoints=breakpoints,
        )
        self._instances[instance.instance_id] = instance
        self._event_bus.publish_event_type(
            EventType.WORKFLOW_REGISTERED,
            workflow_id=graph.workflow_id,
        )
        return instance

    def schedule_instance(
        self,
        instance: WorkflowInstance,
        trigger_type: TriggerType = TriggerType.IMMEDIATE,
        config: ScheduleConfig | None = None,
    ) -> Any:
        if config is None:
            config = ScheduleConfig(trigger_type=trigger_type)
        scheduled = self._scheduler.schedule(instance.workflow_id, config)
        instance.set_state(WorkflowLifecycleState.SCHEDULED)
        return scheduled

    def execute(self, instance: WorkflowInstance) -> ExecutionResult:
        self._ensure_engine()
        instance.set_state(WorkflowLifecycleState.RUNNING)
        instance._started_at = datetime.now(timezone.utc)

        token = ExecutionToken(
            token_id=f"token-{instance.instance_id}",
            workflow_instance_id=instance.instance_id,
        )
        instance._token = token

        self._metrics.record_execution_started()

        result = self._engine.execute(
            graph=instance.graph,
            token=token,
            inputs=instance._inputs or {},
            metadata=ExecutionMetadata(
                workflow_id=instance.workflow_id,
                instance_id=instance.instance_id,
            ),
            control=instance.control,
        )

        if instance.control.is_cancelled:
            result = replace(result, state=ExecutionState.CANCELLED, error="Execution cancelled")
            instance.set_state(WorkflowLifecycleState.CANCELLED)
            self._event_bus.publish_workflow_cancelled(
                workflow_id=instance.workflow_id,
                instance_id=instance.instance_id,
            )
        elif result.success:
            instance.set_state(WorkflowLifecycleState.COMPLETED)
            self._metrics.record_execution_completed(result.duration_ms or 0)
            self._event_bus.publish_workflow_completed(
                workflow_id=instance.workflow_id,
                instance_id=instance.instance_id,
            )
        else:
            instance.set_state(WorkflowLifecycleState.FAILED)
            self._metrics.record_execution_failed(result.duration_ms or 0)
            self._event_bus.publish_workflow_failed(
                workflow_id=instance.workflow_id,
                instance_id=instance.instance_id,
                data={"error": result.error},
            )

        instance.with_result(result)
        return result

    def pause(self, instance_id: str) -> bool:
        instance = self._instances.get(instance_id)
        if instance is None or instance.state != WorkflowLifecycleState.RUNNING:
            return False
        instance.set_state(WorkflowLifecycleState.PAUSED)
        instance.control.pause()
        if instance._token:
            instance._token = instance._token.pause()
        self._event_bus.publish_workflow_paused(
            workflow_id=instance.workflow_id,
            instance_id=instance_id,
        )
        self._health.set_state("Paused")
        return True

    def resume(self, instance_id: str) -> bool:
        instance = self._instances.get(instance_id)
        if instance is None or (
            instance.state != WorkflowLifecycleState.PAUSED and not instance.control.is_paused
        ):
            return False
        instance.set_state(WorkflowLifecycleState.RUNNING)
        instance.control.resume()
        if instance._token:
            instance._token = instance._token.resume()
        self._event_bus.publish_workflow_resumed(
            workflow_id=instance.workflow_id,
            instance_id=instance_id,
        )
        self._health.set_state("Healthy")
        return True

    def cancel(self, instance_id: str) -> bool:
        instance = self._instances.get(instance_id)
        if instance is None:
            return False
        if instance._token:
            instance._token = instance._token.cancel()
        instance.control.cancel()
        instance.set_state(WorkflowLifecycleState.CANCELLED)
        self._event_bus.publish_workflow_cancelled(
            workflow_id=instance.workflow_id,
            instance_id=instance_id,
        )
        return True

    def step(self, instance_id: str) -> bool:
        instance = self._instances.get(instance_id)
        if instance is None or (
            instance.state != WorkflowLifecycleState.PAUSED and not instance.control.is_paused
        ):
            return False
        instance.control.step()
        return True

    def dispose(self, instance_id: str) -> bool:
        instance = self._instances.get(instance_id)
        if instance is None:
            return False
        instance.set_state(WorkflowLifecycleState.DISPOSED)
        del self._instances[instance_id]
        return True

    def get_instance(self, instance_id: str) -> WorkflowInstance | None:
        return self._instances.get(instance_id)

    def get_instances(self) -> dict[str, WorkflowInstance]:
        return dict(self._instances)

    def recover(self, instance_id: str) -> bool:
        snapshot = self._storage.load_snapshot(instance_id)
        if snapshot is None:
            return False
        self._event_bus.publish_workflow_recovered(
            workflow_id="", instance_id=instance_id,
        )
        return True

    def _on_checkpoint(self, checkpoint: dict[str, Any]) -> None:
        self._storage.save_snapshot(
            checkpoint.get("instance_id", ""),
            checkpoint,
        )

    @property
    def event_bus(self) -> EventBus:
        return self._event_bus

    @property
    def node_registry(self) -> NodeRegistry:
        return self._node_registry

    @property
    def plugin_bridge(self) -> PluginBridge:
        return self._plugin_bridge

    @property
    def scheduler(self) -> SchedulerInterface:
        return self._scheduler

    @property
    def storage(self) -> StorageAbstraction:
        return self._storage

    @property
    def metrics(self) -> MetricsCollector:
        return self._metrics

    @property
    def health(self) -> HealthService:
        return self._health
