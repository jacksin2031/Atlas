# Atlas RFC Template

> **Purpose**: Standard template for all new Atlas RFCs.
> **Usage**: Copy this file, fill in all fields, and follow RFC_STYLE_GUIDE.md. Follow RFC_CHANGE_POLICY.md for modification procedures and RFC_VERSIONING_POLICY.md for versioning rules.
> **Owner**: Atlas Specification Committee
> **Related**: [RFC_STYLE_GUIDE.md](RFC_STYLE_GUIDE.md), [RFC_CHANGE_POLICY.md](RFC_CHANGE_POLICY.md), [RFC_VERSIONING_POLICY.md](RFC_VERSIONING_POLICY.md), [RFC_REVIEW_CHECKLIST.md](RFC_REVIEW_CHECKLIST.md)
> **Last Updated**: 2026-07-01

---

RFC: RFC-XXXX
Title: [Title]
Status: Proposed | Accepted | Active | Deprecated | Superseded | Frozen | Experimental
Category: Core | Standard | Experimental
Owner: [Team or Committee]
Authors: [Names]
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
ADS Version: 1.x.x
Spec Version: 1.x.x
Normative: YES | NO
Depends On:
  - RFC-NNNN [Name]
Supersedes: RFC-NNNN | None
Superseded By: RFC-NNNN | None
Related ADR:
  - ADR-NNNN [Title]
Related JSON Schema:
  - schemas/[domain]/[entity].json
Related Catalog:
  - catalog/[entity].md
Audience: [Target audience]
Target Release: 1.x.x
Review Cycle: [Cycle]
Compatibility: Compatible with Spec X.x

---

## Normative Status

This specification is [Normative | Non-Normative]. Every Atlas subsystem [MUST / MUST NOT] conform to the requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution and all active ADRs.

---

## Authority

This RFC is the authoritative specification for the [DOMAIN].

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary and the authoritative RFCs listed below.

| Term | Definition | Source |
|---|---|---|
| [TERM1] | [Definition] | [RFC-XXXX] |
| [TERM2] | [Definition] | [RFC-XXXX] |
| [TERM3] | [Definition] | [RFC-XXXX] |

---

## [Core Content Section]

[Domain-specific content goes here. Follow RFC 2119 language rules. See RFC_STYLE_GUIDE.md section 2.]

---

## Layer Boundaries

### Responsibilities

This specification IS responsible for:

- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

### Non-Responsibilities

This specification IS NOT responsible for:

- [Non-responsibility 1]
- [Non-responsibility 2]

### Dependencies

| Dependency | Direction | Description |
|---|---|---|
| RFC-XXXX | Consumed | [Description] |
| RFC-XXXX | Consumed | [Description] |

### Consumers

- [Consumer 1] (RFC-XXXX): [Description]
- [Consumer 2] (RFC-XXXX): [Description]

### Providers

- [Provider 1] (schemas/...): [Description]
- [Provider 2] (catalog/...): [Description]

### Forbidden Dependencies

- This specification MUST NOT depend on [platform / library / protocol].
- This specification MUST NOT assume [implementation detail].

---

## Security

[Security requirements for this domain.]

---

## Performance

[Performance requirements for this domain.]

---

## Compatibility

[Compatibility requirements for this domain.]

---

## Compliance

[Compliance requirements for this domain.]

---

## Future Evolution

[Planned extensions and 10-year outlook for this domain.]

---

## Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (Rust, Node.js, TypeScript, Go, Python, etc.)
- Any runtime environment (Electron, Tauri, Browser, Desktop, Server)
- Any storage backend (SQLite, PostgreSQL, MongoDB, Redis, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any cloud provider (AWS, Azure, GCP, etc.)
- Any container platform (Docker, containerd, etc.)

---

## Acceptance Criteria

### [Domain Category]

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST [testable requirement]. | [Specific test name] |
| AC-02 | The implementation MUST [testable requirement]. | [Specific test name] |

---

## References

| Reference | Description |
|---|---|
| RFC-XXXX | [Title] |
| ADR-XXXX | [Title] |
| schemas/[domain]/[entity].json | [Description] |
| catalog/[entity].md | [Description] |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |

---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | [List of related RFCs] |
| Related ADR | [List of related ADRs] |
| Related JSON Schema | [List of related schemas] |
| Related Catalog | [List of related catalogs] |

---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | YYYY-MM-DD | [Author] | Initial publication |

