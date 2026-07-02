# Example: Good Review

> **Purpose**: Template for reviews that catch real issues without noise.
> **Reference**: review-checklist.md for full review criteria.

---

## Review Template

`markdown
# Review: {PR Title} — {Reviewer Agent}

## Summary
Approved / Changes Requested / Blocked

## Architecture Conformance
- [ ] Follows RFC-XXXX requirements
- [ ] No forbidden imports detected
- [ ] Dependency graph respected
- [ ] Layer boundaries maintained

## Code Quality
- [ ] Naming follows coding-standard.md
- [ ] No global mutable state
- [ ] No service locator anti-pattern
- [ ] No static mutable state
- [ ] Dependency injection used correctly

## Testing
- [ ] Unit tests cover all public functions
- [ ] Lifecycle tests verify state transitions
- [ ] Failure tests cover error paths
- [ ] Integration tests exercise cross-module flows

## Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Error handling does not leak sensitive data

## Findings
| # | Severity | File | Line | Description |
|---|----------|------|------|-------------|
| 1 | High | lifecycle/mod.rs | 42 | Missing transition for Paused→Failed |
| 2 | Medium | eventbus/mod.rs | 15 | DLQ capacity not bounded |

## Conclusion
{Summary of review outcome and next steps}
`

---

## Review Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **Critical** | Blocks merge | Must fix before any review |
| **High** | Architecture violation | Must fix before approval |
| **Medium** | Code quality issue | Should fix, may defer with note |
| **Low** | Style nit | Nice to fix, not blocking |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Reviewing without reading RFC | Always read governing RFC first |
| No file/line references | Every finding must cite location |
| Subjective feedback | Ground feedback in standards, not opinion |
| Missing critical findings | Use the full checklist, don't skip sections |
| Approving without testing | Verify tests actually run and pass |

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
