# Atlas AI Runtime Tools

"""
Tool execution runtime for the AI Runtime.

Supports Tool, ToolDescriptor, ToolRegistry, ToolInvocation,
ToolResult, ToolPermission, ToolCapability.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional


class ToolCapability(Enum):
    """Tool capabilities."""

    FILE_READ = "file_read"
    FILE_WRITE = "file_write"
    COMMAND_EXECUTION = "command_execution"
    HTTP_REQUEST = "http_request"
    DATABASE_QUERY = "database_query"
    SEARCH = "search"
    CALCULATION = "calculation"
    CODE_EXECUTION = "code_execution"
    EMAIL = "email"
    CALENDAR = "calendar"


class ToolPermission(Enum):
    """Tool permission levels."""

    NONE = "none"
    READ_ONLY = "read_only"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


@dataclass(frozen=True, slots=True, eq=True)
class ToolDescriptor:
    """Describes a tool without instantiating it."""

    tool_id: str
    name: str
    description: str
    version: str = "1.0.0"
    parameters: dict[str, Any] = field(default_factory=dict)
    capabilities: frozenset[ToolCapability] = field(default_factory=frozenset)
    required_permissions: frozenset[ToolPermission] = field(default_factory=frozenset)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "parameters": dict(self.parameters),
            "capabilities": [c.value for c in self.capabilities],
            "required_permissions": [p.value for p in self.required_permissions],
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True, eq=True)
class ToolResult:
    """Result from a tool invocation."""

    tool_id: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "metadata": dict(self.metadata),
        }


@dataclass
class ToolInvocation:
    """Tracks a tool invocation."""

    invocation_id: str
    tool_id: str
    arguments: dict[str, Any] = field(default_factory=dict)
    agent_id: str = ""
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    result: Optional[ToolResult] = None
    permission_granted: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "invocation_id": self.invocation_id,
            "tool_id": self.tool_id,
            "arguments": dict(self.arguments),
            "agent_id": self.agent_id,
            "timestamp": self.timestamp.isoformat(),
            "permission_granted": self.permission_granted,
        }


class Tool:
    """A callable tool with descriptor and handler."""

    def __init__(
        self,
        descriptor: ToolDescriptor,
        handler: Callable[[dict[str, Any]], ToolResult],
    ) -> None:
        self._descriptor = descriptor
        self._handler = handler

    @property
    def descriptor(self) -> ToolDescriptor:
        return self._descriptor

    @property
    def tool_id(self) -> str:
        return self._descriptor.tool_id

    @property
    def name(self) -> str:
        return self._descriptor.name

    def invoke(self, arguments: dict[str, Any]) -> ToolResult:
        return self._handler(arguments)

    def to_dict(self) -> dict[str, Any]:
        return self._descriptor.to_dict()


class ToolRegistry:
    """Registry for tools."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}
        self._handlers: dict[str, Callable] = {}

    def register(self, tool: Tool) -> None:
        if tool.tool_id in self._tools:
            from atlas_ai.errors import DuplicateRegistrationError
            raise DuplicateRegistrationError(
                f"Tool {tool.tool_id} already registered", tool.tool_id
            )
        self._tools[tool.tool_id] = tool

    def get(self, tool_id: str) -> Optional[Tool]:
        return self._tools.get(tool_id)

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    def is_registered(self, tool_id: str) -> bool:
        return tool_id in self._tools

    def invoke(self, tool_id: str, arguments: dict[str, Any]) -> ToolResult:
        tool = self._tools.get(tool_id)
        if tool is None:
            from atlas_ai.errors import ToolInvocationError
            raise ToolInvocationError(f"Tool {tool_id} not found", tool_id)
        return tool.invoke(arguments)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tools": list(self._tools.keys()),
        }
