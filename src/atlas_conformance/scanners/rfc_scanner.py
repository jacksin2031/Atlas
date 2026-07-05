from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class RFCMetadata:
    rfc_id: str
    title: str
    status: str
    version: str
    author: str
    created: str
    category: str
    layer: str
    normative: str
    audience: str
    adr_references: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    supersedes: tuple[str, ...] = ()
    superseded_by: tuple[str, ...] = ()
    related_rfcs: tuple[str, ...] = ()
    target_release: str = ""
    last_updated: str = ""
    file_path: str = ""
    requirements: tuple[str, ...] = ()
    acceptance_criteria: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RFCScanner:
    def __init__(self, specs_root: str | Path) -> None:
        self._specs_root = Path(specs_root)

    def find_all_rfcs(self) -> list[Path]:
        rfcs: list[Path] = []
        if not self._specs_root.exists():
            return rfcs
        for md in sorted(self._specs_root.rglob("RFC-*.md")):
            rfcs.append(md)
        return rfcs

    def parse_rfc(self, path: Path) -> RFCMetadata:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        meta: dict[str, str] = {}
        current_section: str | None = None
        requirements_lines: list[str] = []
        criteria_lines: list[str] = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("# "):
                continue
            if stripped.startswith("## "):
                current_section = stripped.lstrip("# ").strip().lower()
                continue
            if current_section == "normative status":
                meta["normative"] = "YES" if "normative" in stripped.lower() else "NO"
            if current_section == "acceptance criteria":
                if stripped.startswith(("- ", "* ")):
                    criteria_lines.append(stripped.lstrip("- ").lstrip("* ").strip())
                continue
            if current_section == "requirements":
                if stripped.startswith(("- ", "* ")):
                    requirements_lines.append(stripped.lstrip("- ").lstrip("* ").strip())
                continue

            if ":" in stripped and not stripped.startswith(("- ", "* ", "#")):
                key, _, val = stripped.partition(":")
                key = key.strip().lower()
                val = val.strip()
                if key in ("rfc", "title", "status", "version", "author",
                           "created", "last updated", "category", "layer",
                           "audience", "target release", "supersedes",
                           "superseded by", "depends on", "related rfc"):
                    meta[key] = val

        stem = path.stem
        rfc_id = ""
        if stem.startswith("RFC-"):
            parts = stem.split("-")
            if len(parts) >= 3:
                rfc_id = "-".join(parts[:3])
            else:
                rfc_id = stem

        title = meta.get("title", path.stem)
        status = meta.get("status", "Unknown")
        version = meta.get("version", "0.0.0")
        author = meta.get("author", "Unknown")
        created = meta.get("created", "")
        category = meta.get("category", "")
        layer = meta.get("layer", "")
        normative = meta.get("normative", "NO")
        audience = meta.get("audience", "")
        target_release = meta.get("target release", "")
        last_updated = meta.get("last updated", created)

        def parse_list(val: str) -> tuple[str, ...]:
            if not val:
                return ()
            items = []
            for part in val.split(","):
                part = part.strip()
                if part:
                    items.append(part)
            return tuple(items)

        adr_refs = parse_list(meta.get("adr references", ""))
        depends = parse_list(meta.get("depends on", ""))
        supersedes = parse_list(meta.get("supersedes", ""))
        superseded_by = parse_list(meta.get("superseded by", ""))
        related = parse_list(meta.get("related rfc", ""))

        return RFCMetadata(
            rfc_id=rfc_id,
            title=title,
            status=status,
            version=version,
            author=author,
            created=created,
            category=category,
            layer=layer,
            normative=normative,
            audience=audience,
            adr_references=adr_refs,
            depends_on=depends,
            supersedes=supersedes,
            superseded_by=superseded_by,
            related_rfcs=related,
            target_release=target_release,
            last_updated=last_updated,
            file_path=str(path),
            requirements=tuple(requirements_lines),
            acceptance_criteria=tuple(criteria_lines),
        )

    def scan(self) -> list[RFCMetadata]:
        paths = self.find_all_rfcs()
        results: list[RFCMetadata] = []
        for p in paths:
            try:
                results.append(self.parse_rfc(p))
            except Exception:
                pass
        return results

    @property
    def rfc_ids(self) -> tuple[str, ...]:
        return tuple(r.rfc_id for r in self.scan())

    @property
    def categories(self) -> tuple[str, ...]:
        cats = set()
        for r in self.scan():
            if r.category:
                cats.add(r.category)
        return tuple(sorted(cats))

    @property
    def statuses(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for r in self.scan():
            counts[r.status] = counts.get(r.status, 0) + 1
        return counts
