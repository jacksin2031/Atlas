# Atlas Vision Runtime Service Contract

"""
Abstract service base class implementing the Runtime Service Contract.

All Vision Runtime services must inherit from VisionServiceABC
to ensure consistent lifecycle, health, and metrics integration.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional


class ServiceState(Enum):
    """Service lifecycle states."""

    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting_down"
    TERMINATED = "terminated"
    FAILED = "failed"


class ServiceContract(ABC):
    """Abstract base class for all Vision Runtime services."""

    @property
    @abstractmethod
    def service_id(self) -> str:
        """Unique identifier for this service."""
        ...

    @property
    @abstractmethod
    def service_name(self) -> str:
        """Human-readable service name."""
        ...

    @property
    @abstractmethod
    def state(self) -> ServiceState:
        """Current service state."""
        ...

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the service. Must be called before use."""
        ...

    @abstractmethod
    def start(self) -> None:
        """Start the service for operation."""
        ...

    @abstractmethod
    def stop(self) -> None:
        """Stop the service gracefully."""
        ...

    @abstractmethod
    def health_check(self) -> dict[str, Any]:
        """Return health status dictionary."""
        ...

    @abstractmethod
    def shutdown(self) -> None:
        """Perform full shutdown and cleanup."""
        ...

    @abstractmethod
    def get_metrics(self) -> dict[str, Any]:
        """Return service-specific metrics."""
        ...
