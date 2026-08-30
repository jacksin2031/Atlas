# Atlas Sprint 15 Freeze

- Version: `0.15.0-alpha`
- Git tag: `v0.15.0-alpha`
- Date: 2026-08-30
- Acceptance: PASS

## Frozen baseline

```text
Sprint 15
└── Final Acceptance PASS
    ├── 1,074 tests
    ├── Core Automation Loop verified
    ├── Safety verified
    ├── Recovery verified
    ├── Security verified
    ├── Plugin integration verified
    └── AI bridge verified
```

The tag identifies the source, tests, sample workflows, and release documentation accepted as the Sprint 15 baseline. Future Sprint work must not rewrite this tag.

## Verified contracts

- Desktop → Tauri → persistent Python AI Runtime bridge
- `ai_discover`, `ai_infer`, `ai_cancel`, and `ai_provider_action`
- Vision → typed target reference → Input → recapture → validation loop
- Target relocation and missing-target/no-click behavior
- Template matching and native Windows OCR
- Input arming, focus policy, rate bounds, release, and emergency stop
- Project restart, interrupted execution, unarmed recovery, no replay, and manual restart
- Windows credential-vault boundary and credential-free project persistence
- Restricted dynamic plugin registration and execution

## External conditions

The frozen Atlas integration is complete. A healthy external provider/model was not available during acceptance, so these remain explicitly non-blocking:

- Live provider response: `PENDING EXTERNAL CONDITION`
- Live streaming/cancel/retry: `PENDING EXTERNAL CONDITION`
- Multimodal provider response: `PENDING EXTERNAL CONDITION`

Vision capture and attachment to AI Context passed before the provider boundary.

## Verification record

| Suite | Passing |
| --- | ---: |
| Root Python | 310 |
| AI Python | 110 |
| Vision Python | 185 |
| Desktop Vitest | 135 |
| Root Rust workspace | 329 |
| Tauri Rust | 5 |
| **Total** | **1,074** |

The detailed real-desktop evidence and execution IDs are recorded in [SPRINT_15_FINAL_ACCEPTANCE_REPORT.md](SPRINT_15_FINAL_ACCEPTANCE_REPORT.md).
