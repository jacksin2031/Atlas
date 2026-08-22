# Review Rules

> **Purpose**: Define what reviewers check and how they report findings.
> **Reference**: review-checklist.md for full review criteria.

---

## Review Categories

Every review checks these categories in order:

### 1. Architecture (Blocking)
- [ ] Follows governing RFC specifications
- [ ] Respects layer boundaries (layer.rules.md)
- [ ] No forbidden imports (dependency.rules.md)
- [ ] Dependency graph direction is correct
- [ ] No circular dependencies

### 2. Contracts (Blocking)
- [ ] All interfaces are implemented
- [ ] No interface changes without ADR
- [ ] Backward compatibility maintained
- [ ] Error types are properly defined

### 3. Code Quality (Blocking)
- [ ] No TODO comments
- [ ] No placeholder implementations
- [ ] No dead code or unused imports
- [ ] No global/static mutable state
- [ ] No service locator pattern
- [ ] Dependency injection used correctly

### 4. Naming (Non-blocking)
- [ ] Follows naming.rules.md
- [ ] Self-documenting names
- [ ] No magic strings or numbers
- [ ] Consistent patterns across modules

### 5. Testing (Blocking)
- [ ] Unit tests for all public functions
- [ ] Lifecycle tests for state machines
- [ ] Failure tests for error paths
- [ ] Integration tests for cross-module flows
- [ ] Tests actually run and pass

### 6. Security (Blocking)
- [ ] No hardcoded secrets or keys
- [ ] Input validation present
- [ ] Error handling does not leak sensitive data
- [ ] Proper access controls

### 7. Performance (Non-blocking)
- [ ] Within RFC-defined budgets
- [ ] No O(n^2) in hot paths
- [ ] No unnecessary allocations

---

## Review Findings Format

Every finding MUST include:

`
[SEVERITY] File: path/to/file.rs, Line: 42
Description: What is wrong
Reference: Which rule/standard is violated
Suggestion: How to fix it
`

Severity levels:
- **Critical** — Blocks merge. Must fix.
- **High** — Architecture violation. Must fix.
- **Medium** — Quality issue. Should fix.
- **Low** — Style nit. Nice to fix.

---

## Review Outcome

| Outcome | Meaning | Next Step |
|---------|---------|-----------|
| Approved | All checks pass | Merge |
| Changes Requested | One or more High/Medium findings | Fix and resubmit |
| Blocked | One or more Critical findings | Must fix before any further review |

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
