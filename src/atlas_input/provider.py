"""Input provider abstraction and deterministic test implementation."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .contracts import InputRequest, KeyStateRequest, request_dict


class InputProvider(ABC):
    @abstractmethod
    def execute(self, request: InputRequest) -> dict[str, Any]:
        """Execute one typed input request."""

    @abstractmethod
    def is_key_down(self, request: KeyStateRequest) -> bool:
        """Return the current state of a keyboard key."""

    def active_target(self) -> dict[str, Any] | None:
        """Return the current foreground target when the provider can inspect it."""
        return None

    def emergency_stop_requested(self) -> bool:
        return False

    def set_emergency_stopped(self, stopped: bool) -> None:
        """Latch or clear provider-side interruption for long-running input."""


class TestInputProvider(InputProvider):
    """Records requests without sending operating-system input."""

    __test__ = False

    def __init__(self) -> None:
        self.requests: list[InputRequest] = []
        self.keys_down: set[str] = set()
        self.active_target_value: dict[str, Any] | None = {"title": "Atlas Test Target", "processId": 1}
        self.emergency_stopped = False

    def execute(self, request: InputRequest) -> dict[str, Any]:
        self.requests.append(request)
        name = request.__class__.__name__
        if name == "KeyStateRequest":
            return {"accepted": True, **request_dict(request)}
        if name == "InputReleaseAllRequest":
            self.keys_down.clear()
        return {"accepted": True, **request_dict(request)}

    def is_key_down(self, request: KeyStateRequest) -> bool:
        return request.key.lower() in self.keys_down

    def active_target(self) -> dict[str, Any] | None:
        return self.active_target_value

    def set_emergency_stopped(self, stopped: bool) -> None:
        self.emergency_stopped = stopped

    def key_down(self, request: KeyStateRequest) -> dict[str, Any]:
        self.requests.append(request)
        self.keys_down.add(request.key.lower())
        return {"accepted": True, "state": "down", **request_dict(request)}

    def key_up(self, request: KeyStateRequest) -> dict[str, Any]:
        self.requests.append(request)
        self.keys_down.discard(request.key.lower())
        return {"accepted": True, "state": "up", **request_dict(request)}


class UnavailableInputProvider(InputProvider):
    def __init__(self, reason: str) -> None:
        self.reason = reason

    def execute(self, request: InputRequest) -> dict[str, Any]:
        raise RuntimeError(self.reason)

    def is_key_down(self, request: KeyStateRequest) -> bool:
        raise RuntimeError(self.reason)
