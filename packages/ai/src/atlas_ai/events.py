# Atlas AI Runtime Events

"""
Immutable event types for the AI Runtime.

Events are frozen dataclasses representing state changes
in model management, inference, prompts, conversations,
memory, embeddings, agents, tools, and health.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class EventType(Enum):
    """Event type enumeration."""

    MODEL_LOADED = "model_loaded"
    MODEL_UNLOADED = "model_unloaded"
    MODEL_SNAPSHOT_CREATED = "model_snapshot_created"
    INFERENCE_STARTED = "inference_started"
    INFERENCE_COMPLETED = "inference_completed"
    INFERENCE_FAILED = "inference_failed"
    PROMPT_EXECUTED = "prompt_executed"
    PROMPT_COMPILE_FAILED = "prompt_compile_failed"
    CONVERSATION_CREATED = "conversation_created"
    CONVERSATION_CLOSED = "conversation_closed"
    MEMORY_STORED = "memory_stored"
    MEMORY_REMOVED = "memory_removed"
    EMBEDDING_GENERATED = "embedding_generated"
    EMBEDDING_INDEX_UPDATED = "embedding_index_updated"
    AGENT_STARTED = "agent_started"
    AGENT_STOPPED = "agent_stopped"
    AGENT_EXECUTED = "agent_executed"
    TOOL_INVOKED = "tool_invoked"
    TOOL_FAILED = "tool_failed"
    HEALTH_CHANGED = "health_changed"
    PROVIDER_LOADED = "provider_loaded"
    PROVIDER_UNLOADED = "provider_unloaded"
    PROVIDER_HEALTH_CHANGED = "provider_health_changed"
    CAPABILITY_DISCOVERED = "capability_discovered"
    INFERENCE_SCHEDULED = "inference_scheduled"
    INFERENCE_CANCELLED = "inference_cancelled"


@dataclass(frozen=True, slots=True, eq=True)
class Event:
    """Base immutable event."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = EventType.MODEL_LOADED
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    source: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True, eq=True)
class ModelLoaded(Event):
    """Emitted when a model is loaded."""

    event_type: EventType = field(default=EventType.MODEL_LOADED, init=False)
    model_id: str = ""
    provider_id: str = ""
    version: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class ModelUnloaded(Event):
    """Emitted when a model is unloaded."""

    event_type: EventType = field(default=EventType.MODEL_UNLOADED, init=False)
    model_id: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class ModelSnapshotCreated(Event):
    """Emitted when a model snapshot is created."""

    event_type: EventType = field(default=EventType.MODEL_SNAPSHOT_CREATED, init=False)
    model_id: str = ""
    snapshot_id: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class InferenceStarted(Event):
    """Emitted when inference begins."""

    event_type: EventType = field(default=EventType.INFERENCE_STARTED, init=False)
    job_id: str = ""
    model_id: str = ""
    prompt_id: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class InferenceCompleted(Event):
    """Emitted when inference completes."""

    event_type: EventType = field(default=EventType.INFERENCE_COMPLETED, init=False)
    job_id: str = ""
    model_id: str = ""
    duration_ms: float = 0.0
    tokens_generated: int = 0


@dataclass(frozen=True, slots=True, eq=True)
class InferenceFailed(Event):
    """Emitted when inference fails."""

    event_type: EventType = field(default=EventType.INFERENCE_FAILED, init=False)
    job_id: str = ""
    model_id: str = ""
    error_code: str = ""
    error_message: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class InferenceScheduled(Event):
    """Emitted when inference is scheduled."""

    event_type: EventType = field(default=EventType.INFERENCE_SCHEDULED, init=False)
    job_id: str = ""
    model_id: str = ""
    priority: int = 0


@dataclass(frozen=True, slots=True, eq=True)
class InferenceCancelled(Event):
    """Emitted when inference is cancelled."""

    event_type: EventType = field(default=EventType.INFERENCE_CANCELLED, init=False)
    job_id: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class PromptExecuted(Event):
    """Emitted when a prompt is executed."""

    event_type: EventType = field(default=EventType.PROMPT_EXECUTED, init=False)
    prompt_id: str = ""
    conversation_id: str = ""
    duration_ms: float = 0.0


@dataclass(frozen=True, slots=True, eq=True)
class PromptCompileFailed(Event):
    """Emitted when prompt compilation fails."""

    event_type: EventType = field(default=EventType.PROMPT_COMPILE_FAILED, init=False)
    prompt_id: str = ""
    error_code: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class ConversationCreated(Event):
    """Emitted when a conversation is created."""

    event_type: EventType = field(default=EventType.CONVERSATION_CREATED, init=False)
    conversation_id: str = ""
    session_id: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class ConversationClosed(Event):
    """Emitted when a conversation is closed."""

    event_type: EventType = field(default=EventType.CONVERSATION_CLOSED, init=False)
    conversation_id: str = ""
    message_count: int = 0


@dataclass(frozen=True, slots=True, eq=True)
class MemoryStored(Event):
    """Emitted when memory is stored."""

    event_type: EventType = field(default=EventType.MEMORY_STORED, init=False)
    memory_id: str = ""
    scope: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class MemoryRemoved(Event):
    """Emitted when memory is removed."""

    event_type: EventType = field(default=EventType.MEMORY_REMOVED, init=False)
    memory_id: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class EmbeddingGenerated(Event):
    """Emitted when an embedding is generated."""

    event_type: EventType = field(default=EventType.EMBEDDING_GENERATED, init=False)
    embedding_id: str = ""
    model_id: str = ""
    dimension: int = 0


@dataclass(frozen=True, slots=True, eq=True)
class EmbeddingIndexChanged(Event):
    """Emitted when an embedding index is updated."""

    event_type: EventType = field(default=EventType.EMBEDDING_INDEX_UPDATED, init=False)
    index_id: str = ""
    entries_added: int = 0


@dataclass(frozen=True, slots=True, eq=True)
class AgentStarted(Event):
    """Emitted when an agent starts execution."""

    event_type: EventType = field(default=EventType.AGENT_STARTED, init=False)
    agent_id: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class AgentStopped(Event):
    """Emitted when an agent stops."""

    event_type: EventType = field(default=EventType.AGENT_STOPPED, init=False)
    agent_id: str = ""
    steps_executed: int = 0


@dataclass(frozen=True, slots=True, eq=True)
class AgentExecuted(Event):
    """Emitted when an agent completes a step."""

    event_type: EventType = field(default=EventType.AGENT_EXECUTED, init=False)
    agent_id: str = ""
    step: int = 0
    tool_invocations: int = 0


@dataclass(frozen=True, slots=True, eq=True)
class ToolInvoked(Event):
    """Emitted when a tool is invoked."""

    event_type: EventType = field(default=EventType.TOOL_INVOKED, init=False)
    tool_id: str = ""
    agent_id: str = ""
    duration_ms: float = 0.0


@dataclass(frozen=True, slots=True, eq=True)
class ToolFailed(Event):
    """Emitted when a tool invocation fails."""

    event_type: EventType = field(default=EventType.TOOL_FAILED, init=False)
    tool_id: str = ""
    error_code: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class HealthChanged(Event):
    """Emitted when AI runtime health changes."""

    event_type: EventType = field(default=EventType.HEALTH_CHANGED, init=False)
    previous_status: str = ""
    new_status: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class ProviderLoaded(Event):
    """Emitted when a provider is loaded."""

    event_type: EventType = field(default=EventType.PROVIDER_LOADED, init=False)
    provider_id: str = ""
    provider_type: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class ProviderUnloaded(Event):
    """Emitted when a provider is unloaded."""

    event_type: EventType = field(default=EventType.PROVIDER_UNLOADED, init=False)
    provider_id: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class ProviderHealthChanged(Event):
    """Emitted when a provider health status changes."""

    event_type: EventType = field(default=EventType.PROVIDER_HEALTH_CHANGED, init=False)
    provider_id: str = ""
    status: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class CapabilityDiscovered(Event):
    """Emitted when a new capability is discovered."""

    event_type: EventType = field(default=EventType.CAPABILITY_DISCOVERED, init=False)
    capability: str = ""
    provider_id: str = ""
