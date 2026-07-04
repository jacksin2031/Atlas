# Atlas Vision Runtime Resource Manager

"""
Resource management for frame buffers, caches, and temporary buffers.

Implements LRU eviction, temp buffer TTL, and leak prevention.
"""
from __future__ import annotations

import threading
import time
from collections import OrderedDict
from typing import Any, Optional


class LRUCache:
    """Simple LRU cache with capacity limit."""

    def __init__(self, capacity: int = 100) -> None:
        self._cache: OrderedDict[str, Any] = OrderedDict()
        self._capacity = capacity
        self._lock = threading.Lock()

    def get(self, key: str) -> Any | None:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                return self._cache[key]
            return None

    def put(self, key: str, value: Any) -> None:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = value
            while len(self._cache) > self._capacity:
                self._cache.popitem(last=False)

    def evict_one(self) -> Optional[str]:
        with self._lock:
            if self._cache:
                key, _ = self._cache.popitem(last=False)
                return key
            return None

    def __len__(self) -> int:
        return len(self._cache)

    def __contains__(self, key: str) -> bool:
        return key in self._cache


class TempBuffer:
    """Temporarily managed buffer with TTL."""

    def __init__(self, buffer_id: str, data: Any, ttl_seconds: float = 60.0) -> None:
        self.buffer_id = buffer_id
        self.data = data
        self.created_at = time.monotonic()
        self.ttl_seconds = ttl_seconds

    @property
    def is_expired(self) -> bool:
        return (time.monotonic() - self.created_at) > self.ttl_seconds

    def to_dict(self) -> dict[str, Any]:
        return {
            "buffer_id": self.buffer_id,
            "ttl_seconds": self.ttl_seconds,
            "age_seconds": time.monotonic() - self.created_at,
        }


class VisionResourceManager:
    """Manages frame buffers, caches, and temporary resources."""

    def __init__(self, max_cache_size: int = 1000, max_temp_buffers: int = 500) -> None:
        self._image_cache = LRUCache(max_cache_size)
        self._model_cache = LRUCache(max_cache_size)
        self._temp_buffers: dict[str, TempBuffer] = {}
        self._max_temp_buffers = max_temp_buffers
        self._lock = threading.Lock()
        self._total_allocated = 0
        self._total_freed = 0

    def cache_image(self, key: str, data: Any) -> None:
        self._image_cache.put(key, data)
        with self._lock:
            self._total_allocated += 1

    def get_cached_image(self, key: str) -> Any | None:
        return self._image_cache.get(key)

    def cache_model(self, key: str, data: Any) -> None:
        self._model_cache.put(key, data)
        with self._lock:
            self._total_allocated += 1

    def get_cached_model(self, key: str) -> Any | None:
        return self._model_cache.get(key)

    def allocate_temp_buffer(
        self, buffer_id: str, data: Any, ttl_seconds: float = 60.0
    ) -> None:
        with self._lock:
            if len(self._temp_buffers) >= self._max_temp_buffers:
                self._evict_expired()
            if len(self._temp_buffers) >= self._max_temp_buffers:
                first_key = next(iter(self._temp_buffers))
                del self._temp_buffers[first_key]
            self._temp_buffers[buffer_id] = TempBuffer(buffer_id, data, ttl_seconds)
            self._total_allocated += 1

    def get_temp_buffer(self, buffer_id: str) -> Any | None:
        buf = self._temp_buffers.get(buffer_id)
        if buf is not None and not buf.is_expired:
            return buf.data
        if buf is not None:
            with self._lock:
                self._temp_buffers.pop(buffer_id, None)
                self._total_freed += 1
        return None

    def release_temp_buffer(self, buffer_id: str) -> None:
        with self._lock:
            self._temp_buffers.pop(buffer_id, None)
            self._total_freed += 1

    def _evict_expired(self) -> None:
        expired = [
            k for k, v in self._temp_buffers.items() if v.is_expired
        ]
        for k in expired:
            del self._temp_buffers[k]
            self._total_freed += 1

    def get_stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                "image_cache_size": len(self._image_cache),
                "model_cache_size": len(self._model_cache),
                "temp_buffers": len(self._temp_buffers),
                "total_allocated": self._total_allocated,
                "total_freed": self._total_freed,
            }
