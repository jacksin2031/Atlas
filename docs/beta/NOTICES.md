# Beta dependency notices

Generated with `python scripts/bundle_notices.py`, using local installed packages and `cargo metadata --locked --offline --filter-platform x86_64-pc-windows-msvc`.

- Frontend: 48 unique name/version packages from production dependencies and their installed dependency/peer closure.
- Rust: 333 packages in the reachable Windows resolved graph; includes build dependencies and may over-include crates not shipped as executable code.
- Original notice/license files copied: 626.
- Generated bundle: `apps/atlas-desktop/src-tauri/resources/notices/inventory.json` plus original license texts. The inventory preserves package name, version, declared license, source/repository, original filename and SHA-256.
- CPython and its embedded dependency notices: `resources/runtime/LICENSE.txt`; Atlas: `resources/runtime/ATLAS-LICENSE.txt`.

This is a metadata and text collection, not a legal compatibility assessment. Only top-level LICENSE/UNLICENSE/COPYING/NOTICE/COPYRIGHT/AUTHORS files, license directories and Cargo's declared license_file are collected; notices embedded solely in source files or other documentation may require separate review. Frontend development-only packages are excluded unless reachable as production peers. The collected installed npm graph is not proof of which modules Vite emits. Generated resources are ignored by Git and must be regenerated before packaging.

## Missing metadata or texts (18)

- `cargo:alloc-stdlib@0.2.4`: No collected original license/notice text.
- `cargo:atlas-common@0.15.0-alpha`: No collected original license/notice text.
- `cargo:atlas-contracts@0.15.0-alpha`: No collected original license/notice text.
- `cargo:atlas-plugin@0.15.0-alpha`: No collected original license/notice text.
- `cargo:defmt-parser@1.0.0`: No collected original license/notice text.
- `cargo:display-info@0.4.8`: Unknown declared license.
- `cargo:fxhash@0.2.1`: No collected original license/notice text.
- `cargo:pulp-wasm-simd-flag@0.1.1`: No collected original license/notice text.
- `cargo:selectors@0.36.1`: No collected original license/notice text.
- `cargo:unic-char-property@0.9.0`: No collected original license/notice text.
- `cargo:unic-char-range@0.9.0`: No collected original license/notice text.
- `cargo:unic-common@0.9.0`: No collected original license/notice text.
- `cargo:unic-ucd-ident@0.9.0`: No collected original license/notice text.
- `cargo:unic-ucd-version@0.9.0`: No collected original license/notice text.
- `cargo:webview2-com@0.38.2`: No collected original license/notice text.
- `cargo:webview2-com-macros@0.8.1`: No collected original license/notice text.
- `cargo:webview2-com-sys@0.38.2`: No collected original license/notice text.
- `cargo:zune-inflate@0.2.54`: No collected original license/notice text.

## Unresolved frontend dependencies (2)

- `zustand@5.0.14` → `immer` (optional: True).
- `zustand@4.5.7` → `immer` (optional: True).
