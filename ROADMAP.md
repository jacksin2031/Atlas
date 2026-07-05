# Atlas Roadmap

> **Last Updated**: 2026-07-04
> **Current Version**: 0.10.0-alpha
> **Current Sprint**: Sprint 10 (Cross-Runtime Integration)
> **Next Milestone**: Sprint 11 — Cross Runtime Integration

---

## Completed Sprints

### Sprint 0 — Bootstrap
**Version**: 0.0.1-alpha
**Status**: ✅ Complete
- Project initialization
- Rust workspace structure
- Repository organization

### Sprint 1 — Runtime Foundation
**Version**: 0.1.0-alpha
**Status**: ✅ Complete
- Service registry
- Event bus
- Scheduler
- State management
- Runtime lifecycle (FSM)
- Error taxonomy
- Capability registry
- Contract system
- Manifest specification

### Sprint 2 — Runtime Infrastructure
**Version**: 0.2.0-alpha
**Status**: ✅ Complete
- Resource management (LRU cache, temp buffers)
- Health monitoring (6-status service)
- Metrics collection (Counter, Gauge, Histogram)
- Security framework (10 permissions)
- Storage backend abstraction

### Sprint 3 — Plugin Runtime
**Version**: 0.3.0-alpha
**Status**: ✅ Complete
- Plugin loader and registry
- Capability negotiation (9 capabilities)
- Sandbox and permission model
- Hot reload support
- Service discovery
- Telemetry and diagnostics

### Sprint 4 — Workflow Runtime
**Version**: 0.4.0-alpha
**Status**: ✅ Complete
- Workflow manifest parsing and validation
- Immutable workflow graph (Kahn's algorithm)
- Deterministic execution engine
- 7 trigger types
- Plugin bridge integration
- Storage abstraction
- Metrics and health services

### Sprint 5 — IPC Runtime
**Version**: 0.5.0-alpha
**Status**: ✅ Complete
- Message envelope system
- Serialization (JSON, Binary, Structured)
- Transport layer (In-memory, Named Pipe, TCP, WebSocket)
- Router with rule engine
- Channel state machine
- Security (auth, authorization, audit, replay protection)
- Reliability (delivery guarantees, retry, DLQ)
- Command system
- Event bus
- Request/response correlation
- Session management
- Endpoint registry
- Capability negotiation
- Health and metrics
- Distributed tracing
- Plugin and workflow bridges

### Sprint 6 — Vision Runtime
**Version**: 0.6.0-alpha
**Status**: ✅ Complete
- Image acquisition and frame processing
- Computer vision pipeline engine
- Provider abstraction (OpenCV, PIL, etc.)
- Deterministic execution graph
- 11-stage composable pipeline
- 7 trigger types (Immediate, Interval, Frame, Workflow, AI, Event, Cron)
- LRU cache and temp buffer management
- 6-status health monitoring
- Distributed tracing

### Sprint 7 — AI Runtime
**Version**: 0.7.0-alpha
**Status**: ✅ Complete
- AI model inference and management layer
- Model Management (14 types), Provider Abstraction (plugin-based)
- Capability Negotiation (14 capabilities: Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime: deterministic execution with scheduler and executor
- Prompt Runtime: template compilation and execution
- Conversation Runtime: session management with history
- Memory Runtime: scoped storage (Session/Workspace/Project/Global)
- Embedding Runtime: vector index and store
- Agent Runtime: agent lifecycle and execution
- Tool Runtime: tool registry with permission model
- Core Services: AIRuntime (full lifecycle FSM), AIManager, AIContext, AISession, AIRuntimeManager
- Resource Management: LRU cache, temp buffers, leak prevention
- Metrics: latency, tokens, queue depth, memory histograms
- Health: 6-status monitoring (Healthy/Busy/Loading/Recovering/Degraded/Failed)
- Security: model/tool/prompt validation, provider isolation, sandbox
- Storage: abstract persistence (no DB dependency)
- Integration: IPC, Workflow, Vision bridges
- 35 Python source files, 105 tests, 174 exported symbols

### Sprint 8 — Knowledge Runtime
**Version**: 0.8.0-alpha
**Status**: ✅ Complete
- Knowledge pack system design and RFC specifications
- Document lifecycle: Create, Import, Update, Archive, Delete, Restore, Version
- Chunk processing with deterministic lifecycle
- Abstract index builder with no DB dependency
- Retrieval and search orchestrators
- Citation management with policy engine
- Provider abstraction (plugin-based factory)
- Unified KnowledgeRegistry
- Resource management (LRU cache, temp buffers, leak prevention)
- Health service (6 statuses)
- Security service (7 layers)
- Metrics collector (9 metric types)
- Integration bridges: IPC, AI, Vision, Workflow, Scheduler
- 15 module architecture: Common, Document, Chunk, Index, Retrieval, Search, Citation, Provider, Registry, Resource, Health, Security, Metrics, Integration, Runtime
- Frozen dataclass models with slots=True
- Dependency injection throughout, no global mutable state
- Platform-independent Python reference implementation design

---

## Upcoming Sprints

### Sprint 9 — Project Runtime
**Version**: 0.9.0-alpha
**Status**: ✅ Complete
- Project management and orchestration layer
- 16 subsystems implemented as Python Reference Implementation
- Workspace Runtime: Workspace, WorkspaceLifecycle, WorkspaceRegistry, WorkspaceManager
- Project Runtime: Project, ProjectLifecycle, ProjectRegistry, ProjectManager, ProjectContext, ProjectSession, ProjectRuntimeManager
- Asset Runtime: Asset, AssetLifecycle, AssetRegistry, AssetManager (10 asset types)
- Configuration Runtime: ConfigurationProfile, ConfigurationLayer (5 layers), ConfigurationManager
- Environment Runtime: Environment, EnvironmentProfile, EnvironmentManager
- Template Runtime: Template, TemplateDescriptor, TemplateManager (6 builtin templates)
- Build Runtime: BuildProfile, BuildConfiguration, BuildManager (abstract, no compiler)
- Hosting Layer: RuntimeHost, RuntimeHostingLayer (hosts 7 runtimes)
- Common: ProjectError hierarchy, EventType, frozen dataclasses
- Metrics: MetricsCollector (15 metric types)
- Health: HealthService (6 states)
- Security: SecurityService (isolation, validation)
- Events/IPC: EventBus, ProjectIPCBus (16 event types)
- Integration: Workflow/Vision/AI/Knowledge integration services
- Main Runtime: ProjectRuntime (coordinator)
- 57 Python source files, 11 test files, 432 tests, 36 RFC specs
- Quick start: from atlas_project import ProjectRuntime, ProjectDescriptor
### Sprint 10 — Cross-Runtime Integration
**Version**: 0.10.0-alpha
**Status**: ✅ Complete
- Integration Layer: RuntimeIntegrationManager, RuntimeGraph, RuntimeDependencyResolver
- RuntimeBootstrapper: Ordered startup with partial failure tolerance and restart
- RuntimeShutdownManager: Reverse-order shutdown with metrics flush and metadata persist
- RuntimeCoordinator: Full lifecycle management (register → start → stop → validate)
- CrossRuntimeEventRouter: Routes events across all 9 runtime event types with priority ordering
- ArchitectureValidator: Validates layering, forbidden imports, required modules
- PerformanceBenchmarks: Startup, shutdown, event latency, cross-runtime latency, plugin load time
- 99 new tests: Cross-Runtime (32), End-to-End (5), Lifecycle/Bootstrap/Shutdown (12), Health/Metrics (4), Event/Plugin/Workflow (10), Vision→Knowledge→AI Pipeline (4), Failure Recovery (5), Performance Benchmarks (10), Architecture (16)
- 774 tests passing (0 failures)
- Zero TODOs, zero placeholders, zero FIXMEs
- Zero forbidden imports, zero global mutable state
- Dependency injection throughout, immutable frozen dataclass models
- Deterministic topological ordering, platform-independent
- Integration Compliance Report with architecture validation, integration matrix, dependency matrix, scenario coverage
- Bug fix: Resolved 5 test file naming conflicts
### Sprint 11 — Cross Runtime Integration
**Version**: 0.11.0-alpha
**Status**: ⬜ Planned
- Unified event bus across all runtimes
- Cross-runtime service discovery
- Integrated health and metrics aggregation
- End-to-end workflow validation

### Sprint 12 — Performance & Stress
**Version**: 0.12.0-alpha
**Status**: ⬜ Planned
- Load testing and stress testing
- Memory optimization and leak detection
- Throughput benchmarks
- Latency profiling

### Sprint 13 — Desktop Shell
**Version**: 0.13.0-alpha
**Status**: ⬜ Planned
- Desktop integration layer
- System tray and notifications
- File association and handlers
- OS-level automation hooks

### Sprint 14 — Workflow Studio
**Version**: 0.14.0-alpha
**Status**: ⬜ Planned
- Visual workflow designer
- Drag-and-drop node editing
- Real-time execution preview
- Workflow versioning and sharing

### Sprint 15 — Vision Studio
**Version**: 0.15.0-alpha
**Status**: ⬜ Planned
- Visual element recognition editor
- Template matching studio
- Camera calibration tools
- Vision pipeline composer

### Sprint 16 — AI Studio
**Version**: 0.16.0-alpha
**Status**: ⬜ Planned
- Model selection and comparison
- Prompt engineering workspace
- Agent behavior editor
- Capability negotiation visualizer

### Sprint 17 — Marketplace
**Version**: 0.17.0-alpha
**Status**: ⬜ Planned
- Plugin marketplace
- Knowledge pack distribution
- Provider marketplace
- Rating and review system

### Sprint 18 — Beta
**Version**: 0.x.x-beta
**Status**: ⬜ Planned
- All Runtime modules implemented
- API freeze
- Focus on stability and performance
- Community beta testing

---

## Future Milestones

### RC Phase
- Conformance tests pass
- No blocking bugs
- Documentation complete

### Stable Release
- All acceptance criteria met
- Production-ready
- Long-term support plan

---

## Long-term Vision

Build automation that understands intent instead of recording coordinates.

- Local AI first
- Extensible plugin ecosystem
- Cross-platform runtime
- Vision-based interaction
- Knowledge-driven workflows
- Marketplace for plugins and knowledge packs
