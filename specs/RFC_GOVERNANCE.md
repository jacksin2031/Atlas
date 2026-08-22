# Atlas RFC Governance

> **Purpose**: Defines the governance model for the Atlas RFC system — lifecycle, review authority, voting, breaking changes, and ownership.  
> **Applies to**: All RFCs in specs/ and subdirectories.  
> **Owner**: Atlas Specification Committee  
> **Last Updated**: 2026-07-02  
> **Related**: [RFC_CHANGE_POLICY.md](RFC_CHANGE_POLICY.md), [RFC_VERSIONING_POLICY.md](RFC_VERSIONING_POLICY.md), [RFC_REVIEW_CHECKLIST.md](RFC_REVIEW_CHECKLIST.md), [RFC_TEMPLATE.md](RFC_TEMPLATE.md)  

---

## 1. RFC Lifecycle

Every RFC progresses through a defined lifecycle. State transitions are strictly enforced.

### 1.1 Lifecycle States

| State | Description | Can Modify | Who Can Transition |
|---|---|---|---|
| **Proposed** | Initial submission, not yet assigned a reviewer | Author only | Author → Draft |
| **Draft** | Under active review by designated reviewer(s) | Author (per reviewer feedback) | Reviewer → Accepted / Deprecated |
| **Accepted** | Approved, ready for implementation | Author (implementation updates only) | Spec Committee → Active / Frozen |
| **Active** | Implemented and deployed in current release | Bug fixes only | Domain Owner → Frozen |
| **Frozen** | Architecture complete. Only bug fixes allowed. | Typo/clarification fixes only | Spec Committee → Superseded / Deprecated |
| **Superseded** | Replaced by a newer specification | N/A (read-only) | Spec Committee → (final state) |
| **Deprecated** | Planned for removal in future version | N/A (read-only) | Spec Committee → (final state) |
| **Experimental** | Provisional specification, not yet stable | Author freely | Author → Proposed / Superseded |

### 1.2 State Transition Rules

1. **Proposed → Draft**: Requires assignment of a reviewer from the relevant domain team.
2. **Draft → Accepted**: Requires positive review from assigned reviewer(s) AND approval from the domain owner.
3. **Draft → Deprecated**: Reviewer determines the RFC is fundamentally flawed or misaligned with architecture.
4. **Accepted → Active**: After implementation verification by the domain owner.
5. **Active → Frozen**: When the architecture reaches stability. Requires Spec Committee vote.
6. **Frozen → Superseded**: When a new RFC replaces the current one. Requires Spec Committee vote.
7. **Frozen → Deprecated**: When the feature is planned for removal. Requires Spec Committee vote.
8. **Any → Experimental**: Author may mark their own RFC as experimental at any time.
9. **Experimental → Proposed**: When the experiment is deemed stable enough for formal review.

### 1.3 Lifecycle Diagram

`
                    ┌─────────┐
                    │ Proposed │
                    └────┬────┘
                         │ Submit
                    ┌────▼────┐
               ┌───│  Draft   │───┐
               │   └────┬────┘   │
               │    Review     Reject
               │       │         │
               │  ┌────▼────┐   │
               │  │ Accepted │   │
               │  └────┬────┘   │
               │       │        │
          Implement │   │ Deploy │
               │       │        │
               │  ┌────▼────┐   │
               │  │  Active  │   │
               │  └────┬────┘   │
               │       │        │
               │  ┌────▼────┐   │
               │  │  Frozen  │   │
               │  └────┬────┘   │
               │       │        │
               │  ┌────▼────┐   │
               │  │Superseded│  │
               │  └─────────┘  │
               │               │
               ▼               ▼
         ┌──────────┐  ┌──────────┐
         │ Deprecated│  │Experimental│
         └──────────┘  └──────────┘
`

---

## 2. Review Authority

### 2.1 Domain-Based Review Authority

| RFC Range | Reviewer | Review Board | Voting Required |
|---|---|---|---|
| RFC-0001 – RFC-0014 (Runtime) | Runtime Arch Board | Core Architecture Group | 2/3 majority |
| RFC-0101 – RFC-0112 (IPC) | IPC Sub-team Lead | Core Architecture Group | Simple majority |
| RFC-0201 – RFC-0230 (Plugin) | Plugin Sub-team Lead | Core Architecture Group | Simple majority |
| RFC-0301 – RFC-0333 (Workflow) | Workflow Lead | Workflow Team + Core Arch | Simple majority |
| RFC-0401 – RFC-0425 (Storage) | Storage Lead | Storage Team + Core Arch | Simple majority |
| RFC-0501+ (Marketplace) | TBD | Spec Committee | 2/3 majority |
| RFC-0601+ (Knowledge) | TBD | Spec Committee | 2/3 majority |
| RFC-0701+ (Project) | TBD | Spec Committee | 2/3 majority |
| RFC-1001 – RFC-1006 (Common) | Spec Committee | All domain leads | Unanimous |
| Catalog files | Domain owner | Spec Committee (annual) | Simple majority |

### 2.2 Cross-Domain Review

When an RFC spans multiple domains (e.g., RFC-0323 workflow-plugin-integration), it requires **joint review** from ALL affected domain reviewers. No single reviewer may approve a cross-domain RFC without sign-off from the other domain(s).

### 2.3 Reviewer Qualifications

A reviewer must:
- Understand the domain's RFCs and their interdependencies.
- Have reviewed at least 3 RFCs in the domain previously.
- Not be the author of the RFC under review.
- Disclose any conflicts of interest before accepting review assignment.

---

## 3. Voting Procedures

### 3.1 Simple Majority (>50%)

Used for: IPC, Plugin, Workflow, Storage domain RFCs.

- Each domain reviewer casts one vote (Yes / No / Abstain).
- A RFC advances when more Yes votes than No votes are cast.
- Abstentions do not count toward the quorum.
- Minimum quorum: 2 reviewers must participate.

### 3.2 Two-Thirds Majority (≥66.7%)

Used for: Runtime domain RFCs, Marketplace, Knowledge, Project (deferred).

- Each domain reviewer casts one vote (Yes / No / Abstain).
- A RFC advances when Yes votes ≥ 2/3 of total eligible voters.
- Minimum quorum: 3 voters must participate.

### 3.3 Unanimous Consent

Used for: Common Models (RFC-1001–RFC-1006).

- Every domain lead must explicitly approve.
- Any single No vote blocks advancement.
- Abstentions are treated as approval only if the abstaining party confirms in writing.

### 3.4 Tie-Breaking

- In simple majority votes, ties are broken by the Core Architecture Group Chair.
- In two-thirds votes, ties require re-review with expanded reviewer panel.
- In unanimous votes, a tie means the RFC does not advance.

---

## 4. Breaking Change Policy

A **breaking change** is any modification that causes existing implementations to fail or behave incorrectly.

### 4.1 Breaking Change Categories

| Category | Example | Approval Required |
|---|---|---|
| **API Break** | Remove or rename a channel, message type, or interface | Spec Committee + 2/3 vote |
| **Protocol Break** | Change message format, serialization, or transport contract | Spec Committee + 2/3 vote |
| **Behavior Break** | Change lifecycle state transitions or error semantics | Domain Owner + Simple majority |
| **Schema Break** | Change JSON schema validation rules | Domain Owner + Simple majority |
| **Catalog Change** | Add new entry to a catalog (non-destructive) | Domain Owner |
| **Clarification** | Wording fix that does not change meaning | Domain Owner |

### 4.2 Breaking Change Process

1. **Announcement**: Author submits a Breaking Change Notice (BCN) as a comment on the RFC.
2. **Impact Assessment**: Reviewer identifies all affected RFCs, implementations, and downstream domains.
3. **Migration Path**: Author provides a backward-compatible migration path (minimum 1 release cycle).
4. **Vote**: Subject to the approval level in the table above.
5. **Deprecation Window**: Breaking changes enter a minimum 2-release deprecation period before removal.

---

## 5. RFC Categories

| Category | Description | Review Speed |
|---|---|---|
| **Core** | Fundamental to the Atlas architecture. Affects all domains. | Slowest (2/3 vote, all reviewers) |
| **Standard** | Defines behavior for a specific domain. Affects implementations. | Medium (simple majority) |
| **Experimental** | Provisional specification, not yet stable. Not yet reviewed. | Fastest (author discretion) |

### Category Rules

- **Core** RFCs must be marked Core if they affect more than one domain.
- **Standard** RFCs are limited to their own domain unless cross-domain review is granted.
- **Experimental** RFCs may change without notice. They do not require formal review but must be labeled Experimental.
- An RFC may not be promoted from Experimental to Standard without formal review.

---

## 6. Review SLA (Service Level Agreement)

| RFC Category | Max Review Time | Escalation Path |
|---|---|---|
| Core | 14 calendar days | Spec Committee Chair |
| Standard | 7 calendar days | Domain Owner |
| Experimental | 3 calendar days | Author discretion |

If a reviewer does not respond within the SLA, the RFC auto-advances to the next state unless a reviewer objects.

---

## 7. Deprecation Process

1. **Proposal**: Any stakeholder may propose deprecation by filing a comment on the RFC.
2. **Assessment**: Reviewer evaluates whether the RFC is truly obsolete or superseded.
3. **Notice**: The RFC status changes to Deprecated with a deprecation notice explaining why.
4. **Sunset Period**: Deprecated RFCs remain available for 2 full release cycles.
5. **Removal**: After the sunset period, the RFC is moved to a deprecated/ archive directory.

---

## 8. Emergency Override

In exceptional circumstances (security vulnerability, critical bug), the Spec Committee Chair may invoke an **Emergency Override**:

1. Emergency Override bypasses normal review SLA but not voting requirements.
2. Must be documented in the RFC with justification.
3. Expires after 2 releases unless confirmed by normal review.
4. Cannot be used to bypass Breaking Change policies.

---

## 9. Governance Evolution

This governance document itself is governed by:

- **Amendments** require Spec Committee unanimous consent.
- **Emergency amendments** may be proposed by any domain owner and require simple majority of all domain leads.
- **Annual review** on June 30 of each year.

---

*This document is part of the Atlas Specification hierarchy. For change procedures, see [RFC_CHANGE_POLICY.md](RFC_CHANGE_POLICY.md). For versioning, see [RFC_VERSIONING_POLICY.md](RFC_VERSIONING_POLICY.md). For the review checklist, see [RFC_REVIEW_CHECKLIST.md](RFC_REVIEW_CHECKLIST.md). For domain ownership, see [DOMAIN_OWNERS.md](DOMAIN_OWNERS.md). For change processes, see [SPECIFICATION_CHANGE_PROCESS.md](SPECIFICATION_CHANGE_PROCESS.md).*

