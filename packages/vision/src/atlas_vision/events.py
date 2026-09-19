# Atlas Vision Runtime Events

"""
Immutable event types for the Vision Runtime.

Events are frozen dataclasses representing state changes
in capture, pipelines, providers, and health.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class EventType(Enum):
    """Event type enumeration."""

    FRAME_CAPTURED = "frame_captured"
    FRAME_DROPPED = "frame_dropped"
    PIPELINE_STARTED = "pipeline_started"
    PIPELINE_COMPLETED = "pipeline_completed"
    PIPELINE_FAILED = "pipeline_failed"
    PROVIDER_LOADED = "provider_loaded"
    PROVIDER_UNLOADED = "provider_unloaded"
    CAPTURE_STARTED = "capture_started"
    CAPTURE_STOPPED = "capture_stopped"
    CAPTURE_FAILED = "capture_failed"
    VISION_HEALTH_CHANGED = "vision_health_changed"


@dataclass(frozen=True, slots=True, eq=True)
class Event:
    """Base immutable event."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = EventType.FRAME_CAPTURED
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
class FrameCaptured(Event):
    """Emitted when a frame is successfully captured."""

    event_type: EventType = field(default=EventType.FRAME_CAPTURED, init=False)
    frame_id: str = ""
    source_id: str = ""
    duration_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        d = Event.to_dict(self)
        d.update({"frame_id": self.frame_id, "source_id": self.source_id})
        return d


@dataclass(frozen=True, slots=True, eq=True)
class FrameDropped(Event):
    """Emitted when a frame is dropped due to overload."""

    event_type: EventType = field(default=EventType.FRAME_DROPPED, init=False)
    frame_id: str = ""
    reason: str = "buffer_full"


@dataclass(frozen=True, slots=True, eq=True)
class PipelineStarted(Event):
    """Emitted when a pipeline begins execution."""

    event_type: EventType = field(default=EventType.PIPELINE_STARTED, init=False)
    pipeline_id: str = ""
    node_count: int = 0


@dataclass(frozen=True, slots=True, eq=True)
class PipelineCompleted(Event):
    """Emitted when a pipeline finishes successfully."""

    event_type: EventType = field(default=EventType.PIPELINE_COMPLETED, init=False)
    pipeline_id: str = ""
    frame_count: int = 0
    duration_ms: float = 0.0


@dataclass(frozen=True, slots=True, eq=True)
class PipelineFailed(Event):
    """Emitted when a pipeline execution fails."""

    event_type: EventType = field(default=EventType.PIPELINE_FAILED, init=False)
    pipeline_id: str = ""
    error_code: str = ""
    stage: str = ""


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
class CaptureStarted(Event):
    """Emitted when capture begins."""

    event_type: EventType = field(default=EventType.CAPTURE_STARTED, init=False)
    session_id: str = ""
    source_id: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class CaptureStopped(Event):
    """Emitted when capture stops."""

    event_type: EventType = field(default=EventType.CAPTURE_STOPPED, init=False)
    session_id: str = ""
    frames_captured: int = 0


@dataclass(frozen=True, slots=True, eq=True)
class CaptureFailed(Event):
    """Emitted when capture fails."""

    event_type: EventType = field(default=EventType.CAPTURE_FAILED, init=False)
    session_id: str = ""
    error_code: str = ""


@dataclass(frozen=True, slots=True, eq=True)
class VisionHealthChanged(Event):
    """Emitted when vision runtime health changes."""

    event_type: EventType = field(default=EventType.VISION_HEALTH_CHANGED, init=False)
    previous_status: str = ""
    new_status: str = ""
