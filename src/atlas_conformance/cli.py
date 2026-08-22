#!/usr/bin/env python3
"""CI entry point for Atlas Conformance and Architecture Validation.

Usage:
    python -m atlas_conformance.cli [options]
"""

import argparse
import json
import sys
from pathlib import Path

from atlas_conformance._service import ArchitectureValidationService


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Atlas Conformance and Architecture Validation",
    )
    parser.add_argument("--repo-root", type=str, default=".")
    parser.add_argument("--src-root", type=str, default="src")
    parser.add_argument("--specs-root", type=str, default="specs")
    parser.add_argument("--tests-root", type=str, default="tests")
    parser.add_argument("--adr-root", type=str, default=None)
    parser.add_argument("--output", type=str, default="conformance_report.json")
    parser.add_argument("--format", choices=["json", "summary"], default="json")
    parser.add_argument("--sprint", type=str, default="11")
    parser.add_argument("--quiet", action="store_true")

    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    src_root = repo_root / args.src_root
    specs_root = repo_root / args.specs_root
    tests_root = repo_root / args.tests_root
    adr_root = Path(args.adr_root).resolve() if args.adr_root else repo_root / "docs" / "adr"

    service = ArchitectureValidationService(
        repo_root=repo_root,
        src_root=src_root,
        specs_root=specs_root,
        tests_root=tests_root,
        adr_root=adr_root,
    )

    if not args.quiet:
        print("Running Atlas Conformance and Architecture Validation...")
        print(f"  Repo:     {repo_root}")
        print(f"  Source:   {src_root}")
        print(f"  Specs:    {specs_root}")
        print(f"  Tests:    {tests_root}")
        print(f"  ADRs:     {adr_root}")
        print()

    conformance = service.run_full_validation()

    if args.format == "json":
        report_data = service.generate_json_report()
        output_path = service.write_json_report(args.output)
        if not args.quiet:
            print(f"JSON report written to: {output_path}")
    else:
        _print_summary(conformance)

    if not args.quiet:
        _print_compliance(conformance)

    exit_code = 0 if conformance.is_compliant else 1
    return exit_code


def _print_summary(conformance):
    print("=== CONFORMANCE SUMMARY ===")
    if conformance.architecture:
        arch = conformance.architecture
        print(f"Architecture: {arch.rules_passed}/{arch.rules_checked} rules passed")
        if arch.violations:
            crit = [v for v in arch.violations if v.severity.name == "CRITICAL"]
            err = [v for v in arch.violations if v.severity.name == "ERROR"]
            if crit:
                print(f"  CRITICAL violations: {len(crit)}")
            if err:
                print(f"  ERROR violations: {len(err)}")

    if conformance.rfc_coverage:
        rfc = conformance.rfc_coverage
        print(f"RFC Coverage: {rfc.implemented_rfcs}/{rfc.total_rfcs} implemented ({rfc.coverage_percentage:.1f}%)")

    if conformance.adr_compliance:
        adr = conformance.adr_compliance
        print(f"ADR Compliance: {adr.referenced_adrs}/{adr.total_adrs} referenced ({adr.compliance_percentage:.1f}%)")

    if conformance.documentation:
        doc = conformance.documentation
        print(f"Documentation: {doc.total_present_docs}/{doc.total_expected_docs} present ({doc.coverage_percentage:.1f}%)")


def _print_compliance(conformance):
    print()
    print(f"Overall: {conformance.overall_level.value}")
    print(f"Sprint:  {conformance.sprint}")
    if conformance.metadata.get("validation_seconds"):
        print(f"Time:    {conformance.metadata['validation_seconds']}s")


if __name__ == "__main__":
    sys.exit(main())
