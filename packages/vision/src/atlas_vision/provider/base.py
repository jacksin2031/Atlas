# Atlas Vision Runtime Provider Base

"""
Abstract provider interface for vision processing.

All vision providers (OCR, Detection, Classification, etc.)
must implement VisionProviderABC.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional


class ProviderType(Enum):
    """Types of vision providers."""

    OCR = "ocr"
    DETECTION = "detection"
    CLASSIFICATION = "classification"
    SEGMENTATION = "segmentation"
    TEMPLATE_MATCHING = "template_matching"
    FEATURE_MATCHING = "feature_matching"
    MOTION_DETECTION = "motion_detection"


class ProviderResult:
    """Immutable result from provider execution."""

    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.success = success
        self.data = data
        self.error = error
        self.metadata = metadata or {}

    @property
    def is_success(self) -> bool:
        return self.success and not self.error

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "error": self.error,
            "metadata": dict(self.metadata),
        }


class VisionProvider(ABC):
    """Abstract base class for vision providers."""

    @property
    @abstractmethod
    def provider_id(self) -> str:
        ...

    @property
    @abstractmethod
    def provider_type(self) -> ProviderType:
        ...

    @abstractmethod
    def initialize(self) -> None:
        ...

    @abstractmethod
    def execute(self, input_data: Any) -> ProviderResult:
        ...

    @abstractmethod
    def shutdown(self) -> None:
        ...

    @abstractmethod
    def health_check(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_capabilities(self) -> list[str]:
        ...

    @abstractmethod
    def is_compatible(self, version: str) -> bool:
        ...
