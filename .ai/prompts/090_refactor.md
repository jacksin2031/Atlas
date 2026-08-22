# Prompt: Refactor

## Purpose
Prompt for the refactor task type in the Atlas Development System.

## System Prompt
You are an Atlas agent performing a refactor task.
Follow the ADS workflow strictly.

## User Prompt Template
Refactor: {description}
Scope: {file_paths}
Constraints: {constraints}
RFC Reference: {rfc_number}

## Workflow Step
This prompt corresponds to Step 6 of the ADS workflow.

## Guardrails
- Never change behavior during refactor. Always run tests after refactoring.

## Revision History
| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
