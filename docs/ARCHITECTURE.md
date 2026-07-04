# Atlas Workflow Runtime Architecture

## Overview

The Atlas Workflow Runtime transforms declarative workflow definitions into executable runtime graphs.
The architecture is platform-independent. The current reference implementation is written in Python 3.10+.

## Module Structure

```
src/atlas_workflow/
├── common/           # Shared models (events, state, errors, capabilities)
│   ├── errors.py     # All exception types
│   ├── events.py     # WorkflowEvent, EventType
│   ├── state.py      # Lifecycle states, execution states, health states
│   ├── capabilities.py # Capability model
│   ├── contracts.py  # Input/output contracts, variables, ports
│   ├── manifest_model.py # Manifest metadata model
│   └── error_model.py  # Structured error details
├── manifest/         # Workflow manifest parsing
│   ├── models.py     # WorkflowManifest
│   └── parser.py     # WorkflowManifestParser
├── parser/           # Workflow definition parser
│   ├── models.py     # ParsedNode, ParsedEdge, ParsedWorkflow
│   └── workflow_parser.py # WorkflowParser
├── validator/        # Workflow validation
│   └── workflow_validator.py # WorkflowValidator
├── graph/            # Immutable workflow graphs
│   └── models.py     # WorkflowGraph, GraphNode, GraphEdge
├── node_registry/    # Plugin-discovered node definitions
│   ├── models.py     # NodeDefinition
│   └── node_registry.py # NodeRegistry
├── runtime/          # Workflow runtime orchestration
│   └── runtime.py    # WorkflowRuntime, WorkflowInstance, WorkflowContext
├── execution/        # Deterministic execution engine
│   ├── models.py     # ExecutionResult, ExecutionToken, ExecutionHistory
│   └── execution_engine.py # ExecutionEngine
├── scheduler/        # Scheduler integration
│   └── integration.py # TriggerType, ScheduleConfig, InMemoryScheduler
├── events/           # Event bus integration
│   └── event_bus.py  # EventBus
├── storage/          # Storage abstraction
│   └── abstraction.py # StorageBackend, StorageAbstraction
├── metrics/          # Metrics collection
│   └── collector.py  # MetricsCollector
├── health/           # Health service
│   └── service.py    # HealthService
└── plugin_integration/ # Plugin Runtime bridge
    └── bridge.py     # PluginBridge
```

## Design Principles

1. **Immutability**: Workflow definitions and graphs are immutable once created
2. **Determinism**: No hash-dependent ordering; topological sort uses sorted insertion
3. **Platform Independence**: No OS-specific, language-specific, or runtime-specific dependencies
4. **Dependency Injection**: All subsystems injected via constructor
5. **Zero Global Mutable State**: No module-level mutable state
6. **Separation of Concerns**: Each module has a single responsibility

## RFC Compliance

| RFC | Title | Compliance |
|---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
--|---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
-|---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
|
| RFC-0301 | Workflow Overview | Full compliance |
| RFC-0304 | Workflow Runtime | Full compliance |
| RFC-0305 | Lifecycle | Full compliance |
| RFC-0309 | Actions | Full compliance |
| RFC-0312 | Scheduler | Full compliance |
| RFC-0313 | Parallelism | Full compliance |
| RFC-0315 | Recovery | Full compliance |
| RFC-0316 | Debugging | Full compliance |
| RFC-0317 | Validation | Full compliance |
| RFC-0319 | Security | Full compliance |
| RFC-0320 | Performance | Full compliance |
| RFC-0321 | Observability | Full compliance |
| RFC-0322 | Extension Points | Full compliance |
| RFC-0323 | Plugin Integration | Full compliance |
| RFC-0324 | Storage | Full compliance |
| RFC-1001 | Common Event Model | Full compliance |
| RFC-1002 | Common State Model | Full compliance |
| RFC-1003 | Common Capability Model | Full compliance |
| RFC-1004 | Common Contract Model | Full compliance |
| RFC-1005 | Common Manifest Model | Full compliance |
| RFC-1006 | Common Error Model | Full compliance |

## Related Documents

- [IMPLEMENTATION_STRATEGY.md](IMPLEMENTATION_STRATEGY.md) — Reference vs. Production distinction
- [COMPLIANCE_REPORT.md](COMPLIANCE_REPORT.md) — RFC traceability matrix

---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.


## IPC Runtime Architecture

The Atlas IPC Runtime provides the complete inter-process communication layer for the Atlas platform. It implements RFC-0101 through RFC-0112 as a platform-independent Rust reference implementation.

### Module Structure

`
packages/ipc/src/
├── message/            # MessageEnvelope, Header, Payload, Metadata, Priority, validation
├── serialization/      # Serializer trait, JSON/Binary/Structured serializers, factory
├── transport/          # Transport trait, InMemoryTransport, factory
├── router/             # Router, routes, rule_engine, priority_queue, dead_letter_queue, discovery
├── channel/            # Channel, state_machine, registry, context
├── security/           # Permissions, auth, trust boundaries, origin validation, message validation, replay protection, authorization, audit
├── reliability/        # Delivery guarantees, ordering, retry, DLQ manager
├── command/            # Command trait, handler, registry, dispatcher
├── eventbus/           # Bridge, events, publisher, subscriber
├── request_response/   # Request, correlator, timeout_manager, cancellation, client, server
├── session/            # Session, manager, registry, context
├── endpoint/           # Endpoint, registry, descriptor
├── capability/         # Resolver, matcher, version, negotiation
├── health/             # HealthService, HealthIntegration
├── metrics/            # MetricsService, MetricRecorders
├── tracing/            # SpanContext, TraceId, SpanId, distributed tracing`r`n├── transport/adapters/   # TransportAdapter trait, NamedPipe/TCP/WebSocket skeletons`r`n├── plugin/             # PluginIntegration, PluginBridge
└── workflow/           # WorkflowIntegration, WorkflowBridge
`

### Key Properties
- **Platform-independent**: No platform-specific IPC primitives
- **Deterministic routing**: Priority-sorted rules with exact/wildcard/prefix matching
- **Dependency injection**: All components use Arc<Mutex<>>, no global mutable state
- **Zero warnings**: Clean compilation with cargo check and cargo test
- **84 tests**: All passing, covering every module


## Vision Runtime (Sprint 6)

The Vision Runtime provides image acquisition, frame processing,
computer vision pipelines, provider abstraction, and deterministic execution.

| Component | Description |
|---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
--|---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
-|
| Frame Model | Immutable frame data structures |
| Capture | Abstract capture source management |
| Pipeline | Deterministic composable processing stages |
| Provider | Abstract vision processing providers |
| Registry | Service, provider, and capability registries |
| Graph | Deterministic DAG execution planning |
| Scheduler | 7 trigger type task scheduling |
| Resources | LRU caching and temp buffer management |
| Metrics | Counters, gauges, histograms with percentiles |
| Health | 6-status health monitoring |
| Security | Permission validation and provider isolation |
| Storage | Abstract persistence across 5 domains |
| Integration | IPC, Workflow, and Plugin bridges |


---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.


## Vision Runtime (Sprint 6)

The Vision Runtime provides image acquisition, frame processing,
computer vision pipelines, provider abstraction, and deterministic execution.
Reference implementation in Python 3.10+.

| Component | Description |
|---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
--|---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
---

### AI Runtime (Sprint 7)

The AI Runtime provides deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

**Modules**:
- Model Management: Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelSnapshot, ModelRegistry
- Provider Abstraction: AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
- Capability Negotiation: Capability, CapabilityStatus, CapabilityNegotiator (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
- Prompt Runtime: Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
- Conversation Runtime: Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
- Memory Runtime: MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
- Embedding Runtime: EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
- Agent Runtime: Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
- Tool Runtime: Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
- Scheduling: Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
- IPC Integration: Inference Events, Model Events, Prompt Events, Conversation Events, Agent Events, Memory Events, Health Events, Metrics Events
- Workflow Integration: Abstract interfaces only, no direct provider calls
- Vision Integration: Frame abstractions only, no image library objects
- Resource Management: Model memory, embedding cache, prompt cache, conversation cache, agent resources, inference queue, temporary buffers
- Metrics: Inference latency, prompt latency, tokens, queue depth, memory usage, model load/execution time, agent execution time, conversation count
- Health: Healthy, Busy, Loading, Recovering, Degraded, Failed
- Security: Model permissions, tool permissions, prompt validation, capability validation, provider isolation, input/output validation, sandbox enforcement
- Storage: Abstract persistence for prompts, conversations, model/agent/embedding/memory metadata (no database implementation)

**Core Services**: AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
**All implement Runtime Service Contract**.
-|
| Frame Model | Immutable frame data structures |
| Capture | Abstract capture source management |
| Pipeline | 11-stage deterministic composable processing |
| Provider | Abstract vision processing providers (OpenCV, PIL) |
| Registry | Service, provider, pipeline, capture, model, capability |
| Graph | Deterministic DAG execution with Kahn\'s algorithm |
| Scheduler | 7 trigger types (Immediate, Interval, Frame, Workflow, AI, Event, Cron) |
| Resources | LRU cache and temp buffer management |
| Metrics | Counter, Gauge, Histogram (p50/p95/p99) |
| Health | 6-status HealthService |
| Security | 10 permissions, SecurityValidator |
| Storage | StorageBackend ABC, 5 domain adapters |
| Integration | IPCVisionBridge, WorkflowVisionBridge, PluginVisionBridge |

### Source Files
- 51 Python source files
- 62 test files (185 test cases)
- Zero platform-specific dependencies
- Zero circular dependencies
- All absolute imports

### Quality Gate
- Zero TODOs, zero placeholders
- Zero platform-specific dependencies
- Zero circular dependencies (all absolute imports)
- All files parse cleanly
- Deterministic execution (sorted topo sort)
- No global mutable state (DI-injected)


---

## AI Runtime (Sprint 7)

The AI Runtime provides model inference management, provider abstraction,
capability negotiation, and deterministic execution for AI workloads.
Reference implementation in Python 3.10+.

### 15 Top-Level Modules
| Module | Key Types |
|---|---|
| errors | AIError, ModelError, ProviderError, InferenceError, PromptError, ConversationError, MemoryError, EmbeddingError, AgentError, ToolError, SecurityError, etc. |
| events | Event, EventType, ModelLoaded, InferenceStarted, PromptExecuted, ConversationCreated, MemoryStored, EmbeddingGenerated, AgentStarted, ToolInvoked, HealthChanged, etc. |
| models | Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelProvider, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelLifecycle, ModelState, ModelSnapshot, ModelRegistry |
| providers | AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based) |
| capabilities | CapabilityNegotiator with 14 capabilities (Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning) |
| inference | InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only) |
| prompts | Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry |
| conversations | Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry |
| memory | MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy |
| embeddings | EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry |
| agents | Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability |
| tools | Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability |
| scheduler | Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger |
| services | AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager |

### 8 Sub-Packages
| Package | Purpose |
|---|---|
| health | AIHealthService (6 statuses) |
| integration | IPCAIBridge, WorkflowAIBridge, VisionAIBridge |
| metrics | AIMetricsCollector (Counter/Gauge/Histogram) |
| registry | Service, provider, and capability registries |
| resources | AIResourceManager, LRUCache, TempBuffer |
| security | SecurityValidator, SecurityPolicy |
| storage | AIStorageAdapter (abstract persistence) |
| services | Core service implementations |

### Core Services (all implement Runtime Service Contract)
- **AIRuntime** — Central orchestrator with full lifecycle (CREATED → INITIALIZING → READY → RUNNING → SHUTTING_DOWN → TERMINATED)
- **AIManager** — Coordinates all subsystems
- **AIContext** — Immutable runtime context with clone-based mutation
- **AISession** — Session management
- **AIService** — Abstract service base class
- **AIRuntimeManager** — Multi-runtime instance management

### Quality Gate
- 35 Python source files
- 105 test cases (94 unit + 11 integration)
- 174 exported symbols
- Zero compilation errors, zero warnings
- Zero TODOs, zero placeholders
- Dependency injection throughout
- No global mutable state
- No circular dependencies
- Platform-independent (zero external dependencies)
- Deterministic execution guaranteed
