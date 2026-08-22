# Atlas Specification Dependency Graph

> **Purpose**: Defines allowed dependencies, forbidden dependencies, and ownership for every specification domain in Atlas.  
> **Created**: 2026-07-02  
> **Owner**: Atlas Specification Committee  
> **Related**: [SPECIFICATION_LAYERS.md](SPECIFICATION_LAYERS.md), [RFC_MAP.md](RFC_MAP.md), [SPECIFICATION_INDEX.md](SPECIFICATION_INDEX.md), [ARCHITECTURE_MATRIX.md](ARCHITECTURE_MATRIX.md)

---

## 1. Domain Inventory

Atlas has **14 specification domains** organized into **10 RFC number ranges** plus shared common models.

| Domain | RFC Range | Files | Status |
|---|---|---|---|
| **Runtime** | RFC-0001 – RFC-0014 | 14 RFCs | Frozen |
| **IPC** | RFC-0101 – RFC-0112 | 12 RFCs | Active |
| **Plugin** | RFC-0201 – RFC-0230 | 30 RFCs | Proposed |
| **Workflow** | RFC-0301 – RFC-0333 | 33 RFCs | Proposed |
| **Storage** | RFC-0401 – RFC-0425 | 25 RFCs | Proposed |
| **Marketplace** | RFC-0501 – RFC-0508 | 0 RFCs | Deferred |
| **Knowledge** | RFC-0601 – RFC-0608 | 0 RFCs | Deferred |
| **Project** | RFC-0701 – RFC-0708 | 0 RFCs | Deferred |
| **Common** | RFC-1001 – RFC-1006 | 6 RFCs | Draft |
| **Catalogs** | N/A | ~60 catalog files | Active |

Plus 4 empty placeholder domains with README stubs only: **Vision**, **AI**, **UI**, **Events**.

---

## 2. Allowed Dependencies

A domain MAY depend on the domains listed below. Dependencies flow **bottom-up only** — higher layers may reference lower layers; lower layers must never reference higher layers.

### Runtime (RFC-0001 – RFC-0014)
**Can depend on:** Nothing (Foundation layer)  
**Can be depended on by:** IPC, Plugin, Workflow, Storage, Marketplace, Knowledge, Project, Common, Vision, AI, UI

### Common (RFC-1001 – RFC-1006)
**Can depend on:** Runtime  
**Can be depended on by:** IPC, Plugin, Workflow, Storage, Marketplace, Knowledge, Project, Vision, AI, UI

### IPC (RFC-0101 – RFC-0112)
**Can depend on:** Runtime, Common  
**Can be depended on by:** Plugin, Workflow, Storage, Marketplace, Knowledge, Project, Vision, AI, UI

### Plugin (RFC-0201 – RFC-0230)
**Can depend on:** Runtime, Common, IPC, Storage  
**Can be depended on by:** Workflow, Marketplace, Knowledge, Project, Vision, AI, UI

### Workflow (RFC-0301 – RFC-0333)
**Can depend on:** Runtime, Common, IPC, Plugin, Storage  
**Can be depended on by:** Marketplace, Knowledge, Project, Vision, AI, UI

### Storage (RFC-0401 – RFC-0425)
**Can depend on:** Runtime, Common, IPC, Plugin  
**Can be depended on by:** Workflow, Marketplace, Knowledge, Project, Vision, AI, UI

### Marketplace (RFC-0501 – RFC-0508, Deferred)
**Can depend on:** Runtime, Common, IPC, Plugin, Storage, Workflow  
**Can be depended on by:** UI

### Knowledge (RFC-0601 – RFC-0608, Deferred)
**Can depend on:** Runtime, Common, IPC, Plugin, Storage, Workflow  
**Can be depended on by:** UI, AI

### Project (RFC-0701 – RFC-0708, Deferred)
**Can depend on:** Runtime, Common, IPC, Plugin, Storage, Workflow  
**Can be depended on by:** UI

### Vision (placeholder, no RFCs yet)
**Can depend on:** Runtime, Common, IPC, Plugin, Storage, Workflow  
**Can be depended on by:** UI, AI

### AI (placeholder, no RFCs yet)
**Can depend on:** Runtime, Common, IPC, Plugin, Storage, Workflow, Knowledge, Vision  
**Can be depended on by:** UI

### UI (placeholder, no RFCs yet)
**Can depend on:** Everything above  
**Can be depended on by:** Nothing (presentation layer)

---

## 3. Forbidden Dependencies

The following cross-domain dependencies are **strictly prohibited**. Violations indicate architectural drift.

| From | Cannot Depend On | Reason |
|---|---|---|
| **Runtime** | IPC, Plugin, Workflow, Storage, Marketplace, Knowledge, Project, Vision, AI, UI | Foundation must not depend on extensions |
| **Common** | IPC, Plugin, Workflow, Storage, Marketplace, Knowledge, Project, Vision, AI, UI | Shared models must not depend on domain implementations |
| **IPC** | Plugin, Workflow, Storage, Marketplace, Knowledge, Project, Vision, AI, UI | Communication layer must not depend on application logic |
| **Plugin** | Workflow, Marketplace, Knowledge, Project, Vision, AI, UI | Extension framework must not depend on specific use cases |
| **Workflow** | Marketplace, Knowledge, Project, Vision, AI, UI | Orchestration must not depend on domain-specific services |
| **Storage** | Workflow, Marketplace, Knowledge, Project, Vision, AI, UI | Persistence must not depend on orchestration or presentation |
| **Marketplace** | Knowledge, Project, Vision, AI, UI | Distribution must not depend on downstream consumers |
| **Knowledge** | Vision, AI, UI | Data layer must not depend on consumption layer |
| **Project** | Vision, AI, UI | Scope must not depend on downstream consumers |
| **Vision** | AI, UI | Sensory layer must not depend on intelligence or presentation |
| **AI** | UI | Intelligence must not depend on presentation |
| **UI** | *(none)* | UI is the terminal layer — it depends on everything but nothing depends on it |

### Cross-number-range rules
- **RFC-0xxx (00xx)** can NEVER reference **RFC-1xxx**. Common models depend on Runtime, not vice versa.
- **RFC-0xxx (00xx)** can reference **RFC-1xxx** (Common) — Common wraps Runtime concepts.
- **RFC-1xxx** can NEVER reference **RFC-0xxx** directly beyond the 4 common RFCs (1001–1006).
- **Higher-numbered domains** (05xx, 06xx, 07xx) can NEVER reference each other except through lower layers.

---

## 4. Ownership Matrix

| Domain | RFC Range | Owner | Review Board |
|---|---|---|---|
| Runtime | RFC-0001 – RFC-0014 | Runtime Arch Board | Core Architecture Group |
| IPC | RFC-0101 – RFC-0112 | IPC Sub-team | Core Architecture Group |
| Plugin | RFC-0201 – RFC-0230 | Plugin Sub-team | Core Architecture Group |
| Workflow | RFC-0301 – RFC-0333 | Workflow Team | Workflow Lead + Core Arch |
| Storage | RFC-0401 – RFC-0425 | Storage Team | Storage Lead + Core Arch |
| Marketplace | RFC-0501 – RFC-0508 | Marketplace Team | TBD (deferred) |
| Knowledge | RFC-0601 – RFC-0608 | Knowledge Team | TBD (deferred) |
| Project | RFC-0701 – RFC-0708 | Project Team | TBD (deferred) |
| Common | RFC-1001 – RFC-1006 | Spec Committee | All domain leads |
| Catalogs | N/A | Individual domain owners | Spec Committee |

---

## 5. Dependency Enforcement Rules

1. **An RFC may only reference RFCs in its allowed list.** Any new cross-domain reference requires Spec Committee approval.
2. **Catalog files** (e.g., workflow/catalog/workflow-actions.md) belong to their parent domain and may only reference RFCs within that domain plus allowed lower domains.
3. **Cross-domain RFCs** (e.g., RFC-0323 workflow-plugin-integration) are exceptions — they must be reviewed by BOTH domain owners.
4. **Circular dependencies between domains are forbidden.** Within a domain, circular references between RFCs are permitted (e.g., RFC-0004 ↔ RFC-0005 within Runtime).
5. **Deferred domains** (Marketplace, Knowledge, Project, Vision, AI, UI) must not create RFC files until their RFC ranges are officially activated by the Spec Committee.

---

## 6. Visual Summary

`
┌─────────────────────────────────────────────────────────────┐
│                        UI                                   │ ← Presentation (highest)
├─────────────────────────────────────────────────────────────┤
│                   AI · Vision                               │ ← Intelligence
├─────────────────────────────────────────────────────────────┤
│             Knowledge · Project · Marketplace               │ ← Domain Services
├─────────────────────────────────────────────────────────────┤
│              Workflow · Storage                             │ ← Orchestration & Persistence
├─────────────────────────────────────────────────────────────┤
│                         Plugin                              │ ← Extension Framework
├─────────────────────────────────────────────────────────────┤
│                          IPC                                │ ← Communication
├─────────────────────────────────────────────────────────────┤
│                     Common Models                           │ ← Shared Abstractions
├─────────────────────────────────────────────────────────────┤
│                        Runtime                              │ ← Foundation (lowest)
└─────────────────────────────────────────────────────────────┘
`

*Arrows flow upward. Lower layers cannot reference upper layers.*

---

*This document is part of the Atlas Specification hierarchy. For layers, see [SPECIFICATION_LAYERS.md](SPECIFICATION_LAYERS.md) and [LAYER_MODEL.md](LAYER_MODEL.md). For the RFC tree, see [RFC_MAP.md](RFC_MAP.md). For governance, see [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md). For change processes, see [SPECIFICATION_CHANGE_PROCESS.md](SPECIFICATION_CHANGE_PROCESS.md).*


