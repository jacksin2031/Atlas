# Atlas Sprint 16 Stable Development Baseline

- Date: 2026-09-04
- Baseline commit: `bd384d6`
- Scope: Sprint 16 Knowledge Studio & Runtime Integration plus the AI Studio
  live-acceptance rendering hotfix
- Acceptance: PASS, subject to the external live-provider condition below

## Frozen baseline

The accepted post-Sprint 16 development baseline includes the complete Knowledge
Studio/runtime integration and the AI Studio regression fix that restores the
real Tauri Playground, safely invalidates deleted Knowledge references, and
keeps unavailable references out of inference requests.

Future work must preserve `bd384d6` as an ancestor and must not rewrite the
existing `v0.15.0-alpha` tag. No new release tag is created by this freeze record;
version alignment and release tagging remain a separate release-management step.

## Verified status

- AI Studio UI: PASS
- AI Desktop Bridge: PASS
- Knowledge Studio and Runtime integration: PASS
- Deleted Knowledge reference invalidation: PASS
- Real Tauri render and WebView console verification: PASS
- Desktop Vitest: 151 passed
- AI Runtime: 111 passed
- Knowledge Runtime and boundary: 19 passed
- Tauri Rust: 7 passed
- TypeScript, ESLint, production build, and Tauri check: PASS

## External condition

The real OpenAI provider is unconfigured and disconnected, no model is
available, and AI Runtime health is unavailable. No live prompt was transmitted.

```text
Live Provider Acceptance: PENDING EXTERNAL CONDITION
```

When a real OpenAI credential or a local Ollama model is available, complete the
remaining acceptance path without using Demo Provider:

```text
Discover -> Select model -> Send prompt -> Stream -> Cancel -> Retry -> final response
```

Only a real provider response may promote this status to PASS.

## Next roadmap item

Proceed to Sprint 17 — Marketplace. AI Studio remains feature-frozen except for
defect fixes and the pending live-provider acceptance run.
