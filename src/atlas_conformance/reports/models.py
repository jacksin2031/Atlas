from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ArchitectureReportData:
    total_rules: int = 0
    passed_rules: int = 0
    failed_rules: int = 0
    violations: tuple[dict[str, Any], ...] = ()
    compliance_level: str = "Needs Review"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RFCCoverageReportData:
    total_rfcs: int = 0
    implemented: int = 0
    referenced: int = 0
    tested: int = 0
    documented: int = 0
    coverage_pct: float = 0.0
    rfc_details: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ADRCoverageReportData:
    total_adrs: int = 0
    referenced: int = 0
    deprecated: int = 0
    superseded: int = 0
    compliance_pct: float = 0.0
    references: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DocumentationReportData:
    expected_docs: int = 0
    present_docs: int = 0
    missing_docs: tuple[str, ...] = ()
    broken_refs: tuple[str, ...] = ()
    consistency_issues: tuple[str, ...] = ()
    coverage_pct: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ModuleReportData:
    modules: tuple[str, ...] = ()
    edges: tuple[dict[str, Any], ...] = ()
    has_cycles: bool = False
    forbidden_imports: tuple[dict[str, Any], ...] = ()
    naming_violations: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class OverallComplianceReportData:
    architecture: ArchitectureReportData | None = None
    rfc_coverage: RFCCoverageReportData | None = None
    adr_compliance: ADRCoverageReportData | None = None
    documentation: DocumentationReportData | None = None
    modules: ModuleReportData | None = None
    overall_level: str = "Needs Review"
    sprint: str = "11"
    timestamp: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_compliant(self) -> bool:
        return self.overall_level == "Fully Compliant"
