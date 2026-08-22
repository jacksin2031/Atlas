"""Tests for storage abstraction."""

from __future__ import annotations
import pytest

from atlas_workflow.storage import StorageAbstraction


class TestStorageAbstraction:
    def test_save_and_load_snapshot(self):
        storage = StorageAbstraction()
        storage.save_snapshot("inst-1", {"data": "value"})
        result = storage.load_snapshot("inst-1")
        assert result is not None
        assert result["data"] == "value"

    def test_load_missing_snapshot(self):
        storage = StorageAbstraction()
        assert storage.load_snapshot("missing") is None

    def test_save_and_load_checkpoint(self):
        storage = StorageAbstraction()
        storage.save_checkpoint("inst-1", "cp-1", {"checkpoint": True})
        result = storage.load_checkpoint("inst-1", "cp-1")
        assert result is not None
        assert result["checkpoint"] is True

    def test_save_history_entry(self):
        storage = StorageAbstraction()
        entry = {"event_type": "started", "timestamp": "2026-01-01"}
        storage.save_history_entry("inst-1", entry)
        # Just verify no exception

    def test_save_and_load_recovery_metadata(self):
        storage = StorageAbstraction()
        storage.save_recovery_metadata("inst-1", {"state": "paused"})
        result = storage.load_recovery_metadata("inst-1")
        assert result is not None
        assert result["state"] == "paused"

    def test_delete_instance_data(self):
        storage = StorageAbstraction()
        storage.save_snapshot("inst-1", {"data": "value"})
        storage.save_checkpoint("inst-1", "cp-1", {"cp": True})
        storage.save_recovery_metadata("inst-1", {"state": "running"})
        storage.save_history_entry("inst-1", {"event_type": "started", "timestamp": "now"})
        storage.delete_instance_data("inst-1")
        assert storage.load_snapshot("inst-1") is None
        assert storage.load_checkpoint("inst-1", "cp-1") is None
        assert storage.load_recovery_metadata("inst-1") is None

    def test_list_snapshots(self):
        storage = StorageAbstraction()
        storage.save_snapshot("inst-1", {})
        storage.save_snapshot("inst-2", {})
        snaps = storage.list_snapshots()
        assert "inst-1" in snaps
        assert "inst-2" in snaps

    def test_list_checkpoints(self):
        storage = StorageAbstraction()
        storage.save_checkpoint("inst-1", "cp-1", {})
        storage.save_checkpoint("inst-1", "cp-2", {})
        cps = storage.list_checkpoints("inst-1")
        assert "cp-1" in cps
        assert "cp-2" in cps
