# Atlas AI Runtime Models

"""
Immutable model management types for the AI Runtime.

Supports Model, ModelVersion, ModelDescriptor, ModelMetadata,
ModelCapability, ModelProvider, ModelInstance, ModelConfiguration,
ModelRequirements, ModelResourceUsage, ModelLifecycle, ModelState,
ModelSnapshot, and ModelRegistry.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class ModelCapability(Enum):
    """Supported AI capabilities."""

    CHAT = "chat"
    COMPLETION = "completion"
    EMBEDDING = "embedding"
    VISION = "vision"
    AUDIO = "audio"
    IMAGE = "image"
    TOOL_CALLING = "tool_calling"
    STRUCTURED_OUTPUT = "structured_output"
    STREAMING = "streaming"
    BATCH = "batch"
    FINE_TUNING = "fine_tuning"
    RAG = "rag"
    MEMORY = "memory"
    REASONING = "reasoning"


class ModelState(Enum):
    """Model lifecycle states."""

    CREATED = "created"
    LOADING = "loading"
    READY = "ready"
    RUNNING = "running"
    UNLOADING = "unloading"
    UNLOADED = "unloaded"
    ERROR = "error"
    SNAPSHOT = "snapshot"


class ModelProvider(Enum):
    """Model provider types."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLAMA = "ollama"
    LLAMA_CPP = "llamacpp"
    ONNX = "onnx"
    TENSORRT = "tensorrt"
    CUDA = "cuda"
    CUSTOM = "custom"
    PLUGIN = "plugin"


@dataclass(frozen=True, slots=True, eq=True)
class ModelVersion:
    """Immutable model version descriptor."""

    version: str
    build_number: int = 0
    git_sha: str = ""
    released_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    changelog: str = ""

    def __post_init__(self) -> None:
        if not self.version:
            raise ValueError("ModelVersion requires a non-empty version string")


@dataclass(frozen=True, slots=True, eq=True)
class ModelMetadata:
    """Immutable model metadata."""

    creator: str = ""
    license: str = ""
    tags: list[str] = field(default_factory=list)
    size_bytes: int = 0
    parameters_count: int = 0
    context_window: int = 4096
    supported_languages: list[str] = field(default_factory=list)
    benchmarks: dict[str, float] = field(default_factory=dict)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True, eq=True)
class ModelRequirements:
    """Model hardware/software requirements."""

    min_gpu_memory_mb: int = 0
    min_cpu_cores: int = 1
    min_ram_mb: int = 512
    requires_cuda: bool = False
    requires_tensorrt: bool = False
    min_driver_version: str = ""
    extra_requirements: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True, eq=True)
class ModelResourceUsage:
    """Tracks resource usage for a model."""

    gpu_memory_mb: float = 0.0
    cpu_percent: float = 0.0
    ram_mb: float = 0.0
    disk_io_mbps: float = 0.0
    network_mbps: float = 0.0
    inference_count: int = 0
    total_tokens_processed: int = 0
    last_used_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass(frozen=True, slots=True, eq=True)
class ModelConfiguration:
    """Model runtime configuration."""

    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 2048
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: list[str] = field(default_factory=list)
    response_format: Optional[str] = None
    stream: bool = False
    extra_config: dict[str, Any] = field(default_factory=dict)

    def clone_with(self, **overrides: Any) -> ModelConfiguration:
        new_extra = dict(self.extra_config)
        new_extra.update(overrides.pop("extra_config", {}))
        return ModelConfiguration(
            temperature=overrides.get("temperature", self.temperature),
            top_p=overrides.get("top_p", self.top_p),
            max_tokens=overrides.get("max_tokens", self.max_tokens),
            frequency_penalty=overrides.get(
                "frequency_penalty", self.frequency_penalty
            ),
            presence_penalty=overrides.get(
                "presence_penalty", self.presence_penalty
            ),
            stop_sequences=overrides.get(
                "stop_sequences", self.stop_sequences
            ),
            response_format=overrides.get(
                "response_format", self.response_format
            ),
            stream=overrides.get("stream", self.stream),
            extra_config=new_extra,
        )


@dataclass(frozen=True, slots=True, eq=True)
class ModelSnapshot:
    """Immutable model state snapshot."""

    snapshot_id: str
    model_id: str
    state: ModelState
    configuration: ModelConfiguration
    resource_usage: ModelResourceUsage
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(unsafe_hash=True)
class ModelDescriptor:
    """Describes a model without instantiating it."""

    model_id: str
    name: str
    provider: ModelProvider
    version: ModelVersion
    capabilities: frozenset[ModelCapability]
    metadata: ModelMetadata
    requirements: ModelRequirements
    configuration: ModelConfiguration


    def supports(self, capability: ModelCapability) -> bool:
        return capability in self.capabilities

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "name": self.name,
            "provider": self.provider.value,
            "version": self.version.version,
            "capabilities": [c.value for c in self.capabilities],
            "metadata": {
                "creator": self.metadata.creator,
                "license": self.metadata.license,
                "tags": list(self.metadata.tags),
                "parameters_count": self.metadata.parameters_count,
                "context_window": self.metadata.context_window,
            },
            "configuration": {
                "temperature": self.configuration.temperature,
                "max_tokens": self.configuration.max_tokens,
                "stream": self.configuration.stream,
            },
        }


@dataclass(unsafe_hash=True)
class ModelInstance:
    """Represents a loaded model instance."""

    descriptor: ModelDescriptor
    state: ModelState = ModelState.CREATED
    resource_usage: ModelResourceUsage = field(default_factory=ModelResourceUsage)
    loaded_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    instance_id: str = ""

    def __post_init__(self) -> None:
        if not self.instance_id:
            self.instance_id = self.descriptor.model_id


    def update_resource_usage(self) -> None:
        self.resource_usage.last_used_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "model_id": self.descriptor.model_id,
            "state": self.state.value,
            "resource_usage": {
                "gpu_memory_mb": self.resource_usage.gpu_memory_mb,
                "cpu_percent": self.resource_usage.cpu_percent,
                "ram_mb": self.resource_usage.ram_mb,
                "inference_count": self.resource_usage.inference_count,
                "total_tokens_processed": self.resource_usage.total_tokens_processed,
            },
        }
