"""Provider-independent Input Runtime service."""
from __future__ import annotations

import time
import threading
from typing import Any, Callable

from atlas_automation import resolve_reference_point

from .contracts import (
    Coordinate,
    InputReleaseAllRequest,
    InputWaitRequest,
    KeyboardHotkeyRequest,
    KeyboardPressRequest,
    KeyboardTypeRequest,
    KeyStateRequest,
    MouseClickRequest,
    MouseDragRequest,
    MouseMoveRequest,
    MouseScrollRequest,
)
from .provider import InputProvider
from .safety import InputSafetyController, InputSafetyPolicy


class InputService:
    def __init__(self, provider: InputProvider, safety: InputSafetyController | None = None) -> None:
        self.provider = provider
        # Explicitly constructed services remain test/developer friendly. The
        # platform default passes a fail-closed controller below.
        self.safety = safety or InputSafetyController(InputSafetyPolicy(permission_granted=True))
        self._emergency_listeners: list[Callable[[], None]] = []
        self._listener_lock = threading.RLock()

    def add_emergency_stop_listener(self, listener: Callable[[], None]) -> None:
        with self._listener_lock:
            self._emergency_listeners.append(listener)

    def arm(self, policy: InputSafetyPolicy) -> dict[str, Any]:
        status = self.safety.arm(policy)
        self.provider.set_emergency_stopped(False)
        return status

    def emergency_stop(self) -> dict[str, Any]:
        status = self.safety.emergency_stop()
        self.provider.set_emergency_stopped(True)
        self.provider.execute(InputReleaseAllRequest())
        with self._listener_lock:
            listeners = list(self._emergency_listeners)
        for listener in listeners:
            try:
                listener()
            except Exception:
                pass
        return status

    def safety_status(self) -> dict[str, Any]:
        return self.safety.status()

    def start_emergency_watch(self, interval_seconds: float = 0.02) -> None:
        def watch() -> None:
            latched = False
            while True:
                requested = self.provider.emergency_stop_requested()
                if requested and not latched:
                    try:
                        self.emergency_stop()
                    except Exception:
                        pass
                latched = requested
                time.sleep(interval_seconds)
        threading.Thread(target=watch, name="atlas-input-emergency-watch", daemon=True).start()

    @staticmethod
    def _coordinate_value(value: Any) -> Coordinate | None:
        resolved = resolve_reference_point(value)
        return Coordinate(*resolved) if resolved else None

    @staticmethod
    def _coordinate(payload: dict[str, Any], name: str = "target") -> Coordinate:
        value = payload.get(name)
        resolved = InputService._coordinate_value(value)
        if resolved:
            return resolved
        prefix = "" if name == "target" else f"{name}_"
        return Coordinate(int(payload.get(f"{prefix}x", payload.get("x", 0))), int(payload.get(f"{prefix}y", payload.get("y", 0))))

    def execute(self, action: str, payload: dict[str, Any], cancelled: Callable[[], bool] | None = None) -> dict[str, Any]:
        self.safety.authorize(action, payload, self.provider.active_target)
        if action == "mouse_move":
            return self.provider.execute(MouseMoveRequest(self._coordinate(payload), int(payload.get("duration_ms", 0))))
        if action in {"mouse_click", "mouse_double_click"}:
            target = self._coordinate(payload) if "target" in payload or "x" in payload else None
            count = 2 if action == "mouse_double_click" else int(payload.get("click_count", 1))
            return self.provider.execute(MouseClickRequest(target, str(payload.get("button", "left")), count))  # type: ignore[arg-type]
        if action == "mouse_drag":
            return self.provider.execute(MouseDragRequest(
                self._coordinate(payload, "start"), self._coordinate(payload, "end"),
                str(payload.get("button", "left")), int(payload.get("duration_ms", 250)),  # type: ignore[arg-type]
            ))
        if action == "mouse_scroll":
            return self.provider.execute(MouseScrollRequest(int(payload.get("vertical", 0)), int(payload.get("horizontal", 0))))
        if action == "keyboard_press":
            return self.provider.execute(KeyboardPressRequest(str(payload["key"])))
        if action == "keyboard_hotkey":
            keys = payload.get("keys", [])
            if isinstance(keys, str):
                keys = [part.strip() for part in keys.split("+") if part.strip()]
            return self.provider.execute(KeyboardHotkeyRequest(tuple(str(key) for key in keys)))
        if action == "keyboard_type":
            return self.provider.execute(KeyboardTypeRequest(str(payload.get("text", "")), int(payload.get("interval_ms", 0))))
        if action in {"key_down", "key_up"}:
            request = KeyStateRequest(str(payload["key"]))
            method = getattr(self.provider, action, None)
            if not callable(method):
                raise RuntimeError(f"Provider does not support {action}")
            return method(request)
        if action == "input_wait":
            request = InputWaitRequest(
                int(payload.get("duration_ms", 0)), payload.get("key"), payload.get("state"),
                int(payload.get("timeout_ms", 30_000)),
            )
            if not request.key:
                deadline = time.monotonic() + max(0, request.duration_ms) / 1000
                while time.monotonic() < deadline:
                    if cancelled and cancelled():
                        raise RuntimeError("Execution cancelled")
                    time.sleep(min(0.02, deadline - time.monotonic()))
                return {"accepted": True, "waited_ms": max(0, request.duration_ms)}
            expected = request.state != "up"
            deadline = time.monotonic() + max(0, request.timeout_ms) / 1000
            while time.monotonic() <= deadline:
                if cancelled and cancelled():
                    raise RuntimeError("Execution cancelled")
                if self.provider.is_key_down(KeyStateRequest(request.key)) == expected:
                    return {"accepted": True, "key": request.key, "state": request.state or "down"}
                time.sleep(0.01)
            raise TimeoutError(f"Timed out waiting for {request.key} to become {request.state or 'down'}")
        if action == "input_release_all":
            return self.provider.execute(InputReleaseAllRequest())
        raise ValueError(f"Unsupported input action: {action}")
