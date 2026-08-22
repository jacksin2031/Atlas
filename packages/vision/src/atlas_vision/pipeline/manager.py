# Atlas Vision Runtime Pipeline Manager

"""
VisionPipelineManager coordinates pipeline lifecycle and execution tracking.
"""
from __future__ import annotations

from typing import Any

from atlas_vision.errors import PipelineExecutionError, PipelineValidationError
from atlas_vision.metrics.collector import VisionMetricsCollector as MetricsCollector
from atlas_vision.pipeline.pipeline import VisionPipeline
from atlas_vision.registry.pipeline_registry import PipelineRegistry


class VisionPipelineManager:
    """Manages pipeline registration, execution, and tracking."""

    def __init__(
        self,
        registry: PipelineRegistry | None = None,
        metrics: MetricsCollector | None = None,
    ) -> None:
        self._registry = registry or PipelineRegistry()
        self._metrics = metrics or MetricsCollector()
        self._running_count: int = 0

    def register_pipeline(self, pipeline: VisionPipeline) -> None:
        self._registry.register(pipeline)

    def get_pipeline(self, pipeline_id: str) -> VisionPipeline | None:
        return self._registry.get(pipeline_id)

    def list_pipelines(self) -> list[str]:
        return self._registry.list_names()

    def execute(
        self, pipeline_id: str, frame_data: Any
    ) -> Any:
        pipeline = self._registry.get(pipeline_id)
        if pipeline is None:
            raise PipelineValidationError(
                f"Pipeline not found: {pipeline_id}", pipeline_id
            )
        self._running_count += 1
        try:
            result = pipeline.execute(frame_data)
            self._metrics.increment("pipelines_completed")
            return result
        except Exception as exc:
            self._metrics.increment("pipelines_failed")
            raise
        finally:
            self._running_count -= 1

    def health_check(self) -> dict[str, Any]:
        return {
            "total_pipelines": len(self._registry.list_names()),
            "running_pipelines": self._running_count,
        }

    def reset(self) -> None:
        self._registry.clear()
