# Atlas Vision Runtime Errors

"""
Complete error hierarchy for the Atlas Vision Runtime.

All errors inherit from VisionError. Each error category
provides a unique error code and descriptive message.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Optional


class VisionError(Exception):
    """Base error for all Vision Runtime errors."""

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


class FrameError(VisionError):
    """Errors related to frame operations."""

    def _default_code(self) -> str:
        return "VISION_FRAME_ERROR"


class InvalidFrameError(FrameError):
    """Frame data is invalid or corrupted."""

    def __init__(self, message: str = "Invalid frame data", frame_id: str | None = None) -> None:
        details: dict[str, Any] = {}
        if frame_id:
            details["frame_id"] = frame_id
        super().__init__(message, code="FRAME_INVALID", details=details)


class FrameNotFoundError(FrameError):
    """Requested frame not found."""

    def __init__(self, message: str = "Frame not found", frame_id: str | None = None) -> None:
        details: dict[str, Any] = {}
        if frame_id:
            details["frame_id"] = frame_id
        super().__init__(message, code="FRAME_NOT_FOUND", details=details)


class CaptureError(VisionError):
    """Errors related to capture operations."""

    def _default_code(self) -> str:
        return "VISION_CAPTURE_ERROR"


class CaptureSourceError(CaptureError):
    """Capture source is unavailable or invalid."""

    def __init__(self, message: str = "Capture source unavailable", source_id: str | None = None) -> None:
        details: dict[str, Any] = {}
        if source_id:
            details["source_id"] = source_id
        super().__init__(message, code="CAPTURE_SOURCE_ERROR", details=details)


class CaptureSessionError(CaptureError):
    """Capture session error."""

    def __init__(self, message: str = "Capture session error", session_id: str | None = None) -> None:
        details: dict[str, Any] = {}
        if session_id:
            details["session_id"] = session_id
        super().__init__(message, code="CAPTURE_SESSION_ERROR", details=details)


class PipelineError(VisionError):
    """Errors related to pipeline operations."""

    def _default_code(self) -> str:
        return "VISION_PIPELINE_ERROR"


class PipelineValidationError(PipelineError):
    """Pipeline definition is invalid."""

    def __init__(
        self, message: str = "Invalid pipeline definition", pipeline_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if pipeline_id:
            details["pipeline_id"] = pipeline_id
        super().__init__(message, code="PIPELINE_VALIDATION_ERROR", details=details)


class PipelineExecutionError(PipelineError):
    """Pipeline execution failed."""

    def __init__(
        self,
        message: str = "Pipeline execution failed",
        pipeline_id: str | None = None,
        stage: str | None = None,
    ) -> None:
        details: dict[str, Any] = {}
        if pipeline_id:
            details["pipeline_id"] = pipeline_id
        if stage:
            details["stage"] = stage
        super().__init__(message, code="PIPELINE_EXECUTION_ERROR", details=details)


class ProviderError(VisionError):
    """Errors related to provider operations."""

    def _default_code(self) -> str:
        return "VISION_PROVIDER_ERROR"


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


class RegistryError(VisionError):
    """Errors related to registry operations."""

    def _default_code(self) -> str:
        return "VISION_REGISTRY_ERROR"


class DuplicateRegistrationError(RegistryError):
    """Duplicate registration attempted."""

    def __init__(
        self, message: str = "Duplicate registration", entity_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if entity_id:
            details["entity_id"] = entity_id
        super().__init__(message, code="REGISTRY_DUPLICATE", details=details)


class SchedulerError(VisionError):
    """Errors related to scheduling."""

    def _default_code(self) -> str:
        return "VISION_SCHEDULER_ERROR"


class ResourceError(VisionError):
    """Errors related to resource management."""

    def _default_code(self) -> str:
        return "VISION_RESOURCE_ERROR"


class BufferExhaustedError(ResourceError):
    """Frame buffer pool exhausted."""

    def __init__(
        self, message: str = "Frame buffer pool exhausted", limit: int | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if limit is not None:
            details["limit"] = limit
        super().__init__(message, code="RESOURCE_BUFFER_EXHAUSTED", details=details)


class SecurityError(VisionError):
    """Errors related to security validation."""

    def _default_code(self) -> str:
        return "VISION_SECURITY_ERROR"


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


class GraphError(VisionError):
    """Errors related to pipeline graph operations."""

    def _default_code(self) -> str:
        return "VISION_GRAPH_ERROR"


class CycleDetectedError(GraphError):
    """Cycle detected in pipeline graph."""

    def __init__(
        self, message: str = "Cycle detected in graph", nodes: list[str] | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if nodes:
            details["nodes"] = nodes
        super().__init__(message, code="GRAPH_CYCLE_DETECTED", details=details)


class InvalidGraphNodeError(GraphError):
    """Invalid node reference in graph."""

    def __init__(
        self, message: str = "Invalid node reference", node_id: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if node_id:
            details["node_id"] = node_id
        super().__init__(message, code="GRAPH_INVALID_NODE", details=details)


class StorageError(VisionError):
    """Errors related to storage operations."""

    def _default_code(self) -> str:
        return "VISION_STORAGE_ERROR"


class CapabilityError(VisionError):
    """Errors related to capability negotiation."""

    def _default_code(self) -> str:
        return "VISION_CAPABILITY_ERROR"


class CapabilityUnavailableError(CapabilityError):
    """Requested capability is unavailable."""

    def __init__(
        self, message: str = "Capability unavailable", capability: str | None = None
    ) -> None:
        details: dict[str, Any] = {}
        if capability:
            details["capability"] = capability
        super().__init__(message, code="CAPABILITY_UNAVAILABLE", details=details)
