from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core import (
    RFCCompliance,
    RFCRequirement,
    RFCCoverage,
    RFCStatus,
)
from ..scanners.rfc_scanner import RFCMetadata, RFCScanner


class RFCValidator:
    def __init__(self, specs_root: str | Path, src_root: str | Path) -> None:
        self._specs_root = Path(specs_root)
        self._src_root = Path(src_root)
        self._scanner = RFCScanner(self._specs_root)

    def validate(self) -> RFCCoverage:
        rfcs = self._scanner.scan()
        if not rfcs:
            return RFCCoverage(total_rfcs=0, coverage_percentage=0.0)

        compliance_list: list[RFCCompliance] = []
        implemented_count = 0
        referenced_count = 0
        tested_count = 0
        documented_count = 0

        for rfc_meta in rfcs:
            rfc_comp = self._validate_single_rfc(rfc_meta)
            compliance_list.append(rfc_comp)
            if rfc_comp.is_implemented:
                implemented_count += 1
            if rfc_comp.is_referenced:
                referenced_count += 1
            if rfc_comp.is_tested:
                tested_count += 1
            if rfc_comp.is_documented:
                documented_count += 1

        total = len(rfcs)
        avg_coverage = (implemented_count + referenced_count + tested_count + documented_count) / (total * 4) * 100 if total > 0 else 0.0

        return RFCCoverage(
            total_rfcs=total,
            implemented_rfcs=implemented_count,
            referenced_rfcs=referenced_count,
            tested_rfcs=tested_count,
            documented_rfcs=documented_count,
            compliance=tuple(compliance_list),
            coverage_percentage=round(avg_coverage, 2),
        )

    def _validate_single_rfc(self, rfc: RFCMetadata) -> RFCCompliance:
        is_implemented = self._check_implementation(rfc)
        is_referenced = self._check_reference(rfc)
        is_tested = self._check_testing(rfc)
        is_documented = self._check_documentation(rfc)

        requirements = self._extract_requirements(rfc)
        met = sum(1 for req in requirements if req.implemented) if requirements else 0
        pct = (met / len(requirements) * 100) if requirements else 100.0

        status_map = {
            "Draft": RFCStatus.DRAFT,
            "Review": RFCStatus.REVIEW,
            "Accepted": RFCStatus.ACCEPTED,
            "Implemented": RFCStatus.IMPLEMENTED,
            "Superseded": RFCStatus.SUPERSEDED,
            "Frozen": RFCStatus.FROZEN,
        }
        status = status_map.get(rfc.status, RFCStatus.DRAFT)

        return RFCCompliance(
            rfc_id=rfc.rfc_id,
            title=rfc.title,
            status=status,
            total_requirements=len(requirements),
            met_requirements=met,
            requirements=requirements,
            compliance_percentage=round(pct, 2),
            is_implemented=is_implemented,
            is_referenced=is_referenced,
            is_tested=is_tested,
            is_documented=is_documented,
        )

    def _check_implementation(self, rfc: RFCMetadata) -> bool:
        rfc_num = rfc.rfc_id.split("-")[1] if "-" in rfc.rfc_id else ""
        if not rfc_num:
            return False
        for py_file in self._src_root.rglob("*.py"):
            try:
                text = py_file.read_text(encoding="utf-8", errors="ignore").lower()
                if rfc_num.lower() in text:
                    return True
            except Exception:
                pass
        return False

    def _check_reference(self, rfc: RFCMetadata) -> bool:
        rfc_ref = rfc.rfc_id
        for md_file in self._specs_root.rglob("*.md"):
            try:
                text = md_file.read_text(encoding="utf-8")
                if rfc_ref in text:
                    return True
            except Exception:
                pass
        return False

    def _check_testing(self, rfc: RFCMetadata) -> bool:
        rfc_num = rfc.rfc_id.split("-")[1] if "-" in rfc.rfc_id else ""
        tests_root = Path(self._src_root).parent / "tests"
        if not tests_root.exists():
            return False
        for test_file in tests_root.rglob("*.py"):
            try:
                text = test_file.read_text(encoding="utf-8", errors="ignore").lower()
                if rfc_num.lower() in text:
                    return True
            except Exception:
                pass
        return False

    def _check_documentation(self, rfc: RFCMetadata) -> bool:
        docs_root = Path(self._src_root).parent / "docs"
        if not docs_root.exists():
            return False
        for doc_file in docs_root.rglob("*.md"):
            try:
                text = doc_file.read_text(encoding="utf-8")
                if rfc.rfc_id in text:
                    return True
            except Exception:
                pass
        return False

    def _extract_requirements(self, rfc: RFCMetadata) -> tuple[RFCRequirement, ...]:
        if not rfc.requirements:
            return ()
        reqs: list[RFCRequirement] = []
        for i, desc in enumerate(rfc.requirements):
            lower_desc = desc.lower()
            norm = "MUST" if "must" in lower_desc else (
                "SHOULD" if "should" in lower_desc else "MAY"
            )
            reqs.append(RFCRequirement(
                requirement_id=f"{rfc.rfc_id}-REQ-{i+1:03d}",
                description=desc,
                normativity=norm,
                category=rfc.category,
            ))
        return tuple(reqs)
