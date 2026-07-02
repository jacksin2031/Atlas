# Atlas RFC Versioning and Status Policy

> **Purpose**: Define the versioning scheme, status lifecycle, and classification rules for all Atlas RFCs.  
> **Applies to**: All RFCs in specs/ and subdirectories.  
> **Owner**: Atlas Specification Committee  
> **Last Updated**: 2026-07-01  

---

## 1. Semantic Versioning for RFCs

All RFCs follow Semantic Versioning (semver 2.0.0) with the following interpretation:

### 1.1 MAJOR Version

Incremented when:

| Change Type | Examples |
|---|---|
| Architecture change | New layer boundaries, new subsystem |
| Breaking normative change | Removed MUST requirement, renamed term, changed interface |
| Structural change | Changed the fundamental model described in the RFC |
| Scope change | RFC now covers a different domain |

A MAJOR version increment implies that any implementation conforming to the previous MAJOR version MAY be non-conformant with the new version.

#### MAJOR Version Examples

- RFC-0301 Section 4.2 changes from 15 action types to 17 action types (breaking)
- RFC-0312 removes the Tick concept entirely (breaking)
- RFC-0304 changes the Runtime service interface (breaking)

### 1.2 MINOR Version

Incremented when:

| Change Type | Examples |
|---|---|
| New normative section | Added new requirement category |
| New acceptance criteria | Added testable criteria |
| New term definition | Added term to Terminology table |
| New cross-reference | Added reference to another RFC |
| Expanded examples | Added clarification examples |
| New Future Evolution entry | Added planned extension |

A MINOR version increment is backward compatible. Implementations conforming to the previous MINOR version within the same MAJOR version remain conformant.

#### MINOR Version Examples

- RFC-0309 adds AC-11 through AC-15 to Acceptance Criteria
- RFC-0312 adds a new Scheduling Policy section
- RFC-0301 adds a new term to the Terminology table

### 1.3 PATCH Version

Incremented when:

| Change Type | Examples |
|---|---|
| Grammar correction | Spelling, punctuation, syntax |
| Formatting fix | Table alignment, markdown syntax |
| Diagram fix | Mermaid diagram correction |
| Reference fix | Updated cross-reference to another RFC |
| Clarification | Adding explanatory text without changing requirements |

A PATCH version increment is strictly non-substantive. The normative meaning of the RFC is unchanged.

#### PATCH Version Examples

- RFC-0314 fixes a typo in Section 3.2
- RFC-0320 updates a Mermaid diagram node name
- RFC-0301 corrects a reference from RFC-0315 to RFC-0312

---

## 2. RFC Status Lifecycle

### 2.1 Status Values

| Status | Description | Can Be Modified | Can Be Cited |
|---|---|---|---|
| Draft | Under active design, not yet submitted | Yes | No |
| Review | Submitted for review, under discussion | Yes (with review notes) | No |
| Proposed | Accepted for inclusion, awaiting implementation | Yes (via change policy) | Yes (non-normative) |
| Accepted | Approved, ready for implementation | Yes (via change policy) | Yes (normative) |
| Active | Implemented and deployed | Yes (minor changes only) | Yes (normative) |
| Experimental | Novel concept under validation | Yes | No (experimental only) |
| Deprecated | Planned for removal, migration path provided | No (except deprecation notice) | Yes (historical) |
| Superseded | Replaced by a newer RFC | No | No (redirect to successor) |
| Frozen | Architecture complete, only bug fixes | No (bug fixes only) | Yes (normative) |

### 2.2 Status Transitions

`
Draft → Review → Proposed → Accepted → Active → Frozen
                                          ↓
                                       (bug fixes only)

Experimental → (graduation path) → Proposed → Accepted → Active
Deprecated → Superseded → (archived)
`

#### Transition Rules

| From | To | Requirement |
|---|---|---|
| Draft | Review | Author submits RFC for review |
| Review | Proposed | Specification Committee approves (2/3 majority) |
| Proposed | Accepted | Implementation exists and validates the RFC |
| Accepted | Active | Implementation is deployed in production |
| Active | Frozen | Architecture review confirms no further changes needed |
| Active | Deprecated | Specification Committee votes (2/3 majority) |
| Deprecated | Superseded | Replacement RFC is Accepted |
| Experimental | Proposed | Validation plan succeeded, committee votes (simple majority) |
| Experimental | Archived | Sunset clause expired without graduation |

### 2.3 Status-Specific Requirements

#### Draft

- No formal requirements
- MAY be modified freely
- MUST NOT be cited by other RFCs
- SHOULD use RFC_TEMPLATE.md structure

#### Review

- MUST follow RFC_TEMPLATE.md
- MUST include all required sections
- MUST pass RFC_REVIEW_CHECKLIST.md
- Reviewers document findings in review notes

#### Proposed

- MUST have Revision History with initial publication entry
- MUST include all normative sections
- MUST pass full RFC_REVIEW_CHECKLIST.md
- MAY be amended via the change policy

#### Accepted

- MUST have all acceptance criteria defined
- MUST have complete cross-references
- MUST have Revision History maintained
- MUST be cited by downstream RFCs

#### Active

- MUST have at least one conformant implementation
- MUST have deployment evidence
- MUST be reviewed annually
- MUST have performance metrics recorded

#### Frozen

- MUST have architecture review sign-off
- MAY only receive bug fix changes
- MUST document all changes in Revision History
- MUST have no open pull requests

#### Deprecated

- MUST have a replacement RFC identified
- MUST have a migration path documented
- MUST have a deprecation date in Revision History
- MUST remain readable but not normative

#### Superseded

- MUST reference the successor RFC
- MUST NOT be modified (preserved for history)
- MUST be archived after 2 years
- MUST have all cross-references updated to successor

---

## 3. Category Classification

### 3.1 Category Values

| Category | Description | Requirements |
|---|---|---|
| Core | Foundational specification that others depend on | Highest review bar, frozen status target |
| Standard | Cross-cutting specification used by multiple subsystems | Full review, annual review |
| Experimental | Novel concept under exploration | Lower review bar, sunset clause |

### 3.2 Category Rules

- A Core RFC MAY depend on other Core RFCs and Standard RFCs
- A Standard RFC MAY depend on Core RFCs and other Standard RFCs
- An Experimental RFC MAY depend on Core, Standard, or Experimental RFCs
- No RFC MAY depend on a Deprecated or Superseded RFC (except for historical reference)

---

## 4. Version Numbering in Headers

### 4.1 Header Fields

Every RFC header MUST include:

| Field | Format | Example |
|---|---|---|
| Version | semver (MAJOR.MINOR.PATCH) | 1.2.0 |
| Spec Version | semver range (for compatibility) | >= 1.0.0 < 2.0.0 |
| ADS Version | semver (for system compatibility) | 1.0.0 |

### 4.2 Version Assignment Rules

| Action | Version Change |
|---|---|
| Initial publication | 1.0.0 |
| Trivial correction | 1.0.1 |
| New section added | 1.1.0 |
| Breaking change | 2.0.0 |
| Superseded by new RFC | N/A (use Superseded By header) |

---

## 5. Revision History Maintenance

### 5.1 Required Entries

Every RFC MUST maintain a Revision History table with entries for:

| Entry | When Created |
|---|---|
| Initial publication | When RFC is first submitted |
| Each version change | When MAJOR, MINOR, or PATCH is incremented |
| Status change | When RFC transitions between statuses |
| Deprecation | When RFC is marked Deprecated |
| Supersession | When RFC is marked Superseded |

### 5.2 Entry Format

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-01-01 | Author Name | Initial publication |
| 1.1.0 | Proposed | 2026-07-01 | Author Name | Added Terminology, Layer Boundaries, Acceptance Criteria |
| 2.0.0 | Accepted | 2027-01-01 | Author Name | Breaking: Changed action type enumeration from 15 to 17 |

### 5.3 Notes Format

The Notes field MUST follow this pattern:

- Start with the change type: Added, Modified, Removed, Fixed, Breaking
- Describe what changed concisely
- Reference affected sections if applicable

---

## 6. Compatibility Tracking

### 6.1 Compatibility Declaration

Every RFC header MUST include a Compatibility field:

| Value | Meaning |
|---|---|
| Compatible with Spec X.x | Fully compatible with the stated specification version |
| Compatible with Spec X.x (partial) | Partially compatible; exceptions documented in RFC |
| Incompatible with Spec X.x | Known incompatibilities; migration path documented |
| N/A | Not applicable (e.g., experimental RFCs) |

### 6.2 Compatibility Verification

Before an RFC transitions from Proposed to Accepted, the Specification Committee MUST verify:

1. The RFC does not conflict with any Active or Frozen RFC
2. All cross-references resolve to valid RFCs
3. The acceptance criteria can be tested against existing implementations
4. The versioning trajectory is consistent with the RFC's category
