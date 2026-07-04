# Atlas Roadmap

> **Last Updated**: 2026-07-04
> **Current Version**: 0.7.0-alpha
> **Current Sprint**: Sprint 7 (AI Runtime)
> **Next Milestone**: Sprint 8 — Knowledge Runtime

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
- Immutable workflow graph (Kahn\'s algorithm)
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

---

## Upcoming Sprints

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
**Status**: ⬜ Upcoming
- Knowledge pack system
- Semantic search
- Vector embeddings
- Knowledge graph

### Sprint 9 — Project Runtime
**Version**: 0.9.0-alpha
**Status**: ⬜ Planned
- Project management
- Workspace boundaries
- Hierarchical configuration
- Multi-project orchestration

### Sprint 10 — Conformance Tests
**Version**: 0.10.0-alpha
**Status**: ⬜ Planned
- Cross-runtime integration tests
- Protocol conformance validation
- Performance benchmarks
- Security audit

---

## Future Milestones

### Beta Transition
- All Runtime modules implemented
- API freeze
- Focus on stability and performance

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


