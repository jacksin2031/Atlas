from __future__ import annotations

import pytest
from atlas_conformance.core import TestCoverage as TC


class TestTestCoverage:
    def test_covered_with_tests(self):
        tc = TC(
            module_name="test_mod", unit_tests=10, integration_tests=2,
            has_test_file=True, is_covered=True,
        )
        assert tc.module_name == "test_mod"
        assert tc.unit_tests == 10
        assert tc.is_covered is True

    def test_covered_with_test_file(self):
        tc = TC(
            module_name="has_file", has_test_file=True, is_covered=True,
        )
        assert tc.is_covered is True

    def test_not_covered(self):
        tc = TC(module_name="bare_mod", has_test_file=False, is_covered=False)
        assert tc.is_covered is False
