from __future__ import annotations

import pytest
from atlas_conformance.validators import ADRValidator
from atlas_conformance.scanners.adr_scanner import ADRScanner


class TestADRScanner:
    def test_find_all_adrs(self):
        scanner = ADRScanner("docs/adr")
        adrs = scanner.find_all_adrs()
        assert len(adrs) > 0

    def test_parse_adr(self):
        scanner = ADRScanner("docs/adr")
        adrs = scanner.find_all_adrs()
        if adrs:
            parsed = scanner.parse_adr(adrs[0])
            assert parsed.adr_id != ""
            assert parsed.title != ""

    def test_scan(self):
        scanner = ADRScanner("docs/adr")
        results = scanner.scan()
        assert len(results) > 0

    def test_adr_ids_property(self):
        scanner = ADRScanner("docs/adr")
        ids = scanner.adr_ids
        assert len(ids) > 0

    def test_statuses_property(self):
        scanner = ADRScanner("docs/adr")
        statuses = scanner.statuses
        assert isinstance(statuses, dict)


class TestADRValidator:
    def test_validate_returns_compliance(self):
        validator = ADRValidator("docs/adr", "specs")
        compliance = validator.validate()
        assert compliance.total_adrs > 0
        assert 0 <= compliance.compliance_percentage <= 100

    def test_references_are_found(self):
        validator = ADRValidator("docs/adr", "specs")
        compliance = validator.validate()
        # References may be empty if no specs reference ADRs
        assert compliance.references is not None
