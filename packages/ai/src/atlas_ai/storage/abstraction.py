# Atlas AI Runtime Storage Abstraction

"""
Abstract storage for the AI Runtime.
"""
from __future__ import annotations

from enum import Enum
from typing import Any


class StorageDomain(Enum):
    """Storage domain types."""

    PROMPTS = "prompts"
    CONVERSATIONS = "conversations"
    MODEL_METADATA = "model_metadata"
    AGENT_METADATA = "agent_metadata"
    EMBEDDING_METADATA = "embedding_metadata"
    MEMORY_METADATA = "memory_metadata"


class StorageBackend(Enum):
    """Storage backend types (abstract)."""

    IN_MEMORY = "in_memory"
    FILE_SYSTEM = "file_system"
    KEY_VALUE = "key_value"


class AIStorageAdapter:
    """Abstract storage adapter for AI Runtime data."""

    def __init__(self, backend: StorageBackend = StorageBackend.IN_MEMORY) -> None:
        self._backend = backend
        self._data: dict[str, dict[str, Any]] = {}

    def save_prompt(self, prompt_id: str, data: dict[str, Any]) -> None:
        self._save(StorageDomain.PROMPTS, prompt_id, data)

    def load_prompt(self, prompt_id: str) -> dict[str, Any] | None:
        return self._load(StorageDomain.PROMPTS, prompt_id)

    def save_conversation(self, conversation_id: str, data: dict[str, Any]) -> None:
        self._save(StorageDomain.CONVERSATIONS, conversation_id, data)

    def load_conversation(self, conversation_id: str) -> dict[str, Any] | None:
        return self._load(StorageDomain.CONVERSATIONS, conversation_id)

    def save_model_metadata(self, model_id: str, data: dict[str, Any]) -> None:
        self._save(StorageDomain.MODEL_METADATA, model_id, data)

    def load_model_metadata(self, model_id: str) -> dict[str, Any] | None:
        return self._load(StorageDomain.MODEL_METADATA, model_id)

    def save_agent_metadata(self, agent_id: str, data: dict[str, Any]) -> None:
        self._save(StorageDomain.AGENT_METADATA, agent_id, data)

    def load_agent_metadata(self, agent_id: str) -> dict[str, Any] | None:
        return self._load(StorageDomain.AGENT_METADATA, agent_id)

    def save_embedding_metadata(self, embedding_id: str, data: dict[str, Any]) -> None:
        self._save(StorageDomain.EMBEDDING_METADATA, embedding_id, data)

    def load_embedding_metadata(self, embedding_id: str) -> dict[str, Any] | None:
        return self._load(StorageDomain.EMBEDDING_METADATA, embedding_id)

    def save_memory_metadata(self, memory_id: str, data: dict[str, Any]) -> None:
        self._save(StorageDomain.MEMORY_METADATA, memory_id, data)

    def load_memory_metadata(self, memory_id: str) -> dict[str, Any] | None:
        return self._load(StorageDomain.MEMORY_METADATA, memory_id)

    def _save(self, domain: StorageDomain, key: str, data: dict[str, Any]) -> None:
        if domain.value not in self._data:
            self._data[domain.value] = {}
        self._data[domain.value][key] = data

    def _load(self, domain: StorageDomain, key: str) -> dict[str, Any] | None:
        domain_data = self._data.get(domain.value, {})
        return domain_data.get(key)

    def delete(self, domain: StorageDomain, key: str) -> bool:
        domain_data = self._data.get(domain.value, {})
        if key in domain_data:
            del domain_data[key]
            return True
        return False

    def list_keys(self, domain: StorageDomain) -> list[str]:
        domain_data = self._data.get(domain.value, {})
        return list(domain_data.keys())

    def clear(self) -> None:
        self._data.clear()

    def to_dict(self) -> dict[str, Any]:
        return {
            "backend": self._backend.value,
            "domains": {k: list(v.keys()) for k, v in self._data.items()},
        }
