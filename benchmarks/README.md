# benchmarks/

## Purpose

Benchmark suites for measuring performance of Atlas subsystems. Each subdirectory
corresponds to a performance-critical area.

## Ownership

Performance team

## Directory Structure

| Directory  | Measures                          |
| ---------- | --------------------------------- |
| `runtime/` | Runtime boot, lifecycle, service mgmt |
| `ipc/`     | Message latency and throughput    |
| `workflow/`| Pipeline execution speed          |
| `vision/`  | Frame capture and OCR latency     |

## Dependency Rules

- Benchmarks depend on `packages/*` and `crates/*`.
- Benchmark results are tracked over time for regression detection.

## Related RFCs

- RFC-1003 (Performance Standards)

## Future Scope

Automated benchmark reporting, baseline comparison, and CI gating.
