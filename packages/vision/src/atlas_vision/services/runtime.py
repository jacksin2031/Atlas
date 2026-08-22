# Atlas Vision Runtime

"""
Core Vision Runtime orchestrating capture, pipelines, and providers.

Implements the full lifecycle state machine from RFC-0002:
Created -> Initializing -> Ready -> Running -> ShuttingDown -> Terminated
"""
from __future__ import annotations

import threading
import time
from typing import Any, Optional

from atlas_vision.errors import (
    CapabilityError,
    CapabilityUnavailableError,
    GraphError,
    InvalidGraphNodeError,
    PipelineExecutionError,
    PipelineValidationError,
    ProviderError,
    RegistryError,
    ResourceError,
    SchedulerError,
    SecurityError,
    StorageError,
    VisionError,
)
from atlas_vision.health.service import HealthService, HealthStatus
from atlas_vision.metrics.collector import VisionMetricsCollector as MetricsCollector
from atlas_vision.registry.vision_registry import VisionRegistry
from atlas_vision.services.context import VisionContext
from atlas_vision.services.manager import VisionManager
from atlas_vision.services.session import VisionSession
from atlas_vision.services.service import ServiceContract, ServiceState


class VisionRuntime(ServiceContract):
    """Core runtime orchestrating all Vision subsystems."""

    def __init__(
        self,
        registry: Optional[VisionRegistry] = None,
        health_service: Optional[HealthService] = None,
        metrics: Optional[MetricsCollector] = None,
    ) -> None:
        self._state = ServiceState.CREATED
        self._registry = registry or VisionRegistry()
        self._health = health_service or HealthService()
        self._metrics = metrics or MetricsCollector()
        self._manager = VisionManager(
            registry=self._registry,
            health_service=self._health,
            metrics=self._metrics,
        )
        self._session: Optional["VisionSession"] = None
        self._context: Optional[VisionContext] = None
        self._start_time: Optional[float] = None
        self._lock = threading.Lock()

    @property
    def state(self) -> ServiceState:
        return self._state

    @property
    def service_id(self) -> str:
        return "vision_runtime"

    @property
    def service_name(self) -> str:
        return "Vision Runtime"

    @property
    def registry(self) -> VisionRegistry:
        return self._registry

    @property
    def manager(self) -> VisionManager:
        return self._manager

    @property
    def health_service(self) -> HealthService:
        return self._health

    @property
    def metrics(self) -> MetricsCollector:
        return self._metrics

    def initialize(self) -> None:
        with self._lock:
            if self._state != ServiceState.CREATED:
                raise RuntimeError(f"Cannot initialize from state {self._state.value}")
            self._state = ServiceState.INITIALIZING
            try:
                self._registry.initialize()
                self._health.initialize()
                self._metrics.initialize()
                self._registry.register("vision_runtime", self, version="1.0.0")
                self._context = VisionContext(registry=self._registry)
                self._session = VisionSession(runtime=self)
                self._state = ServiceState.READY
                self._health.update_status(HealthStatus.HEALTHY, "Runtime initialized")
            except Exception as exc:
                self._state = ServiceState.FAILED
                self._health.update_status(HealthStatus.FAILED, str(exc))
                raise

    def start(self) -> None:
        with self._lock:
            if self._state != ServiceState.READY:
                raise RuntimeError(f"Cannot start from state {self._state.value}")
            self._state = ServiceState.RUNNING
            self._start_time = time.monotonic()
            self._health.update_status(HealthStatus.HEALTHY, "Runtime running")

    def stop(self) -> None:
        with self._lock:
            if self._state not in (ServiceState.RUNNING, ServiceState.READY):
                return
            self._state = ServiceState.SHUTTING_DOWN
            try:
                self._manager.cleanup()
            finally:
                self._state = ServiceState.TERMINATED

    def shutdown(self) -> None:
        self.stop()

    def health_check(self) -> dict[str, Any]:
        return {
            "state": self._state.value,
            "health": self._health.status.value,
            "uptime_seconds": (
                time.monotonic() - self._start_time
                if self._start_time
                else 0.0
            ),
        }

    def get_metrics(self) -> dict[str, Any]:
        return self._metrics.collect()

    def create_session(self, **kwargs: Any) -> VisionSession:
        if self._session is None:
            raise RuntimeError("Runtime not initialized")
        return self._session

    def get_context(self) -> VisionContext:
        if self._context is None:
            raise RuntimeError("Runtime not initialized")
        return self._context

    def to_dict(self) -> dict[str, Any]:
        return {
            "service_id": self.service_id,
            "service_name": self.service_name,
            "state": self._state.value,
            "health": self._health.status.value,
            "metrics": self.get_metrics(),
        }
