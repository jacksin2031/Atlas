# Atlas Vision Runtime Plugin Bridge

"""
Plugin-Vision integration bridge.

Vision providers MUST be plugins.
Providers MUST NOT communicate directly.
Everything MUST pass through Runtime and IPC.
"""
from __future__ import annotations

from typing import Any, Optional

from atlas_vision.provider.base import ProviderType, VisionProvider
from atlas_vision.registry.provider_registry import ProviderRegistry


class PluginVisionBridge:
    """Bridges Plugin Host to Vision Runtime."""

    def __init__(self, registry: Optional[ProviderRegistry] = None) -> None:
        self._registry = registry or ProviderRegistry()

    def load_provider(self, provider: VisionProvider, name: str = "") -> None:
        self._registry.register(provider, name)

    def unload_provider(self, name: str) -> None:
        self._registry.shutdown_provider(name)

    def get_provider(self, name: str) -> Optional[VisionProvider]:
        return self._registry.get(name)

    def validate_provider_isolation(self, provider: VisionProvider) -> bool:
        return hasattr(provider, "provider_id") and hasattr(provider, "provider_type")

    def list_loaded_providers(self) -> list[str]:
        return self._registry.list_names()

    def get_providers_by_type(self, ptype: ProviderType) -> list[VisionProvider]:
        return self._registry.get_by_type(ptype)
