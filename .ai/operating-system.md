# Atlas Operating System

> **Authority**: Defines the execution loop for every AI agent in the ADS.
> **Scope**: All agents (Architect, Backend, Frontend, Security, QA, Reviewer, Runtime, Plugin, Workflow, Storage, IPC, AI, Vision, Performance, Planner, Documentation, Release).
> **Rule**: No code is written until this loop is followed.

---

## Execution Loop

Every AI agent task follows this deterministic loop:

`
┌─────────────────────────────────────────────────────────┐
│  1. RECEIVE TASK                                         │
│     - Understand the request                            │
│     - Identify the subsystem (Runtime/Plugin/etc.)      │
│     - Check if this is Create / Refactor / Review /     │
│       Fix / Audit / Release                             │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  2. READ CONTEXT                                         │
│     - Follow .ai/bootstrap.md sequence                  │
│     - Read all applicable RFCs, ADRs, contracts         │
│     - Identify which agent role applies                 │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  3. FIND SPECIFICATION                                   │
│     - Locate the governing RFC(s)                       │
│     - Locate the governing ADR(s)                       │
│     - Locate the governing contract(s)                  │
│     - If no spec exists → STOP, report gap              │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  4. ARCHITECTURE REVIEW                                  │
│     - Verify the task does not violate layer boundaries │
│     - Verify no forbidden imports                       │
│     - Verify dependency graph direction is correct      │
│     - If violation detected → STOP, report to user      │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  5. IMPLEMENTATION PLAN                                  │
│     - Break task into atomic steps                      │
│     - Map each step to a file or module                 │
│     - Identify test coverage per step                   │
│     - Present plan to user (if interactive)             │
│     - Mark steps in update_plan tool                    │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  6. CODING                                               │
│     - Implement interfaces first (contracts/)           │
│     - Implement models next (common/)                   │
│     - Implement infrastructure last (runtime/)          │
│     - One file at a time                                │
│     - No placeholders, no TODOs                         │
│     - Follow coding-standard.md exactly                 │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  7. SELF REVIEW                                          │
│     - Check against review-checklist.md                 │
│     - Verify architecture-rules.md conformance          │
│     - Verify security-standard.md compliance            │
│     - Verify no dead code, no unused imports            │
│     - Verify naming conventions                         │
│     - If issues found → fix before proceeding           │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  8. TESTING                                              │
│     - Run unit tests for implemented modules            │
│     - Run lifecycle tests for stateful services         │
│     - Run failure tests for error paths                 │
│     - Run integration tests if applicable               │
│     - If tests fail → fix before proceeding             │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  9. DOCUMENTATION                                        │
│     - Update relevant docs if behavior changed          │
│     - Never modify RFCs or ADRs                         │
│     - Add inline comments only if explicitly requested  │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  10. DONE                                                │
│      - Mark all plan steps complete                     │
│      - Report what was changed                          │
│      - List verification steps taken                    │
│      - Suggest next logical step                        │
└─────────────────────────────────────────────────────────┘
`

---

## Agent Role Matrix

| Agent | Responsibility | Primary RFCs |
|-------|---------------|--------------|
| **Architect** | System design, ADR creation, architecture review | RFC-0001, RFC-0014 |
| **Backend** | Runtime services, schedulers, registries | RFC-0002–0005, RFC-0010 |
| **Frontend** | UI components, dashboard, overlays | RFC-0007 (IPC UI side) |
| **Runtime** | Runtime lifecycle, service model, health | RFC-0001–0006 |
| **Plugin** | Plugin host, loader, registry, sandbox | RFC-0201–0229 |
| **Workflow** | Workflow engine, execution, state | RFC-0301–0333 |
| **Storage** | Storage provider, transactions, schema | RFC-0401–0425 |
| **IPC** | Inter-process communication, routing | RFC-0101–0112 |
| **AI** | AI agent coordination, inference pipeline | Future RFCs |
| **Vision** | Vision capture, OCR, frame processing | Future RFCs |
| **Security** | Security audit, vulnerability scan | security-standard.md |
| **QA** | Test coverage, regression, performance | testing-standard.md |
| **Reviewer** | PR review, conformance check | review-checklist.md |
| **Performance** | Benchmarking, optimization | performance-standard.md |
| **Planner** | Implementation planning, task decomposition | implementation-roadmap.md |
| **Documentation** | Docs, walkthroughs, examples | definition-of-done.md |
| **Release** | Release management, changelog, versioning | pr-template.md |

---

## Task Type Routing

| Task Type | Agent(s) | Additional Steps |
|-----------|----------|-----------------|
| **Create** | Backend/Runtime/Plugin/etc. | Full loop (1–10) |
| **Refactor** | Backend + Reviewer | Steps 1–3, 5, 6, 7, 8, 10 |
| **Review** | Reviewer | Steps 1–3, 7 only |
| **Fix** | Backend + QA | Steps 1–3, 4, 5, 6, 7, 8, 10 |
| **Audit** | Security + Reviewer | Steps 1–3, 7 (extended) |
| **Release** | Release | Steps 1–3, 9, 10 |
| **Hotfix** | Backend + QA + Release | Full loop, skip doc if urgent |

---

## Stop Conditions

An agent MUST stop and report (not proceed) when:

1. A governing RFC is missing for the requested feature.
2. An architecture rule is violated by the requested change.
3. A specification is ambiguous and cannot be resolved from context.
4. A test failure cannot be reproduced or fixed.
5. A security standard is potentially violated.
6. The user's request contradicts the constitution.

---

## Concurrency Rule

When multiple agents work in parallel:

- Each agent follows the full loop independently.
- Agents MUST NOT share mutable state directly.
- Agents communicate through the Event Bus (RFC-0005).
- Conflicts are resolved by the Architect agent.
- The Release agent coordinates final merge.

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
