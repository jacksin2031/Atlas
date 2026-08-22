from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from atlas_conformance.core import (
    ArchitectureReport,
    ComplianceLevel,
    ConformanceReport,
    DocumentationCoverage,
    ModuleGraph,
    RFCCoverage,
    ADRCompliance,
    TestCoverage,
)
from atlas_conformance.reports.models import (
    ArchitectureReportData,
    ADRCoverageReportData,
    DocumentationReportData,
    ModuleReportData,
    OverallComplianceReportData,
    RFCCoverageReportData,
)
from atlas_conformance.validators import (
    ArchitectureValidator,
    ADRValidator,
    DocumentationValidator,
    ModuleValidator,
    RFCValidator,
    RuntimeContractValidator,
    TestCoverageValidator,
)


class ArchitectureValidationService:
    def __init__(
        self,
        repo_root: str | Path,
        src_root: str | Path,
        specs_root: str | Path,
        tests_root: str | Path | None = None,
        adr_root: str | Path | None = None,
    ) -> None:
        self._repo_root = Path(repo_root)
        self._src_root = Path(src_root)
        self._specs_root = Path(specs_root)
        self._tests_root = Path(tests_root) if tests_root else self._repo_root / "tests"
        self._adr_root = Path(adr_root) if adr_root else self._repo_root / "docs" / "adr"

    def run_full_validation(self) -> ConformanceReport:
        start_time = time.monotonic()

        arch_validator = ArchitectureValidator(self._src_root, self._specs_root)
        arch_report = arch_validator.validate()

        rfc_validator = RFCValidator(self._specs_root, self._src_root)
        rfc_coverage = rfc_validator.validate()

        adr_validator = ADRValidator(self._adr_root, self._specs_root)
        adr_compliance = adr_validator.validate()

        doc_validator = DocumentationValidator(self._repo_root)
        doc_coverage = doc_validator.validate()

        module_validator = ModuleValidator(self._src_root)
        module_graph, module_violations = module_validator.validate()

        test_validator = TestCoverageValidator(self._src_root, self._tests_root)
        test_coverage = test_validator.validate()

        runtime_violations: list[Any] = []
        runtimes = self._discover_runtimes()
        for runtime_name in runtimes:
            rt_validator = RuntimeContractValidator(self._src_root)
            _, violations = rt_validator.validate(runtime_name)
            runtime_violations.extend(violations)

        elapsed = time.monotonic() - start_time

        overall = self._compute_overall_compliance(
            arch_report, rfc_coverage, adr_compliance,
            doc_coverage, module_graph, test_coverage,
        )

        return ConformanceReport(
            architecture=arch_report,
            rfc_coverage=rfc_coverage,
            adr_compliance=adr_compliance,
            documentation=doc_coverage,
            modules=module_graph,
            module_rules=module_violations,
            test_coverage=test_coverage,
            overall_level=overall,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata={"validation_seconds": round(elapsed, 3)},
        )

    def _discover_runtimes(self) -> list[str]:
        runtimes: list[str] = []
        if not self._src_root.exists():
            return runtimes
        for pkg in self._src_root.iterdir():
            if pkg.is_dir() and (pkg / "__init__.py").exists():
                if pkg.name.startswith("atlas_"):
                    runtimes.append(pkg.name)
        return runtimes

    def _compute_overall_compliance(
        self,
        arch: ArchitectureReport,
        rfc: RFCCoverage,
        adr: ADRCompliance,
        doc: DocumentationCoverage,
        modules: ModuleGraph,
        tests: tuple[TestCoverage, ...],
    ) -> ComplianceLevel:
        critical_violations = 0
        for v in arch.violations:
            if v.severity.name in ("CRITICAL", "ERROR"):
                critical_violations += 1

        if critical_violations == 0 and rfc.coverage_percentage >= 90 and doc.coverage_percentage >= 90:
            return ComplianceLevel.FULLY_COMPLIANT
        elif critical_violations <= 3:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT

    def generate_json_report(self) -> OverallComplianceReportData:
        conformance = self.run_full_validation()

        arch_data = None
        if conformance.architecture:
            arch_data = ArchitectureReportData(
                total_rules=conformance.architecture.rules_checked,
                passed_rules=conformance.architecture.rules_passed,
                failed_rules=conformance.architecture.rules_failed,
                violations=tuple({
                    "rule_id": v.rule_id,
                    "rule_name": v.rule_name,
                    "category": v.category.name,
                    "severity": v.severity.name,
                    "message": v.message,
                    "file_path": v.file_path,
                    "suggestion": v.suggestion,
                } for v in conformance.architecture.violations),
                compliance_level=conformance.architecture.compliance_level.value,
            )

        rfc_data = None
        if conformance.rfc_coverage:
            rfc_data = RFCCoverageReportData(
                total_rfcs=conformance.rfc_coverage.total_rfcs,
                implemented=conformance.rfc_coverage.implemented_rfcs,
                referenced=conformance.rfc_coverage.referenced_rfcs,
                tested=conformance.rfc_coverage.tested_rfcs,
                documented=conformance.rfc_coverage.documented_rfcs,
                coverage_pct=conformance.rfc_coverage.coverage_percentage,
                rfc_details=tuple({
                    "rfc_id": c.rfc_id,
                    "title": c.title,
                    "status": c.status.value,
                    "compliance_pct": c.compliance_percentage,
                    "is_implemented": c.is_implemented,
                } for c in conformance.rfc_coverage.compliance),
            )

        adr_data = None
        if conformance.adr_compliance:
            adr_data = ADRCoverageReportData(
                total_adrs=conformance.adr_compliance.total_adrs,
                referenced=conformance.adr_compliance.referenced_adrs,
                deprecated=conformance.adr_compliance.deprecated_adrs,
                superseded=conformance.adr_compliance.superseded_adrs,
                compliance_pct=conformance.adr_compliance.compliance_percentage,
                references=tuple({
                    "adr_id": r.adr_id,
                    "referenced_in": r.referenced_in,
                    "line_number": r.line_number,
                } for r in conformance.adr_compliance.references),
            )

        doc_data = None
        if conformance.documentation:
            doc_data = DocumentationReportData(
                expected_docs=conformance.documentation.total_expected_docs,
                present_docs=conformance.documentation.total_present_docs,
                missing_docs=conformance.documentation.missing_docs,
                broken_refs=conformance.documentation.broken_references,
                consistency_issues=conformance.documentation.consistency_issues,
                coverage_pct=conformance.documentation.coverage_percentage,
            )

        mod_data = None
        if conformance.modules:
            mod_data = ModuleReportData(
                modules=conformance.modules.modules,
                edges=tuple({
                    "source": e.source,
                    "target": e.target,
                    "allowed": e.allowed,
                } for e in conformance.modules.edges),
                has_cycles=conformance.modules.has_cycle(),
            )

        return OverallComplianceReportData(
            architecture=arch_data,
            rfc_coverage=rfc_data,
            adr_compliance=adr_data,
            documentation=doc_data,
            modules=mod_data,
            overall_level=conformance.overall_level.value,
            sprint=conformance.sprint,
            timestamp=conformance.timestamp,
        )

    def write_json_report(self, output_path: str | Path) -> str:
        report = self.generate_json_report()
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(self._serialize(report), indent=2), encoding="utf-8")
        return str(output)

    @staticmethod
    def _serialize(obj: Any) -> Any:
        if hasattr(obj, "__dataclass_fields__"):
            return {k: ArchitectureValidationService._serialize(getattr(obj, k)) for k in obj.__dataclass_fields__}
        if hasattr(obj, "__dict__") and not isinstance(obj, type):
            d = obj.__dict__
            if not d:
                return str(obj)
            return {k: ArchitectureValidationService._serialize(v) for k, v in d.items()}
        if isinstance(obj, dict):
            return {k: ArchitectureValidationService._serialize(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [ArchitectureValidationService._serialize(item) for item in obj]
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Enum):
            return obj.value
        return obj
