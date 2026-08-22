# Atlas Vision Runtime Session

"""
VisionSession manages a single vision processing session.

Implements session lifecycle transitions:
Created -> Active -> Paused -> Running -> Stopping -> Stopped
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from atlas_vision.errors import VisionError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from atlas_vision.services.runtime import VisionRuntime
from atlas_vision.services.service import ServiceState


class SessionState(Enum):
    """Session lifecycle states."""

    CREATED = "created"
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"


class VisionSession:
    """Manages a single vision processing session."""

    def __init__(self, runtime: Optional[VisionRuntime] = None) -> None:
        self._runtime = runtime
        self._state = SessionState.CREATED
        self._session_id: str = ""
        self._started_at: Optional[float] = None
        self._stopped_at: Optional[float] = None

    @property
    def state(self) -> SessionState:
        return self._state

    @property
    def runtime(self) -> Optional[VisionRuntime]:
        return self._runtime

    def activate(self, session_id: str = "") -> None:
        if self._state != SessionState.CREATED:
            raise RuntimeError(f"Cannot activate from state {self._state.value}")
        self._state = SessionState.ACTIVE
        self._session_id = session_id or f"session_{id(self)}"
        if self._runtime:
            self._runtime.metrics.increment("sessions_started")

    def pause(self) -> None:
        if self._state != SessionState.ACTIVE:
            raise RuntimeError(f"Cannot pause from state {self._state.value}")
        self._state = SessionState.PAUSED

    def resume(self) -> None:
        if self._state != SessionState.PAUSED:
            raise RuntimeError(f"Cannot resume from state {self._state.value}")
        self._state = SessionState.ACTIVE

    def stop(self) -> None:
        if self._state not in (SessionState.ACTIVE, SessionState.PAUSED):
            raise RuntimeError(f"Cannot stop from state {self._state.value}")
        self._state = SessionState.STOPPING
        self._stopped_at = None
        self._state = SessionState.STOPPED

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self._session_id,
            "state": self._state.value,
            "started_at": self._started_at,
            "stopped_at": self._stopped_at,
        }
