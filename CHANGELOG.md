# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](VERSIONING.md).

---

## [Unreleased]

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
