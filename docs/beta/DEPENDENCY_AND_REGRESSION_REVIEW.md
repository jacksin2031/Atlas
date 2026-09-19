# Sprint 18 dependency, release and regression evidence

Recorded 2026-09-08 on the existing Windows developer workstation. This document is not clean-machine acceptance. Tests use the current worktree, not an immutable released artifact. Frontend and Desktop Rust results are recorded separately by their owners.

## Automated regression

| Command | Result | Evidence |
|---|---|---|
| `cargo test --workspace --locked` | Environment failure: default GNU toolchain cannot find `dlltool.exe`; no test verdict | `evidence/rust-workspace-tests.txt` |
| `cargo +stable-x86_64-pc-windows-msvc test --workspace --locked --target x86_64-pc-windows-msvc` | **348 passed, 0 failed, 0 ignored**; includes successful zero-test doc-test targets | `evidence/rust-workspace-msvc-tests.txt` |
| `python -m pytest tests packages/vision/tests packages/ai/tests packages/knowledge/tests -q --import-mode=importlib` | **717 passed in 96.59 seconds** | `evidence/python-regression-tests.txt` |

Python command uses `PYTHONPATH=src;packages/vision/src;packages/ai/src;packages/knowledge/src` on Windows. These development test imports are not the packaged Runtime discovery strategy. Tests are collected together with importlib mode to avoid same-name test-module collisions. No live provider success is implied by these offline suites.

## Dependency security

Live npm registry audit requests succeeded. The initial snapshot (`evidence/pnpm-audit-before.json`) reported **5 high and 1 moderate** advisories in development/build tooling, listed below. After the narrow lockfile updates on 2026-09-09, `pnpm audit --json` and `pnpm audit --prod --json` both report **0 advisories** (289 total / 48 production dependencies). Final raw snapshots are `evidence/pnpm-audit.json` and `evidence/pnpm-audit-production.json`.

| Package | Severity | Advisory |
|---|---|---|
| postcss | moderate | GHSA-fxqj-rqcc-2cmp |
| nanoid | high | GHSA-28wg-ghj8-5hjv |
| nanoid | high | GHSA-2v37-7h3g-55p8 |
| postcss | high | GHSA-r28c-9q8g-f849 |
| browserslist | high | GHSA-c83g-rgw3-j3cx |
| browserslist | high | GHSA-73wf-gq98-2v4g |

Resolved with `pnpm update postcss nanoid browserslist --lockfile-only --depth Infinity`: postcss 8.5.16 → 8.5.28, nanoid 3.3.15 → 3.3.18, browserslist 4.28.4 → 4.28.9, including the Browserslist data/helper dependencies. A fresh audit then identified GHSA-82fw-gwwq-j7x9 in vitest / @vitest/mocker 4.1.9 (two moderate package findings); `pnpm update vitest --lockfile-only` aligned Vitest packages to 4.1.11 and cleared those findings. Direct dependency ranges and major versions are unchanged; no overrides were needed. `pnpm install --frozen-lockfile` and `pnpm build` passed on the patched graph; build output is `evidence/frontend-build-after-dependency-patch.txt`. The frontend license inventory was regenerated on the same graph. Frontend regression results are recorded separately.

`cargo audit --version` failed because cargo-audit is not installed. Rust advisory scanning is **unverified**, not zero findings. A RustSec scan with a current database is required before clearing that gate. Python production hosts declare no third-party runtime dependencies; the embedded CPython distribution has its own version/hash and license obligations recorded by the bundling script. No claim of a Python advisory scan is made here.

## License inventory

Generated from actual installed/locked metadata:

- `pnpm licenses list --json`: 226 frontend/build package entries, `evidence/frontend-licenses.json`. Machine-local dependency paths removed from the saved inventory; names, versions and license declarations retained.
- `cargo metadata --locked --offline --filter-platform x86_64-pc-windows-msvc --format-version 1`: 82 workspace entries, `evidence/rust-workspace-licenses.json`.
- Same Cargo command with `--manifest-path apps/atlas-desktop/src-tauri/Cargo.toml`: 334 Desktop graph entries, `evidence/rust-desktop-licenses.json`.

Cargo inventories include package name, version, license expression and registry source. This is a dependency-graph inventory, not proof every package is linked into the shipped executable. An initial unfiltered offline query could not load an uncached Android-only dependency; Windows-filtered inventory succeeded.

Desktop metadata has one null license declaration: `display-info 0.4.8`. Its downloaded crate `LICENSE` was inspected and contains **Apache License 2.0**. MPL-2.0 declarations occur in cssparser, cssparser-macros, dtoa-short, option-ext and selectors. Frontend/build declarations include MIT, Apache-2.0, ISC, BSD, BlueOak-1.0.0, 0BSD and CC-BY-4.0. Shipping notices and any applicable source obligations need final distribution review; metadata inventory alone does not complete that work.

## Release workflow

`.github/workflows/release.yml` validates an existing prerelease tag, resolves its commit, checks exact Desktop `package.json`, Tauri JSON and Desktop Cargo version agreement, and checks changelog/roadmap version presence. Every downstream checkout uses the validated immutable commit SHA.

The Windows 2022 job installs Node 22/pnpm 11.9.0, stable Rust with the MSVC target and Python 3.12, installs with `--frozen-lockfile`, runs frontend tests/lint, bundles the pinned interpreter, and builds NSIS with Cargo `--locked`. It saves SHA-256 checksums plus version/commit/target/unsigned metadata and uploads CI artifacts with missing-output failure. It creates no tags or public releases, and uses read-only repository permission.

Workflow YAML parsed successfully (5 jobs); local Tauri CLI help confirms runner arguments after `--` are forwarded to Cargo. GitHub-hosted execution is **not run in this session**. CI compilation is deliberately not described as clean-machine acceptance. Stable Rust is a moving toolchain channel: dependency locks are enforced, but byte-for-byte build reproducibility is not asserted.

