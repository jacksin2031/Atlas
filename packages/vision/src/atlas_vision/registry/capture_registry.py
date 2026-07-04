# Atlas Vision Runtime Capture Registry

"""
Capture source descriptor registry.
"""
from __future__ import annotations

from typing import Any

from atlas_vision.capture.sources import CaptureDescriptor


class CaptureRegistry:
    """Registry for capture source descriptors."""

    def __init__(self) -> None:
        self._descriptors: dict[str, CaptureDescriptor] = {}

    def register(self, descriptor: CaptureDescriptor) -> None:
        self._descriptors[descriptor.descriptor_id] = descriptor

    def get(self, descriptor_id: str) -> CaptureDescriptor | None:
        return self._descriptors.get(descriptor_id)

    def list_descriptors(self) -> list[str]:
        return list(self._descriptors.keys())

    def is_available(self, descriptor_id: str) -> bool:
        desc = self._descriptors.get(descriptor_id)
        return desc is not None and desc.is_available
