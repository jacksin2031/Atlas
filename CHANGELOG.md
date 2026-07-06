# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](VERSIONING.md).

---


---
## [0.12.0-beta] — 2026-07-06

### Sprint 12 — Desktop Shell

#### Added
- **Desktop Shell** — Production desktop foundation with Tauri 2 + React 19
  - Tauri 2 + React 19 + TypeScript + Vite 7 architecture
  - Menu System: Menu Bar, Toolbar, Status Bar, Command Palette
  - Dockable Panels: Project Explorer, Runtime Monitor, Output, Console, Logs, Extensions, Settings, Problems, Notifications
  - Runtime Monitor: Live dashboard for 8 runtimes (Workflow, Vision, AI, Knowledge, Plugin, IPC, Project, Storage)
  - Theme Manager: Dark/Light/System theme support with live switching
  - Layout Manager: Docking, resizable panels, persistence, reset
  - Plugin Support: Extension Manager with search, status, health indicators
  - Logging: Real-time logs, filtering, export, search
  - Project Support: Open/Close/Recent projects, workspace management, settings
  - Command Palette: Quick commands, fuzzy search, recent commands, keyboard shortcuts
- **Architecture Layer 8** — Production Desktop Foundation

#### Changed
- Runtime Architecture extended with Desktop Shell layer
- Repository structure updated with apps/atlas-desktop/

#### Documentation
- Added Desktop Shell compliance report
- Updated Architecture documentation
- Updated Quick Start with desktop build instructions

---

## [0.9.0-alpha] — 2026-07-05

### Sprint 9 — Project Runtime

#### Added
- **Project Runtime** — Complete project management and orchestration layer
  - Workspace Runtime: Workspace, WorkspaceLifecycle, WorkspaceRegistry, WorkspaceManager
  - Project Runtime: Project, ProjectLifecycle, ProjectRegistry, ProjectManager, ProjectContext, ProjectSession, ProjectRuntimeManager
  - Asset Runtime: Asset, AssetLifecycle, AssetRegistry, AssetManager (10 asset types)
  - Configuration Runtime: ConfigurationProfile, ConfigurationLayer (5 layers), ConfigurationManager
  - Environment Runtime: Environment, EnvironmentProfile, EnvironmentManager
  - Template Runtime: Template, TemplateDescriptor, TemplateManager (6 builtin templates)
  - Build Runtime: BuildProfile, BuildConfiguration, BuildManager (abstract, no compiler)
  - Hosting Layer: RuntimeHost, RuntimeHostingLayer (hosts 7 runtimes)
  - Common: ProjectError hierarchy (7 types), EventType, frozen dataclasses
  - Metrics: MetricsCollector (15 metric types)
  - Health: HealthService (6 states)
  - Security: SecurityService (isolation, validation)
  - Events/IPC: EventBus, ProjectIPCBus (16 event types)
  - Integration: Workflow/Vision/AI/Knowledge integration services
  - Main Runtime: ProjectRuntime (coordinator)
- **Project Compliance Report** — Full RFC mapping, acceptance criteria, coverage summary
- 57 Python source files in src/atlas_project/
- 11 test files in tests/project/
- 432 tests passing (237 workflow + 195 project runtime)
- 36 RFC specs

#### Changed
- Workspace structure updated with project package
- Documentation structure updated

#### Security
- SecurityService with isolation and validation
- Asset lifecycle security controls

#### Performance
- Deterministic execution across all 16 subsystems
- Frozen dataclasses with slots=True
- Dependency injection throughout

#### Documentation
- Added Project Compliance Report
- Updated Architecture documentation
- Quick start: from atlas_project import ProjectRuntime, ProjectDescriptor

---
## [Unreleased]
### Sprint 11 — Conformance & Architecture Validation

#### Added
- **Conformance Runtime** — Complete architecture validation and RFC compliance framework
  - Core Models: ArchitectureRule, ArchitectureViolation, ArchitectureReport, RFCCompliance, ADRCompliance, DocumentationCoverage, ModuleGraph, TestCoverage, ConformanceReport
  - Enums: ViolationSeverity, RuleCategory, RFCStatus, ADRStatus, ComplianceLevel
  - RFCScanner: Parses 121 RFCs from specs/, extracts metadata, requirements, acceptance criteria
  - ADRScanner: Parses 12 ADRs from docs/adr/
  - DocumentationScanner: Finds READMEs, compliance reports, architecture docs, cross-references
  - ModuleScanner: AST-based Python module analysis, import tracking, dependency graph
  - ArchitectureValidator: 9 rules (layering, dependency direction, circular deps, forbidden imports, provider pattern, DI, immutable models, runtime contracts, project hosting)
  - RFCValidator: Checks implementation, reference, testing, documentation per RFC
  - ADRValidator: Finds ADR references in specs, tracks deprecation/supersession
  - DocumentationValidator: Verifies 13 expected docs, broken references, version/sprint consistency
  - ModuleValidator: Forbidden imports, naming conventions, required packages, public API
  - TestCoverageValidator: Scans test files per module, counts unit/integration/architecture tests
  - RuntimeContractValidator: Validates 7 contract types (service, lifecycle, metrics, health, provider, security, storage)
  - ArchitectureValidationService: Orchestrates all validators, generates JSON reports
  - CLI entry point with --repo-root, --output, --format, --quiet flags
  - Benchmark suite measuring validation time per component
  - Runtime Contracts: RuntimeContract with 7 sub-contracts
- **Conformance Compliance Report** — Full validation matrix with architecture rules, RFC coverage, ADR references
- 46 Python source files in src/atlas_conformance/
- 10 test files in tests/conformance/
- 52 conformance tests passing
- Generated reports: docs/conformance/CONFORMANCE_REPORT.md, conformance_report.json

#### Changed
- Workspace structure updated with conformance package
- Documentation structure updated with conformance section

#### Fixed
- All existing workflow tests (15) still pass

### Sprint 10 — Cross-Runtime Integration

#### Added
- **Cross-Runtime Integration Layer** — Complete integration framework connecting all 9 runtimes
  - RuntimeIntegrationManager: Master coordinator combining all runtime components
  - RuntimeGraph: Immutable DAG with cycle/missing/illegal dependency detection
  - RuntimeDependencyResolver: Validates dependencies and computes startup/shutdown order
  - RuntimeBootstrapper: Ordered startup with partial failure tolerance and restart
  - RuntimeShutdownManager: Reverse-order shutdown with metrics flush and metadata persist
  - RuntimeCoordinator: Full lifecycle management (register → start → stop → validate)
  - CrossRuntimeEventRouter: Routes events across all 9 runtime event types with priority ordering
  - ArchitectureValidator: Automatically validates layering, forbidden imports, required modules
  - PerformanceBenchmarks: Measurement utilities for startup, shutdown, event latency, cross-runtime latency, plugin load time
- **Integration Compliance Report** — Full compliance report with architecture validation, integration matrix, dependency matrix, scenario coverage, acceptance criteria, known limitations
- 99 new tests covering cross-runtime scenarios

#### Changed
- Workspace structure updated with integration package
- Documentation structure updated with integration quick-start example

#### Fixed
- Test file naming conflicts (5 duplicate module names across subdirectories)

---

## [0.8.0-alpha] — 2026-07-04

### Sprint 8 — Knowledge Runtime

#### Added
- **Knowledge Runtime Specifications** — Full RFC design for knowledge pack system
  - Knowledge pack package format and semantic search architecture
  - Vector embeddings and knowledge graph design
  - Document lifecycle: Create, Import, Update, Archive, Delete, Restore, Version
  - Chunk processing with deterministic lifecycle
  - Abstract index builder with no DB dependency
  - Retrieval and search orchestrators
  - Citation management with policy engine
  - Provider abstraction (plugin-based factory)
  - Unified KnowledgeRegistry
  - Resource management (cache tracking, leak prevention)
  - Health service (6 states)
  - Security service (7 security layers)
  - Metrics collector (9 metric types)
  - Integration bridges: IPC, AI, Vision, Workflow, Scheduler
- **Knowledge Runtime Architecture** — Full design document
  - 15 module structure (Common, Document, Chunk, Index, Retrieval, Search, Citation, Provider, Registry, Resource, Health, Security, Metrics, Integration, Runtime)
  - Frozen dataclass models with slots=True
  - Dependency injection throughout, no global mutable state
  - Platform-independent Python reference implementation design
- **Knowledge Compliance Report** — Full RFC mapping, acceptance criteria, coverage summary
- **Documentation** — DESIGN_PRINCIPLES.md, MODULE_DEPENDENCIES.md

#### Changed
- Workspace structure updated with knowledge package
- Documentation structure updated

#### Security
- KnowledgeSecurityService with 7 security layers
- Provider isolation and sandbox enforcement
- Citation policy validation

#### Documentation
- Added Knowledge Compliance Report
- Updated Architecture documentation
- Added DESIGN_PRINCIPLES.md and MODULE_DEPENDENCIES.md

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

#### Security
- Model/tool/prompt validation
- Provider isolation
- Input/output validation
- Sandbox enforcement

#### Performance
- Deterministic execution (no hash-dependent ordering)
- LRU cache with leak prevention
- Async event processing

#### Documentation
- Added AI Compliance Report
- Updated Architecture documentation

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

#### Security
- Permission validation and provider isolation
- 10 security permissions defined

#### Performance
- Deterministic execution (sorted topological sort)
- LRU cache with bounded memory
- Frozen dataclasses (slots=True)

#### Documentation
- Added Vision Compliance Report
- Updated Architecture documentation

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

