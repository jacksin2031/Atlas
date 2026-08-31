"""Authoritative project Knowledge Runtime."""

from __future__ import annotations

import csv
from dataclasses import replace
from hashlib import sha256
from io import StringIO
import json
import re
import threading
import time
import uuid
from typing import Any, Callable

from .errors import KnowledgeNotFoundError, KnowledgeValidationError
from .models import KnowledgeEntry, KnowledgeEvent, KnowledgeSearchResult, ProjectScope, now_iso
from .storage import JsonProjectKnowledgeStorage, KnowledgeStorage

_TERM = re.compile(r"[\w-]+", re.UNICODE)
_SUPPORTED_IMPORTS = {"txt", "md", "markdown", "json", "csv"}


class KnowledgeRuntime:
    """Runtime authority for CRUD, persistence, lexical indexing, and retrieval."""

    def __init__(self, storage: KnowledgeStorage | None = None) -> None:
        self.storage = storage or JsonProjectKnowledgeStorage()
        self._lock = threading.RLock()
        self._events: dict[str, list[KnowledgeEvent]] = {}
        self._listeners: list[Callable[[KnowledgeEvent], None]] = []
        self._started_at = time.monotonic()

    def add_event_listener(self, listener: Callable[[KnowledgeEvent], None]) -> None:
        self._listeners.append(listener)

    @staticmethod
    def _terms(value: str) -> tuple[str, ...]:
        return tuple(dict.fromkeys(term.casefold() for term in _TERM.findall(value) if term.strip()))

    def _emit(
        self,
        event_type: str,
        scope: ProjectScope,
        *,
        entry_id: str | None = None,
        correlation_id: str | None = None,
        summary: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> KnowledgeEvent:
        event = KnowledgeEvent(
            event_id=f"knowledge-event-{uuid.uuid4()}",
            event_type=event_type,
            project_id=scope.project_id,
            timestamp=now_iso(),
            entry_id=entry_id,
            correlation_id=correlation_id,
            summary=summary,
            metadata=metadata or {},
        )
        self._events.setdefault(scope.project_id, []).append(event)
        self._events[scope.project_id] = self._events[scope.project_id][-500:]
        for listener in tuple(self._listeners):
            listener(event)
        return event

    def status(self, scope: ProjectScope) -> dict[str, Any]:
        started = time.monotonic()
        entries = self.storage.load(scope)
        return {
            "status": "available",
            "project_id": scope.project_id,
            "entry_count": len(entries),
            "index": {"method": "lexical", "state": "ready", "document_count": len(entries)},
            "storage": {"provider": "project_json", "location": "project://.atlas/knowledge.v1.json"},
            "uptime_ms": int((time.monotonic() - self._started_at) * 1000),
            "timing_ms": round((time.monotonic() - started) * 1000, 3),
        }

    def list_entries(
        self,
        scope: ProjectScope,
        *,
        entry_type: str | None = None,
        tags: list[str] | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> dict[str, Any]:
        if offset < 0 or not 1 <= limit <= 100:
            raise KnowledgeValidationError("offset must be non-negative and limit must be between 1 and 100")
        entries = self.storage.load(scope)
        requested_tags = {tag.casefold() for tag in tags or []}
        filtered = [
            entry for entry in entries
            if (entry_type is None or entry.type == entry_type)
            and (not requested_tags or requested_tags.issubset({tag.casefold() for tag in entry.tags}))
        ]
        filtered.sort(key=lambda entry: (entry.updated_at, entry.id), reverse=True)
        return {"entries": [entry.to_dict() for entry in filtered[offset:offset + limit]], "total": len(filtered), "offset": offset, "limit": limit}

    def get(self, scope: ProjectScope, entry_id: str) -> KnowledgeEntry:
        entry = next((item for item in self.storage.load(scope) if item.id == entry_id), None)
        if entry is None:
            raise KnowledgeNotFoundError(f"Knowledge entry not found: {entry_id}")
        return entry

    @staticmethod
    def _new_entry(scope: ProjectScope, value: dict[str, Any]) -> KnowledgeEntry:
        timestamp = now_iso()
        content = str(value.get("content", ""))
        return KnowledgeEntry(
            id=str(value.get("id") or f"knowledge-{uuid.uuid4()}"),
            project_id=scope.project_id,
            type=str(value.get("type", "note")),
            title=str(value.get("title", "Untitled knowledge")),
            content=content,
            metadata=dict(value.get("metadata") or {}),
            tags=tuple(dict.fromkeys(str(tag).strip() for tag in value.get("tags") or [] if str(tag).strip())),
            source=dict(value.get("source") or {"type": "user"}),
            provenance={"content_hash": sha256(content.encode("utf-8")).hexdigest(), **dict(value.get("provenance") or {})},
            created_at=timestamp,
            updated_at=timestamp,
        )

    def create(self, scope: ProjectScope, value: dict[str, Any], *, correlation_id: str | None = None) -> KnowledgeEntry:
        with self._lock:
            entries = self.storage.load(scope)
            entry = self._new_entry(scope, value)
            if any(item.id == entry.id for item in entries):
                raise KnowledgeValidationError(f"Knowledge entry already exists: {entry.id}")
            entries.append(entry)
            self.storage.save(scope, entries)
            self._emit("entry_created", scope, entry_id=entry.id, correlation_id=correlation_id, summary=entry.title)
            return entry

    def update(self, scope: ProjectScope, entry_id: str, changes: dict[str, Any], *, correlation_id: str | None = None) -> KnowledgeEntry:
        with self._lock:
            entries = self.storage.load(scope)
            index = next((position for position, item in enumerate(entries) if item.id == entry_id), None)
            if index is None:
                raise KnowledgeNotFoundError(f"Knowledge entry not found: {entry_id}")
            current = entries[index]
            content = str(changes.get("content", current.content))
            updated = replace(
                current,
                type=str(changes.get("type", current.type)),
                title=str(changes.get("title", current.title)),
                content=content,
                metadata=dict(changes.get("metadata", current.metadata)),
                tags=tuple(dict.fromkeys(str(tag).strip() for tag in changes.get("tags", current.tags) if str(tag).strip())),
                source=dict(changes.get("source", current.source)),
                provenance={**current.provenance, **dict(changes.get("provenance") or {}), "content_hash": sha256(content.encode("utf-8")).hexdigest()},
                updated_at=now_iso(),
                version=current.version + 1,
            )
            entries[index] = updated
            self.storage.save(scope, entries)
            self._emit("entry_updated", scope, entry_id=entry_id, correlation_id=correlation_id, summary=updated.title)
            return updated

    def delete(self, scope: ProjectScope, entry_id: str, *, correlation_id: str | None = None) -> dict[str, Any]:
        with self._lock:
            entries = self.storage.load(scope)
            current = next((item for item in entries if item.id == entry_id), None)
            if current is None:
                raise KnowledgeNotFoundError(f"Knowledge entry not found: {entry_id}")
            self.storage.save(scope, [item for item in entries if item.id != entry_id])
            self._emit("entry_deleted", scope, entry_id=entry_id, correlation_id=correlation_id, summary=current.title)
            return {"deleted": True, "entry_id": entry_id}

    @staticmethod
    def _excerpt(content: str, terms: tuple[str, ...], width: int = 220) -> str:
        folded = content.casefold()
        positions = [folded.find(term) for term in terms if folded.find(term) >= 0]
        start = max(0, (min(positions) if positions else 0) - width // 4)
        excerpt = content[start:start + width].strip()
        return ("…" if start else "") + excerpt + ("…" if start + width < len(content) else "")

    def search(
        self,
        scope: ProjectScope,
        query: str,
        *,
        entry_types: list[str] | None = None,
        tags: list[str] | None = None,
        limit: int = 25,
        request_id: str | None = None,
    ) -> dict[str, Any]:
        started = time.monotonic()
        query = query.strip()
        terms = self._terms(query)
        if not terms:
            raise KnowledgeValidationError("Search query must contain at least one term")
        if not 1 <= limit <= 100:
            raise KnowledgeValidationError("Search limit must be between 1 and 100")
        allowed_types = set(entry_types or [])
        requested_tags = {tag.casefold() for tag in tags or []}
        candidates = [
            entry for entry in self.storage.load(scope)
            if (not allowed_types or entry.type in allowed_types)
            and (not requested_tags or requested_tags.issubset({tag.casefold() for tag in entry.tags}))
        ]
        results: list[KnowledgeSearchResult] = []
        folded_query = query.casefold()
        for entry in candidates:
            title, content = entry.title.casefold(), entry.content.casefold()
            tag_text = " ".join(entry.tags).casefold()
            matched = tuple(term for term in terms if term in title or term in content or term in tag_text)
            if len(matched) != len(terms):
                continue
            score = float(sum((3 if term in title else 0) + (1 if term in content else 0) + (2 if term in tag_text else 0) for term in matched))
            if folded_query in title or folded_query in content:
                score += 5.0
            results.append(KnowledgeSearchResult(entry, entry.reference, self._excerpt(entry.content, matched), score, matched))
        results.sort(key=lambda item: (-item.score, item.entry.title.casefold(), item.entry.id))
        selected = results[:limit]
        correlation = request_id or f"knowledge-search-{uuid.uuid4()}"
        elapsed = round((time.monotonic() - started) * 1000, 3)
        self._emit("search_completed", scope, correlation_id=correlation, summary=query, metadata={"candidate_count": len(candidates), "result_count": len(selected), "method": "lexical", "timing_ms": elapsed})
        return {
            "request_id": correlation,
            "query": query,
            "method": "lexical",
            "candidate_count": len(candidates),
            "result_count": len(selected),
            "results": [result.to_dict() for result in selected],
            "filters": {"types": sorted(allowed_types), "tags": sorted(requested_tags)},
            "timing_ms": elapsed,
        }

    def import_content(
        self,
        scope: ProjectScope,
        *,
        filename: str,
        content: str,
        format_name: str,
        correlation_id: str | None = None,
    ) -> dict[str, Any]:
        format_name = format_name.lower().lstrip(".")
        if format_name not in _SUPPORTED_IMPORTS:
            raise KnowledgeValidationError(f"Unsupported import format: {format_name}")
        safe_filename = filename.replace("\\", "/").rsplit("/", 1)[-1][:255]
        imported_at = now_iso()
        source = {"type": "import", "filename": safe_filename, "format": format_name, "imported_at": imported_at}
        rows: list[dict[str, Any]]
        if format_name in {"txt", "md", "markdown"}:
            rows = [{"title": safe_filename or "Imported document", "content": content, "type": "document"}]
        elif format_name == "json":
            decoded = json.loads(content)
            raw_rows = decoded.get("entries", []) if isinstance(decoded, dict) else decoded
            if not isinstance(raw_rows, list):
                raise KnowledgeValidationError("JSON import must be an array or an object containing entries")
            rows = [dict(row) for row in raw_rows if isinstance(row, dict)]
        else:
            rows = [dict(row) for row in csv.DictReader(StringIO(content))]
        if not rows:
            raise KnowledgeValidationError("Import contains no knowledge records")
        self._emit("import_started", scope, correlation_id=correlation_id, summary=safe_filename, metadata={"format": format_name, "record_count": len(rows)})
        created: list[KnowledgeEntry] = []
        try:
            for index, row in enumerate(rows):
                row_content = str(row.get("content", row.get("text", "")))
                row_tags = row.get("tags", [])
                if isinstance(row_tags, str):
                    row_tags = [tag.strip() for tag in row_tags.split(",") if tag.strip()]
                created.append(self._new_entry(scope, {
                    "type": row.get("type", "document"),
                    "title": row.get("title") or row.get("name") or f"{safe_filename} #{index + 1}",
                    "content": row_content,
                    "tags": row_tags,
                    "metadata": dict(row.get("metadata") or {}),
                    "source": source,
                    "provenance": {"record_index": index, "source_hash": sha256(content.encode("utf-8")).hexdigest()},
                }))
            with self._lock:
                existing = self.storage.load(scope)
                existing_ids = {entry.id for entry in existing}
                if any(entry.id in existing_ids for entry in created):
                    raise KnowledgeValidationError("Import contains an existing knowledge id")
                self.storage.save(scope, [*existing, *created])
            for entry in created:
                self._emit("entry_created", scope, entry_id=entry.id, correlation_id=correlation_id, summary=entry.title)
        except Exception as error:
            self._emit("import_failed", scope, correlation_id=correlation_id, summary=safe_filename, metadata={"error_type": error.__class__.__name__})
            raise
        self._emit("import_completed", scope, correlation_id=correlation_id, summary=safe_filename, metadata={"created_count": len(created)})
        return {"created": [entry.to_dict() for entry in created], "count": len(created), "duplicate_policy": "allow"}

    def export(self, scope: ProjectScope, format_name: str = "json") -> dict[str, Any]:
        entries = self.storage.load(scope)
        if format_name == "json":
            content = json.dumps({"schemaVersion": 1, "projectId": scope.project_id, "entries": [entry.to_dict() for entry in entries]}, ensure_ascii=False, indent=2)
        elif format_name in {"md", "markdown"}:
            content = "\n\n".join(f"# {entry.title}\n\n{entry.content}" for entry in entries)
        else:
            raise KnowledgeValidationError(f"Unsupported export format: {format_name}")
        return {"format": "md" if format_name == "markdown" else format_name, "content": content, "count": len(entries)}

    def events(self, scope: ProjectScope, limit: int = 100) -> list[dict[str, Any]]:
        if not 1 <= limit <= 500:
            raise KnowledgeValidationError("Event limit must be between 1 and 500")
        return [event.to_dict() for event in self._events.get(scope.project_id, [])[-limit:]]

    def assemble_ai_context(self, scope: ProjectScope, references: list[dict[str, Any]]) -> list[dict[str, Any]]:
        entries = {entry.id: entry for entry in self.storage.load(scope)}
        contexts: list[dict[str, Any]] = []
        for reference in references[:50]:
            if str(reference.get("project_id", reference.get("projectId", ""))) != scope.project_id:
                raise KnowledgeValidationError("AI knowledge reference belongs to a different project")
            entry_id = str(reference.get("entry_id", reference.get("entryId", "")))
            entry = entries.get(entry_id)
            if entry is None:
                raise KnowledgeNotFoundError(f"Knowledge entry not found: {entry_id}")
            contexts.append({"reference": entry.reference.to_dict(), "title": entry.title, "content": entry.content, "source": entry.source, "metadata": entry.metadata})
        return contexts
