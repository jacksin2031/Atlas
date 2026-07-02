# Atlas Specification Change Process

> **Purpose**: Defines how to modify any artifact in the Atlas specification repository.  
> **Applies to**: All files under specs/ including RFCs, catalogs, ADRs, governance docs, and implementation.  
> **Owner**: Atlas Specification Committee  
> **Last Updated**: 2026-07-02  
> **Related**: [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md), [RFC_CHANGE_POLICY.md](RFC_CHANGE_POLICY.md), [SPECIFICATION_PRINCIPLES.md](SPECIFICATION_PRINCIPLES.md), [LAYER_MODEL.md](LAYER_MODEL.md)  

---

## 1. Change Classification

Every modification to the specification repository falls into one of four categories. The category determines the required process.

| Category | Description | Examples | Process |
|---|---|---|---|
| **Editorial** | Wording, formatting, typos, reference updates | Fix a typo, update a URL, reword a section | Direct commit |
| **Catalog Addition** | Adding a new entry to a catalog | Add a new message type, channel ID, or error code | Domain owner approval |
| **Specification Change** | Modifying normative content | Change a MUST requirement, add/remove an RFC section | RFC amendment process |
| **Governance Change** | Modifying governance documents | Change RFC_GOVERNANCE.md, SPECIFICATION_PRINCIPLES.md | Spec Committee vote |

---

## 2. When to Use Each Path

### 2.1 Direct Commit (Editorial)

Use when the change:
- Fixes a typo, grammar error, or formatting issue.
- Updates a reference to another document (e.g., changes an RFC number in a citation).
- Improves clarity without changing meaning.
- Adds or updates the revision history table.

**Approval**: Any reviewer may approve editorial changes. No formal vote required.

**Example**: Changing "the system MUST support" to "the system MUST support" (typo fix in surrounding text).

### 2.2 Domain Owner Approval (Catalog Addition)

Use when the change:
- Adds a new entry to an existing catalog (e.g., a new message ID in ipc/catalog/messages.md).
- Adds a new value to an enumerated list.
- Does NOT change the conceptual model behind the catalog.

**Approval**: The domain owner for the catalog's parent RFC.

**Example**: Adding MSG-0041 to the IPC messages catalog.

### 2.3 RFC Amendment Process (Specification Change)

Use when the change:
- Modifies normative content in an existing RFC.
- Adds a new section to an RFC.
- Removes or renames a concept defined in an RFC.
- Changes the scope or layer assignment of an RFC.
- Creates a new RFC.
- Moves an RFC between domains.

**Approval**: Per [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md) voting rules for the RFC's domain.

**Sub-rules**:

| Change Type | Additional Requirement |
|---|---|
| Non-breaking normative change | Standard RFC review per [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md) |
| Breaking normative change | Breaking Change Notice (BCN) + Spec Committee 2/3 vote |
| New RFC | Full RFC submission per [RFC_TEMPLATE.md](RFC_TEMPLATE.md) |
| RFC removal | Deprecation process per [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md) §7 |
| Cross-domain RFC | Joint review from ALL affected domains |

### 2.4 Spec Committee Vote (Governance Change)

Use when the change:
- Modifies [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md), [SPECIFICATION_PRINCIPLES.md](SPECIFICATION_PRINCIPLES.md), [LAYER_MODEL.md](LAYER_MODEL.md), or any other governance document.
- Changes the layer assignment of a domain.
- Creates or dissolves a domain.
- Changes voting thresholds or review authority.

**Approval**: Spec Committee unanimous consent.

---

## 3. When to Create an ADR

An **Architecture Decision Record (ADR)** is required when:

| Condition | Example |
|---|---|
| The decision affects multiple domains | Choosing a serialization format used by both IPC and Plugin |
| The decision is irreversible or costly to reverse | Choosing the Runtime service model |
| The decision establishes a new architectural pattern | Introducing a new extension mechanism |
| The decision conflicts with an existing RFC | Proposing a change that RFC-0003 doesn't support |
| The decision is strategic (not tactical) | Choosing between event-driven vs. request-response architecture |

An ADR is **NOT required** when:

| Condition | Example |
|---|---|
| The decision is within a single domain's scope | Choosing a specific error code format in Storage |
| The decision is editorial or cosmetic | Renaming a section for clarity |
| The decision follows an existing RFC pattern | Using the existing extension mechanism |
| The decision is tactical implementation detail | Choosing which function to call |

**ADR Process**:
1. Author drafts the ADR following the template in .ai/issue-template.md or the project's ADR format.
2. ADR is reviewed by all domain owners affected by the decision.
3. ADR is accepted by Spec Committee vote (simple majority for standard decisions, 2/3 for architectural decisions).
4. Accepted ADRs are referenced by subsequent RFCs.

---

## 4. When to Create a New RFC

A **new RFC** is required when:

| Condition | Example |
|---|---|
| Defining a new capability or interface | New workflow action type |
| Specifying a protocol or contract | New IPC message type |
| Establishing a new domain or subsystem | New AI model routing protocol |
| Modifying an existing RFC's scope significantly | Extending Storage to support distributed transactions |

A **new RFC is NOT required** when:

| Condition | Example |
|---|---|
| The change can be expressed as a catalog addition | Adding a new error code to an existing catalog |
| The change is editorial | Rewording an existing section |
| The change is covered by an existing RFC's extension mechanism | Using RFC-0112 to extend IPC |
| The change is experimental and provisional | Prototyping a new feature |

---

## 5. When a Document Update Suffices

A **document update** (no RFC needed) is sufficient when:

| Condition | Example |
|---|---|
| Updating implementation notes | Changing a code example |
| Updating design diagrams | Refreshing a drawio file |
| Updating catalog enumerations | Adding a new channel ID |
| Editorial changes to governance docs | Fixing a typo in RFC_STYLE_GUIDE.md |
| Adding new examples or guidance | Adding a usage example to an existing RFC |

---

## 6. Review Gate

Every change that is not a pure editorial fix must pass through a **Review Gate**:

1. **Self-Review**: Author checks the change against [SPECIFICATION_PRINCIPLES.md](SPECIFICATION_PRINCIPLES.md).
2. **Peer Review**: A domain expert reviews for technical correctness.
3. **Cross-Domain Check**: If the change affects multiple domains, each domain owner reviews.
4. **Consistency Audit**: The Spec Committee checks for cross-RFC consistency (per Principle P10).

**Review Gate Criteria** (must pass all):
- [ ] Change is classified correctly (editorial / catalog / spec / governance)
- [ ] No duplicate definitions introduced (per P2)
- [ ] References are used instead of copy-paste (per P3)
- [ ] Terminology matches [glossary.md](glossary.md)
- [ ] Layer dependencies are respected (per [LAYER_MODEL.md](LAYER_MODEL.md))
- [ ] RFC 2119 terminology is used correctly (per P6)

---

## 7. Approval Gate

After passing the Review Gate, the change must pass the **Approval Gate**:

| Change Category | Approver | Vote Required |
|---|---|---|
| Editorial | Any reviewer | N/A |
| Catalog Addition | Domain owner | N/A |
| Specification Change | Per [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md) §3 | Simple / 2/3 / Unanimous |
| Governance Change | Spec Committee | Unanimous |

**Approval Gate Criteria** (must pass all):
- [ ] Review Gate passed
- [ ] Breaking Change Notice filed (if applicable)
- [ ] Migration path provided (if breaking)
- [ ] All affected domain owners notified
- [ ] Revision history updated in all modified documents

---

## 8. Change Process Flowchart

`
Change Proposed
     │
     ▼
┌──────────────┐
│ Classify     │
│ Change Type  │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────────┐
│ Editorial?   │────▶│ Direct Commit    │
└──────┬───────┘     └──────────────────┘
       │
       ▼
┌──────────────┐     ┌──────────────────┐
│ Catalog Add? │────▶│ Domain Owner     │
└──────┬───────┘     │ Approval         │
       │             └──────────────────┘
       ▼
┌──────────────┐
│ Spec Change? │────▶│ RFC Amendment    │
└──────┬───────┘     │ Process          │
       │             └──────────────────┘
       ▼
┌──────────────┐
│ Governance?  │────▶│ Spec Committee   │
└──────────────┘     │ Unanimous Vote   │
`

---

## 9. Emergency Changes

For security vulnerabilities or critical defects:

1. **Author** creates an emergency change proposal with justification.
2. **Spec Committee Chair** approves the emergency path (bypasses Review Gate but not Approval Gate).
3. **Approval** follows the normal gate for the change category.
4. **Post-mortem**: Within 2 releases, the change is reviewed for process improvement.

Emergency changes **cannot** bypass Breaking Change policies.

---

*This document is part of the Atlas Specification hierarchy. For governance, see [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md). For principles, see [SPECIFICATION_PRINCIPLES.md](SPECIFICATION_PRINCIPLES.md). For layers, see [LAYER_MODEL.md](LAYER_MODEL.md). For domain ownership, see [DOMAIN_OWNERS.md](DOMAIN_OWNERS.md).*

