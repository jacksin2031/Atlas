# Atlas Vision Runtime Integration Tests

"""
Integration tests for cross-module flows in the Vision Runtime.
"""
from __future__ import annotations

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from atlas_vision.services.runtime import VisionRuntime
from atlas_vision.services.manager import VisionManager
from atlas_vision.services.service import ServiceState
from atlas_vision.pipeline.pipeline import VisionPipeline, PipelineStage
from atlas_vision.registry.pipeline_registry import PipelineRegistry
from atlas_vision.registry.provider_registry import ProviderRegistry
from atlas_vision.registry.vision_registry import VisionRegistry
from atlas_vision.scheduler.scheduler import VisionScheduler, TriggerType
from atlas_vision.graph.graph import VisionGraph
from atlas_vision.graph.nodes import VisionNode
from atlas_vision.graph.edges import VisionEdge
from atlas_vision.graph.validator import VisionGraphValidator
from atlas_vision.graph.execution_plan import VisionExecutionPlan
from atlas_vision.capabilities.negotiation import Capability, CapabilityNegotiator
from atlas_vision.resources.manager import VisionResourceManager
from atlas_vision.metrics.collector import VisionMetricsCollector
from atlas_vision.health.service import HealthService, HealthStatus
from atlas_vision.security.permissions import SecurityValidator, Permission
from atlas_vision.storage.abstraction import VisionStorageAdapter, StorageDomain
from atlas_vision.integration.ipc import IPCVisionBridge
from atlas_vision.integration.workflow import WorkflowVisionBridge
from atlas_vision.integration.plugin import PluginVisionBridge
from atlas_vision.events import FrameCaptured, EventType
from atlas_vision.models.frame import Frame, FrameMetadata, FrameBuffer, FrameTimestamp, FrameResolution, FrameFormat, FrameColorSpace
from atlas_vision.capture.sources import CaptureDescriptor, CaptureSourceType
from atlas_vision.provider.base import ProviderType, ProviderResult, VisionProvider


class TestRuntimeLifecycle(unittest.TestCase):
    """Test full runtime lifecycle integration."""

    def test_full_lifecycle(self) -> None:
        rt = VisionRuntime()
        self.assertEqual(rt.state, ServiceState.CREATED)
        rt.initialize()
        self.assertEqual(rt.state, ServiceState.READY)
        rt.start()
        self.assertEqual(rt.state, ServiceState.RUNNING)
        rt.stop()
        self.assertEqual(rt.state, ServiceState.TERMINATED)

    def test_runtime_registers_core_services(self) -> None:
        rt = VisionRuntime()
        rt.initialize()
        self.assertIn("vision_runtime", rt.registry.list_services())

    def test_runtime_health_after_init(self) -> None:
        rt = VisionRuntime()
        rt.initialize()
        h = rt.health_check()
        self.assertEqual(h["state"], "ready")
        self.assertEqual(h["health"], "healthy")

    def test_runtime_metrics_after_init(self) -> None:
        rt = VisionRuntime()
        rt.initialize()
        m = rt.get_metrics()
        self.assertIn("counters", m)
        self.assertIn("gauges", m)
        self.assertIn("histograms", m)

    def test_runtime_session_creation(self) -> None:
        rt = VisionRuntime()
        rt.initialize()
        session = rt.create_session()
        self.assertIsNotNone(session)

    def test_runtime_context_creation(self) -> None:
        rt = VisionRuntime()
        rt.initialize()
        ctx = rt.get_context()
        self.assertIsNotNone(ctx)


class TestPipelineGraphIntegration(unittest.TestCase):
    """Test pipeline execution with graph-based scheduling."""

    def test_graph_with_pipeline(self) -> None:
        g = VisionGraph()
        g.add_node(VisionNode("n1", "acquire"))
        g.add_node(VisionNode("n2", "decode"))
        g.add_node(VisionNode("n3", "export"))
        g.add_edge(VisionEdge("n1", "n2"))
        g.add_edge(VisionEdge("n2", "n3"))
        plan = VisionExecutionPlan.compile(g)
        self.assertEqual(len(plan.node_order), 3)

    def test_validator_with_pipeline_graph(self) -> None:
        g = VisionGraph()
        g.add_node(VisionNode("n1", "acquire"))
        g.add_node(VisionNode("n2", "export"))
        g.add_edge(VisionEdge("n1", "n2"))
        self.assertTrue(VisionGraphValidator.validate(g))

    def test_pipeline_with_graph_execution(self) -> None:
        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)
        pipe.add_stage(PipelineStage.EXPORT, lambda x: x)
        g = VisionGraph()
        g.add_node(VisionNode("n1", "acquire"))
        g.add_node(VisionNode("n2", "export"))
        g.add_edge(VisionEdge("n1", "n2"))
        self.assertTrue(VisionGraphValidator.validate(g))
        result = pipe.execute(42)
        self.assertEqual(result, 42)


class TestProviderPluginIntegration(unittest.TestCase):
    """Test provider loading through plugin bridge."""

    def test_provider_through_plugin_bridge(self) -> None:
        reg = ProviderRegistry()
        bridge = PluginVisionBridge(registry=reg)

        class MockProvider:
            provider_id = "mp1"
            provider_type = ProviderType.OCR
            def initialize(self): pass
            def shutdown(self): pass
            def health_check(self): return {}
            def get_capabilities(self): return []
            def is_compatible(self, v): return True
            def execute(self, d): return ProviderResult(True)

        bridge.load_provider(MockProvider())
        self.assertEqual(len(bridge.list_loaded_providers()), 1)

    def test_workflow_through_bridge(self) -> None:
        reg = PipelineRegistry()
        bridge = WorkflowVisionBridge(registry=reg)
        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)
        pipe.add_stage(PipelineStage.EXPORT, lambda x: x)
        reg.register(pipe)
        result = bridge.execute_pipeline(pipe.pipeline_id, 100)
        self.assertEqual(result, 100)


class TestIPCEventIntegration(unittest.TestCase):
    """Test IPC event dispatching."""

    def test_ipc_with_events(self) -> None:
        bridge = IPCVisionBridge()
        received = []
        bridge.register_handler(EventType.FRAME_CAPTURED, lambda e: received.append(e))
        bridge.dispatch(FrameCaptured(frame_id="f1"))
        self.assertEqual(len(received), 1)

    def test_ipc_multiple_handlers(self) -> None:
        bridge = IPCVisionBridge()
        received1 = []
        received2 = []
        bridge.register_handler(EventType.FRAME_CAPTURED, lambda e: received1.append(e))
        bridge.register_handler(EventType.FRAME_CAPTURED, lambda e: received2.append(e))
        bridge.dispatch(FrameCaptured(frame_id="f1"))
        self.assertEqual(len(received1), 1)
        self.assertEqual(len(received2), 1)


class TestResourceManagementIntegration(unittest.TestCase):
    """Test resource management with caching and eviction."""

    def test_full_resource_flow(self) -> None:
        rm = VisionResourceManager()
        rm.cache_image("img1", "data1")
        self.assertEqual(rm.get_cached_image("img1"), "data1")
        rm.allocate_temp_buffer("tb1", "temp")
        self.assertEqual(rm.get_temp_buffer("tb1"), "temp")
        rm.release_temp_buffer("tb1")
        self.assertIsNone(rm.get_temp_buffer("tb1"))
        stats = rm.get_stats()
        self.assertIn("image_cache_size", stats)

    def test_lru_eviction_in_resource_manager(self) -> None:
        rm = VisionResourceManager(max_cache_size=2)
        rm.cache_image("a", 1)
        rm.cache_image("b", 2)
        rm.cache_image("c", 3)
        self.assertIsNone(rm.get_cached_image("a"))
        self.assertEqual(rm.get_cached_image("c"), 3)


class TestMetricsHealthIntegration(unittest.TestCase):
    """Test metrics and health service integration."""

    def test_metrics_collection(self) -> None:
        mc = VisionMetricsCollector()
        mc.increment("frames_processed", 10)
        mc.set_gauge("memory_mb", 256.0)
        mc.record_histogram("latency_ms", 5.0)
        mc.record_histogram("latency_ms", 10.0)
        data = mc.collect()
        self.assertEqual(data["counters"]["frames_processed"]["value"], 10)
        self.assertEqual(data["gauges"]["memory_mb"]["value"], 256.0)

    def test_health_service_lifecycle(self) -> None:
        hs = HealthService()
        self.assertEqual(hs.status, HealthStatus.HEALTHY)
        hs.update_status(HealthStatus.DEGRADED, "high load")
        self.assertEqual(hs.status, HealthStatus.DEGRADED)
        hs.update_status(HealthStatus.HEALTHY, "recovered")
        self.assertEqual(hs.status, HealthStatus.HEALTHY)


class TestSecurityStorageIntegration(unittest.TestCase):
    """Test security validation with storage."""

    def test_security_then_storage(self) -> None:
        sv = SecurityValidator()
        sv.grant_permissions("app1", [Permission.CAPTURE_DESKTOP])
        self.assertTrue(sv.has_permission("app1", Permission.CAPTURE_DESKTOP))

        adapter = VisionStorageAdapter()
        adapter.save_settings("config", {"capture_enabled": True})
        data = adapter.load_settings("config")
        self.assertTrue(data["capture_enabled"])

    def test_plugin_isolation(self) -> None:
        sv = SecurityValidator()
        sv.grant_permissions("plugin1", [Permission.PROVIDER_ACCESS])
        self.assertTrue(sv.check_plugin_isolation("plugin1"))
        sv.grant_permissions("plugin2", [Permission.CAPTURE_DESKTOP])
        self.assertFalse(sv.check_plugin_isolation("plugin2"))


class TestCapabilityNegotiationIntegration(unittest.TestCase):
    """Test capability negotiation with provider registry."""

    def test_negotiate_with_multiple_providers(self) -> None:
        neg = CapabilityNegotiator()
        neg.register_provider_capabilities("p1", [Capability.OCR, Capability.DETECTION])
        neg.register_provider_capabilities("p2", [Capability.CLASSIFICATION])
        self.assertTrue(neg.negotiate("p1", [Capability.OCR, Capability.DETECTION]))
        self.assertFalse(neg.negotiate("p1", [Capability.CLASSIFICATION]))
        self.assertIn("p2", neg.discover(Capability.CLASSIFICATION))


class TestSchedulerPipelineIntegration(unittest.TestCase):
    """Test scheduler with pipeline execution."""

    def test_scheduler_triggers_pipeline(self) -> None:
        sched = VisionScheduler()
        results = []
        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)
        pipe.add_stage(PipelineStage.EXPORT, lambda x: results.append(x))
        sched.schedule("t1", TriggerType.IMMEDIATE, lambda: pipe.execute(42))
        sched.execute("t1")
        self.assertEqual(results, [42])


class TestFullRuntimeIntegration(unittest.TestCase):
    """Full integration test exercising all subsystems."""

    def test_complete_vision_flow(self) -> None:
        rt = VisionRuntime()
        rt.initialize()
        rt.start()

        mgr = rt.manager
        reg = mgr.provider_registry
        sched = mgr.scheduler

        class MockProvider:
            provider_id = "test_prov"
            provider_type = ProviderType.OCR
            def initialize(self): pass
            def shutdown(self): pass
            def health_check(self): return True
            def get_capabilities(self): return ["ocr"]
            def is_compatible(self, v): return True
            def execute(self, d): return ProviderResult(True, data=d)

        mgr.register_provider(MockProvider())
        self.assertIn("test_prov", mgr.list_providers())

        pipe = VisionPipeline()
        pipe.add_stage(PipelineStage.ACQUIRE, lambda x: x)
        pipe.add_stage(PipelineStage.EXPORT, lambda x: x)
        mgr.pipeline_manager.register_pipeline(pipe)

        g = VisionGraph()
        g.add_node(VisionNode("n1", "acquire"))
        g.add_node(VisionNode("n2", "export"))
        g.add_edge(VisionEdge("n1", "n2"))
        self.assertTrue(VisionGraphValidator.validate(g))

        neg = CapabilityNegotiator()
        neg.register_provider_capabilities("test_prov", [Capability.OCR])
        self.assertTrue(neg.negotiate("test_prov", [Capability.OCR]))

        rm = VisionResourceManager()
        rm.cache_image("test", "data")
        self.assertEqual(rm.get_cached_image("test"), "data")

        mc = VisionMetricsCollector()
        mc.increment("test_metric", 1)
        data = mc.collect()
        self.assertIn("test_metric", data["counters"])

        hs = HealthService()
        hs.update_status(HealthStatus.HEALTHY, "ok")
        self.assertTrue(hs.is_healthy())

        sv = SecurityValidator()
        sv.grant_permissions("app1", [Permission.CAPTURE_DESKTOP])
        self.assertTrue(sv.has_permission("app1", Permission.CAPTURE_DESKTOP))

        adapter = VisionStorageAdapter()
        adapter.save_pipeline("test_pipe", {"id": "test"})
        self.assertIsNotNone(adapter.load_pipeline("test_pipe"))

        bridge = IPCVisionBridge()
        bridge.dispatch(FrameCaptured(frame_id="f1"))
        self.assertEqual(bridge.get_dispatched_count(), 1)

        rt.stop()
        self.assertEqual(rt.state, ServiceState.TERMINATED)


if __name__ == "__main__":
    unittest.main()
