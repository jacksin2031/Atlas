# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](VERSIONING.md).

---

## [Unreleased]

---

## [0.7.0-alpha] — 2026-07-04

### Sprint 7 — AI Runtime

#### Added
- **AI Runtime** — Complete AI model inference and management layer
  - Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelProvider, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelLifecycle, ModelState, ModelSnapshot, ModelRegistry
  - Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
  - Capability Negotiation: 14 capabilities discovered at runtime (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
  - Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
  - Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
  - Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
  - Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
  - Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
  - Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
  - Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
  - Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
  - Core Services: AIRuntime (full lifecycle FSM), AIManager, AIContext, AISession, AIService, AIRuntimeManager
  - Resource Management: AIResourceManager, LRUCache, TempBuffer (model memory, embedding/prompt/conversation caches, leak prevention)
  - Metrics: AIMetricsCollector with Counter/Gauge/Histogram (latency, tokens, queue depth, memory, load time, execution time)
  - Health: AIHealthService (Healthy/Busy/Loading/Recovering/Degraded/Failed)
  - Security: SecurityValidator, SecurityPolicy (model/tool/prompt/capability validation, provider isolation, input/output validation, sandbox enforcement)
  - Storage: AIStorageAdapter (abstract persistence for prompts/conversations/model/agent/embedding/memory metadata — no DB)
  - Integration: IPCAIBridge (full event bridge), WorkflowAIBridge (abstract interfaces), VisionAIBridge (Frame abstractions)
- **AI Compliance Report** — Full RFC mapping, acceptance criteria, coverage summary
- 35 Python source files (29 src + 6 test)
- 105 test cases (94 unit + 11 integration)
- 174 exported symbols covering every required type
- All core services implement Runtime Service Contract

#### Changed
- Workspace structure updated with AI package
- Documentation structure updated

---

## [0.6.0-alpha] — 2026-07-04

### Sprint 6 — Vision Runtime

#### Added
- **Vision Runtime** — Image acquisition, frame processing, and computer vision pipeline
  - Frame Model: 12 frozen frame dataclasses
  - Capture: Source types, provider ABC, thread-safe manager
  - Pipeline: 11-stage deterministic composable processing
  - Provider: ProviderType enum, VisionProvider ABC
  - Registry: 6 registries (Vision, Provider, Pipeline, Capture, Model, Capability)
  - Graph: VisionNode, Edge, Graph (Kahn's algo), ExecutionPlan, Validator
  - Scheduler: 7 trigger types (Immediate, Interval, Frame, Workflow, AI, Event, Cron)
  - Resources: LRU cache, temp buffers, VisionResourceManager
  - Metrics: Counter, Gauge, Histogram (p50/p95/p99), VisionMetricsCollector
  - Health: 6-status HealthService
  - Security: 10 permissions, SecurityValidator
  - Storage: StorageBackend ABC, VisionStorageAdapter (5 domains)
  - Integration: IPCVisionBridge, WorkflowVisionBridge, PluginVisionBridge
- **Vision Compliance Report** — Full RFC mapping, acceptance criteria, coverage summary
- 51 Python source files
- 185 test cases (163 unit + 22 integration)

#### Changed
- Workspace structure updated with vision package

---
## [0.5.0-alpha] — 2026-07-04

### Sprint 5 — IPC Runtime

#### Added
- **IPC Runtime** — Complete inter-process communication layer
  - Message envelope with header, payload, metadata, priority
  - Serialization: JSON, Binary, Structured
  - Transport: In-memory, Named Pipe, TCP, WebSocket (skeletons)
  - Router: rule engine, priority queue, discovery, dead letter queue
  - Channel: state machine, registry, context
  - Security: authentication, authorization, audit, replay protection, origin validation, trust boundaries
  - Reliability: delivery guarantees, ordering, retry, DLQ manager
  - Command system: handler, registry, dispatcher
  - Event bus: bridge, publisher, subscriber
  - Request/response: correlator, timeout manager, cancellation
  - Session: manager, registry, context
  - Endpoint: descriptor, registry
  - Capability: resolver, matcher, version, negotiation
  - Health: service, integration
  - Metrics: service, recorders
  - Tracing: span context, trace ID, span ID, distributed tracing
  - Plugin integration bridge
  - Workflow integration bridge
- **IPC Compliance Report** — Full RFC-0101 through RFC-0112 mapping
- **Python Reference Implementation** — RFC-compliant IPC reference
- 91 Rust source files
- 100 test cases

#### Changed
- Workspace Cargo.toml updated with IPC package
- Documentation structure reorganized

#### Fixed
- Circular imports between runtime.py and session.py
- MetricsCollector naming → VisionMetricsCollector
- FrameBuffer.empty() default arguments
- VisionPipelineManager registry type mismatch
- Added CapabilityRegistry.discover() method
- Added VisionRuntime self-registration

---

## [0.4.0-alpha] — 2026-07-01

### Sprint 4 — Workflow Runtime

#### Added
- **Workflow Runtime** — Declarative workflow execution engine
  - Workflow manifest parsing and validation
  - Immutable workflow graph with Kahn\'s algorithm
  - Deterministic execution engine
  - 7 trigger types: Immediate, Interval, Frame, Workflow, AI, Event, Cron
  - Plugin bridge integration
  - Storage abstraction
  - Metrics collector
  - Health service
- **Workflow Compliance Report** — Full RFC-0301 through RFC-0333 mapping
- Python reference implementation in `src/atlas_workflow/`

#### Changed
- Runtime Architecture updated with workflow layer
- Documentation reorganized

---

## [0.3.0-alpha] — 2026-06-30

### Sprint 3 — Plugin Runtime

#### Added
- **Plugin Runtime** — Full plugin lifecycle management
  - Plugin loader and registry
  - Capability negotiation (9 capabilities)
  - Sandbox and permission model
  - Hot reload support
  - Service discovery
  - Telemetry and diagnostics
- **Plugin Compliance Report** — Full RFC-0201 through RFC-0230 mapping
- 16 Rust source files
- 133 test cases

#### Changed
- Runtime Architecture updated with plugin layer
- Compliance reporting framework established

---

## [0.2.0-alpha] — 2026-06-29

### Sprint 2 — Runtime Infrastructure

#### Added
- **Runtime Infrastructure** — Core platform services
  - Resource management (LRU cache, temp buffers)
  - Health monitoring (6-status service)
  - Metrics collection (Counter, Gauge, Histogram with p50/p95/p99)
  - Security framework (10 permissions, validator)
  - Storage backend abstraction
- Infrastructure RFCs documented

#### Changed
- Runtime Foundation extended with infrastructure layer

---

## [0.1.0-alpha] — 2026-06-28

### Sprint 1 — Runtime Foundation

#### Added
- **Runtime Foundation** — Core platform runtime
  - Service registry
  - Event bus
  - Scheduler
  - State management
  - Runtime lifecycle (FSM)
  - Error taxonomy
  - Capability registry
  - Contract system
  - Manifest specification
- **Runtime Compliance Report** — Full RFC-0001 through RFC-0014 mapping
- 18 Rust source files
- 33 test cases

#### Fixed
- Registry initialization
- Metrics naming conventions

---

## [0.0.1-alpha] — 2026-06-27

### Sprint 0 — Bootstrap

#### Added
- Project initialization
- Rust workspace structure
- Repository organization
- `.gitignore` with comprehensive exclusions
- Initial documentation scaffold

