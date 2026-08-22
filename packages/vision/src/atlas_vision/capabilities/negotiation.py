# Atlas Vision Runtime Capability Negotiation

"""
Capability negotiation for vision providers.

Supports OCR, Detection, Segmentation, Classification,
GPU, CPU, Batch, Streaming, Feature matching.
"""
from __future__ import annotations

from enum import Enum
from typing import Any


class Capability(Enum):
    """Vision capabilities."""

    OCR = "ocr"
    DETECTION = "detection"
    SEGMENTATION = "segmentation"
    CLASSIFICATION = "classification"
    GPU = "gpu"
    CPU = "cpu"
    BATCH = "batch"
    STREAMING = "streaming"
    FEATURE_MATCHING = "feature_matching"


class CapabilityStatus(Enum):
    """Status of a capability."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    DEGRADED = "degraded"


class CapabilityNegotiator:
    """Negotiates capabilities between providers and runtime."""

    def __init__(self) -> None:
        self._provider_caps: dict[str, set[Capability]] = {}

    def register_provider_capabilities(
        self, provider_id: str, capabilities: list[Capability]
    ) -> None:
        self._provider_caps[provider_id] = set(capabilities)

    def get_capabilities(self, provider_id: str) -> set[Capability]:
        return self._provider_caps.get(provider_id, set())

    def negotiate(
        self, provider_id: str, required: list[Capability]
    ) -> bool:
        caps = self._provider_caps.get(provider_id, set())
        return all(c in caps for c in required)

    def discover(self, capability: Capability) -> list[str]:
        return [
            pid
            for pid, caps in self._provider_caps.items()
            if capability in caps
        ]

    def get_available_capabilities(self) -> list[str]:
        result = []
        for caps in self._provider_caps.values():
            for c in caps:
                if c.value not in result:
                    result.append(c.value)
        return sorted(result)

    def negotiate_capabilities(
        self,
        requested: set[Capability],
        provider_capabilities: set[Capability] | None = None,
    ) -> dict[str, str]:
        caps = provider_capabilities or self._provider_caps.get("__default__", set())
        result: dict[str, str] = {}
        for cap in sorted(requested, key=lambda c: c.value):
            if cap in caps:
                result[cap.value] = CapabilityStatus.AVAILABLE.value
            else:
                result[cap.value] = CapabilityStatus.UNAVAILABLE.value
        return result

    def discover_all(self) -> list[str]:
        all_caps = set()
        for caps in self._provider_caps.values():
            all_caps.update(c.value for c in caps)
        return sorted(all_caps)

    def check_available(self, capability: Capability) -> bool:
        for caps in self._provider_caps.values():
            if capability in caps:
                return True
        return False

    def set_available(self, capabilities: set[Capability]) -> None:
        self._provider_caps["__default__"] = capabilities
