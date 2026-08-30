"""Windows implementation of the InputProvider contract."""
from __future__ import annotations

import ctypes
import sys
import time
import threading
from ctypes import wintypes
from typing import Any

from .contracts import (
    InputReleaseAllRequest,
    InputRequest,
    KeyboardHotkeyRequest,
    KeyboardPressRequest,
    KeyboardTypeRequest,
    KeyStateRequest,
    MouseClickRequest,
    MouseDragRequest,
    MouseMoveRequest,
    MouseScrollRequest,
    request_dict,
)
from .provider import InputProvider


class WindowsInputProvider(InputProvider):
    _MOUSE_FLAGS = {"left": (0x0002, 0x0004), "right": (0x0008, 0x0010), "middle": (0x0020, 0x0040)}
    _SPECIAL_KEYS = {
        "enter": 0x0D, "esc": 0x1B, "escape": 0x1B, "tab": 0x09, "space": 0x20,
        "backspace": 0x08, "delete": 0x2E, "up": 0x26, "down": 0x28,
        "left": 0x25, "right": 0x27, "home": 0x24, "end": 0x23,
        "pageup": 0x21, "pagedown": 0x22, "shift": 0x10, "ctrl": 0x11,
        "control": 0x11, "alt": 0x12, "win": 0x5B, "meta": 0x5B,
    }

    def __init__(self) -> None:
        if sys.platform != "win32":
            raise RuntimeError("WindowsInputProvider requires Windows")
        self._user32 = ctypes.windll.user32
        # Vision capture coordinates are physical screen pixels. Opt the host into
        # per-monitor DPI awareness before issuing any cursor API calls so Windows
        # does not virtualize them as scaled logical coordinates.
        try:
            self._user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
        except (AttributeError, OSError):
            try:
                self._user32.SetProcessDPIAware()
            except (AttributeError, OSError):
                pass
        self._held_keys: set[int] = set()
        self._held_buttons: set[str] = set()
        self._emergency_stopped = threading.Event()

    def _ensure_active(self) -> None:
        if self._emergency_stopped.is_set():
            raise RuntimeError("Input provider is emergency-stopped.")

    def _vk(self, key: str) -> tuple[int, bool]:
        normalized = key.lower()
        if normalized in self._SPECIAL_KEYS:
            return self._SPECIAL_KEYS[normalized], False
        if len(key) == 1:
            value = self._user32.VkKeyScanW(ord(key))
            if value == -1:
                raise ValueError(f"Unsupported key: {key}")
            return value & 0xFF, bool(value & 0x100)
        if normalized.startswith("f") and normalized[1:].isdigit() and 1 <= int(normalized[1:]) <= 24:
            return 0x70 + int(normalized[1:]) - 1, False
        raise ValueError(f"Unsupported key: {key}")

    def _key_down(self, key: str) -> None:
        vk, _ = self._vk(key)
        self._user32.keybd_event(vk, 0, 0, 0)
        self._held_keys.add(vk)

    def _key_up(self, key: str) -> None:
        vk, _ = self._vk(key)
        self._user32.keybd_event(vk, 0, 0x0002, 0)
        self._held_keys.discard(vk)

    def _press(self, key: str) -> None:
        vk, needs_shift = self._vk(key)
        if needs_shift:
            self._user32.keybd_event(0x10, 0, 0, 0)
        self._user32.keybd_event(vk, 0, 0, 0)
        self._user32.keybd_event(vk, 0, 0x0002, 0)
        if needs_shift:
            self._user32.keybd_event(0x10, 0, 0x0002, 0)

    def _move(self, x: int, y: int, duration_ms: int = 0) -> None:
        if duration_ms <= 0:
            self._user32.SetCursorPos(x, y)
            return
        point = wintypes.POINT()
        self._user32.GetCursorPos(ctypes.byref(point))
        steps = max(1, min(120, duration_ms // 8))
        for step in range(1, steps + 1):
            self._ensure_active()
            ratio = step / steps
            self._user32.SetCursorPos(round(point.x + (x - point.x) * ratio), round(point.y + (y - point.y) * ratio))
            time.sleep(duration_ms / steps / 1000)

    def execute(self, request: InputRequest) -> dict[str, Any]:
        if not isinstance(request, InputReleaseAllRequest):
            self._ensure_active()
        if isinstance(request, MouseMoveRequest):
            self._move(request.target.x, request.target.y, request.duration_ms)
        elif isinstance(request, MouseClickRequest):
            if request.target:
                self._move(request.target.x, request.target.y)
            down, up = self._MOUSE_FLAGS[request.button]
            for _ in range(request.click_count):
                self._user32.mouse_event(down, 0, 0, 0, 0)
                self._user32.mouse_event(up, 0, 0, 0, 0)
        elif isinstance(request, MouseDragRequest):
            self._move(request.start.x, request.start.y)
            down, up = self._MOUSE_FLAGS[request.button]
            self._user32.mouse_event(down, 0, 0, 0, 0)
            self._held_buttons.add(request.button)
            try:
                self._move(request.end.x, request.end.y, request.duration_ms)
            finally:
                self._user32.mouse_event(up, 0, 0, 0, 0)
                self._held_buttons.discard(request.button)
        elif isinstance(request, MouseScrollRequest):
            if request.vertical:
                self._user32.mouse_event(0x0800, 0, 0, request.vertical * 120, 0)
            if request.horizontal:
                self._user32.mouse_event(0x01000, 0, 0, request.horizontal * 120, 0)
        elif isinstance(request, KeyboardPressRequest):
            self._press(request.key)
        elif isinstance(request, KeyboardHotkeyRequest):
            keys = [self._vk(key)[0] for key in request.keys]
            for vk in keys:
                self._user32.keybd_event(vk, 0, 0, 0)
            for vk in reversed(keys):
                self._user32.keybd_event(vk, 0, 0x0002, 0)
        elif isinstance(request, KeyboardTypeRequest):
            for char in request.text:
                self._ensure_active()
                self._press(char)
                if request.interval_ms:
                    time.sleep(request.interval_ms / 1000)
        elif isinstance(request, KeyStateRequest):
            # The service selects down/up semantics through this shared request.
            raise ValueError("KeyStateRequest must be dispatched through key_down or key_up")
        elif isinstance(request, InputReleaseAllRequest):
            for vk in tuple(self._held_keys):
                self._user32.keybd_event(vk, 0, 0x0002, 0)
            for button in tuple(self._held_buttons):
                self._user32.mouse_event(self._MOUSE_FLAGS[button][1], 0, 0, 0, 0)
            self._held_keys.clear()
            self._held_buttons.clear()
        return {"accepted": True, **request_dict(request)}

    def key_down(self, request: KeyStateRequest) -> dict[str, Any]:
        self._key_down(request.key)
        return {"accepted": True, "state": "down", **request_dict(request)}

    def key_up(self, request: KeyStateRequest) -> dict[str, Any]:
        self._key_up(request.key)
        return {"accepted": True, "state": "up", **request_dict(request)}

    def is_key_down(self, request: KeyStateRequest) -> bool:
        vk, _ = self._vk(request.key)
        return bool(self._user32.GetAsyncKeyState(vk) & 0x8000)

    def active_target(self) -> dict[str, Any] | None:
        window = self._user32.GetForegroundWindow()
        if not window:
            return None
        length = self._user32.GetWindowTextLengthW(window)
        buffer = ctypes.create_unicode_buffer(length + 1)
        self._user32.GetWindowTextW(window, buffer, length + 1)
        process_id = wintypes.DWORD()
        self._user32.GetWindowThreadProcessId(window, ctypes.byref(process_id))
        return {"title": buffer.value, "processId": int(process_id.value)}

    def emergency_stop_requested(self) -> bool:
        # Pause/Break is deliberately uncommon in normal text and remains
        # observable while another application owns foreground focus.
        return bool(self._user32.GetAsyncKeyState(0x13) & 0x8000)

    def set_emergency_stopped(self, stopped: bool) -> None:
        if stopped:
            self._emergency_stopped.set()
        else:
            self._emergency_stopped.clear()
