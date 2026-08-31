"""Structured Knowledge Runtime errors."""

from __future__ import annotations


class KnowledgeError(RuntimeError):
    code = "KNOWLEDGE_ERROR"

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": str(self)}

    def __str__(self) -> str:
        message = super().__str__()
        return f"{self.code}: {message}" if not message.startswith(f"{self.code}:") else message


class KnowledgeValidationError(KnowledgeError):
    code = "KNOWLEDGE_VALIDATION"


class KnowledgeNotFoundError(KnowledgeError):
    code = "KNOWLEDGE_NOT_FOUND"


class KnowledgeStorageError(KnowledgeError):
    code = "KNOWLEDGE_STORAGE"

