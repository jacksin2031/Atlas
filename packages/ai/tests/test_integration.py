# Atlas AI Runtime Integration Tests

"""
Integration tests for the AI Runtime.
Tests cross-module interactions and full lifecycle flows.
"""
from __future__ import annotations

import sys, os, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from atlas_ai.services import AIRuntime, ServiceState
from atlas_ai.events import EventType
from atlas_ai.models import ModelCapability, ModelProvider, ModelVersion, ModelMetadata, ModelRequirements, ModelConfiguration
from atlas_ai.inference import InferenceRequest, InferenceJob, InferenceState, InferenceScheduler
from atlas_ai.prompts import PromptTemplate, PromptContext, PromptVariables, PromptRegistry
from atlas_ai.conversations import ConversationRegistry, ConversationRole, ConversationMessage
from atlas_ai.memory import MemoryStore, MemoryItem, MemoryScope
from atlas_ai.agents import Agent, AgentExecution, AgentRegistry
from atlas_ai.tools import ToolDescriptor, ToolRegistry, ToolResult, Tool
from atlas_ai.capabilities import CapabilityNegotiator, Capability, CapabilityStatus
from atlas_ai.resources.manager import AIResourceManager
from atlas_ai.metrics.collector import AIMetricsCollector
from atlas_ai.health.service import AIHealthService, HealthStatus
from atlas_ai.security.permissions import SecurityValidator, SecurityPolicy


class TestAIRuntimeIntegration(unittest.TestCase):
    """Test full lifecycle integration of AIRuntime."""

    def test_full_lifecycle(self) -> None:
        rt = AIRuntime()
        # Verify initial state
        self.assertEqual(rt.state, ServiceState.CREATED)
        self.assertEqual(rt.service_id, "ai_runtime")
        self.assertEqual(rt.service_name, "AI Runtime")

        # Initialize
        rt.initialize()
        self.assertEqual(rt.state, ServiceState.READY)
        self.assertEqual(rt.health_service.status, HealthStatus.HEALTHY)

        # Start
        rt.start()
        self.assertEqual(rt.state, ServiceState.RUNNING)

        # Health check
        h = rt.health_check()
        self.assertIn("state", h)
        self.assertIn("health", h)
        self.assertIn("uptime_seconds", h)

        # Metrics
        m = rt.get_metrics()
        self.assertIn("counters", m)
        self.assertIn("gauges", m)
        self.assertIn("histograms", m)

        # Shutdown
        rt.stop()
        self.assertEqual(rt.state, ServiceState.TERMINATED)

    def test_runtime_services_accessible(self) -> None:
        rt = AIRuntime()
        rt.initialize()
        # Verify all services are accessible
        self.assertIsNotNone(rt.registry)
        self.assertIsNotNone(rt.health_service)
        self.assertIsNotNone(rt.metrics)
        self.assertIsNotNone(rt.manager)
        self.assertIsNotNone(rt.get_context())
        session = rt.create_session(model_id="m1", temperature=0.5)
        self.assertIsNotNone(session)
        self.assertEqual(session.context.model_id, "m1")

    def test_runtime_idempotent_stop(self) -> None:
        rt = AIRuntime()
        rt.initialize()
        rt.start()
        rt.stop()
        self.assertEqual(rt.state, ServiceState.TERMINATED)
        # Second stop should not raise
        rt.stop()
        self.assertEqual(rt.state, ServiceState.TERMINATED)


class TestCrossModuleIntegration(unittest.TestCase):
    """Test interactions between AI Runtime modules."""

    def test_runtime_with_prompts_and_conversations(self) -> None:
        rt = AIRuntime()
        rt.initialize()
        registry = rt.registry

        # Register a prompt template
        from atlas_ai.prompts import PromptRegistry as PR
        prompt_reg = PR()
        tmpl = PromptTemplate(
            template_id="greeting", name="Greeting",
            template_text="Hello, {name}!", variables=["name"],
        )
        prompt_reg.register(tmpl)

        # Compile a prompt
        ctx = PromptContext(
            conversation_id="c1",
            variables=PromptVariables({"name": "Alice"}),
        )
        prompt = prompt_reg.compile("greeting", ctx)
        self.assertEqual(prompt.text, "Hello, Alice!")

        # Create a conversation
        conv_reg = ConversationRegistry()
        conv = conv_reg.create_conversation(title="Test", model_id="m1")
        msg = ConversationMessage(
            message_id="msg1", role=ConversationRole.USER, content=prompt.text,
        )
        conv.add_message(msg)
        self.assertEqual(conv.history.count, 1)
        self.assertEqual(conv.state.value, "active")

    def test_runtime_with_agents_and_tools(self) -> None:
        # Create agent
        agent = Agent(agent_id="a1", name="Test Agent")
        agent_reg = AgentRegistry()
        agent_reg.register(agent)

        # Create tool
        desc = ToolDescriptor(tool_id="calc", name="Calculator", description="Calculate")
        def handler(args):
            return ToolResult(tool_id="calc", success=True, output=42)
        tool_reg = ToolRegistry()
        tool_reg.register(Tool(desc, handler))

        # Execute agent with tool
        exec_ = agent_reg.create_execution("a1", "ex1")
        exec_.start()
        result = tool_reg.invoke("calc", {"op": "add", "a": 20, "b": 22})
        self.assertTrue(result.success)
        exec_.record_tool_invocation("calc", result)
        exec_.complete({"result": result.output})
        self.assertEqual(exec_.state.value, "completed")

    def test_runtime_with_memory_and_embeddings(self) -> None:
        from atlas_ai.memory import MemoryStore, MemoryItem, MemoryScope
        from atlas_ai.embeddings import EmbeddingStore, EmbeddingIndex

        # Store memory
        store = MemoryStore()
        store.store(MemoryItem(memory_id="mem1", content="test", scope=MemoryScope.WORKSPACE))
        self.assertEqual(store.count(), 1)

        # Store embedding
        emb_store = EmbeddingStore()
        emb_store.add(EmbeddingIndex(
            entry_id="e1", embedding_id="emb1", text="hello",
            vector=[0.1, 0.2, 0.3],
        ))
        self.assertEqual(emb_store.count(), 1)

    def test_runtime_with_resources_and_metrics(self) -> None:
        rm = AIResourceManager()
        mc = AIMetricsCollector()
        mc.initialize()

        rm.allocate_model_memory("m1", 2048)
        mc.increment_counter("inference_total", 1)
        mc.observe_histogram("model_load_time_ms", 100.0)

        self.assertEqual(rm.get_model_memory("m1"), 2048)
        collected = mc.collect()
        self.assertEqual(collected["counters"]["inference_total"]["value"], 1)

    def test_runtime_with_security(self) -> None:
        validator = SecurityValidator(SecurityPolicy(max_input_length=100))
        self.assertTrue(validator.validate_input("short prompt"))
        self.assertFalse(validator.validate_input("x" * 200))

    def test_runtime_with_capability_negotiation(self) -> None:
        neg = CapabilityNegotiator()
        cap = Capability(
            capability_id="chat", name="Chat",
            status=CapabilityStatus.AVAILABLE,
        )
        neg.register(cap)
        self.assertTrue(neg.check_availability("chat"))

    def test_inference_scheduler_with_model(self) -> None:
        sched = InferenceScheduler()
        req = InferenceRequest(prompt="test", model_id="m1")
        job = InferenceJob(request=req)
        sched.schedule(job)
        self.assertEqual(sched.queue_depth, 1)
        next_job = sched.next_job()
        self.assertIsNotNone(next_job)
        self.assertEqual(sched.queue_depth, 0)


class TestRuntimeManagerIntegration(unittest.TestCase):
    """Test AIRuntimeManager with multiple runtimes."""

    def test_multi_runtime_management(self) -> None:
        from atlas_ai.services import AIRuntimeManager
        mgr = AIRuntimeManager()

        rt1 = AIRuntime()
        rt1.initialize()
        rt1.start()

        rt2 = AIRuntime()
        rt2.initialize()
        rt2.start()

        mgr.register(rt1, default=True)
        mgr.register(rt2)

        self.assertEqual(len(mgr.list_runtimes()), 2)
        self.assertIsNotNone(mgr.get_default())

        hc = mgr.health_check()
        self.assertIn(list(hc.keys())[0], hc)

        mgr.shutdown_all()
        self.assertEqual(rt1.state, ServiceState.TERMINATED)
        self.assertEqual(rt2.state, ServiceState.TERMINATED)


if __name__ == "__main__":
    unittest.main()
