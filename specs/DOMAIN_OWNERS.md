# Atlas Domain Owners

> **Purpose**: Authoritative record of domain ownership, dependencies, and deliverables for every Atlas specification domain.  
> **Created**: 2026-07-02  
> **Owner**: Atlas Specification Committee  

---

## Domain Ownership Registry

Each domain has a designated Owner, Review Authority, and clearly defined responsibilities. This document is the single source of truth for domain ownership.

---

### Layer 1 — Common Models

#### RFC-1001: Event Model
| Field | Value |
|---|---|
| **Owner** | Spec Committee |
| **Review Authority** | All domain leads |
| **Depends On** | Runtime Event Bus (RFC-0005) |
| **Produces** | Standard event envelope, event types, DLQ definition |
| **Consumes** | RFC-0005, RFC-0006 |
| **Voting** | Unanimous consent |

#### RFC-1002: State Model
| Field | Value |
|---|---|
| **Owner** | Spec Committee |
| **Review Authority** | All domain leads |
| **Depends On** | Runtime State (RFC-0006) |
| **Produces** | Standard state scope, state transactions, state types |
| **Consumes** | RFC-0006 |
| **Voting** | Unanimous consent |

#### RFC-1003: Capability Model
| Field | Value |
|---|---|
| **Owner** | Spec Committee |
| **Review Authority** | All domain leads |
| **Depends On** | Runtime Capability Registry (RFC-0012) |
| **Produces** | Standard capability declaration format |
| **Consumes** | RFC-0012 |
| **Voting** | Unanimous consent |

#### RFC-1004: Contract Model
| Field | Value |
|---|---|
| **Owner** | Spec Committee |
| **Review Authority** | All domain leads |
| **Depends On** | Runtime Contracts (RFC-0013) |
| **Produces** | Standard contract interface patterns |
| **Consumes** | RFC-0013 |
| **Voting** | Unanimous consent |

#### RFC-1005: Manifest Model
| Field | Value |
|---|---|
| **Owner** | Spec Committee |
| **Review Authority** | All domain leads |
| **Depends On** | Runtime Manifest (RFC-0010) |
| **Produces** | Standard manifest structure for all packages |
| **Consumes** | RFC-0010 |
| **Voting** | Unanimous consent |

#### RFC-1006: Error Model
| Field | Value |
|---|---|
| **Owner** | Spec Committee |
| **Review Authority** | All domain leads |
| **Depends On** | Runtime Error Taxonomy (RFC-0011) |
| **Produces** | Standard error classification for all subsystems |
| **Consumes** | RFC-0011 |
| **Voting** | Unanimous consent |

---

### Layer 2 — Runtime

#### RFC-0001 – RFC-0014 (Runtime Suite)
| Field | Value |
|---|---|
| **Owner** | Runtime Arch Board |
| **Review Authority** | Core Architecture Group |
| **Depends On** | *(Foundation — nothing)* |
| **Produces** | Lifecycle, Scheduler, Event Bus, State Mgmt, Resource Mgmt, Manifest, Capabilities, Contracts, Error Taxonomy, Reference Arch |
| **Consumed By** | ALL domains |
| **Voting** | 2/3 majority |
| **Status** | Frozen |

---

### Layer 3 — IPC

#### RFC-0101 – RFC-0112 (IPC Suite)
| Field | Value |
|---|---|
| **Owner** | IPC Sub-team Lead |
| **Review Authority** | Core Architecture Group |
| **Depends On** | Runtime (RFC-0007), Common (RFC-1001, RFC-1006) |
| **Produces** | Transport abstraction, channel model, serialization contract, security levels, observability hooks |
| **Consumed By** | Plugin, Workflow, Storage, Marketplace, Knowledge, Vision, AI, UI |
| **Voting** | Simple majority |
| **Status** | Active |

---

### Layer 3 — Storage

#### RFC-0401 – RFC-0425 (Storage Suite)
| Field | Value |
|---|---|
| **Owner** | Storage Lead |
| **Review Authority** | Storage Team + Core Architecture Group |
| **Depends On** | Runtime (RFC-0001–RFC-0009), Common (RFC-1001, RFC-1006), IPC |
| **Produces** | Provider interface, transaction model, schema evolution, backup/recovery, consistency guarantees |
| **Consumed By** | Workflow, Marketplace, Knowledge, Vision, AI, UI, Project |
| **Voting** | Simple majority |
| **Status** | Proposed |

---

### Layer 4 — Plugin

#### RFC-0201 – RFC-0230 (Plugin Suite)
| Field | Value |
|---|---|
| **Owner** | Plugin Sub-team Lead |
| **Review Authority** | Core Architecture Group |
| **Depends On** | Runtime (RFC-0001–RFC-0009, RFC-0012, RFC-0013), Common (RFC-1001–RFC-1006), IPC, Storage |
| **Produces** | Extension framework, loader, registry, sandbox, API, service model, discovery, packaging |
| **Consumed By** | Workflow, Marketplace, Knowledge, Vision, AI, UI |
| **Voting** | Simple majority |
| **Status** | Proposed |

---

### Layer 4 — Workflow

#### RFC-0301 – RFC-0333 (Workflow Suite)
| Field | Value |
|---|---|
| **Owner** | Workflow Lead |
| **Review Authority** | Workflow Team + Core Architecture Group |
| **Depends On** | Runtime (RFC-0001–RFC-0006, RFC-0010–RFC-0012), Common (RFC-1001–RFC-1006), IPC, Plugin, Storage |
| **Produces** | Language, execution engine, actions, triggers, conditions, scheduler, recovery, debugging |
| **Consumed By** | Marketplace, Knowledge, Vision, AI, UI |
| **Voting** | Simple majority |
| **Status** | Proposed |

---

### Layer 5 — Knowledge (Deferred)

#### RFC-0601 – RFC-0608 (Knowledge Suite)
| Field | Value |
|---|---|
| **Owner** | Knowledge Team (TBD) |
| **Review Authority** | Spec Committee |
| **Depends On** | Runtime, Common, IPC, Plugin, Storage, Workflow |
| **Produces** | Knowledge pack protocol, vector search, semantic indexing |
| **Consumed By** | AI, UI |
| **Voting** | 2/3 majority |
| **Status** | Deferred |

---

### Layer 5 — Vision (Placeholder)

#### RFC-0801 – RFC-0804 (Vision Suite)
| Field | Value |
|---|---|
| **Owner** | TBD |
| **Review Authority** | Spec Committee |
| **Depends On** | Runtime, Common, IPC, Plugin, Storage, Workflow |
| **Produces** | Camera pipeline, OCR engine, image processing |
| **Consumed By** | AI, UI |
| **Voting** | 2/3 majority |
| **Status** | Placeholder |

---

### Layer 5 — AI (Placeholder)

#### RFC-0901 – RFC-0904 (AI Suite)
| Field | Value |
|---|---|
| **Owner** | TBD |
| **Review Authority** | Spec Committee |
| **Depends On** | Runtime, Common, IPC, Plugin, Storage, Workflow, Knowledge, Vision |
| **Produces** | Model routing, prompt management, context windows, tool calling |
| **Consumed By** | UI |
| **Voting** | 2/3 majority |
| **Status** | Placeholder |

---

### Layer 6 — Marketplace (Deferred)

#### RFC-0501 – RFC-0508 (Marketplace Suite)
| Field | Value |
|---|---|
| **Owner** | Marketplace Team (TBD) |
| **Review Authority** | Spec Committee |
| **Depends On** | Runtime, Common, IPC, Plugin, Storage, Workflow |
| **Produces** | Package format, version resolution, cryptographic signatures |
| **Consumed By** | UI |
| **Voting** | 2/3 majority |
| **Status** | Deferred |

---

### Layer 6 — Project (Deferred)

#### RFC-0701 – RFC-0708 (Project Suite)
| Field | Value |
|---|---|
| **Owner** | Project Team (TBD) |
| **Review Authority** | Spec Committee |
| **Depends On** | Runtime, Common, IPC, Plugin, Storage, Workflow |
| **Produces** | Project package format, workspace boundaries, config engine |
| **Consumed By** | UI |
| **Voting** | 2/3 majority |
| **Status** | Deferred |

---

### Layer 6 — UI (Placeholder)

#### RFC-0810 – RFC-0812 (UI Suite)
| Field | Value |
|---|---|
| **Owner** | TBD |
| **Review Authority** | Spec Committee |
| **Depends On** | Everything above |
| **Produces** | UI components, themes, accessibility |
| **Consumed By** | *(Nothing — terminal layer)* |
| **Voting** | 2/3 majority |
| **Status** | Placeholder |

---

## Ownership Summary

| Layer | Domain | Owner | Status | Votes Needed |
|---|---|---|---|---|
| 1 | Common (RFC-1xxx) | Spec Committee | Draft | Unanimous |
| 2 | Runtime (RFC-00xx) | Runtime Arch Board | Frozen | 2/3 |
| 3 | IPC (RFC-01xx) | IPC Sub-team Lead | Active | Simple |
| 3 | Storage (RFC-04xx) | Storage Lead | Proposed | Simple |
| 4 | Plugin (RFC-02xx) | Plugin Sub-team Lead | Proposed | Simple |
| 4 | Workflow (RFC-03xx) | Workflow Lead | Proposed | Simple |
| 5 | Knowledge (RFC-06xx) | TBD | Deferred | 2/3 |
| 5 | Vision (RFC-08xx) | TBD | Placeholder | 2/3 |
| 5 | AI (RFC-09xx) | TBD | Placeholder | 2/3 |
| 6 | Marketplace (RFC-05xx) | TBD | Deferred | 2/3 |
| 6 | Project (RFC-07xx) | TBD | Deferred | 2/3 |
| 6 | UI (RFC-08xx) | TBD | Placeholder | 2/3 |

---

*This document is part of the Atlas Specification hierarchy. For dependency rules, see [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md). For governance, see [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md). For traceability, see [TRACEABILITY_MATRIX.md](TRACEABILITY_MATRIX.md). For change processes, see [SPECIFICATION_CHANGE_PROCESS.md](SPECIFICATION_CHANGE_PROCESS.md).*


