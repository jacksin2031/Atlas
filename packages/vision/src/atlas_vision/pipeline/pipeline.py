# Atlas Vision Runtime Pipeline

"""
Deterministic Vision Pipeline with composable stages.

Pipelines execute stages in a fixed order:
Acquire -> Decode -> Normalize -> Crop -> Resize -> Rotate -> Scale -> Convert -> Filter -> Analyze -> Export
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

from atlas_vision.errors import PipelineExecutionError, PipelineValidationError


class PipelineStage(Enum):
    """Ordered pipeline stages."""

    ACQUIRE = "acquire"
    DECODE = "decode"
    NORMALIZE = "normalize"
    CROP = "crop"
    RESIZE = "resize"
    ROTATE = "rotate"
    SCALE = "scale"
    CONVERT = "convert"
    FILTER = "filter"
    ANALYZE = "analyze"
    EXPORT = "export"

    @classmethod
    def ordered_list(cls) -> list["PipelineStage"]:
        return [
            cls.ACQUIRE,
            cls.DECODE,
            cls.NORMALIZE,
            cls.CROP,
            cls.RESIZE,
            cls.ROTATE,
            cls.SCALE,
            cls.CONVERT,
            cls.FILTER,
            cls.ANALYZE,
            cls.EXPORT,
        ]


@dataclass(frozen=True, slots=True, eq=True)
class PipelineStageDef:
    """Definition of a single pipeline stage."""

    stage: PipelineStage
    handler: Callable[..., Any]
    config: dict[str, Any] = field(default_factory=dict)
    optional: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage.value,
            "config": dict(self.config),
            "optional": self.optional,
        }


class VisionPipeline:
    """Deterministic composable pipeline."""

    def __init__(self, pipeline_id: str = "") -> None:
        self.pipeline_id = pipeline_id or str(uuid.uuid4())
        self._stages: dict[PipelineStage, PipelineStageDef] = {}
        self._order: list[PipelineStage] = []
        self._running = False
        self._frames_processed = 0

    def add_stage(
        self,
        stage: PipelineStage,
        handler: Callable[..., Any],
        config: dict[str, Any] | None = None,
        optional: bool = False,
    ) -> None:
        if stage in self._stages:
            raise PipelineValidationError(
                f"Stage {stage.value} already registered", self.pipeline_id
            )
        self._stages[stage] = PipelineStageDef(
            stage=stage, handler=handler, config=config or {}, optional=optional
        )
        self._order = PipelineStage.ordered_list()

    def remove_stage(self, stage: PipelineStage) -> None:
        if stage in self._stages:
            del self._stages[stage]

    def validate(self) -> bool:
        required = [PipelineStage.ACQUIRE, PipelineStage.EXPORT]
        for req in required:
            if req not in self._stages:
                raise PipelineValidationError(
                    f"Missing required stage: {req.value}", self.pipeline_id
                )
        return True

    def execute(self, frame_data: Any) -> Any:
        self.validate()
        self._running = True
        result = frame_data
        try:
            for stage in self._order:
                if stage not in self._stages:
                    continue
                handler = self._stages[stage].handler
                try:
                    result = handler(result, **self._stages[stage].config)
                    self._frames_processed += 1
                except Exception as exc:
                    if not self._stages[stage].optional:
                        raise PipelineExecutionError(
                            f"Stage {stage.value} failed",
                            self.pipeline_id,
                            stage.value,
                        ) from exc
        finally:
            self._running = False
        return result

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def frames_processed(self) -> int:
        return self._frames_processed

    def get_stages(self) -> list[str]:
        return [s.value for s in self._order if s in self._stages]

    def to_dict(self) -> dict[str, Any]:
        return {
            "pipeline_id": self.pipeline_id,
            "stages": [s.to_dict() for s in self._stages.values()],
            "frames_processed": self._frames_processed,
        }
