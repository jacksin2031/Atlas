# Atlas Vision Runtime Health Service

"""
Health status management for the Vision Runtime.
"""
from __future__ import annotations

from enum import Enum
from typing import Any


class HealthStatus(Enum):
    """Health status values."""

    HEALTHY = "healthy"
    BUSY = "busy"
    DEGRADED = "degraded"
    RECOVERING = "recovering"
    FAILED = "failed"
    UNHEALTHY = "unhealthy"


class HealthService:
    """Manages health status for the Vision Runtime."""

    def __init__(self) -> None:
        self._status = HealthStatus.HEALTHY
        self._status_history: list[tuple[str, str]] = []
        self._details: str = ""

    @property
    def status(self) -> HealthStatus:
        return self._status

    def update_status(
        self, new_status: HealthStatus, details: str = ""
    ) -> None:
        old_status = self._status.value
        self._status = new_status
        self._details = details
        self._status_history.append((old_status, new_status.value))

    def is_healthy(self) -> bool:
        return self._status in (
            HealthStatus.HEALTHY,
            HealthStatus.BUSY,
            HealthStatus.DEGRADED,
        )

    def get_report(self) -> dict[str, Any]:
        return {
            "status": self._status.value,
            "details": self._details,
            "history_length": len(self._status_history),
        }

    def initialize(self) -> None:
        pass
