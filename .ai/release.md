# Atlas Release Documentation Update

> **Trigger**: "Perform Atlas Release Documentation Update"
> **Purpose**: Incrementally update all release documentation after a Sprint

---

## Instructions

When invoked, read these files IN ORDER:

1. `README.md` — Current project overview
2. `CHANGELOG.md` — Existing changelog (preserve all history)
3. `ROADMAP.md` — Current roadmap state
4. `VERSIONING.md` — Version policy
5. `RELEASE.md` — Release procedure
6. `PROJECT_STATUS.md` — Status dashboard
7. `specs/RFC_INDEX.md` — RFC registry
8. `docs/ARCHITECTURE.md` — Architecture docs
9. `docs/*_COMPLIANCE_REPORT.md` — Compliance reports
10. All Runtime RFCs in `specs/*/`

---

## Verification Steps

Before making changes, verify:

- [ ] `git log --oneline <prev_tag>..HEAD` shows Sprint commits
- [ ] Count source files per package (`find packages/ -name "*.rs" | wc -l`)
- [ ] Count test annotations per package (`grep -r "#\[test\]" packages/`)
- [ ] Count Python tests (`grep -r "def test_" packages/`)
- [ ] Check for compilation warnings (`cargo check 2>&1 | grep warning`)
- [ ] Verify no TODOs in source code
- [ ] Verify no circular dependencies

---

## Update Rules

### CHANGELOG.md
- Append new version section (never remove previous)
- Use Keep a Changelog format
- Sections: Added, Changed, Deprecated, Removed, Fixed, Security
- Date in ISO-8601 format

### ROADMAP.md
- Mark completed Sprint with ✅
- Add upcoming Sprint with ⬜
- Update Current Version and Next Milestone
- Never remove previous milestones

### VERSIONING.md
- Ensure Sprint-to-version mapping is current
- Verify pre-identifier rules match current state

### PROJECT_STATUS.md
- Update all tables with current data
- Update Quality Metrics
- Update RFC Status counts
- Update Architecture diagram
- Update Next Milestone section

### specs/RFC_INDEX.md
- Update implementation status for newly implemented RFCs
- Never remove RFCs
- Only change status (Draft → Approved → Implemented → Verified)

### README.md
- Update Current Project Status
- Update Implemented Modules list
- Update Latest Sprint and Version
- Update Current Test Count
- Update Quick Start if needed

### docs/ARCHITECTURE.md
- Add new Runtime module section
- Update Module Diagram
- Update Completed Runtime Components
- Update Current Runtime Stack

### Compliance Reports
- Update Architecture Summary
- Update Requirement Matrix
- Update RFC Mapping
- Update Coverage Summary
- Update Known Limitations
- Update Release Summary

---

## Quality Gates

Before finishing, verify:

- [ ] CHANGELOG updated
- [ ] ROADMAP updated
- [ ] RFC_INDEX updated
- [ ] README updated
- [ ] Architecture documentation updated
- [ ] Compliance reports updated
- [ ] Version numbers consistent across all files
- [ ] Sprint numbers consistent across all files
- [ ] No placeholders (TODO, FIXME, etc.)
- [ ] No contradictory status
- [ ] All dates in ISO-8601 format

---

## Output

- Produce only modified files
- Do not rewrite unchanged files
- Preserve formatting and Markdown style
- Ensure every document remains internally consistent
- Treat as incremental release documentation task, not rewrite
