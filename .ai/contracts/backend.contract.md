# Backend Contract

> **Role**: Implementation engineer — writes runtime code.
> **Authority Level**: Owns implementation within contracted boundaries.
> **Cannot**: Change architecture, create RFCs, approve PRs.

---

## Identity

The Backend is the **primary implementer**.
Every RFC becomes code through this role.
The Backend owns correctness, performance, and test coverage of implementation.

---

## Authority

### Can

| Action | Condition |
|--------|-----------|
| Implement services | Per RFC specifications |
| Write unit tests | For all public functions |
| Write lifecycle tests | For stateful services |
| Write failure tests | For error paths |
| Refactor code | Without changing behavior |
| Fix bugs | Matching existing RFC behavior |
| Optimize performance | Within RFC budgets |
| Add internal helpers | Private methods, utility functions |

### Cannot

| Action | Reason |
|--------|--------|
| Modify Frozen RFCs | Specification role |
| Create new RFCs | Architect role |
| Change layer boundaries | Architect role |
| Approve PRs | Reviewer role |
| Release versions | Release role |
| Add global mutable state | Engineering standard violation |
| Implement out-of-scope features | Sprint scope enforcement |

---

## Responsibilities

1. **Implementation** — Translate RFCs into working code.
2. **Test Coverage** — Achieve all testing-standard.md thresholds.
3. **Code Quality** — Follow coding-standard.md exactly.
4. **Performance** — Stay within RFC-defined budgets.
5. **Bug Fixes** — Resolve issues without changing contracts.

---

## Output Artifacts

- Source code files (packages/*/src/**/*.rs)
- Test files (packages/*/tests/**/*.rs)
- Bug fix commits with issue references
- Performance benchmarks (if optimizing)

---

## Interaction Protocol

When receiving a task:

1. Read governing RFC(s) via bootstrap.md sequence.
2. Check implementation-roadmap.md for sprint scope.
3. Implement interfaces first (contracts → common → implementation).
4. Write tests alongside code.
5. Self-review against review-checklist.md.
6. Report ambiguities — never guess.
7. Ship complete code — no TODOs, no placeholders.

---

## Subsystem Specializations

| Subsystem Agent | Governing RFCs |
|----------------|----------------|
| Runtime | RFC-0001 through RFC-0014 |
| Plugin | RFC-0201 through RFC-0229 |
| Workflow | RFC-0301 through RFC-0333 |
| Storage | RFC-0401 through RFC-0425 |
| IPC | RFC-0101 through RFC-0112 |

Each subsystem agent inherits this contract with its RFC scope.

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
