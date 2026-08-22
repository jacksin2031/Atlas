# Atlas Platform Architecture

> **Last Updated**: 2026-07-06
> **Current Version**: 0.12.0-beta

---

## Runtime Foundation (Sprint 1)

The core platform runtime providing service lifecycle, event distribution, scheduling, and state management.

### Module Structure
- **Service Registry** — Dynamic service discovery and registration
- **Event Bus** — Decoupled event distribution
- **Scheduler** — Task scheduling with priority support
- **State Management** — Persistent state with snapshot support
- **Runtime Lifecycle** — FSM-based lifecycle (CREATED → INITIALIZING → READY → RUNNING → SHUTTING_DOWN → TERMINATED)
- **Error Taxonomy** — Structured error types and hierarchies
- **Capability Registry** — Runtime capability negotiation
- **Contract System** — Service contract definitions
- **Manifest Specification** — Runtime configuration manifests

### Quality Gate
- 18 Rust source files
- 33 test cases
- Zero compilation warnings
- RFC-0001 through RFC-0014 (all Frozen)

---

## Runtime Infrastructure (Sprint 2)

Platform services for resource management, health monitoring, metrics, security, and storage abstraction.

### Modules
- **Resource Management** — LRU cache, temp buffers
- **Health Monitoring** — 6-status service
- **Metrics Collection** — Counter, Gauge, Histogram with p50/p95/p99
- **Security Framework** — 10 permissions, validator
- **Storage Backend** — Abstract persistence layer

---

## Plugin Runtime (Sprint 3)

Full plugin lifecycle management with capability negotiation, sandboxing, and service discovery.

### Module Structure
- **Plugin Loader** — Dynamic plugin loading with version awareness
- **Plugin Registry** — Service and capability registries
- **Capability Negotiation** — 9 capabilities discovered at runtime
- **Sandbox** — Permission model and isolation
- **Hot Reload** — Live plugin updates without restart
- **Service Discovery** — Plugin-to-service binding
- **Telemetry** — Plugin health and performance metrics
- **Diagnostics** — Plugin debugging and inspection

### Quality Gate
- 16 Rust source files
- 133 test cases
- RFC-0201 through RFC-0230 (all Implemented)

---

## IPC Runtime (Sprint 5)

Complete inter-process communication layer with message routing, security, and reliability.

### Module Structure
```
packages/ipc/src/
├── message/            # MessageEnvelope, Header, Payload, Metadata, Priority, validation
├── serialization/      # Serializer trait, JSON/Binary/Structured serializers, factory
├── transport/          # Transport trait, InMemoryTransport, factory
├── router/             # Router, routes, rule_engine, priority_queue, dead_letter_queue, discovery
├── channel/            # Channel, state_machine, registry, context
├── security/           # Permissions, auth, trust boundaries, origin validation, replay protection
├── reliability/        # Delivery guarantees, ordering, retry, DLQ manager
├── command/            # Command trait, handler, registry, dispatcher
├── eventbus/           # Bridge, events, publisher, subscriber
├── request_response/   # Request, correlator, timeout_manager, cancellation, client, server
├── session/            # Session, manager, registry, context
├── endpoint/           # Endpoint, registry, descriptor
├── capability/         # Resolver, matcher, version, negotiation
├── health/             # HealthService, HealthIntegration
├── metrics/            # MetricsService, MetricRecorders
├── tracing/            # SpanContext, TraceId, SpanId, distributed tracing
├── transport/adapters/ # TransportAdapter, NamedPipe/TCP/WebSocket skeletons
├── plugin/             # PluginIntegration, PluginBridge
└── workflow/           # WorkflowIntegration, WorkflowBridge
```

### Key Properties
- Platform-independent: No platform-specific IPC primitives
- Deterministic routing: Priority-sorted rules with exact/wildcard/prefix matching
- Dependency injection: All components use Arc<Mutex<>>, no global mutable state
- Zero warnings: Clean compilation with cargo check and cargo test
- 100 tests: All passing, covering every module

---

## Vision Runtime (Sprint 6)

Image acquisition, frame processing, computer vision pipelines, provider abstraction, and deterministic execution.

### Module Structure
```
packages/vision/src/atlas_vision/
├── errors.py           # VisionError + 20+ subclasses
├── events.py           # 11 immutable event types
├── models/
│   └── frame.py        # 12 frozen frame dataclasses
├── capture/            # Source types, provider ABC, thread-safe manager
├── services/           # Runtime, Manager, Context, Session, ServiceContract
├── scheduler/          # 7 trigger types (Immediate, Interval, Frame, Workflow, AI, Event, Cron)
├── pipeline/           # 11-stage deterministic pipeline with composable stages
├── provider/           # ProviderType enum, VisionProvider ABC
├── registry/           # 6 registries (Vision, Provider, Pipeline, Capture, Model, Capability)
├── graph/              # VisionNode, Edge, Graph (Kahn's algo), ExecutionPlan, Validator
├── capabilities/       # CapabilityNegotiator with 9 capabilities
├── resources/          # LRU cache, temp buffers, VisionResourceManager
├── metrics/            # Counter, Gauge, Histogram (p50/p95/p99), VisionMetricsCollector
├── health/             # 6-status HealthService
├── security/           # 10 permissions, SecurityValidator
├── storage/            # StorageBackend ABC, VisionStorageAdapter (5 domains)
└── integration/        # IPCVisionBridge, WorkflowVisionBridge, PluginVisionBridge
```

### Quality Gate
- 51 Python source files
- 185 test cases (163 unit + 22 integration)
- Zero platform-specific dependencies
- Zero circular dependencies
- All absolute imports
- Deterministic execution (sorted topo sort)
- No global mutable state (DI-injected)

---

## AI Runtime (Sprint 7)

Deterministic AI execution, model lifecycle management, provider abstraction, prompt execution, memory management, inference orchestration, agent execution, and capability negotiation.

### Module Structure
```
packages/ai/src/atlas_ai/
├── errors.py           # AIError + 30+ exception types
├── events.py           # 30+ immutable event types
├── models.py           # Model, ModelVersion, ModelDescriptor, ModelMetadata, ModelCapability, ModelProvider, ModelInstance, ModelConfiguration, ModelRequirements, ModelResourceUsage, ModelLifecycle, ModelState, ModelSnapshot, ModelRegistry
├── providers.py        # AIProvider, ProviderRegistry, ProviderDescriptor, ProviderCapability, ProviderHealth, ProviderSession, ProviderFactory (plugin-based)
├── capabilities.py     # CapabilityNegotiator with 14 capabilities
├── inference.py        # InferenceRequest, InferenceResponse, InferenceContext, InferenceJob, InferenceQueue, InferenceScheduler, InferenceExecutor, InferenceResult, InferenceMetadata, InferenceState (deterministic only)
├── prompts.py          # Prompt, PromptTemplate, PromptVariables, PromptContext, PromptCompiler, PromptExecutor, PromptHistory, PromptSnapshot, PromptRegistry
├── conversations.py    # Conversation, ConversationSession, ConversationHistory, ConversationMessage, ConversationRole, ConversationState, ConversationRegistry
├── memory.py           # MemoryStore, MemoryItem, MemoryScope (Session/Workspace/Project/Global), MemoryContext, MemorySnapshot, MemoryQuery, MemoryRegistry, MemoryPolicy
├── embeddings.py       # EmbeddingProvider, EmbeddingModel, EmbeddingRequest, EmbeddingResponse, EmbeddingIndex, EmbeddingStore, EmbeddingRegistry
├── agents.py           # Agent, AgentContext, AgentExecution, AgentState, AgentRegistry, AgentScheduler, AgentPolicy, AgentCapability
├── tools.py            # Tool, ToolDescriptor, ToolRegistry, ToolInvocation, ToolResult, ToolPermission, ToolCapability
├── scheduler.py        # Immediate, Interval, Workflow Trigger, Vision Trigger, IPC Trigger, AI Trigger, Cron Trigger
├── services.py         # AIRuntime, AIManager, AIContext, AISession, AIService, AIRuntimeManager
├── health/             # AIHealthService (6 statuses)
├── integration/        # IPCAIBridge, WorkflowAIBridge, VisionAIBridge
├── metrics/            # AIMetricsCollector (Counter/Gauge/Histogram)
├── registry/           # Service, provider, and capability registries
├── resources/          # AIResourceManager, LRUCache, TempBuffer
├── security/           # SecurityValidator, SecurityPolicy
└── storage/            # AIStorageAdapter (abstract persistence)
```

### Core Services (all implement Runtime Service Contract)
- **AIRuntime** — Central orchestrator with full lifecycle (CREATED → INITIALIZING → READY → RUNNING → SHUTTING_DOWN → TERMINATED)
- **AIManager** — Coordinates all subsystems
- **AIContext** — Immutable runtime context with clone-based mutation
- **AISession** — Session management
- **AIService** — Abstract service base class
- **AIRuntimeManager** — Multi-runtime instance management

### 14 Capabilities Discovered at Runtime
Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning

### Quality Gate
- 29 Python source files (35 total with tests/config)
- 105 test cases (94 unit + 11 integration)
- 174 exported symbols covering every required type
- Zero compilation errors, zero warnings
- Zero TODOs, zero placeholders
- Dependency injection throughout
- No global mutable state
- No circular dependencies
- Platform-independent (zero external dependencies)
- Deterministic execution guaranteed

---

## Knowledge Runtime (Sprint 8)

Knowledge pack management, document lifecycle, semantic search, and vector embeddings.

### Module Structure
```
packages/knowledge/src/atlas_knowledge/
├── common/             # 20+ frozen dataclass models (errors, events, state)
├── document/           # DocumentLifecycle, DocumentRegistry (Create, Import, Update, Archive, Delete, Restore, Version)
├── chunk/              # ChunkLifecycle, ChunkRegistry (deterministic lifecycle)
├── index/              # IndexBuilder, IndexRegistry (abstract lifecycle, no DB)
├── retrieval/          # RetrievalOrchestrator, RetrievalRegistry
├── search/             # SearchOrchestrator, SearchRegistry
├── citation/           # CitationRegistry, CitationPolicy
├── provider/           # ProviderRegistry, ProviderFactory (plugin abstraction)
├── registry/           # KnowledgeRegistry (unified)
├── resource/           # ResourceManager (cache tracking, leak prevention)
├── health/             # KnowledgeHealthService (6 states)
├── security/           # KnowledgeSecurityService (7 security layers)
├── metrics/            # KnowledgeMetricsCollector (9 metric types)
├── integration/        # KnowledgeIPCBus, AI/Vision/Workflow services, scheduler
└── runtime/            # KnowledgeRuntime, KnowledgeManager, KnowledgeContext, KnowledgeSession, KnowledgeService, KnowledgeRuntimeManager
```

### Quality Gate
- All models are frozen dataclasses with slots=True
- Dependency injection throughout, no global mutable state
- Platform-independent Python reference implementation design
- RFC specifications complete; implementation pending

---


## Conformance & Architecture Validation (Sprint 11)

Automated validation of the Atlas Architecture, ADS, ADRs, RFCs, Contracts,
Documentation, Layering Rules, and Runtime Conformance.

### Components

| Component | Description |
|-----------|-------------|
| ArchitectureValidator | Validates layering, dependencies, circular deps, provider pattern, DI |
| RFCValidator | Measures RFC compliance, implementation, testing, documentation |
| ADRValidator | Tracks ADR references, deprecation, supersession |
| DocumentationValidator | Verifies README consistency, cross-references, version numbers |
| ModuleValidator | Checks allowed/forbidden imports, naming conventions, package structure |
| TestCoverageValidator | Validates unit/integration/architecture tests per module |
| RuntimeContractValidator | Verifies service, lifecycle, metrics, health, provider, security, storage contracts |
| ArchitectureValidationService | Central orchestration for all validators |

### Output

Machine-readable JSON reports and human-readable summaries suitable for CI/CD.

See `docs/conformance/CONFORMANCE_REPORT.md` for the full report.

## Architecture Summary

```
Atlas Platform
├── Runtime Foundation (RFC-0001–0014) ✅ — Rust, 33 tests
├── Plugin Runtime (RFC-0201–0230) ✅ — Rust, 133 tests
├── IPC Runtime (RFC-0101–0112) ✅ — Rust, 100 tests
├── Vision Runtime (Sprint 6) ✅ — Python, 185 tests
├── AI Runtime (Sprint 7) ✅ — Python, 105 tests
├── Knowledge Runtime (Sprint 8) ⬜ — Specs only
├── Workflow Runtime (RFC-0301–0333) ⬜ — Specs only
├── Storage Runtime (RFC-0401–0425) ⬜ — Specs only
└── Project Runtime (Sprint 9) ⬜ — Planned
```
├── Cross Runtime Integration (Sprint 10) ✅ — Python, 99 tests

├── Conformance Runtime (Sprint 11) ✅ — Python, 52 tests
**Total Tests**: 1,723 (Rust: 266, Python: 1,458+, Specs: 66 RFCs)


---

## Project Runtime (Sprint 9)

The Project Runtime provides project management, workspace boundaries,
configuration, asset management, and hosting layer for all 7 runtimes.
Reference implementation in Python 3.10+.

### 16 Subsystems

| Subsystem | Files | Key Classes |
|---|---|---|
| Common | 7 | ProjectError hierarchy (7 types), EventType, frozen dataclasses |
| Workspace | 5 | Workspace, WorkspaceLifecycle, WorkspaceRegistry, WorkspaceManager |
| Project | 7 | Project, ProjectLifecycle, ProjectRegistry, ProjectManager, ProjectContext, ProjectSession, ProjectRuntimeManager |
| Asset | 5 | Asset, AssetLifecycle, AssetRegistry, AssetManager (10 asset types) |
| Configuration | 4 | ConfigurationProfile, ConfigurationLayer (5 layers), ConfigurationManager |
| Environment | 4 | Environment, EnvironmentProfile, EnvironmentManager |
| Template | 4 | Template, TemplateDescriptor, TemplateManager (6 builtin templates) |
| Build | 4 | BuildProfile, BuildConfiguration, BuildManager (abstract, no compiler) |
| Hosting Layer | 2 | RuntimeHost, RuntimeHostingLayer (hosts 7 runtimes) |
| Metrics | 2 | MetricsCollector (15 metric types) |
| Health | 2 | HealthService (6 states) |
| Security | 2 | SecurityService (isolation, validation) |
| Events/IPC | 2 | EventBus, ProjectIPCBus (16 event types) |
| Integration | 2 | Workflow/Vision/AI/Knowledge integration services |
| Main Runtime | 1 | ProjectRuntime (coordinator) |

### Quality Gate
- 57 Python source files in src/atlas_project/
- 11 test files in tests/project/
- 432 tests passing (237 workflow + 195 project runtime)
- Zero compilation errors, zero warnings
- Zero TODOs/placeholders
- No circular dependencies, no global mutable state
- Platform-independent Python reference implementation
- RFC-compliant (36 RFCs)
- Frozen dataclasses with slots=True
- Dependency injection throughout

### Quick Start
`python
from atlas_project import ProjectRuntime, ProjectDescriptor
`

### Documentation
- docs/project/PROJECT_COMPLIANCE_REPORT.md — Full RFC traceability matrix with 130+ acceptance criteria


## Desktop Shell (Sprint 12)

The Atlas Desktop Shell provides the graphical user interface that hosts every Atlas runtime.

### Technology Stack

| Layer | Technology |
|-------|-----------|
| Shell | Tauri 2 (Rust) |
| Frontend | React 19 + TypeScript |
| Bundler | Vite 7 |
| State | Zustand |
| UI | Fluent UI (base styles) |

### Implemented Components

| Component | Location |
|-----------|----------|
| Main Window | apps/atlas-desktop/src/App.tsx |
| Menu Bar | apps/atlas-desktop/src/components/layouts/MenuBar.tsx |
| Toolbar | apps/atlas-desktop/src/components/layouts/Toolbar.tsx |
| Workspace Manager | apps/atlas-desktop/src/workspace/WorkspaceManager.tsx |
| Panel Registry | apps/atlas-desktop/src/workspace/panel-registry.tsx |
| Layout Persistence | apps/atlas-desktop/src/workspace/persistence.ts |
| Status Bar | apps/atlas-desktop/src/components/layouts/StatusBar.tsx |
| Command Palette | apps/atlas-desktop/src/components/CommandPalette.tsx |
| Theme Manager | apps/atlas-desktop/src/stores/theme.ts |
| Workspace State | apps/atlas-desktop/src/workspace/store.ts |
| Project Manager | apps/atlas-desktop/src/stores/project.ts |
| Runtime Monitor | apps/atlas-desktop/src/components/panels/RuntimeMonitorPanel.tsx |
| Project Explorer | apps/atlas-desktop/src/components/panels/ProjectExplorerPanel.tsx |
| Log Console | apps/atlas-desktop/src/components/panels/LogConsolePanel.tsx |
| Extensions Manager | apps/atlas-desktop/src/components/panels/ExtensionsPanel.tsx |
| Settings | apps/atlas-desktop/src/components/panels/SettingsPanel.tsx |
| Notifications | apps/atlas-desktop/src/components/panels/NotificationsPanel.tsx |
| Problems | apps/atlas-desktop/src/components/panels/ProblemsPanel.tsx |
| Output | apps/atlas-desktop/src/components/panels/OutputPanel.tsx |
| Console | apps/atlas-desktop/src/components/panels/ConsolePanel.tsx |
| Logs | apps/atlas-desktop/src/components/panels/LogsPanel.tsx |

### Services

| Service | Location |
|---------|----------|
| IPC Service | apps/atlas-desktop/src/services/ipc.ts |
| Plugin Manager | apps/atlas-desktop/src/services/plugin-manager.ts |
| Project Service | apps/atlas-desktop/src/services/project.ts |
| Theme Service | apps/atlas-desktop/src/services/theme.ts |
| Layout Service | apps/atlas-desktop/src/services/layout.ts |
| Log Service | apps/atlas-desktop/src/services/log.ts |
| Command Palette Service | apps/atlas-desktop/src/services/command-palette.ts |

### Compliance

- Architecture compliant (MODULE_DEPENDENCIES.md Layer 8)
- RFC-0001 through RFC-0014 (Runtime)
- RFC-0101 through RFC-0112 (IPC)
- RFC-0201 through RFC-0230 (Plugin)
- Full compliance report: docs/desktop/DESKTOP_COMPLIANCE_REPORT.md



## Workflow Studio (Sprint 13)

The Atlas Workflow Studio provides the visual workflow editor running inside the Desktop Shell.

### Technology Stack

| Layer | Technology |
|-------|-----------|
| Canvas | React Flow (@xyflow/react) |
| State | Zustand |
| Communication | IPC (Tauri) |

### Implemented Components

| Component | Location |
|-----------|----------|
| Workflow Editor | src/studio/workflow/WorkflowStudioPanel.tsx |
| Node Canvas | src/studio/workflow/components/canvas/workflow-canvas.tsx |
| Node Palette | src/studio/workflow/components/sidebar/node-palette.tsx |
| Property Inspector | src/studio/workflow/components/inspector/property-inspector.tsx |
| Variable Manager | src/studio/workflow/components/variables/variable-manager.tsx |
| Toolbar | src/studio/workflow/components/toolbar/workflow-toolbar.tsx |
| Debugger Panel | src/studio/workflow/components/toolbar/debugger-panel.tsx |
| Validation Report | src/studio/workflow/components/properties/validation-report.tsx |
| Custom Nodes | src/studio/workflow/components/nodes/ |
| Custom Edges | src/studio/workflow/components/edges/ |

### Stores

| Store | Location |
|-------|----------|
| Workflow Canvas Store | src/studio/workflow/stores/workflow-store.ts |
| Execution Store | src/studio/workflow/stores/execution-store.ts |
| Debug Store | src/studio/workflow/stores/debug-store.ts |
| Variable Store | src/studio/workflow/stores/variable-store.ts |
| Node Registry Store | src/studio/workflow/stores/node-registry-store.ts |

### Services

| Service | Location |
|---------|----------|
| Executor Service | src/studio/workflow/services/executor-service.ts |
| Debugger Service | src/studio/workflow/services/debugger-service.ts |
| Validation Service | src/studio/workflow/services/validation-service.ts |
| Import/Export Service | src/studio/workflow/services/import-export-service.ts |
| Plugin Discovery Service | src/studio/workflow/services/plugin-discovery-service.ts |

### Compliance

- Full RFC compliance (RFC-0301 through RFC-0333, 33 RFCs)
- Architecture compliant (MODULE_DEPENDENCIES.md Layer 8)
- IPC compliant (all runtime calls via IPC bridge)
- Plugin compliant (RFC-0323 dynamic discovery)
- 91 unit/integration tests across 10 test files
- 44 node types across 18 categories
- Zero TODOs, zero placeholders, zero warnings
- Full compliance report: docs/workflow/WORKFLOW_STUDIO_COMPLIANCE_REPORT.md

## Vision Studio (Sprint 14, alpha)

Vision Studio is a standalone Layer 8 workspace. It does not use React Flow and React components do not import the Python Vision Runtime. The active dependency path is:

```text
DesktopShell -> WorkspaceManager -> FlexLayout -> PanelRegistry -> Vision panels
Vision panels -> Zustand stores / UI services -> IPC bridge -> Vision Runtime
```

FlexLayout JSON contains layout data and stable panel references only. Workflow and Vision retain independent, versioned models (`atlas.layout.workflow.v1` and `atlas.layout.vision.v1`). Validation rejects malformed, unsupported, unknown-panel, duplicate-panel, and blank-center layouts and restores the relevant default.

Vision UI source is under `apps/atlas-desktop/src/studio/vision/`; workspace infrastructure is under `apps/atlas-desktop/src/workspace/`. Runtime analysis remains under `packages/vision/`.
