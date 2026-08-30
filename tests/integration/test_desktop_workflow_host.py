from __future__ import annotations

import time
from typing import Any

from atlas_input import InputService, TestInputProvider
from atlas_input.contracts import MouseClickRequest, MouseMoveRequest
from atlas_workflow.host import DesktopWorkflowHost


def node(node_id: str, node_type: str, *, inputs=(), outputs=(), config=None) -> dict[str, Any]:
    return {
        "id": node_id, "type": node_type, "config": config or {},
        "inputs": list(inputs), "outputs": list(outputs),
        "ports_in": [f"{node_id}:in:{index}" for index, _ in enumerate(inputs)],
        "ports_out": [f"{node_id}:out:{index}" for index, _ in enumerate(outputs)],
        "metadata": {
            "input_ports": {f"{node_id}:in:{index}": name for index, name in enumerate(inputs)},
            "output_ports": {f"{node_id}:out:{index}": name for index, name in enumerate(outputs)},
            "input_port_types": {f"{node_id}:in:{index}": "any" for index, _ in enumerate(inputs)},
            "output_port_types": {f"{node_id}:out:{index}": "any" for index, _ in enumerate(outputs)},
        },
    }


def edge(source: str, target: str, source_index=0, target_index=0) -> dict[str, Any]:
    return {
        "source": source, "target": target,
        "source_port": f"{source}:out:{source_index}",
        "target_port": f"{target}:in:{target_index}",
    }


def definition(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], exits: list[str]) -> dict[str, Any]:
    return {
        "name": "desktop-acceptance", "version": "1.0.0",
        "metadata": {"name": "desktop-acceptance"},
        "nodes": nodes, "edges": edges, "variables": [],
        "entry_nodes": [item["id"] for item in nodes if item["type"] == "entry"],
        "exit_nodes": exits,
    }


def host() -> tuple[DesktopWorkflowHost, list[dict[str, Any]]]:
    value = DesktopWorkflowHost()
    messages: list[dict[str, Any]] = []
    value.write = messages.append  # type: ignore[method-assign]
    value.bridge._write = messages.append
    return value, messages


def wait_result(value: DesktopWorkflowHost, execution_id: str, timeout=3.0) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = value.result(execution_id)["result"]
        if result is not None:
            return result
        time.sleep(0.01)
    raise AssertionError("workflow did not finish")


def test_real_backend_edge_propagation_and_output() -> None:
    value, messages = host()
    manifest = definition(
        [node("entry", "entry", outputs=("output",)), node("constant", "constant", inputs=("trigger",), outputs=("value",), config={"value": "Atlas"}), node("transform", "transform", inputs=("input",), outputs=("value",)), node("output", "output", inputs=("input",), outputs=("value",)), node("exit", "exit", inputs=("input",))],
        [edge("entry", "constant"), edge("constant", "transform"), edge("transform", "output"), edge("output", "exit")], ["exit"],
    )
    started = value.start({"definition": manifest})
    result = wait_result(value, started["executionId"])
    assert result["success"] is True
    assert result["output"] == {"value": "Atlas"}
    event_types = [item["payload"]["eventType"] for item in messages if item.get("kind") == "event"]
    assert "NodeStarted" in event_types
    assert "NodeCompleted" in event_types
    assert "WorkflowCompleted" in event_types


def test_condition_executes_only_selected_branch() -> None:
    value, _ = host()
    nodes = [
        node("entry", "entry", outputs=("output",)),
        node("constant", "constant", inputs=("trigger",), outputs=("value",), config={"value": True}),
        node("condition", "condition", inputs=("input",), outputs=("true", "false")),
        node("true_output", "output", inputs=("input",), outputs=("value",)),
        node("false_output", "output", inputs=("input",), outputs=("value",)),
        node("true_exit", "exit", inputs=("input",)), node("false_exit", "exit", inputs=("input",)),
    ]
    manifest = definition(nodes, [
        edge("entry", "constant"), edge("constant", "condition"),
        edge("condition", "true_output", 0), edge("condition", "false_output", 1),
        edge("true_output", "true_exit"), edge("false_output", "false_exit"),
    ], ["true_exit", "false_exit"])
    execution_id = value.start({"definition": manifest})["executionId"]
    result = wait_result(value, execution_id)
    state = value.result(execution_id)["state"]
    assert result["output"] == {"value": True}
    assert state["nodeStates"]["true_output"] == "completed"
    assert state["nodeStates"]["false_output"] == "skipped"
    assert state["nodeStates"]["false_exit"] == "skipped"


def test_pause_step_resume_cancel_and_restart() -> None:
    value, _ = host()
    manifest = definition(
        [node("entry", "entry", outputs=("output",)), node("delay", "delay", inputs=("input",), outputs=("value",), config={"seconds": 0.15}), node("output", "output", inputs=("input",), outputs=("value",)), node("exit", "exit", inputs=("input",))],
        [edge("entry", "delay"), edge("delay", "output"), edge("output", "exit")], ["exit"],
    )
    execution_id = value.start({"definition": manifest})["executionId"]
    assert value.control(execution_id, "pause")
    time.sleep(0.2)
    assert value._state(execution_id)["status"] == "paused"
    assert value.control(execution_id, "step")
    time.sleep(0.05)
    assert value.control(execution_id, "resume")
    assert wait_result(value, execution_id)["success"] is True
    restarted = value.restart(execution_id)
    assert restarted["executionId"] != execution_id
    assert wait_result(value, restarted["executionId"])["success"] is True

    slow = definition([node("entry", "entry", outputs=("output",)), node("delay", "delay", inputs=("input",), outputs=("value",), config={"seconds": 2}), node("exit", "exit", inputs=("input",))], [edge("entry", "delay"), edge("delay", "exit")], ["exit"])
    cancelled_id = value.start({"definition": slow})["executionId"]
    time.sleep(0.05)
    assert value.control(cancelled_id, "stop")
    cancelled = wait_result(value, cancelled_id)
    assert cancelled["status"] == "cancelled"


def test_provider_emergency_stop_cancels_active_workflow_and_releases_input() -> None:
    provider = TestInputProvider()
    service = InputService(provider)
    value = DesktopWorkflowHost(input_service=service)
    manifest = definition(
        [
            node("entry", "entry", outputs=("output",)),
            node("move", "mouse_move", inputs=("trigger",), outputs=("result",), config={"x": 400, "y": 300}),
            node("delay", "delay", inputs=("input",), outputs=("value",), config={"seconds": 2}),
            node("exit", "exit", inputs=("input",)),
        ],
        [edge("entry", "move"), edge("move", "delay"), edge("delay", "exit")],
        ["exit"],
    )
    execution_id = value.start({"definition": manifest})["executionId"]
    time.sleep(0.05)
    status = service.emergency_stop()
    result = wait_result(value, execution_id)
    assert status["armed"] is False
    assert status["emergencyStopped"] is True
    assert result["status"] == "cancelled"
    assert provider.requests[-1].__class__.__name__ == "InputReleaseAllRequest"


def test_ai_and_plugin_nodes_use_runtime_bridges_and_errors_recover() -> None:
    value, _ = host()
    calls: list[tuple[str, str, dict[str, Any]]] = []
    value.bridge.request = lambda bridge, command, payload, timeout=180: calls.append((bridge, command, payload)) or {"content": "ATLAS_OK", "usage": {"totalTokens": 3}}  # type: ignore[method-assign]
    manifest = definition(
        [node("entry", "entry", outputs=("output",)), node("ai", "ai_inference", inputs=("prompt",), outputs=("text", "response"), config={"providerId": "provider", "modelId": "model", "prompt": "Reply exactly with ATLAS_OK"}), node("plugin", "plugin_test", inputs=("input",), outputs=("value",)), node("exit", "exit", inputs=("input",))],
        [edge("entry", "ai"), edge("ai", "plugin", 0), edge("plugin", "exit")], ["exit"],
    )
    execution_id = value.start({"definition": manifest})["executionId"]
    result = wait_result(value, execution_id)
    assert calls[0][0:2] == ("ai", "ai_infer")
    assert calls[0][2]["request"]["messages"][0]["content"] == "Reply exactly with ATLAS_OK"
    assert result["output"] == {"value": "plugin:ATLAS_OK"}

    invalid = definition([node("entry", "entry"), node("bad", "missing_type"), node("exit", "exit")], [{"source": "entry", "target": "bad"}, {"source": "bad", "target": "exit"}], ["exit"])
    failed_id = value.start({"definition": invalid})["executionId"]
    assert wait_result(value, failed_id)["success"] is False
    follow_up = value.start({"definition": manifest})["executionId"]
    assert wait_result(value, follow_up)["success"] is True


def test_dynamic_plugin_manifest_registers_and_executes_without_arbitrary_code() -> None:
    value, _ = host()
    registered = value.register_plugin({"plugin": {
        "id": "atlas.acceptance.dynamic",
        "version": "1.0.0",
        "nodes": [{
            "typeName": "acceptance_dynamic_prefix",
            "label": "Dynamic Prefix",
            "operation": "prefix",
            "prefix": "dynamic:",
        }],
    }})
    assert registered["pluginId"] == "atlas.acceptance.dynamic"
    assert registered["registrations"][0]["typeName"] == "acceptance_dynamic_prefix"

    manifest = definition(
        [
            node("entry", "entry", outputs=("output",)),
            node("constant", "constant", inputs=("trigger",), outputs=("value",), config={"value": "Atlas"}),
            node("dynamic", "acceptance_dynamic_prefix", inputs=("input",), outputs=("value",)),
            node("exit", "exit", inputs=("input",)),
        ],
        [edge("entry", "constant"), edge("constant", "dynamic"), edge("dynamic", "exit")],
        ["exit"],
    )
    result = wait_result(value, value.start({"definition": manifest})["executionId"])
    assert result["success"] is True
    assert result["output"] == {"value": "dynamic:Atlas"}

    try:
        value.register_plugin({"plugin": {"id": "atlas.unsafe", "nodes": [{
            "typeName": "unsafe_node", "operation": "python", "source": "open('secret')",
        }]}})
    except RuntimeError as error:
        assert "Unsupported safe plugin operation" in str(error)
    else:
        raise AssertionError("unsafe plugin operation was accepted")


def test_type_mismatch_validation_and_unknown_command() -> None:
    value, messages = host()
    source = node("entry", "entry", outputs=("output",))
    target = node("exit", "exit", inputs=("input",))
    source["metadata"]["output_port_types"]["entry:out:0"] = "string"
    target["metadata"]["input_port_types"]["exit:in:0"] = "boolean"
    validation = value.validate(definition([source, target], [edge("entry", "exit")], ["exit"]))
    assert validation["valid"] is False
    assert "Port type mismatch" in validation["errors"][0]
    value.handle({"id": "bad", "command": "not_a_command", "payload": {}})
    assert messages[-1]["ok"] is False


def test_input_workflow_executes_through_test_provider() -> None:
    provider = TestInputProvider()
    value = DesktopWorkflowHost(input_service=InputService(provider))
    manifest = definition(
        [
            node("entry", "entry", outputs=("output",)),
            node("move", "mouse_move", inputs=("trigger",), outputs=("result",), config={"x": 400, "y": 300}),
            node("click", "mouse_click", inputs=("trigger",), outputs=("result",), config={"x": 400, "y": 300}),
            node("wait", "input_wait", inputs=("trigger",), outputs=("result",), config={"duration_ms": 0}),
            node("type", "keyboard_type", inputs=("trigger",), outputs=("result",), config={"text": "Atlas"}),
            node("output", "output", inputs=("input",), outputs=("value",)),
            node("exit", "exit", inputs=("input",)),
        ],
        [edge("entry", "move"), edge("move", "click"), edge("click", "wait"), edge("wait", "type"), edge("type", "output"), edge("output", "exit")],
        ["exit"],
    )
    result = wait_result(value, value.start({"definition": manifest})["executionId"])
    request_names = [request.__class__.__name__ for request in provider.requests]
    assert result["success"] is True
    assert request_names[:3] == ["MouseMoveRequest", "MouseClickRequest", "KeyboardTypeRequest"]
    assert request_names[-1] == "InputReleaseAllRequest"


def test_vision_region_drives_mouse_move_and_click() -> None:
    provider = TestInputProvider()
    value = DesktopWorkflowHost(input_service=InputService(provider))
    value.bridge.request = lambda bridge, command, payload, timeout=180: {"x": 100, "y": 200, "width": 80, "height": 40}  # type: ignore[method-assign]
    nodes = [
        node("entry", "entry", outputs=("output",)),
        node("vision", "vision_current_frame", inputs=("trigger",), outputs=("frame",)),
        node("move", "mouse_move", inputs=("trigger", "target"), outputs=("result",)),
        node("click", "mouse_click", inputs=("trigger", "target"), outputs=("result",)),
        node("exit", "exit", inputs=("input",)),
    ]
    manifest = definition(nodes, [
        edge("entry", "vision"),
        edge("vision", "move", 0, 1),
        edge("vision", "click", 0, 1),
        edge("move", "click", 0, 0),
        edge("click", "exit"),
    ], ["exit"])
    result = wait_result(value, value.start({"definition": manifest})["executionId"])
    move = next(request for request in provider.requests if isinstance(request, MouseMoveRequest))
    click = next(request for request in provider.requests if isinstance(request, MouseClickRequest))
    assert result["success"] is True
    assert move.target.x == click.target.x == 140
    assert move.target.y == click.target.y == 220


def test_closed_loop_vision_reference_click_and_validation() -> None:
    provider = TestInputProvider()
    value = DesktopWorkflowHost(input_service=InputService(provider))
    captures = 0

    def bridge(bridge_name: str, command: str, payload: dict[str, Any], timeout: float = 180) -> dict[str, Any]:
        nonlocal captures
        assert bridge_name == "vision"
        if command == "vision_capture_frame":
            captures += 1
            return {"frameId": f"frame-{captures}", "url": "data:image/png;base64,test", "originX": 0, "originY": 0}
        color = payload["configuration"]["targetColor"]
        return {"matched": True, "matches": [{
            "x": 300, "y": 180, "width": 100, "height": 40,
            "confidence": 0.99, "label": color, "sourceFrameId": f"frame-{captures}",
        }]}

    value.bridge.request = bridge  # type: ignore[method-assign]
    nodes = [
        node("entry", "entry", outputs=("output",)),
        node("before", "vision_current_frame", inputs=("trigger",), outputs=("frame",)),
        node("detect", "vision_detect", inputs=("frame",), outputs=("region", "bounds", "point"), config={"targetColor": "#ff00c8"}),
        node("click", "mouse_click", inputs=("target",), outputs=("result",)),
        node("after", "vision_current_frame", inputs=("trigger",), outputs=("frame",)),
        node("validate", "vision_validate", inputs=("frame",), outputs=("valid", "result"), config={"operation": "detection", "targetColor": "#a8ff00", "expect": "present"}),
        node("exit", "exit", inputs=("input",)),
    ]
    nodes[2]["metadata"]["output_port_types"]["detect:out:0"] = "region_reference"
    nodes[3]["metadata"]["input_port_types"]["click:in:0"] = "target_reference"
    manifest = definition(nodes, [
        edge("entry", "before"), edge("before", "detect"), edge("detect", "click"),
        edge("click", "after"), edge("after", "validate"), edge("validate", "exit"),
    ], ["exit"])

    result = wait_result(value, value.start({"definition": manifest})["executionId"])
    click = next(request for request in provider.requests if isinstance(request, MouseClickRequest))
    assert result["success"] is True
    assert captures == 2
    assert click.target is not None
    assert (click.target.x, click.target.y) == (350, 200)


def test_missing_visual_target_fails_before_any_click() -> None:
    provider = TestInputProvider()
    value = DesktopWorkflowHost(input_service=InputService(provider))
    messages: list[dict[str, Any]] = []
    value.write = messages.append  # type: ignore[method-assign]

    def bridge(_bridge: str, command: str, _payload: dict[str, Any], timeout: float = 180) -> dict[str, Any]:
        if command == "vision_capture_frame":
            return {"frameId": "missing-frame", "url": "data:image/png;base64,test", "originX": 0, "originY": 0}
        return {"operation": "detection", "matched": False, "matches": []}

    value.bridge.request = bridge  # type: ignore[method-assign]
    nodes = [
        node("entry", "entry", outputs=("output",)),
        node("capture", "vision_current_frame", inputs=("trigger",), outputs=("frame",)),
        node("detect", "vision_detect", inputs=("frame",), outputs=("region",), config={"targetColor": "#ff00c8"}),
        node("click", "mouse_click", inputs=("target",), outputs=("result",)),
        node("exit", "exit", inputs=("input",)),
    ]
    nodes[2]["metadata"]["output_port_types"]["detect:out:0"] = "region_reference"
    nodes[3]["metadata"]["input_port_types"]["click:in:0"] = "target_reference"
    manifest = definition(nodes, [
        edge("entry", "capture"), edge("capture", "detect"), edge("detect", "click"), edge("click", "exit"),
    ], ["exit"])

    result = wait_result(value, value.start({"definition": manifest})["executionId"])
    assert result["success"] is False
    assert result["error"] == "Workflow failed: 1 node(s) failed"
    failed = next(item["payload"] for item in messages if item.get("kind") == "event" and item["payload"]["eventType"] == "NodeFailed")
    assert "did not resolve a target" in failed["data"]["error"]
    assert not any(isinstance(request, MouseClickRequest) for request in provider.requests)


def test_ocr_provider_boxes_use_the_same_reference_contract() -> None:
    value, _ = host()
    handler = value._vision_reference_handler("ocr")
    result = handler("ocr", {"results": [{"x": 1, "y": 2, "width": 30, "height": 10, "text": "Atlas"}]}, {"frame": {"frameId": "f", "url": "data:image/png;base64,test"}}, {})
    assert result["region"]["referenceType"] == "region"
    assert result["bounds"]["label"] == "Atlas"
    assert result["point"]["x"] == 16
