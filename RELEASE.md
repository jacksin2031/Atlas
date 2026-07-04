# Atlas Release Procedure

> **Effective**: 2026-07-04
> **Owner**: Atlas Release Manager

---

## Release Checklist

Complete these steps in order after each Sprint.

### 1. Verify Implementation

- [ ] All source files committed
- [ ] Tests pass (`cargo test` for Rust, `pytest` for Python)
- [ ] Zero compilation warnings
- [ ] Zero TODOs in source code
- [ ] No circular dependencies
- [ ] All imports are absolute

### 2. Update Documentation

- [ ] `CHANGELOG.md` — Add new version section
- [ ] `ROADMAP.md` — Mark completed Sprint
- [ ] `specs/RFC_INDEX.md` — Update RFC statuses
- [ ] `README.md` — Update status, version, modules, tests
- [ ] `docs/ARCHITECTURE.md` — Add new Runtime section
- [ ] Compliance reports — Update for new modules
- [ ] `PROJECT_STATUS.md` — Update status dashboard

### 3. Create Version Files

- [ ] `VERSIONING.md` — Ensure Sprint-to-version mapping is current
- [ ] `RELEASE.md` — This file

### 4. Create AI Release Skill

- [ ] `.ai/release.md` — Updated with latest procedures

### 5. Tag and Release

- [ ] `git tag -a vX.X.X-alpha -m "Atlas vX.X.X-alpha\nSprint N — Module Name"`
- [ ] `git push origin vX.X.X-alpha`
- [ ] `gh release create vX.X.X-alpha --target main --title "Atlas vX.X.X-alpha" --notes RELEASE_NOTES`

### 6. Post-Release Verification

- [ ] GitHub Release page renders correctly
- [ ] Tag points to correct commit
- [ ] All documentation is consistent
- [ ] Version numbers match across all files

---

## Release Notes Template

```markdown
# Atlas vX.Y.Z-alpha
## Sprint N — Module Name

### Runtime Foundation
- Core runtime infrastructure established
- Service registry, event bus, scheduler

### [New Module]
- Feature 1
- Feature 2

### Quality Gate
- **X/Y tests passing**
- **Zero warnings**
- **Zero errors**

### Documentation Updated
- CHANGELOG.md
- ROADMAP.md
- RFC_INDEX.md
- README.md
- ARCHITECTURE.md
- Compliance reports
```

---

## Version Transition Rules

| From | To | Condition |
|---|---|---|
| alpha | beta | All Runtime modules complete |
| beta | rc | Conformance tests pass |
| rc | stable | All acceptance criteria pass |
| stable | next minor | New feature Sprint |
| stable | next major | Breaking changes |

---

## Governance

Changes to this procedure require Architecture Board approval.
