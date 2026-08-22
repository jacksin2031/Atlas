# Atlas AI Runtime Prompts

"""
Prompt execution runtime for the AI Runtime.

Supports Prompt, PromptTemplate, PromptVariables, PromptContext,
PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass(frozen=True, slots=True, eq=True)
class PromptVariables:
    """Template variables for prompt compilation."""

    variables: dict[str, Any] = field(default_factory=dict)

    def get(self, name: str, default: Any = None) -> Any:
        return self.variables.get(name, default)

    def set(self, name: str, value: Any) -> PromptVariables:
        new_vars = dict(self.variables)
        new_vars[name] = value
        return PromptVariables(new_vars)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.variables)


@dataclass(frozen=True, slots=True, eq=True)
class PromptContext:
    """Context for prompt execution."""

    conversation_id: str = ""
    session_id: str = ""
    model_id: str = ""
    system_prompt: str = ""
    variables: PromptVariables = field(default_factory=PromptVariables)
    extra: dict[str, Any] = field(default_factory=dict)

    def clone_with(self, **overrides: Any) -> PromptContext:
        new_vars = dict(self.variables.variables)
        new_vars.update(overrides.pop("variables", {}))
        new_extra = dict(self.extra)
        new_extra.update(overrides.pop("extra", {}))
        return PromptContext(
            conversation_id=overrides.get("conversation_id", self.conversation_id),
            session_id=overrides.get("session_id", self.session_id),
            model_id=overrides.get("model_id", self.model_id),
            system_prompt=overrides.get("system_prompt", self.system_prompt),
            variables=PromptVariables(new_vars),
            extra=new_extra,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "session_id": self.session_id,
            "model_id": self.model_id,
            "system_prompt": self.system_prompt,
            "variables": self.variables.to_dict(),
            "extra": dict(self.extra),
        }


@dataclass(unsafe_hash=True)
class PromptTemplate:
    """A reusable prompt template with variables."""

    template_id: str
    name: str
    template_text: str
    version: str = "1.0.0"
    description: str = ""
    variables: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


    def compile(self, context: PromptContext) -> Prompt:
        return PromptCompiler.compile(self, context)

    def to_dict(self) -> dict[str, Any]:
        return {
            "template_id": self.template_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "variables": list(self.variables),
            "metadata": dict(self.metadata),
        }


@dataclass(unsafe_hash=True)
class Prompt:
    """A compiled prompt ready for execution."""

    prompt_id: str
    text: str
    template_id: str = ""
    context: PromptContext = field(default_factory=PromptContext)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)
    _compiled: bool = True


    def to_dict(self) -> dict[str, Any]:
        return {
            "prompt_id": self.prompt_id,
            "text": self.text,
            "template_id": self.template_id,
            "context": self.context.to_dict(),
            "created_at": self.created_at.isoformat(),
            "metadata": dict(self.metadata),
        }


class PromptCompiler:
    """Compiles templates into prompts."""

    @staticmethod
    def compile(template: PromptTemplate, context: PromptContext) -> Prompt:
        import uuid
        text = template.template_text
        for key, value in context.variables.variables.items():
            placeholder = "{" + key + "}"
            text = text.replace(placeholder, str(value))
        missing = [
            v for v in template.variables
            if v not in context.variables.variables
        ]
        if missing:
            from atlas_ai.errors import PromptCompileError
            raise PromptCompileError(
                f"Missing variables: {missing}",
                str(getattr(context, "conversation_id", "")),
            )
        return Prompt(
            prompt_id=str(uuid.uuid4()),
            text=text,
            template_id=template.template_id,
            context=context,
        )

    @staticmethod
    def validate(template: PromptTemplate) -> bool:
        return all(
            "{" + v + "}" in template.template_text
            for v in template.variables
        )


class PromptExecutor:
    """Executes compiled prompts."""

    def execute(self, prompt: Prompt) -> dict[str, Any]:
        return {
            "prompt_id": prompt.prompt_id,
            "text": prompt.text,
            "executed_at": datetime.now(timezone.utc).isoformat(),
        }


@dataclass(frozen=True, slots=True, eq=True)
class PromptHistory:
    """History of prompt executions."""

    prompt_id: str
    executed_at: datetime
    duration_ms: float = 0.0
    status: str = "success"
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "prompt_id": self.prompt_id,
            "executed_at": self.executed_at.isoformat(),
            "duration_ms": self.duration_ms,
            "status": self.status,
            "error": self.error,
        }


@dataclass(frozen=True, slots=True, eq=True)
class PromptSnapshot:
    """Snapshot of a prompt at a point in time."""

    snapshot_id: str
    prompt: Prompt
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "prompt": self.prompt.to_dict(),
            "created_at": self.created_at.isoformat(),
        }


class PromptRegistry:
    """Registry for prompt templates."""

    def __init__(self) -> None:
        self._templates: dict[str, PromptTemplate] = {}
        self._history: list[PromptHistory] = []
        self._snapshots: dict[str, PromptSnapshot] = {}

    def register(self, template: PromptTemplate) -> None:
        self._templates[template.template_id] = template

    def get(self, template_id: str) -> Optional[PromptTemplate]:
        return self._templates.get(template_id)

    def list_templates(self) -> list[str]:
        return list(self._templates.keys())

    def compile(self, template_id: str, context: PromptContext) -> Prompt:
        template = self._templates.get(template_id)
        if template is None:
            from atlas_ai.errors import PromptCompileError
            raise PromptCompileError(f"Template {template_id} not found")
        return PromptCompiler.compile(template, context)

    def record_history(self, history: PromptHistory) -> None:
        self._history.append(history)

    def get_history(self) -> list[dict[str, Any]]:
        return [h.to_dict() for h in self._history]

    def take_snapshot(self, prompt: Prompt, snapshot_id: str) -> None:
        self._snapshots[snapshot_id] = PromptSnapshot(
            snapshot_id=snapshot_id, prompt=prompt
        )

    def get_snapshot(self, snapshot_id: str) -> Optional[PromptSnapshot]:
        return self._snapshots.get(snapshot_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "templates": list(self._templates.keys()),
            "history_count": len(self._history),
            "snapshot_count": len(self._snapshots),
        }
