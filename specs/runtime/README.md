# Atlas Runtime Specification Suite

> **Status**: Frozen  
> **Version**: 1.0.0  
> **Last Updated**: 2026-06-30  
> **Owner**: Runtime Architecture Board  

---

## Navigation

This directory contains the complete Runtime specification suite for Project Atlas.  
Read in the order listed below. Each specification is self-contained but cross-references others.

### Core Runtime Specifications

| # | RFC | Title | Status | Lines |
|---|-----|-------|--------|-------|
| 1 | [RFC-0001](specs/runtime/RFC-0001-runtime-overview.md) | Runtime Overview | Frozen | 342 |
| 2 | [RFC-0002](specs/runtime/RFC-0002-runtime-lifecycle.md) | Runtime Lifecycle | Frozen | 906 |
| 3 | [RFC-0003](specs/runtime/RFC-0003-runtime-service-model.md) | Runtime Service Model | Frozen | 518 |
| 4 | [RFC-0004](specs/runtime/RFC-0004-runtime-scheduler.md) | Runtime Scheduler | Frozen | 445 |
| 5 | [RFC-0005](specs/runtime/RFC-0005-runtime-eventbus.md) | Runtime Event Bus | Frozen | 450 |
| 6 | [RFC-0006](specs/runtime/RFC-0006-runtime-state.md) | Runtime State Management | Frozen | 488 |
| 7 | [RFC-0007](specs/runtime/RFC-0007-runtime-ipc.md) | Runtime IPC Architecture | Frozen | 454 |
| 8 | [RFC-0008](specs/runtime/RFC-0008-runtime-plugin.md) | Runtime Plugin Host | Frozen | 482 |
| 9 | [RFC-0009](specs/runtime/RFC-0009-runtime-resource.md) | Runtime Resource Management | Frozen | 486 |
| 10 | [RFC-0010](specs/runtime/RFC-0010-runtime-manifest.md) | Runtime Manifest Specification | Frozen | 481 |
| 11 | [RFC-0011](specs/runtime/RFC-0011-runtime-errors.md) | Runtime Error Taxonomy | Frozen | 302 |
| 12 | [RFC-0012](specs/runtime/RFC-0012-runtime-capability.md) | Runtime Capability Registry | Frozen | 290 |
| 13 | [RFC-0013](specs/runtime/RFC-0013-runtime-contracts.md) | Runtime Contracts | Frozen | 398 |
| 14 | [RFC-0014](specs/runtime/RFC-0014-runtime-reference-architecture.md) | Runtime Reference Architecture | Frozen | TBD |

**Total**: 14 RFCs, 6,500+ lines of normative specification.

---

## Reading Order

The Runtime specifications are organized in dependency order.  
Follow this reading path for complete understanding:

`
┌─────────────────────────────────────────────────────────┐
│                    LEVEL 0: FOUNDATION                    │
├─────────────────────────────────────────────────────────┤
│  RFC-0001  Runtime Overview                             │
│  └─ What is Atlas Runtime? Architecture principles      │
│     Invariants, boundaries, responsibilities             │
└─────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│     LEVEL 1: CORE        │   │     LEVEL 1: CORE        │
├──────────────────────────┤   ├──────────────────────────┤
│ RFC-0002 Runtime         │   │ RFC-0003 Runtime         │
│     Lifecycle State      │   │     Service Model        │
│     Machine              │   │     Registry             │
│     Transitions          │   │     Dependency Injection │
└──────────────────────────┘   └──────────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────┐
│                   LEVEL 2: EXECUTION                      │
├─────────────────────────────────────────────────────────┤
│  RFC-0004  Runtime Scheduler          (Execution)        │
│  RFC-0005  Runtime Event Bus            (Messaging)      │
│  RFC-0006  Runtime State Management     (Persistence)    │
│  RFC-0009  Runtime Resource Management  (Quotas)         │
└─────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│   LEVEL 3: COMMUNICATION │   │   LEVEL 3: EXTENSIBILITY │
├──────────────────────────┤   ├──────────────────────────┤
│ RFC-0007 Runtime         │   │ RFC-0008 Runtime         │
│     IPC Architecture     │   │     Plugin Host          │
│     Message Schema       │   │     Sandbox Model        │
│     Contract Verification│   │     WASM Runtime         │
└──────────────────────────┘   └──────────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────┐
│                  LEVEL 4: METADATA                        │
├─────────────────────────────────────────────────────────┤
│  RFC-0010  Runtime Manifest Specification (Config)       │
│  RFC-0012  Runtime Capability Registry   (Features)      │
│  RFC-0011  Runtime Error Taxonomy        (Errors)        │
└─────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│   LEVEL 5: CONTRACTS     │   │   LEVEL 5: REFERENCE     │
├──────────────────────────┤   ├──────────────────────────┤
│ RFC-0013 Runtime         │   │ RFC-0014 Runtime         │
│     Contracts            │   │     Reference Architecture│
│     Service Interface    │   │     Block Diagram        │
│     IPC Schema           │   │     Sequence Diagram     │
│     Event Schema         │   │     Dependency Graph     │
│     State Schema         │   │     Data Flow            │
└──────────────────────────┘   └──────────────────────────┘
`

---

## Architecture Layers

### Layer 0: Foundation
- **RFC-0001** Runtime Overview
- Defines the Runtime as a whole
- Responsibility boundaries, invariants, principles
- Reference architecture overview

### Layer 1: Core
- **RFC-0002** Runtime Lifecycle
  - State machine, transitions, boot/shutdown, recovery
  - Dependencies: RFC-0001
- **RFC-0003** Runtime Service Model
  - Service registry, dependency injection, lifecycle contracts
  - Dependencies: RFC-0001, RFC-0002

### Layer 2: Execution
- **RFC-0004** Runtime Scheduler
  - Task queues, worker pools, priority dispatch
  - Dependencies: RFC-0001, RFC-0002, RFC-0003, RFC-0005
- **RFC-0005** Runtime Event Bus
  - Publish-subscribe, priority queues, delivery guarantees
  - Dependencies: RFC-0001, RFC-0002, RFC-0003
- **RFC-0006** Runtime State Management
  - Transactions, WAL, snapshots, conflict resolution
  - Dependencies: RFC-0001 through RFC-0005
- **RFC-0009** Runtime Resource Management
  - CPU/GPU/memory quotas, throttling, eviction
  - Dependencies: RFC-0001 through RFC-0006

### Layer 3: Communication & Extensibility
- **RFC-0007** Runtime IPC Architecture
  - Inter-process messaging, contract verification, security
  - Dependencies: RFC-0001, RFC-0002, RFC-0003, RFC-0005
- **RFC-0008** Runtime Plugin Host
  - Sandbox isolation, WASM runtime, plugin lifecycle
  - Dependencies: RFC-0001 through RFC-0007, RFC-0009

### Layer 4: Metadata
- **RFC-0010** Runtime Manifest Specification
  - Configuration schema, capability declarations, version negotiation
  - Dependencies: RFC-0001, RFC-0002, RFC-0003, RFC-0005
- **RFC-0012** Runtime Capability Registry
  - System capabilities, entitlement verification, status maps
  - Dependencies: RFC-0001, RFC-0002, RFC-0010
- **RFC-0011** Runtime Error Taxonomy
  - Error classifications, error codes, recovery paths
  - Dependencies: RFC-0001, RFC-0002

### Layer 5: Contracts & Reference
- **RFC-0013** Runtime Contracts
  - Consolidated interface signatures, JSON schemas, serialization
  - Dependencies: All Runtime RFCs (RFC-0001 through RFC-0012)
- **RFC-0014** Runtime Reference Architecture
  - Large block diagram, sequence diagrams, data flow, thread model
  - Dependencies: All Runtime RFCs

---

## Cross-Reference Map

### By Concern

| Concern | Primary RFC(s) | Supporting RFC(s) |
|---|---|---|
| **Lifecycle** | RFC-0002 | RFC-0011 (errors), RFC-0005 (events) |
| **Services** | RFC-0003 | RFC-0013 (contracts), RFC-0012 (capabilities) |
| **Scheduling** | RFC-0004 | RFC-0009 (resources), RFC-0005 (events) |
| **Messaging** | RFC-0005 | RFC-0007 (IPC), RFC-0013 (schemas) |
| **State** | RFC-0006 | RFC-0009 (resources), RFC-0013 (schemas) |
| **IPC** | RFC-0007 | RFC-0008 (plugins), RFC-0013 (schemas) |
| **Plugins** | RFC-0008 | RFC-0009 (resources), RFC-0010 (manifest) |
| **Resources** | RFC-0009 | RFC-0004 (scheduling), RFC-0008 (plugins) |
| **Manifest** | RFC-0010 | RFC-0012 (capabilities), RFC-0008 (plugins) |
| **Capabilities** | RFC-0012 | RFC-0010 (manifest), RFC-0009 (resources) |
| **Errors** | RFC-0011 | RFC-0002 (lifecycle), RFC-0008 (plugins) |
| **Contracts** | RFC-0013 | All RFCs (normative references) |
| **Reference** | RFC-0014 | All RFCs (diagrams) |

### By Audience

| Audience | Read First | Then Read |
|---|---|---|
| **Runtime Developer** | RFC-0001 | RFC-0002, RFC-0003, RFC-0013 |
| **Plugin Developer** | RFC-0001, RFC-0008 | RFC-0007, RFC-0010, RFC-0012 |
| **Integration Engineer** | RFC-0001, RFC-0007 | RFC-0005, RFC-0013 |
| **Architect Reviewer** | RFC-0001, RFC-0014 | RFC-0002 through RFC-0013 |
| **QA Engineer** | RFC-0013 | RFC-0001 through RFC-0012 (acceptance criteria) |

---

## Specification Status

| Status | Meaning |
|---|---|
| **Draft** | Under active design and community review |
| **Review** | Reviewing by core maintainers |
| **Accepted** | Approved specification, ready for or in implementation |
| **Frozen** | Architecture complete. Only bug fixes and clarifications allowed |
| **Superseded** | Replaced by a newer specification |

**Current Runtime Status**: All 14 RFCs are **Frozen**.

---

## Governance

- **Owner**: Runtime Architecture Board
- **Change Process**: Any change to Frozen RFCs requires:
  1. Architecture Decision Record (ADR) submission
  2. Core Architecture Board approval
  3. Migration plan for existing implementations
  4. Minimum 30-day community review period
- **Bug Reports**: File against the specific RFC in this directory
- **Clarifications**: File as RFC errata (non-breaking documentation fixes)

---

## Related Specifications

| Directory | Purpose |
|---|---|
| [specs/common/](specs/common/) | Shared models (events, state, capabilities, errors) |
| [specs/workflow/](specs/workflow/) | Workflow Engine specifications |
| [specs/vision/](specs/vision/) | Vision Engine specifications |
| [specs/plugin/](specs/plugin/) | Plugin system specifications |
| [specs/marketplace/](specs/marketplace/) | Marketplace infrastructure |
| [specs/storage/](specs/storage/) | Storage engine specifications |
| [specs/ui/](specs/ui/) | UI/UX specifications |
| [specs/ipc/](specs/ipc/) | IPC protocol specifications |
| [specs/knowledge/](specs/knowledge/ | Knowledge pack specifications |
| [specs/project/](specs/project/) | Project/workspace specifications |
| [docs/adr/](docs/adr/) | Architecture Decision Records |
| [rfcs/](rfc/) | Historical RFCs |
| [specs/glossary.md](specs/glossary.md) | Master terminology |
