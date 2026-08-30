import pytest

from atlas_input import InputSafetyController, InputSafetyError, InputSafetyPolicy, InputService, TestInputProvider


def test_input_runtime_fails_closed_until_explicitly_armed():
    provider = TestInputProvider()
    service = InputService(provider, InputSafetyController())
    with pytest.raises(InputSafetyError, match="not armed"):
        service.execute("mouse_click", {"x": 10, "y": 20})
    service.arm(InputSafetyPolicy(permission_granted=True, allowed_window_title="Atlas Test"))
    assert service.execute("mouse_click", {"x": 10, "y": 20})["accepted"] is True


def test_focus_policy_and_dangerous_action_confirmation_are_enforced():
    provider = TestInputProvider()
    service = InputService(provider, InputSafetyController())
    service.arm(InputSafetyPolicy(permission_granted=True, allowed_window_title="Target App"))
    with pytest.raises(InputSafetyError, match="does not match"):
        service.execute("keyboard_press", {"key": "a"})
    provider.active_target_value = {"title": "Target App — Document", "processId": 7}
    with pytest.raises(InputSafetyError, match="dangerous-action confirmation"):
        service.execute("keyboard_hotkey", {"keys": ["alt", "f4"]})


def test_rate_limit_and_emergency_stop_release_input():
    provider = TestInputProvider()
    service = InputService(provider, InputSafetyController())
    service.arm(InputSafetyPolicy(permission_granted=True, max_actions_per_second=1))
    service.execute("keyboard_press", {"key": "a"})
    with pytest.raises(InputSafetyError, match="rate limit"):
        service.execute("keyboard_press", {"key": "b"})
    status = service.emergency_stop()
    assert status["emergencyStopped"] is True
    assert provider.requests[-1].__class__.__name__ == "InputReleaseAllRequest"
    with pytest.raises(InputSafetyError, match="emergency-stopped"):
        service.execute("mouse_move", {"x": 1, "y": 2})
