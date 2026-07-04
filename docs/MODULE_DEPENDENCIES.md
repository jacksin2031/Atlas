# Atlas Module Dependencies

> **Last Updated**: 2026-07-04
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

- packages/workflow — Manifest parsing, graph execution, scheduling, recovery

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
