"""Canonical immutable models for mutable project knowledge."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any

from .errors import KnowledgeValidationError

_PROJECT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")
_ENTRY_TYPES = {"note", "document", "fact", "observation"}
_SENSITIVE_KEYS = {"apikey", "authorization", "bearer", "credential", "password", "secret", "token"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalized_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _assert_safe_metadata(value: Any, path: str = "metadata") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if _normalized_key(str(key)) in _SENSITIVE_KEYS:
                raise KnowledgeValidationError(f"Credential-shaped field is not allowed at {path}.{key}")
            _assert_safe_metadata(item, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _assert_safe_metadata(item, f"{path}[{index}]")
    try:
        json.dumps(value)
    except (TypeError, ValueError) as error:
        raise KnowledgeValidationError(f"{path} must be JSON serializable") from error


@dataclass(frozen=True, slots=True)
class ProjectScope:
    project_id: str
    project_path: str

    def __post_init__(self) -> None:
        if not _PROJECT_ID.fullmatch(self.project_id):
            raise KnowledgeValidationError("project_id must be a safe non-empty identifier")
        path = Path(self.project_path)
        if not self.project_path or not path.is_absolute():
            raise KnowledgeValidationError("project_path must be an absolute project directory")


@dataclass(frozen=True, slots=True)
class KnowledgeReference:
    entry_id: str
    project_id: str
    entry_type: str
    title: str
    source_type: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class KnowledgeEntry:
    id: str
    project_id: str
    type: str
    title: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: tuple[str, ...] = field(default_factory=tuple)
    source: dict[str, Any] = field(default_factory=lambda: {"type": "user"})
    provenance: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)
    version: int = 1

    def __post_init__(self) -> None:
        if not self.id or len(self.id) > 200:
            raise KnowledgeValidationError("id is required and must be at most 200 characters")
        if not _PROJECT_ID.fullmatch(self.project_id):
            raise KnowledgeValidationError("project_id must be a safe non-empty identifier")
        if self.type not in _ENTRY_TYPES:
            raise KnowledgeValidationError(f"Unsupported knowledge type: {self.type}")
        if not self.title.strip() or len(self.title) > 500:
            raise KnowledgeValidationError("title is required and must be at most 500 characters")
        if not isinstance(self.content, str) or len(self.content) > 2_000_000:
            raise KnowledgeValidationError("content must be text no larger than 2 MB")
        if self.version < 1:
            raise KnowledgeValidationError("version must be positive")
        _assert_safe_metadata(self.metadata)
        _assert_safe_metadata(self.source, "source")
        _assert_safe_metadata(self.provenance, "provenance")

    @property
    def reference(self) -> KnowledgeReference:
        return KnowledgeReference(
            entry_id=self.id,
            project_id=self.project_id,
            entry_type=self.type,
            title=self.title,
            source_type=str(self.source.get("type", "unknown")),
        )

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["tags"] = list(self.tags)
        return value

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "KnowledgeEntry":
        return cls(
            id=str(value.get("id", "")),
            project_id=str(value.get("project_id", value.get("projectId", ""))),
            type=str(value.get("type", "note")),
            title=str(value.get("title", "")),
            content=str(value.get("content", "")),
            metadata=dict(value.get("metadata") or {}),
            tags=tuple(str(tag) for tag in value.get("tags") or ()),
            source=dict(value.get("source") or {"type": "user"}),
            provenance=dict(value.get("provenance") or {}),
            created_at=str(value.get("created_at", value.get("createdAt", now_iso()))),
            updated_at=str(value.get("updated_at", value.get("updatedAt", now_iso()))),
            version=int(value.get("version", 1)),
        )


@dataclass(frozen=True, slots=True)
class KnowledgeSearchResult:
    entry: KnowledgeEntry
    reference: KnowledgeReference
    excerpt: str
    score: float
    matched_terms: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry": self.entry.to_dict(),
            "reference": self.reference.to_dict(),
            "excerpt": self.excerpt,
            "score": self.score,
            "matched_terms": list(self.matched_terms),
        }


@dataclass(frozen=True, slots=True)
class KnowledgeEvent:
    event_id: str
    event_type: str
    project_id: str
    timestamp: str
    entry_id: str | None = None
    correlation_id: str | None = None
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

