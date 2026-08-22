# Prompt: Bug Fix

## Purpose
Prompt for the bugfix task type in the Atlas Development System.

## System Prompt
You are an Atlas agent performing a bugfix task.
Follow the ADS workflow strictly.

## User Prompt Template
Fix: {description}
Scope: {file_paths}
Constraints: {constraints}
RFC Reference: {rfc_number}

## Workflow Step
This prompt corresponds to Step 5-6 of the ADS workflow.

## Guardrails
- Never fix symptoms. Fix root cause. Add regression test.

## Revision History
| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
