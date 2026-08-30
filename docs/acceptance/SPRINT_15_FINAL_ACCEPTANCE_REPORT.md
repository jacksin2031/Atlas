# Atlas Sprint 15.6 Final Acceptance Closure

**Frozen release:** `v0.15.0-alpha`

This report supersedes the earlier Sprint 15 `PARTIAL` baseline. It records the blocker-closure work and the real Windows/Tauri evidence collected on 2026-08-30 (Asia/Hong_Kong). A registered command, rendered control, or mock-only test is not counted as a real desktop E2E.

## Verdict

The Atlas-owned Sprint 15 graduation contracts are complete. The Desktop AI bridge is connected through Tauri to the persistent Python host; project and interrupted-execution recovery are safe; missing visual targets cannot click; Template, native Windows OCR, the kill switch, and dynamic plugin execution all pass.

A healthy external AI provider/model was not available in the acceptance environment. Live token streaming and the final multimodal provider response are therefore `PENDING EXTERNAL CONDITION`, as explicitly allowed by the Sprint 15.6 graduation rules. This does not hide an Atlas bridge failure: provider discovery, Connect routing, health testing, and Vision-context attachment were exercised in the real Tauri application.

## Graduation matrix

| Contract | Result | Observed evidence |
| --- | --- | --- |
| AI Desktop Bridge | PASS | Real Tauri AI Studio discovered OpenAI through the Python host. `Connect` no longer returned `unavailable`; provider health testing returned the explicit `unhealthy` result. |
| AI Runtime Integration | PASS | `ai_discover`, `ai_infer`, `ai_cancel`, and `ai_provider_action` are routed through the Desktop/Tauri/Python boundary; host and frontend regression suites pass. |
| Live Provider | PENDING EXTERNAL CONDITION | OpenAI was discoverable, but the endpoint was unhealthy and exposed no selectable model. No Ollama listener was available. |
| Multimodal provider response | PENDING EXTERNAL CONDITION | A real Windows frame was captured and attached to AI Context as one Vision item. Provider submission could not proceed without a healthy model. |
| Project Restart | PASS | The `.acceptance/sprint15-final` project, workspace, workflow, and execution snapshot restored after terminating and restarting the real Tauri process. |
| Interrupted Recovery | PASS | Active run `execution-0662e1d0-8be3-40b8-aaf2-e7e08117bda3` restored as `interrupted`. |
| Unarmed after restart | PASS | The restored UI displayed `Arm Input`, not `Input Armed`. |
| No automatic replay | PASS | After waiting following restart, the status and active execution ID remained unchanged; no new run was created. |
| Manual Restart | PASS | After explicit re-arming, `Restart` created `execution-ef331106-abc8-45f4-887a-49a08b47674f`, which completed all five nodes. The interrupted run remained in history. |
| Target Relocation | PASS | The unchanged visual workflow completed against the target in two different positions (`execution-9dd93d70-f39c-4612-ba70-d54f294a1894` and `execution-914982a5-8c6d-4f6d-aa5e-9960a50aad00`). |
| Target Missing → No Click | PASS | With the target removed, `execution-b4a770a4-3be0-4711-9736-4c3da7187313` failed at Detection; Mouse Click, recapture, validation, and exit were `skipped`. The target remained absent. |
| Template | PASS | Real Tauri Template closed loop completed as `execution-fe2b7821-4bf8-4b04-adf8-5c0d4872b3df`. |
| OCR | PASS | Native Windows OCR workflow completed as `execution-3c8eb3e2-0046-4d24-ad2a-fc38925a832d` and emitted the expected OCR target label. |
| Global Kill Switch | PASS | During a real armed Input workflow, Emergency Stop changed the run to `Stopped`, persisted `cancelled`, and returned the UI to `Arm Input`. The provider-triggered emergency callback also has an integration regression proving active workflow cancellation and input release. |
| Dynamic Plugin | PASS | The runtime registered a data-driven plugin node in the real desktop, executed it, and persisted output `dynamic:Atlas` in `execution-c012db1f-398f-4d76-b89a-4d1a273fa84e`. Unsafe plugin operations are rejected. |

## Recovery safety trace

The required recovery scenario was executed against a real Input workflow:

```text
Input Armed
→ start Sprint 15.6 Interrupted Input Recovery
→ status Running
→ terminate atlas-desktop.exe
→ restart Tauri application
→ project and workflow restored
→ execution-0662… = interrupted
→ Arm Input (unarmed)
→ wait: no replay and no new execution ID
→ explicit re-arm
→ manual Restart
→ execution-ef331… = completed
```

The project asset retains both executions. The original run remains `interrupted`; the manually restarted run is a distinct completed execution. No input action was automatically replayed after process restart.

## Visual safety trace

The missing-target negative case is fail-closed:

```text
Vision Current Frame  completed
Detection             failed: no target
Mouse Click           skipped
Vision Current Frame  skipped
Vision Validate       skipped
Exit                  skipped
```

The integration regression additionally records zero `MouseClickRequest` deliveries when no typed target reference is produced.

## AI boundary result

The material Sprint 15.1 regression is closed. Provider actions now distinguish three outcomes:

- bridge unavailable: command invocation returns no result;
- provider action rejected/health failed: command returns `false`;
- bridge accepted the action: command returns `true`.

In the real desktop, provider discovery returned OpenAI, Connect traversed the Desktop bridge without an `unavailable` error, and Test reported the endpoint as unhealthy. The environment therefore blocks only the external live-provider steps, not Atlas integration.

Vision Capture and multimodal context preparation were also exercised after restart. The AI project asset persisted one `kind: vision` context item and contained no credential-shaped field. The existing stale “no current frame” notification did not prevent the later successful attachment and is not an execution-boundary failure.

## Security and persistence

- Credentials remain in the Windows credential vault boundary; no API key was printed, placed in Zustand, written to the project asset, or exposed in request evidence.
- Project asset scanning found no `api_key`, `authorization`, or `bearer` field.
- Emergency stop cancels running/paused/scheduled workflows and releases provider-held input.
- Restart never restores Input Runtime authorization.
- Active execution snapshots are persisted as recoverable `interrupted` state, never as an instruction to auto-run.
- The project asset uses primary/backup recovery and retains execution history across restart.

## Regression evidence

Final complete suite:

| Suite | Passing |
| --- | ---: |
| Root Python | 310 |
| AI Python | 110 |
| Vision Python | 185 |
| Desktop Vitest | 135 |
| Root Rust workspace | 329 |
| Tauri Rust | 5 |
| **Total** | **1,074** |

Additional checks:

- TypeScript `tsc --noEmit`: PASS
- ESLint with zero warnings: PASS
- Production build: PASS, 379 modules transformed
- Root and Tauri `cargo fmt --check`: PASS
- Rust tests used the installed `stable-x86_64-pc-windows-msvc` toolchain and Visual Studio developer environment. The machine-wide default GNU toolchain lacks `dlltool`; that local default-toolchain issue is not an Atlas test failure.

## Final acceptance

All Atlas-owned safety contracts are PASS. The only pending items require a healthy external model endpoint:

```text
Live Provider                PENDING EXTERNAL CONDITION
Live streaming/cancel/retry  PENDING EXTERNAL CONDITION
Multimodal provider response PENDING EXTERNAL CONDITION
```

SPRINT 15 FINAL ACCEPTANCE: PASS
