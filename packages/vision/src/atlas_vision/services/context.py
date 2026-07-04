# Atlas Vision Runtime Context

"""
Immutable runtime context with clone-based mutation.

VisionContext carries configuration and state through the runtime
without allowing in-place mutation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from atlas_vision.registry.vision_registry import VisionRegistry


@dataclass(frozen=True, slots=True, eq=True)
class VisionContext:
    """Immutable runtime context for Vision operations."""

    registry: VisionRegistry
    max_frame_buffer_size: int = 1000
    enable_streaming: bool = True
    enable_caching: bool = True
    cache_ttl_seconds: int = 300
    max_pipeline_depth: int = 100
    default_color_space: str = "srgb"
    extra_config: dict[str, Any] = field(default_factory=dict)

    def clone_with(self, **overrides: Any) -> "VisionContext":
        """Return a new context with the given overrides applied."""
        new_config = dict(self.extra_config)
        new_config.update(overrides.get("extra_config", {}))
        return VisionContext(
            registry=self.registry,
            max_frame_buffer_size=overrides.get(
                "max_frame_buffer_size", self.max_frame_buffer_size
            ),
            enable_streaming=overrides.get("enable_streaming", self.enable_streaming),
            enable_caching=overrides.get("enable_caching", self.enable_caching),
            cache_ttl_seconds=overrides.get(
                "cache_ttl_seconds", self.cache_ttl_seconds
            ),
            max_pipeline_depth=overrides.get(
                "max_pipeline_depth", self.max_pipeline_depth
            ),
            default_color_space=overrides.get(
                "default_color_space", self.default_color_space
            ),
            extra_config=new_config,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_frame_buffer_size": self.max_frame_buffer_size,
            "enable_streaming": self.enable_streaming,
            "enable_caching": self.enable_caching,
            "cache_ttl_seconds": self.cache_ttl_seconds,
            "max_pipeline_depth": self.max_pipeline_depth,
            "default_color_space": self.default_color_space,
            "extra_config": dict(self.extra_config),
        }
