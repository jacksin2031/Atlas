# Atlas Vision Runtime Pipeline Registry

"""
Pipeline definition registry.
"""
from __future__ import annotations

from typing import Any

from atlas_vision.errors import DuplicateRegistrationError, PipelineValidationError
from atlas_vision.pipeline.pipeline import VisionPipeline


class PipelineRegistry:
    """Registry for pipeline definitions."""

    def __init__(self) -> None:
        self._pipelines: dict[str, VisionPipeline] = {}

    def register(self, pipeline: VisionPipeline) -> None:
        if pipeline.pipeline_id in self._pipelines:
            raise DuplicateRegistrationError(
                f"Pipeline {pipeline.pipeline_id} already registered",
                pipeline.pipeline_id,
            )
        self._pipelines[pipeline.pipeline_id] = pipeline

    def get(self, pipeline_id: str) -> VisionPipeline | None:
        return self._pipelines.get(pipeline_id)

    def list_names(self) -> list[str]:
        return list(self._pipelines.keys())

    def clear(self) -> None:
        self._pipelines.clear()
