# Atlas Workflow

> **Authority**: Defines the end-to-end development lifecycle for every feature in Atlas.
> **Scope**: All agents, all tasks, all subsystems.
> **Rule**: No step may be skipped. No feature ships without completing all steps.

---

## Development Lifecycle

`
Issue
  ↓
Architecture
  ↓
RFC (Specification)
  ↓
Implementation Plan
  ↓
Implementation
  ↓
Review
  ↓
Test
  ↓
Merge
  ↓
Release
`

---

## Step 1 — Issue

**Purpose**: Define what needs to be done.

**Inputs**: User request, bug report, feature request, refactor ticket.

**Outputs**: Issue document with:
- Title
- Description (what and why)
- Acceptance criteria
- Assigned agent role
- Linked RFC (if applicable)
- Priority (P0–P3)

**Issue Types**:

| Type | When Used | Template |
|------|-----------|----------|
| Bug Report | Something is broken | issue-template.md (Bug) |
| Feature Request | New capability needed | issue-template.md (Feature) |
| Refactor Ticket | Code quality improvement | issue-template.md (Refactor) |
| Security Finding | Vulnerability detected | security-standard.md |
| Performance Issue | Budget exceeded | performance-standard.md |
| Release Task | Version preparation | pr-template.md |

**Gate**: Issue must have clear acceptance criteria before proceeding.

---

## Step 2 — Architecture

**Purpose**: Determine how the feature fits into the existing system.

**Inputs**: Issue document, existing RFCs, existing ADRs.

**Outputs**: Architecture decision with:
- Affected layers and subsystems
- New or modified interfaces
- Dependency graph changes
- Risk assessment
- Linked ADR (if new decision needed)

**Agent**: Architect

**Gate**: Architecture must not violate layer boundaries (architecture-rules.md).
If it does, create an ADR first.

---

## Step 3 — RFC (Specification)

**Purpose**: Define WHAT the feature does, not HOW.

**Inputs**: Architecture decision, issue acceptance criteria.

**Outputs**: RFC document with:
- Normative requirements
- State machines / sequence diagrams
- API contracts
- Compliance checklist
- Acceptance criteria
- Performance budgets

**Agent**: Architect + relevant subsystem agent

**Gate**: RFC must be in Accepted or Frozen status before implementation begins.
Draft RFCs are not implementable.

**Reference**: specification-rules.md for RFC creation/modification rules.

---

## Step 4 — Implementation Plan

**Purpose**: Break the RFC into executable steps.

**Inputs**: RFC document, coding-standard.md, implementation-roadmap.md.

**Outputs**: Step-by-step plan with:
- Ordered list of files/modules to create or modify
- Interface-first ordering (contracts → common → implementation)
- Test coverage per step
- Estimated complexity per step

**Agent**: Planner

**Gate**: Plan must follow the dependency graph.
No implementation may depend on a module that comes after it in the plan.

---

## Step 5 — Implementation

**Purpose**: Write code that satisfies the RFC.

**Inputs**: Implementation plan, RFC, contracts, coding-standard.md.

**Outputs**: Source code files with:
- Complete implementations (no TODOs, no placeholders)
- Unit tests for each module
- Lifecycle tests for stateful services
- Failure tests for error paths

**Agent**: Backend (or relevant subsystem agent)

**Gate**: Every file must pass self-review (Step 6) and testing (Step 7)
before proceeding.

**Order**:
1. Contracts (interfaces)
2. Common types (shared structs/enums)
3. Infrastructure (data access, external deps)
4. Services (business logic)
5. Runtime assembly (integration)

---

## Step 6 — Review

**Purpose**: Verify conformance before testing.

**Inputs**: Implementation code, review-checklist.md.

**Checks**:
- Architecture conformance (layer boundaries, no forbidden imports)
- Naming conventions (coding-standard.md)
- Security compliance (security-standard.md)
- Static analysis (no unused imports, no dead code)
- Contract compliance (all interfaces implemented)

**Agent**: Reviewer

**Gate**: All review checks must pass.
Failures are returned to Step 5 with specific feedback.

---

## Step 7 — Test

**Purpose**: Verify correctness and performance.

**Inputs**: Implementation code, testing-standard.md.

**Test Types**:
- Unit tests (every public function)
- Lifecycle tests (state machine transitions)
- Failure tests (error paths, edge cases)
- Integration tests (cross-module flows)
- Performance tests (budget compliance)

**Agent**: QA

**Gate**: All tests must pass.
Coverage must meet testing-standard.md thresholds.
Performance must stay within budgets.

---

## Step 8 — Merge

**Purpose**: Integrate changes into the main branch.

**Inputs**: Passed review, passed tests.

**Outputs**: Merged PR with:
- pr-template.md filled out
- Description of changes
- Verification checklist
- Impact matrix (what broke, what changed)
- Linked issue and RFC

**Agent**: Release

**Gate**: No merge without passed review and tests.
No merge without filled PR template.

---

## Step 9 — Release

**Purpose**: Package and ship the feature.

**Inputs**: Merged PR, changelog entries.

**Outputs**:
- Updated CHANGELOG.md
- Version bump (per RFC_VERSIONING_POLICY.md)
- Release notes
- Updated documentation

**Agent**: Release

**Gate**: Release must include all changes from the current sprint.
No partial releases.

---

## Workflow Variants

### Bug Fix

`
Issue (Bug) → Architecture (if needed) → Fix → Review → Test → Merge
`

Skip RFC step for bugs that match existing RFC behavior.
Create RFC if the bug reveals a missing specification.

### Refactor

`
Issue (Refactor) → Architecture → Implementation → Review → Test → Merge
`

No RFC needed if behavior does not change.
RFC required if interfaces or contracts change.

### Hotfix

`
Issue → Fix → Test → Merge → Release
`

Minimal steps for critical production issues.
Architecture and RFC steps may be deferred and completed retroactively.

### Audit

`
Issue (Audit) → Review (extended) → Report → Fix (if needed) → Merge
`

Audit is a read-only operation that may trigger bug fixes.

---

## Agent Assignment Matrix

| Step | Primary Agent | Secondary Agent |
|------|--------------|-----------------|
| Issue | Planner | — |
| Architecture | Architect | — |
| RFC | Architect | Subsystem agent |
| Plan | Planner | — |
| Implementation | Backend / Runtime / Plugin / etc. | — |
| Review | Reviewer | Security |
| Test | QA | — |
| Merge | Release | — |
| Release | Release | — |

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
