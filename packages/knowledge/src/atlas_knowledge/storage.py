"""Project-scoped storage adapter for Knowledge Runtime."""

from __future__ import annotations

from abc import ABC, abstractmethod
import json
import os
from pathlib import Path
import threading
import uuid
from typing import Any

from .errors import KnowledgeStorageError, KnowledgeValidationError
from .models import KnowledgeEntry, ProjectScope


class KnowledgeStorage(ABC):
    @abstractmethod
    def load(self, scope: ProjectScope) -> list[KnowledgeEntry]:
        raise NotImplementedError

    @abstractmethod
    def save(self, scope: ProjectScope, entries: list[KnowledgeEntry]) -> None:
        raise NotImplementedError


class IncompatibleKnowledgeStorage(KnowledgeStorageError):
    """A source that must never be recovered over or downgraded."""


class JsonProjectKnowledgeStorage(KnowledgeStorage):
    """Atomic dedicated storage under a project's fixed .atlas directory."""

    SCHEMA_VERSION = 1
    FILE_NAME = "knowledge.v1.json"

    def __init__(self) -> None:
        self._lock = threading.RLock()

    def _paths(self, scope: ProjectScope) -> tuple[Path, Path]:
        supplied = Path(scope.project_path)
        for path in (supplied / ".atlas", supplied, *supplied.parents):
            if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
                raise KnowledgeStorageError("Knowledge storage refuses symbolic links or junctions")
        root = supplied.resolve()
        if not root.is_dir():
            raise KnowledgeStorageError("Project directory does not exist")
        data_dir = (root / ".atlas").resolve()
        try:
            data_dir.relative_to(root)
        except ValueError as error:
            raise KnowledgeStorageError("Knowledge storage escaped the project directory") from error
        data_dir.mkdir(parents=True, exist_ok=True)
        primary = data_dir / self.FILE_NAME
        backup = primary.with_suffix(primary.suffix + ".bak")
        for path in (primary, backup):
            if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
                raise KnowledgeStorageError("Knowledge storage refuses redirected files")
        return primary, backup

    @staticmethod
    def _decode(path: Path, scope: ProjectScope) -> list[KnowledgeEntry]:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise KnowledgeStorageError("Knowledge storage must be an object")
        if type(value.get("schemaVersion")) is not int or value.get("schemaVersion") != JsonProjectKnowledgeStorage.SCHEMA_VERSION:
            raise IncompatibleKnowledgeStorage("Unsupported knowledge storage version; open with a compatible Atlas release")
        if value.get("projectId") != scope.project_id:
            raise IncompatibleKnowledgeStorage("Knowledge storage belongs to a different project")
        entries = value.get("entries")
        if not isinstance(entries, list):
            raise KnowledgeStorageError("Knowledge storage entries must be a list")
        if any(not isinstance(item, dict) for item in entries):
            raise KnowledgeStorageError("Every knowledge entry must be an object")
        try:
            decoded = [KnowledgeEntry.from_dict(item) for item in entries]
        except (TypeError, ValueError, KnowledgeValidationError) as error:
            raise KnowledgeStorageError("Knowledge storage contains an invalid entry") from error
        if any(item.project_id != scope.project_id for item in decoded):
            raise IncompatibleKnowledgeStorage("Knowledge entry belongs to a different project")
        if len({item.id for item in decoded}) != len(decoded):
            raise KnowledgeStorageError("Knowledge storage contains duplicate entry identifiers")
        return decoded

    def load(self, scope: ProjectScope) -> list[KnowledgeEntry]:
        with self._lock:
            primary, backup = self._paths(scope)
            if not primary.exists() and not backup.exists():
                return []
            try:
                return self._decode(primary, scope)
            except IncompatibleKnowledgeStorage:
                raise
            except (OSError, ValueError, KnowledgeStorageError) as primary_error:
                try:
                    recovered = self._decode(backup, scope)
                    # Recovery is read-only; the next validated save repairs primary.
                    return recovered
                except (OSError, ValueError, KnowledgeStorageError) as backup_error:
                    raise KnowledgeStorageError(
                        f"Unable to read primary or backup knowledge storage: {primary_error}; {backup_error}"
                    ) from backup_error

    def save(self, scope: ProjectScope, entries: list[KnowledgeEntry]) -> None:
        with self._lock:
            primary, backup = self._paths(scope)
            previous = None
            for candidate in (primary, backup):
                if candidate.exists():
                    try:
                        decoded = self._decode(candidate, scope)
                        if candidate == primary:
                            previous = candidate.read_bytes()
                    except IncompatibleKnowledgeStorage:
                        raise
                    except (OSError, ValueError, KnowledgeStorageError):
                        if candidate == primary and (not backup.exists()):
                            raise KnowledgeStorageError("Corrupt knowledge has no recovery backup; original preserved")
                        if candidate == backup and previous is None:
                            raise KnowledgeStorageError("No valid knowledge recovery source; original preserved")
            if any(entry.project_id != scope.project_id for entry in entries):
                raise KnowledgeStorageError("Cannot persist knowledge from another project")
            value: dict[str, Any] = {
                "schemaVersion": self.SCHEMA_VERSION,
                "projectId": scope.project_id,
                "entries": [entry.to_dict() for entry in sorted(entries, key=lambda item: item.id)],
            }
            temporary = primary.parent / f".{self.FILE_NAME}.{uuid.uuid4().hex}.tmp"
            try:
                with temporary.open("x", encoding="utf-8", newline="\n") as stream:
                    json.dump(value, stream, ensure_ascii=False, indent=2)
                    stream.flush()
                    os.fsync(stream.fileno())
                if previous is not None:
                    backup_temporary = backup.with_name(f".{backup.name}.{uuid.uuid4().hex}.tmp")
                    try:
                        with backup_temporary.open("xb") as stream:
                            stream.write(previous)
                            stream.flush()
                            os.fsync(stream.fileno())
                        os.replace(backup_temporary, backup)
                    finally:
                        backup_temporary.unlink(missing_ok=True)
                os.replace(temporary, primary)
            except OSError as error:
                temporary.unlink(missing_ok=True)
                raise KnowledgeStorageError(f"Unable to persist project knowledge: {error}") from error
