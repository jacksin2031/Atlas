"""Tests for plugin bridge."""

from __future__ import annotations
import pytest

from atlas_workflow.common import PluginError
from atlas_workflow.plugin_integration import PluginBridge


class TestPluginBridge:
    def test_register_and_execute(self):
        bridge = PluginBridge()

        def handler(node_id, configuration, inputs, metadata):
            return {"result": "ok", "node_id": node_id}

        bridge.register_handler("test-type", handler)
        output = bridge.execute_node(
            node_type="test-type",
            node_id="n1",
            configuration={},
            inputs={"key": "val"},
            node_metadata={},
        )
        assert output["result"] == "ok"
        assert output["node_id"] == "n1"

    def test_execute_unregistered_type_raises(self):
        bridge = PluginBridge()
        with pytest.raises(PluginError, match="not registered"):
            bridge.execute_node(
                node_type="unknown",
                node_id="n1",
                configuration={},
                inputs={},
                node_metadata={},
            )

    def test_unregister_handler(self):
        bridge = PluginBridge()
        bridge.register_handler("t1", lambda **kw: {})
        assert bridge.has_handler("t1")
        assert bridge.unregister_handler("t1") is True
        assert not bridge.has_handler("t1")
        assert bridge.unregister_handler("missing") is False

    def test_get_registered_types(self):
        bridge = PluginBridge()
        bridge.register_handler("t1", lambda **kw: {})
        bridge.register_handler("t2", lambda **kw: {})
        assert bridge.get_registered_types() == {"t1", "t2"}

    def test_handler_passthrough(self):
        bridge = PluginBridge()
        bridge.register_handler("echo", lambda node_id, configuration, inputs, metadata: dict(inputs))
        output = bridge.execute_node(
            node_type="echo",
            node_id="n1",
            configuration={},
            inputs={"a": 1, "b": 2},
            node_metadata={"meta": True},
        )
        assert output == {"a": 1, "b": 2}

    def test_handler_exception_wrapped(self):
        bridge = PluginBridge()
        bridge.register_handler("failing", lambda **kw: (_ for _ in ()).throw(RuntimeError("boom")))
        with pytest.raises(PluginError, match="boom"):
            bridge.execute_node(
                node_type="failing",
                node_id="n1",
                configuration={},
                inputs={},
                node_metadata={},
            )
