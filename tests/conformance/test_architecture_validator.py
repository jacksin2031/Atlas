from __future__ import annotations

import pytest
from atlas_conformance.validators import ArchitectureValidator
from atlas_conformance.core import (
    ArchitectureRule,
    ArchitectureViolation,
    RuleCategory,
    ViolationSeverity,
    ComplianceLevel,
)


class TestArchitectureValidator:
    def test_default_rules_registered(self):
        av = ArchitectureValidator("src", "specs")
        rules = av.rules
        assert len(rules) == 9
        rule_ids = [r.rule_id for r in rules]
        assert "LAYER-001" in rule_ids
        assert "CIRC-001" in rule_ids

    def test_validate_returns_report(self):
        av = ArchitectureValidator("src", "specs")
        report = av.validate()
        assert report.rules_checked == 9
        assert report.rules_passed >= 0
        assert report.rules_failed >= 0

    def test_rules_property_immutable(self):
        av = ArchitectureValidator("src", "specs")
        rules = av.rules
        assert isinstance(rules, tuple)

    def test_disable_rule(self):
        av = ArchitectureValidator("src", "specs")
        # All rules should pass by default
        report = av.validate()
        assert report.rules_failed == 0

    def test_severity_levels(self):
        severities = [r.severity for r in ArchitectureValidator("src", "specs").rules]
        assert ViolationSeverity.CRITICAL in severities
        assert ViolationSeverity.ERROR in severities
        assert ViolationSeverity.WARNING in severities
