# Sprint 15.5 — Secrets, Persistence & Recovery Hardening

## Security boundaries

### Provider credentials

The production Desktop path is:

`password input (component-local state) -> Tauri ai_credential_set -> Windows Credential Manager -> Python host process`

The credential value is never returned through IPC. React can query only whether a provider has a configured credential. Credential-shaped keys are rejected from Project Asset persistence in both TypeScript and Rust. The normalized request/response inspectors do not contain credential fields. `ATLAS_AI_API_KEY` and `OPENAI_API_KEY` remain developer/CI compatibility fallbacks, not the Desktop configuration UX.

The current native vault implementation is Windows-only. Other platforms fail closed until their native Keychain/Secret Service adapter is added.

### Project-owned assets

An opened project owns `.atlas/project-assets.v1.json` and `.atlas/project-assets.v1.backup.json`. The document contains:

- AI prompts, sessions, active conversation, model selection, inference configuration and context references;
- the editable Workflow definition and execution snapshots;
- the Vision document/session and timeline;
- Workflow, Vision and AI Studio layouts plus the active Studio;
- explicit recovery metadata.

Writes use a temporary document and recovery backup. A corrupt primary document falls back to the backup. localStorage remains a layout rendering cache, but the canonical recoverable copy is stored under the project.

### Restart semantics

Terminal workflow runs remain terminal. Runs saved as `created`, `initializing`, `validated`, `scheduled`, `running`, `paused` or `restarting` restore as `interrupted`, receive an `INTERRUPTED` diagnostic and never resume side effects automatically. The operator must inspect and explicitly restart them.

Input permission is intentionally not persisted. Every application/host restart returns the real Input Runtime to unarmed state.

## Automation safety

All provider-independent input requests pass through `InputSafetyController` before `WindowsInputProvider`:

- fail-closed explicit arm/permission;
- required foreground-window title policy checked before every action;
- per-second action rate limit and typed-text limit;
- dangerous shortcut, held system modifier and excessive-click rejection unless a separately confirmed policy permits them;
- in-app Emergency Stop and Escape action;
- global Windows `Pause/Break` watchdog, provider-side interruption of long mouse/type operations, release-all and a latched emergency-stopped state;
- automatic release-all when a workflow finishes, fails or is cancelled.

Re-arming requires an explicit confirmation and target window title. The default UI never enables dangerous actions.

## Verification

- Frontend: Project credential rejection, interrupted-run recovery, AI request credential exclusion and the complete Workflow/AI UI suite.
- Python: unarmed rejection, focus policy, dangerous-action denial, rate limiting, emergency release and Desktop Workflow host integration.
- Rust: credential-shaped Project Asset rejection, safe token-usage fields, provider ID validation and Windows Credential Manager compilation.
