from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ADRMetadata:
    adr_id: str
    title: str
    status: str
    date: str
    authors: tuple[str, ...] = ()
    supersedes: tuple[str, ...] = ()
    superseded_by: tuple[str, ...] = ()
    context: str = ""
    decision: str = ""
    consequences: str = ""
    alternatives: tuple[str, ...] = ()
    file_path: str = ""


@dataclass
class ADRScanner:
    def __init__(self, adr_root: str | Path) -> None:
        self._adr_root = Path(adr_root)

    def find_all_adrs(self) -> list[Path]:
        adrs: list[Path] = []
        if not self._adr_root.exists():
            return adrs
        for md in sorted(self._adr_root.rglob("*.md")):
            stem = md.stem.lower()
            if stem.startswith("adr-") or stem.startswith("00") or stem.startswith("adr_00"):
                if stem != "readme":
                    adrs.append(md)
        return adrs

    def parse_adr(self, path: Path) -> ADRMetadata:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        meta: dict[str, str] = {}
        sections: dict[str, list[str]] = {}
        current_section: str | None = None

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("# ") and not stripped.startswith("## "):
                continue
            if stripped.startswith("## "):
                current_section = stripped.lstrip("# ").strip().lower()
                sections.setdefault(current_section, [])
                continue
            if current_section and stripped:
                sections[current_section].append(stripped)
            if ":" in stripped and not stripped.startswith(("- ", "* ", "#")):
                key, _, val = stripped.partition(":")
                key = key.strip().lower()
                val = val.strip()
                if key in ("title", "status", "date", "authors", "supersedes", "superseded by"):
                    meta[key] = val

        stem = path.stem
        adr_id = stem
        if stem.startswith("adr-"):
            adr_id = stem
        elif stem.startswith("00"):
            adr_id = "adr-" + stem
        elif stem.startswith("adr_"):
            adr_id = "adr-" + stem.replace("_", "-")

        authors_raw = meta.get("authors", "")
        authors = tuple(a.strip() for a in authors_raw.split(",") if a.strip()) if authors_raw else ()

        def parse_list(val: str) -> tuple[str, ...]:
            if not val:
                return ()
            items = []
            for part in val.split(","):
                part = part.strip()
                if part:
                    items.append(part)
            return tuple(items)

        supersedes = parse_list(meta.get("supersedes", ""))
        superseded_by = parse_list(meta.get("superseded by", ""))

        context_text = " ".join(sections.get("context", []))
        decision_text = " ".join(sections.get("decision", []))
        consequences_text = " ".join(sections.get("consequences", []))

        return ADRMetadata(
            adr_id=adr_id,
            title=meta.get("title", path.stem),
            status=meta.get("status", "Unknown"),
            date=meta.get("date", ""),
            authors=authors,
            supersedes=supersedes,
            superseded_by=superseded_by,
            context=context_text,
            decision=decision_text,
            consequences=consequences_text,
            file_path=str(path),
        )

    def scan(self) -> list[ADRMetadata]:
        paths = self.find_all_adrs()
        results: list[ADRMetadata] = []
        for p in paths:
            try:
                results.append(self.parse_adr(p))
            except Exception:
                pass
        return results

    @property
    def adr_ids(self) -> tuple[str, ...]:
        return tuple(a.adr_id for a in self.scan())

    @property
    def statuses(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for a in self.scan():
            counts[a.status] = counts.get(a.status, 0) + 1
        return counts
