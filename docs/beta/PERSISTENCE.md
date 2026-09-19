
## Persistence hardening (Sprint 18)

The project asset envelope remains version 1. No incompatible schema change or fabricated v2 migration was introduced. The deterministic migration entry point currently validates and returns the v1 document unchanged, retaining unknown payload fields. A representative v1 fixture is in `tests/fixtures/project-v1/project-assets.v1.json` (Workflow nodes/plugin references, Vision, AI, Knowledge reference, compatible layout metadata). This is format compatibility evidence, not a historical installer or production UI restart test.

### Implemented

- Project assets refuse unsupported numeric versions on open and save, even when an older valid backup exists. Missing/malformed envelopes are errors rather than silently interpreted as an empty project.
- Writes validate the destination first; synchronise unique create-new temporary files; atomically rename into place on the same volume. The previous validated primary is independently committed as the recovery backup first. A corrupt primary never overwrites a valid recovery backup. Failed replacement leaves the original source intact.
- Project asset and session writers use OS advisory locks (`fs2`), released automatically on process exit. A persistent lock filename is harmless and is not a stale exclusive lock. This serialises writers; application single-instance policy is still needed to avoid stale snapshots from separate live app instances.
- Project asset/session paths reject statically observed symbolic links and Windows reparse points on ancestors. This does not close malicious concurrent path-substitution races; handle-relative/no-follow APIs would be required for that threat model.
- Session pointers use flushed atomic replacement and refuse incompatible existing versions before rewrite.
- Knowledge v1 refuses unsupported versions and different-project sources before recovery or save, rejects non-object entries instead of silently dropping them, uses read-only backup recovery, validates sources before save, and atomically commits flushed recovery backups. Redirected data files and project/.atlas junctions are refused.

### Validation and boundaries

- Knowledge tests: `PYTHONPATH=packages/knowledge/src python -m pytest packages/knowledge/tests -q` — 24 passed, including future-schema refusal with old backup, malformed entries, and injected replacement failure preserving original bytes.
- Rust module tests cover v1 identity preservation, future-version downgrade refusal, corruption recovery, failed commit cleanup, envelope validation, exclusive writer lock and Unicode/space paths. See final validation record for executed result.
- There is no older supported envelope requiring a transformation. The identity path and failure safeguards do not prove any future v1-to-v2 transform; one must add explicit source/destination validation and fixtures before changing schema semantics.
- Frontend layouts remain separately versioned `atlas.layout.<workspace>.v1` localStorage records. Browser parse fallback is not proof of production restart persistence or a migration framework for layouts.
- Plugin metadata/execution recovery are separate existing persistence paths and require their own acceptance results. Knowledge's per-object thread lock is not by itself cross-process read-modify-write isolation; application single-instance enforcement is required.
- File flush + atomic rename protects normal process interruption, but sudden power-loss directory-entry durability has not been proven. Native fault injection, hostile path races, and installer-to-installer upgrade remain unverified.
