---
id: ATLAS-PLUGINSPEC-CATALOG-MANDEX
title: Plugin Manifest Examples Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Manifest Examples Catalog

## 1. Purpose

Canonical manifest examples for common plugin types.

## 2. Minimal Manifest (Utility Plugin)

```json
{
  "$schema": "https://atlas.dev/schemas/plugin/v1",
  "name": "hello-world",
  "version": "1.0.0",
  "title": "Hello World",
  "description": "A minimal utility plugin",
  "author": { "name": "Dev" },
  "license": "MIT",
  "capabilities": ["PT-UTILITY"],
  "permissions": [{ "level": "low", "resources": ["workspace:read"] }]
}
```

## 3. Full Manifest (AI Plugin)

```json
{
  "$schema": "https://atlas.dev/schemas/plugin/v1",
  "name": "ai-vision-processor",
  "version": "2.1.0",
  "title": "AI Vision Processor",
  "description": "Provides AI-powered vision and OCR capabilities",
  "author": { "name": "Atlas Team", "email": "team@atlas.dev" },
  "license": "Apache-2.0",
  "homepage": "https://atlas.dev/plugins/ai-vision",
  "capabilities": ["PT-AI", "PT-VISION"],
  "permissions": [
    { "level": "elevated", "resources": ["ai:model", "vision:ocr"] }
  ],
  "dependencies": [
    { "name": "core-runtime", "version_range": ">=2.0.0 <3.0.0", "type": "hard" }
  ],
  "config_schema": { "type": "object", "properties": { "model_path": { "type": "string" } } },
  "hot_reload": { "eligible": false },
  "feature_gates": [{ "name": "ai-model-v3", "required": true }]
}
```

## 4. Cross-References

- RFC-0202 Plugin Manifest
- catalog/plugin-manifest-schema.md
