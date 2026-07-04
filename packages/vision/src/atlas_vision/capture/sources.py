# Atlas Vision Runtime Capture Sources

"""
Capture source definitions and descriptors.

Provides abstract source types and capability negotiation
without platform-specific dependencies.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional


class CaptureSourceType(Enum):
    """Types of capture sources."""

    DESKTOP = "desktop"
    WINDOW = "window"
    REGION = "region"
    CAMERA = "camera"
    IMAGE = "image"
    VIDEO = "video"
    STREAM = "stream"
    VIRTUAL = "virtual"


class CaptureCapability(Enum):
    """Capture capabilities."""

    RESOLUTION_PROBE = auto()
    FRAMERATE_CONFIG = auto()
    COLOR_FORMAT_CONFIG = auto()
    REGION_CROP = auto()
    ROTATION = auto()
    SCALING = auto()
    STREAMING = auto()
    SNAPSHOT = auto()
    AUDIO = auto()


@dataclass(frozen=True, slots=True, eq=True)
class CaptureConfiguration:
    """Immutable capture configuration."""

    source_type: CaptureSourceType
    resolution_width: int = 0
    resolution_height: int = 0
    framerate: float = 30.0
    color_format: str = "RGBA"
    region_x: int = 0
    region_y: int = 0
    region_width: int = 0
    region_height: int = 0
    rotation_degrees: int = 0
    scaling_factor: float = 1.0
    streaming: bool = True
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_type": self.source_type.value,
            "resolution": f"{self.resolution_width}x{self.resolution_height}",
            "framerate": self.framerate,
            "color_format": self.color_format,
            "region": (
                f"{self.region_x},{self.region_y},{self.region_width}x{self.region_height}"
                if self.region_width > 0
                else None
            ),
            "rotation_degrees": self.rotation_degrees,
            "scaling_factor": self.scaling_factor,
            "streaming": self.streaming,
            "extra": dict(self.extra),
        }


@dataclass(frozen=True, slots=True, eq=True)
class CaptureDescriptor:
    """Immutable descriptor for a capture source."""

    descriptor_id: str
    source_type: CaptureSourceType
    name: str
    capabilities: tuple[CaptureCapability, ...] = ()
    is_available: bool = True
    configuration: Optional[CaptureConfiguration] = None
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def for_desktop(cls, name: str = "Desktop") -> "CaptureDescriptor":
        return cls(
            descriptor_id=str(uuid.uuid4()),
            source_type=CaptureSourceType.DESKTOP,
            name=name,
            capabilities=(
                CaptureCapability.RESOLUTION_PROBE,
                CaptureCapability.FRAMERATE_CONFIG,
                CaptureCapability.COLOR_FORMAT_CONFIG,
                CaptureCapability.REGION_CROP,
                CaptureCapability.STREAMING,
                CaptureCapability.SNAPSHOT,
            ),
        )

    @classmethod
    def for_camera(cls, name: str = "Camera", camera_index: int = 0) -> "CaptureDescriptor":
        return cls(
            descriptor_id=str(uuid.uuid4()),
            source_type=CaptureSourceType.CAMERA,
            name=name,
            capabilities=(
                CaptureCapability.RESOLUTION_PROBE,
                CaptureCapability.FRAMERATE_CONFIG,
                CaptureCapability.COLOR_FORMAT_CONFIG,
                CaptureCapability.STREAMING,
                CaptureCapability.SNAPSHOT,
            ),
            extra={"camera_index": camera_index},
        )

    @classmethod
    def for_image(cls, path: str) -> "CaptureDescriptor":
        return cls(
            descriptor_id=str(uuid.uuid4()),
            source_type=CaptureSourceType.IMAGE,
            name=path,
            capabilities=(CaptureCapability.SNAPSHOT,),
            extra={"path": path},
        )

    @classmethod
    def for_video(cls, path: str) -> "CaptureDescriptor":
        return cls(
            descriptor_id=str(uuid.uuid4()),
            source_type=CaptureSourceType.VIDEO,
            name=path,
            capabilities=(
                CaptureCapability.RESOLUTION_PROBE,
                CaptureCapability.FRAMERATE_CONFIG,
                CaptureCapability.COLOR_FORMAT_CONFIG,
                CaptureCapability.SNAPSHOT,
            ),
            extra={"path": path},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "descriptor_id": self.descriptor_id,
            "source_type": self.source_type.value,
            "name": self.name,
            "capabilities": [c.value for c in self.capabilities],
            "is_available": self.is_available,
            "configuration": self.configuration.to_dict() if self.configuration else None,
            "extra": dict(self.extra),
        }


@dataclass(frozen=True, slots=True, eq=True)
class CaptureSource:
    """Immutable capture source handle."""

    source_id: str
    descriptor: CaptureDescriptor
    is_connected: bool = False
    connected_at: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "descriptor": self.descriptor.to_dict(),
            "is_connected": self.is_connected,
            "connected_at": self.connected_at,
        }
