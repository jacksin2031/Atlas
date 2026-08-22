# Atlas Development System (ADS)

> **Authority**: This is the homepage of the entire ADS.
> **Scope**: Every developer, every AI agent, every contribution.
> **Rule**: Read this file first. Then read bootstrap.md for the reading sequence.

---

## What is Atlas?

Atlas is an AI-native automation platform.
It is not a desktop app. It is not a simple script runner.
It is a **runtime orchestration system** with:

- A core Runtime that manages lifecycle, services, scheduling, and events.
- A Plugin system for extensibility.
- A Workflow Engine for automation pipelines.
- A Vision Engine for screen capture and OCR.
- An AI Agent Coordinator for LLM orchestration.
- A Marketplace for plugin distribution.
- A Storage system for persistent state.

---

## ADS Structure

The ADS is organized in **five layers**, from abstract to concrete:

`
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Governance                                    │
│  ─────────────────                                      │
│  Who we are. What we value. What we never do.           │
│                                                         │
│  .ai/constitution.md                                    │
│  .ai/ai-behavior.md                                     │
│  governance/                                            │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌──────────────────────┴──────────────────────────────────┐
│  Layer 2: Operating System                               │
│  ───────────────────────                                 │
│  How agents execute work. The entry protocol.            │
│                                                         │
│  .ai/bootstrap.md             ← ENTRY POINT             │
│  .ai/operating-system.md      ← EXECUTION LOOP          │
│  .ai/workflow.md              ← DEVELOPMENT LIFECYCLE   │
│  .ai/specification-rules.md   ← RFC/ADR RULES           │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌──────────────────────┴──────────────────────────────────┐
│  Layer 3: Engineering Standards                          │
│  ───────────────────────────                             │
│  How code is written, reviewed, and tested.              │
│                                                         │
│  .ai/architecture-rules.md   ← Layer boundaries         │
│  .ai/coding-standard.md      ← Style & naming           │
│  .ai/engineering.md          ← Code gen best practices  │
│  .ai/security-standard.md    ← Security rules           │
│  .ai/testing-standard.md     ← Test requirements        │
│  .ai/performance-standard.md ← Performance budgets      │
│  .ai/review-checklist.md     ← Review criteria          │
│  .ai/definition-of-done.md   ← Completion criteria      │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌──────────────────────┴──────────────────────────────────┐
│  Layer 4: Specifications                                 │
│  ─────────────────                                       │
│  What the system does. The RFCs.                         │
│                                                         │
│  specs/runtime/            ← Runtime RFCs               │
│  specs/ipc/                ← IPC RFCs                   │
│  specs/plugin/             ← Plugin RFCs                │
│  specs/workflow/           ← Workflow RFCs              │
│  specs/storage/            ← Storage RFCs               │
│  specs/common/             ← Cross-cutting RFCs         │
│  docs/adr/                 ← Architecture Decisions     │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌──────────────────────┴──────────────────────────────────┐
│  Layer 5: Implementation                                 │
│  ─────────────────                                       │
│  How the system is built. The code.                      │
│                                                         │
│  packages/runtime/         ← Core runtime               │
│  packages/plugin/          ← Plugin host                │
│  packages/workflow/        ← Workflow engine            │
│  packages/vision/          ← Vision capture             │
│  packages/common/          ← Shared types               │
│  packages/contracts/       ← Interface definitions      │
│  crates/                   ← Rust-native modules        │
│  apps/                     ← Application entry points   │
└─────────────────────────────────────────────────────────┘
`

---

## Quick Reference

| You Want To... | Read This |
|----------------|-----------|
| Enter the repo for the first time | .ai/bootstrap.md |
| Understand how to execute any task | .ai/operating-system.md |
| Know what the development process looks like | .ai/workflow.md |
| Learn the rules for all AI agents | .ai/ai-behavior.md |
| Create or modify an RFC | .ai/specification-rules.md |
| Understand how code should be written | .ai/coding-standard.md |
| Check if your architecture is correct | .ai/architecture-rules.md |
| Review someone's code | .ai/review-checklist.md |
| Know when a task is truly done | .ai/definition-of-done.md |
| Find the specs for a subsystem | specs/{subsystem}/ |
| Understand a past architectural decision | docs/adr/ |
| See what to implement this sprint | .ai/implementation-roadmap.md |

---

## Agent Roles

| Agent | Manages |
|-------|---------|
| **Architect** | ADRs, system design, architecture review |
| **Runtime** | RFC-0001 through RFC-0014 |
| **Plugin** | RFC-0201 through RFC-0229 |
| **Workflow** | RFC-0301 through RFC-0333 |
| **Storage** | RFC-0401 through RFC-0425 |
| **IPC** | RFC-0101 through RFC-0112 |
| **AI** | AI agent coordination (future RFCs) |
| **Vision** | Vision capture engine (future RFCs) |
| **Security** | Vulnerability scanning, security audits |
| **QA** | Test coverage, regression, performance |
| **Reviewer** | PR review, conformance checks |
| **Performance** | Benchmarking, optimization |
| **Planner** | Implementation planning, task decomposition |
| **Documentation** | Docs, walkthroughs, examples |
| **Release** | Versioning, changelog, merge coordination |

---

## Golden Rules

1. **Specifications > Implementation** — The RFC defines the truth. Code follows specs.
2. **Architecture Before Code** — Never implement without understanding the architecture.
3. **Contracts First** — Define interfaces before implementations.
4. **No Guessing** — If unsure, ask. Never invent.
5. **No Skipping** — Every step in the workflow is mandatory.
6. **No TODOs** — Ship complete code.
7. **No Dead Code** — Remove what is not used.
8. **Test Everything** — Unit, lifecycle, failure, integration.
9. **Review Always** — Self-review before every submission.
10. **Explain Trade-offs** — Document why, not just what.

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
