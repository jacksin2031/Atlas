from __future__ import annotations

import json
import tempfile
from pathlib import Path

from atlas_conformance._service import ArchitectureValidationService
from atlas_conformance.core import ComplianceLevel


class TestArchitectureValidationService:
    def test_init(self):
        svc = ArchitectureValidationService(".", "src", "specs", "tests", "docs/adr")
        assert svc._repo_root is not None
        assert svc._src_root is not None

    def test_discover_runtimes(self):
        svc = ArchitectureValidationService(".", "src", "specs", "tests", "docs/adr")
        runtimes = svc._discover_runtimes()
        assert "atlas_workflow" in runtimes

    def test_generate_json_report(self):
        svc = ArchitectureValidationService(".", "src", "specs", "tests", "docs/adr")
        report = svc.generate_json_report()
        assert report is not None
        assert report.overall_level is not None

    def test_write_json_report(self):
        svc = ArchitectureValidationService(".", "src", "specs", "tests", "docs/adr")
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, dir=".") as f:
            output_path = f.name
        path = svc.write_json_report(output_path)
        assert path == output_path
        # Verify JSON is valid
        data = json.loads(Path(output_path).read_text(encoding="utf-8"))
        assert "overall_level" in data

    def test_serialization(self):
        svc = ArchitectureValidationService(".", "src", "specs", "tests", "docs/adr")
        report = svc.generate_json_report()
        serialized = svc._serialize(report)
        assert isinstance(serialized, dict)
        assert "overall_level" in serialized
