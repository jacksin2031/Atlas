# Atlas Release Procedure

> **Effective**: 2026-09-20  
> **Current candidate line**: 0.18.0-alpha  
> **Rule**: buildability is not release acceptance.

This procedure applies to prerelease promotion after the implementation branch has been reviewed. It does **not** authorize merging, tagging, publishing, signing, or creating a GitHub Release. Those are separate human release decisions.

## 1. Repository gate

Before promotion:

- [ ] The intended commit is reviewed and merged through the normal repository process.
- [ ] Pull Request Check is green for the exact candidate commit.
- [ ] Dependency Security Audit is green for the exact candidate commit.
- [ ] Windows Installed-Product Smoke is green for the exact candidate commit.
- [ ] Frontend lint/tests/build and Tauri backend check pass.
- [ ] Root Rust, combined Python and conformance suites pass.
- [ ] No first-party compilation warnings are accepted silently.
- [ ] Generated dependency notices are reviewed; unresolved required dependencies are zero.
- [ ] Architecture / ADR / RFC / documentation validation pass.
- [ ] Version values agree across Desktop package.json, Tauri config and Desktop Cargo.toml.

A green CI build does not convert hardware-dependent acceptance to PASS.

## 2. Installed-product acceptance gate

For a beta promotion, complete the real-machine protocol in
[docs/beta/SPRINT_18_1_REAL_MACHINE_ACCEPTANCE.md](docs/beta/SPRINT_18_1_REAL_MACHINE_ACCEPTANCE.md).

Required evidence includes, where applicable:

- [ ] clean installed launch independent of development PATH/source execution;
- [ ] five-workspace persistence/recovery;
- [ ] installed Vision → RegionReference → Input → Vision closed loop;
- [ ] Input foreground restriction and global emergency stop;
- [ ] mixed-DPI/multi-monitor behavior;
- [ ] keyboard-only and screen-reader checks;
- [ ] representative 60-minute soak and process/memory evidence;
- [ ] Marketplace interruption/recovery;
- [ ] diagnostics/privacy redaction;
- [ ] uninstall/reinstall and any actually available installer-to-installer upgrade path.

Hardware-unavailable cases remain `NOT FULLY RUN`; historical installers that do not exist remain `UNAVAILABLE HISTORY`. Neither state may be rewritten as PASS.

## 3. Documentation and evidence gate

- [ ] CHANGELOG.md contains the candidate version.
- [ ] ROADMAP.md reflects the actual current milestone.
- [ ] VERSIONING.md agrees with the candidate line.
- [ ] PROJECT_STATUS.md matches the authoritative acceptance report.
- [ ] README.md does not present stale test counts or acceptance status as current.
- [ ] docs/ARCHITECTURE.md describes the current installed-product boundary.
- [ ] Sprint beta-readiness report is updated only from recorded evidence.
- [ ] Installer filename, byte size and SHA-256 are recorded for the exact accepted artifact.
- [ ] External conditions (live provider, production Marketplace, publisher PKI, code signing/SmartScreen) are kept separate from internal engineering evidence.

## 4. Explicit promotion decision

Only after the gates above are reviewed may a release owner explicitly authorize a promotion.

No automation in this repository is allowed to infer that authorization from a successful build, a merged pull request, or the existence of an installer.

For the current Sprint 18.1 review branch:

- do not merge solely because checks are green;
- do not move an existing tag;
- do not create a beta tag;
- do not create or publish a GitHub Release;
- do not represent unsigned artifacts as trusted production distribution.

## 5. Tag and immutable release build

After explicit authorization, create a **new** prerelease tag that points to the reviewed commit. Never move an existing release tag.

The release workflow:

1. accepts an existing prerelease tag;
2. resolves it to an immutable commit SHA;
3. verifies Desktop version agreement and release documentation;
4. runs locked Rust/Python/frontend verification;
5. fetches the complete locked Cargo graph needed for deterministic offline notice inventory;
6. bundles the pinned Python runtime and notices;
7. builds the Windows NSIS installer with Cargo `--locked`;
8. creates SHA-256/build metadata;
9. uploads unsigned CI artifacts.

The workflow itself does not establish real-machine acceptance and does not grant permission to publish.

## 6. Signing and publication

If trusted Windows signing is available, sign only the exact artifact selected for release and record the post-signing checksum separately. Code-signing certificate availability and SmartScreen reputation are external release conditions; do not fabricate them.

When a GitHub Release is explicitly authorized:

- use the immutable accepted tag/commit;
- attach the exact reviewed installer and checksum metadata;
- state signing status accurately;
- include known limitations and external conditions;
- verify the release page and downloadable assets after publication.

## 7. Post-release verification

- [ ] Tag points to the intended immutable commit.
- [ ] Published artifact checksum matches the release record.
- [ ] Version is consistent in UI, metadata and documentation.
- [ ] No release note claims exceed collected evidence.
- [ ] Previous tags/releases were not moved or rewritten.
- [ ] Next milestone/status documents are updated separately after release.

## Version transition rules

| From | To | Minimum condition |
|---|---|---|
| alpha | beta | Internally controllable beta acceptance gates complete under their required scope |
| beta | rc | Feature freeze plus conformance and release-candidate acceptance |
| rc | stable | Stable-release acceptance complete |
| stable | next minor | Backward-compatible feature release |
| stable | next major | Reviewed breaking-change release |

## Governance

Release-process changes require normal project review. Release promotion remains an explicit human decision.
