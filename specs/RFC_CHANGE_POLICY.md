# Atlas RFC Change Policy

> **Purpose**: Define the authoritative process for proposing, reviewing, approving, and retiring RFCs.  
> **Applies to**: All RFCs in specs/ and subdirectories.  
> **Owner**: Atlas Specification Committee  
> **Last Updated**: 2026-07-01  

---

## 1. Scope

This policy governs all modifications to accepted or proposed RFCs within the Atlas Specification System. It applies to:

- New RFC submissions
- Amendments to existing RFCs
- Status transitions (Proposed → Accepted → Active → Deprecated → Superseded)
- Breaking changes to normative content
- Non-breaking clarifications

### 1.1 Exceptions

The following are exempt from this policy:

- Typographical corrections that do not alter meaning
- Formatting improvements that do not change content
- Reference updates to external documents
- Catalog file content updates (governed by catalog maintenance procedures)

Changes that are exempt MUST still be recorded in the RFC's Revision History table.

---

## 2. Proposal Process

### 2.1 Who May Propose

Any individual with read access to the Atlas specification repository MAY submit an RFC change proposal. Proposals are submitted as pull requests against the target RFC file.

### 2.2 Proposal Requirements

Every proposal MUST include:

| Field | Description |
|---|---|
| RFC Number | The RFC being modified |
| Change Type | Breaking, Non-Breaking, Clarification, Typographical |
| Proposed Text | The exact text to be added, modified, or removed |
| Rationale | Why the change is necessary |
| Impact Assessment | Which downstream RFCs, schemas, and catalogs are affected |
| Migration Path | If breaking, how existing implementations migrate |

### 2.3 Proposal Classification

| Classification | Criteria | Review Path |
|---|---|---|
| Trivial | Typos, formatting, reference updates | Single reviewer approval |
| Clarification | Adds explanatory text without changing requirements | Two reviewer approval |
| Non-Breaking | Adds new sections, new criteria, new options | Specification Committee vote |
| Breaking | Changes normative requirements, removes sections, changes terminology | Specification Committee + ADR |

---

## 3. Review Process

### 3.1 Review Tiers

| Tier | Proposal Type | Reviewers | Approval Threshold |
|---|---|---|---|
| Tier 1 | Trivial | 1 reviewer | Unanimous |
| Tier 2 | Clarification | 2 reviewers | Unanimous |
| Tier 3 | Non-Breaking | 3 reviewers | 2/3 majority |
| Tier 4 | Breaking | Specification Committee | Supermajority (2/3) |

### 3.2 Review Timeline

| Tier | Response SLA | Decision SLA |
|---|---|---|
| Tier 1 | 48 hours | 72 hours |
| Tier 2 | 72 hours | 5 business days |
| Tier 3 | 5 business days | 10 business days |
| Tier 4 | 5 business days | 20 business days |

If the SLA expires without a decision, the proposal is automatically escalated to the next tier.

### 3.3 Review Checklist

Reviewers MUST verify:

1. The proposal follows the format in Section 2.2
2. The change does not contradict higher-level RFCs
3. The impact assessment is complete and accurate
4. The migration path (if applicable) is feasible
5. All affected downstream RFCs are identified
6. The change improves clarity or correctness

---

## 4. ADR Creation Requirements

An Architecture Decision Record (ADR) MUST be created when:

| Condition | ADR Type |
|---|---|
| An RFC change is breaking | RFC-Breaking-Change ADR |
| A new layer boundary is introduced | RFC-Layer ADR |
| Terminology is redefined | RFC-Terminology ADR |
| A conflict between RFCs is resolved | RFC-Conflict ADR |
| A subsystem departs from the standard pattern | RFC-Exception ADR |

An ADR is NOT required for:

- Trivial corrections
- Clarifications that do not change requirements
- Non-breaking additions that follow existing patterns

### 4.1 ADR Content

Every ADR MUST contain:

- Decision context (why the change is needed)
- Options considered (with trade-offs)
- The decision made
- Consequences (positive and negative)
- Related RFCs and their revision numbers
- Effective date

---

## 5. Breaking Changes

### 5.1 Definition

A breaking change is any modification that causes an existing conformant implementation to cease conforming to the revised RFC. This includes:

- Removing or renaming a normative term
- Changing the value of a MUST requirement
- Adding a new MUST requirement that was not previously implied
- Removing a section that implementations rely on
- Changing the structure of a defined interface or protocol

### 5.2 Breaking Change Process

1. **Proposal**: Submit a Tier 4 proposal with full impact assessment
2. **ADR**: Create an RFC-Breaking-Change ADR documenting the decision
3. **Announcement**: Publish a deprecation notice in the affected RFCs
4. **Transition Period**: Minimum 90 days between announcement and effective date
5. **Implementation Window**: Affected implementations have one major version cycle to migrate
6. **Enforcement**: After the transition period, the old behavior is non-conformant

### 5.3 Deprecation Notice Format

Every breaking change MUST include a deprecation notice in the affected RFC:

| Field | Value |
|---|---|
| Deprecated Element | [Name of element being deprecated] |
| Deprecated In | [RFC version and date] |
| Removal Scheduled | [Effective date] |
| Replacement | [New element that replaces it] |
| Migration Guide | [Link to migration documentation] |

---

## 6. Deprecated RFCs

### 6.1 Deprecation Criteria

An RFC MAY be deprecated when:

- It is superseded by a newer RFC
- Its domain is no longer relevant to the system
- It contains requirements that cannot be practically implemented
- It conflicts with higher-level RFCs that cannot be resolved

### 6.2 Deprecation Process

1. The Specification Committee votes to deprecate (2/3 majority)
2. A deprecation notice is added to the RFC header: Status: Deprecated
3. A Deprecated In and Replacement RFC field are added
4. The RFC remains in the repository for historical reference
5. All cross-references to the deprecated RFC are updated in downstream RFCs

### 6.3 Deprecated RFC Status

A deprecated RFC:

- MUST NOT be cited as the authoritative source for new implementations
- MAY be cited for historical context
- MUST remain readable and unmodified (preserving the deprecation notice)
- MUST be included in the Revision History of its replacement RFC

---

## 7. Experimental RFCs

### 7.1 Experimental Classification

An RFC is classified as Experimental when:

- It proposes a novel concept not yet validated
- It addresses a future capability not yet required
- It explores alternative designs for comparison
- It is intended for community feedback before commitment

### 7.2 Experimental RFC Requirements

Experimental RFCs MUST:

- Have Status: Experimental in the header
- Include a Validation Plan section describing how the concept will be validated
- Include a Success Criteria section defining when the RFC graduates from Experimental
- Be reviewed by at least 2 reviewers (Tier 2 minimum)
- Have a sunset clause: if not graduated within 12 months, the RFC is archived

### 7.3 Graduation from Experimental

An Experimental RFC graduates to Proposed when:

- The validation plan has been executed successfully
- The success criteria have been met
- The Specification Committee votes to graduate (simple majority)
- A graduation notice is added to the Revision History

---

## 8. Conflict Resolution

### 8.1 Conflict Types

| Type | Description | Resolution |
|---|---|---|
| Terminology Conflict | Same term used with different meanings | ADR-Conflict + RFC amendment |
| Requirement Conflict | Two RFCs impose contradictory requirements | ADR-Conflict + RFC amendment |
| Scope Conflict | Two RFCs cover overlapping domain | ADR-Conflict + scope clarification |

### 8.2 Resolution Process

1. The conflict is identified and documented
2. An RFC-Conflict ADR is created
3. Affected RFC owners are notified
4. The Specification Committee reviews the ADR
5. A resolution is voted on (supermajority for breaking changes)
6. All affected RFCs are amended simultaneously

---

## 9. Emergency Changes

### 9.1 Emergency Criteria

Emergency changes bypass the normal review process only when:

- A security vulnerability is discovered in the specification
- A critical defect prevents any conformant implementation
- The specification contradicts a legal or regulatory requirement

### 9.2 Emergency Process

1. The change is proposed with an emergency justification
2. Two Specification Committee members approve within 24 hours
3. The change is merged with an emergency annotation
4. A full retrospective ADR is created within 5 business days
5. The change is reviewed through the normal process at the next committee meeting

---

## 10. Governance

- The **Atlas Specification Committee** owns this policy
- This policy follows the same RFC process as any other specification
- Changes to this policy require a Tier 4 proposal
- The policy is reviewed annually by the Specification Committee
