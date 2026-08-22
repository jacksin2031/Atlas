# Atlas AI Runtime Provider Abstraction

"""
Provider abstraction for the AI Runtime.

Providers are plugins. The runtime MUST NOT know concrete providers.
Supports AIProvider, ProviderRegistry, ProviderDescriptor,
ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class ProviderCapability(Enum):
    """Provider-level capabilities."""

    INFERENCE = "inference"
    EMBEDDING = "embedding"
    TOOL_CALLING = "tool_calling"
    STREAMING = "streaming"
    BATCH = "batch"
    FINE_TUNING = "fine_tuning"
    VISION = "vision"
    AUDIO = "audio"
    IMAGE = "image"
    RAG = "rag"
    MEMORY = "memory"
    REASONING = "reasoning"


class ProviderHealth(Enum):
    """Provider health states."""

    HEALTHY = "healthy"
    BUSY = "busy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True, eq=True)
class ProviderDescriptor:
    """Describes a provider without instantiating it."""

    provider_id: str
    name: str
    provider_type: str
    version: str
    capabilities: frozenset[ProviderCapability]
    endpoints: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def supports(self, capability: ProviderCapability) -> bool:
        return capability in self.capabilities

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "name": self.name,
            "provider_type": self.provider_type,
            "version": self.version,
            "capabilities": [c.value for c in self.capabilities],
            "endpoints": dict(self.endpoints),
        }


@dataclass
class ProviderSession:
    """Represents an active provider session."""

    session_id: str
    provider_id: str
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    last_activity: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, Any] = field(default_factory=dict)
    _active: bool = True

    def touch(self) -> None:
        self.last_activity = datetime.now(timezone.utc)

    def close(self) -> None:
        self._active = False

    @property
    def is_active(self) -> bool:
        return self._active

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "provider_id": self.provider_id,
            "active": self._active,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
        }


class ProviderFactory(ABC):
    """Abstract factory for creating provider instances."""

    @abstractmethod
    def create(self, descriptor: ProviderDescriptor) -> Any:
        """Create a provider instance from a descriptor."""
        ...

    @abstractmethod
    def destroy(self, provider: Any) -> None:
        """Destroy a provider instance."""
        ...


class AIProvider(ABC):
    """Abstract base class for all AI providers.

    Providers are plugins. The runtime must never import
    concrete provider implementations.
    """

    @property
    @abstractmethod
    def provider_id(self) -> str:
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...

    @property
    @abstractmethod
    def provider_type(self) -> str:
        ...

    @property
    @abstractmethod
    def health(self) -> ProviderHealth:
        ...

    @property
    @abstractmethod
    def capabilities(self) -> frozenset[ProviderCapability]:
        ...

    @abstractmethod
    def initialize(self) -> None:
        ...

    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...

    @abstractmethod
    def shutdown(self) -> None:
        ...

    @abstractmethod
    def health_check(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_session(self) -> ProviderSession:
        ...

    @abstractmethod
    def release_session(self, session: ProviderSession) -> None:
        ...

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "provider_name": self.provider_name,
            "provider_type": self.provider_type,
            "health": self.health.value,
            "capabilities": [c.value for c in self.capabilities],
        }


class ProviderRegistry:
    """Registry for AI providers."""

    def __init__(self) -> None:
        self._providers: dict[str, AIProvider] = {}
        self._factories: dict[str, ProviderFactory] = {}
        self._descriptors: dict[str, ProviderDescriptor] = {}

    def register(self, provider: AIProvider, descriptor: Optional[ProviderDescriptor] = None) -> None:
        pid = provider.provider_id
        if pid in self._providers:
            from atlas_ai.errors import DuplicateRegistrationError
            raise DuplicateRegistrationError(f"Provider {pid} already registered", pid)
        self._providers[pid] = provider
        if descriptor:
            self._descriptors[pid] = descriptor

    def register_factory(self, provider_type: str, factory: ProviderFactory) -> None:
        self._factories[provider_type] = factory

    def get(self, provider_id: str) -> Optional[AIProvider]:
        return self._providers.get(provider_id)

    def get_descriptor(self, provider_id: str) -> Optional[ProviderDescriptor]:
        return self._descriptors.get(provider_id)

    def list_providers(self) -> list[str]:
        return list(self._providers.keys())

    def is_registered(self, provider_id: str) -> bool:
        return provider_id in self._providers

    def create_provider(self, descriptor: ProviderDescriptor) -> AIProvider:
        factory = self._factories.get(descriptor.provider_type)
        if factory is None:
            from atlas_ai.errors import ProviderLoadError
            raise ProviderLoadError(
                f"No factory for provider type: {descriptor.provider_type}",
                descriptor.provider_id,
            )
        return factory.create(descriptor)

    def remove(self, provider_id: str) -> None:
        provider = self._providers.pop(provider_id, None)
        if provider is not None:
            provider.shutdown()
        self._descriptors.pop(provider_id, None)

    def health_check(self) -> dict[str, Any]:
        result = {}
        for pid, provider in self._providers.items():
            try:
                result[pid] = provider.health_check()
            except Exception as exc:
                result[pid] = {"status": "error", "error": str(exc)}
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "providers": list(self._providers.keys()),
            "factories": list(self._factories.keys()),
        }
