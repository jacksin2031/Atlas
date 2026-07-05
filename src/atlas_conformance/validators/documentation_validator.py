from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ..core import DocumentationCoverage
from ..scanners.documentation_scanner import DocumentationScanner


class DocumentationValidator:
    def __init__(self, repo_root: str | Path) -> None:
        self._repo_root = Path(repo_root)
        self._scanner = DocumentationScanner(self._repo_root)

    def validate(self) -> DocumentationCoverage:
        scan_results = self._scanner.scan()

        expected_docs = self._expected_documents()
        present_docs = set()
        for path_str in scan_results.get("markdown_files", []):
            present_docs.add(Path(path_str).name)
        for path_str in scan_results.get("readme_files", []):
            present_docs.add("README.md")

        missing = tuple(d for d in expected_docs if d not in present_docs)

        broken_refs = self._check_broken_references(scan_results)
        consistency_issues = self._check_consistency(scan_results)

        total_expected = len(expected_docs)
        total_present = len(present_docs.intersection(set(expected_docs)))
        pct = (total_present / total_expected * 100) if total_expected > 0 else 100.0

        return DocumentationCoverage(
            total_expected_docs=total_expected,
            total_present_docs=total_present,
            missing_docs=missing,
            broken_references=tuple(broken_refs),
            consistency_issues=tuple(consistency_issues),
            coverage_percentage=round(pct, 2),
        )

    def _expected_documents(self) -> set[str]:
        return {
            "README.md",
            "ARCHITECTURE.md",
            "DESIGN_PRINCIPLES.md",
            "MODULE_DEPENDENCIES.md",
            "COMPLIANCE_REPORT.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "VERSIONING.md",
            "RELEASE.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "CODE_OF_CONDUCT.md",
            "PROJECT_STATUS.md",
        }

    def _check_broken_references(self, scan_results: dict[str, Any]) -> list[str]:
        broken: list[str] = []
        all_md = scan_results.get("markdown_files", [])
        for path_str in all_md:
            try:
                text = Path(path_str).read_text(encoding="utf-8")
                links = re.findall(r"\[.*?\]\(([^)]+)\)", text)
                for link in links:
                    if link.startswith("./") or link.startswith("../"):
                        target = Path(path_str).parent / link
                        if not target.exists():
                            broken.append(f"{path_str}: {link}")
            except Exception:
                pass
        return broken

    def _check_consistency(self, scan_results: dict[str, Any]) -> list[str]:
        issues: list[str] = []
        readme_path = self._repo_root / "README.md"
        if readme_path.exists():
            text = readme_path.read_text(encoding="utf-8")
            versions = re.findall(r"v?\d+\.\d+\.\d+", text)
            if len(versions) > 3:
                unique_versions = set(versions)
                if len(unique_versions) > 1:
                    issues.append(f"Multiple version numbers in README: {unique_versions}")

        for path_str in scan_results.get("markdown_files", []):
            try:
                text = Path(path_str).read_text(encoding="utf-8")
                if "sprint" in text.lower():
                    sprints = re.findall(r"sprint\s*(\d+)", text, re.IGNORECASE)
                    if sprints:
                        unique = set(int(s) for s in sprints)
                        if len(unique) > 1:
                            issues.append(f"{Path(path_str).name}: Multiple sprint references: {sorted(unique)}")
            except Exception:
                pass
        return issues
