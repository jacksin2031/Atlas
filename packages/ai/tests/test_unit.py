# Atlas AI Runtime Unit Tests
"""Comprehensive unit tests for all AI Runtime modules."""
from __future__ import annotations

import sys, os, unittest, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from atlas_ai.errors import (
    AIError, ModelError, ModelNotFoundError, ModelLoadError,
    ModelSnapshotError, ProviderError, ProviderNotFoundError,
    ProviderLoadError, ProviderHealthError, InferenceError,
    InferenceQueueError, InferenceExecutionError, InferenceTimeoutError,
    PromptError, PromptCompileError, PromptValidationError,
    ConversationError, ConversationNotFoundError, MemoryError,
    MemoryStoreError, EmbeddingError, EmbeddingIndexError,
    AgentError, AgentExecutionError, ToolError, ToolInvocationError,
    ToolPermissionError, RegistryError, DuplicateRegistrationError,
    ResourceError, ResourceExhaustedError, SecurityError,
    PermissionDeniedError, CapabilityError, CapabilityUnavailableError,
    SchedulingError, StorageError, HealthError, MetricsError,
)
from atlas_ai.events import (
    Event, EventType, ModelLoaded, ModelUnloaded,
    ModelSnapshotCreated, InferenceStarted, InferenceCompleted,
    InferenceFailed, InferenceScheduled, InferenceCancelled,
    PromptExecuted, PromptCompileFailed, ConversationCreated,
    ConversationClosed, MemoryStored, MemoryRemoved,
    EmbeddingGenerated, EmbeddingIndexChanged, AgentStarted,
    AgentStopped, AgentExecuted, ToolInvoked, ToolFailed,
    HealthChanged, ProviderLoaded, ProviderUnloaded,
    ProviderHealthChanged, CapabilityDiscovered,
)
from atlas_ai.models import (
    ModelCapability, ModelState, ModelProvider, ModelVersion,
    ModelMetadata, ModelRequirements, ModelResourceUsage,
    ModelConfiguration, ModelSnapshot, ModelDescriptor, ModelInstance,
)
from atlas_ai.providers import (
    ProviderCapability, ProviderHealth, ProviderDescriptor,
    ProviderSession, ProviderFactory, AIProvider, ProviderRegistry,
)
from atlas_ai.capabilities import (
    AIModelCapability, CapabilityStatus, Capability,
    CapabilityNegotiator,
)
from atlas_ai.inference import (
    InferenceState, InferenceMode, InferenceMetadata,
    InferenceRequest, InferenceResult, InferenceResponse,
    InferenceContext, InferenceJob, InferenceQueue,
    InferenceScheduler, InferenceExecutor,
)
from atlas_ai.prompts import (
    PromptVariables, PromptContext, PromptTemplate, Prompt,
    PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot,
    PromptRegistry,
)
from atlas_ai.conversations import (
    ConversationRole, ConversationState, ConversationMessage,
    ConversationHistory, Conversation, ConversationSession,
    ConversationRegistry,
)
from atlas_ai.memory import (
    MemoryScope, MemoryItem, MemoryContext, MemorySnapshot,
    MemoryQuery, MemoryPolicy, MemoryStore, MemoryRegistry,
)
from atlas_ai.embeddings import (
    EmbeddingModel, EmbeddingRequest, EmbeddingResponse,
    EmbeddingIndex, EmbeddingStore, EmbeddingRegistry,
    EmbeddingProvider,
)
from atlas_ai.agents import (
    AgentState, AgentCapability, AgentPolicy, AgentContext,
    Agent, AgentExecution, AgentRegistry, AgentScheduler,
)
from atlas_ai.tools import (
    ToolCapability, ToolPermission, ToolDescriptor, ToolResult,
    ToolInvocation, Tool, ToolRegistry,
)
from atlas_ai.scheduler import TriggerType, ScheduleEntry, AIScheduler
from atlas_ai.services import (
    AIService, ServiceState, AIContext, AISession,
    AIManager, AIRuntime, AIRuntimeManager,
)
from atlas_ai.integration.bridges import (
    IPCAIBridge, WorkflowAIBridge, VisionAIBridge,
)
from atlas_ai.resources.manager import (
    AIResourceManager, LRUCache, TempBuffer,
)
from atlas_ai.metrics.collector import (
    AIMetricsCollector, Counter, Gauge, Histogram,
)
from atlas_ai.health.service import AIHealthService, HealthStatus
from atlas_ai.security.permissions import (
    SecurityValidator, SecurityPolicy, Permission,
)
from atlas_ai.storage.abstraction import (
    AIStorageAdapter, StorageDomain, StorageBackend,
)
from atlas_ai.registry.ai_registry import AIRegistry


# ===== Error Tests =====
class TestAIError(unittest.TestCase):
    def test_base_error_creation(self) -> None:
        err = AIError('test message', code='TEST', details={'key': 'val'})
        self.assertEqual(err.error_code, 'TEST')
        self.assertEqual(err.error_message, 'test message')
        self.assertEqual(err.error_details, {'key': 'val'})

    def test_error_to_dict(self) -> None:
        err = AIError('test')
        d = err.to_dict()
        self.assertIn('error_code', d)
        self.assertIn('error_message', d)
        self.assertIn('error_details', d)

    def test_error_inheritance(self) -> None:
        self.assertTrue(issubclass(ModelError, AIError))
        self.assertTrue(issubclass(ProviderError, AIError))
        self.assertTrue(issubclass(InferenceError, AIError))
        self.assertTrue(issubclass(PromptError, AIError))
        self.assertTrue(issubclass(ConversationError, AIError))
        self.assertTrue(issubclass(MemoryError, AIError))
        self.assertTrue(issubclass(EmbeddingError, AIError))
        self.assertTrue(issubclass(AgentError, AIError))
        self.assertTrue(issubclass(ToolError, AIError))
        self.assertTrue(issubclass(RegistryError, AIError))
        self.assertTrue(issubclass(ResourceError, AIError))
        self.assertTrue(issubclass(SecurityError, AIError))
        self.assertTrue(issubclass(CapabilityError, AIError))
        self.assertTrue(issubclass(SchedulingError, AIError))
        self.assertTrue(issubclass(StorageError, AIError))
        self.assertTrue(issubclass(HealthError, AIError))
        self.assertTrue(issubclass(MetricsError, AIError))


# ===== Event Tests =====
class TestAIEvents(unittest.TestCase):
    def test_event_creation(self) -> None:
        evt = Event(event_type=EventType.MODEL_LOADED, source='test')
        self.assertEqual(evt.event_type, EventType.MODEL_LOADED)
        self.assertEqual(evt.source, 'test')
        d = evt.to_dict()
        self.assertIn('event_id', d)
        self.assertIn('event_type', d)
        self.assertIn('timestamp', d)

    def test_model_loaded_event(self) -> None:
        evt = ModelLoaded(model_id='m1', provider_id='p1', version='1.0')
        self.assertEqual(evt.model_id, 'm1')
        self.assertEqual(evt.event_type, EventType.MODEL_LOADED)

    def test_inference_events(self) -> None:
        started = InferenceStarted(job_id='j1', model_id='m1')
        self.assertEqual(started.job_id, 'j1')
        completed = InferenceCompleted(job_id='j1', duration_ms=100.0, tokens_generated=50)
        self.assertEqual(completed.duration_ms, 100.0)
        failed = InferenceFailed(job_id='j1', error_code='ERR_TIMEOUT')
        self.assertEqual(failed.error_code, 'ERR_TIMEOUT')

    def test_health_changed_event(self) -> None:
        evt = HealthChanged(previous_status='healthy', new_status='degraded')
        self.assertEqual(evt.previous_status, 'healthy')
        self.assertEqual(evt.new_status, 'degraded')


# ===== Model Tests =====
class TestModelManagement(unittest.TestCase):
    def test_model_version(self) -> None:
        v = ModelVersion('1.0.0', build_number=42)
        self.assertEqual(v.version, '1.0.0')
        self.assertEqual(v.build_number, 42)

    def test_model_version_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            ModelVersion('')

    def test_model_metadata(self) -> None:
        m = ModelMetadata(creator='test', license='MIT', tags=['nlp'])
        self.assertEqual(m.creator, 'test')

    def test_model_requirements(self) -> None:
        r = ModelRequirements(min_gpu_memory_mb=4096, requires_cuda=True)
        self.assertEqual(r.min_gpu_memory_mb, 4096)
        self.assertTrue(r.requires_cuda)

    def test_model_configuration(self) -> None:
        c = ModelConfiguration(temperature=0.5, max_tokens=1024, stream=True)
        self.assertEqual(c.temperature, 0.5)
        self.assertTrue(c.stream)

    def test_model_configuration_clone(self) -> None:
        c = ModelConfiguration(temperature=0.7)
        c2 = c.clone_with(temperature=0.9, max_tokens=2048)
        self.assertEqual(c2.temperature, 0.9)
        self.assertEqual(c2.max_tokens, 2048)
        self.assertNotEqual(c.temperature, c2.temperature)

    def test_model_resource_usage(self) -> None:
        u = ModelResourceUsage(gpu_memory_mb=2048.0, cpu_percent=45.0)
        self.assertEqual(u.gpu_memory_mb, 2048.0)

    def test_model_descriptor(self) -> None:
        desc = ModelDescriptor(
            model_id='test-model', name='Test Model',
            provider=ModelProvider.CUSTOM,
            version=ModelVersion('1.0.0'),
            capabilities=frozenset([ModelCapability.CHAT, ModelCapability.COMPLETION]),
            metadata=ModelMetadata(creator='test'),
            requirements=ModelRequirements(),
            configuration=ModelConfiguration(),
        )
        self.assertTrue(desc.supports(ModelCapability.CHAT))
        self.assertFalse(desc.supports(ModelCapability.AUDIO))
        d = desc.to_dict()
        self.assertEqual(d['model_id'], 'test-model')

    def test_model_instance(self) -> None:
        desc = ModelDescriptor(
            model_id='m1', name='M1', provider=ModelProvider.CUSTOM,
            version=ModelVersion('1.0.0'),
            capabilities=frozenset(), metadata=ModelMetadata(),
            requirements=ModelRequirements(), configuration=ModelConfiguration(),
        )
        inst = ModelInstance(descriptor=desc)
        self.assertEqual(inst.instance_id, 'm1')
        self.assertEqual(inst.state, ModelState.CREATED)

    def test_model_snapshot(self) -> None:
        snap = ModelSnapshot(
            snapshot_id='s1', model_id='m1',
            state=ModelState.READY,
            configuration=ModelConfiguration(),
            resource_usage=ModelResourceUsage(),
        )
        self.assertEqual(snap.snapshot_id, 's1')


# ===== Provider Tests =====
class TestProviders(unittest.TestCase):
    def test_provider_descriptor(self) -> None:
        desc = ProviderDescriptor(
            provider_id='p1', name='Test', provider_type='custom',
            version='1.0',
            capabilities=frozenset([ProviderCapability.INFERENCE]),
        )
        self.assertTrue(desc.supports(ProviderCapability.INFERENCE))

    def test_provider_session(self) -> None:
        sess = ProviderSession(session_id='s1', provider_id='p1')
        self.assertTrue(sess.is_active)
        sess.touch()
        sess.close()
        self.assertFalse(sess.is_active)

    def test_provider_registry(self) -> None:
        reg = ProviderRegistry()
        self.assertEqual(reg.list_providers(), [])
        self.assertIsNone(reg.get('nonexistent'))


# ===== Capability Tests =====
class TestCapabilities(unittest.TestCase):
    def test_capability_negotiator(self) -> None:
        neg = CapabilityNegotiator()
        cap = Capability(capability_id='chat', name='Chat', status=CapabilityStatus.AVAILABLE)
        neg.register(cap)
        self.assertTrue(neg.check_availability('chat'))
        self.assertFalse(neg.check_availability('nonexistent'))
        self.assertEqual(neg.list_capabilities(), ['chat'])

    def test_capability_unavailable(self) -> None:
        neg = CapabilityNegotiator()
        cap = Capability(capability_id='vision', name='Vision', status=CapabilityStatus.UNAVAILABLE)
        neg.register(cap)
        self.assertFalse(neg.check_availability('vision'))


# ===== Inference Tests =====
class TestInference(unittest.TestCase):
    def test_inference_request(self) -> None:
        req = InferenceRequest(prompt='hello', model_id='m1')
        self.assertIsNotNone(req.request_id)
        d = req.to_dict()
        self.assertEqual(d['model_id'], 'm1')

    def test_inference_result(self) -> None:
        res = InferenceResult(request_id='r1', text='world', token_count=5, model_id='m1', duration_ms=100.0)
        self.assertEqual(res.text, 'world')

    def test_inference_metadata(self) -> None:
        meta = InferenceMetadata(model_id='m1', priority=5, timeout_ms=30000)
        self.assertEqual(meta.priority, 5)

    def test_inference_queue(self) -> None:
        q = InferenceQueue(max_size=2)
        req1 = InferenceRequest(prompt='a', model_id='m1')
        req2 = InferenceRequest(prompt='b', model_id='m1')
        job1 = InferenceJob(request=req1)
        job2 = InferenceJob(request=req2)
        self.assertTrue(q.enqueue(job1))
        self.assertTrue(q.enqueue(job2))
        self.assertEqual(q.size, 2)
        dequeued = q.dequeue()
        self.assertIsNotNone(dequeued)
        self.assertEqual(dequeued.job_id, job1.job_id)
        self.assertEqual(q.size, 1)

    def test_inference_queue_full(self) -> None:
        q = InferenceQueue(max_size=1)
        q.enqueue(InferenceJob(request=InferenceRequest(prompt='a', model_id='m1')))
        self.assertTrue(q.is_full)
        self.assertFalse(q.enqueue(InferenceJob(request=InferenceRequest(prompt='b', model_id='m1'))))

    def test_inference_scheduler(self) -> None:
        sched = InferenceScheduler()
        req = InferenceRequest(prompt='test', model_id='m1')
        job = InferenceJob(request=req)
        self.assertTrue(sched.schedule(job))
        self.assertEqual(sched.queue_depth, 1)
        next_job = sched.next_job()
        self.assertIsNotNone(next_job)
        self.assertEqual(sched.queue_depth, 0)

    def test_inference_executor(self) -> None:
        exec_ = InferenceExecutor()
        req = InferenceRequest(prompt='test', model_id='m1')
        job = InferenceJob(request=req)
        job.state = InferenceState.SCHEDULED
        with self.assertRaises(InferenceExecutionError):
            exec_.execute(job, None)


# ===== Prompt Tests =====
class TestPrompts(unittest.TestCase):
    def test_prompt_variables(self) -> None:
        vars_ = PromptVariables().set('name', 'Alice').set('city', 'Tokyo')
        self.assertEqual(vars_.get('name'), 'Alice')
        self.assertEqual(vars_.get('missing', 'default'), 'default')

    def test_prompt_context(self) -> None:
        ctx = PromptContext(conversation_id='c1', model_id='m1')
        ctx2 = ctx.clone_with(model_id='m2')
        self.assertEqual(ctx2.model_id, 'm2')
        self.assertEqual(ctx.conversation_id, ctx2.conversation_id)

    def test_prompt_template(self) -> None:
        tmpl = PromptTemplate(template_id='t1', name='Greeting', template_text='Hello, {name}!', variables=['name'])
        self.assertEqual(tmpl.template_id, 't1')

    def test_prompt_compiler(self) -> None:
        tmpl = PromptTemplate(template_id='t1', name='Test', template_text='Hello, {name}!', variables=['name'])
        ctx = PromptContext(variables=PromptVariables({'name': 'Alice'}))
        prompt = PromptCompiler.compile(tmpl, ctx)
        self.assertEqual(prompt.text, 'Hello, Alice!')

    def test_prompt_compiler_missing_var(self) -> None:
        tmpl = PromptTemplate(template_id='t1', name='Test', template_text='Hello, {name}!', variables=['name'])
        ctx = PromptContext(variables=PromptVariables({}))
        with self.assertRaises(PromptCompileError):
            PromptCompiler.compile(tmpl, ctx)

    def test_prompt_executor(self) -> None:
        exec_ = PromptExecutor()
        prompt = Prompt(prompt_id='p1', text='Hello!')
        result = exec_.execute(prompt)
        self.assertEqual(result['prompt_id'], 'p1')

    def test_prompt_registry(self) -> None:
        reg = PromptRegistry()
        tmpl = PromptTemplate(template_id='t1', name='Test', template_text='Hi', variables=[])
        reg.register(tmpl)
        self.assertEqual(reg.list_templates(), ['t1'])
        compiled = reg.compile('t1', PromptContext(variables=PromptVariables({})))
        self.assertEqual(compiled.text, 'Hi')


# ===== Conversation Tests =====
class TestConversations(unittest.TestCase):
    def test_conversation_message(self) -> None:
        msg = ConversationMessage(message_id='m1', role=ConversationRole.USER, content='Hello')
        self.assertEqual(msg.role, ConversationRole.USER)

    def test_conversation_history(self) -> None:
        hist = ConversationHistory()
        self.assertEqual(hist.count, 0)
        msg = ConversationMessage(message_id='m1', role=ConversationRole.USER, content='Hi')
        hist2 = hist.append(msg)
        self.assertEqual(hist2.count, 1)
        self.assertEqual(hist2.last_message.message_id, 'm1')

    def test_conversation(self) -> None:
        conv = Conversation(conversation_id='c1', title='Test')
        self.assertEqual(conv.state, ConversationState.CREATED)
        msg = ConversationMessage(message_id='m1', role=ConversationRole.USER, content='Hi')
        conv.add_message(msg)
        self.assertEqual(conv.state, ConversationState.ACTIVE)
        self.assertEqual(conv.history.count, 1)
        conv.close()
        self.assertEqual(conv.state, ConversationState.CLOSED)

    def test_conversation_registry(self) -> None:
        reg = ConversationRegistry()
        conv = reg.create_conversation(title='Test', model_id='m1')
        self.assertIsNotNone(conv)
        self.assertIn(conv.conversation_id, reg.list_conversations())
        self.assertTrue(reg.close(conv.conversation_id))


# ===== Memory Tests =====
class TestMemory(unittest.TestCase):
    def test_memory_item(self) -> None:
        item = MemoryItem(memory_id='mem1', content='test', scope=MemoryScope.SESSION)
        self.assertFalse(item.is_expired())

    def test_memory_item_expiry(self) -> None:
        item = MemoryItem(memory_id='mem1', content='test', scope=MemoryScope.SESSION, ttl_seconds=0)
        time.sleep(0.01)
        self.assertTrue(item.is_expired())

    def test_memory_policy(self) -> None:
        policy = MemoryPolicy()
        self.assertEqual(policy.max_items_per_scope[MemoryScope.SESSION], 1000)
        self.assertTrue(policy.auto_cleanup)

    def test_memory_store(self) -> None:
        store = MemoryStore()
        item = MemoryItem(memory_id='mem1', content='test data')
        store.store(item)
        retrieved = store.retrieve('mem1')
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.content, 'test data')
        self.assertEqual(store.count(), 1)

    def test_memory_store_remove(self) -> None:
        store = MemoryStore()
        store.store(MemoryItem(memory_id='mem1', content='test'))
        self.assertTrue(store.remove('mem1'))
        self.assertIsNone(store.retrieve('mem1'))

    def test_memory_query(self) -> None:
        store = MemoryStore()
        store.store(MemoryItem(memory_id='m1', content='a', scope=MemoryScope.WORKSPACE, metadata={'project': 'p1'}))
        store.store(MemoryItem(memory_id='m2', content='b', scope=MemoryScope.GLOBAL, metadata={'project': 'p2'}))
        query = MemoryQuery(scope=MemoryScope.WORKSPACE, metadata_filter={'project': 'p1'})
        results = store.query(query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].memory_id, 'm1')

    def test_memory_snapshot(self) -> None:
        store = MemoryStore()
        store.store(MemoryItem(memory_id='m1', content='test'))
        snap = store.snapshot('snap1')
        self.assertEqual(snap.snapshot_id, 'snap1')
        self.assertIn('m1', snap.items)


# ===== Embedding Tests =====
class TestEmbeddings(unittest.TestCase):
    def test_embedding_model(self) -> None:
        model = EmbeddingModel(model_id='emb1', name='Test Embedding', dimension=768)
        self.assertEqual(model.dimension, 768)

    def test_embedding_store(self) -> None:
        store = EmbeddingStore()
        entry = EmbeddingIndex(entry_id='e1', embedding_id='emb1', text='hello', vector=[0.1, 0.2, 0.3])
        store.add(entry)
        self.assertEqual(store.count(), 1)
        retrieved = store.get('e1')
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.text, 'hello')

    def test_embedding_registry(self) -> None:
        reg = EmbeddingRegistry()
        reg.register_model(EmbeddingModel(model_id='m1', name='Test'))
        self.assertIn('m1', reg.list_models())


# ===== Agent Tests =====
class TestAgents(unittest.TestCase):
    def test_agent_policy(self) -> None:
        policy = AgentPolicy(max_steps=50, timeout_seconds=120)
        d = policy.to_dict()
        self.assertEqual(d['max_steps'], 50)

    def test_agent(self) -> None:
        agent = Agent(agent_id='a1', name='Test Agent')
        self.assertEqual(agent.state, AgentState.CREATED)

    def test_agent_execution(self) -> None:
        ex = AgentExecution(execution_id='ex1', agent_id='a1')
        ex.start()
        self.assertEqual(ex.state, AgentState.EXECUTING)
        ex.complete({'result': 'done'})
        self.assertEqual(ex.state, AgentState.COMPLETED)

    def test_agent_registry(self) -> None:
        reg = AgentRegistry()
        agent = Agent(agent_id='a1', name='Test')
        reg.register(agent)
        self.assertIn('a1', reg.list_agents())
        ex = reg.create_execution('a1', 'ex1')
        self.assertEqual(ex.agent_id, 'a1')

    def test_agent_scheduler(self) -> None:
        sched = AgentScheduler()
        ex = AgentExecution(execution_id='ex1', agent_id='a1')
        sched.schedule(ex)
        self.assertEqual(sched.queue_depth, 1)
        next_ex = sched.next_execution()
        self.assertIsNotNone(next_ex)
        self.assertEqual(sched.queue_depth, 0)


# ===== Tool Tests =====
class TestTools(unittest.TestCase):
    def test_tool_descriptor(self) -> None:
        desc = ToolDescriptor(tool_id='t1', name='Test Tool', description='A test tool')
        self.assertEqual(desc.tool_id, 't1')

    def test_tool_result(self) -> None:
        res = ToolResult(tool_id='t1', success=True, output='result')
        self.assertTrue(res.success)

    def test_tool_registry(self) -> None:
        reg = ToolRegistry()
        desc = ToolDescriptor(tool_id='t1', name='Test', description='Desc')
        def handler(args):
            return ToolResult(tool_id='t1', success=True, output='ok')
        tool = Tool(desc, handler)
        reg.register(tool)
        self.assertIn('t1', reg.list_tools())
        result = reg.invoke('t1', {})
        self.assertTrue(result.success)
        self.assertEqual(result.output, 'ok')

    def test_tool_not_found(self) -> None:
        reg = ToolRegistry()
        with self.assertRaises(ToolInvocationError):
            reg.invoke('nonexistent', {})


# ===== Scheduler Tests =====
class TestScheduler(unittest.TestCase):
    def test_schedule_entry(self) -> None:
        entry = ScheduleEntry(entry_id='e1', trigger_type=TriggerType.IMMEDIATE)
        self.assertEqual(entry.trigger_type, TriggerType.IMMEDIATE)

    def test_ai_scheduler(self) -> None:
        sched = AIScheduler()
        entry = ScheduleEntry(entry_id='e1', trigger_type=TriggerType.IMMEDIATE)
        called = []
        sched.schedule(entry, callback=lambda: called.append(1))
        self.assertIn('e1', sched.list_entries())
        executed = sched.execute_pending()
        self.assertIn('e1', executed)
        self.assertEqual(len(called), 1)

    def test_scheduler_disable(self) -> None:
        sched = AIScheduler()
        entry = ScheduleEntry(entry_id='e1', trigger_type=TriggerType.IMMEDIATE)
        sched.schedule(entry)
        self.assertTrue(sched.disable('e1'))
        self.assertFalse(sched.enable('nonexistent'))


# ===== Service Tests =====
class TestServices(unittest.TestCase):
    def test_ai_context(self) -> None:
        ctx = AIContext(model_id='m1', temperature=0.5, max_tokens=512)
        self.assertEqual(ctx.model_id, 'm1')
        self.assertEqual(ctx.temperature, 0.5)

    def test_ai_context_clone(self) -> None:
        ctx = AIContext(model_id='m1', temperature=0.5)
        ctx2 = ctx.clone_with(temperature=0.9)
        self.assertEqual(ctx2.temperature, 0.9)
        self.assertNotEqual(ctx.temperature, ctx2.temperature)

    def test_ai_session(self) -> None:
        ctx = AIContext(model_id='m1')
        session = AISession(session_id='s1', context=ctx, runtime=None)
        self.assertEqual(session.session_id, 's1')
        self.assertTrue(session.is_active)
        session.close()
        self.assertFalse(session.is_active)

    def test_airuntime_lifecycle(self) -> None:
        rt = AIRuntime()
        self.assertEqual(rt.state, ServiceState.CREATED)
        self.assertEqual(rt.service_id, 'ai_runtime')
        rt.initialize()
        self.assertEqual(rt.state, ServiceState.READY)
        rt.start()
        self.assertEqual(rt.state, ServiceState.RUNNING)
        rt.stop()
        self.assertEqual(rt.state, ServiceState.TERMINATED)

    def test_airuntime_health(self) -> None:
        rt = AIRuntime()
        rt.initialize()
        h = rt.health_check()
        self.assertIn('state', h)
        self.assertIn('health', h)

    def test_airuntime_metrics(self) -> None:
        rt = AIRuntime()
        rt.initialize()
        m = rt.get_metrics()
        self.assertIn('counters', m)
        self.assertIn('gauges', m)
        self.assertIn('histograms', m)

    def test_airuntime_create_session(self) -> None:
        rt = AIRuntime()
        rt.initialize()
        session = rt.create_session(model_id='m1', temperature=0.3)
        self.assertIsNotNone(session)
        self.assertEqual(session.context.model_id, 'm1')

    def test_airuntime_get_context(self) -> None:
        rt = AIRuntime()
        rt.initialize()
        ctx = rt.get_context()
        self.assertIsNotNone(ctx)


# ===== Runtime Manager Tests =====
class TestRuntimeManager(unittest.TestCase):
    def test_register_runtime(self) -> None:
        mgr = AIRuntimeManager()
        rt = AIRuntime()
        rt.initialize()
        mgr.register(rt, default=True)
        self.assertEqual(len(mgr.list_runtimes()), 1)
        self.assertIsNotNone(mgr.get_default())

    def test_health_check_all(self) -> None:
        mgr = AIRuntimeManager()
        rt = AIRuntime()
        rt.initialize()
        mgr.register(rt)
        hc = mgr.health_check()
        self.assertEqual(len(hc), 1)


# ===== Integration Tests =====
class TestIntegration(unittest.TestCase):
    def test_ipc_bridge(self) -> None:
        bridge = IPCAIBridge()
        received = []
        bridge.register_handler('model_loaded', lambda e: received.append(e))
        evt = ModelLoaded(model_id='m1')
        bridge.dispatch(evt)
        self.assertEqual(len(received), 1)

    def test_workflow_bridge(self) -> None:
        bridge = WorkflowAIBridge()
        result = bridge.execute_inference('m1', 'Hello')
        self.assertEqual(result['model_id'], 'm1')

    def test_vision_bridge(self) -> None:
        bridge = VisionAIBridge()
        frame = {'width': 640, 'height': 480}
        result = bridge.process_frame(frame)
        self.assertEqual(result['status'], 'processed')


# ===== Resource Tests =====
class TestResources(unittest.TestCase):
    def test_lru_cache(self) -> None:
        cache = LRUCache(max_size=2)
        cache.put('a', 1)
        cache.put('b', 2)
        self.assertEqual(cache.get('a'), 1)
        cache.put('c', 3)
        # 'a' was accessed, so 'b' is evicted (LRU), not 'a'
        self.assertIsNone(cache.get('b'))
        self.assertIsNotNone(cache.get('a'))
        self.assertEqual(cache.size, 2)

    def test_temp_buffer(self) -> None:
        buf = TempBuffer(buffer_id='b1', data=b'hello')
        self.assertEqual(buf.buffer_id, 'b1')
        self.assertEqual(buf.size_bytes, 5)

    def test_resource_manager(self) -> None:
        rm = AIResourceManager()
        rm.allocate_model_memory('m1', 1024)
        self.assertEqual(rm.get_model_memory('m1'), 1024)
        rm.cache_embedding('e1', 'vec')
        self.assertEqual(rm.get_embedding_cache_size(), 1)
        rm.cleanup()
        self.assertEqual(rm.get_total_allocated(), 0)


# ===== Metrics Tests =====
class TestMetrics(unittest.TestCase):
    def test_counter(self) -> None:
        c = Counter('test_counter')
        c.increment(5)
        self.assertEqual(c.value, 5)

    def test_gauge(self) -> None:
        g = Gauge('test_gauge')
        g.set(42.0)
        self.assertEqual(g.value, 42.0)
        g.increment(8.0)
        self.assertEqual(g.value, 50.0)

    def test_histogram(self) -> None:
        h = Histogram('test_hist')
        h.observe(10.0)
        h.observe(20.0)
        h.observe(30.0)
        self.assertEqual(h.count, 3)
        self.assertEqual(h.average, 20.0)
        self.assertEqual(h.min_value, 10.0)
        self.assertEqual(h.max_value, 30.0)

    def test_metrics_collector(self) -> None:
        mc = AIMetricsCollector()
        mc.initialize()
        mc.increment_counter('inference_total', 5)
        mc.set_gauge('queue_depth', 10)
        mc.observe_histogram('inference_latency_ms', 100.0)
        collected = mc.collect()
        self.assertIn('counters', collected)
        self.assertIn('gauges', collected)
        self.assertIn('histograms', collected)


# ===== Health Tests =====
class TestHealth(unittest.TestCase):
    def test_health_status(self) -> None:
        self.assertEqual(HealthStatus.HEALTHY.value, 'healthy')
        self.assertEqual(HealthStatus.FAILED.value, 'failed')

    def test_health_service(self) -> None:
        hs = AIHealthService()
        hs.initialize()
        hs.update_status(HealthStatus.HEALTHY, 'all good')
        self.assertEqual(hs.status, HealthStatus.HEALTHY)
        hs.register_service('svc1', HealthStatus.HEALTHY)
        hc = hs.health_check()
        self.assertEqual(hc['status'], 'healthy')

    def test_health_service_failed(self) -> None:
        hs = AIHealthService()
        hs.register_service('svc1', HealthStatus.FAILED)
        hs.health_check()
        self.assertEqual(hs.status, HealthStatus.FAILED)


# ===== Security Tests =====
class TestSecurity(unittest.TestCase):
    def test_security_policy(self) -> None:
        policy = SecurityPolicy(max_input_length=1000, sandbox_enabled=True)
        self.assertEqual(policy.max_input_length, 1000)

    def test_security_validator(self) -> None:
        validator = SecurityValidator(SecurityPolicy(max_input_length=10))
        self.assertTrue(validator.validate_input('short'))
        self.assertFalse(validator.validate_input('this is way too long'))

    def test_permission_enum(self) -> None:
        self.assertEqual(Permission.READ.value, 'read')
        self.assertEqual(Permission.ADMIN.value, 'admin')


# ===== Storage Tests =====
class TestStorage(unittest.TestCase):
    def test_storage_domain(self) -> None:
        self.assertEqual(StorageDomain.PROMPTS.value, 'prompts')

    def test_storage_adapter(self) -> None:
        adapter = AIStorageAdapter()
        adapter.save_prompt('p1', {'text': 'hello'})
        data = adapter.load_prompt('p1')
        self.assertEqual(data['text'], 'hello')
        adapter.save_conversation('c1', {'title': 'Test'})
        conv = adapter.load_conversation('c1')
        self.assertEqual(conv['title'], 'Test')

    def test_storage_delete(self) -> None:
        adapter = AIStorageAdapter()
        adapter.save_prompt('p1', {'text': 'hello'})
        self.assertTrue(adapter.delete(StorageDomain.PROMPTS, 'p1'))
        self.assertIsNone(adapter.load_prompt('p1'))


# ===== Registry Tests =====
class TestRegistry(unittest.TestCase):
    def test_ai_registry(self) -> None:
        reg = AIRegistry()
        reg.register('svc1', {'test': True})
        self.assertIn('svc1', reg.list_services())
        self.assertTrue(reg.is_registered('svc1'))
        self.assertEqual(reg.get('svc1'), {'test': True})

    def test_duplicate_registration(self) -> None:
        reg = AIRegistry()
        reg.register('svc1', {'test': True})
        with self.assertRaises(DuplicateRegistrationError):
            reg.register('svc1', {'test': False})

    def test_version_compatibility(self) -> None:
        reg = AIRegistry()
        reg.register('svc1', {}, version='1.2.3')
        self.assertTrue(reg.check_version_compatibility('svc1', '1.0.0'))
        self.assertFalse(reg.check_version_compatibility('svc1', '2.0.0'))


if __name__ == '__main__':
    unittest.main()
