---
id: ATLAS-PLUGINSPEC-CATALOG-PKG_LAYOUT
title: Plugin Package Layout Catalog
version: \"1.0.0\"
status: active
language: independent
---

# Plugin Package Layout Catalog

## 1. Purpose

This catalog documents the standard directory layout for an tlas-plugin package archive.

## 2. Standard Package Tree

`
my-plugin.atlas-plugin/
├── manifest.json              [REQUIRED] Plugin manifest
├── signature.sig              [REQUIRED] Digital signature (RSA/ECDSA)
├── checksum.sha256            [REQUIRED] SHA-256 integrity hash
├── schema/                    [OPTIONAL] JSON Schema for plugin config
│   └── config-v1.json
├── resources/                 [OPTIONAL] Bundled resources
│   ├── icons/                 [RECOMMENDED] Icon files
│   │   ├── icon-16.png
│   │   ├── icon-32.png
│   │   ├── icon-64.png
│   │   └── icon.svg
│   ├── translations/          [RECOMMENDED] i18n files
│   │   ├── en.json
│   │   ├── ja.json
│   │   └── zh-TW.json
│   └── fonts/                 [OPTIONAL] Embedded font files
│       └── custom-font.woff2
├── assets/                    [OPTIONAL] Bundled assets
│   ├── models/                [OPTIONAL] AI/ML model files
│   │   └── classifier.onnx
│   ├── ocr/                   [OPTIONAL] OCR data packs
│   │   └── lang-pack-jpn/
│   └── templates/             [OPTIONAL] Workflow/code templates
│       └── boilerplate.ts
├── bin/                       [REQUIRED] Compiled code / scripts
│   ├── main.js                [REQUIRED] Entry point
│   └── utils.js
├── tests/                     [OPTIONAL] Plugin test suite
│   ├── manifest.test.js
│   └── api.test.js
└── license.txt                [REQUIRED if license is not SPDX]
`

## 3. Directory Specifications

| Directory   | Required | Contents                              | Validation Rules                           |
|-------------|----------|---------------------------------------|--------------------------------------------|
| Root        | Yes      | manifest.json, signature.sig, checksum.sha256 | Manifest MUST be valid, sig MUST verify |
| schema/     | No       | JSON Schema files                     | Files MUST be valid JSON Schema Draft 2020-12 |
| resources/icons/ | No  | PNG (16/32/64px), SVG                | Files MUST be valid image formats          |
| resources/translations/ | No | i18n JSON files with locale codes | Files MUST match ^[a-z]{2}(-[A-Z]{2})?.json$ |
| resources/fonts/ | No   | WOFF2, TTF, OTF files               | Files MUST be valid font formats           |
| assets/models/ | No    | ONNX, PB, SAFETENSORS files         | Hash MUST match checksum in manifest       |
| assets/ocr/ | No       | OCR language pack directories        | Each subdir MUST contain config.json       |
| assets/templates/ | No  | Template files (.ejs, .hbs, .txt)    | Files MUST be valid template syntax        |
| bin/        | Yes      | Entry point and dependencies         | Entry point MUST be executable             |
| tests/      | No       | Test files                            | Tests MUST pass when run via tlas-plugin test |
| Root license.txt | Yes  | Full license text (if not SPDX)      | MUST match declared license field          |

## 4. Archive Format

- File extension: .atlas-plugin
- Internal format: ZIP archive (MUST be extractable with standard ZIP tools)
- Encoding: UTF-8 for all text files
- Maximum size: 500 MB per package (excluding downloadable assets)

## 5. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- RFC-0217 Plugin Packaging
- RFC-0202 Plugin Manifest
