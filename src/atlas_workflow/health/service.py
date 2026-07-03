"""Health service integration for workflow runtime.

Per RFC-0306 (Runtime State Management). Health states:
Healthy, Busy, Paused, Recovering, Failed.
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Any


class HealthService:
    """Manages health state for the workflow runtime.

    Integrates with the Runtime Health service to report
    current operational status.
    """

    def __init__(self) -> None:
        self._state = "Healthy"
        self._last_updated: datetime = datetime.now(timezone.utc)
        self._details: dict[str, Any] = {}
        self._components: dict[str, str] = {}

    @property
    def state(self) -> str:
        return self._state

    def set_state(self, state: str, details: dict[str, Any] | None = None) -> None:
        """Set the overall health state."""
        valid_states = {"Healthy", "Busy", "Paused", "Recovering", "Failed"}
        if state not in valid_states:
            raise ValueError(f"Invalid health state: {state!r}. Must be one of {valid_states}")
        self._state = state
        self._last_updated = datetime.now(timezone.utc)
        if details:
            self._details = details

    def update_component_health(self, component: str, state: str) -> None:
        """Update health state for a specific component."""
        self._components[component] = state
        self._recompute_overall_state()

    def get_health_report(self) -> dict[str, Any]:
        return {
            "state": self._state,
            "last_updated": self._last_updated.isoformat(),
            "details": dict(self._details),
            "components": dict(self._components),
        }

    def is_healthy(self) -> bool:
        return self._state == "Healthy"

    def is_failed(self) -> bool:
        return self._state == "Failed"

    def _recompute_overall_state(self) -> None:
        if not self._components:
            return
        if any(s == "Failed" for s in self._components.values()):
            self._state = "Failed"
        elif any(s == "Busy" for s in self._components.values()):
            self._state = "Busy"
        elif all(s == "Healthy" for s in self._components.values()):
            self._state = "Healthy"
