from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core import (
    ArchitectureViolation,
    ModuleDependency,
    ModuleGraph,
    ModuleRules,
    RuleCategory,
    ViolationSeverity,
)
from ..scanners.module_scanner import ModuleInfo, ModuleScanner


class ModuleValidator:
    def __init__(self, src_root: str | Path, rules: ModuleRules | None = None) -> None:
        self._src_root = Path(src_root)
        self._rules = rules or self._default_rules()
        self._scanner = ModuleScanner(self._src_root)

    def _default_rules(self) -> ModuleRules:
        return ModuleRules(
            allowed_imports=(
                ("atlas_workflow", "atlas_workflow.common"),
                ("atlas_workflow", "atlas_workflow.events"),
                ("atlas_workflow", "atlas_workflow.execution"),
                ("atlas_workflow", "atlas_workflow.graph"),
                ("atlas_workflow", "atlas_workflow.health"),
                ("atlas_workflow", "atlas_workflow.manifest"),
                ("atlas_workflow", "atlas_workflow.metrics"),
                ("atlas_workflow", "atlas_workflow.node_registry"),
                ("atlas_workflow", "atlas_workflow.parser"),
                ("atlas_workflow", "atlas_workflow.plugin_integration"),
                ("atlas_workflow", "atlas_workflow.runtime"),
                ("atlas_workflow", "atlas_workflow.scheduler"),
                ("atlas_workflow", "atlas_workflow.storage"),
                ("atlas_workflow", "atlas_workflow.validator"),
            ),
            forbidden_imports=(
                ("atlas_workflow", "atlas_desktop"),
                ("atlas_workflow", "atlas_marketplace"),
                ("atlas_workflow", "atlas_cloud"),
                ("atlas_workflow", "atlas_network"),
            ),
            public_api_patterns=("^[A-Z][a-zA-Z0-9]*$"),
            naming_conventions={
                "module": "snake_case",
                "class": "PascalCase",
                "function": "snake_case",
                "constant": "UPPER_SNAKE_CASE",
            },
            required_packages=("common", "events", "runtime", "validator"),
            required_services=(),
        )

    @property
    def rules(self) -> ModuleRules:
        return self._rules

    def validate(self) -> tuple[ModuleGraph, tuple[ArchitectureViolation, ...]]:
        violations: list[ArchitectureViolation] = []
        graph = self._build_module_graph()
        violations.extend(self._check_forbidden_imports())
        violations.extend(self._check_naming_conventions())
        violations.extend(self._check_required_packages())
        violations.extend(self._check_public_api())
        return graph, tuple(violations)

    def _build_module_graph(self) -> ModuleGraph:
        scanner = ModuleScanner(self._src_root)
        packages = scanner.find_packages()
        modules = tuple(str(p.relative_to(self._src_root.parent)) for p in packages if p.name == "__init__.py")

        edges: list[ModuleDependency] = []
        for info in scanner.scan():
            src = str(Path(info.path).parts[0]) if "/" in str(info.path) else info.name
            for imp in info.imports:
                if imp.is_internal:
                    target = imp.target_module.split(".")[0]
                    allowed = not any(
                        src == pair[0] and target == pair[1]
                        for pair in self._rules.forbidden_imports
                    )
                    edges.append(ModuleDependency(
                        source=src,
                        target=target,
                        allowed=allowed,
                    ))

        return ModuleGraph(
            modules=modules,
            edges=tuple(edges),
        )

    def _check_forbidden_imports(self) -> list[ArchitectureViolation]:
        violations: list[ArchitectureViolation] = []
        for info in self._scanner.scan():
            for imp in info.imports:
                for forbidden_src, forbidden_tgt in self._rules.forbidden_imports:
                    src_match = imp.source_module.startswith(forbidden_src)
                    tgt_match = imp.target_module.startswith(forbidden_tgt)
                    if src_match and tgt_match:
                        violations.append(ArchitectureViolation(
                            rule_id="MOD-FORBID",
                            rule_name="Forbidden imports",
                            category=RuleCategory.MODULE_RULES,
                            severity=ViolationSeverity.ERROR,
                            message=f"Forbidden import: {imp.source_module} -> {imp.target_module}",
                            file_path=info.path,
                            line_number=imp.line_number,
                            suggestion=f"Remove import from {forbidden_tgt}",
                        ))
        return violations

    def _check_naming_conventions(self) -> list[ArchitectureViolation]:
        violations: list[ArchitectureViolation] = []
        for info in self._scanner.scan():
            name = Path(info.path).stem
            if name.startswith("_"):
                continue
            conventions = self._rules.naming_conventions
            expected_pattern = conventions.get("module", "snake_case")
            if expected_pattern == "snake_case" and "_" not in name and name.isupper():
                violations.append(ArchitectureViolation(
                    rule_id="MOD-NAMING",
                    rule_name="Naming conventions",
                    category=RuleCategory.NAMING_CONVENTIONS,
                    severity=ViolationSeverity.INFO,
                    message=f"Module '{name}' may not follow snake_case convention",
                    file_path=info.path,
                ))
        return violations

    def _check_required_packages(self) -> list[ArchitectureViolation]:
        violations: list[ArchitectureViolation] = []
        found_packages = set()
        for info in self._scanner.scan():
            parts = Path(info.path).parts
            for part in parts:
                if part != "__pycache__":
                    found_packages.add(part)

        for required in self._rules.required_packages:
            if required not in found_packages:
                violations.append(ArchitectureViolation(
                    rule_id="MOD-REQUIRED",
                    rule_name="Required packages",
                    category=RuleCategory.MODULE_RULES,
                    severity=ViolationSeverity.WARNING,
                    message=f"Required package '{required}' not found",
                ))
        return violations

    def _check_public_api(self) -> list[ArchitectureViolation]:
        return []
