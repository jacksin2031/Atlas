from __future__ import annotations

import pytest
from atlas_conformance.validators import RFCValidator
from atlas_conformance.scanners.rfc_scanner import RFCScanner
from atlas_conformance.core import RFCStatus


class TestRFCScanner:
    def test_find_all_rfcs(self):
        scanner = RFCScanner("specs")
        rfcs = scanner.find_all_rfcs()
        assert len(rfcs) > 0

    def test_parse_rfc(self):
        scanner = RFCScanner("specs")
        rfcs = scanner.find_all_rfcs()
        if rfcs:
            parsed = scanner.parse_rfc(rfcs[0])
            assert parsed.rfc_id != ""
            assert parsed.title != ""
            assert parsed.status != ""

    def test_rfc_ids_property(self):
        scanner = RFCScanner("specs")
        ids = scanner.rfc_ids
        assert len(ids) > 0
        assert all("RFC-" in rid for rid in ids)

    def test_statuses_property(self):
        scanner = RFCScanner("specs")
        statuses = scanner.statuses
        assert isinstance(statuses, dict)
        assert sum(statuses.values()) > 0

    def test_scan_empty_directory(self):
        scanner = RFCScanner("/nonexistent/path")
        results = scanner.scan()
        assert results == []


class TestRFCValidator:
    def test_validate_returns_coverage(self):
        validator = RFCValidator("specs", "src")
        coverage = validator.validate()
        assert coverage.total_rfcs > 0
        assert 0 <= coverage.coverage_percentage <= 100

    def test_coverage_has_compliance_entries(self):
        validator = RFCValidator("specs", "src")
        coverage = validator.validate()
        assert len(coverage.compliance) == coverage.total_rfcs

    def test_rfc_compliance_fields(self):
        validator = RFCValidator("specs", "src")
        coverage = validator.validate()
        if coverage.compliance:
            first = coverage.compliance[0]
            assert first.rfc_id != ""
            assert first.title != ""
            assert isinstance(first.status, RFCStatus)
            assert first.is_implemented is not None
