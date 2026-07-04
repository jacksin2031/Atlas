# Atlas AI Runtime Resources

"""
Resource management for the AI Runtime.

Tracks model memory, embedding cache, prompt cache,
conversation cache, agent resources, inference queue,
temporary buffers. Prevents leaks.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TempBuffer:
    """Temporary buffer for inference data."""

    buffer_id: str
    data: bytes = field(default_factory=bytes)
    size_bytes: int = 0
    created_at: float = 0.0

    def __post_init__(self) -> None:
        import time
        if self.size_bytes == 0:
            self.size_bytes = len(self.data)
        if self.created_at == 0.0:
            self.created_at = time.monotonic()


class LRUCache:
    """Simple LRU cache for AI resources."""

    def __init__(self, max_size: int = 1000) -> None:
        self._cache: dict[str, Any] = {}
        self._order: list[str] = []
        self._max_size = max_size

    def get(self, key: str) -> Any | None:
        if key in self._cache:
            self._order.remove(key)
            self._order.append(key)
            return self._cache[key]
        return None

    def put(self, key: str, value: Any) -> None:
        if key in self._cache:
            self._order.remove(key)
        elif len(self._order) >= self._max_size:
            oldest = self._order.pop(0)
            del self._cache[oldest]
        self._cache[key] = value
        self._order.append(key)

    def remove(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            self._order.remove(key)
            return True
        return False

    def clear(self) -> None:
        self._cache.clear()
        self._order.clear()

    @property
    def size(self) -> int:
        return len(self._cache)


class AIResourceManager:
    """Manages AI runtime resources."""

    def __init__(self) -> None:
        self._model_memory: dict[str, int] = {}
        self._embedding_cache = LRUCache()
        self._prompt_cache = LRUCache()
        self._conversation_cache = LRUCache()
        self._agent_buffers: dict[str, TempBuffer] = {}
        self._inference_queue_size: int = 0
        self._temp_buffers: dict[str, TempBuffer] = {}
        self._total_allocated = 0

    def allocate_model_memory(self, model_id: str, bytes_: int) -> None:
        self._model_memory[model_id] = bytes_
        self._total_allocated += bytes_

    def release_model_memory(self, model_id: str) -> int:
        freed = self._model_memory.pop(model_id, 0)
        self._total_allocated -= freed
        return freed

    def cache_embedding(self, key: str, value: Any) -> None:
        self._embedding_cache.put(key, value)

    def cache_prompt(self, key: str, value: Any) -> None:
        self._prompt_cache.put(key, value)

    def cache_conversation(self, key: str, value: Any) -> None:
        self._conversation_cache.put(key, value)

    def create_temp_buffer(self, buffer_id: str, data: bytes) -> TempBuffer:
        buf = TempBuffer(buffer_id=buffer_id, data=data)
        self._temp_buffers[buffer_id] = buf
        return buf

    def release_temp_buffer(self, buffer_id: str) -> bool:
        return self._temp_buffers.pop(buffer_id, None) is not None

    def track_inference_queue(self, delta: int) -> None:
        self._inference_queue_size += delta

    def get_model_memory(self, model_id: str) -> int:
        return self._model_memory.get(model_id, 0)

    def get_total_allocated(self) -> int:
        return self._total_allocated

    def get_embedding_cache_size(self) -> int:
        return self._embedding_cache.size

    def get_prompt_cache_size(self) -> int:
        return self._prompt_cache.size

    def get_conversation_cache_size(self) -> int:
        return self._conversation_cache.size

    def cleanup(self) -> None:
        self._embedding_cache.clear()
        self._prompt_cache.clear()
        self._conversation_cache.clear()
        self._temp_buffers.clear()
        self._model_memory.clear()
        self._total_allocated = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_memory": dict(self._model_memory),
            "embedding_cache_size": self._embedding_cache.size,
            "prompt_cache_size": self._prompt_cache.size,
            "conversation_cache_size": self._conversation_cache.size,
            "temp_buffers": len(self._temp_buffers),
            "inference_queue_size": self._inference_queue_size,
            "total_allocated": self._total_allocated,
        }
