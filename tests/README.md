# tests/

## Purpose

Test suite hierarchy for Atlas. Organized by test type to enforce separation of
concerns and enable targeted test execution.

## Ownership

QA team

## Directory Structure

| Directory       | Purpose                                          |
| --------------- | ------------------------------------------------ |
| `unit/`         | Fast, isolated unit tests for individual modules |
| `integration/`  | Cross-module integration tests                   |
| `contract/`     | API and interface contract tests                 |
| `e2e/`          | End-to-end scenario tests                        |
| `performance/`  | Performance and regression benchmarks            |

## Dependency Rules

- Tests depend on `packages/*` and `apps/*` as appropriate.
- Each test directory mirrors the module it tests.

## Related RFCs

- RFC-1002 (Testing Protocol)

## Future Scope

Flaky test detection, test parallelization, and coverage dashboards.
