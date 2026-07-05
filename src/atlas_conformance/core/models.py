from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path as _Path
from typing import Any


class ViolationSeverity(Enum):
    CRITICAL = auto()
    ERROR = auto()
    WARNING = auto()
    INFO = auto()


class RuleCategory(Enum):
    LAYERING = auto()
    DEPENDENCY_DIRECTION = auto()
    CIRCULAR_DEPENDENCY = auto()
    FORBIDDEN_IMPORTS = auto()
    PROVIDER_PATTERN = auto()
    DEPENDENCY_INJECTION = auto()
    IMMUTABLE_MODELS = auto()
    RUNTIME_CONTRACTS = auto()
    PROJECT_HOSTING = auto()
    RFC_COMPLIANCE = auto()
    ADR_COMPLIANCE = auto()
    DOCUMENTATION = auto()
    MODULE_RULES = auto()
    TEST_COVERAGE = auto()
    NAMING_CONVENTIONS = auto()
    PUBLIC_API = auto()


class RFCStatus(Enum):
    DRAFT = "Draft"
    REVIEW = "Review"
    ACCEPTED = "Accepted"
    IMPLEMENTED = "Implemented"
    SUPERSEDED = "Superseded"
    FROZEN = "Frozen"


class ADRStatus(Enum):
    PROPOSED = "Proposed"
    ACCEPTED = "Accepted"
    SUPERSEDED = "Superseded"
    DEPRECATED = "Deprecated"
    ARCHIVED = "Archived"


class ComplianceLevel(Enum):
    FULLY_COMPLIANT = "Fully Compliant"
    PARTIALLY_COMPLIANT = "Partially Compliant"
    NON_COMPLIANT = "Non-Compliant"
    NEEDS_REVIEW = "Needs Review"


@dataclass(frozen=True, slots=True)
class ArchitectureRule:
    rule_id: str
    name: str
    category: RuleCategory
    description: str
    severity: ViolationSeverity
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def id(self) -> str:
        return self.rule_id


@dataclass(frozen=True, slots=True)
class ArchitectureViolation:
    rule_id: str
    rule_name: str
    category: RuleCategory
    severity: ViolationSeverity
    message: str
    file_path: str | None = None
    line_number: int | None = None
    suggestion: str | None = None
    evidence: tuple[str, ...] = ()

    @property
    def fingerprint(self) -> str:
        parts = (self.rule_id, self.message, self.file_path or "", str(self.line_number or ""))
        raw = "|".join(parts)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


@dataclass(frozen=True, slots=True)
class ArchitectureReport:
    rules_passed: int = 0
    rules_failed: int = 0
    violations: tuple[ArchitectureViolation, ...] = ()
    rules_checked: int = 0
    compliance_level: ComplianceLevel = ComplianceLevel.NEEDS_REVIEW
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_compliant(self) -> bool:
        return self.compliance_level == ComplianceLevel.FULLY_COMPLIANT


@dataclass(frozen=True, slots=True)
class RFCRequirement:
    requirement_id: str
    description: str
    normativity: str
    category: str
    accepted: bool = False
    implemented: bool = False
    tested: bool = False
    documented: bool = False
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RFCCompliance:
    rfc_id: str
    title: str
    status: RFCStatus
    total_requirements: int = 0
    met_requirements: int = 0
    requirements: tuple[RFCRequirement, ...] = ()
    compliance_percentage: float = 0.0
    is_implemented: bool = False
    is_referenced: bool = False
    is_tested: bool = False
    is_documented: bool = False

    @property
    def is_compliant(self) -> bool:
        return self.compliance_percentage >= 100.0


@dataclass(frozen=True, slots=True)
class RFCCoverage:
    total_rfcs: int = 0
    implemented_rfcs: int = 0
    referenced_rfcs: int = 0
    tested_rfcs: int = 0
    documented_rfcs: int = 0
    compliance: tuple[RFCCompliance, ...] = ()
    coverage_percentage: float = 0.0

    @property
    def is_complete(self) -> bool:
        return self.coverage_percentage >= 100.0


@dataclass(frozen=True, slots=True)
class ADRReference:
    adr_id: str
    referenced_in: str
    line_number: int | None = None
    context: str = ""


@dataclass(frozen=True, slots=True)
class ADRCompliance:
    total_adrs: int = 0
    referenced_adrs: int = 0
    deprecated_adrs: int = 0
    superseded_adrs: int = 0
    references: tuple[ADRReference, ...] = ()
    compliance_percentage: float = 0.0


@dataclass(frozen=True, slots=True)
class DocumentationCoverage:
    total_expected_docs: int = 0
    total_present_docs: int = 0
    missing_docs: tuple[str, ...] = ()
    broken_references: tuple[str, ...] = ()
    consistency_issues: tuple[str, ...] = ()
    coverage_percentage: float = 0.0


@dataclass(frozen=True, slots=True)
class ModuleDependency:
    source: str
    target: str
    allowed: bool
    reason: str = ""


@dataclass(frozen=True, slots=True)
class ModuleGraph:
    modules: tuple[str, ...] = ()
    edges: tuple[ModuleDependency, ...] = ()

    @property
    def adjacency(self) -> dict[str, set[str]]:
        adj: dict[str, set[str]] = {}
        for mod in self.modules:
            adj.setdefault(mod, set())
        for edge in self.edges:
            adj.setdefault(edge.source, set()).add(edge.target)
        return adj

    def has_cycle(self) -> bool:
        visited: set[str] = set()
        rec_stack: set[str] = set()
        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.adjacency.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.discard(node)
            return False
        for mod in self.modules:
            if mod not in visited:
                if dfs(mod):
                    return True
        return False

    def topological_sort(self) -> tuple[str, ...]:
        in_degree: dict[str, int] = {m: 0 for m in self.modules}
        adj: dict[str, list[str]] = {m: [] for m in self.modules}
        for edge in self.edges:
            if edge.source in adj and edge.target in adj:
                adj[edge.source].append(edge.target)
                in_degree[edge.target] += 1
        queue = sorted(m for m, d in in_degree.items() if d == 0)
        result: list[str] = []
        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbor in sorted(adj[node]):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    queue.sort()
        return tuple(result)


@dataclass(frozen=True, slots=True)
class ModuleRules:
    allowed_imports: tuple[tuple[str, str], ...] = ()
    forbidden_imports: tuple[tuple[str, str], ...] = ()
    public_api_patterns: tuple[str, ...] = ()
    naming_conventions: dict[str, str] = field(default_factory=dict)
    required_packages: tuple[str, ...] = ()
    required_services: tuple[str, ...] = ()
    registry_presence_required: bool = True


@dataclass(frozen=True, slots=True)
class TestCoverage:
    module_name: str
    unit_tests: int = 0
    integration_tests: int = 0
    architecture_tests: int = 0
    compliance_report: bool = False
    documentation: bool = False
    has_test_file: bool = False
    is_covered: bool = False


@dataclass(frozen=True, slots=True)
class ConformanceReport:
    architecture: ArchitectureReport | None = None
    rfc_coverage: RFCCoverage | None = None
    adr_compliance: ADRCompliance | None = None
    documentation: DocumentationCoverage | None = None
    modules: ModuleGraph | None = None
    module_rules: tuple[ArchitectureViolation, ...] = ()
    test_coverage: tuple[TestCoverage, ...] = ()
    overall_level: ComplianceLevel = ComplianceLevel.NEEDS_REVIEW
    timestamp: str = ""
    sprint: str = "11"
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_compliant(self) -> bool:
        return self.overall_level == ComplianceLevel.FULLY_COMPLIANT
