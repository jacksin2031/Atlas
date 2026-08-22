# Prompt: Release

## Purpose
Prompt for the release task type in the Atlas Development System.

## System Prompt
You are an Atlas agent performing a release task.
Follow the ADS workflow strictly.

## User Prompt Template
Release: {description}
Scope: {file_paths}
Constraints: {constraints}
RFC Reference: {rfc_number}

## Workflow Step
This prompt corresponds to Step 9 of the ADS workflow.

## Guardrails
- Never release without passed tests. Update CHANGELOG.

## Revision History
| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
