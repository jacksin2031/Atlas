# Atlas AI Runtime Services

"""
Core AI service classes implementing the Runtime Service Contract.

Supports AIRuntime, AIManager, AIContext, AISession, AIService.
"""
from __future__ import annotations

import threading
import time
import uuid
from typing import Any, Optional
from atlas_ai.health.service import AIHealthService, HealthStatus
from atlas_ai.metrics.collector import AIMetricsCollector
from atlas_ai.registry.ai_registry import AIRegistry
import time
from typing import Any, Optional


class AIService:
    """Abstract base class for all AI Runtime services."""

    @property
    def service_id(self) -> str:
        raise NotImplementedError

    @property
    def service_name(self) -> str:
        raise NotImplementedError

    def initialize(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def health_check(self) -> dict[str, Any]:
        return {"status": "healthy"}

    def shutdown(self) -> None:
        pass

    def get_metrics(self) -> dict[str, Any]:
        return {}


class ServiceState:
    """Service lifecycle states."""

    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting_down"
    TERMINATED = "terminated"
    FAILED = "failed"


class AIContext:
    """Immutable runtime context with clone-based mutation."""

    def __init__(
        self,
        model_id: str = "",
        provider_id: str = "",
        conversation_id: str = "",
        session_id: str = "",
        max_tokens: int = 2048,
        temperature: float = 0.7,
        enable_streaming: bool = False,
        enable_caching: bool = True,
        extra_config: dict[str, Any] | None = None,
    ) -> None:
        self._model_id = model_id
        self._provider_id = provider_id
        self._conversation_id = conversation_id
        self._session_id = session_id
        self._max_tokens = max_tokens
        self._temperature = temperature
        self._enable_streaming = enable_streaming
        self._enable_caching = enable_caching
        self._extra_config = extra_config or {}

    @property
    def model_id(self) -> str:
        return self._model_id

    @property
    def provider_id(self) -> str:
        return self._provider_id

    @property
    def conversation_id(self) -> str:
        return self._conversation_id

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def max_tokens(self) -> int:
        return self._max_tokens

    @property
    def temperature(self) -> float:
        return self._temperature

    @property
    def enable_streaming(self) -> bool:
        return self._enable_streaming

    @property
    def enable_caching(self) -> bool:
        return self._enable_caching

    @property
    def extra_config(self) -> dict[str, Any]:
        return dict(self._extra_config)

    def clone_with(self, **overrides: Any) -> AIContext:
        new_extra = dict(self._extra_config)
        new_extra.update(overrides.pop("extra_config", {}))
        return AIContext(
            model_id=overrides.get("model_id", self._model_id),
            provider_id=overrides.get("provider_id", self._provider_id),
            conversation_id=overrides.get(
                "conversation_id", self._conversation_id
            ),
            session_id=overrides.get("session_id", self._session_id),
            max_tokens=overrides.get("max_tokens", self._max_tokens),
            temperature=overrides.get("temperature", self._temperature),
            enable_streaming=overrides.get(
                "enable_streaming", self._enable_streaming
            ),
            enable_caching=overrides.get(
                "enable_caching", self._enable_caching
            ),
            extra_config=new_extra,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_id": self._model_id,
            "provider_id": self._provider_id,
            "conversation_id": self._conversation_id,
            "session_id": self._session_id,
            "max_tokens": self._max_tokens,
            "temperature": self._temperature,
            "enable_streaming": self._enable_streaming,
            "enable_caching": self._enable_caching,
            "extra_config": dict(self._extra_config),
        }


class AISession:
    """Manages an AI runtime session."""

    def __init__(
        self,
        session_id: str,
        context: AIContext,
        runtime: Any,
    ) -> None:
        self._session_id = session_id
        self._context = context
        self._runtime = runtime
        self._created_at = time.monotonic()
        self._active = True

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def context(self) -> AIContext:
        return self._context

    @property
    def is_active(self) -> bool:
        return self._active

    def update_context(self, **overrides: Any) -> None:
        self._context = self._context.clone_with(**overrides)

    def close(self) -> None:
        self._active = False

    @property
    def uptime_seconds(self) -> float:
        return time.monotonic() - self._created_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self._session_id,
            "context": self._context.to_dict(),
            "active": self._active,
            "uptime_seconds": self.uptime_seconds,
        }


class AIManager:
    """Central coordinator for all AI Runtime subsystems."""

    def __init__(self, runtime: Any) -> None:
        self._runtime = runtime
        self._registry = runtime.registry if hasattr(runtime, "registry") else None
        self._health = runtime.health_service if hasattr(runtime, "health_service") else None
        self._metrics = runtime.metrics if hasattr(runtime, "metrics") else None

    def get_registry(self) -> Any:
        return self._registry

    def get_health(self) -> Any:
        return self._health

    def get_metrics(self) -> Any:
        return self._metrics

    def health_check(self) -> dict[str, Any]:
        return {
            "registry": self._registry.to_dict() if self._registry else {},
            "health": self._health.status.value if self._health else "unknown",
        }

    def shutdown(self) -> None:
        if self._health:
            self._health.update_status("shutdown", "Manager shutting down")


class AIRuntime(AIService):
    """Core AI Runtime orchestrating all AI subsystems."""

    def __init__(self) -> None:
        self._state = ServiceState.CREATED
        self._lock = threading.Lock()
        self._start_time: Optional[float] = None
        from atlas_ai.registry.ai_registry import AIRegistry
        from atlas_ai.health.service import AIHealthService, HealthStatus
        from atlas_ai.metrics.collector import AIMetricsCollector
        self._registry = AIRegistry()
        self._health = AIHealthService()
        self._metrics = AIMetricsCollector()
        self._manager = AIManager(self)
        self._session: Optional[AISession] = None
        self._context: Optional[AIContext] = None

    @property
    def state(self) -> str:
        return self._state

    @property
    def service_id(self) -> str:
        return "ai_runtime"

    @property
    def service_name(self) -> str:
        return "AI Runtime"

    @property
    def registry(self) -> AIRegistry:
        return self._registry

    @property
    def manager(self) -> AIManager:
        return self._manager

    @property
    def health_service(self) -> AIHealthService:
        return self._health

    @property
    def metrics(self) -> AIMetricsCollector:
        return self._metrics

    def initialize(self) -> None:
        with self._lock:
            if self._state != ServiceState.CREATED:
                raise RuntimeError(f"Cannot initialize from state {self._state}")
            self._state = ServiceState.INITIALIZING
            try:
                self._registry.initialize()
                self._health.initialize()
                self._metrics.initialize()
                self._registry.register("ai_runtime", self, version="1.0.0")
                self._context = AIContext()
                self._session = AISession(
                    session_id="default", context=self._context, runtime=self
                )
                self._state = ServiceState.READY
                self._health.update_status(HealthStatus.HEALTHY, "Runtime initialized")
            except Exception as exc:
                self._state = ServiceState.FAILED
                self._health.update_status(HealthStatus.FAILED, str(exc))
                raise

    def start(self) -> None:
        with self._lock:
            if self._state != ServiceState.READY:
                raise RuntimeError(f"Cannot start from state {self._state}")
            self._state = ServiceState.RUNNING
            self._start_time = time.monotonic()
            self._health.update_status(HealthStatus.HEALTHY, "Runtime running")

    def stop(self) -> None:
        with self._lock:
            if self._state not in (ServiceState.RUNNING, ServiceState.READY):
                return
            self._state = ServiceState.SHUTTING_DOWN
            try:
                self._manager.shutdown()
            finally:
                self._state = ServiceState.TERMINATED

    def shutdown(self) -> None:
        self.stop()

    def health_check(self) -> dict[str, Any]:
        return {
            "state": self._state,
            "health": self._health.status.value,
            "uptime_seconds": (
                time.monotonic() - self._start_time
                if self._start_time
                else 0.0
            ),
        }

    def get_metrics(self) -> dict[str, Any]:
        return self._metrics.collect()

    def create_session(self, **kwargs: Any) -> AISession:
        import uuid
        context = AIContext(**kwargs) if kwargs else self._context
        session_id = str(uuid.uuid4())
        return AISession(session_id=session_id, context=context, runtime=self)

    def get_context(self) -> AIContext:
        if self._context is None:
            raise RuntimeError("Runtime not initialized")
        return self._context

    def to_dict(self) -> dict[str, Any]:
        return {
            "service_id": self.service_id,
            "service_name": self.service_name,
            "state": self._state,
            "health": self._health.status.value,
            "metrics": self.get_metrics(),
        }


class AIRuntimeManager:
    """Manages multiple AIRuntime instances."""

    def __init__(self) -> None:
        self._runtimes: dict[str, Any] = {}
        self._default_runtime: Any | None = None

    def register(self, runtime: Any, default: bool = False) -> None:
        rid = id(runtime)
        self._runtimes[str(rid)] = runtime
        if default:
            self._default_runtime = runtime

    def get(self, runtime_id: str) -> Any | None:
        return self._runtimes.get(runtime_id)

    def get_default(self) -> Any | None:
        return self._default_runtime

    def list_runtimes(self) -> list[str]:
        return list(self._runtimes.keys())

    def initialize_all(self) -> None:
        for runtime in self._runtimes.values():
            if hasattr(runtime, "initialize"):
                runtime.initialize()

    def start_all(self) -> None:
        for runtime in self._runtimes.values():
            if hasattr(runtime, "start"):
                runtime.start()

    def shutdown_all(self) -> None:
        for runtime in self._runtimes.values():
            if hasattr(runtime, "shutdown"):
                runtime.shutdown()

    def health_check(self) -> dict[str, Any]:
        result = {}
        for rid, runtime in self._runtimes.items():
            if hasattr(runtime, "health_check"):
                result[rid] = runtime.health_check()
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtimes": list(self._runtimes.keys()),
            "default_runtime": (
                self._default_runtime.service_id
                if self._default_runtime
                else None
            ),
        }
