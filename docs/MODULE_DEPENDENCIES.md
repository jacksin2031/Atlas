# Atlas Module Dependencies

> **Last Updated**: 2026-08-24
> **Owner**: Atlas Architecture Board

---

## Dependency Hierarchy

Atlas follows a strict layered dependency model. Lower layers do NOT depend on upper layers.

`
┌─────────────────────────────────────────────────────┐
│                    Desktop UI                        │
├─────────────────────────────────────────────────────┤
│           Marketplace  │  Workflow Studio            │
├─────────────────────────────────────────────────────┤
│                 Atlas Runtime                       │
├──────────┬──────────┬──────────┬──────────┬─────────┤
│  Plugin  │   IPC    │  Vision  │   AI     │Knowledge│
├──────────┴──────────┴──────────┴──────────┴─────────┤
│              Core Foundation                        │
├─────────────────────────────────────────────────────┤
│  Runtime │ Contracts │ Common │ Events │ Errors     │
└─────────────────────────────────────────────────────┘
`

---

## Layer Definitions

### Layer 0: Core Foundation
**No dependencies on any other layer.**

- packages/common — Shared types (events, errors, state, health, metrics, scheduler)
- packages/contracts — Runtime contracts (lifecycle, service, event bus, scheduler, health, metrics, storage)
- packages/runtime — Core runtime (service registry, event bus, scheduler, state, resource management)

**Depended on by**: All other layers.

---

### Layer 1: Plugin System
**Depends on**: Core Foundation

- packages/plugin — Plugin lifecycle, capability negotiation, sandbox, registry, hot reload

**Depends on**: Runtime, Contracts, Common

**Provided to**: IPC, Workflow, Vision, AI, Knowledge, Marketplace

---

### Layer 2: IPC
**Depends on**: Core Foundation, Plugin

- packages/ipc — Message routing, security, reliability, serialization, tracing

**Depends on**: Plugin, Runtime, Contracts

**Provided to**: Workflow, Vision, AI, Knowledge

---

### Layer 3: Workflow
**Depends on**: Core Foundation, Plugin, IPC

- src/atlas_workflow — Manifest parsing, immutable graph execution, scheduling, events, Node Registry, and persistent Desktop host
- packages/workflow — package landing documentation; the current Python implementation is `src/atlas_workflow`

**Depends on**: Runtime, Plugin, IPC, Contracts

**Provided to**: Vision, AI, Knowledge, Desktop Shell

---

### Layer 4: Vision
**Depends on**: Core Foundation, Plugin, IPC, Workflow

- packages/vision — Frame processing, pipeline execution, provider abstraction

**Depends on**: Runtime, Plugin, IPC, Contracts

**Provided to**: AI, Knowledge, Workflow Studio, Vision Studio

---

### Layer 5: AI
**Depends on**: Core Foundation, Plugin, IPC, Workflow, Vision

- packages/ai — Model management, inference, prompts, conversations, agents, tools

**Depends on**: Runtime, Plugin, IPC, Contracts

**Provided to**: Knowledge, AI Studio, Marketplace

---

### Layer 6: Knowledge
**Depends on**: Core Foundation, Plugin, IPC, Workflow, Vision, AI

- packages/knowledge — Document lifecycle, chunking, indexing, retrieval, search, citations

**Depends on**: Runtime, Plugin, IPC, Contracts

**Provided to**: Project Runtime, Marketplace

---

### Layer 7: Project
**Depends on**: All previous layers

- packages/project — Project management, workspace boundaries, configuration

**Depends on**: Runtime, Plugin, IPC, Workflow, Vision, AI, Knowledge

**Provided to**: Desktop Shell, Marketplace

---

## Forbidden Dependencies

### Layer 8 Studio boundary

- `apps/atlas-desktop/src/studio/vision/components` depends only on Vision UI stores, UI services, shared desktop components, and the IPC bridge.
- `apps/atlas-desktop/src/studio/ai` depends only on AI UI contracts/state/services, shared desktop infrastructure, Vision frame-reference state, and the typed IPC bridge. It must not import the Python AI Runtime.
- `apps/atlas-desktop/src/studio/workflow` depends only on Workflow UI contracts/stores/services and the typed IPC bridge. It must not import or execute the Python Workflow Runtime.
- `apps/atlas-desktop/src-tauri` owns the process boundary and may launch `packages/ai` as a long-running host; JSON-lines command responses and `ai://runtime-event` payloads are the only Desktop-to-Python integration contract.
- `apps/atlas-desktop/src-tauri` also owns the persistent `atlas_workflow.host` process boundary. Workflow JSON-lines responses, bridge requests, and `workflow://runtime-event` payloads are the Desktop-to-Workflow-Python contract.
- Workflow AI nodes call the existing Tauri AI host manager; Vision nodes call the existing native capture boundary; Plugin nodes execute through the Workflow Runtime Node Registry and Plugin Bridge.
- Concrete provider HTTP/SSE/NDJSON transport belongs to the Python host. React and Rust must not receive or persist provider credentials.
- Vision React components must not import `packages/vision` or a concrete provider/runtime implementation.
- FlexLayout depends on panel identifiers and component factories only; it contains no studio business state.
- Workflow, Vision, and AI panel content may share shell panels, but a layout may contain each stable panel component ID at most once.

The following dependencies are **explicitly forbidden**:

| From | To | Reason |
|---|---|---|
| Core Foundation | Plugin | Circular dependency |
| Plugin | IPC | IPC depends on Plugin |
| IPC | Plugin | Already covered |
| Workflow | Vision | Different domains |
| Vision | AI | Different domains |
| AI | Knowledge | Knowledge is higher layer |
| Any upper layer | Desktop UI | UI is presentation, not runtime |

---

## Dependency Graph (Mermaid)

`mermaid
graph TD
    Core[Core Foundation] --> Plugin[Plugin System]
    Core --> Runtime[Core Runtime]
    Plugin --> IPC[IPC Runtime]
    Runtime --> IPC
    IPC --> Workflow[Workflow Runtime]
    Plugin --> Workflow
    Runtime --> Workflow
    IPC --> Vision[Vision Runtime]
    Plugin --> Vision
    Runtime --> Vision
    Workflow --> Vision
    IPC --> AI[AI Runtime]
    Plugin --> AI
    Runtime --> AI
    Workflow --> AI
    Vision --> AI
    IPC --> Knowledge[Knowledge Runtime]
    Plugin --> Knowledge
    Runtime --> Knowledge
    Workflow --> Knowledge
    Vision --> Knowledge
    AI --> Knowledge
    Knowledge --> Project[Project Runtime]
    Plugin --> Project
    Runtime --> Project
`

---

## Governance

Changes to this dependency model require Architecture Board approval and an RFC update.

---
### Layer 8: Desktop UI
**Depends on**: All previous layers

- apps/atlas-desktop — Tauri 2 + React 19 + TypeScript + Vite 7 + Zustand

**Depends on**: Runtime, Plugin, IPC, Workflow, Vision, AI, Knowledge, Project

**Provides to**: None (presentation layer only)
