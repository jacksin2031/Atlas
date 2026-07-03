"""Tests for metrics collector."""

from __future__ import annotations
import pytest

from atlas_workflow.metrics import MetricsCollector


class TestMetricsCollector:
    def test_record_execution_completed(self):
        mc = MetricsCollector()
        mc.record_execution_started()
        mc.record_execution_completed(100.0)
        assert mc.execution_count == 1
        assert mc.success_count == 1
        assert mc.failure_count == 0

    def test_record_execution_failed(self):
        mc = MetricsCollector()
        mc.record_execution_started()
        mc.record_execution_failed(50.0)
        assert mc.execution_count == 1
        assert mc.success_count == 0
        assert mc.failure_count == 1

    def test_average_execution_duration(self):
        mc = MetricsCollector()
        mc.record_execution_completed(100.0)
        mc.record_execution_completed(200.0)
        avg = mc.get_average_execution_duration_ms()
        assert avg == 150.0

    def test_no_average_when_empty(self):
        mc = MetricsCollector()
        assert mc.get_average_execution_duration_ms() is None

    def test_node_duration_stats(self):
        mc = MetricsCollector()
        mc.record_node_duration("n1", 10.0)
        mc.record_node_duration("n1", 20.0)
        stats = mc.get_node_duration_stats("n1")
        assert stats["count"] == 2
        assert stats["avg"] == 15.0
        assert stats["min"] == 10.0
        assert stats["max"] == 20.0

    def test_node_no_stats(self):
        mc = MetricsCollector()
        stats = mc.get_node_duration_stats("missing")
        assert stats["count"] == 0
        assert stats["avg"] is None

    def test_queue_latency(self):
        mc = MetricsCollector()
        mc.record_queue_latency(5.0)
        mc.record_queue_latency(10.0)
        assert mc.get_total_queue_latency_ms() == 15.0
        assert mc.get_average_queue_latency_ms() == 7.5

    def test_retry_counts(self):
        mc = MetricsCollector()
        mc.record_retry("n1")
        mc.record_retry("n1")
        mc.record_retry("n2")
        assert mc.retry_counts["n1"] == 2
        assert mc.retry_counts["n2"] == 1

    def test_parallel_branch_count(self):
        mc = MetricsCollector()
        mc.record_parallel_branch(3)
        mc.record_parallel_branch(5)
        assert mc.get_average_parallel_branch_count() == 4.0

    def test_to_dict(self):
        mc = MetricsCollector()
        mc.record_execution_started()
        mc.record_execution_completed(100.0)
        mc.record_node_duration("n1", 50.0)
        d = mc.to_dict()
        assert d["execution_count"] == 1
        assert d["success_count"] == 1
        assert "n1" in d["node_durations"]
        assert d["node_durations"]["n1"]["count"] == 1

    def test_reset(self):
        mc = MetricsCollector()
        mc.record_execution_completed(100.0)
        mc.reset()
        assert mc.execution_count == 0
        assert mc.success_count == 0
        assert mc.get_average_execution_duration_ms() is None
