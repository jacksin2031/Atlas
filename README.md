# Atlas

> Record Once. Understand Forever.

Atlas is an open-source AI-powered automation platform designed to automate desktop applications, games, and workflows through computer vision, local AI, and extensible plugins.

## Vision

Build automation that understands intent instead of recording coordinates.

## Goals

- AI Workflow Generation
- Vision-based Automation
- Knowledge Packs
- Plugin Ecosystem
- Marketplace
- Local AI First

## Current Status

| Attribute | Value |
|---|---|
| **Version** | 0.7.0-alpha |
| **Latest Sprint** | Sprint 7 — AI Runtime |
| **Next Sprint** | Sprint 8 — Knowledge Runtime |
| **Total Packages** | 14 (Rust + Python) |
| **Test Cases** | 702+ |
| **RFCs Implemented** | 56 (Runtime + IPC + Plugin) |
| **License** | Apache 2.0 |

## Implemented Modules

### Runtime Foundation (Sprint 1)
- Service Registry
- Event Bus
- Scheduler
- State Management
- Runtime Lifecycle (FSM)
- Error Taxonomy
- Capability Registry
- Contract System
- Manifest Specification

### Runtime Infrastructure (Sprint 2)
- Resource Management (LRU cache)
- Health Monitoring (6-status)
- Metrics Collection (Counter, Gauge, Histogram)
- Security Framework (10 permissions)
- Storage Backend Abstraction

### Plugin Runtime (Sprint 3)
- Plugin Loader and Registry
- Capability Negotiation (9 capabilities)
- Sandbox and Permission Model
- Hot Reload Support
- Service Discovery
- Telemetry and Diagnostics

### IPC Runtime (Sprint 5)
- Message Envelope System
- Serialization (JSON, Binary, Structured)
- Transport Layer (In-memory, Named Pipe, TCP, WebSocket)
- Router with Rule Engine
- Channel State Machine
- Security (Auth, Authorization, Audit, Replay Protection)
- Reliability (Delivery Guarantees, Retry, DLQ)
- Command System
- Event Bus
- Request/Response Correlation
- Session Management
- Endpoint Registry
- Distributed Tracing

### Vision Runtime (Sprint 6)
- Frame Model (12 frozen dataclasses)
- Capture Sources and Provider ABC
- 11-stage Deterministic Pipeline
- 6 Registries (Vision, Provider, Pipeline, Capture, Model, Capability)
- Graph Execution (Kahn's algorithm)
- 7 Trigger Types Scheduler
- LRU Cache and Temp Buffer Management
- Metrics (Counter, Gauge, Histogram p50/p95/p99)
- Health (6-status)
- Security (10 permissions)
- Storage Abstraction (5 domains)
- Integration Bridges (IPC, Workflow, Plugin)
- 185 test cases

### AI Runtime (Sprint 7)
- Model Management (14 types)
- Provider Abstraction (plugin-based factory)
- Capability Negotiation (14 capabilities: Chat, Completion, Embedding, Vision, Audio, Image, Tool Calling, Structured Output, Streaming, Batch, Fine Tuning, RAG, Memory, Reasoning)
- Inference Runtime (deterministic execution)
- Prompt Runtime (template compilation)
- Conversation Runtime (session + history)
- Memory Runtime (scoped: Session/Workspace/Project/Global)
- Embedding Runtime (vector index/store)
- Agent Runtime (lifecycle + execution)
- Tool Runtime (registry + permissions)
- Core Services (AIRuntime, AIManager, AIContext, AISession)
- Resource Management (LRU cache, temp buffers, leak prevention)
- Metrics (latency, tokens, queue depth, memory histograms)
- Health (6-status: Healthy/Busy/Loading/Recovering/Degraded/Failed)
- Security (model/tool/prompt validation, sandbox enforcement)
- Storage (abstract persistence — no DB dependency)
- Integration (IPCAIBridge, WorkflowAIBridge, VisionAIBridge)
- 105 test cases, 174 exported symbols

## Architecture

```
Atlas Platform
├── Runtime Foundation (RFC-0001–0014) ✅
├── IPC Runtime (RFC-0101–0112) ✅
├── Plugin Runtime (RFC-0201–0230) ✅
├── AI Runtime (Sprint 7) ✅
├── Vision Runtime (Sprint 6) ✅
├── Workflow Runtime (RFC-0301–0333) ⬜
├── Storage Runtime (RFC-0401–0425) ⬜
├── Knowledge Runtime (Sprint 8) ⬜
└── Project Runtime (Sprint 9) ⬜
```

## Quick Start

### Prerequisites
- Rust 1.75+ (edition 2021)
- Python 3.10+ (for reference implementations)

### Build
```bash
cargo build
cargo test
```

### Run Tests
```bash
cargo test --all
cd packages/vision && pytest
cd packages/ai && pytest
```

## Repository Structure

```
Atlas/
├── packages/           # Source packages
│   ├── common/         # Shared Rust types
│   ├── contracts/      # Runtime contracts
│   ├── runtime/        # Core runtime (Rust)
│   ├── plugin/         # Plugin runtime (Rust)
│   ├── ipc/            # IPC runtime (Rust)
│   ├── storage/        # Storage abstraction (Rust)
│   ├── workflow/       # Workflow specs (Python ref)
│   ├── vision/         # Vision runtime (Python ref)
│   └── ai/             # AI runtime (Python ref)
├── specs/              # RFC specifications
│   ├── runtime/        # RFC-0001–0014
│   ├── ipc/            # RFC-0101–0112
│   ├── plugin/         # RFC-0201–0230
│   ├── workflow/       # RFC-0301–0333
│   ├── storage/        # RFC-0401–0425
│   └── common/         # RFC-1001–1006
├── docs/               # Architecture docs
├── .ai/                # AI agent skills
└── Cargo.toml          # Workspace manifest
```

## Documentation

- [VERSIONING.md](VERSIONING.md) — Version policy
- [RELEASE.md](RELEASE.md) — Release procedure
- [PROJECT_STATUS.md](PROJECT_STATUS.md) — Project status dashboard
- [ROADMAP.md](ROADMAP.md) — Sprint roadmap
- [CHANGELOG.md](CHANGELOG.md) — Release history
- [specs/RFC_INDEX.md](specs/RFC_INDEX.md) — RFC registry
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — Architecture docs

## License

Apache 2.0
