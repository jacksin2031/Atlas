# Atlas Release Procedure

> **Effective**: 2026-07-04
> **Owner**: Atlas Release Manager

---

## Release Checklist

Complete these steps in order after each Sprint.

### 1. Verify Implementation

- [ ] All source files committed
- [ ] Tests pass (cargo test for Rust, pytest for Python)
- [ ] Zero compilation warnings
- [ ] Zero TODOs in source code
- [ ] No circular dependencies
- [ ] All imports are absolute
- [ ] No global mutable state
- [ ] Dependency injection throughout

### 2. Update Documentation

- [ ] CHANGELOG.md — Add new version section (Added, Changed, Security, Performance, Documentation)
- [ ] ROADMAP.md — Mark completed Sprint, update upcoming Sprints
- [ ] VERSIONING.md — Ensure Sprint-to-version mapping is current
- [ ] PROJECT_STATUS.md — Update status dashboard, metrics, RFC status
- [ ] README.md — Update status, version, modules, tests, architecture
- [ ] docs/ARCHITECTURE.md — Add new Runtime section
- [ ] docs/README.md — Update documentation links
- [ ] specs/RFC_INDEX.md — Update RFC statuses
- [ ] Compliance reports — Update for new modules
- [ ] .ai/release.md — Update AI skill

### 3. Create Version Files

- [ ] VERSIONING.md — Ensure Sprint-to-version mapping is current
- [ ] RELEASE.md — This file

### 4. Create AI Release Skill

- [ ] .ai/release.md — Updated with latest procedures

### 5. Git Tag

- [ ] git tag -a vX.X.X-alpha -m "Atlas vX.X.X-alpha\nSprint N — Module Name"
- [ ] git push origin vX.X.X-alpha
- [ ] Verify tag points to correct commit

### 6. GitHub Release

- [ ] gh release create vX.X.X-alpha --target main --title "Atlas vX.X.X-alpha" --notes RELEASE_NOTES
- [ ] Include: Runtime Foundation, new modules, quality gates, documentation updated
- [ ] Verify release page renders correctly

### 7. GitHub Milestone

- [ ] Create milestone for next Sprint
- [ ] Link all related issues/PRs
- [ ] Set due date

### 8. RFC Index

- [ ] Update specs/RFC_INDEX.md with new implementation statuses
- [ ] Verify dependency graph is accurate
- [ ] Update specification statistics

### 9. Compliance Reports

- [ ] Generate/update compliance report for new module
- [ ] Verify RFC traceability matrix
- [ ] Update coverage summary
- [ ] Document known limitations

### 10. Post-Release Verification

- [ ] All documentation is consistent
- [ ] Version numbers match across all files
- [ ] Sprint numbers are sequential and correct
- [ ] No placeholders or TODOs remain
- [ ] No contradictory status between files
- [ ] GitHub Release page is complete

---

## Release Notes Template

`markdown
# Atlas vX.Y.Z-alpha
## Sprint N — Module Name

### Runtime Foundation
- Core runtime infrastructure established
- Service registry, event bus, scheduler

### [New Module]
- Feature 1
- Feature 2

### Security
- [Security improvements]

### Performance
- [Performance improvements]

### Documentation
- [Docs added/updated]

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
`

---

## Version Transition Rules

| From | To | Condition |
|---|---|---|
| alpha | beta | All Runtime modules complete, architecture frozen |
| beta | rc | Conformance tests pass, feature freeze |
| rc | stable | All acceptance criteria pass |
| stable | next minor | New feature Sprint |
| stable | next major | Breaking changes |

---

## Governance

Changes to this procedure require Architecture Board approval.
