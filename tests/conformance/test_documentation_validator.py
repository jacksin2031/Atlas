from __future__ import annotations

import pytest
from atlas_conformance.validators import DocumentationValidator
from atlas_conformance.scanners.documentation_scanner import DocumentationScanner


class TestDocumentationScanner:
    def test_find_readme_files(self):
        scanner = DocumentationScanner(".")
        readmes = scanner.find_readme_files()
        assert len(readmes) > 0

    def test_find_all_markdown(self):
        scanner = DocumentationScanner(".")
        md_files = scanner.find_all_markdown()
        assert len(md_files) > 0

    def test_find_compliance_reports(self):
        scanner = DocumentationScanner(".")
        reports = scanner.find_compliance_reports()
        assert len(reports) > 0

    def test_find_architecture_docs(self):
        scanner = DocumentationScanner(".")
        docs = scanner.find_architecture_docs()
        assert len(docs) > 0

    def test_extract_references(self):
        scanner = DocumentationScanner(".")
        readmes = scanner.find_readme_files()
        if readmes:
            refs = scanner.extract_references(readmes[0])
            assert isinstance(refs, tuple)


class TestDocumentationValidator:
    def test_validate_returns_coverage(self):
        validator = DocumentationValidator(".")
        coverage = validator.validate()
        assert coverage.total_expected_docs > 0
        assert coverage.total_present_docs >= 0
        assert 0 <= coverage.coverage_percentage <= 100

    def test_missing_docs_empty_when_all_present(self):
        validator = DocumentationValidator(".")
        coverage = validator.validate()
        assert len(coverage.missing_docs) == 0

    def test_broken_references_checked(self):
        validator = DocumentationValidator(".")
        coverage = validator.validate()
        assert isinstance(coverage.broken_references, tuple)
