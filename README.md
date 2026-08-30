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
| **Version** | 0.15.0-alpha |
| **Current Focus** | Sprint 15 frozen; preparing Sprint 16 Marketplace |
| **Implemented Packages** | 6 Rust workspace crates, 3 Python runtimes, 1 desktop app |
| **Automated Tests** | 1,074 passing in the Sprint 15 freeze |
| **Specification Status** | RFCs are present across the planned runtimes; implementation coverage varies |
| **License** | Apache 2.0 |

## Architecture

```
            Desktop Shell (Tauri 2 + React)
                 │
      ┌──────────┴──────────┐
      │                     │
 Marketplace         Workflow Studio
      │                     │
      └──────────┬──────────┘
                 │
          Atlas Runtime
                 │
 ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐
 │Plugin│IPC│Vision│AI│Knowledge│Project│Desktop│
 └─────┴─────┴─────┴─────┴─────┴─────┴─────┘
```

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

### Knowledge Runtime (Sprint 8)
- RFC specifications and architecture documentation are present.
- The `packages/knowledge` implementation and its previously reported 247 tests are not present in this snapshot.

### Project Runtime (Sprint 9)
- RFC specifications and architecture documentation are present.
- A `packages/project` implementation and its previously reported 432 tests are not present in this snapshot.

## Quick Start

### Prerequisites
- Rust 1.75+ (edition 2021)
- Python 3.10+ (for reference implementations)

### Build

```bash
cargo build --workspace
cd apps/atlas-desktop
pnpm install
pnpm run build
pnpm tauri build --debug --no-bundle
```

### Run Tests

```bash
cargo test --workspace --all-targets
PYTHONPATH=src python -m pytest
PYTHONPATH=packages/vision/src python -m pytest packages/vision/tests
PYTHONPATH=packages/ai/src python -m pytest packages/ai/tests
cd apps/atlas-desktop && pnpm test
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
│   ├── workflow/       # Workflow specifications; Python code is under src/
│   ├── vision/         # Vision runtime (Python ref)
│   ├── ai/             # AI runtime (Python ref)
│   └── knowledge/      # Knowledge specifications placeholder
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
- [docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md) — Design philosophy
- [docs/MODULE_DEPENDENCIES.md](docs/MODULE_DEPENDENCIES.md) — Module dependency map


## GitHub Infrastructure

- [.github/](.github/) — GitHub configuration
  - [CODEOWNERS](.github/CODEOWNERS) — PR review assignment rules
  - [workflows/](.github/workflows/) — CI/CD pipelines
  - [ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) — Issue templates
  - [PULL_REQUEST_TEMPLATE/](.github/PULL_REQUEST_TEMPLATE/) — PR checklist
- [docs/github/GITHUB_INFRASTRUCTURE.md](docs/github/GITHUB_INFRASTRUCTURE.md) — Complete GitHub infrastructure documentation
- [SECURITY.md](SECURITY.md) — Security policy and vulnerability reporting

## Implemented Modules (Continued)

### Cross-Runtime Integration (Sprint 10)
- Cross-runtime integration RFCs and design documentation are present.
- The previously reported standalone implementation and 99 tests are not present in this snapshot.

### Conformance & Architecture Validation (Sprint 11)
- Conformance Runtime: 13 modules (Core Models, Scanners, Validators, Contracts, Service, CLI, Benchmark)
- ArchitectureValidator: 9 rules (layering, dependency direction, circular deps, forbidden imports, provider pattern, DI, immutable models, runtime contracts, project hosting)
- RFCValidator: 121 RFCs scanned, 18 implemented
- ADRValidator: 12 ADRs parsed, 11 referenced
- DocumentationValidator: 13/13 docs present (100%)
- 52 conformance tests passing, 0 warnings, 0 errors
- CLI entry point: `atlas-conformance`
- Generated reports: CONFORMANCE_REPORT.md, conformance_report.json

### Desktop Shell (Sprint 12, alpha)
- **Tauri 2 + React 19 + TypeScript + Vite 7** — alpha desktop foundation
- **Menu System**: Menu Bar, Toolbar, Status Bar, Command Palette
- **Dockable Panels**: Project Explorer, Runtime Monitor, Output, Console, Logs, Extensions, Settings, Problems, Notifications
- **Runtime Monitor**: Live dashboard for 8 runtimes (Workflow, Vision, AI, Knowledge, Plugin, IPC, Project, Storage)
- **Theme Manager**: Dark/Light/System theme support with live switching
- **Layout Manager**: Docking, resizable panels, persistence, reset
- **Plugin Support**: Extension Manager with search, status, health indicators
- **Logging**: Real-time logs, filtering, export, search
- **Project Support**: Open/Close/Recent projects, workspace management, settings
- **Command Palette**: Quick commands, fuzzy search, recent commands, keyboard shortcuts
- **Architecture Layer 8** — desktop foundation under active stabilization
## License

Apache 2.0

| **Current Focus** | Sprint 15.2 Workflow Execution Integration; live-provider acceptance pending |
| **Desktop Shell** | apps/atlas-desktop/ — Alpha GUI with Tauri 2 + React |

### Desktop Shell (Sprint 12, alpha)
- Tauri 2 + React 19 + TypeScript + Vite 7
- Menu Bar, Toolbar, Status Bar, Command Palette
- Dockable panels: Project Explorer, Runtime Monitor, Output, Console, Logs, Extensions, Settings, Problems, Notifications
- Runtime Monitor: 8 runtimes (Workflow, Vision, AI, Knowledge, Plugin, IPC, Project, Storage)
- Theme Manager: Dark/Light/System
- Layout Manager: Docking, resizable panels, persistence, reset
- Plugin Support: Extension Manager with search, status, health
- Logging: Real-time logs, filtering, export, search
- Project Support: Open/Close/Recent projects, workspace, settings
- Command Palette: Quick commands, search, recent commands, keyboard shortcuts

### Vision Studio (Sprint 14, alpha)
- Separate Vision workspace alongside Workflow Studio
- FlexLayout docking with persisted, recoverable per-workspace layouts
- Image loading, pan/zoom canvas, grid/rulers, editable overlays, and properties
- OCR, detection, color, template, and timeline panels behind UI service / IPC boundaries
- Frontend, browser, Vision runtime, and Tauri MSVC verification pass

### Workflow Execution Integration (Sprint 15.2, alpha)
- Canonical graph serialization and validation through the existing Workflow Runtime
- Persistent Tauri/Python host and nine native workflow lifecycle commands
- Real port-to-port values, deterministic DAG order, conditional branch skipping, variables, cancellation, pause/resume, step, restart, results, history, and metrics
- Runtime-driven canvas, edge, debugger, variable, Output, and Properties state
- Core, AI bridge, Vision bridge, and deterministic Plugin Bridge node boundaries
- Browser mode explicitly reports Runtime unavailable; simulation remains separate
