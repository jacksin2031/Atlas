"""Project-scoped storage adapter for Knowledge Runtime."""

from __future__ import annotations

from abc import ABC, abstractmethod
import json
import os
from pathlib import Path
import shutil
import threading
import uuid
from typing import Any

from .errors import KnowledgeStorageError
from .models import KnowledgeEntry, ProjectScope


class KnowledgeStorage(ABC):
    @abstractmethod
    def load(self, scope: ProjectScope) -> list[KnowledgeEntry]:
        raise NotImplementedError

    @abstractmethod
    def save(self, scope: ProjectScope, entries: list[KnowledgeEntry]) -> None:
        raise NotImplementedError


class JsonProjectKnowledgeStorage(KnowledgeStorage):
    """Atomic dedicated storage under a project's fixed .atlas directory."""

    SCHEMA_VERSION = 1
    FILE_NAME = "knowledge.v1.json"

    def __init__(self) -> None:
        self._lock = threading.RLock()

    def _paths(self, scope: ProjectScope) -> tuple[Path, Path]:
        root = Path(scope.project_path).resolve()
        if not root.is_dir():
            raise KnowledgeStorageError("Project directory does not exist")
        data_dir = (root / ".atlas").resolve()
        try:
            data_dir.relative_to(root)
        except ValueError as error:
            raise KnowledgeStorageError("Knowledge storage escaped the project directory") from error
        data_dir.mkdir(parents=True, exist_ok=True)
        primary = data_dir / self.FILE_NAME
        return primary, primary.with_suffix(primary.suffix + ".bak")

    @staticmethod
    def _decode(path: Path, scope: ProjectScope) -> list[KnowledgeEntry]:
        value = json.loads(path.read_text(encoding="utf-8"))
        if value.get("schemaVersion") != JsonProjectKnowledgeStorage.SCHEMA_VERSION:
            raise KnowledgeStorageError("Unsupported knowledge storage version")
        if value.get("projectId") != scope.project_id:
            raise KnowledgeStorageError("Knowledge storage belongs to a different project")
        entries = value.get("entries")
        if not isinstance(entries, list):
            raise KnowledgeStorageError("Knowledge storage entries must be a list")
        return [KnowledgeEntry.from_dict(item) for item in entries if isinstance(item, dict)]

    def load(self, scope: ProjectScope) -> list[KnowledgeEntry]:
        with self._lock:
            primary, backup = self._paths(scope)
            if not primary.exists() and not backup.exists():
                return []
            try:
                return self._decode(primary, scope)
            except (OSError, ValueError, KnowledgeStorageError) as primary_error:
                try:
                    recovered = self._decode(backup, scope)
                    shutil.copy2(backup, primary)
                    return recovered
                except (OSError, ValueError, KnowledgeStorageError) as backup_error:
                    raise KnowledgeStorageError(
                        f"Unable to read primary or backup knowledge storage: {primary_error}; {backup_error}"
                    ) from backup_error

    def save(self, scope: ProjectScope, entries: list[KnowledgeEntry]) -> None:
        with self._lock:
            primary, backup = self._paths(scope)
            if any(entry.project_id != scope.project_id for entry in entries):
                raise KnowledgeStorageError("Cannot persist knowledge from another project")
            value: dict[str, Any] = {
                "schemaVersion": self.SCHEMA_VERSION,
                "projectId": scope.project_id,
                "entries": [entry.to_dict() for entry in sorted(entries, key=lambda item: item.id)],
            }
            temporary = primary.parent / f".{self.FILE_NAME}.{uuid.uuid4().hex}.tmp"
            try:
                with temporary.open("w", encoding="utf-8", newline="\n") as stream:
                    json.dump(value, stream, ensure_ascii=False, indent=2)
                    stream.flush()
                    os.fsync(stream.fileno())
                if primary.exists():
                    shutil.copy2(primary, backup)
                os.replace(temporary, primary)
            except OSError as error:
                temporary.unlink(missing_ok=True)
                raise KnowledgeStorageError(f"Unable to persist project knowledge: {error}") from error
