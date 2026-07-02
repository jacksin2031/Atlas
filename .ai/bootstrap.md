# Atlas Bootstrap

> **Authority**: This file is the highest-priority entry point in the ADS.
> **Scope**: Every AI agent, every human contributor.
> **Rule**: Nothing is implemented until this sequence is completed.

---

## Bootstrap Sequence

When an AI agent or human contributor enters the Atlas repository,
they MUST read the following files **in this exact order**.
No file may be skipped. No file may be read out of order.

### Tier 1 — Identity & Governance (Non-Negotiable)

1. .ai/constitution.md — Who we are, what we value, what we never do.
2. .ai/operating-system.md — How every agent executes work.
3. .ai/SYSTEM.md — The full ADS map. Read this first for context.

### Tier 2 — Engineering Standards

4. .ai/architecture-rules.md — Layer boundaries, DI rules, interface isolation.
5. .ai/engineering.md — Code generation best practices, agent interaction model.
6. .ai/coding-standard.md — TypeScript style, naming, clean code rules.
7. .ai/security-standard.md — Input validation, auth controls, secrets management.
8. .ai/testing-standard.md — Coverage metrics, mocking protocols.
9. .ai/performance-standard.md — Execution budgets, resource limits.

### Tier 3 — Specification Layer

10. Relevant .ai/agents/*.md — Agent role definitions for the current task.
11. Relevant docs/adr/*.md — Architecture Decision Records that govern the current domain.
12. Relevant specs/\*/RFC-\*.md — Specifications for the subsystem being implemented.
13. Relevant contracts/\*/*.md — Interface contracts for the current module.

### Tier 4 — Implementation Context

14. .ai/implementation-roadmap.md — Sprint scope, implementation order, quality gates.
15. .ai/specification-rules.md — How to add/modify RFCs, when to use ADRs.
16. .ai/workflow.md — Issue → RFC → Implementation → Review → Test → Merge flow.

### Tier 5 — Execution

17. .ai/bootstrap.md — **This file.** Re-read before starting any implementation.
    It tells you what you just read.

---

## Execution Rule

`
Read Tier 1 → Read Tier 2 → Read Tier 3 → Read Tier 4 → Read Tier 5 → Implement
`

If any file is missing, **stop** and report the gap.
Do not proceed until all tiers are accounted for.

---

## Agent Entry Protocol

Every AI agent MUST execute this protocol on entry:

`
1. Print: "Entering Atlas. Reading bootstrap sequence..."
2. Read each file in Tier 1, in order.
3. Print: "Tier 1 complete. Reading Tier 2..."
4. Read each file in Tier 2, in order.
5. Print: "Tier 2 complete. Reading Tier 3..."
6. Read each file in Tier 3, in order.
7. Print: "Tier 3 complete. Reading Tier 4..."
8. Read each file in Tier 4, in order.
9. Print: "Tier 4 complete. Reading Tier 5..."
10. Read Tier 5 (this file).
11. Print: "Bootstrap complete. Ready to execute."
12. Begin task execution.
`

---

## Override Rule

Developer/user instructions explicitly stated in the current prompt
override ALL bootstrap file content.
The bootstrap sequence defines **how to learn the system**,
not **what to do in this session**.

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
