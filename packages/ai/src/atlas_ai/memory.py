# Atlas AI Runtime Memory

"""
Memory management runtime for the AI Runtime.

Supports MemoryStore, MemoryItem, MemoryScope, MemoryContext,
MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy.
No database implementation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class MemoryScope(Enum):
    """Memory scope levels."""

    SESSION = "session"
    WORKSPACE = "workspace"
    PROJECT = "project"
    GLOBAL = "global"


@dataclass(frozen=True, slots=True, eq=True)
class MemoryItem:
    """A single memory item."""

    memory_id: str
    content: str
    scope: MemoryScope = MemoryScope.SESSION
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, Any] = field(default_factory=dict)
    embedding_id: Optional[str] = None
    ttl_seconds: Optional[int] = None

    def is_expired(self) -> bool:
        if self.ttl_seconds is None:
            return False
        age = (datetime.now(timezone.utc) - self.updated_at).total_seconds()
        return age > self.ttl_seconds

    def to_dict(self) -> dict[str, Any]:
        return {
            "memory_id": self.memory_id,
            "content": self.content,
            "scope": self.scope.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": dict(self.metadata),
            "embedding_id": self.embedding_id,
            "ttl_seconds": self.ttl_seconds,
        }


@dataclass(frozen=True, slots=True, eq=True)
class MemoryContext:
    """Context for memory operations."""

    session_id: str = ""
    workspace_id: str = ""
    project_id: str = ""
    scope: MemoryScope = MemoryScope.SESSION
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "workspace_id": self.workspace_id,
            "project_id": self.project_id,
            "scope": self.scope.value,
            "extra": dict(self.extra),
        }


@dataclass(frozen=True, slots=True, eq=True)
class MemorySnapshot:
    """Snapshot of memory state at a point in time."""

    snapshot_id: str
    items: dict[str, MemoryItem]
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "items": {k: v.to_dict() for k, v in self.items.items()},
            "created_at": self.created_at.isoformat(),
        }


@dataclass(frozen=True, slots=True, eq=True)
class MemoryQuery:
    """A memory query specification."""

    scope: Optional[MemoryScope] = None
    session_id: Optional[str] = None
    project_id: Optional[str] = None
    metadata_filter: dict[str, Any] = field(default_factory=dict)
    limit: int = 100
    offset: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "scope": self.scope.value if self.scope else None,
            "session_id": self.session_id,
            "project_id": self.project_id,
            "metadata_filter": dict(self.metadata_filter),
            "limit": self.limit,
            "offset": self.offset,
        }


@dataclass
class MemoryPolicy:
    """Policy for memory management."""

    max_items_per_scope: dict[MemoryScope, int] = field(default_factory=dict)
    default_ttl_seconds: Optional[int] = None
    auto_cleanup: bool = True
    eviction_policy: str = "lru"

    def __post_init__(self) -> None:
        if not self.max_items_per_scope:
            object.__setattr__(
                self,
                "max_items_per_scope",
                {
                    MemoryScope.SESSION: 1000,
                    MemoryScope.WORKSPACE: 5000,
                    MemoryScope.PROJECT: 10000,
                    MemoryScope.GLOBAL: 50000,
                },
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_items_per_scope": {
                k.value: v for k, v in self.max_items_per_scope.items()
            },
            "default_ttl_seconds": self.default_ttl_seconds,
            "auto_cleanup": self.auto_cleanup,
            "eviction_policy": self.eviction_policy,
        }


class MemoryStore:
    """In-memory store for AI memory items."""

    def __init__(self, policy: Optional[MemoryPolicy] = None) -> None:
        self._items: dict[str, MemoryItem] = {}
        self._policy = policy or MemoryPolicy()

    def store(self, item: MemoryItem) -> None:
        self._items[item.memory_id] = item

    def retrieve(self, memory_id: str) -> Optional[MemoryItem]:
        item = self._items.get(memory_id)
        if item and item.is_expired():
            self.remove(memory_id)
            return None
        return item

    def query(self, query: MemoryQuery) -> list[MemoryItem]:
        results = []
        for item in self._items.values():
            if item.is_expired():
                continue
            if query.scope and item.scope != query.scope:
                continue
            if query.session_id and item.metadata.get("session_id") != query.session_id:
                continue
            if query.project_id and item.metadata.get("project_id") != query.project_id:
                continue
            for k, v in query.metadata_filter.items():
                if item.metadata.get(k) != v:
                    break
            else:
                results.append(item)
                if len(results) >= query.limit:
                    break
        return results[query.offset:]

    def remove(self, memory_id: str) -> bool:
        return self._items.pop(memory_id, None) is not None

    def snapshot(self, snapshot_id: str) -> MemorySnapshot:
        return MemorySnapshot(
            snapshot_id=snapshot_id,
            items=dict(self._items),
        )

    def restore(self, snapshot: MemorySnapshot) -> None:
        self._items.update(snapshot.items)

    def cleanup_expired(self) -> int:
        expired = [
            mid for mid, item in self._items.items() if item.is_expired()
        ]
        for mid in expired:
            del self._items[mid]
        return len(expired)

    def count(self, scope: Optional[MemoryScope] = None) -> int:
        if scope is None:
            return len(self._items)
        return sum(
            1 for item in self._items.values() if item.scope == scope
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_items": len(self._items),
            "policy": self._policy.to_dict(),
        }


class MemoryRegistry:
    """Registry for memory stores and snapshots."""

    def __init__(self) -> None:
        self._stores: dict[str, MemoryStore] = {}
        self._snapshots: dict[str, MemorySnapshot] = {}

    def register_store(self, store_id: str, store: MemoryStore) -> None:
        self._stores[store_id] = store

    def get_store(self, store_id: str) -> Optional[MemoryStore]:
        return self._stores.get(store_id)

    def take_snapshot(self, store_id: str, snapshot_id: str) -> None:
        store = self._stores.get(store_id)
        if store:
            self._snapshots[snapshot_id] = store.snapshot(snapshot_id)

    def restore_snapshot(self, store_id: str, snapshot_id: str) -> bool:
        snapshot = self._snapshots.get(snapshot_id)
        if snapshot:
            store = self._stores.get(store_id)
            if store:
                store.restore(snapshot)
                return True
        return False

    def list_stores(self) -> list[str]:
        return list(self._stores.keys())

    def to_dict(self) -> dict[str, Any]:
        return {
            "stores": list(self._stores.keys()),
            "snapshots": list(self._snapshots.keys()),
        }
