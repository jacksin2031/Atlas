# Atlas Traceability Matrix

> **Purpose**: End-to-end traceability from Vision through Release for every Atlas capability.  
> **Applies to**: All specification domains and their implementations.  
> **Owner**: Atlas Specification Committee  
> **Last Updated**: 2026-07-02  
> **Related**: [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md), [RFC_MAP.md](RFC_MAP.md), [SPECIFICATION_LAYERS.md](SPECIFICATION_LAYERS.md)  

---

## Traceability Chain

Every Atlas capability flows through this chain. Each step produces artifacts that feed the next step.

`
Vision
  ↓ (produces)
Mission Statement
  ↓ (informs)
ADR (Architecture Decision Record)
  ↓ (decides)
RFC (Request for Comments)
  ↓ (specifies)
Specification Artifact
  ↓ (implements)
Source Code / Implementation
  ↓ (validates)
Test Case
  ↓ (delivers)
Release
`

### Chain Rules

1. **Every ADR must reference a Mission Statement** (or be marked as technical infrastructure).
2. **Every RFC must reference at least one ADR** (or be marked as editorial/catalog).
3. **Every Specification Artifact must reference at least one RFC**.
4. **Every Implementation module must reference at least one Specification**.
5. **Every Test Case must reference at least one Implementation module**.
6. **Every Release must reference at least one Test Case suite**.

Violations are caught during the RFC Review process per [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md).

---

## Domain Traceability

### Runtime (RFC-0001 – RFC-0014)

| Capability | ADR | RFC | Spec Artifact | Implementation | Test |
|---|---|---|---|---|---|
| Process Lifecycle | ADR-0001 | RFC-0001, RFC-0002 | specs/runtime/ | crates/runtime/ | tests/runtime/ |
| Service Model | ADR-0003 | RFC-0003 | specs/runtime/ | crates/runtime/ | tests/runtime/ |
| Scheduler | ADR-0004 | RFC-0004 | specs/runtime/ | crates/runtime/ | tests/runtime/ |
| Event Bus | ADR-0005 | RFC-0005, RFC-1001 | specs/runtime/, specs/common/ | crates/runtime/ | tests/runtime/ |
| State Management | ADR-0006 | RFC-0006, RFC-1002 | specs/runtime/, specs/common/ | crates/runtime/ | tests/runtime/ |
| IPC Architecture | ADR-0010 | RFC-0007, RFC-0101+ | specs/runtime/, specs/ipc/ | crates/runtime/ | tests/ipc/ |
| Plugin Host | ADR-0015 | RFC-0008, RFC-0201+ | specs/runtime/, specs/plugin/ | crates/runtime/ | tests/plugin/ |
| Resource Mgmt | ADR-0009 | RFC-0009 | specs/runtime/ | crates/runtime/ | tests/runtime/ |
| Manifest | ADR-0012 | RFC-0010, RFC-1005 | specs/runtime/, specs/common/ | crates/runtime/ | tests/runtime/ |
| Error Taxonomy | ADR-0030 | RFC-0011, RFC-1006 | specs/runtime/, specs/common/ | crates/runtime/ | tests/runtime/ |
| Capability Registry | ADR-0012 | RFC-0012, RFC-1003 | specs/runtime/, specs/common/ | crates/runtime/ | tests/runtime/ |
| Contracts | ADR-0012 | RFC-0013, RFC-1004 | specs/runtime/, specs/common/ | crates/runtime/ | tests/runtime/ |
| Reference Arch | — | RFC-0014 | specs/runtime/ | — | — |

### IPC (RFC-0101 – RFC-0112)

| Capability | ADR | RFC | Spec Artifact | Implementation | Test |
|---|---|---|---|---|---|
| Transport Abstraction | ADR-0020 | RFC-0101, RFC-0103, RFC-0104 | specs/ipc/ | crates/ipc/ | tests/ipc/ |
| Channel Model | ADR-0020 | RFC-0105 | specs/ipc/ | crates/ipc/ | tests/ipc/ |
| Serialization | ADR-0012 | RFC-0106 | specs/ipc/ | crates/ipc/ | tests/ipc/ |
| Security Levels | ADR-0008 | RFC-0107, RFC-0108 | specs/ipc/ | crates/ipc/ | tests/ipc/ |
| Observability | ADR-0025 | RFC-0109, RFC-0110 | specs/ipc/ | crates/ipc/ | tests/ipc/ |
| Reliability | — | RFC-0108, RFC-0110 | specs/ipc/ | crates/ipc/ | tests/ipc/ |
| Error Model | ADR-0030 | RFC-0111, RFC-1006 | specs/ipc/, specs/common/ | crates/ipc/ | tests/ipc/ |
| Extension | — | RFC-0112 | specs/ipc/ | crates/ipc/ | tests/ipc/ |

### Plugin (RFC-0201 – RFC-0230)

| Capability | ADR | RFC | Spec Artifact | Implementation | Test |
|---|---|---|---|---|---|
| Overview & Manifest | ADR-0005 | RFC-0201, RFC-0202, RFC-1005 | specs/plugin/ | crates/plugin/ | tests/plugin/ |
| Lifecycle | ADR-0015 | RFC-0203, RFC-0002 | specs/plugin/, specs/runtime/ | crates/plugin/ | tests/plugin/ |
| Loader & Registry | ADR-0015 | RFC-0204, RFC-0205 | specs/plugin/ | crates/plugin/ | tests/plugin/ |
| Security & Sandbox | ADR-0015 | RFC-0207, RFC-0208 | specs/plugin/ | crates/plugin/ | tests/plugin/ |
| API & Services | ADR-0015 | RFC-0209, RFC-0215 | specs/plugin/ | crates/plugin/ | tests/plugin/ |
| Events & Telemetry | ADR-0025 | RFC-0210, RFC-0229 | specs/plugin/ | crates/plugin/ | tests/plugin/ |
| Discovery & Dependencies | — | RFC-0211, RFC-0216, RFC-0227, RFC-0228 | specs/plugin/ | crates/plugin/ | tests/plugin/ |
| Packaging & Signatures | — | RFC-0217, RFC-0230 | specs/plugin/ | crates/plugin/ | tests/plugin/ |
| IPC & Storage Integration | — | RFC-0220, RFC-0222 | specs/plugin/ | crates/plugin/ | tests/plugin/ |
| Hot Reload & Migration | — | RFC-0225, RFC-0226 | specs/plugin/ | crates/plugin/ | tests/plugin/ |

### Workflow (RFC-0301 – RFC-0333)

| Capability | ADR | RFC | Spec Artifact | Implementation | Test |
|---|---|---|---|---|---|
| Language & Execution | ADR-0005 | RFC-0301, RFC-0302, RFC-0303 | specs/workflow/ | crates/workflow/ | tests/workflow/ |
| State & Context | ADR-0006 | RFC-0304, RFC-0306, RFC-0307 | specs/workflow/ | crates/workflow/ | tests/workflow/ |
| Actions & Triggers | — | RFC-0309, RFC-0310, RFC-0311 | specs/workflow/ | crates/workflow/ | tests/workflow/ |
| Scheduler & Parallelism | — | RFC-0312, RFC-0313 | specs/workflow/ | crates/workflow/ | tests/workflow/ |
| Error & Recovery | ADR-0030 | RFC-0314, RFC-0315 | specs/workflow/ | crates/workflow/ | tests/workflow/ |
| Debugging & Testing | — | RFC-0316, RFC-0331 | specs/workflow/ | crates/workflow/ | tests/workflow/ |
| Versioning & Compatibility | — | RFC-0318, RFC-0329, RFC-0332 | specs/workflow/ | crates/workflow/ | tests/workflow/ |
| Plugin Integration | — | RFC-0323 | specs/workflow/ | crates/workflow/ | tests/workflow/ |
| Storage Integration | — | RFC-0324 | specs/workflow/ | crates/workflow/ | tests/workflow/ |
| AI / Vision / IPC Integration | — | RFC-0325, RFC-0326, RFC-0327, RFC-0328 | specs/workflow/ | crates/workflow/ | tests/workflow/ |

### Storage (RFC-0401 – RFC-0425)

| Capability | ADR | RFC | Spec Artifact | Implementation | Test |
|---|---|---|---|---|---|
| Provider Interface | — | RFC-0403 | specs/storage/ | crates/storage/ | tests/storage/ |
| Transactions & Consistency | — | RFC-0406, RFC-0416, RFC-0417 | specs/storage/ | crates/storage/ | tests/storage/ |
| Schema & Versioning | — | RFC-0405, RFC-0407 | specs/storage/ | crates/storage/ | tests/storage/ |
| Backup & Recovery | — | RFC-0411, RFC-0412 | specs/storage/ | crates/storage/ | tests/storage/ |
| Security & Compliance | ADR-0008 | RFC-0409, RFC-0420 | specs/storage/ | crates/storage/ | tests/storage/ |
| Events & Observability | ADR-0025 | RFC-0413, RFC-0414 | specs/storage/ | crates/storage/ | tests/storage/ |
| Extension & Domains | — | RFC-0419, RFC-0421, RFC-0422 | specs/storage/ | crates/storage/ | tests/storage/ |

---

## Deferred Domains Traceability (Placeholders)

| Capability | Reserved RFC | Expected ADR | Expected Implementation | Expected Test |
|---|---|---|---|---|
| Marketplace Protocol | RFC-0501 | TBD | apps/marketplace/ | tests/marketplace/ |
| Package Format | RFC-0502 | TBD | crates/package/ | tests/package/ |
| Version Resolution | RFC-0503 | TBD | crates/version/ | tests/version/ |
| Crypto Signatures | RFC-0504 | TBD | crates/crypto/ | tests/crypto/ |
| Knowledge Pack Protocol | RFC-0601 | TBD | crates/knowledge/ | tests/knowledge/ |
| Vector Search | RFC-0602 | TBD | crates/search/ | tests/search/ |
| Vision Camera | RFC-0801 | TBD | crates/vision/ | tests/vision/ |
| Vision OCR | RFC-0802 | TBD | crates/vision/ | tests/vision/ |
| AI Model Routing | RFC-0901 | TBD | crates/ai/ | tests/ai/ |
| AI Prompt Mgmt | RFC-0902 | TBD | crates/ai/ | tests/ai/ |
| UI Component Model | RFC-0810 | TBD | apps/desktop/ | tests/ui/ |
| Project Package | RFC-0701 | TBD | crates/project/ | tests/project/ |
| Workspace Boundaries | RFC-0702 | TBD | crates/workspace/ | tests/workspace/ |
| Config Engine | RFC-0703 | TBD | crates/config/ | tests/config/ |

---

## Traceability Verification

During each Release cycle, the following verification is performed:

1. **Coverage Check**: Every Active RFC must have at least one test module.
2. **Gap Report**: Any RFC without a corresponding test module is flagged as TRACEABILITY_GAP.
3. **Blocker**: Releases cannot ship with more than 3 TRACEABILITY_GAP flags.
4. **Audit**: Spec Committee reviews gap reports quarterly per [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md).

---

*This document is part of the Atlas Specification hierarchy. For the RFC tree, see [RFC_MAP.md](RFC_MAP.md). For governance, see [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md). For layer definitions, see [SPECIFICATION_LAYERS.md](SPECIFICATION_LAYERS.md) and [LAYER_MODEL.md](LAYER_MODEL.md). For domain ownership, see [DOMAIN_OWNERS.md](DOMAIN_OWNERS.md).*

