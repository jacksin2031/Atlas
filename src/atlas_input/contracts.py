"""Typed requests shared by Input Service clients and providers."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal, TypeAlias


MouseButton = Literal["left", "right", "middle"]


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


@dataclass(frozen=True)
class Region:
    x: int
    y: int
    width: int
    height: int

    @property
    def center(self) -> Coordinate:
        return Coordinate(self.x + self.width // 2, self.y + self.height // 2)


@dataclass(frozen=True)
class MouseMoveRequest:
    target: Coordinate
    duration_ms: int = 0


@dataclass(frozen=True)
class MouseClickRequest:
    target: Coordinate | None = None
    button: MouseButton = "left"
    click_count: int = 1


@dataclass(frozen=True)
class MouseDragRequest:
    start: Coordinate
    end: Coordinate
    button: MouseButton = "left"
    duration_ms: int = 250


@dataclass(frozen=True)
class MouseScrollRequest:
    vertical: int = 0
    horizontal: int = 0


@dataclass(frozen=True)
class KeyboardPressRequest:
    key: str


@dataclass(frozen=True)
class KeyboardHotkeyRequest:
    keys: tuple[str, ...]


@dataclass(frozen=True)
class KeyboardTypeRequest:
    text: str
    interval_ms: int = 0


@dataclass(frozen=True)
class KeyStateRequest:
    key: str


@dataclass(frozen=True)
class InputWaitRequest:
    duration_ms: int = 0
    key: str | None = None
    state: Literal["down", "up"] | None = None
    timeout_ms: int = 30_000


@dataclass(frozen=True)
class InputReleaseAllRequest:
    pass


InputRequest: TypeAlias = (
    MouseMoveRequest | MouseClickRequest | MouseDragRequest | MouseScrollRequest |
    KeyboardPressRequest | KeyboardHotkeyRequest | KeyboardTypeRequest |
    KeyStateRequest | InputWaitRequest | InputReleaseAllRequest
)


def request_dict(request: InputRequest) -> dict[str, Any]:
    return {"request_type": request.__class__.__name__, **asdict(request)}
