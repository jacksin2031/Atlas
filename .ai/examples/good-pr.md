# Example: Good PR

> **Purpose**: Template for PRs that pass review on first submission.
> **Reference**: pr-template.md for full PR requirements.

---

## PR Template

`markdown
# PR: {Title}

## Description of Changes
- What changed and why
- Link to governing RFC: RFC-XXXX
- Link to issue: #{ISSUE}

## Verification Checklist
- [ ] Architecture follows RFC specifications
- [ ] Naming follows coding-standard.md
- [ ] Lifecycle follows RFC-0002 state machine
- [ ] Service contracts implemented per RFC-0003
- [ ] Dependency graph respected (no forbidden imports)
- [ ] No circular dependencies
- [ ] Unit tests passing
- [ ] Lifecycle tests passing
- [ ] Failure tests passing
- [ ] Integration tests passing (if applicable)
- [ ] No TODO comments
- [ ] No placeholder implementations
- [ ] No dead code

## Impact Matrix

| File | Changed | Reason |
|------|---------|--------|
| packages/runtime/src/lifecycle/mod.rs | Modified | FSM state transitions |
| packages/runtime/src/lifecycle/error.rs | Added | StateTransitionError type |
| packages/contracts/src/lifecycle.rs | Added | LifecycleManager trait |
| packages/common/src/lifecycle.rs | Added | RuntimeState enum |

## Breaking Changes
None / List breaking changes if any.

## Performance Impact
- Measured within RFC budgets
- Benchmark results (if applicable)

## Related RFCs
- RFC-0002 Runtime Lifecycle
- RFC-0003 Runtime Service Model

## Related ADRs
- ADR-NNNN (if applicable)
`

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing RFC link | Always link the governing RFC |
| Empty verification checklist | Check every item, don't leave unchecked |
| No impact matrix | List every changed file with reason |
| No breaking changes section | Explicitly state "None" or list them |
| Missing test verification | List which tests were run |

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
