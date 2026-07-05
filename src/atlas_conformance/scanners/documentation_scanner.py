from __future__ import annotations

import re
from pathlib import Path
from typing import Any


class DocumentationScanner:
    def __init__(self, repo_root: str | Path) -> None:
        self._repo_root = Path(repo_root)

    def find_readme_files(self) -> list[Path]:
        return sorted(self._repo_root.rglob("README.md"))

    def find_all_markdown(self) -> list[Path]:
        md_files: list[Path] = []
        if not self._repo_root.exists():
            return md_files
        for md in sorted(self._repo_root.rglob("*.md")):
            if md.name == "README.md" or ".ai" not in str(md.parts):
                md_files.append(md)
        return md_files

    def find_compliance_reports(self) -> list[Path]:
        reports: list[Path] = []
        if not self._repo_root.exists():
            return reports
        for rpt in sorted(self._repo_root.rglob("*COMPLIANCE*.md")):
            reports.append(rpt)
        for rpt in sorted(self._repo_root.rglob("*compliance*.md")):
            if rpt not in reports:
                reports.append(rpt)
        return reports

    def find_architecture_docs(self) -> list[Path]:
        docs: list[Path] = []
        if not self._repo_root.exists():
            return docs
        for name in ["ARCHITECTURE.md", "architecture.md"]:
            p = self._repo_root / "docs" / name
            if p.exists():
                docs.append(p)
        return docs

    def extract_references(self, path: Path) -> tuple[str, ...]:
        text = path.read_text(encoding="utf-8")
        refs: list[str] = []
        for line in text.splitlines():
            line = line.strip()
            if "ADR-" in line or "adr-" in line:
                matches = re.findall(r"(ADR-?\d+)", line, re.IGNORECASE)
                refs.extend(matches)
            if "RFC-" in line:
                matches = re.findall(r"(RFC-\d+-?\w*)", line)
                refs.extend(matches)
        return tuple(dict.fromkeys(refs))

    def scan(self) -> dict[str, Any]:
        return {
            "readme_files": [str(p) for p in self.find_readme_files()],
            "markdown_files": [str(p) for p in self.find_all_markdown()],
            "compliance_reports": [str(p) for p in self.find_compliance_reports()],
            "architecture_docs": [str(p) for p in self.find_architecture_docs()],
        }
