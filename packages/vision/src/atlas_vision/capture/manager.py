# Atlas Vision Runtime Capture Manager

"""
Capture session management with thread-safe lifecycle control.

Manages capture sessions, providers, and source discovery
through dependency injection.
"""
from __future__ import annotations

import threading
from typing import Any, Optional

from atlas_vision.capture.sources import (
    CaptureCapability,
    CaptureConfiguration,
    CaptureDescriptor,
    CaptureSource,
    CaptureSourceType,
)
from atlas_vision.capture.provider import CaptureProviderABC
from atlas_vision.errors import (
    CaptureSessionError,
    CaptureSourceError,
    ProviderError,
    VisionError,
)
from atlas_vision.health.service import HealthStatus
from atlas_vision.models.frame import Frame


class CaptureSession:
    """Manages a single capture session lifecycle."""

    def __init__(
        self,
        session_id: str,
        source: CaptureSource,
        provider: CaptureProviderABC,
        config: Optional[CaptureConfiguration] = None,
    ) -> None:
        self.session_id = session_id
        self.source = source
        self.provider = provider
        self.config = config or CaptureConfiguration(
            source_type=source.descriptor.source_type,
            streaming=True,
        )
        self._session_handle: Any = None
        self._running = False
        self._frames_captured = 0
        self._lock = threading.Lock()

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def frames_captured(self) -> int:
        return self._frames_captured

    def start(self) -> None:
        with self._lock:
            if self._running:
                return
            self._session_handle = self.provider.create_session(self.source)
            if not self.provider.start_session(self._session_handle):
                raise CaptureSessionError("Failed to start capture session", self.session_id)
            self._running = True

    def stop(self) -> None:
        with self._lock:
            if not self._running:
                return
            self.provider.stop_session(self._session_handle)
            self.provider.release_session(self._session_handle)
            self._session_handle = None
            self._running = False

    def capture(self) -> Optional[Frame]:
        if not self._running:
            raise CaptureSessionError("Session not running", self.session_id)
        frame = self.provider.capture_frame(self._session_handle)
        if frame is not None:
            with self._lock:
                self._frames_captured += 1
        return frame

    def health_check(self) -> HealthStatus:
        if not self._running:
            return HealthStatus.UNHEALTHY
        try:
            if self.provider.health_check():
                return HealthStatus.HEALTHY
            return HealthStatus.DEGRADED
        except Exception:
            return HealthStatus.FAILED

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "source_id": self.source.source_id,
            "running": self._running,
            "frames_captured": self._frames_captured,
        }


class CaptureManager:
    """Thread-safe manager for capture sessions and providers."""

    def __init__(self) -> None:
        self._sessions: dict[str, CaptureSession] = {}
        self._providers: dict[str, CaptureProviderABC] = {}
        self._lock = threading.Lock()

    def register_provider(self, provider: CaptureProviderABC, name: str = "") -> None:
        pid = name or type(provider).__name__
        with self._lock:
            self._providers[pid] = provider

    def get_provider(self, name: str) -> Optional[CaptureProviderABC]:
        return self._providers.get(name)

    def list_providers(self) -> list[str]:
        return list(self._providers.keys())

    def create_session(
        self,
        source: CaptureSource,
        provider_name: str = "",
        config: Optional[CaptureConfiguration] = None,
    ) -> CaptureSession:
        provider = self._providers.get(provider_name) if provider_name else next(iter(self._providers.values()), None)
        if provider is None:
            raise ProviderError("No capture provider available")
        session = CaptureSession(
            session_id=f"sess_{source.source_id}_{len(self._sessions)}",
            source=source,
            provider=provider,
            config=config,
        )
        with self._lock:
            self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[CaptureSession]:
        return self._sessions.get(session_id)

    def list_sessions(self) -> list[str]:
        return list(self._sessions.keys())

    def stop_all_sessions(self) -> None:
        with self._lock:
            for session in list(self._sessions.values()):
                try:
                    session.stop()
                except Exception:
                    pass
            self._sessions.clear()

    def health_check(self) -> dict[str, Any]:
        with self._lock:
            sessions = list(self._sessions.values())
        session_health = {}
        for s in sessions:
            session_health[s.session_id] = s.health_check().value
        return {
            "total_sessions": len(sessions),
            "active_sessions": sum(1 for s in sessions if s.is_running),
            "session_health": session_health,
            "providers": list(self._providers.keys()),
        }
