# Atlas Vision Runtime Model Registry

"""
Model metadata registry for vision providers.
"""
from __future__ import annotations

from typing import Any


class ModelRegistry:
    """Registry for model metadata and version tracking."""

    def __init__(self) -> None:
        self._models: dict[str, dict[str, Any]] = {}

    def register(
        self,
        model_id: str,
        model_type: str,
        version: str = "1.0.0",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self._models[model_id] = {
            "type": model_type,
            "version": version,
            "metadata": metadata or {},
        }

    def get(self, model_id: str) -> dict[str, Any] | None:
        return self._models.get(model_id)

    def list_models(self) -> list[str]:
        return list(self._models.keys())
