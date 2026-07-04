# Atlas AI Runtime Inference

"""
Deterministic inference execution for the AI Runtime.

Supports InferenceRequest, InferenceResponse, InferenceContext,
InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor,
InferenceResult, InferenceMetadata, InferenceState.
Deterministic scheduling only.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class InferenceState(Enum):
    """Inference job states."""

    PENDING = "pending"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class InferenceMode(Enum):
    """Inference execution modes."""

    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    STREAMING = "streaming"
    BATCH = "batch"


@dataclass(frozen=True, slots=True, eq=True)
class InferenceMetadata:
    """Metadata for an inference job."""

    model_id: str
    provider_id: str = ""
    capability: str = ""
    priority: int = 0
    timeout_ms: int = 30000
    max_retries: int = 0
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "provider_id": self.provider_id,
            "capability": self.capability,
            "priority": self.priority,
            "timeout_ms": self.timeout_ms,
            "max_retries": self.max_retries,
            "extra": dict(self.extra),
        }


@dataclass(eq=True, unsafe_hash=True)
class InferenceRequest:
    """An inference request."""

    prompt: str
    model_id: str
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.9
    stop_sequences: list[str] = field(default_factory=list)
    stream: bool = False
    metadata: Optional[InferenceMetadata] = None
    request_id: str = ""

    def __post_init__(self) -> None:
        if not self.request_id:
            import uuid
            object.__setattr__(self, "request_id", str(uuid.uuid4()))
        if self.metadata is None:
            object.__setattr__(
                self,
                "metadata",
                InferenceMetadata(model_id=self.model_id),
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "prompt": self.prompt,
            "model_id": self.model_id,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "stop_sequences": list(self.stop_sequences),
            "stream": self.stream,
            "metadata": self.metadata.to_dict() if self.metadata else None,
        }


@dataclass(frozen=True, slots=True, eq=True)
class InferenceResult:
    """Result from an inference execution."""

    request_id: str
    text: str = ""
    tokens: list[str] = field(default_factory=list)
    token_count: int = 0
    model_id: str = ""
    finish_reason: str = ""
    usage: dict[str, int] = field(default_factory=dict)
    duration_ms: float = 0.0
    error: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "text": self.text,
            "token_count": self.token_count,
            "model_id": self.model_id,
            "finish_reason": self.finish_reason,
            "usage": dict(self.usage),
            "duration_ms": self.duration_ms,
            "error": self.error,
        }


@dataclass
class InferenceResponse:
    """Wrapper around InferenceResult with context."""

    result: InferenceResult
    context: Optional[InferenceContext] = None

    def to_dict(self) -> dict[str, Any]:
        d = self.result.to_dict()
        if self.context:
            d["context"] = self.context.to_dict()
        return d


@dataclass(frozen=True, slots=True, eq=True)
class InferenceContext:
    """Context for an inference execution."""

    conversation_id: str = ""
    session_id: str = ""
    trace_id: str = ""
    correlation_id: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "session_id": self.session_id,
            "trace_id": self.trace_id,
            "correlation_id": self.correlation_id,
            "extra": dict(self.extra),
        }


@dataclass(eq=True, unsafe_hash=True)
class InferenceJob:
    """A scheduled inference job."""

    request: InferenceRequest
    state: InferenceState = InferenceState.PENDING
    job_id: str = ""
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[InferenceResult] = None
    retry_count: int = 0
    error: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.job_id:
            import uuid
            object.__setattr__(self, "job_id", str(uuid.uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "request_id": self.request.request_id,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "retry_count": self.retry_count,
            "error": self.error,
        }


class InferenceQueue:
    """Priority-based inference job queue."""

    def __init__(self, max_size: int = 10000) -> None:
        self._queue: list[InferenceJob] = []
        self._max_size = max_size

    @property
    def size(self) -> int:
        return len(self._queue)

    @property
    def is_full(self) -> bool:
        return len(self._queue) >= self._max_size

    def enqueue(self, job: InferenceJob) -> bool:
        if self.is_full:
            return False
        self._queue.append(job)
        self._queue.sort(key=lambda j: j.request.metadata.priority if j.request.metadata else 0, reverse=True)
        return True

    def dequeue(self) -> Optional[InferenceJob]:
        if not self._queue:
            return None
        return self._queue.pop(0)

    def peek(self) -> Optional[InferenceJob]:
        return self._queue[0] if self._queue else None

    def cancel(self, job_id: str) -> bool:
        for i, job in enumerate(self._queue):
            if job.job_id == job_id:
                self._queue.pop(i)
                return True
        return False

    def list_jobs(self) -> list[dict[str, Any]]:
        return [job.to_dict() for job in self._queue]

    def clear(self) -> None:
        self._queue.clear()


class InferenceScheduler:
    """Deterministic inference scheduler."""

    def __init__(self, queue: Optional[InferenceQueue] = None) -> None:
        self._queue = queue or InferenceQueue()
        self._running = False

    def schedule(self, job: InferenceJob) -> bool:
        if not self._queue.enqueue(job):
            return False
        return True

    def next_job(self) -> Optional[InferenceJob]:
        return self._queue.dequeue()

    def cancel(self, job_id: str) -> bool:
        return self._queue.cancel(job_id)

    @property
    def queue_depth(self) -> int:
        return self._queue.size

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "queue_depth": self.queue_depth,
            "running": self._running,
            "jobs": self._queue.list_jobs(),
        }


class InferenceExecutor:
    """Executes inference jobs against providers."""

    def execute(
        self,
        job: InferenceJob,
        provider: Any,
    ) -> InferenceResult:
        if job.state != InferenceState.SCHEDULED:
            from atlas_ai.errors import InferenceExecutionError
            raise InferenceExecutionError(
                f"Job {job.job_id} is not in SCHEDULED state",
                job.job_id,
            )
        job.started_at = datetime.now(timezone.utc)
        job.state = InferenceState.RUNNING
        try:
            result = provider.run_inference(job.request)
            job.result = result
            job.state = InferenceState.COMPLETED
            job.completed_at = datetime.now(timezone.utc)
            return result
        except Exception as exc:
            job.error = str(exc)
            job.state = InferenceState.FAILED
            job.completed_at = datetime.now(timezone.utc)
            from atlas_ai.errors import InferenceExecutionError
            raise InferenceExecutionError(str(exc), job.job_id) from exc
