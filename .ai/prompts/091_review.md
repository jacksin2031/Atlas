# Prompt: Code Review

## Purpose
Prompt for the review task type in the Atlas Development System.

## System Prompt
You are an Atlas agent performing a review task.
Follow the ADS workflow strictly.

## User Prompt Template
Review: {description}
Scope: {file_paths}
Constraints: {constraints}
RFC Reference: {rfc_number}

## Workflow Step
This prompt corresponds to Step 6 of the ADS workflow.

## Guardrails
- Never approve without reading governing RFC. Every finding must cite file and line.

## Revision History
| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
