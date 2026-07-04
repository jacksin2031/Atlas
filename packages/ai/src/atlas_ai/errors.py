# Atlas AI Runtime Errors

"""
Complete error hierarchy for the Atlas AI Runtime.

All errors inherit from AIError. Each error category
provides a unique error code and descriptive message.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Optional


class AIError(Exception):
    """Base error for all AI Runtime errors."""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.error_code = code or self._default_code()
        self.error_message = message
        self.error_details = details or {}
        super().__init__(self.error_message)

    def _default_code(self) -> str:
        return type(self).__name__

    def to_dict(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "error_message": self.error_message,
            "error_details": self.error_details,
        }


class ModelError(AIError):
    """Errors related to model operations."""

    def _default_code(self) -> str:
        return "AI_MODEL_ERROR"


class ModelNotFoundError(ModelError):
    """Model not found."""

    def __init__(
        self, message: str = "Model not found", model_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if model_id:
            details["model_id"] = model_id
        super().__init__(message, code="MODEL_NOT_FOUND", details=details)


class ModelLoadError(ModelError):
    """Model failed to load."""

    def __init__(
        self, message: str = "Model load failed", model_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if model_id:
            details["model_id"] = model_id
        super().__init__(message, code="MODEL_LOAD_ERROR", details=details)


class ModelSnapshotError(ModelError):
    """Model snapshot operation failed."""

    def __init__(
        self, message: str = "Model snapshot failed", model_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if model_id:
            details["model_id"] = model_id
        super().__init__(message, code="MODEL_SNAPSHOT_ERROR", details=details)


class ProviderError(AIError):
    """Errors related to provider operations."""

    def _default_code(self) -> str:
        return "AI_PROVIDER_ERROR"


class ProviderNotFoundError(ProviderError):
    """Provider not found."""

    def __init__(
        self, message: str = "Provider not found", provider_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if provider_id:
            details["provider_id"] = provider_id
        super().__init__(message, code="PROVIDER_NOT_FOUND", details=details)


class ProviderLoadError(ProviderError):
    """Provider failed to load."""

    def __init__(
        self, message: str = "Provider load failed", provider_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if provider_id:
            details["provider_id"] = provider_id
        super().__init__(message, code="PROVIDER_LOAD_ERROR", details=details)


class ProviderHealthError(ProviderError):
    """Provider health check failed."""

    def __init__(
        self, message: str = "Provider health check failed", provider_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if provider_id:
            details["provider_id"] = provider_id
        super().__init__(message, code="PROVIDER_HEALTH_ERROR", details=details)


class InferenceError(AIError):
    """Errors related to inference operations."""

    def _default_code(self) -> str:
        return "AI_INFERENCE_ERROR"


class InferenceQueueError(InferenceError):
    """Inference queue error."""

    def __init__(
        self, message: str = "Inference queue error", queue_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if queue_id:
            details["queue_id"] = queue_id
        super().__init__(message, code="INFERENCE_QUEUE_ERROR", details=details)


class InferenceExecutionError(InferenceError):
    """Inference execution failed."""

    def __init__(
        self, message: str = "Inference execution failed", job_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if job_id:
            details["job_id"] = job_id
        super().__init__(message, code="INFERENCE_EXECUTION_ERROR", details=details)


class InferenceTimeoutError(InferenceError):
    """Inference timed out."""

    def __init__(
        self, message: str = "Inference timed out", job_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if job_id:
            details["job_id"] = job_id
        super().__init__(message, code="INFERENCE_TIMEOUT", details=details)


class PromptError(AIError):
    """Errors related to prompt operations."""

    def _default_code(self) -> str:
        return "AI_PROMPT_ERROR"


class PromptCompileError(PromptError):
    """Prompt compilation failed."""

    def __init__(
        self, message: str = "Prompt compilation failed", prompt_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if prompt_id:
            details["prompt_id"] = prompt_id
        super().__init__(message, code="PROMPT_COMPILE_ERROR", details=details)


class PromptValidationError(PromptError):
    """Prompt validation failed."""

    def __init__(
        self, message: str = "Prompt validation failed", prompt_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if prompt_id:
            details["prompt_id"] = prompt_id
        super().__init__(message, code="PROMPT_VALIDATION_ERROR", details=details)


class ConversationError(AIError):
    """Errors related to conversation operations."""

    def _default_code(self) -> str:
        return "AI_CONVERSATION_ERROR"


class ConversationNotFoundError(ConversationError):
    """Conversation not found."""

    def __init__(
        self, message: str = "Conversation not found", conversation_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if conversation_id:
            details["conversation_id"] = conversation_id
        super().__init__(message, code="CONVERSATION_NOT_FOUND", details=details)


class MemoryError(AIError):
    """Errors related to memory operations."""

    def _default_code(self) -> str:
        return "AI_MEMORY_ERROR"


class MemoryStoreError(MemoryError):
    """Memory store operation failed."""

    def __init__(
        self, message: str = "Memory store failed", memory_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if memory_id:
            details["memory_id"] = memory_id
        super().__init__(message, code="MEMORY_STORE_ERROR", details=details)


class EmbeddingError(AIError):
    """Errors related to embedding operations."""

    def _default_code(self) -> str:
        return "AI_EMBEDDING_ERROR"


class EmbeddingIndexError(EmbeddingError):
    """Embedding index operation failed."""

    def __init__(
        self, message: str = "Embedding index failed", index_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if index_id:
            details["index_id"] = index_id
        super().__init__(message, code="EMBEDDING_INDEX_ERROR", details=details)


class AgentError(AIError):
    """Errors related to agent operations."""

    def _default_code(self) -> str:
        return "AI_AGENT_ERROR"


class AgentExecutionError(AgentError):
    """Agent execution failed."""

    def __init__(
        self, message: str = "Agent execution failed", agent_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if agent_id:
            details["agent_id"] = agent_id
        super().__init__(message, code="AGENT_EXECUTION_ERROR", details=details)


class ToolError(AIError):
    """Errors related to tool operations."""

    def _default_code(self) -> str:
        return "AI_TOOL_ERROR"


class ToolInvocationError(ToolError):
    """Tool invocation failed."""

    def __init__(
        self, message: str = "Tool invocation failed", tool_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if tool_id:
            details["tool_id"] = tool_id
        super().__init__(message, code="TOOL_INVOCATION_ERROR", details=details)


class ToolPermissionError(ToolError):
    """Tool permission denied."""

    def __init__(
        self, message: str = "Tool permission denied", tool_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if tool_id:
            details["tool_id"] = tool_id
        super().__init__(message, code="TOOL_PERMISSION_DENIED", details=details)


class RegistryError(AIError):
    """Errors related to registry operations."""

    def _default_code(self) -> str:
        return "AI_REGISTRY_ERROR"


class DuplicateRegistrationError(RegistryError):
    """Duplicate registration attempted."""

    def __init__(
        self, message: str = "Duplicate registration", entity_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if entity_id:
            details["entity_id"] = entity_id
        super().__init__(message, code="REGISTRY_DUPLICATE", details=details)


class ResourceError(AIError):
    """Errors related to resource management."""

    def _default_code(self) -> str:
        return "AI_RESOURCE_ERROR"


class ResourceExhaustedError(ResourceError):
    """Resource pool exhausted."""

    def __init__(
        self, message: str = "Resource pool exhausted", resource_type: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if resource_type:
            details["resource_type"] = resource_type
        super().__init__(message, code="RESOURCE_EXHAUSTED", details=details)


class SecurityError(AIError):
    """Errors related to security validation."""

    def _default_code(self) -> str:
        return "AI_SECURITY_ERROR"


class PermissionDeniedError(SecurityError):
    """Permission denied for operation."""

    def __init__(
        self,
        message: str = "Permission denied",
        caller_id: str | None = None,
        required_permission: str | None = None,
    ) -> None:
        details: dict[str, Any] = {}
        if caller_id:
            details["caller_id"] = caller_id
        if required_permission:
            details["required_permission"] = required_permission
        super().__init__(message, code="SECURITY_PERMISSION_DENIED", details=details)


class CapabilityError(AIError):
    """Errors related to capability negotiation."""

    def _default_code(self) -> str:
        return "AI_CAPABILITY_ERROR"


class CapabilityUnavailableError(CapabilityError):
    """Requested capability is unavailable."""

    def __init__(
        self, message: str = "Capability unavailable", capability: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if capability:
            details["capability"] = capability
        super().__init__(message, code="CAPABILITY_UNAVAILABLE", details=details)


class SchedulingError(AIError):
    """Errors related to scheduling."""

    def _default_code(self) -> str:
        return "AI_SCHEDULING_ERROR"


class StorageError(AIError):
    """Errors related to storage operations."""

    def _default_code(self) -> str:
        return "AI_STORAGE_ERROR"


class HealthError(AIError):
    """Errors related to health monitoring."""

    def _default_code(self) -> str:
        return "AI_HEALTH_ERROR"


class MetricsError(AIError):
    """Errors related to metrics collection."""

    def _default_code(self) -> str:
        return "AI_METRICS_ERROR"
