# Sprint 18 — Beta Readiness & Product Hardening

SPRINT 18: PARTIAL  
BETA READINESS: NOT YET

Evidence checkpoint: 2026-09-11. This report distinguishes automated tests, installed application observations on the existing developer workstation, and unperformed clean-machine acceptance. An installer is available; that alone does not establish Beta readiness. No tag or public release was created.

## 1. Initial repository state

Initial HEAD: `9fa08d477f26b3c9ea4ed2f0f48858a2406ba66e`. The implementation is an uncommitted worktree change based on that commit. Pre-existing generated Python caches, TypeScript build information and acceptance scratch files were preserved. See [initial audit matrix](AUDIT.md).

## 2. Sprint 17 baseline

Sprint 17 remains COMPLETE under Local Development Distribution. Its M-A–M-T acceptance and historical reports were not rewritten. Existing `v0.15.0-alpha` and `v0.17.0-alpha` tags were not moved or replaced.

## 3. Scope

Deliver Windows packaging, isolated bundled runtimes, onboarding, safer persistence, local diagnostics, dependency/release hardening and verifiable acceptance evidence. No new Studio or major Runtime architecture was introduced. Version is `0.18.0-alpha`, not 1.0 or an accepted beta.

## 4. Packaging architecture

Tauri release executable → installed resources → embedded CPython → existing Workflow/AI hosts. Workflow hosts Knowledge/Input; Vision capture uses the native bridge. Frontend assets are compiled into the application. Release runtime discovery has no repository/global-Python fallback.

## 5. Installer

NSIS Windows x64, current-user installation, bundled offline WebView2 installer. Silent installation into a disposable directory containing spaces, Traditional Chinese and Japanese returned exit code 0. WebView2 was already present on this workstation; the missing-WebView2 prerequisite path is unverified.

## 6. Runtime bundling

`scripts/runtime-lock.json` pins official CPython 3.13.12 embedded x64, SHA-256 `76f238f606250c87c6beac75dccd35ee99070a13490555936abb6cb64ecce3d0`. `bundle_runtime.py` checks the archive hash, stages first-party modules and licenses, configures the isolated `_pth`, and smoke-tests imports. No pip install is needed by the installed user.

## 7. Runtime discovery

Production paths derive from Tauri resource locations. Hosts run with `-I -B -u -m` and an allowlisted module name. Developer/provider environment overrides are removed before approved vault credentials are added. Installed process inspection confirmed both Python hosts came from the installed `runtime` directory.

## 8. First-run UX

Welcome provides Create/Open Project, session recent projects, Getting Started and About/Diagnostics. The isolated first launch was observed with six available health entries and a separate missing-provider-credential message. Final footer and About both show native version `0.18.0-alpha`. See [UX evidence](UX.md).

## 9. Runtime health

Workflow/AI health requests, native display enumeration, Plugin service opening and an app-data write probe are real backend checks. Knowledge health establishes its shared host availability, not full project CRUD. Vision enumeration is not capture acceptance. Health checks never arm Input.

## 10. Project persistence

Project/session writes use validated temporary files, flush, atomic same-volume replacement and OS advisory writer locks. Recovery preserves a valid backup when the primary is corrupt. Project activation completes persistence/session work before exposing the new project; failed switching keeps the old project active. See [persistence details](PERSISTENCE.md).

## 11. Schema versions

Project assets and Knowledge remain v1; layouts retain their existing separately versioned localStorage records. No incompatible semantics were introduced under a reused version number.

## 12. Migration framework

The explicit v1 migration entry point validates and preserves the compatible document. No historical v2 transformation was invented. A future transformation must add source/destination validation and migration fixtures. Failed commits leave recoverable source data.

## 13. Backward compatibility

`tests/fixtures/project-v1/project-assets.v1.json` covers historical v1 payload preservation, including plugin references and compatible layout metadata. Automated identity checks pass. This is not installer upgrade evidence or proof that every Studio's historical UI layout is restored.

## 14. Upgrade behavior

The final installer was installed over an earlier Sprint 18 candidate of the same version on the disposable workstation profile; the project and Vision frame reopened. This is same-version replacement evidence only.

## 15. Downgrade safety

The current implementation refuses unsupported future schema versions before backup recovery or save, including when an older valid backup exists. Tests pass. This does not retrofit refusal behavior into already published older binaries.

## 16. Crash recovery

Existing interrupted-execution/no-replay semantics are retained. Runtime Job Objects terminate bundled children when Desktop dies. Installed acceptance now covers both the safe constant/delay workflow and an explicitly armed, Atlas-only mouse-move workflow. The armed run was interrupted by terminating Desktop PID 4348; after reopening, UI and persisted state show the same execution `execution-3d298d5c-6346-448c-ae65-a387d70ebafe` as `interrupted`, with no result and no new execution. The restarted toolbar is unarmed (`Arm Input`). See [safe reopen evidence](evidence/installed-crash-reopen.json), [Input evidence](evidence/installed-input-safety.json).

## 17. Workflow production E2E

Installed UI imported the five-node acceptance workflow, ran it through the bundled host and displayed `HELLO FROM ATLAS WORKFLOW RUNTIME`, 5/5 nodes completed. The final installer repeated this successfully: execution `execution-ba570ac0-97c4-4e93-9292-3458755bb9c7`, 4 ms reported runtime duration. The earlier candidate execution was `execution-2c471863-e460-4648-a14c-726d73bf5497`. Both results persisted in the project. Clean-machine repetition remains required.

## 18. Vision production E2E

Installed native capture displayed a desktop frame in Vision. The frame and selected workspace survived application restart and candidate replacement. Screenshot payloads are intentionally excluded from committed evidence. Full detection/template → RegionReference → explicitly armed Input → validation was not performed.

## 19. Input safety

Unarmed launch, explicit Arm, Atlas-only foreground restriction, in-app emergency stop, global Pause/Break cancellation and armed no-replay are PASS in the installed workstation build. The safe target was a blank Atlas canvas point and dangerous actions remained disabled. The new installed binary registered Windows `VK_PAUSE` with `RegisterHotKey`; an active delay workflow was cancelled by an OS-level Pause event and the toolbar returned to `Arm Input`. See [installed Input evidence](evidence/installed-input-safety.json).

## 20. Knowledge production E2E

The isolated bundled-host smoke exercised create/search/edit/restart/delete/restart without developer PATH or repository working directory. Installed UI creation, one-result search and update to version 2 succeeded. Installed restart exposed a frontend initialization race: the restored Knowledge workspace ran before project restoration, then did not reload when the project became ready. A failing regression reproduced it; initialization now waits for the project and tracks project changes. All 178 frontend tests pass. The rebuilt installer then automatically restored the project and version-2 entry; search returned the updated content. UI deletion followed by another process restart and search returned zero entries and 0 of 0 candidates. See [installed Knowledge evidence](evidence/installed-knowledge.json).

## 21. Marketplace production-build E2E

The installed build completed the full workstation lifecycle against the Local Development Registry: discover `atlas.acceptance.echo@1.2.0`, review the elevated outbound permission, install, enable, execute a contributed node, restart, disable and uninstall. The node execution completed 4/4 nodes with output `ATLAS_MARKETPLACE_1710`; after removal, the installed package set was empty while the saved workflow definition remained serialized with its plugin reference. Audit events and request IDs are recorded in [installed Marketplace evidence](evidence/installed-marketplace.json). Production registry and publisher PKI remain separate external infrastructure.

## 22. Plugin recovery

Existing transactional store and missing-plugin serialized-reference behavior remain. The Rust regression suite passes; installed interruption during package mutation and removed-plugin workflow reopening are unverified.

## 23. Workspace persistence

Installed project, selected Vision workspace and captured frame reopened. Frontend lifecycle regression covers workspace reset and cross-project isolation. Full five-Studio restart/layout and installed corruption matrix remain unverified; recent-project history is currently session-only except the last-project pointer.

## 24. Runtime lifecycle

Explicit shutdown and Windows kill-on-job-close ownership are implemented. After an observed normal close, no acceptance-path Python host remained. Bundled smoke includes repeated host cycles. A multi-cycle installed application orphan test remains outstanding.

## 25. Logging

Local timestamp/severity/subsystem/static event codes and validated backend correlation IDs are recorded. In-memory history is capped at 200 events; local log rotation is bounded around 256 KiB. Raw stderr, error strings, requests and provider responses are excluded.

## 26. Diagnostics

Final installed UI exported a 4,194-byte JSON file via the native create-new save dialog after executing the seeded synthetic-content workflow. [Seeded export evidence](evidence/installed-diagnostics-seeded.json) records the completed execution, export hash and redaction matrix; the export contains only schemaVersion, system, recentLogs and inclusionPolicy. It is local-only and does not overwrite an existing file. Historical crash logs and plugin inventories are not included by this minimal exporter.

## 27. Credential redaction

The installed seeded-content export was checked for API-key patterns, Authorization/Bearer, image/base64 payloads, Knowledge sentinel text and the fixture's private strings; none were found. Automated tests inject forbidden secret-like content and reject untrusted correlation values. This closes the seeded-secret matrix on the installed workstation; clean-machine confirmation remains outstanding.

## 28. Security review

Focused review covered subprocess/environment boundaries, credential vault access, persistence, diagnostic export and existing plugin validation. Native tests cover provider ID bounds, credential exclusion and real disposable vault round-trip. This is a focused engineering review, not a complete command-by-command security certification; Rust advisory scanning and hostile concurrent path substitution remain open.

## 29. Path safety

Static parent traversal, inappropriate UNC/device prefixes, symlink/reparse ancestors and redirected storage are refused. Native regression tests pass. Static checks do not eliminate malicious time-of-check/time-of-use substitution; no handle-relative hostile-race guarantee is claimed.

## 30. Privacy/network boundary

No new Atlas telemetry/upload or remote crash service was introduced. Diagnostics stay local. Provider requests occur through explicit AI execution; existing provider configuration remains the network boundary. The bundled local development registry uses local resources. An exhaustive packet-level production network audit was not performed.

## 31. Accessibility

Menus gained keyboard navigation/dismissal; onboarding and modal controls have semantics/focus styling; critical panels have independent error boundaries. Screen-reader, complete keyboard-only Studios and theme contrast acceptance remain open.

## 32. DPI/multi-monitor

User identifies the left physical display as monitor 2; that is the operational convention regardless of Windows device enumeration. In the installed acceptance run, the Atlas window was displayed there at capture originX `-2453`; File/Edit menus opened and dismissed with Escape, and Tab focus remained visible. Mixed-DPI movement still exposed clipping and native unparented dialogs opening on the other display; dialogs were manually moved before operation. Screen-reader, complete keyboard-only Studio, theme contrast and a full alternate-scaling matrix remain unverified, so full DPI/display acceptance is not PASS. See [installed DPI/accessibility evidence](evidence/installed-dpi-accessibility.json).

## 33. Performance

An initial process launch-to-window-handle detection was 643 ms. This is a workstation observation, not cold boot, rendered UI readiness, runtime readiness or project readiness. Complete cold/warm milestone measurements remain outstanding. Bundled-host smoke completed 21 checks in approximately 12.73 seconds. A short installed idle sampling pass remained responsive across three samples at three-second intervals; it is not a workflow benchmark. See [installed performance/memory/soak evidence](evidence/installed-performance-memory-soak.json).

## 34. Memory

Initial native working set at first window-handle detection was 22,335,488 bytes. A later installed idle sample observed Atlas at 31,625,216 bytes working set and the two Python hosts at 24,788,992 and 26,316,800 bytes, stable across nine seconds. This excludes a post-workflow baseline and does not establish leak-free behaviour; see [installed performance/memory/soak evidence](evidence/installed-performance-memory-soak.json).

## 35. Stability/soak

Automated regression and bounded component smoke pass. The installed idle sampling pass remained stable, but representative workspace/workflow/plugin soak and long-duration memory sampling remain unperformed because the preceding acceptance intentionally removed the disposable Marketplace plugin. No soak PASS is claimed.

## 36. Installer upgrade

No usable earlier public installer was found in the queried historical release assets; see [release evidence](evidence/historical-release-assets.json). Full previous-version installer upgrade is unavailable, explicitly separate from same-version candidate replacement. Compatible v1 fixtures were tested instead.

## 37. Uninstall/reinstall

Current-user NSIS strategy and user-data retention expectations are documented in [Getting Started](GETTING_STARTED.md). The installed uninstaller was run with **Delete the application data** unchecked: application files, the executable, the uninstaller and the Start Menu shortcut were removed, while the disposable project data was retained and no Atlas process remained. The final NSIS installer then reported successful completion; the executable, uninstaller, running process and Start Menu shortcut were restored, and the retained Marketplace project reopened with its workflow state. See [installed uninstall/reinstall evidence](evidence/installed-uninstall-reinstall.json). This is workstation evidence; clean-machine acceptance remains outstanding. Both recorded pre-existing Roaming/Local profile directories were restored after closing the acceptance app; test profiles were retained separately. See evidence/profile-restoration.json.

## 38. Release pipeline

CI resolves a validated existing prerelease tag to an immutable SHA, checks version agreement, installs frozen dependencies, bundles runtimes/notices, builds MSVC NSIS with `--locked`, and uploads checksummed artifacts. No tags or public releases are created. Hosted CI has not run in this session.

## 39. Artifact metadata

Filename: `Atlas_0.18.0-alpha_x64-setup.exe`; size: **227,702,216 bytes**; version: **0.18.0-alpha**; target: **x86_64-pc-windows-msvc**; installer: **NSIS current-user**. Local output is under `apps/atlas-desktop/src-tauri/target/release/bundle/nsis/`. See [machine-readable metadata](evidence/final-artifact.json).

## 40. Checksums

Final SHA-256: `f99bcd6c72b634f364fcc58a98b5fd819d98da5ad56cd8ec6fe87e671871d941`. This identifies the build with the Knowledge initialization fix and Windows global Pause/Break emergency stop, superseding earlier candidate hashes. Embedded commit metadata identifies the baseline HEAD, not a committed copy of the full worktree changes.

## 41. Code-signing status

Unsigned. No trusted certificate or SmartScreen reputation is claimed. These are external release conditions, not reasons to mark incomplete internal acceptance PASS.

## 42. Dependency locks/security

Frontend and Cargo lockfiles are retained; root Cargo.lock is now includable in source control. A fresh `pnpm audit --json` and `pnpm audit --prod --json` on 2026-09-11 report zero advisories across 289 total and 48 production dependencies. `cargo-audit` is not installed, so Rust advisory review is not cleared; the license inventory also retains 18 missing metadata/text items and two optional frontend dependency resolutions. See [dependency review](DEPENDENCY_AND_REGRESSION_REVIEW.md) and [final dependency/license evidence](evidence/dependency-license-final-review.json).

## 43. License inventory

The notices bundler records 381 production dependency entries and 626 original notice files with hashes. Missing text/metadata obligations are explicitly recorded in [notices review](NOTICES.md); inventory generation does not clear all redistribution obligations.

## 44. Automated tests

Root Rust, combined Python, frontend and Desktop native tests ran separately. Frontend lint/typecheck/build passed after the final version/lifecycle changes. Development tests do not prove clean Windows installation.

## 45. Exact test counts

| Suite | Passed | Failed |
|---|---:|---:|
| Root Rust workspace, MSVC | 348 | 0 |
| Combined Python regression | 717 | 0 |
| Frontend, 25 files | 178 | 0 |
| Desktop native Rust | 17 | 0 |
| Total across these separate suites | 1,260 | 0 |

The 21 bundled-host smoke checks are separate acceptance checks, not additional unit tests. Earlier partial reruns are not added to totals. Default GNU Rust failed for missing `dlltool.exe`; explicit MSVC passed.

## 46. Build results

Final frontend build and optimized MSVC release succeeded. Tauri reported `Finished 1 bundle`; final silent installer returned 0. Use direct Node Tauri CLI invocation with Cargo arguments after `--` to preserve `--locked`; local pnpm wrappers did not preserve that separator reliably. Byte-for-byte reproducibility is not asserted.

## 47. Clean-machine environment

Only the existing Windows developer workstation was available. Acceptance used a disposable Atlas profile, install/project directories outside checkout, restricted PATH and no Python environment overrides. Codex Windows package filesystem virtualization redirects apparent AppData paths into its package LocalCache. This is not a clean machine. The current session had no available virtualization tool or identified clean VM; optional-feature inspection also required elevation. See [clean Windows lifecycle evidence](evidence/clean-windows-lifecycle.json).

## 48. Clean-machine E2E

NOT RUN. The required clean Windows 20-step lifecycle is still a release gate. Workstation installed observations and copied embedded-host tests are useful but cannot substitute for it. A clean VM or separate machine must be provisioned before this can be marked PASS.

## 49. Upgrade E2E

Previous-version installer-to-installer flow is unverified due to unavailable historical assets. Fixture validation and same-version replacement do not establish that flow.

## 50. Crash/failure E2E

Final installed AI host PID 24128 was deliberately terminated while Desktop PID 27748 remained alive. UI health then showed AI unavailable while Workflow, Vision, Knowledge, Plugin and Storage remained available. This proves idle AI failure isolation and controlled indication; automatic recovery was not established. The subsequent safe and armed active-workflow Desktop terminations produced persisted interrupted records; UI reopen confirmed interrupted with no new execution. See [failure evidence](evidence/installed-runtime-failure.json), [crash checkpoint](evidence/installed-crash-recovery.json) and [Input evidence](evidence/installed-input-safety.json).

## 51. Mandatory acceptance matrix

PASS below is bounded by its evidence column. PARTIAL/NOT RUN are internal outstanding acceptance, not fabricated external conditions.

| ID | Scenario | Status | Evidence / remaining gate |
|---|---|---|---|
| B-A | Production installer builds | PASS | Final NSIS built and installed, exit 0 |
| B-B | Clean install | NOT RUN | Clean Windows environment required |
| B-C | Launch without dev dependencies | PARTIAL | Restricted PATH installed launch; clean machine absent |
| B-D | First run | PASS, workstation | Isolated profile Welcome and health observed |
| B-E | Bundled Runtime startup | PASS, workstation | Installed host paths and health |
| B-F | Project create/reopen | PASS, workstation | Native folder creation/open and restart |
| B-G | Workflow production E2E | PASS, workstation | Final installer 5/5 with expected output; clean-machine gate remains |
| B-H | Vision capture | PASS, workstation | Installed capture and restored frame |
| B-I | Input safety | PASS, workstation | Installed arm, Atlas-only safe move, in-app emergency stop and global Pause/Break cancellation pass; clean-machine gate remains |
| B-J | Knowledge persistence E2E | PASS, workstation | Installed create/search/edit/restart/search/delete/restart/zero-result flow completed |
| B-K | Marketplace/plugin E2E | PASS, workstation | Discover/install/enable/node execute/restart/disable/uninstall; saved workflow retained after removal; clean-machine gate remains |
| B-L | Restart persistence | PARTIAL | Project/Vision observed, complete Studio matrix outstanding |
| B-M | Migration | PASS, fixture scope | Supported v1 identity preserved; no v2 invented |
| B-N | Migration failure recovery | PASS, automated | Injected failure/backup/future-version tests |
| B-O | Crash → interrupted/no replay | PASS, workstation | Safe and armed Atlas-only workflows interrupted in UI and file after Desktop termination; no automatic replay; clean-machine gate remains |
| B-P | Runtime failure isolation | PASS, idle AI scope | Host killed; UI survived; controlled unavailable status |
| B-Q | Diagnostics/redaction | PASS, workstation | Seeded synthetic workflow completed and native export redaction matrix passed; clean-machine confirmation outstanding |
| B-R | Unicode/space paths | PASS, workstation | Installed and project paths include all requested classes |
| B-S | DPI/display regression | PARTIAL | Installed left-monitor keyboard/menu checks pass; mixed-DPI clipping/dialog location gaps and full accessibility matrix remain |
| B-T | Full regression suite | PASS | 1,260 tests across four suites; lint/typecheck/build |
| B-U | Installer upgrade | UNAVAILABLE HISTORY | No earlier distributable; fixtures tested |
| B-V | Uninstall/reinstall | PASS, workstation | Uninstaller cleanup, user-data retention, reinstall, shortcut restoration and project reopen verified; clean-machine gate remains |
| B-W | Artifact checksum | PASS | Final SHA-256 and byte size recorded |
| B-X | Security review | PARTIAL | Focused review done; advisory/full boundary gates open |

## 52. External conditions

Live OpenAI/Ollama response, production Marketplace registry, publisher certification PKI, trusted Windows signing certificate and SmartScreen reputation remain unverified external conditions. Demo providers are not live-provider evidence.

## 53. Known limitations

Clean-machine proof, complete DPI/accessibility, representative performance/memory/soak, Rust advisory clearance and final redistribution/license review remain. These are tracked as outstanding, not silently waived. Original isolated profiles have been restored; disposable test results remain separately preserved.

## 54. Final verdict

**SPRINT 18: PARTIAL — BETA READINESS: NOT YET.** The implementation and real installer are substantial progress; mandatory acceptance is incomplete. No claim that Atlas has been proven outside a developer machine is justified yet.

## 55. Recommended next step

Provision a clean Windows VM or separate machine and run the prescribed full lifecycle with the final installer checksum, including Marketplace and uninstall/reinstall. In parallel, run a current RustSec advisory scan and resolve the outstanding redistribution metadata; append reproducible evidence for each. Update this report only with observed results; tag/publish requires separate authorization.

## 56. Final Beta Readiness Review

Reviewed 2026-09-11. Evidence links and mandatory-matrix scopes are consistent: workstation PASS results remain explicitly bounded, while clean Windows lifecycle is recorded as NOT RUN. The final verdict remains **PARTIAL — BETA READINESS: NOT YET**. Open release gates are captured in [final review evidence](evidence/final-beta-readiness-review.json).
