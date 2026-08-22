# Atlas Common Specifications

> **Purpose**: Cross-cutting shared models referenced by ALL subsystems.  
> **Last Updated**: 2026-06-30  
> **Owner**: Atlas Specification Committee  

---

## Overview

These shared models eliminate duplication. Instead of each subsystem defining its own event model, state model, capability model, etc., all subsystems reference these common specifications.

`
All Subsystems
    ├── Workflow Engine ──→ references RFC-1001, RFC-1002, RFC-1003, RFC-1004, RFC-1005, RFC-1006
    ├── Vision Engine ──→ references RFC-1001, RFC-1002, RFC-1003, RFC-1004, RFC-1005, RFC-1006
    ├── AI Engine ──→ references RFC-1001, RFC-1002, RFC-1003, RFC-1004, RFC-1005, RFC-1006
    ├── Plugin System ──→ references RFC-1001, RFC-1002, RFC-1003, RFC-1004, RFC-1005, RFC-1006
    └── Marketplace ──→ references RFC-1001, RFC-1002, RFC-1003, RFC-1004, RFC-1005, RFC-1006
`

---

## Common RFCs

| RFC | Title | Depends On | Purpose |
|---|---|---|---|
| [RFC-1001](specs/common/RFC-1001-event-model.md) | Event Model | RFC-0005 | Standard event structure for ALL subsystems |
| [RFC-1002](specs/common/RFC-1002-state-model.md) | State Model | RFC-0006 | Standard state scope and transaction model |
| [RFC-1003](specs/common/RFC-1003-capability-model.md) | Capability Model | RFC-0012 | Standard capability declaration format |
| [RFC-1004](specs/common/RFC-1004-contract-model.md) | Contract Model | RFC-0013 | Standard contract interface patterns |
| [RFC-1005](specs/common/RFC-1005-manifest-model.md) | Manifest Model | RFC-0010 | Standard manifest structure for ALL packages |
| [RFC-1006](specs/common/RFC-1006-error-model.md) | Error Model | RFC-0011 | Standard error classification for ALL subsystems |

---

## Reading Order

1. RFC-1001 Event Model (foundation for messaging)
2. RFC-1002 State Model (foundation for persistence)
3. RFC-1003 Capability Model (foundation for feature detection)
4. RFC-1004 Contract Model (foundation for interfaces)
5. RFC-1005 Manifest Model (foundation for configuration)
6. RFC-1006 Error Model (foundation for error handling)

---

## Governance

Changes to common RFCs require approval from the Atlas Specification Committee.  
All subsystem teams MUST be notified of changes.  
Backward compatibility MUST be maintained.
