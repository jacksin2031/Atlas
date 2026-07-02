# Atlas RFC Style Guide

> **Purpose**: Define the canonical style rules for all Atlas RFCs.  
> **Applies to**: All RFCs in specs/ and subdirectories.  > **Related**: [RFC_CHANGE_POLICY.md](RFC_CHANGE_POLICY.md), [RFC_VERSIONING_POLICY.md](RFC_VERSIONING_POLICY.md), [RFC_TEMPLATE.md](RFC_TEMPLATE.md), [RFC_REVIEW_CHECKLIST.md](RFC_REVIEW_CHECKLIST.md)  
> **Owner**: Atlas Specification Committee  
> **Last Updated**: 2026-07-01  

---

## 1. Document Structure

Every RFC MUST follow this exact structure:

RFC: RFC-XXXX
Title: [Title]
Status: [Proposed | Accepted | Active | Deprecated | Superseded]
Category: [Core | Standard | Experimental]
Owner: [Team/Committee]
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
Last Updated: YYYY-MM-DD

---

## Normative Status
[Paragraph]

## Authority
[Paragraph]

## Terminology
[Table]

## [Core Content Section]
[Content...]

## Layer Boundaries
[Section...]

## Security
[Section...]

## Performance
[Section...]

## Compatibility
[Section...]

## Compliance
[Section...]

## Future Evolution
[Section...]

## Runtime Independence
[Section...]

## Acceptance Criteria
[Table]

## References
[Table]

## Compliance Matrix
[Table]

## Revision History
[Table]

### 1.1 Section Ordering

Sections MUST appear in this order:

1. Normative Status
2. Authority
3. Terminology
4. [Core content sections — domain specific]
5. Layer Boundaries
6. Security
7. Performance
8. Compatibility
9. Compliance
10. Future Evolution
11. Runtime Independence
12. Acceptance Criteria
13. References
14. Compliance Matrix
15. Revision History

### 1.2 Section Numbering

- All RFCs use unnumbered section headings: `## Terminology`, `## Layer Boundaries`, etc.
- The exception is RFC-0301 (Workflow Overview), which uses numbered headings `## 42` through `## 88` to reserve headings 1–41 for the metadata header block. This convention is deprecated and new RFCs MUST use unnumbered headings.

---

## 2. Language

### 2.1 RFC 2119 Keywords

The following keywords MUST be used consistently:

| Keyword | Meaning | Usage |
|---|---|---|
| **MUST** | Absolute requirement | "The implementation MUST..." |
| **MUST NOT** | Absolute prohibition | "The implementation MUST NOT..." |
| **REQUIRED** | Same as MUST | Rarely used; prefer MUST |
| **SHALL** | Same as MUST | Rarely used; prefer MUST |
| **SHALL NOT** | Same as MUST NOT | Rarely used; prefer MUST NOT |
| **SHOULD** | Strong recommendation | "The implementation SHOULD..." |
| **SHOULD NOT** | Strong discouragement | "The implementation SHOULD NOT..." |
| **RECOMMENDED** | Same as SHOULD | Rarely used; prefer SHOULD |
| **MAY** | Optional | "The implementation MAY..." |
| **OPTIONAL** | Same as MAY | Rarely used; prefer MAY |

### 2.2 Prohibited Language

The following language patterns MUST NOT appear in normative sections:

- ~~"should probably"~~ — replace with "SHOULD"
- ~~"might want to"~~ — replace with "MAY"
- ~~"it is recommended that"~~ — replace with "SHOULD"
- ~~"implementors are advised to"~~ — replace with "SHOULD"
- ~~"can be done by"~~ — replace with "MAY"
- ~~"could potentially"~~ — remove qualifier, use "MAY"
- ~~"we suggest"~~ — replace with "SHOULD"
- ~~"you should"~~ — replace with "The implementation SHOULD"

### 2.3 Tone

- Use **active voice** exclusively.
- Use **present tense** for requirements.
- Address **"The implementation"** not **"you"** or **"the developer"**.
- Use **third person** exclusively.

---

## 3. Terminology

### 3.1 Canonical Terms

The following terms have fixed definitions across ALL RFCs. Every RFC MUST use these exact definitions:

| Term | Definition | Authoritative RFC |
|---|---|---|
| Workflow | A declarative directed graph specification expressing WHAT must happen, not HOW. | RFC-0301 |
| Execution | The process of evaluating a workflow graph and activating nodes to produce results. | RFC-0303 |
| Run | A single invocation of a workflow definition producing a workflow instance. | RFC-0301 |
| Task | An atomic unit of work within a workflow, represented as a node. | RFC-0301 |
| Node | A graph element representing an atomic unit of work with defined inputs and outputs. | RFC-0301 |
| Context | The scoped data environment available to nodes during execution. | RFC-0307 |
| Frame | A discrete unit of visual data processed by vision nodes. | RFC-0301 |
| Tick | A single evaluation cycle of the workflow scheduler. | RFC-0301 |
| Scheduler | The component that determines WHEN and WHERE each node is executed. | RFC-0312 |
| Trigger | An event or condition that initiates workflow execution. | RFC-0311 |
| Condition | A boolean expression that evaluates to determine execution paths. | RFC-0310 |
| State | The current snapshot of a workflow instance's execution position and data. | RFC-0306 |
| Checkpoint | A serialized snapshot of execution state used for recovery. | RFC-0315 |
| Recovery | The process of restoring workflow execution from a checkpoint after failure. | RFC-0315 |
| Manifest | A structured document declaring workflow metadata, dependencies, and capabilities. | RFC-1005 |
| Version | A semantic identifier (MAJOR.MINOR.PATCH) for a specific snapshot of a workflow definition. | RFC-0318 |

### 3.2 Term Usage Rules

- Every term defined in RFC-0301 MUST be referenced with "per RFC-0301" on first use.
- Domain-specific terms MUST be defined in the RFC's Terminology section.
- Acronyms MUST be spelled out on first use: "Inter-Process Communication (IPC)".
- Terms MUST NOT be used interchangeably: "Run" ≠ "Execution" ≠ "Task".

---

## 4. Cross-References

### 4.1 Mandatory Cross-References

Whenever these concepts are mentioned, the following RFCs MUST be referenced:

| Concept | Must Reference |
|---|---|
| Workflow Runtime | RFC-0304 |
| Scheduler | RFC-0312 |
| Recovery | RFC-0315 |
| Debugging | RFC-0316 |
| Validation | RFC-0317 |
| Versioning | RFC-0318 |
| Security | RFC-0319 |
| Performance | RFC-0320 |
| Observability | RFC-0321 |
| Extension | RFC-0322 |
| Plugin Integration | RFC-0323 |
| Storage | RFC-0324 |
| AI | RFC-0325 |
| Vision | RFC-0326 |
| IPC | RFC-0327 |
| Serialization | RFC-0328 |
| Compatibility | RFC-0329 |
| Compliance | RFC-0330 || Testing | RFC-0331 || Migration | RFC-0332 || SDK | RFC-0333 |

### 4.2 Reference Format

- In prose: "per RFC-0304" or "as defined in RFC-0304".
- In tables: "RFC-0304" with a link or description.
- In header metadata: "Related RFCs:" section listing all cross-references.
- In References section: Full table with RFC number, title, and description.

### 4.3 Self-Reference Prohibition

An RFC MUST NOT reference itself in its "Related RFCs" header section.

---

## 5. Diagrams

### 5.1 Mermaid Diagrams

All Mermaid diagrams MUST follow these rules:

- Use **consistent node naming** across all diagrams in the repository.
- Node IDs MUST be **unique** within each diagram.
- No **duplicate nodes** (same label, different ID).
- No **cyclic error paths** unless explicitly modeled as recovery loops.
- Diagrams MUST **match the text description** — no orphan diagrams.
- Use mermaid fenced code blocks exclusively.
- Label nodes with **human-readable names**, not internal IDs.

### 5.2 Diagram Types

| Type | Use Case | Example |
|---|---|---|
| graph TB / graph LR / graph TD | General flow, architecture | RFC-0301 architecture diagram |
| sequenceDiagram | Interaction between components | RFC-0327 IPC diagram |
| stateDiagram-v2 | State transitions | RFC-0306 state diagram |
| classDiagram | Type relationships | RFC-0302 AST model |

---

## 6. Acceptance Criteria

### 6.1 Format

Every acceptance criterion MUST follow this exact format:

| # | Criterion | Verification Method |
|---|---|---|
| AC-XX | The implementation MUST [specific, testable requirement]. | [Specific test name] |

### 6.2 Writing Rules

- Criteria MUST use **"The implementation MUST"** — never "should", "could", or "will".
- Criteria MUST be **measurable** and **verifiable**.
- Verification Method MUST name a **specific test** or **analysis technique**.
- Group criteria by domain: Architecture, Security, Performance, Compatibility, Compliance.

### 6.3 Examples

**BAD** — "The scheduler MUST be deterministic."

**GOOD** — "Running the same workflow twice with identical inputs MUST produce identical execution ordering. Verification: Same Event IDs, Same State IDs, Same Output Graph."

**BAD** — "The implementation should support recovery."

**GOOD** — "The implementation MUST support six recovery strategies: Restart, Resume, Rollback, Compensate, Skip, Abort. Verification: Strategy enumeration test."

---

## 7. Naming Conventions

### 7.1 File Names

- RFC files: RFC-XXXX-short-name.md
- Catalog files: workflow-[category].md
- Schema files: schemas/workflow/[entity].json
- Template files: RFC_TEMPLATE.md

### 7.2 Section Names

- Use **Title Case** for section headers.
- Use **short, descriptive names** (1-3 words).
- Avoid generic names like "Overview", "Details", "Summary".

### 7.3 Table Names

- Tables MUST have descriptive captions.
- Column names MUST be singular nouns.
- Use consistent column order across similar tables.

---

## 8. Versioning

All RFC versioning follows RFC_VERSIONING_POLICY.md. This section provides a quick reference only.

For full versioning rules, status lifecycles, category classifications, and compatibility tracking, see [RFC_VERSIONING_POLICY.md](RFC_VERSIONING_POLICY.md).

### 8.1 Quick Reference

| Version Change | Example | Description |
|---|---|---|
| MAJOR (1.x → 2.x) | Removed term, changed interface | Breaking change |
| MINOR (x.1.x → x.2.x) | New section, new criteria | Backward-compatible addition |
| PATCH (x.y.1 → x.y.2) | Typo fix, diagram fix | Non-substantive correction |
## 9. Layer Independence

### 9.1 Platform Neutrality

Every RFC MUST include a "Runtime Independence" section that explicitly excludes assumptions about:

- Programming languages (Rust, Node.js, TypeScript, Go, Python, etc.)
- Runtime environments (Electron, Tauri, Browser, Desktop, Server)
- Storage backends (SQLite, PostgreSQL, MongoDB, Redis, etc.)
- Operating systems (Windows, Linux, macOS, etc.)
- Hardware architectures (CPU, GPU, FPGA, etc.)
- Threading models (single-threaded, multi-threaded, actor-based, etc.)
- Cloud providers (AWS, Azure, GCP, etc.)
- Container platforms (Docker, containerd, etc.)

### 9.2 Exception

Hardware-specific considerations (e.g., GPU for AI/Vision nodes) MUST be expressed in abstract terms — describing WHAT is needed, not HOW it is provided.

---

## 10. Compliance

### 10.1 ADS Compliance

Every RFC MUST reference:

- The ADS Constitution
- ADR-0012 (Contract-First Specification-Driven Development)
- ADR-0010 (Security Architecture, where applicable)

### 10.2 Compliance Verification

RFC compliance is verified through:

1. **Structural check**: All required sections present.
2. **Terminology check**: All terms match RFC-0301 definitions.
3. **Cross-reference check**: All mandatory references present.
4. **Style check**: RFC 2119 language, no prohibited patterns.
5. **Diagram check**: All Mermaid diagrams consistent and correct.
6. **Acceptance Criteria check**: All criteria verifiable and testable.

---

## 11. Future RFCs

New RFCs MUST be created using RFC_TEMPLATE.md and reviewed against this RFC_STYLE_GUIDE.md.

The Specification Committee reserves the right to update this style guide. Updates follow the same RFC process as any other specification.




