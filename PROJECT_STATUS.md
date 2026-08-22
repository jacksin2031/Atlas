# Atlas Project Status

> **Last Updated**: 2026-08-22  
> **Current Version**: 0.12.0-alpha  
> **Current Focus**: Sprint 14 Vision Studio complete; runtime adapter follow-up

## Verified Implementation Status

| Component | Status | Verified automated tests |
|---|---|---:|
| Runtime | Implemented | 70 |
| Plugin | Implemented | 133 |
| IPC | Implemented | 100 |
| Contracts | Implemented | 16 |
| Storage | Partial | 10 |
| Common | Implemented; no direct tests | 0 |
| Workflow and Conformance | Implemented in `src/` | 289 |
| Vision | Implemented | 185 |
| AI | Implemented | 105 |
| Desktop, Workflow Studio, and Vision Studio UI | Alpha | 110 |
| Knowledge | Specifications only | 0 |
| Project | Specifications only; package absent | 0 |
| Cross-runtime integration | Specifications and design only | 0 |

**Verified test total**: 1,018

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

## Version and License

- Release line: `0.12.0-alpha`
- Python-compatible version: `0.12.0a0`
- License: Apache-2.0
