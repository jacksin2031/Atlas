from __future__ import annotations

from atlas_input import InputService, TestInputProvider
from atlas_input.contracts import (
    InputReleaseAllRequest,
    KeyboardHotkeyRequest,
    KeyboardPressRequest,
    KeyboardTypeRequest,
    KeyStateRequest,
    MouseClickRequest,
    MouseDragRequest,
    MouseMoveRequest,
    MouseScrollRequest,
)


def service() -> tuple[InputService, TestInputProvider]:
    provider = TestInputProvider()
    return InputService(provider), provider


def test_mouse_requests_and_region_center_resolution() -> None:
    value, provider = service()
    value.execute("mouse_move", {"target": {"x": 10, "y": 20, "width": 100, "height": 40}})
    value.execute("mouse_click", {"x": 12, "y": 24, "button": "right"})
    value.execute("mouse_double_click", {"target": {"x": 20, "y": 30}})
    value.execute("mouse_drag", {"start_x": 1, "start_y": 2, "end_x": 3, "end_y": 4})
    value.execute("mouse_scroll", {"vertical": -2, "horizontal": 1})

    assert provider.requests[0] == MouseMoveRequest(target=provider.requests[0].target, duration_ms=0)
    assert provider.requests[0].target.x == 60
    assert provider.requests[0].target.y == 40
    assert isinstance(provider.requests[1], MouseClickRequest)
    assert provider.requests[1].button == "right"
    assert provider.requests[2].click_count == 2
    assert isinstance(provider.requests[3], MouseDragRequest)
    assert isinstance(provider.requests[4], MouseScrollRequest)


def test_mouse_click_accepts_typed_region_reference_directly() -> None:
    value, provider = service()
    value.execute("mouse_click", {"target": {
        "contract": "atlas.automation.reference/v1",
        "referenceType": "region",
        "coordinateSpace": "screen",
        "regionId": "detected-button",
        "bounds": {
            "referenceType": "bounds", "coordinateSpace": "screen",
            "x": 500, "y": 300, "width": 120, "height": 40,
        },
    }})

    request = provider.requests[0]
    assert isinstance(request, MouseClickRequest)
    assert request.target is not None
    assert (request.target.x, request.target.y) == (560, 320)


def test_keyboard_requests_hold_release_wait_and_cleanup() -> None:
    value, provider = service()
    value.execute("keyboard_press", {"key": "enter"})
    value.execute("keyboard_hotkey", {"keys": "ctrl+s"})
    value.execute("keyboard_type", {"text": "Atlas", "interval_ms": 5})
    value.execute("key_down", {"key": "w"})
    assert provider.is_key_down(KeyStateRequest("w"))
    assert value.execute("input_wait", {"key": "w", "state": "down", "timeout_ms": 10})["accepted"]
    value.execute("key_up", {"key": "w"})
    assert not provider.is_key_down(KeyStateRequest("w"))
    value.execute("input_release_all", {})

    assert isinstance(provider.requests[0], KeyboardPressRequest)
    assert provider.requests[1] == KeyboardHotkeyRequest(("ctrl", "s"))
    assert provider.requests[2] == KeyboardTypeRequest("Atlas", 5)
    assert isinstance(provider.requests[-1], InputReleaseAllRequest)


def test_time_wait_does_not_require_provider_support() -> None:
    value, provider = service()
    result = value.execute("input_wait", {"duration_ms": 0})
    assert result == {"accepted": True, "waited_ms": 0}
    assert provider.requests == []
