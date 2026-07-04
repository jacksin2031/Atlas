# Atlas AI Runtime Conversations

"""
Conversation execution runtime for the AI Runtime.

Supports Conversation, ConversationSession, ConversationHistory,
ConversationMessage, ConversationRole, ConversationState, ConversationRegistry.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class ConversationRole(Enum):
    """Message roles in a conversation."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    FUNCTION = "function"


class ConversationState(Enum):
    """Conversation lifecycle states."""

    CREATED = "created"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True, eq=True)
class ConversationMessage:
    """A single message in a conversation."""

    message_id: str
    role: ConversationRole
    content: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, Any] = field(default_factory=dict)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    tool_result: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": dict(self.metadata),
            "tool_calls": list(self.tool_calls),
            "tool_result": self.tool_result,
        }


@dataclass(frozen=True, slots=True, eq=True)
class ConversationHistory:
    """Immutable history of a conversation."""

    messages: tuple[ConversationMessage, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "messages", tuple(self.messages))

    @property
    def count(self) -> int:
        return len(self.messages)

    @property
    def last_message(self) -> Optional[ConversationMessage]:
        return self.messages[-1] if self.messages else None

    def append(self, message: ConversationMessage) -> ConversationHistory:
        return ConversationHistory(self.messages + (message,))

    def to_dict(self) -> dict[str, Any]:
        return {
            "messages": [m.to_dict() for m in self.messages],
            "count": self.count,
        }


@dataclass(unsafe_hash=True)
class Conversation:
    """An active conversation."""

    conversation_id: str
    title: str = ""
    state: ConversationState = ConversationState.CREATED
    history: ConversationHistory = field(default_factory=ConversationHistory)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    session_id: str = ""
    model_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


    def add_message(self, message: ConversationMessage) -> None:
        self.history = self.history.append(message)
        self.updated_at = datetime.now(timezone.utc)
        if self.state == ConversationState.CREATED:
            self.state = ConversationState.ACTIVE

    def close(self) -> None:
        self.state = ConversationState.CLOSED

    def pause(self) -> None:
        self.state = ConversationState.PAUSED

    def resume(self) -> None:
        if self.state == ConversationState.PAUSED:
            self.state = ConversationState.ACTIVE

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "title": self.title,
            "state": self.state.value,
            "message_count": self.history.count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "session_id": self.session_id,
            "model_id": self.model_id,
            "metadata": dict(self.metadata),
        }


@dataclass
class ConversationSession:
    """Manages a conversation session."""

    session_id: str
    conversation: Conversation
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    _active: bool = True

    @property
    def is_active(self) -> bool:
        return self._active

    def add_message(self, message: ConversationMessage) -> None:
        self.conversation.add_message(message)

    def close(self) -> None:
        self.conversation.close()
        self._active = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "conversation": self.conversation.to_dict(),
            "active": self._active,
        }


class ConversationRegistry:
    """Registry for conversations."""

    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}
        self._sessions: dict[str, ConversationSession] = {}

    def create_conversation(
        self,
        title: str = "",
        model_id: str = "",
        session_id: str = "",
    ) -> Conversation:
        import uuid
        conv_id = str(uuid.uuid4())
        conv = Conversation(
            conversation_id=conv_id,
            title=title,
            model_id=model_id,
            session_id=session_id,
        )
        self._conversations[conv_id] = conv
        return conv

    def get(self, conversation_id: str) -> Optional[Conversation]:
        return self._conversations.get(conversation_id)

    def list_conversations(self) -> list[str]:
        return list(self._conversations.keys())

    def close(self, conversation_id: str) -> bool:
        conv = self._conversations.get(conversation_id)
        if conv:
            conv.close()
            return True
        return False

    def delete(self, conversation_id: str) -> bool:
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            return True
        return False

    def register_session(self, session: ConversationSession) -> None:
        self._sessions[session.session_id] = session

    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        return self._sessions.get(session_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversations": list(self._conversations.keys()),
            "sessions": list(self._sessions.keys()),
        }
