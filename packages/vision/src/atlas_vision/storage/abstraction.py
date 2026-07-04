# Atlas Vision Runtime Storage Abstraction

"""
Abstract storage backend for Vision Runtime persistence.

Supports abstract persistence of pipeline definitions,
vision settings, provider metadata, capture configuration,
and model metadata. Does NOT implement specific databases.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional


class StorageDomain(Enum):
    """Storage domains."""

    PIPELINES = "pipelines"
    SETTINGS = "settings"
    PROVIDER_METADATA = "provider_metadata"
    CAPTURE_CONFIG = "capture_config"
    MODEL_METADATA = "model_metadata"


class StorageBackend(ABC):
    """Abstract storage backend interface."""

    @abstractmethod
    def save(self, domain: StorageDomain, key: str, data: dict[str, Any]) -> None:
        ...

    @abstractmethod
    def load(self, domain: StorageDomain, key: str) -> Optional[dict[str, Any]]:
        ...

    @abstractmethod
    def delete(self, domain: StorageDomain, key: str) -> bool:
        ...

    @abstractmethod
    def list_keys(self, domain: StorageDomain) -> list[str]:
        ...

    @abstractmethod
    def exists(self, domain: StorageDomain, key: str) -> bool:
        ...


class VisionStorageAdapter:
    """Adapts storage backends for Vision Runtime domains."""

    def __init__(self, backend: Optional[StorageBackend] = None) -> None:
        self._backend = backend
        self._data: dict[str, dict[str, dict[str, Any]]] = {}

    def _ensure_domain(self, domain: StorageDomain) -> None:
        if domain.value not in self._data:
            self._data[domain.value] = {}

    def save_pipeline(self, pipeline_id: str, data: dict[str, Any]) -> None:
        self._ensure_domain(StorageDomain.PIPELINES)
        self._data[StorageDomain.PIPELINES.value][pipeline_id] = data
        if self._backend is not None:
            self._backend.save(StorageDomain.PIPELINES, pipeline_id, data)

    def load_pipeline(self, pipeline_id: str) -> Optional[dict[str, Any]]:
        if self._backend is not None:
            return self._backend.load(StorageDomain.PIPELINES, pipeline_id)
        self._ensure_domain(StorageDomain.PIPELINES)
        return self._data.get(StorageDomain.PIPELINES.value, {}).get(pipeline_id)

    def save_settings(self, key: str, data: dict[str, Any]) -> None:
        self._ensure_domain(StorageDomain.SETTINGS)
        self._data[StorageDomain.SETTINGS.value][key] = data
        if self._backend is not None:
            self._backend.save(StorageDomain.SETTINGS, key, data)

    def load_settings(self, key: str) -> Optional[dict[str, Any]]:
        if self._backend is not None:
            return self._backend.load(StorageDomain.SETTINGS, key)
        self._ensure_domain(StorageDomain.SETTINGS)
        return self._data.get(StorageDomain.SETTINGS.value, {}).get(key)

    def save_provider_metadata(
        self, provider_id: str, data: dict[str, Any]
    ) -> None:
        self._ensure_domain(StorageDomain.PROVIDER_METADATA)
        self._data[StorageDomain.PROVIDER_METADATA.value][provider_id] = data
        if self._backend is not None:
            self._backend.save(
                StorageDomain.PROVIDER_METADATA, provider_id, data
            )

    def load_provider_metadata(
        self, provider_id: str
    ) -> Optional[dict[str, Any]]:
        if self._backend is not None:
            return self._backend.load(
                StorageDomain.PROVIDER_METADATA, provider_id
            )
        self._ensure_domain(StorageDomain.PROVIDER_METADATA)
        return self._data.get(StorageDomain.PROVIDER_METADATA.value, {}).get(
            provider_id
        )

    def save_capture_config(
        self, source_id: str, data: dict[str, Any]
    ) -> None:
        self._ensure_domain(StorageDomain.CAPTURE_CONFIG)
        self._data[StorageDomain.CAPTURE_CONFIG.value][source_id] = data
        if self._backend is not None:
            self._backend.save(StorageDomain.CAPTURE_CONFIG, source_id, data)

    def load_capture_config(
        self, source_id: str
    ) -> Optional[dict[str, Any]]:
        if self._backend is not None:
            return self._backend.load(StorageDomain.CAPTURE_CONFIG, source_id)
        self._ensure_domain(StorageDomain.CAPTURE_CONFIG)
        return self._data.get(StorageDomain.CAPTURE_CONFIG.value, {}).get(
            source_id
        )

    def save_model_metadata(
        self, model_id: str, data: dict[str, Any]
    ) -> None:
        self._ensure_domain(StorageDomain.MODEL_METADATA)
        self._data[StorageDomain.MODEL_METADATA.value][model_id] = data
        if self._backend is not None:
            self._backend.save(
                StorageDomain.MODEL_METADATA, model_id, data
            )

    def load_model_metadata(
        self, model_id: str
    ) -> Optional[dict[str, Any]]:
        if self._backend is not None:
            return self._backend.load(StorageDomain.MODEL_METADATA, model_id)
        self._ensure_domain(StorageDomain.MODEL_METADATA)
        return self._data.get(StorageDomain.MODEL_METADATA.value, {}).get(
            model_id
        )
