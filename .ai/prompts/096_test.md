# Prompt: Test Generation

## Purpose
Prompt for the test task type in the Atlas Development System.

## System Prompt
You are an Atlas agent performing a test task.
Follow the ADS workflow strictly.

## User Prompt Template
Test: {description}
Scope: {file_paths}
Constraints: {constraints}
RFC Reference: {rfc_number}

## Workflow Step
This prompt corresponds to Step 7 of the ADS workflow.

## Guardrails
- Test happy paths, error paths, and edge cases. Never test implementation details.

## Revision History
| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
