# Atlas AI Runtime Integration Bridges

"""
Integration bridges for IPC, Workflow, and Vision.
"""
from __future__ import annotations

from typing import Any, Callable


class IPCAIBridge:
    """Bridge between AI Runtime and IPC Runtime."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable]] = {}
        self._dispatched = 0

    def register_handler(
        self, event_type: str, handler: Callable[[Any], None]
    ) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def dispatch(self, event: Any) -> None:
        event_dict = event.to_dict() if hasattr(event, "to_dict") else {}
        event_type = event_dict.get("event_type", "")
        for handler in self._handlers.get(event_type, []):
            handler(event)
        self._dispatched += 1

    def get_dispatched_count(self) -> int:
        return self._dispatched

    def list_event_types(self) -> list[str]:
        return list(self._handlers.keys())


class WorkflowAIBridge:
    """Bridge between AI Runtime and Workflow Runtime."""

    def __init__(self, registry: Any = None) -> None:
        self._registry = registry

    def execute_inference(
        self, model_id: str, prompt: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        return {"model_id": model_id, "prompt": prompt, "status": "executed"}

    def execute_agent(
        self, agent_id: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        return {"agent_id": agent_id, "status": "executed"}

    def register_conversation(
        self, conversation_id: str, model_id: str
    ) -> None:
        pass

    def list_conversations(self) -> list[str]:
        return []


class VisionAIBridge:
    """Bridge between AI Runtime and Vision Runtime."""

    def __init__(self) -> None:
        self._frames: list[dict[str, Any]] = []

    def process_frame(self, frame: Any) -> dict[str, Any]:
        frame_data = frame.to_dict() if hasattr(frame, "to_dict") else {}
        self._frames.append(frame_data)
        return {"status": "processed", "frame": frame_data}

    def get_processed_frames(self) -> list[dict[str, Any]]:
        return list(self._frames)

    def reset(self) -> None:
        self._frames.clear()
