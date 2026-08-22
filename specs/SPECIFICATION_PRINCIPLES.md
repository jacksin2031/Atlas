# Atlas Specification Principles

> **Purpose**: Foundational principles governing how Atlas specifications are written, organized, and maintained.  
> **Applies to**: All files under specs/ and their subdirectories.  
> **Owner**: Atlas Specification Committee  
> **Last Updated**: 2026-07-02  
> **Related**: [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md), [glossary.md](glossary.md), [SPECIFICATION_CHANGE_PROCESS.md](SPECIFICATION_CHANGE_PROCESS.md)  

---

## P1: Single Source of Truth

Every concept, model, and interface in Atlas has exactly **one authoritative definition**.

- Common Models (RFC-1001–RFC-1006) are the single source of truth for events, state, capabilities, contracts, manifests, and errors.
- No domain may redefine a Common Model. Domains reference Common Models; they do not replicate them.
- If a domain needs a variation, it extends the Common Model through the extension mechanism (RFC-0112, RFC-0214, RFC-0419, RFC-0322).
- Catalog files (e.g., catalog/messages.md) are the single source of truth for enumerated identifiers.

**Violation**: Two RFCs define their own event structure.  
**Correction**: Both must reference RFC-1001 (Event Model).

---

## P2: No Duplicate Definitions

If a concept is defined in one RFC, it MUST NOT be redefined in another.

- Use cross-references (see RFC-NNNN) instead of copying definitions.
- If a concept appears in multiple places, consolidate it into the most foundational RFC and reference it.
- Catalog files may enumerate values but must not redefine the conceptual model behind them.

**Violation**: RFC-0309 defines "Action" and RFC-0310 also defines "Action" with slightly different semantics.  
**Correction**: Both reference RFC-0301's definition of Action; RFC-0310 defines "Condition" instead.

---

## P3: Reference Instead of Copy

Specifications reference other specifications rather than embedding their content.

- Copy-paste definitions create drift. When the source changes, copies become stale.
- Use normative references: "MUST conform to RFC-NNNN."
- Use informative references for context: "For background, see RFC-NNNN."

**Violation**: RFC-0406 copies the transaction semantics from RFC-0006.  
**Correction**: RFC-0406 states "Transactions follow the model defined in RFC-0006."

---

## P4: Contracts Before Implementation

No implementation code may ship without a corresponding specification contract.

- Every interface, message type, channel, and storage provider MUST have an RFC or catalog entry.
- Implementation code that lacks a specification is considered undocumented and must be spec'd before merging.
- This rule applies to all layers: Runtime, IPC, Plugin, Workflow, Storage, and beyond.

**Exception**: Experimental RFCs may precede implementation by any amount.

---

## P5: Implementation Independent

Specifications define WHAT, not HOW.

- RFCs must not prescribe programming languages, frameworks, libraries, or operating systems.
- RFCs must not embed implementation-specific details (e.g., "use Redis for caching," "use gRPC for transport").
- Implementation details belong in ADRs, design documents, or SDK documentation — not in RFCs.

**Violation**: RFC-0103 says "Use ZeroMQ as the default transport."  
**Correction**: RFC-0103 defines the transport abstraction; ZeroMQ is mentioned only as an example implementation.

---

## P6: RFC 2119 First

Every RFC uses RFC 2119 terminology (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, RECOMMENDED) for normative statements.

- RFC 2119 terminology is used exclusively throughout all normative content.
- Informative content (examples, background, rationale) is clearly separated from normative content.
- Catalog files are normative by default — every entry is a required identifier.

**Violation**: An RFC mixes "we suggest using" with "MUST implement" without distinction.  
**Correction**: Separate into a "Guidance" section (informative) and "Requirements" section (normative).

---

## P7: Specification Before Code

Specifications must be written and reviewed before implementation begins.

- No implementation may proceed without an Accepted or Active RFC covering the behavior.
- The RFC must define the interface, data model, and constraints before code is written.
- Implementation code that deviates from the RFC requires a formal RFC amendment per [RFC_CHANGE_POLICY.md](RFC_CHANGE_POLICY.md).

**Exception**: Experimental RFCs may be implemented without formal review.

---

## P8: Backward Compatibility

Specifications must support forward compatibility where feasible.

- New RFCs must not break existing consumers of older RFCs.
- Extension mechanisms (RFC-0112, RFC-0214, RFC-0322, RFC-0419) must be used for new capabilities.
- Version negotiation must be defined for all protocols that cross process boundaries.

**Violation**: RFC-0405 removes a field from the storage schema without a migration path.  
**Correction**: RFC-0405 marks the field as deprecated and provides RFC-0408 migration procedure.

---

## P9: Minimal Surface Area

Specifications define the smallest interface surface necessary.

- Every new RFC, catalog entry, or extension point increases the maintenance burden.
- Before adding a new specification, ask: "Can this be handled by an existing RFC?"
- Avoid over-engineering: if a simple rule solves the problem, do not create a complex framework.

**Violation**: Creating a new "Workflow Notification Service" RFC when RFC-0308 (Workflow Events) already covers notifications.  
**Correction**: Extend RFC-0308 with notification event types.

---

## P10: Cross-RFC Consistency

All RFCs within a release must be internally consistent.

- Terminology must be uniform across all RFCs (see [glossary.md](glossary.md) for authoritative terms).
- Error codes, message types, channel IDs, and capability IDs must not collide.
- State transition diagrams must agree across RFCs that reference the same lifecycle.
- The Spec Committee performs a consistency audit before promoting any RFC from Draft to Accepted.

**Violation**: RFC-0305 defines a workflow state "Running" but RFC-0306 defines it as "Executing."  
**Correction**: Both reference RFC-1002 (State Model) which defines the canonical state names.

---

## Principle Enforcement

| Principle | Enforced By | Frequency |
|---|---|---|
| P1: Single Source of Truth | Spec Committee | Per RFC review |
| P2: No Duplicate Definitions | Spec Committee | Per RFC review |
| P3: Reference Instead of Copy | Reviewers | Per RFC review |
| P4: Contracts Before Implementation | Release Gate | Per release |
| P5: Implementation Independent | Reviewers | Per RFC review |
| P6: RFC 2119 First | RFC Style Guide | Per RFC review |
| P7: Specification Before Code | Release Gate | Per release |
| P8: Backward Compatibility | Reviewers | Per RFC review |
| P9: Minimal Surface Area | Reviewers | Per RFC review |
| P10: Cross-RFC Consistency | Spec Committee | Quarterly audit |

---

*This document is part of the Atlas Specification hierarchy. For governance, see [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md). For the glossary, see [glossary.md](glossary.md). For domain ownership, see [DOMAIN_OWNERS.md](DOMAIN_OWNERS.md). For change processes, see [SPECIFICATION_CHANGE_PROCESS.md](SPECIFICATION_CHANGE_PROCESS.md).*

