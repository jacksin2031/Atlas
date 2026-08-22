from __future__ import annotations

import pytest
from atlas_conformance.validators.test_coverage_validator import TestCoverageValidator as TCV


class TestTestCoverageValidator:
    def test_validate_returns_tuple(self):
        validator = TCV("src", "tests")
        coverage = validator.validate()
        assert isinstance(coverage, tuple)
        assert len(coverage) > 0

    def test_each_module_has_coverage(self):
        validator = TCV("src", "tests")
        coverage = validator.validate()
        for tc in coverage:
            assert tc.module_name != ""
            assert tc.unit_tests >= 0
            assert tc.integration_tests >= 0
            assert tc.is_covered is not None

    def test_workflow_module_found(self):
        validator = TCV("src", "tests")
        coverage = validator.validate()
        module_names = [tc.module_name for tc in coverage]
        assert any("workflow" in m for m in module_names)
