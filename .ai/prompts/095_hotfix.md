# Prompt: Hotfix

## Purpose
Prompt for the hotfix task type in the Atlas Development System.

## System Prompt
You are an Atlas agent performing a hotfix task.
Follow the ADS workflow strictly.

## User Prompt Template
Hotfix: {description}
Scope: {file_paths}
Constraints: {constraints}
RFC Reference: {rfc_number}

## Workflow Step
This prompt corresponds to Step 5-6-7-8 of the ADS workflow.

## Guardrails
- Minimal changes only. Document everything. Follow up with proper RFC if needed.

## Revision History
| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
