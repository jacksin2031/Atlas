# Atlas Vision Runtime Workflow Bridge

"""
Workflow-Vision integration bridge.

Workflow Runtime invokes Vision through abstract interfaces.
Workflow MUST NOT directly access providers.
"""
from __future__ import annotations

from typing import Any, Optional

from atlas_vision.pipeline.pipeline import VisionPipeline
from atlas_vision.registry.pipeline_registry import PipelineRegistry


class WorkflowVisionBridge:
    """Bridges Workflow Runtime to Vision Runtime."""

    def __init__(self, registry: Optional[PipelineRegistry] = None) -> None:
        self._registry = registry or PipelineRegistry()

    def execute_pipeline(
        self, pipeline_id: str, input_data: Any
    ) -> Any:
        pipeline = self._registry.get(pipeline_id)
        if pipeline is None:
            raise ValueError(f"Pipeline not found: {pipeline_id}")
        return pipeline.execute(input_data)

    def register_pipeline(self, pipeline: VisionPipeline) -> None:
        self._registry.register(pipeline)

    def list_pipelines(self) -> list[str]:
        return self._registry.list_names()

    def get_pipeline_info(self, pipeline_id: str) -> Optional[dict[str, Any]]:
        pipeline = self._registry.get(pipeline_id)
        if pipeline is None:
            return None
        return pipeline.to_dict()
