# Sprint 17 — Marketplace and Plugin Distribution

**SPRINT 17: COMPLETE** for the local development distribution profile. All M-A through M-T acceptance items pass. Production registry/trust services remain separate external conditions. Evidence distinguishes automated tests from native Desktop observations.

Implementation commit: `0e4bf42` (new commit above the preserved baseline). The report and evidence are recorded in a separate follow-up commit.

## Initial repository audit

| Area | Existing | Complete | Reusable | Missing |
| --- | --- | --- | --- | --- |
| Stable baseline | HEAD a5b2acb; bd384d6, 33ac4de, af439fd present | Yes | All existing history | New Sprint 17 commits |
| Plugin Runtime | packages/plugin Rust manager, loader, lifecycle, provider/factory contracts | Core only | Yes | Desktop composition and package execution provider |
| Canonical manifest | PluginManifest, from_json, compatibility, capabilities, permissions | Partial validation | Yes | Distribution entrypoint and platform validation |
| Version/dependencies | SemanticVersion, VersionConstraint, DependencyResolver | Implemented | Yes | Distribution integration |
| Packaging/discovery/trust | RFC-0213/0216/0217; ZIP, SHA256, signature catalog | Specs only | Contracts | Acquisition, verification, installation |
| Permissions/isolation | SandboxPolicy and scoped PluginContext | Policy model | Yes | Reviewed grants and distribution enforcement |
| Workflow Runtime/bridge | Python host, PluginBridge, dynamic register_plugin | Constrained operations only | Yes | Rust Runtime execution bridge and durable registrations |
| Plugin Test | Built-in prefix node and dynamic safe plugin declarations | Existing regression path | Yes | Disposable signed acceptance packages |
| Registry ownership | Frontend pluginId/hotReload; host dynamic owner map | Partial | Yes | Atomic owner synchronization and missing-node errors |
| Health/events | Rust plugin event bus and health monitor; Tauri host events | Core only | Yes | Distribution audit/provenance and UI |
| Desktop Extensions | Hard-coded demo store and logging service | No real lifecycle | Shell only | Route to authoritative Marketplace |
| Desktop shell | WorkspaceManager, FlexLayout, panel/command registry, design system | Yes | Yes | Marketplace workspace/panels/commands |
| Layout persistence | atlas.layout.<workspace>.v1 | Yes | Yes | Marketplace layout |
| Tauri/Python hosts | Persistent Workflow/AI hosts; bridge requests | Yes | Yes | Marketplace IPC and Rust plugin bridge |
| Storage/project | StorageProvider contracts; backend project assets and user app-data | Existing | Yes | Backend package store and atomic state commit |
| Input/security | Arm, emergency stop, kill switch; secure AI credential boundary | Existing regression baseline | Yes | Regression evidence; no plugin bypass |
| Knowledge/AI/Vision | Runtime bridges and scoped knowledge references | Existing | Yes | Preserve existing boundaries; no direct privileged API |
| RFC/ADR/conformance | ADS, ADR-0005, Plugin/Runtime/Storage RFCs and conformance tests | Existing | Yes | Sprint 17 implementation evidence and limitations |
| Tests/docs | Python, Rust, Vitest, build/lint, Sprint 15/16 acceptance | Existing | Yes | Distribution tests and real Tauri lifecycle acceptance |

## Implementation plan

1. Add distribution contracts and signed ZIP verification using the canonical Rust manifest and dependency resolver.
2. Compose the existing PluginManager with a constrained package provider, backend storage, transactions, permissions and recovery.
3. Connect Python Workflow PluginBridge to Rust execution through the existing Tauri host protocol, and synchronize owner-scoped metadata.
4. Add Marketplace panels, commands and layout with backend-authoritative presentation state; route Extensions there.
5. Add signed disposable acceptance packages, negative tests, regressions and real Desktop acceptance; report exact results.

The package provider extends the existing constrained data-operation model; arbitrary native/script execution remains unsupported and rejected. Development signing keys establish local integrity only, not production certification. AI Studio remains feature-frozen; live-provider acceptance remains PENDING EXTERNAL CONDITION.

## Implemented architecture and required report topics

Detailed contracts, trust framing, storage decisions and limitations are in [DISTRIBUTION_PROFILE.md](DISTRIBUTION_PROFILE.md). Fixtures and reproduction commands are in the [registry README](../../marketplace/local-development/README.md).

| Topics | Implementation / evidence |
| --- | --- |
| 2. Stable baseline | Work began at a5b2acb. bd384d6, 33ac4de and af439fd remain in history. No reset, force push, tag replacement or AI feature expansion. Generated caches and existing temporary files are excluded from commits. |
| 3–4. Architecture / Runtime reuse | MarketplaceService composes the existing Rust PluginManager, PluginProvider/Factory, lifecycle, registry, health, dependency resolver and canonical manifest. Concrete Rust Plugin instances execute package-provided operations. |
| 5–6. Provider / Studio | LocalRegistry implements discovery/acquisition behind MarketplaceProvider. Three Marketplace panels reuse WorkspaceManager, FlexLayout, central panel registration, design-system controls and independent layout persistence. |
| 7–10. Manifest / format / identity / version | Canonical PluginManifest; signed ZIP with bounded declarative entrypoint. Manifest ID and version must match discovery. Identity history prevents different content reusing an ID/version. Updates use canonical semantic ordering. |
| 11–13. Compatibility / integrity / trust | Runtime/API and OS/architecture validation; whole-archive SHA-256, exact content checksums and strict Ed25519 verification. Development-key provenance is explicit. No production verification claim. |
| 14–16. Permissions / pipeline / rollback | Inspection pins exact bytes and permissions under a review token. Explicit approval precedes staging, activation, owner synchronization and atomic state commit. Load, registration and commit rejection restore prior runtime/state. |
| 17–18. Dependencies / storage | Required dependencies resolved by existing canonical resolver; missing/incompatible/cyclic graphs reject. Removal cannot break installed dependents. Dedicated backend app-data store provides exclusive locking and atomic filesystem commits. |
| 19–22. Enable / load / registration / execution | New installs disabled; enable invokes PluginManager load/start. Python receives versioned owner metadata and PluginBridge calls Rust through existing Tauri host messaging. No package-specific ID branch or frontend execution. |
| 23–24. Update / escalation | Newer versions preserve enabled state and contributed type compatibility. Every update requires exact review, including new grants. Rejected review leaves old version intact. |
| 25–28. Uninstall / missing nodes / restart / recovery | Uninstall unregisters only the owner and commits absence before blob deletion. Saved nodes remain visible and serialized; execution rejects with PLUGIN_UNAVAILABLE. Restart re-verifies committed blobs and restores enabled state. Orphan cleanup preserves unrelated files. |
| 29–33. Failure / security / paths / credentials / Input | Finite data operations have no native, shell, filesystem, network or credential API. Controlled failure is isolated. ZIP traversal, links, duplicate paths, Windows devices and oversized content reject. Grants never arm Input; emergency stop remains independent. |
| 34–36. Knowledge / AI / Vision | Existing runtime bridges remain intact. Packages receive no direct access to these services. Their regression suites pass. AI live-provider acceptance remains external and was not fabricated. |
| 37–39. Events / health / audit | PluginManager retains its existing events and health. Distribution emits canonical lifecycle actions and structured failures; latest 100 records retain request IDs, timestamps and available version/digest/source provenance. Enabled health follows successful activation/recovery, with failures displayed explicitly. |
| 40–41. Commands / Extensions | marketplace.open, search, installed, updates, installLocal and refresh use the central command system. Extensions routes to the authoritative installed view. |
| 42–48. Automated tests / counts / TS / lint / Python / Rust / build | Exact results and commands below. Native debug backend and production frontend builds pass. |
| 49–50. Native E2E / negative acceptance | Real Windows Tauri lifecycle observations are recorded separately from automated error injection. See matrix and execution IDs below. |
| 51. Sprint 15/16 regression | Root Python, Rust workspace, Desktop, Tauri, AI, Knowledge and Vision suites pass. Existing Input safety and built-in Plugin Test coverage remains intact; no live external-provider success is inferred. |
| 52–53. External conditions / limitations | Local development source only; no production registry, publisher PKI/revocation, remote acquisition, arbitrary native-code sandbox or privileged capability broker. Review cancellation precedes mutation; local reads have no download queue. Node schema migrations and dependency auto-install are unsupported. Cleanup/audit writes are best effort under storage failure; fail-closed recovery errors remain visible. |
| 54–55. Verdict / next step | Final verdict follows the acceptance matrix. Next step is independent code review and a separately scoped production trust/registry design; do not present the development key as publisher verification. |

## Exact automated results

| Suite | Baseline at audited HEAD | Final | Result |
| --- | ---: | ---: | --- |
| Rust workspace | 329 | 348 | PASS; 19 new distribution tests; Plugin crate contains 152 total |
| Root Python | 314 | 322 | PASS; 8 new Marketplace host tests |
| Desktop Vitest | 151 | 161 | PASS; 20 files, 10 new Marketplace tests |
| Tauri Rust | 7 | 7 | PASS |
| Vision Python | 185 | 185 | PASS |
| AI Python | 111 | 111 | PASS |
| Knowledge Python | 19 | 19 | PASS |
| Total across these suites | 1116 | 1153 | PASS; targeted reruns are not counted twice |

The audited Desktop baseline includes hotfix tests added after the earlier Sprint 16 report; its 141 figure is not reused as the current baseline. TypeScript (`pnpm typecheck` and the build's `tsc -b`), ESLint with zero allowed warnings, Vite production build (388 modules), native Rust build and Tauri tests pass. Windows Rust commands use `+stable-x86_64-pc-windows-msvc`; the machine's default GNU linker setup is not used. [Extracted command results](evidence/test-results.txt) preserve the suite results without counting targeted reruns twice.

Reproduction: `cargo +stable-x86_64-pc-windows-msvc test --workspace` at root; `python -B -m pytest -q` with `src` and the Vision/AI/Knowledge package `src` paths on PYTHONPATH; `pnpm test`, `pnpm lint`, `pnpm build` in Desktop; `cargo +stable-x86_64-pc-windows-msvc test` in src-tauri. Package-specific Python suites run against their own tests. Raw local logs are `.acceptance/sprint17-*-tests.log`, `sprint17-build.log`, `sprint17-eslint.log` and `sprint17-tauri-build.log`; concise durable evidence is committed beside this report.

## Real Tauri acceptance

The repository debug executable ran the Vite-served UI inside Tauri on Windows, with its real persistent Python Workflow host and real Rust PluginManager. This was not browser simulation or an IPC mock. [Native observations](evidence/native-lifecycle.json) capture the full lifecycle and preserved workflow. The acceptance graph is [sample-workflow-marketplace.json](../../sample-workflow-marketplace.json).

| Native observation | Result |
| --- | --- |
| Discover, inspect and explicitly install Echo 1.0.0 | Package digest b4701b99b81e9db55265bc70141daa85849005b4aaba24f92699e7e28a680635; installed disabled, then enabled healthy |
| Imported saved graph; fresh runtime execution after restart | execution-0af1f140-b7c7-4987-844f-96480a2f5944; 5/5 nodes; value ATLAS_MARKETPLACE_1700 |
| Disable and attempt Run | Palette contribution absent; saved node shows missing/disabled; PLUGIN_UNAVAILABLE validation error |
| Re-enable and Run | execution-a23aac95-8487-4443-b149-620337942c99; 5/5; ATLAS_MARKETPLACE_1700 |
| Review and update to 1.1.0 | Exact update digest e80e28967400a0184e1b2d7eb3da22efe8a64231beed690651546a8ce4c6be9f; enabled state preserved |
| Full Desktop close/relaunch, then Run | execution-2a37ecad-c237-4098-a2f9-fce0c5f344e3; 5/5; ATLAS_MARKETPLACE_1710 |
| Uninstall and full close/relaunch | Installed view empty; contributed palette entry absent; saved graph intact and Run denied with PLUGIN_UNAVAILABLE |

Native outputs retain the previous successful result when a subsequent validation attempt fails; the current validation error is shown above it. This is existing Workflow result-history behavior, not evidence of execution while disabled.

The final rebuilt backend was also exercised through the native local-package picker, explicit review, reinstall and enable. The untouched saved graph recovered and execution `execution-b7972077-7859-48ae-88c1-edf711d631ed` completed all five nodes with `ATLAS_MARKETPLACE_1700`. A real palette click added a second owned Marketplace Echo node; Undo restored the graph. [Final native smoke evidence](evidence/final-native-smoke.json) records these observations. This final inspection leaves Echo 1.0.0 installed and enabled; the earlier uninstall/restart absence was verified before this deliberate reinstall. Historical evidence contains STARTED/STOPPED activity labels from the earlier build; final distribution activity uses the catalog's ACTIVATED/DEACTIVATED IDs.

## Mandatory acceptance matrix

| ID | Scenario | Evidence | Result |
| --- | --- | --- | --- |
| M-A | Discovery | Native six-package registry; Rust search/empty/semantic ordering | PASS |
| M-B | Manifest validation | Invalid ID/version/entrypoint/permission tests, unsigned package rejection | PASS |
| M-C | Compatibility rejection | Runtime/API and unsupported platform tests | PASS |
| M-D | Integrity rejection | Digest/signature rejection; modified committed blob never registers after restart | PASS |
| M-E | Permission review | Native exact-digest dialog; exact-grant backend tests | PASS |
| M-F | Install | Native review/install; local package pipeline; transactional tests | PASS |
| M-G | Enable/load | Native healthy enable; actual PluginManager lifecycle | PASS |
| M-H | Dynamic registration | Native palette ownership; Python duplicate/foreign-owner/metadata atomicity tests | PASS |
| M-I | Real execution | Native execution IDs and typed outputs above | PASS |
| M-J | Disable blocks execution | Native missing-node denial; backend execution denial | PASS |
| M-K | Re-enable restores execution | Native execution-a23aac95; duplicate registration test | PASS |
| M-L | Update | Native 1.1.0 + changed output; failed-health, failed-commit and failed-registration rollback tests | PASS |
| M-M | Permission escalation review | Exact old grants rejected for 1.1 test update; explicit new grants accepted; prior version retained on denial | PASS |
| M-N | Restart persistence | Native enabled/update/removed restart; automated disabled restart and offline recovery | PASS |
| M-O | Uninstall | Native removal and durable absence; owner-isolated multiple-package removal | PASS |
| M-P | Missing-plugin handling | Native intact unresolved graph; Python validation preservation and reinstall recovery | PASS |
| M-Q | Failure isolation | Runtime controlled-failure and failed-health packages; healthy runtime/other owners remain usable | PASS |
| M-R | Unauthorized capability | Undeclared Workflow declaration rejected; privileged probe returns structured PERMISSION_DENIED | PASS |
| M-S | Input safety | Root Input regressions and registration-does-not-arm/emergency-stop tests; native workflow never armed Input | PASS |
| M-T | Sprint 16 regression | Complete regression suites listed above | PASS |

Live AI provider, production marketplace availability and production publisher certification remain **PENDING EXTERNAL CONDITION / NOT PROVIDED**, separately from this local distribution acceptance.
