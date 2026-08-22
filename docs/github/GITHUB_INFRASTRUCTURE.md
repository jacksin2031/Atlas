# Atlas GitHub Infrastructure

> **Last Updated**: 2026-07-05
> **Owner**: Atlas Architecture Board

---

## Repository Structure

`
.github/
├── CODEOWNERS              # PR review assignment rules
├── ISSUE_TEMPLATE/         # Issue templates for bug reports, features, RFCs
│   ├── bug_report.yml
│   ├── feature_request.yml
│   ├── documentation.yml
│   └── rfc.yml
├── PULL_REQUEST_TEMPLATE/  # PR checklist template
│   └── .gitkeep
└── workflows/              # GitHub Actions CI/CD pipelines
    ├── ci.yml              # Main continuous integration
    ├── pull_request.yml    # PR validation checks
    ├── release.yml         # Release automation
    ├── docs.yml            # Documentation validation
    └── benchmark.yml       # Performance benchmarks
`

---

## Project Management

### GitHub Project V2

**Name**: Atlas Development  
**Description**: Development board for Atlas Architecture, Runtime, Studio, Marketplace and Release planning.

**Views**:
- **Board**: Kanban-style with columns (Backlog, Ready, In Progress, Review, Done, Released)
- **Table**: Spreadsheet-style for bulk editing
- **Roadmap**: Timeline view for sprint planning

### Labels

30 labels organized by category:

**Runtimes**: architecture, runtime, workflow, vision, ai, knowledge, ipc, plugin, storage, project, integration  
**Documentation**: documentation, rfc, adr  
**Testing**: testing, performance  
**Security**: security  
**UI/UX**: ui, marketplace  
**Release**: release  
**Issue Types**: bug, enhancement, refactor, research  
**Priority**: good first issue, help wanted, high priority, medium priority, low priority

### Milestones

| Milestone | Description |
|-----------|-------------|
| Sprint 12 | Performance & Stress testing |
| Sprint 13 | Desktop Shell implementation |
| Sprint 14 | Workflow Studio |
| Sprint 15 | Vision Studio |
| Sprint 16 | AI Studio |
| Sprint 17 | Marketplace |
| Sprint 18 | Beta release preparation |
| Future | Post-1.0 features and roadmap |

---

## CI/CD

### Workflow Overview

`
Push to main
    ↓
┌─────────────────────────────────┐
│  CI Pipeline (ci.yml)           │
│  ├─ Rust build & test           │
│  ├─ Python unit tests           │
│  ├─ Python integration tests    │
│  ├─ Python e2e tests            │
│  ├─ Conformance validation      │
│  ├─ Architecture validation     │
│  ├─ RFC validation              │
│  ├─ Documentation validation    │
│  └─ Conformance report          │
└─────────────────────────────────┘

Pull Request
    ↓
┌─────────────────────────────────┐
│  PR Check (pull_request.yml)    │
│  ├─ Architecture validation     │
│  ├─ RFC compliance              │
│  ├─ ADR validation              │
│  ├─ Documentation check         │
│  ├─ TODO/placeholder scan       │
│  ├─ Full test suite             │
│  └─ Conformance suite           │
└─────────────────────────────────┘

Tag Pushed (vX.Y.Z-alpha)
    ↓
┌─────────────────────────────────┐
│  Release (release.yml)          │
│  ├─ Validate tag format         │
│  ├─ Verify version in docs      │
│  ├─ Rust release build          │
│  ├─ Python release tests        │
│  └─ Generate release notes      │
└─────────────────────────────────┘

Docs Changed
    ↓
┌─────────────────────────────────┐
│  Docs (docs.yml)                │
│  ├─ Broken link check           │
│  ├─ Documentation consistency   │
│  ├─ Compliance report validation│
│  └─ README format check         │
└─────────────────────────────────┘

Weekly Schedule
    ↓
┌─────────────────────────────────┐
│  Benchmark (benchmark.yml)      │
│  ├─ Rust startup benchmark      │
│  ├─ Python startup/shutdown     │
│  ├─ Memory usage                │
│  ├─ Plugin load time            │
│  ├─ Workflow execution          │
│  ├─ Vision pipeline             │
│  └─ AI runtime                  │
└─────────────────────────────────┘
`

### Workflow Triggers

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| ci.yml | Push to main, manual | Full CI pipeline |
| pull_request.yml | PR opened/synchronized | PR validation |
| elease.yml | Release published, manual | Release automation |
| docs.yml | Docs changed, manual | Documentation validation |
| enchmark.yml | Weekly schedule, manual | Performance tracking |

---

## Release Workflow

`
Sprint Complete
    ↓
Create Git Tag (git tag -a vX.Y.Z-alpha)
    ↓
Push Tag to GitHub (git push origin vX.Y.Z-alpha)
    ↓
Create GitHub Release (gh release create)
    ↓
Update CHANGELOG.md
    ↓
Update ROADMAP.md
    ↓
Update PROJECT_STATUS.md
    ↓
Update Compliance Reports
    ↓
Announcement (future)
`

### Versioning Policy

- **Alpha** (0.x.x-alpha): Active development, architecture may change
- **Beta** (0.x.x-beta): Architecture frozen, feature-complete
- **RC** (0.x.x-rc.N): Conformance tests must pass, feature freeze
- **Stable** (x.y.z): Public API stable, production-ready

See [VERSIONING.md](VERSIONING.md) for details.

---

## Branch Strategy

`
main ────────────────────────────────────────►
  │
  ├─ sprint/12 ──► Performance & Stress
  ├─ sprint/13 ──► Desktop Shell
  ├─ sprint/14 ──► Workflow Studio
  └─ ...
`

### Branch Naming Rules

| Pattern | Purpose |
|---------|---------|
| main | Stable development branch |
| sprint/N | Sprint feature branches |
| elease/vX.Y.Z | Release preparation branches |
| hotfix/description | Emergency fixes |

### Branch Protection (Recommended)

Go to: **Settings → Branches → Branch protection rules**

**Rule for main**:
- ✓ Require pull request reviews
- ✓ Require status checks to pass
- ✓ Require conversation resolution before merging
- ✗ Exclude administrators
- ✗ Require signed commits (optional)
- ✗ Allow force pushes
- ✗ Allow deletions
- ✓ Require linear history
- ✓ Include administrators
- Restrict who can push: match contributors

---

## Contribution Workflow

### For Contributors

1. **Fork** the repository
2. **Create** a feature branch: git checkout -b sprint/12/my-feature
3. **Make** changes and **test** locally
4. **Push** to your fork: git push origin sprint/12/my-feature
5. **Open** a Pull Request against main
6. **Address** review comments
7. **Merge** when all checks pass

### PR Checklist

All PRs must include:
- [ ] RFC updated (if architecture change)
- [ ] Tests added
- [ ] Documentation updated
- [ ] Compliance report updated
- [ ] Architecture unchanged (or documented)
- [ ] Conformance passes
- [ ] CI passes

### Issue Templates

| Template | Use Case |
|----------|----------|
| ug_report.yml | Report a bug |
| eature_request.yml | Suggest a new feature |
| documentation.yml | Suggest documentation changes |
| fc.yml | Propose a new RFC |

---

## GitHub Discussions

### Recommended Categories

| Category | Purpose |
|----------|---------|
| General | General questions and announcements |
| Architecture | Design discussions and decisions |
| RFC | RFC proposals and reviews |
| ADR | Architecture Decision Record discussions |
| Ideas | Brainstorming and feature ideas |
| Q&A | Help and support |
| Showcase | Share projects built with Atlas |
| Announcements | Official project updates |

Enable via: **Settings → Features → Discussions**

---

## Automation Scripts

### bootstrap_github.py

**Location**: scripts/bootstrap_github.py  
**Purpose**: Idempotent GitHub infrastructure configuration  
**Requirements**: Python 3.10+, GitHub CLI (gh) authenticated

**Usage**:
`ash
# Preview changes
python scripts/bootstrap_github.py --dry-run

# Apply changes
python scripts/bootstrap_github.py

# Custom org/repo
python scripts/bootstrap_github.py --org MyOrg --repo MyRepo
`

**Creates/Verifies**:
- Labels (30 total, idempotent)
- Milestones (8 total, idempotent)
- Project V2 (idempotent)
- Workflows (verification only)
- Templates (verification only)
- CODEOWNERS (verification only)

---

## Security

### Security Policy

See [SECURITY.md](SECURITY.md) for:
- Supported versions
- Vulnerability reporting process
- Disclosure policy

### Dependabot (Recommended)

Enable via: **Settings → Security → Actions → Dependabot**

- ✓ Enable alerts
- ✓ Enable auto-merge for minor versions

---

## Funding

Future: FUNDING.yml for GitHub Sponsors, Patreon, or Open Collective.

---

*For architecture details, see [ARCHITECTURE.md](docs/ARCHITECTURE.md).*
*For design principles, see [DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md).*
*For the roadmap, see [ROADMAP.md](ROADMAP.md).*
