"""Tests for scheduler integration."""

from __future__ import annotations
import pytest

from atlas_workflow.scheduler import (
    TriggerType,
    ScheduleConfig,
    InMemoryScheduler,
)


class TestTriggerType:
    def test_all_trigger_types_exist(self):
        expected = [
            "Immediate", "Scheduled", "Interval", "Cron",
            "Manual", "EventTrigger", "AITrigger",
        ]
        actual = [t.value for t in TriggerType]
        for exp in expected:
            assert exp in actual


class TestScheduleConfig:
    def test_immediate_config(self):
        config = ScheduleConfig(trigger_type=TriggerType.IMMEDIATE)
        assert config.trigger_type == TriggerType.IMMEDIATE

    def test_scheduled_config(self):
        from datetime import datetime, timezone
        dt = datetime.now(timezone.utc)
        config = ScheduleConfig(
            trigger_type=TriggerType.SCHEDULED,
            scheduled_at=dt,
        )
        assert config.scheduled_at == dt

    def test_cron_config(self):
        config = ScheduleConfig(
            trigger_type=TriggerType.CRON,
            cron_expression="0 0 * * *",
        )
        assert config.cron_expression == "0 0 * * *"


class TestInMemoryScheduler:
    def test_schedule_immediate(self):
        sched = InMemoryScheduler()
        config = ScheduleConfig(trigger_type=TriggerType.IMMEDIATE)
        result = sched.schedule("wf-1", config)
        assert result.schedule_id is not None
        assert result.workflow_id == "wf-1"
        assert result.status == "pending"

    def test_schedule_multiple(self):
        sched = InMemoryScheduler()
        config = ScheduleConfig(trigger_type=TriggerType.MANUAL)
        r1 = sched.schedule("wf-1", config)
        r2 = sched.schedule("wf-2", config)
        assert r1.schedule_id != r2.schedule_id

    def test_cancel_existing(self):
        sched = InMemoryScheduler()
        config = ScheduleConfig(trigger_type=TriggerType.IMMEDIATE)
        result = sched.schedule("wf-1", config)
        assert sched.cancel(result.schedule_id) is True
        assert result.status == "cancelled"

    def test_cancel_missing(self):
        sched = InMemoryScheduler()
        assert sched.cancel("nonexistent") is False

    def test_get_scheduled(self):
        sched = InMemoryScheduler()
        config = ScheduleConfig(trigger_type=TriggerType.IMMEDIATE)
        result = sched.schedule("wf-1", config)
        fetched = sched.get_scheduled(result.schedule_id)
        assert fetched is not None
        assert fetched.workflow_id == "wf-1"

    def test_get_scheduled_missing(self):
        sched = InMemoryScheduler()
        assert sched.get_scheduled("nonexistent") is None

    def test_list_all(self):
        sched = InMemoryScheduler()
        config = ScheduleConfig(trigger_type=TriggerType.IMMEDIATE)
        sched.schedule("wf-1", config)
        sched.schedule("wf-2", config)
        all_sched = sched.list_all()
        assert len(all_sched) == 2

    def test_mark_executed(self):
        sched = InMemoryScheduler()
        config = ScheduleConfig(trigger_type=TriggerType.IMMEDIATE)
        result = sched.schedule("wf-1", config)
        assert sched.mark_executed(result.schedule_id) is True
        assert result.status == "executed"
        assert result.executed_at is not None

    def test_mark_executed_missing(self):
        sched = InMemoryScheduler()
        assert sched.mark_executed("nonexistent") is False
