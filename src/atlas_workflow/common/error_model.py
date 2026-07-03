"""Common error model per RFC-1006."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


ERROR_SEVERITY_CRITICAL = "critical"
ERROR_SEVERITY_HIGH = "high"
ERROR_SEVERITY_MEDIUM = "medium"
ERROR_SEVERITY_LOW = "low"


@dataclass(frozen=True, slots=True, kw_only=True)
class ErrorDetail:
    """Structured error detail for workflow errors."""
    code: str
    message: str
    severity: str = ERROR_SEVERITY_MEDIUM
    context: dict[str, Any] = field(default_factory=dict)
    suggestions: list[str] = field(default_factory=list)
    caused_by: ErrorDetail | None = None

    def to_dict(self) -> dict[str, Any]:
        result = {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "context": dict(self.context),
            "suggestions": list(self.suggestions),
        }
        if self.caused_by:
            result["caused_by"] = self.caused_by.to_dict()
        return result
