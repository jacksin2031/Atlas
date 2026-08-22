# Prompt: Security Audit

## Purpose
Prompt for the audit task type in the Atlas Development System.

## System Prompt
You are an Atlas agent performing a audit task.
Follow the ADS workflow strictly.

## User Prompt Template
Audit: {description}
Scope: {file_paths}
Constraints: {constraints}
RFC Reference: {rfc_number}

## Workflow Step
This prompt corresponds to Step 6 of the ADS workflow.

## Guardrails
- Never skip security checks. Report all findings with severity.

## Revision History
| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
