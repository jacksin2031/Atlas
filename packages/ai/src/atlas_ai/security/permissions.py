# Atlas AI Runtime Security

"""
Security for the AI Runtime.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Permission(Enum):
    """AI permission levels."""

    NONE = "none"
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


@dataclass(frozen=True, slots=True, eq=True)
class SecurityPolicy:
    """Security policy for AI operations."""

    max_input_length: int = 100000
    max_output_length: int = 50000
    allowed_tools: list[str] = field(default_factory=list)
    blocked_patterns: list[str] = field(default_factory=list)
    require_approval_for: list[str] = field(default_factory=list)
    sandbox_enabled: bool = True
    extra_policy: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_input_length": self.max_input_length,
            "max_output_length": self.max_output_length,
            "allowed_tools": list(self.allowed_tools),
            "blocked_patterns": list(self.blocked_patterns),
            "require_approval_for": list(self.require_approval_for),
            "sandbox_enabled": self.sandbox_enabled,
            "extra_policy": dict(self.extra_policy),
        }


class SecurityValidator:
    """Validates AI inputs, outputs, and permissions."""

    def __init__(self, policy: SecurityPolicy | None = None) -> None:
        self._policy = policy or SecurityPolicy()

    def validate_input(self, text: str, caller_id: str = "") -> bool:
        if len(text) > self._policy.max_input_length:
            return False
        for pattern in self._policy.blocked_patterns:
            if pattern in text:
                return False
        return True

    def validate_output(self, text: str) -> bool:
        if len(text) > self._policy.max_output_length:
            return False
        for pattern in self._policy.blocked_patterns:
            if pattern in text:
                return False
        return True

    def validate_tool_access(
        self, tool_id: str, caller_id: str, required_permission: Permission
    ) -> bool:
        if not self._policy.sandbox_enabled:
            return True
        if self._policy.allowed_tools and tool_id not in self._policy.allowed_tools:
            return False
        return True

    def validate_prompt(self, prompt: str) -> bool:
        return self.validate_input(prompt)

    def validate_capability(
        self, capability: str, caller_id: str
    ) -> bool:
        return True

    def to_dict(self) -> dict[str, Any]:
        return {"policy": self._policy.to_dict()}
