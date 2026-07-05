# Atlas Architecture Decisions Summary

> **Purpose**: One-page overview of the design decisions that define Atlas.
> **Audience**: New contributors, reviewers, stakeholders.
> **Last Updated**: 2026-07-05
> **Owner**: Atlas Architecture Board

---

## The Big Picture

Atlas is a **multi-runtime automation platform**. Seven runtimes (Plugin, IPC, Workflow, Vision, AI, Knowledge, Project) are hosted inside a unified **Project Runtime** that manages workspaces, assets, configuration, and the hosting layer.

```
Desktop UI / CLI
       │
  ┌────┴────┐
  │  Project │ ← Workspace, Asset, Config, Template, Build
  │ Runtime  │
  └────┬────┘
       │ hosts
  ┌────┼─────────────────────────────────────────┐
  │    │    │    │    │    │    │                │
Plugin IPC Workflow Vision  AI Knowledge  …      │
Runtime Runtime Runtime Runtime Runtime Runtime  │
  │    │    │    │    │    │    │                │
  └────┴────┴────┴────┴────┴────┘                │
                                                 │
                                        Hosting Layer
                                        (RuntimeHost)
```

---

## Ten Core Design Decisions

### 1. Project Hosts All Runtimes
The **Project Runtime** is the top-level coordinator. It owns the workspace boundary and hosts every other runtime (Plugin, IPC, Workflow, Vision, AI, Knowledge) via the `RuntimeHostingLayer`. Runtimes are never standalone — they always belong to a project context.

### 2. Everything is Runtime
Every subsystem follows the same lifecycle FSM:
`CREATED → INITIALIZING → READY → RUNNING → SHUTTING_DOWN → TERMINATED`
Each runtime has its own health monitor, metrics collector, and service contract. This uniformity lets you reason about any subsystem the same way.

### 3. Everything is Plugin
All extensibility points use the **Provider Plugin** pattern. Providers are discovered at runtime via capability negotiation, can be hot-swapped, and are isolated by a security sandbox. OpenAI → local LLM, OpenCV → PIL — zero restart needed.

### 4. Everything is Event
Subsystem communication goes through an **immutable event bus**. Events are versioned, persisted for replay, and delivered asynchronously. No direct method calls between runtimes — only events.

### 5. Everything is Deterministic
Every computation produces **reproducible results**:
- Topological sort with sorted insertion (no hash-dependent ordering)
- Frozen dataclasses with `slots=True`
- Zero global mutable state
- Dependency injection throughout
- Deterministic execution guaranteed

### 6. Contracts First
All interfaces are defined by **versioned RFCs** before any code is written. Contracts define input/output shapes, enable cross-language interoperability (Rust ↔ Python), and are tested for compliance via automated reports.

### 7. Provider Pattern
All external dependencies are abstracted behind a **Provider ABC**. A provider registry discovers implementations, negotiates capabilities, and selects the right one at runtime. This makes the system swappable and testable.

### 8. Dependency Injection
Every component receives its dependencies via constructor injection (`Arc<T>`). No singletons, no globals. This eliminates hidden coupling and makes unit testing trivial.

### 9. Python Reference → Rust Production
- **Python** (`src/atlas_*`) is the reference implementation. Fast to prototype, readable, fully testable.
- **Rust** (`packages/`) is the production runtime. Memory-safe, zero-cost abstraction, compiled.
Both share the same RFC contracts. They are interoperable via the IPC layer.

### 10. Storage Abstraction
No runtime talks directly to a database. All persistence goes through a **Storage Backend ABC** with domain-specific adapters (PromptStorage, ConversationStorage, DocumentStorage…). Swap SQLite for PostgreSQL by implementing one interface.

---

## Cross-Cutting Concerns

| Concern | Mechanism | Status |
|---------|-----------|--------|
| **Lifecycle** | FSM (6 states) | Implemented in all 7 runtimes |
| **Health** | 6-state health service | Implemented in all runtimes |
| **Metrics** | Counter, Gauge, Histogram (p50/p95/p99) | Implemented in all runtimes |
| **Security** | Permission model, sandbox, validation | Implemented in all runtimes |
| **Error Handling** | Typed error hierarchy per runtime | Implemented in all runtimes |
| **Events** | Immutable, versioned, persisted | Implemented in all runtimes |
| **Integration** | Bridge services (IPC, Vision, AI, Workflow) | Implemented in all runtimes |

---

## Forbidden Dependencies

```
Project Runtime (top)
  ↓ depends on
Workflow Runtime
  ↓ depends on
Vision Runtime
  ↓ depends on
AI Runtime
  ↓ depends on
Knowledge Runtime
  ↓ depends on
IPC Runtime
  ↓ depends on
Plugin Runtime
  ↓ depends on
Runtime Foundation (bottom)
```

**Rules:**
- A layer may only depend on layers below it.
- No cross-dependencies between sibling runtimes.
- No runtime may depend on the Project Runtime.
- Circular dependencies are **forbidden** (enforced by CI).

---

## Quick Reference

| Question | Answer |
|----------|--------|
| How do I add a new capability? | Define an RFC contract → implement a Provider → register it → negotiate at runtime |
| How do I debug a runtime? | Check health service (6 states) → inspect metrics → replay events from bus |
| How do I swap an implementation? | Implement the Provider ABC → register it → capability negotiation picks the right one |
| How do I test a component? | Inject mocks via constructor → no globals → pure unit tests |
| How do I cross languages? | Define RFC contract in Python → implement in Rust (or vice versa) → IPC bridges them |

---

*For detailed principles, see [docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md).*
*For the full specification index, see [specs/RFC_INDEX.md](specs/RFC_INDEX.md).*
