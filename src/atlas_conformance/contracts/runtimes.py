from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class ContractType(Enum):
    SERVICE = auto()
    LIFECYCLE = auto()
    METRICS = auto()
    HEALTH = auto()
    PROVIDER = auto()
    SECURITY = auto()
    STORAGE = auto()


@dataclass(frozen=True, slots=True)
class RuntimeServiceContract:
    service_name: str
    required_methods: tuple[str, ...] = ()
    required_attributes: tuple[str, ...] = ()
    lifecycle_aware: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RuntimeLifecycleContract:
    states: tuple[str, ...] = (
        "CREATED", "INITIALIZING", "READY",
        "RUNNING", "SHUTTING_DOWN", "TERMINATED",
    )
    required_transitions: tuple[tuple[str, str], ...] = (
        ("CREATED", "INITIALIZING"),
        ("INITIALIZING", "READY"),
        ("READY", "RUNNING"),
        ("RUNNING", "SHUTTING_DOWN"),
        ("SHUTTING_DOWN", "TERMINATED"),
    )
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RuntimeMetricsContract:
    required_metric_types: tuple[str, ...] = ("counter", "gauge", "histogram")
    required_endpoints: tuple[str, ...] = ("/metrics",)
    p50_supported: bool = True
    p95_supported: bool = True
    p99_supported: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RuntimeHealthContract:
    required_states: tuple[str, ...] = (
        "healthy", "degraded", "warning",
        "error", "unknown", "initializing",
    )
    health_endpoint: str = "/health"
    requires_health_service: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RuntimeProviderContract:
    requires_abstract_base_class: bool = True
    requires_registry: bool = True
    requires_factory: bool = True
    requires_capability_negotiation: bool = True
    swappable_without_restart: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RuntimeSecurityContract:
    requires_permission_model: bool = True
    requires_sandbox: bool = True
    requires_audit_logging: bool = True
    permission_count: int = 10
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RuntimeStorageContract:
    requires_backend_abstraction: bool = True
    requires_transaction_support: bool = True
    requires_snapshot_support: bool = True
    backend_types: tuple[str, ...] = ("sqlite", "postgresql", "memory")
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RuntimeContract:
    runtime_name: str
    service: RuntimeServiceContract | None = None
    lifecycle: RuntimeLifecycleContract | None = None
    metrics: RuntimeMetricsContract | None = None
    health: RuntimeHealthContract | None = None
    provider: RuntimeProviderContract | None = None
    security: RuntimeSecurityContract | None = None
    storage: RuntimeStorageContract | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def contract_types(self) -> tuple[ContractType, ...]:
        types = []
        if self.service:
            types.append(ContractType.SERVICE)
        if self.lifecycle:
            types.append(ContractType.LIFECYCLE)
        if self.metrics:
            types.append(ContractType.METRICS)
        if self.health:
            types.append(ContractType.HEALTH)
        if self.provider:
            types.append(ContractType.PROVIDER)
        if self.security:
            types.append(ContractType.SECURITY)
        if self.storage:
            types.append(ContractType.STORAGE)
        return tuple(types)
