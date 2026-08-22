# Atlas AI Runtime Embeddings

"""
Embedding runtime for the AI Runtime.

Supports EmbeddingProvider, EmbeddingModel, EmbeddingRequest,
EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass(frozen=True, slots=True, eq=True)
class EmbeddingModel:
    """Embedding model descriptor."""

    model_id: str
    name: str
    provider_id: str = ""
    dimension: int = 1536
    version: str = "1.0.0"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "name": self.name,
            "provider_id": self.provider_id,
            "dimension": self.dimension,
            "version": self.version,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True, eq=True)
class EmbeddingRequest:
    """Request to generate embeddings."""

    texts: list[str]
    model_id: str
    normalize: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "texts": list(self.texts),
            "model_id": self.model_id,
            "normalize": self.normalize,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True, eq=True)
class EmbeddingResponse:
    """Response from embedding generation."""

    embedding_id: str
    model_id: str
    vectors: list[list[float]] = field(default_factory=list)
    text_count: int = 0
    usage: dict[str, int] = field(default_factory=dict)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "embedding_id": self.embedding_id,
            "model_id": self.model_id,
            "vector_count": len(self.vectors),
            "text_count": self.text_count,
            "usage": dict(self.usage),
            "created_at": self.created_at.isoformat(),
        }


@dataclass(frozen=True, slots=True, eq=True)
class EmbeddingIndex:
    """Vector index entry."""

    entry_id: str
    embedding_id: str
    text: str
    vector: list[float] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "embedding_id": self.embedding_id,
            "text": self.text,
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }


class EmbeddingStore:
    """Stores and retrieves embeddings."""

    def __init__(self) -> None:
        self._entries: dict[str, EmbeddingIndex] = {}
        self._by_embedding: dict[str, list[str]] = {}

    def add(self, entry: EmbeddingIndex) -> None:
        self._entries[entry.entry_id] = entry
        by_emb = self._by_embedding.setdefault(entry.embedding_id, [])
        if entry.entry_id not in by_emb:
            by_emb.append(entry.entry_id)

    def get(self, entry_id: str) -> Optional[EmbeddingIndex]:
        return self._entries.get(entry_id)

    def query_by_embedding(self, embedding_id: str) -> list[EmbeddingIndex]:
        ids = self._by_embedding.get(embedding_id, [])
        return [self._entries[i] for i in ids if i in self._entries]

    def remove(self, entry_id: str) -> bool:
        if entry_id in self._entries:
            entry = self._entries.pop(entry_id)
            by_emb = self._by_embedding.get(entry.embedding_id, [])
            if entry_id in by_emb:
                by_emb.remove(entry_id)
            return True
        return False

    def count(self) -> int:
        return len(self._entries)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_entries": len(self._entries),
            "embedding_groups": len(self._by_embedding),
        }


class EmbeddingRegistry:
    """Registry for embedding models and stores."""

    def __init__(self) -> None:
        self._models: dict[str, EmbeddingModel] = {}
        self._stores: dict[str, EmbeddingStore] = {}

    def register_model(self, model: EmbeddingModel) -> None:
        self._models[model.model_id] = model

    def get_model(self, model_id: str) -> Optional[EmbeddingModel]:
        return self._models.get(model_id)

    def register_store(self, store_id: str, store: EmbeddingStore) -> None:
        self._stores[store_id] = store

    def get_store(self, store_id: str) -> Optional[EmbeddingStore]:
        return self._stores.get(store_id)

    def list_models(self) -> list[str]:
        return list(self._models.keys())

    def list_stores(self) -> list[str]:
        return list(self._stores.keys())

    def to_dict(self) -> dict[str, Any]:
        return {
            "models": list(self._models.keys()),
            "stores": list(self._stores.keys()),
        }


class EmbeddingProvider:
    """Abstract embedding provider interface."""

    def generate(self, request: EmbeddingRequest) -> EmbeddingResponse:
        import uuid
        response = EmbeddingResponse(
            embedding_id=str(uuid.uuid4()),
            model_id=request.model_id,
            text_count=len(request.texts),
            usage={"tokens": len(request.texts)},
        )
        for text in request.texts:
            vec = [hash(t) % 10000 / 10000.0 for t in text[:50]]
            while len(vec) < request.model.dimension:
                vec.append(0.0)
            response.vectors.append(vec[:request.model.dimension])
        return response
