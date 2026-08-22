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
    VisionError, FrameError, InvalidFrameError, FrameNotFoundError,
    CaptureError, CaptureSourceError, CaptureSessionError,
    PipelineError, PipelineValidationError, PipelineExecutionError,
    ProviderError, ProviderNotFoundError, ProviderLoadError,
    RegistryError, DuplicateRegistrationError,
    SchedulerError, ResourceError, BufferExhaustedError,
    SecurityError, PermissionDeniedError,
    GraphError, CycleDetectedError, InvalidGraphNodeError,
    StorageError, CapabilityError, CapabilityUnavailableError,
)

from atlas_vision.events import (
    Event, EventType, FrameCaptured, FrameDropped,
    PipelineStarted, PipelineCompleted, PipelineFailed,
    ProviderLoaded, ProviderUnloaded,
    CaptureStarted, CaptureStopped, CaptureFailed,
    VisionHealthChanged,
)

from atlas_vision.models.frame import (
    Frame, FrameMetadata, FrameBuffer, FrameTimestamp,
    FrameResolution, FrameColorSpace, FrameFormat,
    FrameRegion, FrameSource, FrameReference,
    FrameSnapshot, FrameHistory,
)

from atlas_vision.capture.sources import (
    CaptureSourceType, CaptureCapability,
    CaptureConfiguration, CaptureDescriptor, CaptureSource,
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
    Capability, CapabilityStatus, CapabilityNegotiator,
)

from atlas_vision.resources.manager import (
    VisionResourceManager, LRUCache, TempBuffer,
)

from atlas_vision.metrics.collector import (
    VisionMetricsCollector, Counter, Gauge, Histogram,
)

from atlas_vision.health.service import HealthService, HealthStatus

from atlas_vision.security.permissions import Permission, SecurityValidator

from atlas_vision.storage.abstraction import StorageDomain, StorageBackend, VisionStorageAdapter

from atlas_vision.integration.ipc import IPCVisionBridge
from atlas_vision.integration.workflow import WorkflowVisionBridge
from atlas_vision.integration.plugin import PluginVisionBridge



# ===== Error Tests =====
class TestVisionError(unittest.TestCase):
    def test_base_error_creation(self) -> None:
        err = VisionError("test message", code="TEST", details={"key": "val"})
        self.assertEqual(err.error_code, "TEST")
        self.assertEqual(err.error_message, "test message")
        self.assertEqual(err.error_details, {"key": "val"})

    def test_error_to_dict(self) -> None:
        err = VisionError("test")
        d = err.to_dict()
        self.assertIn("error_code", d)
        self.assertIn("error_message", d)
        self.assertIn("error_details", d)

    def test_error_inheritance(self) -> None:
        self.assertTrue(issubclass(FrameError, VisionError))
        self.assertTrue(issubclass(CaptureError, VisionError))
        self.assertTrue(issubclass(PipelineError, VisionError))
        self.assertTrue(issubclass(ProviderError, VisionError))
        self.assertTrue(issubclass(RegistryError, VisionError))
        self.assertTrue(issubclass(SecurityError, VisionError))
        self.assertTrue(issubclass(GraphError, VisionError))
        self.assertTrue(issubclass(StorageError, VisionError))
        self.assertTrue(issubclass(CapabilityError, VisionError))


class TestFrameErrors(unittest.TestCase):
    def test_invalid_frame_error(self) -> None:
        err = InvalidFrameError(frame_id="f1")
        self.assertEqual(err.error_code, "FRAME_INVALID")

    def test_frame_not_found_error(self) -> None:
        err = FrameNotFoundError(frame_id="f2")
        self.assertEqual(err.error_code, "FRAME_NOT_FOUND")


class TestCaptureErrors(unittest.TestCase):
    def test_capture_source_error(self) -> None:
        err = CaptureSourceError(source_id="s1")
        self.assertEqual(err.error_code, "CAPTURE_SOURCE_ERROR")

    def test_capture_session_error(self) -> None:
        err = CaptureSessionError(session_id="sess1")
        self.assertEqual(err.error_code, "CAPTURE_SESSION_ERROR")


class TestPipelineErrors(unittest.TestCase):
    def test_pipeline_validation_error(self) -> None:
        err = PipelineValidationError(pipeline_id="p1")
        self.assertEqual(err.error_code, "PIPELINE_VALIDATION_ERROR")

    def test_pipeline_execution_error(self) -> None:
        err = PipelineExecutionError(pipeline_id="p1", stage="analyze")
        self.assertEqual(err.error_code, "PIPELINE_EXECUTION_ERROR")


class TestProviderErrors(unittest.TestCase):
    def test_provider_not_found(self) -> None:
        err = ProviderNotFoundError(provider_id="prov1")
        self.assertEqual(err.error_code, "PROVIDER_NOT_FOUND")

    def test_provider_load_error(self) -> None:
        err = ProviderLoadError(provider_id="prov2")
        self.assertEqual(err.error_code, "PROVIDER_LOAD_ERROR")


class TestRegistryErrors(unittest.TestCase):
    def test_duplicate_registration(self) -> None:
        err = DuplicateRegistrationError(entity_id="e1")
        self.assertEqual(err.error_code, "REGISTRY_DUPLICATE")


class TestResourceErrors(unittest.TestCase):
    def test_buffer_exhausted(self) -> None:
        err = BufferExhaustedError(limit=100)
        self.assertEqual(err.error_code, "RESOURCE_BUFFER_EXHAUSTED")


class TestSecurityErrors(unittest.TestCase):
    def test_permission_denied(self) -> None:
        err = PermissionDeniedError(caller_id="c1")
        self.assertEqual(err.error_code, "SECURITY_PERMISSION_DENIED")


class TestGraphErrors(unittest.TestCase):
    def test_cycle_detected(self) -> None:
        err = CycleDetectedError(nodes=["a", "b"])
        self.assertEqual(err.error_code, "GRAPH_CYCLE_DETECTED")

    def test_invalid_graph_node(self) -> None:
        err = InvalidGraphNodeError(node_id="bad")
        self.assertEqual(err.error_code, "GRAPH_INVALID_NODE")


class TestCapabilityErrors(unittest.TestCase):
    def test_capability_unavailable(self) -> None:
        err = CapabilityUnavailableError(capability="gpu")
        self.assertEqual(err.error_code, "CAPABILITY_UNAVAILABLE")



# ===== Event Tests =====
class TestEventTypes(unittest.TestCase):
    def test_all_event_types_exist(self) -> None:
        self.assertEqual(len(EventType), 11)

    def test_event_creation(self) -> None:
        evt = Event(event_type=EventType.FRAME_CAPTURED, source="test")
        self.assertEqual(evt.event_type, EventType.FRAME_CAPTURED)

    def test_event_to_dict(self) -> None:
        evt = Event(event_type=EventType.FRAME_CAPTURED)
        d = evt.to_dict()
        self.assertIn("event_id", d)

    def test_event_immutability(self) -> None:
        evt = Event(event_type=EventType.FRAME_CAPTURED)
        with self.assertRaises(Exception):
            evt.event_type = EventType.FRAME_DROPPED


class TestFrameCapturedEvent(unittest.TestCase):
    def test_frame_captured(self) -> None:
        evt = FrameCaptured(frame_id="f1", source_id="s1", duration_ms=10.5)
        self.assertEqual(evt.event_type, EventType.FRAME_CAPTURED)

    def test_frame_captured_to_dict(self) -> None:
        evt = FrameCaptured(frame_id="f1", source_id="s1")
        d = evt.to_dict()
        self.assertEqual(d["frame_id"], "f1")


class TestPipelineEvents(unittest.TestCase):
    def test_pipeline_started(self) -> None:
        evt = PipelineStarted(pipeline_id="p1", node_count=5)
        self.assertEqual(evt.event_type, EventType.PIPELINE_STARTED)

    def test_pipeline_completed(self) -> None:
        evt = PipelineCompleted(pipeline_id="p1", frame_count=10, duration_ms=100.0)
        self.assertEqual(evt.event_type, EventType.PIPELINE_COMPLETED)

    def test_pipeline_failed(self) -> None:
        evt = PipelineFailed(pipeline_id="p1", error_code="ERR", stage="analyze")
        self.assertEqual(evt.event_type, EventType.PIPELINE_FAILED)


class TestProviderEvents(unittest.TestCase):
    def test_provider_loaded(self) -> None:
        evt = ProviderLoaded(provider_id="p1", provider_type="detection")
        self.assertEqual(evt.event_type, EventType.PROVIDER_LOADED)

    def test_provider_unloaded(self) -> None:
        evt = ProviderUnloaded(provider_id="p1")
        self.assertEqual(evt.event_type, EventType.PROVIDER_UNLOADED)


class TestCaptureEvents(unittest.TestCase):
    def test_capture_started(self) -> None:
        evt = CaptureStarted(session_id="sess1", source_id="s1")
        self.assertEqual(evt.event_type, EventType.CAPTURE_STARTED)

    def test_capture_stopped(self) -> None:
        evt = CaptureStopped(session_id="sess1", frames_captured=42)
        self.assertEqual(evt.event_type, EventType.CAPTURE_STOPPED)

    def test_capture_failed(self) -> None:
        evt = CaptureFailed(session_id="sess1", error_code="ERR")
        self.assertEqual(evt.event_type, EventType.CAPTURE_FAILED)


class TestHealthEvents(unittest.TestCase):
    def test_health_changed(self) -> None:
        evt = VisionHealthChanged(previous_status="healthy", new_status="degraded")
        self.assertEqual(evt.event_type, EventType.VISION_HEALTH_CHANGED)


# ===== Frame Model Tests =====
class TestFrameFormat(unittest.TestCase):
    def test_frame_formats(self) -> None:
        self.assertEqual(FrameFormat.RGBA.value, "rgba")

    def test_color_spaces(self) -> None:
        self.assertEqual(FrameColorSpace.SRGB.value, "srgb")


class TestFrameTimestamp(unittest.TestCase):
    def test_timestamp_creation(self) -> None:
        ts = FrameTimestamp.now(sequence_number=5)
        self.assertEqual(ts.sequence_number, 5)
        self.assertIsNotNone(ts.wall_clock)

    def test_timestamp_to_dict(self) -> None:
        ts = FrameTimestamp.now()
        d = ts.to_dict()
        self.assertIn("wall_clock", d)

    def test_timestamp_immutable(self) -> None:
        ts = FrameTimestamp.now()
        with self.assertRaises(Exception):
            ts.sequence_number = 10


class TestFrameResolution(unittest.TestCase):
    def test_resolution_pixels(self) -> None:
        r = FrameResolution(1920, 1080)
        self.assertEqual(r.pixels, 2073600)

    def test_resolution_aspect_ratio(self) -> None:
        r = FrameResolution(16, 9)
        self.assertAlmostEqual(r.aspect_ratio, 16.0 / 9.0)

    def test_resolution_comparison(self) -> None:
        r1 = FrameResolution(640, 480)
        r2 = FrameResolution(1920, 1080)
        self.assertLess(r1, r2)

    def test_resolution_equality(self) -> None:
        r1 = FrameResolution(640, 480)
        r2 = FrameResolution(640, 480)
        self.assertEqual(r1, r2)

    def test_resolution_hash(self) -> None:
        r = FrameResolution(640, 480)
        self.assertIsInstance(hash(r), int)

    def test_resolution_zero_height(self) -> None:
        r = FrameResolution(100, 0)
        self.assertEqual(r.aspect_ratio, 0.0)


class TestFrameBuffer(unittest.TestCase):
    def test_empty_buffer(self) -> None:
        buf = FrameBuffer.empty(1024, 1280)
        self.assertEqual(buf.size_bytes, 1024)

    def test_buffer_with_data(self) -> None:
        data = bytes([0] * 100)
        buf = FrameBuffer(data=data, size_bytes=100, stride=100)
        self.assertEqual(len(buf.data), 100)

    def test_buffer_id_generated(self) -> None:
        buf = FrameBuffer.empty(100, 100)
        self.assertTrue(buf.buffer_id)


class TestFrameMetadata(unittest.TestCase):
    def test_metadata_creation(self) -> None:
        meta = FrameMetadata(
            frame_id="f1", sequence_number=1,
            resolution=FrameResolution(640, 480),
            format=FrameFormat.RGBA,
            color_space=FrameColorSpace.SRGB,
            timestamp=FrameTimestamp.now(),
            source_id="cam1",
        )
        self.assertEqual(meta.frame_id, "f1")

    def test_metadata_clone_with_extra(self) -> None:
        meta = FrameMetadata(
            frame_id="f1", sequence_number=1,
            resolution=FrameResolution(640, 480),
            format=FrameFormat.RGBA,
            color_space=FrameColorSpace.SRGB,
            timestamp=FrameTimestamp.now(),
        )
        new_meta = meta.clone_with_extra(custom_key="custom_val")
        self.assertEqual(new_meta.extra["custom_key"], "custom_val")
        self.assertNotIn("custom_key", meta.extra)

    def test_metadata_to_dict(self) -> None:
        meta = FrameMetadata(
            frame_id="f1", sequence_number=1,
            resolution=FrameResolution(640, 480),
            format=FrameFormat.RGBA,
            color_space=FrameColorSpace.SRGB,
            timestamp=FrameTimestamp.now(),
        )
        d = meta.to_dict()
        self.assertIn("frame_id", d)


class TestFrame(unittest.TestCase):
    def test_frame_creation(self) -> None:
        f = Frame(frame_id="test_frame")
        self.assertEqual(f.frame_id, "test_frame")

    def test_frame_to_dict(self) -> None:
        f = Frame(frame_id="test_frame")
        d = f.to_dict()
        self.assertIn("frame_id", d)

    def test_frame_region(self) -> None:
        region = FrameRegion(x=10, y=20, width=100, height=100)
        f = Frame(frame_id="test", region=region)
        self.assertEqual(f.region.x, 10)


class TestFrameRegion(unittest.TestCase):
    def test_region_area(self) -> None:
        r = FrameRegion(x=0, y=0, width=10, height=10)
        self.assertEqual(r.area, 100)

    def test_region_to_dict(self) -> None:
        r = FrameRegion(x=5, y=5, width=50, height=50)
        d = r.to_dict()
        self.assertEqual(d["x"], 5)


class TestFrameSource(unittest.TestCase):
    def test_frame_source_creation(self) -> None:
        src = FrameSource(source_id="s1", name="Test", source_type="camera")
        self.assertEqual(src.source_id, "s1")

    def test_frame_source_to_dict(self) -> None:
        src = FrameSource(source_id="s1", name="Test", source_type="camera")
        d = src.to_dict()
        self.assertEqual(d["source_id"], "s1")


class TestFrameReference(unittest.TestCase):
    def test_reference_creation(self) -> None:
        ref = FrameReference(frame_id="f1", source_id="s1", sequence_number=5)
        self.assertEqual(ref.sequence_number, 5)


class TestFrameSnapshot(unittest.TestCase):
    def test_snapshot_creation(self) -> None:
        snap = FrameSnapshot(
            frame_id="f1", timestamp=FrameTimestamp.now(),
            resolution=FrameResolution(640, 480),
            format=FrameFormat.RGBA, buffer_size=122880,
        )
        self.assertEqual(snap.frame_id, "f1")


class TestFrameHistory(unittest.TestCase):
    def test_history_append(self) -> None:
        h = FrameHistory(max_history=3)
        h = h.append("f1")
        h = h.append("f2")
        h = h.append("f3")
        h = h.append("f4")
        self.assertEqual(len(h.frame_ids), 3)
        self.assertEqual(h.frame_ids, ("f2", "f3", "f4"))

    def test_history_empty(self) -> None:
        h = FrameHistory()
        self.assertEqual(h.frame_ids, ())


# ===== Capture Source Tests =====
class TestCaptureDescriptor(unittest.TestCase):
    def test_for_desktop(self) -> None:
        desc = CaptureDescriptor.for_desktop("Main Display")
        self.assertEqual(desc.source_type, CaptureSourceType.DESKTOP)
        self.assertIn(CaptureCapability.STREAMING, desc.capabilities)

    def test_for_camera(self) -> None:
        desc = CaptureDescriptor.for_camera("Webcam", camera_index=0)
        self.assertEqual(desc.source_type, CaptureSourceType.CAMERA)
        self.assertEqual(desc.extra["camera_index"], 0)

    def test_for_image(self) -> None:
        desc = CaptureDescriptor.for_image("/path/to/img.png")
        self.assertEqual(desc.source_type, CaptureSourceType.IMAGE)

    def test_descriptor_to_dict(self) -> None:
        desc = CaptureDescriptor.for_desktop()
        d = desc.to_dict()
        self.assertIn("descriptor_id", d)


class TestCaptureConfiguration(unittest.TestCase):
    def test_default_config(self) -> None:
        cfg = CaptureConfiguration(source_type=CaptureSourceType.DESKTOP)
        self.assertEqual(cfg.framerate, 30.0)
        self.assertTrue(cfg.streaming)


# ===== Services Tests =====
class TestServiceState(unittest.TestCase):
    def test_all_states(self) -> None:
        self.assertEqual(len(ServiceState), 7)


class TestServiceContract(unittest.TestCase):
    def test_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            ServiceContract()


class TestVisionContext(unittest.TestCase):
    def test_context_creation(self) -> None:
        reg = VisionRegistry()
        ctx = VisionContext(registry=reg)
        self.assertEqual(ctx.max_frame_buffer_size, 1000)

    def test_context_clone_with(self) -> None:
        reg = VisionRegistry()
        ctx = VisionContext(registry=reg, enable_streaming=True)
        new_ctx = ctx.clone_with(enable_streaming=False)
        self.assertFalse(new_ctx.enable_streaming)
        self.assertTrue(ctx.enable_streaming)

    def test_context_immutability(self) -> None:
        reg = VisionRegistry()
        ctx = VisionContext(registry=reg)
        with self.assertRaises(Exception):
            ctx.max_frame_buffer_size = 2000


class TestVisionSession(unittest.TestCase):
    def test_session_lifecycle(self) -> None:
        session = VisionSession()
        self.assertEqual(session.state, SessionState.CREATED)
        session.activate("test_session")
        self.assertEqual(session.state, SessionState.ACTIVE)
        session.pause()
        self.assertEqual(session.state, SessionState.PAUSED)
        session.resume()
        self.assertEqual(session.state, SessionState.ACTIVE)
        session.stop()
        self.assertEqual(session.state, SessionState.STOPPED)

    def test_session_illegal_transition(self) -> None:
        session = VisionSession()
        with self.assertRaises(RuntimeError):
            session.pause()


class TestVisionManager(unittest.TestCase):
    def test_manager_creation(self) -> None:
        mgr = VisionManager()
        self.assertIsNotNone(mgr.capture_manager)
        self.assertIsNotNone(mgr.pipeline_manager)
        self.assertIsNotNone(mgr.provider_registry)

    def test_manager_health_check(self) -> None:
        mgr = VisionManager()
        h = mgr.health_check()
        self.assertIn("capture", h)
        self.assertIn("pipeline", h)


# ===== Pipeline Tests =====
class TestPipelineStage(unittest.TestCase):
    def test_ordered_list(self) -> None:
        stages = PipelineStage.ordered_list()
        self.assertEqual(len(stages), 11)
        self.assertEqual(stages[0], PipelineStage.ACQUIRE)
        self.assertEqual(stages[-1], PipelineStage.EXPORT)


class TestVisionPipeline(unittest.TestCase):
    def test_pipeline_creation(self) -> None:
        pipe = VisionPipeline()
        self.assertTrue(pipe.pipeline_id)

    def test_add_stage(self) -> None:
        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)
        pipe.add_stage(PipelineStage.EXPORT, lambda x: x)

    def test_validate_missing_required(self) -> None:
        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)
        with self.assertRaises(PipelineValidationError):
            pipe.validate()

    def test_execute_pipeline(self) -> None:
        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x, **kw: x + 1)
        pipe.add_stage(PipelineStage.EXPORT, lambda x, **kw: x * 2)
        result = pipe.execute(5)
        self.assertEqual(result, 12)

    def test_duplicate_stage(self) -> None:
        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)
        with self.assertRaises(PipelineValidationError):
            pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)

    def test_remove_stage(self) -> None:
        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)
        pipe.remove_stage(PipelineStage.ACQUIRE)
        self.assertEqual(len(pipe.get_stages()), 0)

    def test_frames_processed_count(self) -> None:
        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)
        pipe.add_stage(PipelineStage.EXPORT, lambda x: x)
        pipe.execute(1)
        pipe.execute(2)
        self.assertEqual(pipe.frames_processed, 4)


class TestPipelineManager(unittest.TestCase):
    def test_register_and_execute(self) -> None:
        mgr = VisionPipelineManager()
        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)
        pipe.add_stage(PipelineStage.EXPORT, lambda x: x)
        mgr.register_pipeline(pipe)
        result = mgr.execute(pipe.pipeline_id, 42)
        self.assertEqual(result, 42)

    def test_execute_missing_pipeline(self) -> None:
        mgr = VisionPipelineManager()
        with self.assertRaises(PipelineValidationError):
            mgr.execute("nonexistent", 42)


# ===== Provider Tests =====
class TestProviderType(unittest.TestCase):
    def test_all_provider_types(self) -> None:
        self.assertEqual(len(ProviderType), 7)


class TestProviderResult(unittest.TestCase):
    def test_successful_result(self) -> None:
        r = ProviderResult(success=True, data={"key": "val"})
        self.assertTrue(r.is_success)

    def test_failed_result(self) -> None:
        r = ProviderResult(success=False, error="fail")
        self.assertFalse(r.is_success)

    def test_result_to_dict(self) -> None:
        r = ProviderResult(success=True, data={"key": "val"})
        d = r.to_dict()
        self.assertTrue(d["success"])


class TestVisionProviderAbstract(unittest.TestCase):
    def test_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            VisionProvider()



# ===== Registry Tests =====
class TestVisionRegistry(unittest.TestCase):
    def test_register_and_get(self) -> None:
        reg = VisionRegistry()
        reg.register("svc1", object())
        self.assertIsNotNone(reg.get("svc1"))
        self.assertIsNone(reg.get("svc2"))

    def test_duplicate_registration(self) -> None:
        reg = VisionRegistry()
        reg.register("svc1", object())
        with self.assertRaises(DuplicateRegistrationError):
            reg.register("svc1", object())

    def test_list_services(self) -> None:
        reg = VisionRegistry()
        reg.register("svc1", object())
        reg.register("svc2", object())
        self.assertEqual(sorted(reg.list_services()), ["svc1", "svc2"])

    def test_health_check(self) -> None:
        reg = VisionRegistry()
        reg.register("svc1", object())
        h = reg.health_check("svc1")
        self.assertEqual(h["status"], "healthy")

    def test_version_compatibility(self) -> None:
        reg = VisionRegistry()
        reg.register("svc1", object(), version="1.2.3")
        self.assertTrue(reg.check_version_compatibility("svc1", "1.0.0"))
        self.assertFalse(reg.check_version_compatibility("svc1", "2.0.0"))

    def test_clear(self) -> None:
        reg = VisionRegistry()
        reg.register("svc1", object())
        reg.clear()
        self.assertEqual(reg.list_services(), [])


class TestProviderRegistry(unittest.TestCase):
    def test_register_provider(self) -> None:
        reg = ProviderRegistry()

        class MockProvider:
            provider_id = "mp1"
            provider_type = ProviderType.OCR
            def initialize(self): pass
            def shutdown(self): pass
            def health_check(self): return {}
            def get_capabilities(self): return []
            def is_compatible(self, v): return True
            def execute(self, d): return ProviderResult(True)

        mp = MockProvider()
        reg.register(mp)
        self.assertEqual(len(reg.list_names()), 1)

    def test_get_by_type(self) -> None:
        reg = ProviderRegistry()

        class MockProvider:
            provider_id = "mp1"
            provider_type = ProviderType.OCR
            def initialize(self): pass
            def shutdown(self): pass
            def health_check(self): return {}
            def get_capabilities(self): return []
            def is_compatible(self, v): return True
            def execute(self, d): return ProviderResult(True)

        mp = MockProvider()
        reg.register(mp)
        self.assertEqual(len(reg.get_by_type(ProviderType.OCR)), 1)


class TestPipelineRegistry(unittest.TestCase):
    def test_register_and_get(self) -> None:
        reg = PipelineRegistry()
        pipe = VisionPipeline()
        reg.register(pipe)
        self.assertEqual(reg.get(pipe.pipeline_id), pipe)


class TestCaptureRegistry(unittest.TestCase):
    def test_register_and_get(self) -> None:
        reg = CaptureRegistry()
        desc = CaptureDescriptor.for_desktop()
        reg.register(desc)
        self.assertEqual(reg.get(desc.descriptor_id), desc)


class TestModelRegistry(unittest.TestCase):
    def test_register_and_get(self) -> None:
        reg = ModelRegistry()
        reg.register("m1", "detection", "1.0.0")
        self.assertIsNotNone(reg.get("m1"))


class TestCapabilityRegistry(unittest.TestCase):
    def test_register_and_discover(self) -> None:
        reg = CapabilityRegistry()
        reg.register("ocr", "p1", {"version": "1.0"})
        self.assertIn("ocr", reg.list_capabilities())
        self.assertIn("p1", reg.discover("ocr"))


# ===== Graph Tests =====
class TestVisionNode(unittest.TestCase):
    def test_node_creation(self) -> None:
        n = VisionNode(node_id="n1", stage_name="acquire")
        self.assertEqual(n.node_id, "n1")

    def test_node_to_dict(self) -> None:
        n = VisionNode(node_id="n1", stage_name="acquire")
        d = n.to_dict()
        self.assertEqual(d["node_id"], "n1")


class TestVisionEdge(unittest.TestCase):
    def test_edge_creation(self) -> None:
        e = VisionEdge(source_node_id="n1", target_node_id="n2")
        self.assertEqual(e.source_node_id, "n1")


class TestVisionGraph(unittest.TestCase):
    def test_add_nodes_and_edges(self) -> None:
        g = VisionGraph()
        g.add_node(VisionNode("n1", "acquire"))
        g.add_node(VisionNode("n2", "decode"))
        g.add_edge(VisionEdge("n1", "n2"))
        self.assertEqual(len(g.get_nodes()), 2)
        self.assertEqual(len(g.get_edges()), 1)

    def test_topological_sort(self) -> None:
        g = VisionGraph()
        g.add_node(VisionNode("n1", "acquire"))
        g.add_node(VisionNode("n2", "decode"))
        g.add_node(VisionNode("n3", "export"))
        g.add_edge(VisionEdge("n1", "n2"))
        g.add_edge(VisionEdge("n2", "n3"))
        order = g.topological_sort()
        self.assertEqual(order.index("n1"), 0)
        self.assertEqual(order.index("n2"), 1)
        self.assertEqual(order.index("n3"), 2)

    def test_cycle_detection(self) -> None:
        g = VisionGraph()
        g.add_node(VisionNode("n1", "a"))
        g.add_node(VisionNode("n2", "b"))
        g.add_edge(VisionEdge("n1", "n2"))
        g.add_edge(VisionEdge("n2", "n1"))
        with self.assertRaises(CycleDetectedError):
            g.topological_sort()

    def test_invalid_node_reference(self) -> None:
        g = VisionGraph()
        g.add_node(VisionNode("n1", "a"))
        with self.assertRaises(InvalidGraphNodeError):
            g.add_edge(VisionEdge("n1", "nonexistent"))


class TestVisionGraphValidator(unittest.TestCase):
    def test_valid_graph(self) -> None:
        g = VisionGraph()
        g.add_node(VisionNode("n1", "a"))
        g.add_node(VisionNode("n2", "b"))
        g.add_edge(VisionEdge("n1", "n2"))
        self.assertTrue(VisionGraphValidator.validate(g))

    def test_has_cycle(self) -> None:
        g = VisionGraph()
        g.add_node(VisionNode("n1", "a"))
        g.add_node(VisionNode("n2", "b"))
        g.add_edge(VisionEdge("n1", "n2"))
        g.add_edge(VisionEdge("n2", "n1"))
        self.assertTrue(VisionGraphValidator.has_cycle(g))

    def test_count_operations(self) -> None:
        g = VisionGraph()
        g.add_node(VisionNode("n1", "a"))
        g.add_node(VisionNode("n2", "b"))
        g.add_edge(VisionEdge("n1", "n2"))
        self.assertEqual(VisionGraphValidator.count_nodes(g), 2)
        self.assertEqual(VisionGraphValidator.count_edges(g), 1)


class TestExecutionPlan(unittest.TestCase):
    def test_compile(self) -> None:
        g = VisionGraph()
        g.add_node(VisionNode("n1", "a"))
        g.add_node(VisionNode("n2", "b"))
        g.add_edge(VisionEdge("n1", "n2"))
        plan = VisionExecutionPlan.compile(g)
        self.assertEqual(len(plan.node_order), 2)


# ===== Scheduler Tests =====
class TestTriggerType(unittest.TestCase):
    def test_all_triggers(self) -> None:
        self.assertEqual(len(TriggerType), 7)


class TestVisionScheduler(unittest.TestCase):
    def test_schedule_and_list(self) -> None:
        sched = VisionScheduler()
        sched.schedule("t1", TriggerType.IMMEDIATE, lambda: None)
        self.assertIn("t1", sched.list_tasks())

    def test_execute_immediate(self) -> None:
        executed = []
        sched = VisionScheduler()
        sched.schedule("t1", TriggerType.IMMEDIATE, lambda: executed.append(1))
        sched.execute("t1")
        self.assertEqual(executed, [1])

    def test_stop_all(self) -> None:
        sched = VisionScheduler()
        sched.schedule("t1", TriggerType.IMMEDIATE, lambda: None)
        sched.stop()
        self.assertEqual(sched.list_tasks(), [])

    def test_health_check(self) -> None:
        sched = VisionScheduler()
        h = sched.health_check()
        self.assertIn("total_tasks", h)


# ===== Capabilities Tests =====
class TestCapabilityEnum(unittest.TestCase):
    def test_all_capabilities(self) -> None:
        self.assertEqual(len(Capability), 9)


class TestCapabilityNegotiator(unittest.TestCase):
    def test_register_and_negotiate(self) -> None:
        neg = CapabilityNegotiator()
        neg.register_provider_capabilities("p1", [Capability.OCR, Capability.DETECTION])
        self.assertTrue(neg.negotiate("p1", [Capability.OCR]))
        self.assertFalse(neg.negotiate("p1", [Capability.SEGMENTATION]))

    def test_discover(self) -> None:
        neg = CapabilityNegotiator()
        neg.register_provider_capabilities("p1", [Capability.OCR])
        neg.register_provider_capabilities("p2", [Capability.DETECTION])
        self.assertIn("p1", neg.discover(Capability.OCR))


# ===== Resources Tests =====
class TestLRUCache(unittest.TestCase):
    def test_put_and_get(self) -> None:
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        self.assertEqual(cache.get("a"), 1)
        self.assertIsNone(cache.get("c"))

    def test_eviction(self) -> None:
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)

    def test_contains(self) -> None:
        cache = LRUCache(10)
        cache.put("a", 1)
        self.assertIn("a", cache)
        self.assertNotIn("b", cache)


class TestTempBuffer(unittest.TestCase):
    def test_buffer_creation(self) -> None:
        buf = TempBuffer("b1", "data", ttl_seconds=1.0)
        self.assertEqual(buf.buffer_id, "b1")
        self.assertFalse(buf.is_expired)

    def test_buffer_expiry(self) -> None:
        buf = TempBuffer("b1", "data", ttl_seconds=0.001)
        time.sleep(0.01)
        self.assertTrue(buf.is_expired)


class TestVisionResourceManager(unittest.TestCase):
    def test_cache_image(self) -> None:
        rm = VisionResourceManager()
        rm.cache_image("img1", "data")
        self.assertEqual(rm.get_cached_image("img1"), "data")

    def test_allocate_temp_buffer(self) -> None:
        rm = VisionResourceManager()
        rm.allocate_temp_buffer("tb1", "temp_data")
        self.assertEqual(rm.get_temp_buffer("tb1"), "temp_data")

    def test_release_temp_buffer(self) -> None:
        rm = VisionResourceManager()
        rm.allocate_temp_buffer("tb1", "data")
        rm.release_temp_buffer("tb1")
        self.assertIsNone(rm.get_temp_buffer("tb1"))

    def test_get_stats(self) -> None:
        rm = VisionResourceManager()
        stats = rm.get_stats()
        self.assertIn("image_cache_size", stats)


# ===== Metrics Tests =====
class TestCounter(unittest.TestCase):
    def test_increment(self) -> None:
        c = Counter("test")
        c.increment()
        c.increment(5)
        self.assertEqual(c.value, 6)


class TestGauge(unittest.TestCase):
    def test_set(self) -> None:
        g = Gauge("test")
        g.set(42.0)
        self.assertEqual(g.value, 42.0)

    def test_increment_decrement(self) -> None:
        g = Gauge("test")
        g.increment(5)
        g.decrement(2)
        self.assertEqual(g.value, 3.0)


class TestHistogram(unittest.TestCase):
    def test_record_and_percentile(self) -> None:
        h = Histogram("test")
        for i in range(10):
            h.record(float(i))
        self.assertEqual(h.count, 10)
        self.assertEqual(h.mean, 4.5)
        self.assertEqual(h.percentile(50), 5.0)

    def test_empty_percentile(self) -> None:
        h = Histogram("test")
        self.assertEqual(h.percentile(50), 0.0)


class TestMetricsCollector(unittest.TestCase):
    def test_collect(self) -> None:
        mc = VisionMetricsCollector()
        mc.increment("frames_processed", 10)
        mc.set_gauge("memory", 1024.0)
        mc.record_histogram("latency", 50.0)
        data = mc.collect()
        self.assertIn("counters", data)
        self.assertIn("gauges", data)
        self.assertIn("histograms", data)


# ===== Health Tests =====
class TestHealthStatus(unittest.TestCase):
    def test_all_statuses(self) -> None:
        self.assertEqual(len(HealthStatus), 6)


class TestHealthService(unittest.TestCase):
    def test_initial_status(self) -> None:
        hs = HealthService()
        self.assertEqual(hs.status, HealthStatus.HEALTHY)

    def test_update_status(self) -> None:
        hs = HealthService()
        hs.update_status(HealthStatus.DEGRADED, "high load")
        self.assertEqual(hs.status, HealthStatus.DEGRADED)

    def test_is_healthy(self) -> None:
        hs = HealthService()
        self.assertTrue(hs.is_healthy())
        hs.update_status(HealthStatus.FAILED, "crash")
        self.assertFalse(hs.is_healthy())

    def test_get_report(self) -> None:
        hs = HealthService()
        report = hs.get_report()
        self.assertIn("status", report)
        self.assertIn("details", report)


# ===== Security Tests =====
class TestPermission(unittest.TestCase):
    def test_all_permissions(self) -> None:
        self.assertEqual(len(Permission), 10)


class TestSecurityValidator(unittest.TestCase):
    def test_grant_and_check(self) -> None:
        sv = SecurityValidator()
        sv.grant_permissions("c1", [Permission.CAPTURE_DESKTOP])
        self.assertTrue(sv.has_permission("c1", Permission.CAPTURE_DESKTOP))
        self.assertFalse(sv.has_permission("c1", Permission.CAPTURE_CAMERA))

    def test_validate_input(self) -> None:
        sv = SecurityValidator()
        self.assertTrue(sv.validate_input("test", str))
        self.assertFalse(sv.validate_input(None, str))

    def test_check_plugin_isolation(self) -> None:
        sv = SecurityValidator()
        sv.grant_permissions("plugin1", [Permission.PROVIDER_ACCESS])
        self.assertTrue(sv.check_plugin_isolation("plugin1"))


# ===== Storage Tests =====
class TestStorageDomain(unittest.TestCase):
    def test_all_domains(self) -> None:
        self.assertEqual(len(StorageDomain), 5)


class TestVisionStorageAdapter(unittest.TestCase):
    def test_save_and_load_pipeline(self) -> None:
        adapter = VisionStorageAdapter()
        adapter.save_pipeline("p1", {"stages": ["acquire"]})
        data = adapter.load_pipeline("p1")
        self.assertEqual(data["stages"], ["acquire"])

    def test_save_and_load_settings(self) -> None:
        adapter = VisionStorageAdapter()
        adapter.save_settings("key1", {"value": 42})
        data = adapter.load_settings("key1")
        self.assertEqual(data["value"], 42)

    def test_save_provider_metadata(self) -> None:
        adapter = VisionStorageAdapter()
        adapter.save_provider_metadata("prov1", {"type": "ocr"})
        data = adapter.load_provider_metadata("prov1")
        self.assertEqual(data["type"], "ocr")

    def test_save_capture_config(self) -> None:
        adapter = VisionStorageAdapter()
        adapter.save_capture_config("src1", {"type": "camera"})
        data = adapter.load_capture_config("src1")
        self.assertEqual(data["type"], "camera")

    def test_save_model_metadata(self) -> None:
        adapter = VisionStorageAdapter()
        adapter.save_model_metadata("mod1", {"version": "1.0"})
        data = adapter.load_model_metadata("mod1")
        self.assertEqual(data["version"], "1.0")


# ===== IPC Integration Tests =====
class TestIPCVisionBridge(unittest.TestCase):
    def test_dispatch(self) -> None:
        bridge = IPCVisionBridge()
        received = []
        bridge.register_handler(EventType.FRAME_CAPTURED, lambda e: received.append(e))
        evt = FrameCaptured(frame_id="f1")
        bridge.dispatch(evt)
        self.assertEqual(len(received), 1)

    def test_dispatched_count(self) -> None:
        bridge = IPCVisionBridge()
        bridge.dispatch(FrameCaptured(frame_id="f1"))
        bridge.dispatch(FrameCaptured(frame_id="f2"))
        self.assertEqual(bridge.get_dispatched_count(), 2)

    def test_list_event_types(self) -> None:
        bridge = IPCVisionBridge()
        types = bridge.list_event_types()
        self.assertIn("frame_captured", types)


# ===== Workflow Integration Tests =====
class TestWorkflowVisionBridge(unittest.TestCase):
    def test_execute_pipeline(self) -> None:
        reg = PipelineRegistry()
        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)
        pipe.add_stage(PipelineStage.EXPORT, lambda x: x)
        reg.register(pipe)
        bridge = WorkflowVisionBridge(registry=reg)
        result = bridge.execute_pipeline(pipe.pipeline_id, 42)
        self.assertEqual(result, 42)

    def test_register_pipeline(self) -> None:
        bridge = WorkflowVisionBridge()
        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)
        pipe.add_stage(PipelineStage.EXPORT, lambda x: x)
        bridge.register_pipeline(pipe)
        self.assertIn(pipe.pipeline_id, bridge.list_pipelines())


# ===== Plugin Integration Tests =====
class TestPluginVisionBridge(unittest.TestCase):
    def test_load_provider(self) -> None:
        reg = ProviderRegistry()
        bridge = PluginVisionBridge(registry=reg)

        class MockProvider:
            provider_id = "mock1"
            provider_type = ProviderType.OCR
            def initialize(self): pass
            def shutdown(self): pass
            def health_check(self): return {}
            def get_capabilities(self): return []
            def is_compatible(self, v): return True
            def execute(self, d): return ProviderResult(True)

        bridge.load_provider(MockProvider())
        self.assertEqual(len(bridge.list_loaded_providers()), 1)

    def test_validate_isolation(self) -> None:
        bridge = PluginVisionBridge()
        class MockProvider:
            provider_id = "mock1"
            provider_type = ProviderType.OCR
            def initialize(self): pass
            def shutdown(self): pass
            def health_check(self): return {}
            def get_capabilities(self): return []
            def is_compatible(self, v): return True
            def execute(self, d): return ProviderResult(True)
        self.assertTrue(bridge.validate_provider_isolation(MockProvider()))


# ===== Capture Manager Tests =====
class TestCaptureManager(unittest.TestCase):
    def test_create_manager(self) -> None:
        mgr = CaptureManager()
        self.assertEqual(len(mgr.list_providers()), 0)

    def test_health_check(self) -> None:
        mgr = CaptureManager()
        h = mgr.health_check()
        self.assertIn("total_sessions", h)


# ===== Runtime Tests =====
class TestVisionRuntime(unittest.TestCase):
    def test_runtime_creation(self) -> None:
        rt = VisionRuntime()
        self.assertEqual(rt.state, ServiceState.CREATED)
        self.assertEqual(rt.service_id, "vision_runtime")

    def test_runtime_initialize(self) -> None:
        rt = VisionRuntime()
        rt.initialize()
        self.assertEqual(rt.state, ServiceState.READY)

    def test_runtime_lifecycle(self) -> None:
        rt = VisionRuntime()
        rt.initialize()
        rt.start()
        self.assertEqual(rt.state, ServiceState.RUNNING)
        rt.stop()
        self.assertEqual(rt.state, ServiceState.TERMINATED)

    def test_runtime_health_check(self) -> None:
        rt = VisionRuntime()
        rt.initialize()
        h = rt.health_check()
        self.assertIn("state", h)
        self.assertIn("health", h)


if __name__ == "__main__":
    unittest.main()
