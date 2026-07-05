from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core import TestCoverage


class TestCoverageValidator:
    def __init__(self, src_root: str | Path, tests_root: str | Path) -> None:
        self._src_root = Path(src_root)
        self._tests_root = Path(tests_root)

    def validate(self) -> tuple[TestCoverage, ...]:
        modules = self._discover_modules()
        results: list[TestCoverage] = []

        for module_name, module_path in modules:
            tc = self._validate_module(module_name, module_path)
            results.append(tc)

        return tuple(results)

    def _discover_modules(self) -> list[tuple[str, str]]:
        modules: list[tuple[str, str]] = []
        if not self._src_root.exists():
            return modules
        for init_file in self._src_root.rglob("__init__.py"):
            pkg_dir = init_file.parent
            if pkg_dir.name == "__pycache__":
                continue
            rel = str(pkg_dir.relative_to(self._src_root.parent))
            modules.append((rel, str(pkg_dir)))
        return modules

    def _validate_module(self, module_name: str, module_path: str) -> TestCoverage:
        test_module_path = module_path.replace(str(self._src_root), str(self._tests_root))
        test_path = Path(test_module_path)

        has_test_file = test_path.exists() or test_path.parent.exists()
        unit_tests = 0
        integration_tests = 0
        architecture_tests = 0

        if has_test_file and test_path.parent.exists():
            for tf in test_path.parent.glob("test_*.py"):
                try:
                    text = tf.read_text(encoding="utf-8")
                    unit_tests += text.count("def test_")
                    integration_tests += text.count("def test_integration") + text.count("def test_e2e")
                    architecture_tests += text.count("def test_architecture") + text.count("def test_conformance")
                except Exception:
                    pass

        compliance_report = self._has_compliance_report(module_name)
        documentation = self._has_documentation(module_name)

        return TestCoverage(
            module_name=module_name,
            unit_tests=unit_tests,
            integration_tests=integration_tests,
            architecture_tests=architecture_tests,
            compliance_report=compliance_report,
            documentation=documentation,
            has_test_file=has_test_file,
            is_covered=unit_tests > 0 or has_test_file,
        )

    def _has_compliance_report(self, module_name: str) -> bool:
        docs_root = self._src_root.parent / "docs"
        if not docs_root.exists():
            return False
        for doc_file in docs_root.rglob("*COMPLIANCE*.md"):
            try:
                text = doc_file.read_text(encoding="utf-8")
                if module_name.lower().replace("-", "_") in text.lower():
                    return True
            except Exception:
                pass
        return False

    def _has_documentation(self, module_name: str) -> bool:
        docs_root = self._src_root.parent / "docs"
        if not docs_root.exists():
            return False
        for doc_file in docs_root.rglob("*.md"):
            try:
                text = doc_file.read_text(encoding="utf-8")
                if module_name.lower().replace("-", "_") in text.lower():
                    return True
            except Exception:
                pass
        return False
