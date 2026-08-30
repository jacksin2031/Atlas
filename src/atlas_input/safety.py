"""Safety boundary enforced before any real desktop input provider call."""
from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Any, Callable


class InputSafetyError(PermissionError):
    """Raised when an input request is rejected by the safety policy."""


@dataclass(frozen=True)
class InputSafetyPolicy:
    permission_granted: bool = False
    allowed_window_title: str | None = None
    max_actions_per_second: int = 15
    max_text_length: int = 1000
    allow_dangerous_actions: bool = False

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "InputSafetyPolicy":
        title = str(value.get("allowedWindowTitle", "")).strip() or None
        return cls(
            permission_granted=bool(value.get("permissionGranted", False)),
            allowed_window_title=title,
            max_actions_per_second=max(1, min(int(value.get("maxActionsPerSecond", 15)), 60)),
            max_text_length=max(1, min(int(value.get("maxTextLength", 1000)), 10_000)),
            allow_dangerous_actions=bool(value.get("allowDangerousActions", False)),
        )


class InputSafetyController:
    def __init__(self, policy: InputSafetyPolicy | None = None) -> None:
        self._lock = threading.RLock()
        self._policy = policy or InputSafetyPolicy()
        self._emergency_stopped = False
        self._actions: deque[float] = deque()

    def arm(self, policy: InputSafetyPolicy) -> dict[str, Any]:
        if not policy.permission_granted:
            raise InputSafetyError("Input permission must be explicitly granted when arming.")
        with self._lock:
            self._policy = policy
            self._emergency_stopped = False
            self._actions.clear()
        return self.status()

    def emergency_stop(self) -> dict[str, Any]:
        with self._lock:
            self._emergency_stopped = True
            self._actions.clear()
        return self.status()

    def status(self) -> dict[str, Any]:
        with self._lock:
            return {
                "armed": self._policy.permission_granted and not self._emergency_stopped,
                "emergencyStopped": self._emergency_stopped,
                "allowedWindowTitle": self._policy.allowed_window_title,
                "maxActionsPerSecond": self._policy.max_actions_per_second,
                "maxTextLength": self._policy.max_text_length,
                "dangerousActionsAllowed": self._policy.allow_dangerous_actions,
            }

    @staticmethod
    def _dangerous(action: str, payload: dict[str, Any], max_text_length: int) -> str | None:
        keys = payload.get("keys", [])
        if isinstance(keys, str):
            keys = [part.strip() for part in keys.split("+")]
        normalized = {str(key).lower() for key in keys}
        if action == "keyboard_hotkey" and (
            normalized.intersection({"win", "meta"})
            or {"alt", "f4"}.issubset(normalized)
            or {"ctrl", "alt", "delete"}.issubset(normalized)
        ):
            return "dangerous keyboard shortcut"
        if action == "key_down" and str(payload.get("key", "")).lower() in {"win", "meta", "alt", "ctrl", "control"}:
            return "held system modifier"
        if action == "keyboard_type" and len(str(payload.get("text", ""))) > max_text_length:
            return "typed text exceeds the configured safety limit"
        if action in {"mouse_click", "mouse_double_click"} and int(payload.get("click_count", 2 if action == "mouse_double_click" else 1)) > 3:
            return "excessive click count"
        return None

    def authorize(self, action: str, payload: dict[str, Any], active_target: Callable[[], dict[str, Any] | None]) -> None:
        if action in {"input_release_all", "input_wait"}:
            return
        with self._lock:
            policy = self._policy
            if self._emergency_stopped:
                raise InputSafetyError("Input Runtime is emergency-stopped. Re-arm it before continuing.")
            if not policy.permission_granted:
                raise InputSafetyError("Input Runtime is not armed. Explicit input permission is required.")
            if policy.allowed_window_title:
                target = active_target()
                title = str((target or {}).get("title", ""))
                if policy.allowed_window_title.casefold() not in title.casefold():
                    raise InputSafetyError(
                        f"Foreground target '{title or 'unknown'}' does not match allowed window '{policy.allowed_window_title}'."
                    )
            dangerous = self._dangerous(action, payload, policy.max_text_length)
            if dangerous and not policy.allow_dangerous_actions:
                raise InputSafetyError(f"Input request requires dangerous-action confirmation: {dangerous}.")
            now = time.monotonic()
            while self._actions and now - self._actions[0] >= 1.0:
                self._actions.popleft()
            if len(self._actions) >= policy.max_actions_per_second:
                raise InputSafetyError("Input action rate limit exceeded.")
            self._actions.append(now)
