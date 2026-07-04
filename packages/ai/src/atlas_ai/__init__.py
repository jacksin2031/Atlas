# Atlas AI Runtime

"""Atlas AI Runtime - Platform-independent reference implementation."""
from __future__ import annotations

from atlas_ai.errors import (
    AIError, ModelError, ModelNotFoundError, ModelLoadError,
    ModelSnapshotError, ProviderError, ProviderNotFoundError,
    ProviderLoadError, ProviderHealthError, InferenceError,
    InferenceQueueError, InferenceExecutionError, InferenceTimeoutError,
    PromptError, PromptCompileError, PromptValidationError,
    ConversationError, ConversationNotFoundError, MemoryError,
    MemoryStoreError, EmbeddingError, EmbeddingIndexError,
    AgentError, AgentExecutionError, ToolError, ToolInvocationError,
    ToolPermissionError, RegistryError, DuplicateRegistrationError,
    ResourceError, ResourceExhaustedError, SecurityError,
    PermissionDeniedError, CapabilityError, CapabilityUnavailableError,
    SchedulingError, StorageError, HealthError, MetricsError,
)
from atlas_ai.events import (
    Event, EventType, ModelLoaded, ModelUnloaded,
    ModelSnapshotCreated, InferenceStarted, InferenceCompleted,
    InferenceFailed, InferenceScheduled, InferenceCancelled,
    PromptExecuted, PromptCompileFailed, ConversationCreated,
    ConversationClosed, MemoryStored, MemoryRemoved,
    EmbeddingGenerated, EmbeddingIndexChanged, AgentStarted,
    AgentStopped, AgentExecuted, ToolInvoked, ToolFailed,
    HealthChanged, ProviderLoaded, ProviderUnloaded,
    ProviderHealthChanged, CapabilityDiscovered,
)
from atlas_ai.models import (
    ModelCapability, ModelState, ModelProvider, ModelVersion,
    ModelMetadata, ModelRequirements, ModelResourceUsage,
    ModelConfiguration, ModelSnapshot, ModelDescriptor, ModelInstance,
)
from atlas_ai.providers import (
    ProviderCapability, ProviderHealth, ProviderDescriptor,
    ProviderSession, ProviderFactory, AIProvider, ProviderRegistry,
)
from atlas_ai.capabilities import (
    AIModelCapability, CapabilityStatus, Capability,
    CapabilityNegotiator,
)
from atlas_ai.inference import (
    InferenceState, InferenceMode, InferenceMetadata,
    InferenceRequest, InferenceResult, InferenceResponse,
    InferenceContext, InferenceJob, InferenceQueue,
    InferenceScheduler, InferenceExecutor,
)
from atlas_ai.prompts import (
    PromptVariables, PromptContext, PromptTemplate, Prompt,
    PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot,
    PromptRegistry,
)
from atlas_ai.conversations import (
    ConversationRole, ConversationState, ConversationMessage,
    ConversationHistory, Conversation, ConversationSession,
    ConversationRegistry,
)
from atlas_ai.memory import (
    MemoryScope, MemoryItem, MemoryContext, MemorySnapshot,
    MemoryQuery, MemoryPolicy, MemoryStore, MemoryRegistry,
)
from atlas_ai.embeddings import (
    EmbeddingModel, EmbeddingRequest, EmbeddingResponse,
    EmbeddingIndex, EmbeddingStore, EmbeddingRegistry,
    EmbeddingProvider,
)
from atlas_ai.agents import (
    AgentState, AgentCapability, AgentPolicy, AgentContext,
    Agent, AgentExecution, AgentRegistry, AgentScheduler,
)
from atlas_ai.tools import (
    ToolCapability, ToolPermission, ToolDescriptor, ToolResult,
    ToolInvocation, Tool, ToolRegistry,
)
from atlas_ai.scheduler import TriggerType, ScheduleEntry, AIScheduler
from atlas_ai.services import (
    AIService, ServiceState, AIContext, AISession,
    AIManager, AIRuntime, AIRuntimeManager,
)
from atlas_ai.integration.bridges import (
    IPCAIBridge, WorkflowAIBridge, VisionAIBridge,
)
from atlas_ai.resources.manager import (
    AIResourceManager, LRUCache, TempBuffer,
)
from atlas_ai.metrics.collector import (
    AIMetricsCollector, Counter, Gauge, Histogram,
)
from atlas_ai.health.service import AIHealthService, HealthStatus
from atlas_ai.security.permissions import (
    SecurityValidator, SecurityPolicy, Permission,
)
from atlas_ai.storage.abstraction import (
    AIStorageAdapter, StorageDomain, StorageBackend,
)

__all__ = [
    "AIError", "ModelError", "ModelNotFoundError", "ModelLoadError",
    "ModelSnapshotError", "ProviderError", "ProviderNotFoundError",
    "ProviderLoadError", "ProviderHealthError", "InferenceError",
    "InferenceQueueError", "InferenceExecutionError",
    "InferenceTimeoutError", "PromptError", "PromptCompileError",
    "PromptValidationError", "ConversationError",
    "ConversationNotFoundError", "MemoryError", "MemoryStoreError",
    "EmbeddingError", "EmbeddingIndexError", "AgentError",
    "AgentExecutionError", "ToolError", "ToolInvocationError",
    "ToolPermissionError", "RegistryError", "DuplicateRegistrationError",
    "ResourceError", "ResourceExhaustedError", "SecurityError",
    "PermissionDeniedError", "CapabilityError",
    "CapabilityUnavailableError", "SchedulingError", "StorageError",
    "HealthError", "MetricsError", "Event", "EventType",
    "ModelLoaded", "ModelUnloaded", "ModelSnapshotCreated",
    "InferenceStarted", "InferenceCompleted", "InferenceFailed",
    "InferenceScheduled", "InferenceCancelled", "PromptExecuted",
    "PromptCompileFailed", "ConversationCreated", "ConversationClosed",
    "MemoryStored", "MemoryRemoved", "EmbeddingGenerated",
    "EmbeddingIndexChanged", "AgentStarted", "AgentStopped",
    "AgentExecuted", "ToolInvoked", "ToolFailed", "HealthChanged",
    "ProviderLoaded", "ProviderUnloaded", "ProviderHealthChanged",
    "CapabilityDiscovered", "ModelCapability", "ModelState",
    "ModelProvider", "ModelVersion", "ModelMetadata",
    "ModelRequirements", "ModelResourceUsage", "ModelConfiguration",
    "ModelSnapshot", "ModelDescriptor", "ModelInstance",
    "ProviderCapability", "ProviderHealth", "ProviderDescriptor",
    "ProviderSession", "ProviderFactory", "AIProvider",
    "ProviderRegistry", "AIModelCapability", "CapabilityStatus",
    "Capability", "CapabilityNegotiator", "InferenceState",
    "InferenceMode", "InferenceMetadata", "InferenceRequest",
    "InferenceResult", "InferenceResponse", "InferenceContext",
    "InferenceJob", "InferenceQueue", "InferenceScheduler",
    "InferenceExecutor", "PromptVariables", "PromptContext",
    "PromptTemplate", "Prompt", "PromptCompiler", "PromptExecutor",
    "PromptHistory", "PromptSnapshot", "PromptRegistry",
    "ConversationRole", "ConversationState", "ConversationMessage",
    "ConversationHistory", "Conversation", "ConversationSession",
    "ConversationRegistry", "MemoryScope", "MemoryItem",
    "MemoryContext", "MemorySnapshot", "MemoryQuery", "MemoryPolicy",
    "MemoryStore", "MemoryRegistry", "EmbeddingModel",
    "EmbeddingRequest", "EmbeddingResponse", "EmbeddingIndex",
    "EmbeddingStore", "EmbeddingRegistry", "EmbeddingProvider",
    "AgentState", "AgentCapability", "AgentPolicy", "AgentContext",
    "Agent", "AgentExecution", "AgentRegistry", "AgentScheduler",
    "ToolCapability", "ToolPermission", "ToolDescriptor", "ToolResult",
    "ToolInvocation", "Tool", "ToolRegistry", "TriggerType",
    "ScheduleEntry", "AIScheduler", "AIService", "ServiceState",
    "AIContext", "AISession", "AIManager", "AIRuntime",
    "AIRuntimeManager", "IPCAIBridge", "WorkflowAIBridge",
    "VisionAIBridge", "AIResourceManager", "LRUCache", "TempBuffer",
    "AIMetricsCollector", "Counter", "Gauge", "Histogram",
    "AIHealthService", "HealthStatus", "SecurityValidator",
    "SecurityPolicy", "Permission", "AIStorageAdapter",
    "StorageDomain", "StorageBackend",
]
