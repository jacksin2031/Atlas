# Atlas Vision Runtime Frame Models

"""
Immutable frame data structures for the Vision Runtime.

All frame models use frozen dataclasses to guarantee immutability.
Frame data flows through the runtime without mutation.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class FrameFormat(Enum):
    """Supported frame pixel formats."""

    RGBA = "rgba"
    RGB = "rgb"
    BGR = "bgr"
    GRAY = "gray"
    YUV420 = "yuv420"
    BAYER_RGGB = "bayer_rggb"


class FrameColorSpace(Enum):
    """Color space identifiers."""

    SRGB = "srgb"
    LINEAR_SRGB = "linear_srgb"
    BT709 = "bt709"
    BT2020 = "bt2020"
    GRAYSCALE = "grayscale"


@dataclass(frozen=True, slots=True, eq=True)
class FrameTimestamp:
    """Immutable timestamp for frame timing."""

    wall_clock: datetime
    monotonic_ns: int
    sequence_number: int = 0

    @classmethod
    def now(cls, sequence_number: int = 0) -> "FrameTimestamp":
        import time
        return cls(
            wall_clock=datetime.now(timezone.utc),
            monotonic_ns=time.monotonic_ns(),
            sequence_number=sequence_number,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "wall_clock": self.wall_clock.isoformat(),
            "monotonic_ns": self.monotonic_ns,
            "sequence_number": self.sequence_number,
        }


@dataclass(frozen=True, slots=True, eq=True)
class FrameResolution:
    """Immutable resolution descriptor."""

    width: int
    height: int

    @property
    def pixels(self) -> int:
        return self.width * self.height

    @property
    def aspect_ratio(self) -> float:
        if self.height == 0:
            return 0.0
        return self.width / self.height

    def __lt__(self, other: "FrameResolution") -> bool:
        if self.width != other.width:
            return self.width < other.width
        return self.height < other.height

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FrameResolution):
            return NotImplemented
        return self.width == other.width and self.height == other.height

    def __hash__(self) -> int:
        return hash((self.width, self.height))

    def to_dict(self) -> dict[str, Any]:
        return {"width": self.width, "height": self.height}


@dataclass(frozen=True, slots=True, eq=True)
class FrameMetadata:
    """Immutable metadata attached to each frame."""

    frame_id: str
    sequence_number: int
    resolution: FrameResolution
    format: FrameFormat
    color_space: FrameColorSpace
    timestamp: FrameTimestamp
    source_id: str = ""
    rotation_degrees: int = 0
    exposure_time_us: int = 0
    gain_db: float = 0.0
    extra: dict[str, Any] = field(default_factory=dict)

    def clone_with_extra(self, **kwargs: Any) -> "FrameMetadata":
        new_extra = dict(self.extra)
        new_extra.update(kwargs)
        return FrameMetadata(
            frame_id=self.frame_id,
            sequence_number=self.sequence_number,
            resolution=self.resolution,
            format=self.format,
            color_space=self.color_space,
            timestamp=self.timestamp,
            source_id=self.source_id,
            rotation_degrees=self.rotation_degrees,
            exposure_time_us=self.exposure_time_us,
            gain_db=self.gain_db,
            extra=new_extra,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "frame_id": self.frame_id,
            "sequence_number": self.sequence_number,
            "resolution": self.resolution.to_dict(),
            "format": self.format.value,
            "color_space": self.color_space.value,
            "timestamp": self.timestamp.to_dict(),
            "source_id": self.source_id,
            "rotation_degrees": self.rotation_degrees,
            "extra": dict(self.extra),
        }


@dataclass(frozen=True, slots=True, eq=True)
class FrameBuffer:
    """Immutable frame pixel buffer."""

    data: bytes
    size_bytes: int
    stride: int
    buffer_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def empty(cls, size_bytes: int = 0, stride: int = 0) -> "FrameBuffer":
        return cls(data=bytes(0), size_bytes=size_bytes, stride=stride)

    def to_dict(self) -> dict[str, Any]:
        return {
            "buffer_id": self.buffer_id,
            "size_bytes": self.size_bytes,
            "stride": self.stride,
        }


@dataclass(frozen=True, slots=True, eq=True)
class Frame:
    """Immutable frame combining buffer, metadata, and region."""

    frame_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    buffer: FrameBuffer = field(default_factory=lambda: FrameBuffer.empty())
    metadata: FrameMetadata = field(
        default_factory=lambda: FrameMetadata(
            frame_id="",
            sequence_number=0,
            resolution=FrameResolution(0, 0),
            format=FrameFormat.RGBA,
            color_space=FrameColorSpace.SRGB,
            timestamp=FrameTimestamp.now(),
        )
    )
    region: Optional["FrameRegion"] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "frame_id": self.frame_id,
            "buffer": self.buffer.to_dict(),
            "metadata": self.metadata.to_dict(),
            "region": self.region.to_dict() if self.region else None,
        }


@dataclass(frozen=True, slots=True, eq=True)
class FrameRegion:
    """Immutable region of interest within a frame."""

    x: int
    y: int
    width: int
    height: int

    @property
    def area(self) -> int:
        return self.width * self.height

    def to_dict(self) -> dict[str, Any]:
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}


@dataclass(frozen=True, slots=True, eq=True)
class FrameSource:
    """Immutable descriptor of a frame capture source."""

    source_id: str
    name: str
    source_type: str
    is_active: bool = False
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "name": self.name,
            "source_type": self.source_type,
            "is_active": self.is_active,
            "extra": dict(self.extra),
        }


@dataclass(frozen=True, slots=True, eq=True)
class FrameReference:
    """Immutable reference to a frame without copying data."""

    frame_id: str
    source_id: str
    sequence_number: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "frame_id": self.frame_id,
            "source_id": self.source_id,
            "sequence_number": self.sequence_number,
        }


@dataclass(frozen=True, slots=True, eq=True)
class FrameSnapshot:
    """Immutable snapshot of frame state at a point in time."""

    frame_id: str
    timestamp: FrameTimestamp
    resolution: FrameResolution
    format: FrameFormat
    buffer_size: int
    metadata_hash: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "frame_id": self.frame_id,
            "timestamp": self.timestamp.to_dict(),
            "resolution": self.resolution.to_dict(),
            "format": self.format.value,
            "buffer_size": self.buffer_size,
            "metadata_hash": self.metadata_hash,
        }


@dataclass(frozen=True, slots=True, eq=True)
class FrameHistory:
    """Immutable history of recent frames."""

    frame_ids: tuple[str, ...] = ()
    max_history: int = 100

    def append(self, frame_id: str) -> "FrameHistory":
        ids = list(self.frame_ids)
        ids.append(frame_id)
        if len(ids) > self.max_history:
            ids = ids[-self.max_history :]
        return FrameHistory(frame_ids=tuple(ids), max_history=self.max_history)

    def to_dict(self) -> dict[str, Any]:
        return {
            "frame_ids": list(self.frame_ids),
            "max_history": self.max_history,
        }
