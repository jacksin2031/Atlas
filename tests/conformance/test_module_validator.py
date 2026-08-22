from __future__ import annotations

import pytest
from atlas_conformance.validators import ModuleValidator
from atlas_conformance.scanners.module_scanner import ModuleScanner


class TestModuleScanner:
    def test_find_packages(self):
        scanner = ModuleScanner("src")
        pkgs = scanner.find_packages()
        assert len(pkgs) > 0

    def test_parse_python_file(self):
        scanner = ModuleScanner("src")
        pkgs = scanner.find_packages()
        if pkgs:
            py_files = list(pkgs[0].rglob("*.py"))
            if py_files:
                info = scanner.parse_python_file(py_files[0])
                assert info.name != ""
                assert isinstance(info.imports, tuple)

    def test_build_dependency_graph(self):
        scanner = ModuleScanner("src")
        graph = scanner.build_dependency_graph()
        assert isinstance(graph, dict)


class TestModuleValidator:
    def test_validate_returns_graph_and_violations(self):
        validator = ModuleValidator("src")
        graph, violations = validator.validate()
        assert graph is not None
        assert isinstance(violations, tuple)

    def test_default_rules_exist(self):
        validator = ModuleValidator("src")
        rules = validator.rules
        assert len(rules.forbidden_imports) > 0
        assert len(rules.allowed_imports) > 0

    def test_no_forbidden_imports_in_workflow(self):
        validator = ModuleValidator("src")
        graph, violations = validator.validate()
        forbidden = [v for v in violations if "Forbidden" in v.rule_name]
        assert len(forbidden) == 0
