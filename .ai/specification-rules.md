# Atlas Specification Rules

> **Authority**: Governs how RFCs, ADRs, contracts, and glossary are created, modified, or retired.
> **Scope**: All subsystem teams (Runtime, Plugin, Workflow, Storage, IPC, AI, Vision, etc.).
> **Rule**: Specifications have higher priority than implementation. Never modify a Frozen RFC without an ADR.

---

## Specification Hierarchy

`
Constitution (highest — never changes without governance vote)
    ↓
ADR (Architecture Decision Records — changes require board approval)
    ↓
RFC (Specifications — changes require review cycle)
    ↓
Contract (Interface definitions — changes require consumer coordination)
    ↓
README / docs (Implementation details — changes freely, must stay in sync)
`

---

## When to Create an RFC

Create a new RFC when:

1. **New subsystem** is being designed (e.g., "Vision Capture Engine").
2. **New major feature** within a subsystem (e.g., "Plugin Hot Reload" within Plugin).
3. **Behavioral contract** is being defined (e.g., "Event Bus Priority Queues").
4. **Interface change** affects multiple consumers (e.g., "Service Contract v2").
5. **Cross-cutting concern** is being standardized (e.g., "Common Event Model").

RFC naming convention: {domain}-RFC-{NNNN}-{slug}.md

| Domain | Prefix | Range |
|--------|--------|-------|
| Runtime | RFC-0001–0099 | Core runtime |
| IPC | RFC-0101–0199 | Inter-process communication |
| Plugin | RFC-0201–0299 | Plugin system |
| Workflow | RFC-0301–0399 | Workflow engine |
| Storage | RFC-0401–0499 | Storage system |
| Common | RFC-1001–1099 | Cross-cutting concerns |
| Errors | RFC-2001–2099 | Error taxonomy |
| Events | RFC-3001–3099 | Event schemas |

---

## When to Modify an RFC

| Condition | Action |
|-----------|--------|
| Typo, formatting, clarifying language | Direct edit, note in changelog |
| Adding non-normative text (examples, notes) | Direct edit, note in changelog |
| Changing normative behavior | **Requires ADR** |
| Adding new requirements | **Requires ADR** |
| Removing requirements | **Requires ADR + governance vote** |
| Changing status from Draft to Frozen | **Requires board review** |

---

## When to Create an ADR

Create an ADR when:

1. **Architecture decision** that affects multiple subsystems.
2. **Trade-off analysis** between competing approaches.
3. **Breaking change** to an existing contract or RFC.
4. **New layer** or boundary being introduced.
5. **Technology choice** that constrains implementation (e.g., "Use WASM for plugins").
6. **Disagreement** between subsystem teams that needs resolution.
7. **Reversing** a previously made ADR.

ADR naming: dr-NNNN-{slug}.md

---

## When to Create a Contract

Create a contract when:

1. **Interface definition** that multiple modules implement.
2. **Protocol specification** for inter-process communication.
3. **Schema definition** for data exchange (JSON, protobuf, etc.).
4. **API boundary** between subsystems.

Contracts live in contracts/ organized by type:
- contracts/api/ — Service interfaces
- contracts/ipc/ — IPC protocols
- contracts/json/ — JSON schemas

---

## When to Update README Only

Update documentation (no RFC/ADR needed) when:

1. Implementation details change (e.g., "Changed from HashMap to BTreeMap").
2. Configuration file format is updated with backward-compatible fields.
3. Build or test instructions are corrected.
4. Example code is updated.
5. Internal module structure changes (file moves, renames).

---

## When to Update Glossary

Update the glossary when:

1. A **new term** is introduced that will be reused across RFCs.
2. An **existing term's definition** has changed meaning.
3. A term is **deprecated** and no longer in use.

Glossary updates do NOT require an ADR unless the term change affects an existing RFC.

---

## RFC Lifecycle

`
Draft → Review → Accepted → Frozen → (Deprecated | Retired)
`

| Stage | Description | Change Policy |
|-------|-------------|---------------|
| **Draft** | Under active development | Free changes, no ADR needed |
| **Review** | Submitted for review | Changes require reviewer approval |
| **Accepted** | Approved, ready for implementation | Changes require ADR |
| **Frozen** | Stable, in production | Changes require ADR + board approval |
| **Deprecated** | Being phased out | No new usage, existing usage allowed |
| **Retired** | Removed | Archive, do not reference |

---

## RFC Template

Every RFC MUST include these sections:

1. Header (RFC number, title, status, version, authors, dates)
2. Normative Status statement
3. Authority statement
4. Terminology table
5. Layer Boundaries (Responsibilities, Non-Responsibilities, Dependencies, Consumers, Providers, Forbidden Dependencies)
6. Main content (sections specific to the domain)
7. Compliance Checklist
8. Acceptance Criteria
9. References
10. Changelog
11. Compatibility statement
12. Runtime Independence statement
13. Revision History

---

## ADR Template

Every ADR MUST include:

1. Title and metadata (status, date, deciders)
2. Context (why this decision is needed)
3. Decision (what was decided)
4. Consequences (positive and negative outcomes)
5. Alternatives Considered (what else was evaluated)
6. Compliance requirements
7. References

---

## Governance

| Change Type | Requires |
|------------|----------|
| RFC typo fix | Author approval |
| RFC clarification | Author + reviewer approval |
| RFC normative change | ADR + board approval |
| ADR creation | Board approval |
| ADR reversal | Board + governance vote |
| Constitution change | Governance vote |
| New RFC domain | Governance vote |

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
