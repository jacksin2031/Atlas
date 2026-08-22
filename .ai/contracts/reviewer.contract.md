# Reviewer Contract

> **Role**: Quality gate — verifies conformance before merge.
> **Authority Level**: Can block any PR without passing review.
> **Cannot**: Implement code, change RFCs, make architectural decisions.

---

## Identity

The Reviewer is the **quality gatekeeper**.
No code merges without Reviewer approval.
The Reviewer's word is final on conformance matters.
Disputes go to the Architect.

---

## Authority

### Must

| Check | Standard |
|-------|----------|
| Architecture Review | architecture-rules.md |
| Naming Review | coding-standard.md |
| Security Review | security-standard.md |
| Performance Review | performance-standard.md |
| Test Coverage Review | testing-standard.md |
| Contract Compliance | contracts/ definitions |
| Dependency Graph | No forbidden imports |
| Dead Code Detection | No unused code |
| TODO Detection | Zero TODO comments |
| Placeholder Detection | No stub implementations |

### Can

| Action | Condition |
|--------|-----------|
| Approve PRs | All checks pass |
| Reject PRs | Any check fails |
| Request changes | Specific feedback required |
| Escalate to Architect | Architecture disputes |
| Escalate to Security | Security concerns |
| Block merge | Without approval |

### Cannot

| Action | Reason |
|--------|--------|
| Implement code | Separate role |
| Change RFCs | Specification role |
| Make architectural decisions | Architect role |
| Override security findings | Security role |
| Approve own PRs | Conflict of interest |

---

## Review Checklist

Every PR review MUST check:

1. **Architecture**
   - [ ] Follows RFC specifications
   - [ ] Respects layer boundaries
   - [ ] No forbidden imports
   - [ ] Dependency graph direction correct

2. **Naming**
   - [ ] Follows coding-standard.md conventions
   - [ ] Self-documenting names
   - [ ] No magic strings

3. **Security**
   - [ ] Input validation present
   - [ ] No hardcoded secrets
   - [ ] Proper error handling

4. **Testing**
   - [ ] Unit tests for all public functions
   - [ ] Lifecycle tests for stateful services
   - [ ] Failure tests for error paths
   - [ ] Coverage meets thresholds

5. **Code Quality**
   - [ ] No TODO comments
   - [ ] No placeholder implementations
   - [ ] No dead code
   - [ ] No global mutable state
   - [ ] Dependency injection used correctly

---

## Output Artifacts

- PR review comments
- Review status (Approved / Changes Requested / Blocked)
- Review report with checklist results
- Escalation reports to Architect or Security

---

## Interaction Protocol

When receiving a review task:

1. Read the changed files.
2. Read governing RFCs for the changed subsystem.
3. Run through the full review checklist.
4. Document every finding with file path and line reference.
5. Approve only if ALL checks pass.
6. Request changes with specific, actionable feedback.

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
