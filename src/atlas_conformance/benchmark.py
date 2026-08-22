#!/usr/bin/env python3
\"\"\"Benchmark suite for Atlas Conformance & Architecture Validation.\"\"\"

import time
from pathlib import Path

from atlas_conformance._service import ArchitectureValidationService


def benchmark_validation(
    repo_root: str | Path = ".",
    src_root: str = "src",
    specs_root: str = "specs",
    tests_root: str = "tests",
    adr_root: str | None = None,
    iterations: int = 3,
) -> dict[str, float]:
    repo_root = Path(repo_root).resolve()
    src_root = repo_root / src_root
    specs_root = repo_root / specs_root
    tests_root = repo_root / tests_root
    adr_root_val = Path(adr_root).resolve() if adr_root else repo_root / "docs" / "adr"

    service = ArchitectureValidationService(
        repo_root=repo_root,
        src_root=src_root,
        specs_root=specs_root,
        tests_root=tests_root,
        adr_root=adr_root_val,
    )

    timings: dict[str, float] = {}

    start = time.monotonic()
    for _ in range(iterations):
        from atlas_conformance.validators import ArchitectureValidator
        av = ArchitectureValidator(src_root, specs_root)
        av.validate()
    timings["architecture"] = (time.monotonic() - start) / iterations

    start = time.monotonic()
    for _ in range(iterations):
        from atlas_conformance.validators import RFCValidator
        rv = RFCValidator(specs_root, src_root)
        rv.validate()
    timings["rfc"] = (time.monotonic() - start) / iterations

    start = time.monotonic()
    for _ in range(iterations):
        from atlas_conformance.validators import ADRValidator
        adv = ADRValidator(adr_root_val, specs_root)
        adv.validate()
    timings["adr"] = (time.monotonic() - start) / iterations

    start = time.monotonic()
    for _ in range(iterations):
        from atlas_conformance.validators import DocumentationValidator
        dv = DocumentationValidator(repo_root)
        dv.validate()
    timings["documentation"] = (time.monotonic() - start) / iterations

    start = time.monotonic()
    for _ in range(iterations):
        from atlas_conformance.validators import ModuleValidator
        mv = ModuleValidator(src_root)
        mv.validate()
    timings["module"] = (time.monotonic() - start) / iterations

    start = time.monotonic()
    for _ in range(iterations):
        service.run_full_validation()
    timings["full_validation"] = (time.monotonic() - start) / iterations

    return timings


def print_benchmark_report(timings: dict[str, float]) -> None:
    print("=== BENCHMARK RESULTS ===")
    print(f"{'Metric':<25} {'Time (s)':>12}")
    print("-" * 40)
    for name, t in sorted(timings.items()):
        print(f"{name:<25} {t:>12.4f}")
    print(f"{'Total':<25} {sum(timings.values()):>12.4f}")


if __name__ == "__main__":
    timings = benchmark_validation()
    print_benchmark_report(timings)
