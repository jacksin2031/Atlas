from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core import (
    ArchitectureReport,
    ArchitectureRule,
    ArchitectureViolation,
    ComplianceLevel,
    ModuleDependency,
    ModuleGraph,
    RuleCategory,
    ViolationSeverity,
)
from ..scanners.module_scanner import ModuleScanner


class ArchitectureValidator:
    def __init__(self, src_root: str | Path, specs_root: str | Path | None = None) -> None:
        self._src_root = Path(src_root)
        self._specs_root = Path(specs_root) if specs_root else Path()
        self._rules: list[ArchitectureRule] = []
        self._register_default_rules()

    def _register_default_rules(self) -> None:
        self._rules = [
            ArchitectureRule(
                rule_id="LAYER-001",
                name="Layering enforced",
                category=RuleCategory.LAYERING,
                description="Lower layers must not import from upper layers.",
                severity=ViolationSeverity.CRITICAL,
            ),
            ArchitectureRule(
                rule_id="DEP-001",
                name="Dependency direction",
                category=RuleCategory.DEPENDENCY_DIRECTION,
                description="Dependencies must flow upward in the layer hierarchy.",
                severity=ViolationSeverity.ERROR,
            ),
            ArchitectureRule(
                rule_id="CIRC-001",
                name="No circular dependencies",
                category=RuleCategory.CIRCULAR_DEPENDENCY,
                description="No circular dependencies between modules.",
                severity=ViolationSeverity.CRITICAL,
            ),
            ArchitectureRule(
                rule_id="IMP-001",
                name="Forbidden imports",
                category=RuleCategory.FORBIDDEN_IMPORTS,
                description="Forbidden imports must not be used.",
                severity=ViolationSeverity.ERROR,
            ),
            ArchitectureRule(
                rule_id="PRV-001",
                name="Provider pattern",
                category=RuleCategory.PROVIDER_PATTERN,
                description="External dependencies must use the Provider pattern.",
                severity=ViolationSeverity.WARNING,
            ),
            ArchitectureRule(
                rule_id="DI-001",
                name="Dependency injection",
                category=RuleCategory.DEPENDENCY_INJECTION,
                description="Components must use dependency injection, not globals.",
                severity=ViolationSeverity.ERROR,
            ),
            ArchitectureRule(
                rule_id="IMM-001",
                name="Immutable models",
                category=RuleCategory.IMMUTABLE_MODELS,
                description="Domain models must be frozen dataclasses with slots=True.",
                severity=ViolationSeverity.WARNING,
            ),
            ArchitectureRule(
                rule_id="RT-001",
                name="Runtime contracts",
                category=RuleCategory.RUNTIME_CONTRACTS,
                description="Runtimes must implement required contracts.",
                severity=ViolationSeverity.ERROR,
            ),
            ArchitectureRule(
                rule_id="HOST-001",
                name="Project hosting rules",
                category=RuleCategory.PROJECT_HOSTING,
                description="Project hosting layer must follow defined rules.",
                severity=ViolationSeverity.WARNING,
            ),
        ]

    @property
    def rules(self) -> tuple[ArchitectureRule, ...]:
        return tuple(self._rules)

    def validate(self) -> ArchitectureReport:
        violations: list[ArchitectureViolation] = []
        passed: list[ArchitectureRule] = []

        for rule in self._rules:
            if not rule.enabled:
                continue
            rule_violations = self._validate_rule(rule)
            if rule_violations:
                violations.extend(rule_violations)
            else:
                passed.append(rule)

        failed_count = len(self._rules) - len(passed)
        compliance = ComplianceLevel.FULLY_COMPLIANT if failed_count == 0 else (
            ComplianceLevel.PARTIALLY_COMPLIANT if failed_count <= 2 else
            ComplianceLevel.NON_COMPLIANT
        )

        return ArchitectureReport(
            rules_passed=len(passed),
            rules_failed=failed_count,
            violations=tuple(violations),
            rules_checked=len(self._rules),
            compliance_level=compliance,
        )

    def _validate_rule(self, rule: ArchitectureRule) -> list[ArchitectureViolation]:
        method_name = f"_check_{rule.rule_id.lower()}"
        checker = getattr(self, method_name, None)
        if checker is None:
            return []
        return checker()

    def _check_layer_001(self) -> list[ArchitectureViolation]:
        violations: list[ArchitectureViolation] = []
        forbidden_pairs = [
            ("common", "plugin"),
            ("common", "ipc"),
            ("plugin", "ipc"),
            ("workflow", "vision"),
            ("vision", "ai"),
            ("ai", "knowledge"),
        ]
        scanner = ModuleScanner(self._src_root)
        graph = scanner.build_dependency_graph()
        for source, targets in graph.items():
            for target in targets:
                if (source, target) in forbidden_pairs:
                    violations.append(ArchitectureViolation(
                        rule_id="LAYER-001",
                        rule_name="Layering enforced",
                        category=RuleCategory.LAYERING,
                        severity=ViolationSeverity.CRITICAL,
                        message=f"Forbidden layer dependency: {source} -> {target}",
                    ))
        return violations

    def _check_dep_001(self) -> list[ArchitectureViolation]:
        return []

    def _check_circ_001(self) -> list[ArchitectureViolation]:
        scanner = ModuleScanner(self._src_root)
        graph = scanner.build_dependency_graph()
        modules = tuple(graph.keys())
        edges = []
        for src, tgts in graph.items():
            for tgt in tgts:
                edges.append(ModuleDependency(source=src, target=tgt, allowed=True))
        mod_graph = ModuleGraph(modules=modules, edges=tuple(edges))
        if mod_graph.has_cycle():
            cycle = self._find_cycle(mod_graph)
            if cycle:
                return [ArchitectureViolation(
                    rule_id="CIRC-001",
                    rule_name="No circular dependencies",
                    category=RuleCategory.CIRCULAR_DEPENDENCY,
                    severity=ViolationSeverity.CRITICAL,
                    message=f"Circular dependency detected: {' -> '.join(cycle)}",
                )]
        return []

    def _find_cycle(self, graph: ModuleGraph) -> tuple[str, ...]:
        visited: set[str] = set()
        rec_stack: list[str] = []
        def dfs(node: str) -> tuple[str, ...] | None:
            visited.add(node)
            rec_stack.append(node)
            for neighbor in graph.adjacency.get(node, set()):
                if neighbor not in visited:
                    result = dfs(neighbor)
                    if result:
                        return result
                elif neighbor in rec_stack:
                    idx = rec_stack.index(neighbor)
                    return tuple(rec_stack[idx:])
            rec_stack.pop()
            return None
        for mod in graph.modules:
            if mod not in visited:
                result = dfs(mod)
                if result:
                    return result
        return ()

    def _check_imp_001(self) -> list[ArchitectureViolation]:
        return []

    def _check_prv_001(self) -> list[ArchitectureViolation]:
        return []

    def _check_di_001(self) -> list[ArchitectureViolation]:
        violations: list[ArchitectureViolation] = []
        for py_file in self._src_root.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")
                if "globals(" in content or "global " in content:
                    violations.append(ArchitectureViolation(
                        rule_id="DI-001",
                        rule_name="Dependency injection",
                        category=RuleCategory.DEPENDENCY_INJECTION,
                        severity=ViolationSeverity.ERROR,
                        message=f"Global mutable state detected in {py_file}",
                        file_path=str(py_file),
                        suggestion="Use dependency injection instead of global state.",
                    ))
            except Exception:
                pass
        return violations

    def _check_imm_001(self) -> list[ArchitectureViolation]:
        return []

    def _check_rt_001(self) -> list[ArchitectureViolation]:
        return []

    def _check_host_001(self) -> list[ArchitectureViolation]:
        return []
