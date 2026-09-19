# Sprint 18.1 — Final Real-Machine Acceptance

This checklist begins only after repository CI and the GitHub-hosted Windows installed-product smoke are green. It is intentionally limited to evidence that cannot be established faithfully by headless CI. Do not convert an unobserved item to PASS.

## Environment record

Record before testing:

- Atlas commit SHA and installer SHA-256.
- Windows edition/version/build and architecture.
- GPU and graphics driver version.
- Display count, physical arrangement, resolution, scale factor, and primary display.
- Whether WebView2 was already installed.
- Test account privilege level.
- Installation path and project path.

Use paths containing spaces and non-ASCII characters for at least one installation/project run.

## RM-A — Clean installation and first launch

1. Start from a Windows machine/profile that has no Atlas source checkout and no Atlas development environment dependency in PATH.
2. Install the exact candidate installer.
3. Launch from the installed shortcut/executable, not a repository command.
4. Confirm Welcome/Create/Open/Recent/Getting Started/About/Diagnostics render without unexpected WebView console errors.
5. Confirm runtime health is reported independently from missing AI provider credentials.
6. Confirm Atlas starts unarmed.

Evidence: screenshots, installer hash, process executable paths, diagnostics export.

## RM-B — Five-workspace persistence

For Workflow, Vision, AI, Knowledge, and Marketplace:

1. Open the workspace.
2. Move at least one panel and resize a splitter.
3. Where supported, close/reopen a panel.
4. Switch to another workspace.
5. Close Atlas normally and relaunch.
6. Confirm each workspace restores its own layout and no panel is cloned or replaced by another workspace's layout.
7. Corrupt one disposable layout/state fixture through the supported acceptance mechanism and confirm only that workspace falls back safely.

Evidence: before/after screenshots and diagnostics. Do not manually edit production user data unless the acceptance mechanism explicitly supports it.

## RM-C — Installed visual closed loop

Using a disposable Atlas-owned target:

1. Capture the target through installed Vision Studio.
2. Resolve it through Detection or Template matching to a RegionReference.
3. Feed the reference to an Input mouse action without storing hard-coded click coordinates.
4. Arm Input explicitly.
5. Confirm foreground restriction.
6. Execute the action.
7. Capture again and validate the expected target state change.
8. Repeat once after Atlas restart.

PASS requires the reference-driven path: Vision → RegionReference → Input → post-action Vision validation.

## RM-D — Input safety and kill switch

1. Confirm restart is unarmed.
2. Arm and execute a harmless Atlas-owned input workflow.
3. Move focus outside the allowed target and confirm action is blocked.
4. During an active delay/held-input scenario, trigger the global Pause/Break kill switch.
5. Confirm execution cancels, held input is released, and Atlas disarms.
6. Relaunch and confirm no automation replay occurs.

Do not use destructive shortcuts or third-party applications as targets.

## RM-E — Mixed-DPI and multi-monitor

Test each available display and at least two scale factors if the hardware permits:

1. Move Atlas between monitors.
2. Verify menus, modal dialogs, native file/folder pickers, tooltips, panel drag/drop, and Vision coordinates.
3. Capture a target on a non-primary monitor, including a monitor with negative desktop coordinates when available.
4. Confirm the RegionReference/Input action lands on the intended physical target.
5. Confirm no clipping, unreachable modal, incorrect scaling, or coordinate offset.

If only one display/scale factor is available, record this gate as NOT FULLY RUN rather than PASS.

## RM-F — Keyboard and accessibility acceptance

Without using the mouse for the tested path:

1. Navigate top-level menus and dismiss with Escape.
2. Reach all five workspaces and their primary actions.
3. Operate onboarding and modal controls.
4. Verify visible focus indication.
5. Verify logical focus order and that focus returns after modal dismissal.
6. Run Windows Narrator (or equivalent supported screen reader) through Welcome, project open/create, Workflow run controls, Input arm warning, and Diagnostics.
7. Check light/dark themes at normal and high-contrast/relevant Windows contrast settings.

Record specific inaccessible controls; do not summarize partial coverage as PASS.

## RM-G — Process lifecycle and soak

1. Perform at least 10 normal launch/close cycles.
2. After every close, verify no Atlas-owned Python host remains.
3. Run a representative 60-minute session that includes workspace switching, repeated Workflow runs, Vision captures, Knowledge searches, and local Marketplace enable/disable cycles.
4. Sample Atlas and child-process working set at start, 15, 30, 45, and 60 minutes.
5. Record crashes, unbounded growth, stalled runtimes, orphan processes, and unexpected logs.
6. Kill one disposable runtime host and confirm failure isolation; record whether recovery is automatic or requires an explicit action.

A stable short idle sample is not a substitute for this soak.

## RM-H — Marketplace interruption/recovery

With a disposable local-development package:

1. Begin an install/update transaction.
2. Interrupt Atlas at the documented safe acceptance point.
3. Relaunch.
4. Confirm the package store is either the old committed version or the new committed version, never a mixed partial state.
5. Confirm owner/node registration matches the committed package state.
6. Remove the plugin and reopen a workflow that still contains its serialized node reference.
7. Confirm the graph remains readable and execution fails with the documented unavailable-plugin error instead of silently substituting behavior.

## RM-I — Diagnostics/privacy

1. Seed disposable sentinel strings resembling an API key, Authorization/Bearer header, private Knowledge content, image/base64 payload, and local project path.
2. Exercise affected panels/runtimes.
3. Export Diagnostics through the installed UI.
4. Confirm secrets/private payloads are absent and only the documented diagnostic schema is exported.
5. Confirm no automatic telemetry/upload occurs during the acceptance run.

Never use a real credential as a redaction test fixture.

## RM-J — Upgrade/reinstall boundary

If a real previous installer exists, install it first and perform installer-to-installer upgrade while retaining an existing project. If no previous distributable exists, keep the historical upgrade gate recorded as UNAVAILABLE HISTORY; fixture migration and same-version replacement are not equivalent.

Always test uninstall/reinstall of the current candidate both with retained user data and with the product's supported clean-data option where available.

## Final evidence rule

A real-machine PASS requires recorded evidence for every applicable RM gate above. Hardware-unavailable cases remain NOT FULLY RUN. External AI provider availability, production Marketplace infrastructure, publisher PKI, trusted code signing, and SmartScreen reputation remain separate external conditions and must not be simulated.

After completion, update the authoritative Sprint 18 beta-readiness report by changing only matrix rows supported by the collected evidence. Do not create or publish a beta tag/release until that review is complete.
