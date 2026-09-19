# Atlas 0.18.0-alpha: getting started

This is an unsigned Windows x64 alpha candidate. Beta readiness is not established until the acceptance matrix in [the report](SPRINT_18_BETA_READINESS_REPORT.md) passes.

## Install and launch

Run `Atlas_0.18.0-alpha_x64-setup.exe` and choose a per-user installation directory. The package includes Atlas, its Python hosts, third-party notices, and the WebView2 offline installer. Normal use does not require Node, pnpm, Rust, Cargo, global Python, a checkout, or execution-policy changes. WebView2 installation is conditional on the machine's existing runtime. Windows may show SmartScreen warnings because Atlas has no trusted production signature/reputation; do not interpret this candidate as trusted production distribution.

Launch Atlas from its shortcut. Welcome shows Create Project, Open Project, current-session recent projects and Getting Started. A previous session reopens its last project when compatible; failures leave a visible controlled message. Choose a dedicated local folder, including paths with spaces or Unicode. Network/device paths and redirected metadata paths are unsupported. Atlas stores metadata under `.atlas` and retains explicit version identifiers. A newer unsupported project must be opened with a compatible release.

## Work with studios

- Workflow: create a safe Entry → Constant → Output → Exit graph, validate and Run. Inspect execution output. A sample is in the source distribution's `examples/workflow` and Sprint 18 fixtures; use only data operations for initial acceptance.
- Vision: open Vision Studio and capture your display deliberately. Screen content is private; capture does not upload it to an Atlas service. Validate detection/reference resolution before Input.
- Input: starts unarmed, including after restart. Explicit Arm is required; keep the allowed foreground application and rate/shortcut policy narrow. Emergency Stop and global Pause/Break stop input; Release All releases held inputs. Restart never automatically replays a desktop action.
- Knowledge: open a project, create a note, search and edit it. Changes are project-scoped. Close/reopen to verify persistence; deletion should remain absent after restart.
- Marketplace: the bundled source is **Local Development Registry**, using development trust. Inspect permissions, install, then explicitly enable a package. Disabled/missing plugin nodes remain serialized and cannot execute. This is not a production Marketplace or publisher certification service.
- AI: use AI Studio's provider configuration and Windows credential vault. Runtime availability is independent of credential/provider availability. Real provider inference is an external condition until a real response is observed. No demo fallback establishes live acceptance.

## Recovery and support

Save/close before moving project folders. Only one Atlas instance per Windows user may run. OS-owned locks release after abnormal process termination; do not delete internal locks manually. Interrupted executions require explicit user action and do not resume desktop automation automatically. Valid backups can be read when supported; unknown future versions are never treated as ordinary corruption.

Help → About / Diagnostics reports executable version/build and measured runtime status. Export Diagnostics chooses a **new** JSON filename and writes locally; existing files are not overwritten. It includes version, OS family, architecture, runtime health and bounded static event codes. It excludes credentials, project paths/content, Knowledge, conversations, screenshots and raw Runtime stderr. Inspect a bundle before sharing it yourself. Atlas does not upload it.

## Upgrade, uninstall and reinstall

Updates are manual installer updates; no remote updater is configured. Back up projects before testing alpha upgrades. The current v1 schema is preserved; there is no fabricated v2 migration or historical installer. An older binary's behavior cannot be retroactively fixed; avoid opening newer incompatible state with old releases.

Uninstall removes application binaries and shortcuts. Preserve user data when the uninstaller offers an optional data-removal choice; do not select removal for upgrade/reinstall testing. Projects outside the install directory and Windows Credential Manager entries are not installer-owned content. Reinstall is intended to reopen compatible retained state. Verified versus unverified uninstall/upgrade behavior is recorded in the report.

## Developer builds (separate from end-user installation)

From the checkout, with committed locks and an MSVC toolchain:

```powershell
python -B scripts/bundle_runtime.py
python -B scripts/bundle_notices.py
cd apps/atlas-desktop
pnpm install --frozen-lockfile
$env:RUSTUP_TOOLCHAIN = 'stable-x86_64-pc-windows-msvc'
node node_modules/@tauri-apps/cli/tauri.js build --target x86_64-pc-windows-msvc --bundles nsis -- --locked
```

The direct CLI invocation preserves the Cargo `--locked` separator with the pinned pnpm version. Record compiler versions and artifact SHA-256. Locked dependencies do not imply bit-for-bit reproducibility. Do not create tags or publish a public release without authorization.
