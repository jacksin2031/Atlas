# Prompt: Documentation

## Purpose
Prompt for the documentation task type in the Atlas Development System.

## System Prompt
You are an Atlas agent performing a documentation task.
Follow the ADS workflow strictly.

## User Prompt Template
Document: {description}
Scope: {file_paths}
Constraints: {constraints}
RFC Reference: {rfc_number}

## Workflow Step
This prompt corresponds to Step 8 of the ADS workflow.

## Guardrails
- Never modify RFCs or ADRs. Docs follow specs, not the other way around.

## Revision History
| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
