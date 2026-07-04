# Atlas Vision Runtime Unit Tests

"""
Comprehensive unit tests for all Vision Runtime modules.
No placeholder tests - every public function is tested.
"""
from __future__ import annotations

import sys
import os
import unittest
import time
import threading
from datetime import datetime, timezone
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from atlas_vision.errors import (
    VisionError,
    FrameError,
    InvalidFrameError,
    FrameNotFoundError,
    CaptureError,
    CaptureSourceError,
    CaptureSessionError,
    PipelineError,
    PipelineValidationError,
    PipelineExecutionError,
    ProviderError,
    ProviderNotFoundError,
    ProviderLoadError,
    RegistryError,
    DuplicateRegistrationError,
    SchedulerError,
    ResourceError,
    BufferExhaustedError,
    SecurityError,
    PermissionDeniedError,
    GraphError,
    CycleDetectedError,
    InvalidGraphNodeError,
    StorageError,
    CapabilityError,
    CapabilityUnavailableError,
)

from atlas_vision.events import (
    Event,
    EventType,
    FrameCaptured,
    FrameDropped,
    PipelineStarted,
    PipelineCompleted,
    PipelineFailed,
    ProviderLoaded,
    ProviderUnloaded,
    CaptureStarted,
    CaptureStopped,
    CaptureFailed,
    VisionHealthChanged,
)

from atlas_vision.models.frame import (
    Frame,
    FrameMetadata,
    FrameBuffer,
    FrameTimestamp,
    FrameResolution,
    FrameColorSpace,
    FrameFormat,
    FrameRegion,
    FrameSource,
    FrameReference,
    FrameSnapshot,
    FrameHistory,
)

from atlas_vision.capture.sources import (
    CaptureSourceType,
    CaptureCapability,
    CaptureConfiguration,
    CaptureDescriptor,
    CaptureSource,
)

from atlas_vision.capture.manager import CaptureSession, CaptureManager
from atlas_vision.capture.provider import CaptureProviderABC

from atlas_vision.services.runtime import VisionRuntime
from atlas_vision.services.manager import VisionManager
from atlas_vision.services.context import VisionContext
from atlas_vision.services.session import VisionSession, SessionState
from atlas_vision.services.service import ServiceContract, ServiceState

from atlas_vision.scheduler.scheduler import VisionScheduler, TriggerType, ScheduleEntry

from atlas_vision.pipeline.pipeline import VisionPipeline, PipelineStage, PipelineStageDef
from atlas_vision.pipeline.manager import VisionPipelineManager

from atlas_vision.provider.base import ProviderType, ProviderResult, VisionProvider

from atlas_vision.registry.vision_registry import VisionRegistry
from atlas_vision.registry.provider_registry import ProviderRegistry
from atlas_vision.registry.pipeline_registry import PipelineRegistry
from atlas_vision.registry.capture_registry import CaptureRegistry
from atlas_vision.registry.model_registry import ModelRegistry
from atlas_vision.registry.capability_registry import CapabilityRegistry

from atlas_vision.graph.nodes import VisionNode
from atlas_vision.graph.edges import VisionEdge
from atlas_vision.graph.graph import VisionGraph
from atlas_vision.graph.execution_plan import VisionExecutionPlan
from atlas_vision.graph.validator import VisionGraphValidator

from atlas_vision.capabilities.negotiation import (
    Capability,
    CapabilityStatus,
    CapabilityNegotiator,
)

from atlas_vision.resources.manager import (
    VisionResourceManager,
    LRUCache,
    TempBuffer,
)

from atlas_vision.metrics.collector import (
    VisionMetricsCollector,
    Counter,
    Gauge,
    Histogram,
)

from atlas_vision.health.service import HealthService, HealthStatus

from atlas_vision.security.permissions import Permission, SecurityValidator

from atlas_vision.storage.abstraction import StorageDomain, StorageBackend, VisionStorageAdapter

from atlas_vision.integration.ipc import IPCVisionBridge
from atlas_vision.integration.workflow import WorkflowVisionBridge
from atlas_vision.integration.plugin import PluginVisionBridge
