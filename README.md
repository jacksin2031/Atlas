# Atlas

> Sprint 18 candidate: **0.18.0-alpha**. **SPRINT 18: PARTIAL — BETA READINESS: NOT YET.** See [Sprint 18 Beta Readiness Report](docs/beta/SPRINT_18_BETA_READINESS_REPORT.md) for the evidence and remaining release gates.

> Record Once. Understand Forever.

Atlas is an open-source AI-powered desktop automation platform for workflows, computer vision, AI, knowledge, input automation, and extensible plugins.

## Current Status

| Attribute | Value |
|---|---|
| **Version** | 0.18.0-alpha (unreleased candidate) |
| **Current Focus** | Sprint 18.1 Beta Acceptance Closure |
| **Sprint 18 Verdict** | PARTIAL — Beta Readiness NOT YET |
| **Automated Tests** | 1,260 passing, 0 failing across the final recorded Sprint 18 suites |
| **Windows Packaging** | NSIS x64 installer with isolated embedded CPython runtime |
| **Clean-machine Acceptance** | NOT RUN — mandatory release gate |
| **Marketplace** | Local Development Distribution verified; production registry/PKI external |
| **Live AI Provider** | PENDING EXTERNAL CONDITION |
| **License** | Apache-2.0 |

The test count above is the recorded Sprint 18 evidence checkpoint. Do not treat it as a current CI result unless the suites are rerun.

## Product Architecture

```text
Desktop Shell (Tauri 2 + React)
        |
Workspace / Command / Panel infrastructure
        |
+-------+--------+---------+----------+-------------+
| Workflow | Vision | AI | Knowledge | Marketplace |
+-------+--------+---------+----------+-------------+
        |
Typed IPC / service boundaries
        |
Workflow / Vision / AI / Knowledge / Plugin / Input runtimes
        |
Persistence / Security / Diagnostics / Credential Vault
```

The UI does not execute runtime logic directly. Workflow, AI, Vision, Knowledge, Plugin, and Input capabilities cross explicit service/IPC boundaries. Production Windows builds bundle the Python-dependent hosts and do not require a user-installed Python runtime.

## Implemented Product Areas

- Runtime foundation, contracts, IPC, storage abstractions, metrics, health, and security.
- Plugin Runtime and local development Marketplace distribution lifecycle.
- Workflow Studio with persistent native execution, lifecycle controls, bridges, and dynamic plugin nodes.
- Vision Studio with native capture, analysis boundaries, visual references, and persisted workspace state.
- AI Studio with provider/model discovery, streaming/cancellation bridge, secure credential boundary, and explicit unavailable states.
- Knowledge Studio with project-scoped CRUD, retrieval, persistence, recovery, and Workflow/Vision/AI integration.
- Input Runtime with bounded mouse/keyboard nodes, explicit arming, foreground restrictions, emergency stop, and release-all safety.
- Project persistence, interrupted-execution recovery, diagnostics/redaction, and Windows installer/runtime delivery.

## Sprint 18 Packaging

The current candidate uses a Windows x64 NSIS installer and an isolated embedded CPython runtime. The recorded artifact is:

```text
Atlas_0.18.0-alpha_x64-setup.exe
SHA-256: f99bcd6c72b634f364fcc58a98b5fd819d98da5ad56cd8ec6fe87e671871d941
```

This artifact was exercised on the developer workstation in an isolated installed-product setup. It has **not** completed the mandatory clean-Windows lifecycle, so it is not an accepted beta release.

## Development Quick Start

### Prerequisites

- Rust toolchain (Windows desktop builds use MSVC)
- Python for development/reference-runtime tests
- Node.js + pnpm for the desktop frontend

Installed end users are not expected to install these development dependencies.

### Build

```bash
cargo build --workspace
cd apps/atlas-desktop
pnpm install
pnpm run build
pnpm tauri build --debug --no-bundle
```

### Core Test Entry Points

```bash
cargo test --workspace --all-targets
PYTHONPATH=src python -m pytest
PYTHONPATH=packages/vision/src python -m pytest packages/vision/tests
PYTHONPATH=packages/ai/src python -m pytest packages/ai/tests
cd apps/atlas-desktop && pnpm test
```

Use the repository's documented Windows MSVC commands and Sprint 18 acceptance scripts for release verification. Development tests alone do not establish Beta readiness.

## Repository Structure

```text
Atlas/
├── apps/
│   └── atlas-desktop/   # Tauri 2 + React desktop product
├── packages/            # Rust/Python runtime packages and contracts
├── src/                 # Workflow/Knowledge and integration implementation used by the desktop hosts
├── specs/               # Runtime, IPC, Plugin, Workflow, Storage, and common RFCs
├── docs/                # Architecture, acceptance, security, marketplace, and beta evidence
├── scripts/             # Runtime bundling/release/acceptance support
├── .ai/                 # AI engineering rules/skills
└── Cargo.toml
```

## Documentation

- [Sprint 18 Beta Readiness](docs/beta/SPRINT_18_BETA_READINESS_REPORT.md)
- [Project Status](PROJECT_STATUS.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)
- [Versioning](VERSIONING.md)
- [Release Procedure](RELEASE.md)
- [RFC Index](specs/RFC_INDEX.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Security Policy](SECURITY.md)

## Release Boundary

Sprint 18 remains incomplete until internally controllable mandatory acceptance gates are closed, especially clean-machine installation/lifecycle validation. Live OpenAI/Ollama availability, production Marketplace infrastructure, publisher certification, trusted Windows code signing, and SmartScreen reputation are tracked separately and must not be simulated to claim acceptance.

No beta tag or public release is implied by this repository state.

## License

Apache 2.0
