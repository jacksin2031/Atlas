# Sprint 18 UX implementation and evidence

## Delivered

- No project: Welcome screen replaces Studio panels and provides Create Project, Open Project, Open Recent, inline Getting Started and About / Diagnostics.
- Create/Open use the native directory picker and the existing project asset persistence boundary. Create initializes metadata in a selected directory; selecting an existing Atlas directory opens its project without overwriting its format.
- Project activation waits for validated asset loading/initialization and durable last-project pointer before setting the current project. Failed activation remains controlled; incompatible project data is not declared open. Concurrent open requests are rejected.
- Fresh projects reset private AI, Vision and Workflow in-memory stores before initial persistence. Save errors propagate during activation; debounced save failures remain user-visible notifications.
- Independent review repaired detached-project writes after failed activation, reset workspace/layout state between projects, and reject malformed execution runs before restoring AI state. A failed pre-switch save keeps the original project open so unsaved changes can be saved again.
- Closing saves assets and clears the durable session pointer before releasing ownership. A session-clear failure keeps the project and its autosave subscriptions active for retry.
- About queries `beta_system_info` for authoritative executable version, OS, architecture, build type, commit and runtime probes. It does not infer health from credentials. `export_diagnostics` uses a native save picker and backend allowlisted export; no browser fallback or upload.
- Legacy synthetic Run-menu runtime state mutations now open measured diagnostics. Help and Tools log-export entry points open the diagnostic flow. No hardcoded About version remains.
- Footer and Settings About use Tauri `getVersion()` through the shared `AppVersion` component. A failed native query displays version unavailable without inventing a release version.
- Each registered FlexLayout panel has an independent error boundary with a retry action and safe user message. The underlying error is not presented as a raw stack trace.
- Welcome uses existing Atlas buttons and active shell colours. About is a native modal dialog with Escape/focus containment. Menus support arrow navigation, Escape dismissal, and close when focus leaves. Primary controls have visible keyboard focus.

## Automated validation

Commands run from `apps/atlas-desktop`:

- `pnpm typecheck`: PASS (final lifecycle and native-version changes included).
- `pnpm lint`: PASS (final lifecycle and native-version changes included).
- `pnpm test`: 25 files / 178 tests PASS (2026-09-10, including the installed-restart Knowledge regression). Counts are not cumulative.
- `pnpm build`: PASS (`tsc -b && vite build`), 390 modules transformed. Final artifact may be rebuilt after integration.

Targeted tests cover unavailable backend onboarding, real runtime/provider status distinction, panel error containment, delayed activation, rejected future-schema activation, private data and layout isolation, rejected initialization writes, no writes after failed project load or stopped ownership, malformed execution rejection before AI restore, and preserving an active project after pre-switch save failure. Lint and typecheck were rerun successfully with these final review changes.

## Known gaps / unverified acceptance

- Installed Knowledge restart exposed initialization before asynchronous project restoration. The regression failed before the fix and now passes: initialization waits for a current project and reruns when it changes. Lint/typecheck and all 178 frontend tests pass; the rebuilt installer passed automatic project/Knowledge restoration, updated-content search and delete/restart/absence acceptance.

- The recent-project list currently persists only during the current process session. The last project is restored from backend app-data on restart; the Welcome UI explicitly describes its recent-list limitation.
- Create Project selects a directory rather than supplying a separate folder-creation wizard. Native picker folder creation is used where available.
- Layout corruption handling remains the existing `workspace/persistence` validation/default mechanism; it has not been replaced.
- Manual installed-build first-run, screen-reader use, complete theme contrast, DPI scaling, display movement and complete keyboard-only Studio operation require installed-Windows acceptance. Unit/build results do not claim those PASS.
- Runtime health and diagnostic-export native integration requires the backend commands and installed build. Browser tests deliberately reject missing IPC; they are not production-runtime evidence.
- No new remote telemetry or crash reporting service was introduced.
