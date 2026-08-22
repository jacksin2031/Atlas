# Lessons Learned

> **Purpose**: Record patterns that worked, patterns that failed, and why.
> **Audience**: All agents and human contributors.
> **Rule**: Every sprint ends with a lesson review. Add relevant lessons.

---

## Lesson 0001: Read RFCs Before Implementing

**Problem**: Agent implemented a service without reading the governing RFC.
**Result**: The implementation violated a normative requirement that was only in the RFC.
**Lesson**: Always follow the bootstrap.md sequence. Never skip RFC reading.
**Category**: Specification Compliance
**Date**: 2026-07-02
**Status**: Active

---

## Lesson 0002: Interface-First Prevents Refactoring

**Problem**: Agent implemented concrete service first, then tried to extract an interface.
**Result**: Had to rewrite the entire module to decouple dependencies.
**Lesson**: Define the trait/contract BEFORE writing any implementation.
**Category**: Architecture
**Date**: 2026-07-02
**Status**: Active

---

## Lesson 0003: Test Failure Paths, Not Just Happy Paths

**Problem**: Tests only covered successful execution paths.
**Result**: Edge cases and error paths caused production failures.
**Lesson**: Every service needs failure tests. Test the error paths as thoroughly as happy paths.
**Category**: Testing
**Date**: 2026-07-02
**Status**: Active

---

## Lesson 0004: Parallel Agents Need Disjoint Write Scopes

**Problem**: Two agents wrote to the same file in parallel.
**Result**: Merge conflict, lost changes, wasted time.
**Lesson**: Planner must assign disjoint write scopes. No two agents write the same file.
**Category**: Concurrency
**Date**: 2026-07-02
**Status**: Active

---

## Lesson 0005: No TODOs, Ever

**Problem**: Agent left TODO comments for "later implementation."
**Result**: TODOs accumulated, became dead code, confused reviewers.
**Lesson**: Ship complete code or don't ship at all. TODOs are debt, not planning.
**Category**: Code Quality
**Date**: 2026-07-02
**Status**: Active

---

## How to Add a Lesson

1. Find the next available number.
2. Fill in: Problem, Result, Lesson, Category, Date, Status.
3. Keep it concise — one paragraph each.
4. Link to relevant RFC or ADR if applicable.

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
