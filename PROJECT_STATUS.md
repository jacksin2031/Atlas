# Atlas Project Status

> **Last Updated**: 2026-09-19
> **Current Version**: 0.18.0-alpha (unreleased candidate)
> **Current Focus**: Sprint 18.1 Beta Acceptance Closure
> **Sprint 18 Verdict**: PARTIAL — BETA READINESS: NOT YET

The authoritative Sprint 18 acceptance record is [docs/beta/SPRINT_18_BETA_READINESS_REPORT.md](docs/beta/SPRINT_18_BETA_READINESS_REPORT.md). Historical sprint reports remain evidence for their own checkpoints and must not override the current acceptance matrix.

## Current Product Status

| Area | Current state |
|---|---|
| Desktop Shell | Implemented alpha product shell (Tauri 2 + React) |
| Workflow Studio | Integrated with persistent native Workflow host |
| Vision Studio | Integrated native capture/analysis workspace |
| AI Studio | Integrated Desktop bridge; live-provider response remains external |
| Knowledge Studio | Integrated project-scoped CRUD/retrieval/persistence |
| Input Runtime | Integrated with explicit arm/foreground/emergency-stop safety |
| Plugin Runtime | Implemented |
| Marketplace | Sprint 17 local development distribution complete |
| Project persistence | Implemented for current product assets with backup/recovery/version gates |
| Windows packaging | NSIS x64 candidate with bundled isolated CPython |
| Clean-machine lifecycle | **NOT RUN** |
| Beta readiness | **NOT YET** |

## Sprint 18 Recorded Verification

The final recorded Sprint 18 automated checkpoint is:

| Suite | Passed | Failed |
|---|---:|---:|
| Root Rust workspace (MSVC) | 348 | 0 |
| Combined Python regression | 717 | 0 |
| Frontend (25 files) | 178 | 0 |
| Desktop native Rust | 17 | 0 |
| **Total** | **1,260** | **0** |

The 21 bundled-host smoke checks are acceptance checks and are not added to this unit/integration total. These figures are recorded evidence, not a claim that CI has been rerun after every later documentation change.

## Installed-Product Evidence

On the existing Windows developer workstation, the installed candidate has evidence for:

- first-run Welcome and runtime-health UX;
- embedded Workflow/AI Python hosts launched from installed resources;
- project create/reopen;
- Workflow production execution;
- native Vision capture;
- Input arming, foreground restriction, emergency stop and global Pause/Break;
- crash to interrupted/no-replay recovery;
- Knowledge create/search/edit/restart/delete/restart;
- local-development Marketplace install/enable/execute/restart/disable/uninstall;
- local diagnostics export and seeded-secret redaction;
- Unicode/space installation and project paths;
- uninstall/reinstall with retained user data.

These workstation results remain bounded by their evidence. They do not substitute for the required clean-Windows lifecycle.

## Open Internal Acceptance Gates

The current report still records internally controllable gaps:

1. Clean Windows install and complete no-source/no-dev-dependency lifecycle.
2. Complete workspace persistence/corruption matrix.
3. Full mixed-DPI/display and accessibility acceptance.
4. Representative installed soak/memory/runtime-orphan testing.
5. Installed plugin mutation-interruption recovery.
6. Full installed visual closed loop (detection/template → RegionReference → armed Input → validation).
7. Rust advisory review and remaining redistribution/license metadata review.
8. Full command/boundary security review beyond the focused Sprint 18 review.

Installer-to-installer upgrade from a previous distributable is recorded as unavailable historical evidence; fixture migration and same-version replacement are not represented as equivalent proof.

## External Conditions

The following do not justify fabricating a PASS and remain separate from internal engineering acceptance when unavailable:

- live OpenAI/Ollama provider response;
- production Marketplace registry;
- publisher certification PKI;
- trusted Windows code-signing certificate;
- SmartScreen reputation.

## Release Artifact Record

```text
Version:   0.18.0-alpha
Target:    x86_64-pc-windows-msvc
Installer: NSIS current-user
Filename:  Atlas_0.18.0-alpha_x64-setup.exe
Size:      227,702,216 bytes
SHA-256:   f99bcd6c72b634f364fcc58a98b5fd819d98da5ad56cd8ec6fe87e671871d941
```

The recorded artifact is unsigned. No production code-signing trust or SmartScreen reputation is claimed.

## Promotion Rule

Do not change the verdict to `SPRINT 18: COMPLETE / BETA READINESS: PASS` until all internally controllable mandatory gates in the B-A–B-X matrix pass under their required scope. In particular, the clean-machine lifecycle cannot be replaced by a restricted-PATH test on the developer workstation.

Do not create or publish a beta tag/release solely because the installer builds.

## Version and License

- Release line: `0.18.0-alpha`
- Python-compatible release notation, where required: `0.18.0a0`
- License: Apache-2.0
