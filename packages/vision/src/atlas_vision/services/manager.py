# Atlas Vision Runtime Manager

"""
VisionManager coordinates capture, pipeline, and provider subsystems.

Acts as the central coordinator between the runtime and individual
Vision subsystems through dependency injection.
"""
from __future__ import annotations

from typing import Any, Optional

from atlas_vision.capture.manager import CaptureManager
from atlas_vision.capture.sources import CaptureDescriptor, CaptureSource
from atlas_vision.errors import CaptureError, PipelineError, ProviderError, RegistryError
from atlas_vision.health.service import HealthService, HealthStatus
from atlas_vision.metrics.collector import VisionMetricsCollector as MetricsCollector
from atlas_vision.pipeline.manager import VisionPipelineManager
from atlas_vision.provider.base import ProviderType, VisionProvider
from atlas_vision.registry.capture_registry import CaptureRegistry
from atlas_vision.registry.pipeline_registry import PipelineRegistry
from atlas_vision.registry.provider_registry import ProviderRegistry
from atlas_vision.registry.vision_registry import VisionRegistry
from atlas_vision.scheduler.scheduler import VisionScheduler


class VisionManager:
    """Coordinates all Vision Runtime subsystems."""

    def __init__(
        self,
        registry: Optional[VisionRegistry] = None,
        health_service: Optional[HealthService] = None,
        metrics: Optional[MetricsCollector] = None,
    ) -> None:
        self._registry = registry or VisionRegistry()
        self._health = health_service or HealthService()
        self._metrics = metrics or MetricsCollector()
        self._capture_manager = CaptureManager()
        self._pipeline_registry = PipelineRegistry()
        self._pipeline_manager = VisionPipelineManager(
            registry=self._pipeline_registry,
            metrics=self._metrics,
        )
        self._provider_registry = ProviderRegistry()
        self._capture_registry = CaptureRegistry()
        self._scheduler = VisionScheduler(metrics=self._metrics)

    @property
    def capture_manager(self) -> CaptureManager:
        return self._capture_manager

    @property
    def pipeline_manager(self) -> VisionPipelineManager:
        return self._pipeline_manager

    @property
    def provider_registry(self) -> ProviderRegistry:
        return self._provider_registry

    @property
    def capture_registry(self) -> CaptureRegistry:
        return self._capture_registry

    @property
    def pipeline_registry(self) -> PipelineRegistry:
        return self._pipeline_registry

    @property
    def scheduler(self) -> VisionScheduler:
        return self._scheduler

    def register_provider(
        self, provider: VisionProvider, name: str = ""
    ) -> None:
        self._provider_registry.register(provider, name)
        self._metrics.increment("providers_loaded")

    def get_provider(self, name: str) -> Optional[VisionProvider]:
        return self._provider_registry.get(name)

    def list_providers(self) -> list[str]:
        return self._provider_registry.list_names()

    def register_capture_source(self, descriptor: CaptureDescriptor) -> None:
        self._capture_registry.register(descriptor)

    def get_capture_descriptor(self, descriptor_id: str) -> Optional[CaptureDescriptor]:
        return self._capture_registry.get(descriptor_id)

    def health_check(self) -> dict[str, Any]:
        return {
            "capture": self._capture_manager.health_check(),
            "pipeline": self._pipeline_manager.health_check(),
            "providers": self._provider_registry.health_check(),
            "scheduler": self._scheduler.health_check(),
        }

    def cleanup(self) -> None:
        self._capture_manager.stop_all_sessions()
        self._pipeline_manager.reset()
        self._scheduler.stop()
