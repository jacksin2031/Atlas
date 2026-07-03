"""Tests for health service."""

from __future__ import annotations
import pytest

from atlas_workflow.health import HealthService


class TestHealthService:
    def test_initial_state_healthy(self):
        hs = HealthService()
        assert hs.state == "Healthy"
        assert hs.is_healthy()

    def test_set_state_busy(self):
        hs = HealthService()
        hs.set_state("Busy")
        assert hs.state == "Busy"

    def test_set_state_failed(self):
        hs = HealthService()
        hs.set_state("Failed")
        assert hs.is_failed()

    def test_set_state_invalid_raises(self):
        hs = HealthService()
        with pytest.raises(ValueError, match="Invalid health state"):
            hs.set_state("InvalidState")

    def test_update_component_health(self):
        hs = HealthService()
        hs.update_component_health("executor", "Healthy")
        hs.update_component_health("scheduler", "Busy")
        report = hs.get_health_report()
        assert report["components"]["executor"] == "Healthy"
        assert report["components"]["scheduler"] == "Busy"

    def test_recompute_overall_state(self):
        hs = HealthService()
        hs.update_component_health("c1", "Failed")
        assert hs.state == "Failed"

    def test_health_report_structure(self):
        hs = HealthService()
        hs.set_state("Busy", details={"reason": "high load"})
        report = hs.get_health_report()
        assert report["state"] == "Busy"
        assert report["details"]["reason"] == "high load"
        assert "last_updated" in report
        assert "components" in report

    def test_all_valid_states(self):
        hs = HealthService()
        for state in ["Healthy", "Busy", "Paused", "Recovering", "Failed"]:
            hs.set_state(state)
            assert hs.state == state
