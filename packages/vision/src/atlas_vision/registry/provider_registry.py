# Atlas Vision Runtime Provider Registry

"""
Provider lifecycle management through the registry.
"""
from __future__ import annotations

from typing import Any

from atlas_vision.errors import DuplicateRegistrationError, ProviderNotFoundError
from atlas_vision.provider.base import ProviderType, VisionProvider


class ProviderRegistry:
    """Registry for vision providers with lifecycle management."""

    def __init__(self) -> None:
        self._providers: dict[str, VisionProvider] = {}
        self._types: dict[str, list[str]] = {}

    def register(
        self, provider: VisionProvider, name: str = ""
    ) -> None:
        pid = name or provider.provider_id
        if pid in self._providers:
            raise DuplicateRegistrationError(
                f"Provider {pid} already registered", pid
            )
        self._providers[pid] = provider
        ptype = provider.provider_type.value
        if ptype not in self._types:
            self._types[ptype] = []
        self._types[ptype].append(pid)

    def get(self, name: str) -> VisionProvider | None:
        return self._providers.get(name)

    def get_by_type(self, ptype: ProviderType) -> list[VisionProvider]:
        pid_list = self._types.get(ptype.value, [])
        return [self._providers[p] for p in pid_list if p in self._providers]

    def list_names(self) -> list[str]:
        return list(self._providers.keys())

    def list_by_type(self) -> dict[str, list[str]]:
        return {k: list(v) for k, v in self._types.items()}

    def initialize_provider(self, name: str) -> None:
        provider = self._providers.get(name)
        if provider is None:
            raise ProviderNotFoundError(f"Provider not found: {name}", name)
        provider.initialize()

    def shutdown_provider(self, name: str) -> None:
        provider = self._providers.get(name)
        if provider is not None:
            provider.shutdown()
            del self._providers[name]

    def dispose(self, name: str) -> None:
        self.shutdown_provider(name)

    def health_check(self) -> dict[str, Any]:
        return {
            "total_providers": len(self._providers),
            "by_type": {k: len(v) for k, v in self._types.items()},
        }
