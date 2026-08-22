"""Tests for common capability model."""

from __future__ import annotations
import pytest

from atlas_workflow.common.capabilities import CapabilityRequirement, Capability, Permission


class TestCapabilityRequirement:
    def test_satisfies_same_version(self):
        req = CapabilityRequirement(name="basic", minimum_version="1.0.0")
        assert req.satisfies("1.0.0")

    def test_satisfies_higher_version(self):
        req = CapabilityRequirement(name="basic", minimum_version="1.0.0")
        assert req.satisfies("2.0.0")
        assert req.satisfies("1.5.0")

    def test_does_not_satisfy_lower_version(self):
        req = CapabilityRequirement(name="basic", minimum_version="2.0.0")
        assert not req.satisfies("1.9.9")

    def test_version_parsing(self):
        req = CapabilityRequirement(name="x", minimum_version="1.2.3")
        assert req.satisfies("1.2.3")
        assert req.satisfies("1.2.4")
        assert not req.satisfies("1.2.2")


class TestCapability:
    def test_capability_satisfies_requirement(self):
        cap = Capability(name="basic", version="2.0.0")
        req = CapabilityRequirement(name="basic", minimum_version="1.0.0")
        assert cap.satisfies(req)

    def test_capability_does_not_match_name(self):
        cap = Capability(name="advanced", version="2.0.0")
        req = CapabilityRequirement(name="basic", minimum_version="1.0.0")
        assert not cap.satisfies(req)


class TestPermission:
    def test_permission_allows_action(self):
        perm = Permission(name="execute", actions=["run", "execute"])
        assert perm.allows("execute")
        assert perm.allows("run")

    def test_permission_denies_unknown_action(self):
        perm = Permission(name="execute", actions=["run"])
        assert not perm.allows("delete")

    def test_permission_allows_specific_resource(self):
        perm = Permission(name="read", resource="db", actions=["read"])
        assert perm.allows("read", "db")
        assert not perm.allows("read", "other")

    def test_permission_wildcard_resource(self):
        perm = Permission(name="execute", resource="*", actions=["execute"])
        assert perm.allows("execute", "anything")
