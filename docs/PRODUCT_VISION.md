# Atlas Product Vision

> **Last Updated**: 2026-07-05
> **Owner**: Atlas Product Board
> **Related**: [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) · [ROADMAP.md](ROADMAP.md) · [ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## Mission

**Build automation that understands intent instead of recording coordinates.**

Atlas replaces fragile coordinate-based recording with a platform that perceives screens, reasons about applications, plans actions, and executes them reliably — all through a unified runtime architecture.

---

## The Problem

Current automation tools fall into three categories, each with fundamental limitations:

| Category | Examples | Limitation |
|----------|----------|------------|
| **Macro Recorders** | AutoHotkey, Selenium IDE | Record-and-replay. Break on any layout change. Zero intelligence. |
| **Scripting Frameworks** | Playwright, Puppeteer | DOM-only. Blind to desktop apps, games, virtual machines. |
| **RPA Platforms** | UiPath, Automation Anywhere | Enterprise-licensed. Cloud-dependent. Vendor lock-in. Slow to adapt. |

None of them combine **vision perception**, **local AI reasoning**, and **extensible plugin architecture** into a single open platform.

## The Atlas Solution

Atlas is a **multi-runtime automation platform** that:

1. **Sees** — Vision Runtime captures and understands screen content
2. **Thinks** — AI Runtime reasons about intent, plans actions, uses tools
3. **Knows** — Knowledge Runtime stores and retrieves domain context
4. **Acts** — Workflow Runtime orchestrates multi-step automation
5. **Extends** — Plugin Runtime allows anyone to add capabilities
6. **Connects** — IPC Runtime bridges processes, languages, and machines
7. **Manages** — Project Runtime organizes everything into workspaces

All of this runs **locally first**, with optional cloud extension.

---

## Goals

### What Atlas Will Do

| Goal | Description | Status |
|------|-------------|--------|
| **Intent-based automation** | Users describe what they want; Atlas figures out how | 🟡 Planned |
| **Vision-based perception** | Understand screens through computer vision, not DOM selectors | ✅ Sprint 6 |
| **Local-first AI** | Run models locally for privacy and speed | ✅ Sprint 7 |
| **Knowledge-driven workflows** | Learn from past automations, adapt over time | ✅ Sprint 8 |
| **Plugin ecosystem** | Anyone can extend Atlas with providers and tools | ✅ Sprint 3 |
| **Cross-process orchestration** | Coordinate multiple applications simultaneously | ✅ Sprint 5 |
| **Deterministic execution** | Every automation produces reproducible results | ✅ All Sprints |
| **Open standards** | RFC-defined contracts, language-agnostic, no vendor lock-in | ✅ All Sprints |

### What Atlas Will Not Do

| Non-goal | Why |
|----------|-----|
| **Replace IDEs** | Atlas automates workflows; it doesn't compete with development tools |
| **Cloud-first SaaS** | Local-first is a design principle. Cloud is optional extension |
| **Mobile automation** | Mobile is out of scope for the initial platform. May come later |
| **Web scraping as a service** | Atlas automates interactions; it is not a scraping API |
| **GUI builder (yet)** | Visual studios (Workflow Studio, Vision Studio, AI Studio) are post-1.0 |
| **Database management** | Storage is abstracted; Atlas doesn't compete with DB tools |
| **Network scanning / pentesting** | Security is about sandbox isolation, not penetration testing |

---

## Target Users

| Persona | Use Case | Primary Runtimes |
|---------|----------|-----------------|
| **QA Engineers** | Automated regression testing across desktop apps | Vision, Workflow, IPC |
| **DevOps** | Cross-service deployment and health-check automation | Workflow, IPC, AI |
| **Data Analysts** | Repetitive data collection and transformation | Vision, AI, Knowledge |
| **Developers** | IDE-adjacent automation (file ops, build triggers, CI) | Workflow, Plugin, IPC |
| **Power Users** | Personal productivity automation (file organization, notifications) | Vision, AI, Workflow |
| **Plugin Authors** | Extend Atlas with custom providers and tools | Plugin, IPC |

---

## Architecture at a Glance

```
                    Desktop UI / CLI
                    Workflow Studio (future)
                    Marketplace (future)
                          │
                   ┌──────┴──────┐
                   │  Project    │ ← Workspace, Assets, Config, Templates
                   │  Runtime    │
                   └──────┬──────┘
                          │ hosts
              ┌───────────┼───────────┬───────────┐
              │           │           │           │
       ┌──────┴──────┐ ┌─┴────────┐ ┌┴────────┐ ┌┴────────┐
       │  Plugin     │ │   IPC    │ │ Workflow│ │  Vision │
       │  Runtime    │ │ Runtime  │ │ Runtime │ │ Runtime │
       └─────────────┘ └──────────┘ └─────────┘ └─────────┘
              │           │           │           │
       ┌──────┴──────┐ ┌─┴────────┐ ┌┴────────┐ ┌┴────────┐
       │     AI      │ │Knowledge │ │  ...     │ │  ...     │
       │  Runtime    │ │ Runtime  │ │          │ │          │
       └─────────────┘ └──────────┘ └──────────┘ └──────────┘
```

Each runtime is independently lifecycle-managed, health-monitored, and plugin-extensible. See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full diagram.

---

## Design Philosophy

Atlas is built on six principles. See [DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md) for details.

In short:

- **Everything is Runtime** — Uniform lifecycle, health, metrics
- **Everything is Plugin** — Swappable providers, hot-reloadable
- **Everything is Event** — Immutable, versioned, persisted
- **Everything is Deterministic** — Reproducible, no globals, frozen dataclasses
- **Contracts First** — RFC-defined interfaces before code
- **Provider Pattern** — All external dependencies abstracted

---

## Long-term Roadmap

### Phase 1: Runtime Construction (Sprints 0–10) ✅

Build the foundation — all core runtimes implemented and integrated.

- Runtime Foundation, Infrastructure, Plugin, IPC, Workflow, Vision, AI, Knowledge, Project, Cross-Runtime Integration

### Phase 2: Stability & Performance (Sprints 11–12)

Performance tuning, stress testing, memory optimization, throughput benchmarks.

### Phase 3: Developer Experience (Sprints 13–16)

Desktop Shell, Workflow Studio, Vision Studio, AI Studio — visual tooling for power users.

### Phase 4: Ecosystem (Sprints 17–18)

Marketplace for plugins, knowledge packs, and providers. Beta release.

### Phase 5: Production (Post-1.0)

Stable release, LTS support, enterprise features, cloud extensions.

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Runtimes implemented | 8+ | 8 ✅ |
| RFCs implemented | 100+ | 134 ✅ |
| Test coverage | 700+ | 1,671+ ✅ |
| Zero circular dependencies | Yes | Yes ✅ |
| Platform-independent | Yes | Yes ✅ |
| Deterministic execution | Guaranteed | Guaranteed ✅ |
| Plugin extensibility | 100% of capabilities | 100% ✅ |

---

## History

| Date | Milestone |
|------|-----------|
| 2026-06-27 | Sprint 0 — Project bootstrap |
| 2026-06-28 | Sprint 1 — Runtime Foundation |
| 2026-06-29 | Sprint 2 — Runtime Infrastructure |
| 2026-06-30 | Sprint 3 — Plugin Runtime |
| 2026-07-01 | Sprint 4 — Workflow Runtime |
| 2026-07-04 | Sprint 5 — IPC Runtime |
| 2026-07-04 | Sprint 6 — Vision Runtime |
| 2026-07-04 | Sprint 7 — AI Runtime |
| 2026-07-04 | Sprint 8 — Knowledge Runtime |
| 2026-07-05 | Sprint 9 — Project Runtime |
| 2026-07-05 | Sprint 10 — Cross-Runtime Integration |

---

*"Record Once. Understand Forever."*

---

*For design decisions, see [DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md).*
*For technical architecture, see [ARCHITECTURE.md](docs/ARCHITECTURE.md).*
*For the roadmap, see [ROADMAP.md](ROADMAP.md).*
