# Example: Good RFC

> **Purpose**: Template for writing RFCs that pass review on first submission.
> **Reference**: specification-rules.md for full RFC requirements.

---

## Structure

Every RFC MUST follow this structure:

`markdown
# RFC-XXXX: Title

RFC: RFC-XXXX
Title: Title
Status: Draft | Review | Accepted | Frozen
Version: 1.0.0
Author: Name
Created: YYYY-MM-DD
Last Updated: YYYY-MM-DD
Depends On:
  - RFC-YYYY Title
Required By:
  - RFC-ZZZZ Title
Category: Subsystem
Layer: Layer Name
Normative: YES/NO
Audience: Target audience
ADR References:
  - ADR-NNNN
Related RFCs:
  - RFC-YYYY Title
Target Release: 1.0.0
Review Cycle: Review cycle
Compatibility: Compatible with Spec X.Y

---

## Normative Status
This specification is Normative. Every ... implementation MUST conform ...

## Authority
This RFC is the authoritative specification for the domain ...

## Terminology
| Term | Definition | Source |
|------|-----------|--------|

## Layer Boundaries
### Responsibilities
- What this RFC defines

### Non-Responsibilities
- What this RFC does NOT define

### Dependencies
| Dependency | Direction | Description |

### Consumers
- Who consumes this RFC

### Providers
- What this RFC provides

### Forbidden Dependencies
- What this RFC MUST NOT depend on

## Main Content Sections
...

## Compliance Checklist
| # | Requirement | Verification Method |

## Acceptance Criteria
### AC-XXX
- **Requirement**: ...
- **Verification**: ...
- **Expected Result**: ...

## References

## Changelog

## Compatibility

## Runtime Independence
This specification is completely independent of any runtime implementation platform ...

## Revision History
| Version | Status | Date | Author | Notes |
`

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing Normative Status | Add "This specification is Normative" |
| No Terminology table | Add all key terms with definitions |
| No Layer Boundaries | Add all 5 subsections |
| No Runtime Independence | Add the full independence statement |
| Missing Acceptance Criteria | Add numbered AC-XXX with Requirement/Verification/Expected Result |
| No Compliance Checklist | Add numbered requirements with verification methods |
| No Revision History | Add version table |
| Status is Draft but content is complete | Change to Accepted or Frozen |

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
