from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core import (
    ADRCompliance,
    ADRReference,
)
from ..scanners.adr_scanner import ADRMetadata, ADRScanner


class ADRValidator:
    def __init__(self, adr_root: str | Path, specs_root: str | Path | None = None) -> None:
        self._adr_root = Path(adr_root)
        self._specs_root = Path(specs_root) if specs_root else Path()
        self._scanner = ADRScanner(self._adr_root)

    def validate(self) -> ADRCompliance:
        adrs = self._scanner.scan()
        if not adrs:
            return ADRCompliance(total_adrs=0, compliance_percentage=0.0)

        references: list[ADRReference] = []
        referenced_ids: set[str] = set()
        deprecated_count = 0
        superseded_count = 0

        for adr in adrs:
            if adr.status.lower() == "deprecated":
                deprecated_count += 1
            if adr.status.lower() == "superseded":
                superseded_count += 1

            adr_refs = self._find_references(adr)
            for ref in adr_refs:
                references.append(ref)
                referenced_ids.add(ref.adr_id)

        all_adr_ids = set(a.adr_id for a in adrs)
        referenced_count = len(referenced_ids.intersection(all_adr_ids))
        total = len(adrs)
        pct = (referenced_count / total * 100) if total > 0 else 0.0

        return ADRCompliance(
            total_adrs=total,
            referenced_adrs=referenced_count,
            deprecated_adrs=deprecated_count,
            superseded_adrs=superseded_count,
            references=tuple(references),
            compliance_percentage=round(pct, 2),
        )

    def _find_references(self, adr: ADRMetadata) -> list[ADRReference]:
        refs: list[ADRReference] = []
        search_dirs = [self._specs_root] if self._specs_root and self._specs_root.exists() else []
        for search_dir in search_dirs:
            for md_file in search_dir.rglob("*.md"):
                try:
                    text = md_file.read_text(encoding="utf-8")
                    lines = text.splitlines()
                    for i, line in enumerate(lines, 1):
                        if adr.adr_id.upper() in line.upper():
                            ctx = line.strip()[:100]
                            refs.append(ADRReference(
                                adr_id=adr.adr_id,
                                referenced_in=str(md_file),
                                line_number=i,
                                context=ctx,
                            ))
                except Exception:
                    pass
        return refs
