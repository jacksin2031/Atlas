from __future__ import annotations

import pytest

from atlas_input import InputService, TestInputProvider
from atlas_input.safety import InputSafetyController
from atlas_workflow.host import DesktopWorkflowHost


def host():
    value = DesktopWorkflowHost(InputService(TestInputProvider(), InputSafetyController()))
    value.write = lambda message: None
    return value


def registration(plugin="package.one"):
    return {"pluginId": plugin, "typeName": plugin + ".echo", "nodeId": plugin + ".definition", "label": "Package Echo", "capabilities": ["workflow"]}


def test_runtime_bridge_preserves_typed_result_and_identity():
    value = host()
    calls = []
    def request(bridge, command, payload, timeout):
        calls.append((bridge, command, payload, timeout))
        return {"value": {"typed": 17}}
    value.bridge.request = request
    value.sync_marketplace({"revision": 1, "registrations": [registration()]})
    result = value.runtime.plugin_bridge.execute_node("package.one.echo", "n", {}, {"input": "ATLAS_MARKETPLACE_1700"}, {})
    assert result == {"value": {"typed": 17}}
    assert calls[0][0:2] == ("plugin", "execute")
    assert calls[0][2]["pluginId"] == "package.one"


def test_disable_uninstall_reenable_and_ownership():
    value = host()
    value.sync_marketplace({"revision": 1, "registrations": [registration(), registration("package.two")]})
    value.sync_marketplace({"revision": 2, "registrations": [registration("package.two")]})
    assert not value.runtime.plugin_bridge.has_handler("package.one.echo")
    assert value.runtime.plugin_bridge.has_handler("package.two.echo")
    value.sync_marketplace({"revision": 3, "registrations": [registration(), registration("package.two")]})
    value.sync_marketplace({"revision": 3, "registrations": [registration(), registration("package.two")]})
    assert len(value.runtime.node_registry.lookup_by_type("package.one.echo")) == 1
    value.sync_marketplace({"revision": 1, "registrations": []})
    assert value.runtime.plugin_bridge.has_handler("package.one.echo")


def test_missing_workflow_is_preserved_and_structured():
    value = host()
    definition = {"nodes": [{"id": "n", "type": "package.one.echo", "metadata": {"plugin_id": "package.one"}}]}
    assert "PLUGIN_UNAVAILABLE" in value.validate(definition)["errors"][0]
    assert definition["nodes"][0]["type"] == "package.one.echo"


def test_duplicate_and_foreign_ownership_are_atomic():
    value = host()
    value.sync_marketplace({"revision": 1, "registrations": [registration()]})
    with pytest.raises(RuntimeError):
        value.sync_marketplace({"revision": 2, "registrations": [registration(), registration()]})
    assert value.runtime.plugin_bridge.has_handler("package.one.echo")


def test_package_registration_never_arms_input():
    value = host()
    value.sync_marketplace({"revision": 1, "registrations": [registration()]})
    assert value.input_service.safety_status()["armed"] is False
    value.input_service.emergency_stop()
    assert value.input_service.safety_status()["armed"] is False


def test_invalid_registration_metadata_keeps_previous_registry():
    value = host()
    value.sync_marketplace({"revision": 1, "registrations": [registration()]})
    invalid = registration("package.two")
    del invalid["label"]
    with pytest.raises(KeyError):
        value.sync_marketplace({"revision": 2, "registrations": [invalid]})
    assert value.runtime.plugin_bridge.has_handler("package.one.echo")
    assert not value.runtime.plugin_bridge.has_handler("package.two.echo")


def test_registration_preserves_updated_runtime_version():
    value = host()
    value.sync_marketplace({"revision": 1, "registrations": [{**registration(), "version": "1.1.0"}]})
    assert value.runtime.node_registry.lookup_by_type("package.one.echo")[0].version == "1.1.0"


def test_runtime_error_is_structured_and_host_survives():
    value = host()
    def request(*args, **kwargs):
        raise RuntimeError('{"code":"PERMISSION_DENIED","message":"Denied by Plugin Runtime"}')
    value.bridge.request = request
    value.sync_marketplace({"revision": 1, "registrations": [registration()]})
    with pytest.raises(Exception) as error:
        value.runtime.plugin_bridge.execute_node("package.one.echo", "n", {}, {}, {})
    assert error.value.details["code"] == "PERMISSION_DENIED"
    assert value.runtime.plugin_bridge.has_handler("entry")
