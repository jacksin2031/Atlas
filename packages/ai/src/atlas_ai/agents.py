# Atlas AI Runtime Agents

"""
Agent execution runtime for the AI Runtime.

Supports Agent, AgentContext, AgentExecution, AgentState,
AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class AgentState(Enum):
    """Agent lifecycle states."""

    CREATED = "created"
    IDLE = "idle"
    EXECUTING = "executing"
    WAITING = "waiting"
    PAUSED = "paused"
    STOPPED = "stopped"
    FAILED = "failed"
    COMPLETED = "completed"


class AgentCapability(Enum):
    """Agent capabilities."""

    PLANNING = "planning"
    REASONING = "reasoning"
    TOOL_USE = "tool_use"
    MEMORY_ACCESS = "memory_access"
    CONVERSATION = "conversation"
    CODE_EXECUTION = "code_execution"
    WEB_SEARCH = "web_search"
    FILE_OPERATIONS = "file_operations"


@dataclass(frozen=True, slots=True, eq=True)
class AgentPolicy:
    """Policy governing agent behavior."""

    max_steps: int = 100
    max_tools_per_step: int = 10
    timeout_seconds: int = 300
    allow_web_access: bool = False
    allow_file_write: bool = False
    allow_code_execution: bool = False
    required_capabilities: list[AgentCapability] = field(default_factory=list)
    extra_policy: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_steps": self.max_steps,
            "max_tools_per_step": self.max_tools_per_step,
            "timeout_seconds": self.timeout_seconds,
            "allow_web_access": self.allow_web_access,
            "allow_file_write": self.allow_file_write,
            "allow_code_execution": self.allow_code_execution,
            "required_capabilities": [c.value for c in self.required_capabilities],
            "extra_policy": dict(self.extra_policy),
        }


@dataclass(frozen=True, slots=True, eq=True)
class AgentContext:
    """Context for agent execution."""

    agent_id: str = ""
    conversation_id: str = ""
    session_id: str = ""
    memory_scope: str = ""
    tools: list[str] = field(default_factory=list)
    extra_context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "conversation_id": self.conversation_id,
            "session_id": self.session_id,
            "memory_scope": self.memory_scope,
            "tools": list(self.tools),
            "extra_context": dict(self.extra_context),
        }


@dataclass(unsafe_hash=True)
class Agent:
    """An AI agent definition."""

    agent_id: str
    name: str
    description: str = ""
    state: AgentState = AgentState.CREATED
    policy: AgentPolicy = field(default_factory=AgentPolicy)
    capabilities: frozenset[AgentCapability] = field(default_factory=frozenset)
    context: Optional[AgentContext] = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, Any] = field(default_factory=dict)


    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "state": self.state.value,
            "policy": self.policy.to_dict(),
            "capabilities": [c.value for c in self.capabilities],
            "context": self.context.to_dict() if self.context else None,
            "created_at": self.created_at.isoformat(),
            "metadata": dict(self.metadata),
        }


@dataclass
class AgentExecution:
    """Tracks an agent execution run."""

    execution_id: str
    agent_id: str
    state: AgentState = AgentState.CREATED
    step: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    tool_invocations: list[dict[str, Any]] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

    def start(self) -> None:
        self.state = AgentState.EXECUTING
        self.started_at = datetime.now(timezone.utc)
        self.step += 1

    def complete(self, result: Any) -> None:
        self.state = AgentState.COMPLETED
        self.result = result
        self.completed_at = datetime.now(timezone.utc)

    def fail(self, error: str) -> None:
        self.state = AgentState.FAILED
        self.error = error
        self.completed_at = datetime.now(timezone.utc)

    def record_tool_invocation(self, tool_id: str, result: Any) -> None:
        self.tool_invocations.append({
            "tool_id": tool_id,
            "result": result,
            "step": self.step,
        })

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "agent_id": self.agent_id,
            "state": self.state.value,
            "step": self.step,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "tool_invocations": len(self.tool_invocations),
            "error": self.error,
        }


class AgentRegistry:
    """Registry for agents and executions."""

    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}
        self._executions: dict[str, AgentExecution] = {}

    def register(self, agent: Agent) -> None:
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> Optional[Agent]:
        return self._agents.get(agent_id)

    def list_agents(self) -> list[str]:
        return list(self._agents.keys())

    def create_execution(self, agent_id: str, execution_id: str) -> AgentExecution:
        return AgentExecution(execution_id=execution_id, agent_id=agent_id)

    def record_execution(self, execution: AgentExecution) -> None:
        self._executions[execution.execution_id] = execution

    def get_execution(self, execution_id: str) -> Optional[AgentExecution]:
        return self._executions.get(execution_id)

    def get_agent_executions(self, agent_id: str) -> list[AgentExecution]:
        return [
            ex for ex in self._executions.values()
            if ex.agent_id == agent_id
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "agents": list(self._agents.keys()),
            "executions": list(self._executions.keys()),
        }


class AgentScheduler:
    """Schedules agent executions deterministically."""

    def __init__(self) -> None:
        self._queue: list[AgentExecution] = []

    def schedule(self, execution: AgentExecution) -> None:
        self._queue.append(execution)

    def next_execution(self) -> Optional[AgentExecution]:
        return self._queue.pop(0) if self._queue else None

    @property
    def queue_depth(self) -> int:
        return len(self._queue)

    def to_dict(self) -> dict[str, Any]:
        return {
            "queue_depth": self.queue_depth,
            "pending": [ex.to_dict() for ex in self._queue],
        }
