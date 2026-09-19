# Sprint 18 initial repository audit

Initial HEAD: `9fa08d477f26b3c9ea4ed2f0f48858a2406ba66e`. Existing tags: `v0.15.0-alpha`, `v0.17.0-alpha`. No tags created or replaced. Existing modified caches, tsbuildinfo and untracked acceptance/temp files predate this work.

Sprint 17 report accepts M-A–M-T under **Local Development Distribution**. Its native evidence explicitly uses a debug executable and Vite; it does not establish installer acceptance. Historical results remain unchanged.

| Area | Current State | Developer Dependency | Beta Gap | Required Action |
|---|---|---|---|---|
| Version | Desktop manifests 0.15.0-alpha; v0.17 tag exists | None | stale Desktop metadata; old policy proposes 1.0 beta | use requested pre-1.0 0.18.0-alpha; no tag |
| Tauri / installer | Tauri 2.11.5, bundle all, empty icons, no resources | frontend build tooling | no proven Windows product | NSIS current-user package, bundled resources |
| Frontend | React 19/Vite 7, dist configured | Vite only for debug | release not exercised | build dist and package |
| Runtime launch | lib.rs searches ancestors/ATLAS_ROOT, global Python, PYTHONPATH | checkout and Python | critical production blocker | resource-dir embedded interpreter, isolated module path |
| Runtime inventory | Workflow host includes Input/Knowledge; separate AI host; native Vision capture/bridge | Python stdlib, Rust Windows APIs | no interpreter delivery | pin official embedded CPython and ship first-party modules |
| Dependencies | pnpm/Tauri Cargo locks present; root Cargo.lock ignored/untracked; Python hosts stdlib | build tools | root lock not committed; interpreter not pinned | include root lock; hash-lock interpreter; inventory |
| Subprocess lifecycle | Drop kills/waits; piped stderr printed; stdin EOF handling | inherited environment | crash/orphan acceptance missing | parent-death protection and explicit exit cleanup |
| First run / version | existing project picker and sessions; About hardcoded | no installer evidence | coherent welcome/health missing | reuse shell/design system and backend version |
| Project assets | fixed v1 JSON envelope, backup rename sequence | none | future version fallback and crash window | validated recovery and atomic replacement |
| Knowledge storage | v1 JSON, backup, os.replace | none | future schema could restore older backup | fail closed before recovery/write |
| Migration | version fields exist | none | fixtures/failure evidence absent | retain compatible v1 semantics, explicit version gate and fixtures |
| Concurrent access | plugin store exclusive lock; project writes not globally protected | none | unsafe competing writers | storage locks and single-instance strategy |
| Workflow recovery / Input | existing snapshot/recovery contracts and unarmed Input default | native host | installed kill/restart not tested | preserve no replay and test installed lifecycle |
| Workspace | per-workspace FlexLayout/localStorage | WebView user profile | corruption/restart evidence needed | targeted fallback/selector checks |
| Plugins | signed bounded ZIP, local registry, transactional package store | registry in repo | installed discovery path missing | explicitly named bundled Local Development Registry |
| Credentials | Windows keyring, validated provider IDs | Windows Credential Manager | stderr content not guaranteed safe | metadata-only diagnostics; regression tests |
| IPC / paths | existing backend validation, fixed asset names, constrained plugin actions | none | trust boundary review incomplete | bounds/path regression and controlled errors |
| Logs / diagnostics | runtime stderr console; no user export | developer console | no production support bundle | bounded structured metadata logs, explicit allowlist export |
| Network / privacy | AI urllib OpenAI/Ollama; Marketplace local filesystem | optional provider | boundary documentation missing | document explicit AI calls and no Atlas telemetry |
| Release workflow | Linux Rust/Python only; some jobs checkout default ref | CI toolchain 1.80 | no Windows package/checksum; ref mismatch | locked Windows artifact job and exact ref |
| Updates | no configured updater | manual installer | upgrade artifact unknown | manual install-over, no fake historical installer |
| Security / ownership | SECURITY.md stale 0.10 table, CODEOWNERS present | maintainer review | dependency and IPC review needed | report evidence and unresolved items |
| Constraints | existing Runtime/Plugin ADRs and Sprint15–17 contracts | none | no need for new Runtime architecture | preserve bridges and constrained plugin model |
| Clean Windows | current machine is developer workstation; Sandbox feature inspection needs elevation | current workstation | clean-machine proof absent | inspect availability; never equate isolated PATH test to clean VM |

This is a pre-implementation gap assessment, not acceptance evidence. Final verdict is in the readiness report.
