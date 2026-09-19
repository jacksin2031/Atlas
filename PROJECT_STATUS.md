# Atlas Project Status

> Sprint 18 candidate: **0.18.0-alpha**. Beta readiness is **NOT YET**; see [current evidence and acceptance gaps](docs/beta/SPRINT_18_BETA_READINESS_REPORT.md). Earlier sprint results below remain historical evidence.

> **Last Updated**: 2026-08-30
> **Current Version**: 0.15.0-alpha
> **Current Focus**: Sprint 15 Final Acceptance PASS; baseline frozen

## Verified Implementation Status

| Component | Status | Verified automated tests |
|---|---|---:|
| Runtime | Implemented | 70 |
| Plugin | Implemented | 133 |
| IPC | Implemented | 100 |
| Contracts | Implemented | 16 |
| Storage | Partial | 10 |
| Common | Implemented; no direct tests | 0 |
| Workflow and Conformance | Implemented in `src/`; Desktop host integrated | 310 |
| Vision | Implemented | 185 |
| AI | Implemented | 110 |
| Desktop, Workflow, Vision, and AI Studio UI | Alpha | 135 |
| Knowledge | Specifications only | 0 |
| Project | Specifications only; package absent | 0 |
| Cross-runtime integration | Workflow-to-AI/Vision/Plugin boundaries integrated; broader integration partial | 0 |

**Verified test total**: 1,074

The counts above reflect tests that are present and executable in this repository snapshot. Historical sprint reports may describe implementations that are not included here.

## Build Health

| Check | Expected result |
|---|---|
| `cargo fmt --all --check` | Pass |
| `cargo test --workspace --all-targets` | Pass |
| Root Python tests | Pass |
| AI package tests | Pass |
| Vision package tests | Pass |
| Desktop TypeScript check | Pass |
| Desktop ESLint | Pass |
| Desktop Vitest suite | Pass |
| Desktop production build | Pass |
| Tauri backend check/build | Pass |

CI runs all of these implementation-level checks. Knowledge and Project remain specification work until source packages and tests are added.

## Sprint 14 Verification Note

Vision Studio is implemented as a separate FlexLayout workspace with versioned per-workspace persistence, a centralized panel registry, image canvas, overlays, properties, result panels, timeline, commands, and an IPC capture boundary. On 2026-08-22, desktop TypeScript, ESLint, all 110 Vitest tests, the production build, the Tauri MSVC check, and all 185 Vision runtime tests passed.

## Sprint 15 Verification Note

AI Studio is implemented as a third FlexLayout workspace with provider/model discovery views, Playground, Prompt/Conversation modes, Context/Request/Response inspectors, Memory, Tools, Agent, Events, Metrics, and Vision input. The persistent Rust/Tauri-to-Python host exposes all four AI commands with request-correlated streaming/cancellation events, Runtime metrics, and multimodal plumbing. The former Desktop Connect `unavailable` regression is closed. Live provider output remains `PENDING EXTERNAL CONDITION` because no healthy provider/model was available; the Atlas-owned bridge and Vision-context attachment pass.

## Sprint 15.2 Verification Note

Workflow Studio serializes its editable graph into the canonical Workflow manifest and executes through Tauri commands and a persistent Python host. Typed edge propagation, branches, variables, cancellation, restart, Input/Vision/AI bridges, dynamic plugins, and recovery are integrated. Real target relocation, missing-target/no-click, Template, OCR, emergency stop, project restart, interrupted recovery, no replay, and manual restart pass. The final suite contains 310 root Python, 110 AI, 185 Vision, 135 Desktop, 329 root Rust, and 5 Tauri Rust tests.

## Version and License

- Release line: `0.15.0-alpha`
- Python-compatible version: `0.15.0a0`
- License: Apache-2.0
