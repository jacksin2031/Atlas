# Atlas AI Runtime Capabilities

"""
Capability negotiation and discovery for the AI Runtime.

Supports discovery of Chat, Completion, Embedding, Vision, Audio,
Image, Tool Calling, Structured Output, Streaming, Batch,
Fine Tuning, RAG, Memory, Reasoning.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class AIModelCapability(Enum):
    """AI-specific capabilities."""

    CHAT = "chat"
    COMPLETION = "completion"
    EMBEDDING = "embedding"
    VISION = "vision"
    AUDIO = "audio"
    IMAGE = "image"
    TOOL_CALLING = "tool_calling"
    STRUCTURED_OUTPUT = "structured_output"
    STREAMING = "streaming"
    BATCH = "batch"
    FINE_TUNING = "fine_tuning"
    RAG = "rag"
    MEMORY = "memory"
    REASONING = "reasoning"


class CapabilityStatus(Enum):
    """Capability availability status."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    PARTIAL = "partial"
    DISABLED = "disabled"
    DEGRADED = "degraded"


@dataclass(frozen=True, slots=True, eq=True)
class Capability:
    """Describes a single capability."""

    capability_id: str
    name: str
    status: CapabilityStatus = CapabilityStatus.AVAILABLE
    version: str = "1.0.0"
    provider_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    required_permissions: list[str] = field(default_factory=list)
    fallback_capabilities: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "name": self.name,
            "status": self.status.value,
            "version": self.version,
            "provider_id": self.provider_id,
            "metadata": dict(self.metadata),
            "required_permissions": list(self.required_permissions),
            "fallback_capabilities": list(self.fallback_capabilities),
        }


class CapabilityNegotiator:
    """Discovers and negotiates capabilities at runtime."""

    def __init__(self) -> None:
        self._capabilities: dict[str, Capability] = {}

    def register(self, capability: Capability) -> None:
        self._capabilities[capability.capability_id] = capability

    def get(self, capability_id: str) -> Optional[Capability]:
        return self._capabilities.get(capability_id)

    def list_capabilities(self) -> list[str]:
        return list(self._capabilities.keys())

    def check_availability(self, capability_id: str) -> bool:
        cap = self._capabilities.get(capability_id)
        if cap is None:
            return False
        return cap.status in (CapabilityStatus.AVAILABLE, CapabilityStatus.PARTIAL)

    def check_entitlement(self, capability_id: str, caller_id: str) -> bool:
        cap = self._capabilities.get(capability_id)
        if cap is None:
            return False
        return True

    def discover_capabilities(
        self, provider_capabilities: list[str]
    ) -> list[Capability]:
        results = []
        for cap_id in provider_capabilities:
            cap = self._capabilities.get(cap_id)
            if cap is not None:
                results.append(cap)
        return results

    def get_available(self) -> list[Capability]:
        return [
            cap for cap in self._capabilities.values()
            if cap.status == CapabilityStatus.AVAILABLE
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "capabilities": {
                k: v.to_dict() for k, v in self._capabilities.items()
            }
        }
