"""Storage abstraction for workflow execution data.

Per RFC-0324 (Workflow Storage). The runtime MUST NOT implement
database-specific logic. This provides a unified interface for:
- Execution snapshots
- Checkpoint persistence
- Execution history
- Recovery metadata
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from atlas_workflow.common import StorageError


class StorageBackend(ABC):
    """Abstract storage backend interface."""

    @abstractmethod
    def save(self, key: str, data: dict[str, Any]) -> bool:
        """Save data to storage."""
        ...

    @abstractmethod
    def load(self, key: str) -> dict[str, Any] | None:
        """Load data from storage."""
        ...

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete data from storage."""
        ...

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if data exists in storage."""
        ...

    @abstractmethod
    def list_keys(self, prefix: str = "") -> list[str]:
        """List all keys with optional prefix filter."""
        ...


class StorageAbstraction:
    """Unified storage abstraction for workflow execution data.

    Routes data to appropriate backends based on entity type.
    Per RFC-0324.
    """

    def __init__(self, backend: StorageBackend | None = None) -> None:
        self._backend = backend
        self._data: dict[str, dict[str, Any]] = {}
        self._initialized = backend is not None

    def initialize(self, backend: StorageBackend) -> None:
        self._backend = backend
        self._initialized = True

    def save_snapshot(self, instance_id: str, snapshot: dict[str, Any]) -> None:
        """Save an execution snapshot."""
        key = f"snapshot:{instance_id}"
        self._store(key, snapshot)

    def load_snapshot(self, instance_id: str) -> dict[str, Any] | None:
        """Load an execution snapshot for recovery."""
        key = f"snapshot:{instance_id}"
        return self._retrieve(key)

    def save_checkpoint(self, instance_id: str, checkpoint_id: str, data: dict[str, Any]) -> None:
        """Save a checkpoint."""
        key = f"checkpoint:{instance_id}:{checkpoint_id}"
        self._store(key, data)

    def load_checkpoint(self, instance_id: str, checkpoint_id: str) -> dict[str, Any] | None:
        """Load a checkpoint."""
        key = f"checkpoint:{instance_id}:{checkpoint_id}"
        return self._retrieve(key)

    def save_history_entry(self, instance_id: str, entry: dict[str, Any]) -> None:
        """Save an execution history entry."""
        key = f"history:{instance_id}:{entry.get('event_type', 'unknown')}:{entry.get('timestamp', '')}"
        self._store(key, entry)

    def load_recovery_metadata(self, instance_id: str) -> dict[str, Any] | None:
        """Load recovery metadata for a workflow instance."""
        key = f"recovery:{instance_id}"
        return self._retrieve(key)

    def save_recovery_metadata(self, instance_id: str, metadata: dict[str, Any]) -> None:
        """Save recovery metadata."""
        key = f"recovery:{instance_id}"
        self._store(key, metadata)

    def delete_instance_data(self, instance_id: str) -> None:
        """Delete all data for an instance."""
        keys_to_delete = [k for k in self._data if k.startswith(f"{instance_id}:") or k.startswith(f"snapshot:{instance_id}") or k.startswith(f"checkpoint:{instance_id}") or k.startswith(f"recovery:{instance_id}") or k.startswith(f"history:{instance_id}")]
        for key in keys_to_delete:
            del self._data[key]

    def list_snapshots(self) -> list[str]:
        """List all snapshot keys."""
        return [k.replace("snapshot:", "") for k in self._data if k.startswith("snapshot:")]

    def list_checkpoints(self, instance_id: str) -> list[str]:
        """List all checkpoint IDs for an instance."""
        prefix = f"checkpoint:{instance_id}:"
        return [k.replace(prefix, "") for k in self._data if k.startswith(prefix)]

    def _store(self, key: str, data: dict[str, Any]) -> None:
        if self._backend:
            if not self._backend.save(key, data):
                raise StorageError(
                    f"Failed to save key {key!r}",
                    operation="save",
                )
        else:
            self._data[key] = dict(data)

    def _retrieve(self, key: str) -> dict[str, Any] | None:
        if self._backend:
            return self._backend.load(key)
        return self._data.get(key)
