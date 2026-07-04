# Atlas Vision Runtime Capability Registry

"""
Capability discovery and registration.
"""
from __future__ import annotations

from typing import Any


class CapabilityRegistry:
    """Registry for discoverable capabilities."""

    def __init__(self) -> None:
        self._capabilities: dict[str, dict[str, Any]] = {}

    def register(
        self,
        capability: str,
        provider_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if capability not in self._capabilities:
            self._capabilities[capability] = {
                "supported_by": [],
                "metadata": {},
            }
        self._capabilities[capability]["supported_by"].append(provider_id)
        self._capabilities[capability]["metadata"].update(metadata or {})

    def is_supported(self, capability: str, provider_id: str) -> bool:
        cap = self._capabilities.get(capability)
        if cap is None:
            return False
        return provider_id in cap["supported_by"]

    def list_capabilities(self) -> list[str]:
        return list(self._capabilities.keys())

    def discover_for_provider(self, provider_id: str) -> list[str]:
        result = []
        for cap, info in self._capabilities.items():
            if provider_id in info["supported_by"]:
                result.append(cap)
        return result

    def discover(self, capability: str) -> list[str]:
        cap = self._capabilities.get(capability)
        if cap is None:
            return []
        return list(cap["supported_by"])
