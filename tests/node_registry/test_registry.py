"""Tests for node registry."""

from __future__ import annotations
import pytest

from atlas_workflow.common import PluginError
from atlas_workflow.node_registry import NodeRegistry, NodeDefinition


class TestNodeRegistry:
    def test_register_and_lookup(self):
        reg = NodeRegistry()
        reg.register(NodeDefinition(node_id="n1", node_type="noop"))
        result = reg.lookup("n1")
        assert result is not None
        assert result.node_id == "n1"
        assert result.node_type == "noop"

    def test_lookup_missing_returns_none(self):
        reg = NodeRegistry()
        assert reg.lookup("missing") is None

    def test_register_duplicate_raises(self):
        reg = NodeRegistry()
        reg.register(NodeDefinition(node_id="n1", node_type="noop"))
        with pytest.raises(PluginError, match="already registered"):
            reg.register(NodeDefinition(node_id="n1", node_type="transform"))

    def test_unregister(self):
        reg = NodeRegistry()
        reg.register(NodeDefinition(node_id="n1", node_type="noop"))
        assert reg.unregister("n1") is True
        assert reg.lookup("n1") is None

    def test_unregister_missing_returns_false(self):
        reg = NodeRegistry()
        assert reg.unregister("missing") is False

    def test_lookup_by_type(self):
        reg = NodeRegistry()
        reg.register(NodeDefinition(node_id="n1", node_type="noop"))
        reg.register(NodeDefinition(node_id="n2", node_type="noop"))
        reg.register(NodeDefinition(node_id="n3", node_type="transform"))
        results = reg.lookup_by_type("noop")
        assert len(results) == 2
        ids = {r.node_id for r in results}
        assert ids == {"n1", "n2"}

    def test_list_all(self):
        reg = NodeRegistry()
        reg.register(NodeDefinition(node_id="n1", node_type="a"))
        reg.register(NodeDefinition(node_id="n2", node_type="b"))
        all_defs = reg.list_all()
        assert len(all_defs) == 2

    def test_list_capabilities(self):
        reg = NodeRegistry()
        reg.register(NodeDefinition(node_id="n1", node_type="a", capabilities=["cap1", "cap2"]))
        reg.register(NodeDefinition(node_id="n2", node_type="b", capabilities=["cap2", "cap3"]))
        caps = reg.list_capabilities()
        assert set(caps) == {"cap1", "cap2", "cap3"}

    def test_filter_by_capability(self):
        reg = NodeRegistry()
        reg.register(NodeDefinition(node_id="n1", node_type="a", capabilities=["basic"]))
        reg.register(NodeDefinition(node_id="n2", node_type="b", capabilities=["advanced"]))
        results = reg.filter_by_capability("basic")
        assert len(results) == 1
        assert results[0].node_id == "n1"

    def test_filter_by_version(self):
        reg = NodeRegistry()
        reg.register(NodeDefinition(node_id="n1", node_type="a", version="1.0.0"))
        reg.register(NodeDefinition(node_id="n2", node_type="b", version="2.0.0"))
        results = reg.filter_by_version("1.5.0")
        assert len(results) == 1
        assert results[0].node_id == "n2"

    def test_filter_by_capabilities_multiple(self):
        reg = NodeRegistry()
        reg.register(NodeDefinition(node_id="n1", node_type="a", capabilities=["basic", "transform"]))
        reg.register(NodeDefinition(node_id="n2", node_type="b", capabilities=["basic"]))
        reg.register(NodeDefinition(node_id="n3", node_type="c", capabilities=["transform"]))
        results = reg.filter_by_capabilities(["basic", "transform"])
        assert len(results) == 1
        assert results[0].node_id == "n1"

    def test_node_satisfies_capabilities(self):
        defn = NodeDefinition(node_id="n1", node_type="a", capabilities=["basic", "advanced"])
        assert defn.satisfies_capabilities(["basic"])
        assert defn.satisfies_capabilities(["basic", "advanced"])
        assert not defn.satisfies_capabilities(["basic", "missing"])

    def test_node_satisfies_version(self):
        defn = NodeDefinition(node_id="n1", node_type="a", version="2.0.0")
        assert defn.satisfies_version("1.0.0")
        assert defn.satisfies_version("2.0.0")
        assert not defn.satisfies_version("3.0.0")

    def test_get_available_for_capabilities(self):
        reg = NodeRegistry()
        reg.register(NodeDefinition(node_id="n1", node_type="a", capabilities=["basic", "transform"]))
        reg.register(NodeDefinition(node_id="n2", node_type="b", capabilities=["basic"]))
        results = reg.get_available_for_capabilities(["basic"])
        assert len(results) == 2
