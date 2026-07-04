# Atlas AI Runtime Health

"""
Health monitoring for the AI Runtime.

Exposes Healthy, Busy, Loading, Recovering, Degraded, Failed states.
"""
from __future__ import annotations

from enum import Enum
from typing import Any


class HealthStatus(Enum):
    """Health status enumeration."""

    HEALTHY = "healthy"
    BUSY = "busy"
    LOADING = "loading"
    RECOVERING = "recovering"
    DEGRADED = "degraded"
    FAILED = "failed"


class AIHealthService:
    """Health monitoring service for AI Runtime."""

    def __init__(self) -> None:
        self._status = HealthStatus.HEALTHY
        self._details: dict[str, Any] = {}
        self._services: dict[str, HealthStatus] = {}
        self._initialized = False

    def initialize(self) -> None:
        self._initialized = True

    def update_status(self, status: HealthStatus, details: str = "") -> None:
        self._status = status
        if details:
            self._details["message"] = details

    @property
    def status(self) -> HealthStatus:
        return self._status

    def register_service(self, service_id: str, status: HealthStatus = HealthStatus.HEALTHY) -> None:
        self._services[service_id] = status

    def update_service_status(self, service_id: str, status: HealthStatus) -> None:
        self._services[service_id] = status

    def health_check(self) -> dict[str, Any]:
        degraded_count = sum(
            1 for s in self._services.values() if s == HealthStatus.DEGRADED
        )
        failed_count = sum(
            1 for s in self._services.values() if s == HealthStatus.FAILED
        )
        if failed_count > 0:
            self.update_status(HealthStatus.FAILED)
        elif degraded_count > 0:
            self.update_status(HealthStatus.DEGRADED)
        elif any(s == HealthStatus.LOADING for s in self._services.values()):
            self.update_status(HealthStatus.LOADING)
        elif any(s == HealthStatus.HEALTHY for s in self._services.values()):
            self.update_status(HealthStatus.HEALTHY)
        return {
            "status": self._status.value,
            "details": dict(self._details),
            "services": {k: v.value for k, v in self._services.items()},
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self._status.value,
            "details": dict(self._details),
            "service_count": len(self._services),
        }
