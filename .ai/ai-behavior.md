# Atlas AI Behavior Rules

> **Authority**: These rules apply to ALL agents — human and AI.
> **Scope**: Every interaction with the Atlas repository.
> **Rule**: Violating these rules is grounds for immediate task rejection.

---

## Core Principles

### 1. Never Guess

If you do not know, say so.
Never invent API signatures, RFC content, or behavioral contracts.
When in doubt: **ask, don't assume.**

### 2. Never Invent Architecture

The architecture is defined by RFCs and ADRs.
If your implementation requires a new architectural decision:
- Document it as a draft ADR
- Present it for review
- Do not proceed until approved

### 3. Never Skip RFC

Every feature has a governing RFC.
Before implementing, locate and read the relevant RFC.
If no RFC exists, the feature does not exist yet.
Create the RFC first (follow specification-rules.md).

### 4. Never Skip Review

Self-review is mandatory.
Use the review-checklist.md before marking any task complete.
If the task is a Review-type task, follow the Reviewer agent role.

### 5. Always Explain Trade-offs

Every implementation decision has trade-offs.
Document them in the PR description or ADR.
Never claim "this is the best approach" without justification.

### 6. Always Report Ambiguity

If a specification is unclear, contradictory, or incomplete:
- Quote the ambiguous section
- List possible interpretations
- Ask for clarification
- Do not pick one silently

### 7. Always Follow the Dependency Graph

Implement interfaces before implementations.
Never create circular dependencies.
Never import from a layer above you.
Refer to architecture-rules.md for layer boundaries.

### 8. Always Write Testable Code

Every module must be independently testable.
If you cannot write a unit test for a function,
the function is too large or has too many responsibilities.
Split it.

### 9. Always Respect Scope

Sprint N only implements Sprint N scope.
Do not implement future features "while you're at it."
Do not refactor unrelated code "to make it cleaner."
Stay surgical.

### 10. Always Use Contracts First

Define the interface (trait/protocol) before the implementation.
The contract is the agreement. The implementation is the promise.
If the contract changes, document why.

---

## Anti-Patterns (Never Do These)

| Anti-Pattern | Why | Correct Approach |
|-------------|-----|-----------------|
| Global mutable state | Unpredictable, untestable | Dependency injection |
| Service locator | Hides coupling | Explicit constructor injection |
| Static mutable state | Breaks parallelism | Instance-scoped state |
| Magic strings | Brittle, unrefactorable | Named constants or enums |
| Deeply nested conditionals | Unclear control flow | Early returns, guard clauses |
| God objects | Too many responsibilities | Single responsibility principle |
| Silent failures | Bugs hide forever | Fail fast, log always |
| TODO comments | Debt accumulation | Complete the work or don't start |
| Placeholder implementations | False progress | Ship working code |
| Copy-paste code | DRY violation | Extract shared logic |

---

## Communication Rules

### With the User

- Be concise. 8–12 words for status updates.
- State assumptions explicitly.
- Report blockers immediately.
- Suggest next steps, don't just describe problems.
- Use the update_plan tool for multi-step work.

### With Other Agents

- Communicate through shared artifacts (files, specs, contracts).
- Do not assume knowledge from other agents' work.
- If an agent changes a contract you depend on, re-read it.
- Parallel agents must have disjoint write scopes.

### In Code

- Names must be self-documenting.
- No inline comments unless explicitly requested.
- Function names describe behavior, not implementation.
- Variable names describe meaning, not type.

---

## Quality Thresholds

| Check | Pass Condition |
|-------|---------------|
| Architecture | Follows RFC, respects layer boundaries |
| Naming | Follows coding-standard.md |
| Lifecycle | Follows RFC-0002 state machine |
| Contracts | All interfaces defined before implementations |
| Dependencies | No forbidden imports, no circular deps |
| Tests | Unit + lifecycle + failure tests pass |
| Documentation | Updated if behavior changed |
| TODOs | Zero TODO comments in shipped code |
| Placeholders | Zero stub implementations |
| Dead Code | Zero unreachable or unused code |

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
