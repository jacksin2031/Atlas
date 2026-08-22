---
id: ATLAS-PLUGINSPEC-CATALOG-SIG
title: Plugin Signature Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Signature Catalog

## 1. Purpose

Documents the signature formats and verification process for plugin packages.

## 2. Signature Formats

| Format       | Algorithm           | Key Size    | Use Case              |
|--------------|---------------------|-------------|-----------------------|
| RSA-PSS      | RSA-PSS-SHA256      | 2048/4096   | Production (default)  |
| ECDSA        | P-256 + SHA-256     | 256-bit     | Lightweight plugins   |
| Ed25519      | EdDSA               | 256-bit     | Modern, fastest       |

## 3. Signature File Format

```
<algorithm>:<base64_encoded_signature>
```

Example:
```
RSA-PSS-SHA256:MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
```

## 4. Verification Process

1. Extract signature.sig from package.
2. Compute SHA-256 hash of all other package files.
3. Verify signature against hash using public key.
4. If verified, trust the package integrity and authenticity.
5. If failed, reject the package with LOAD_002.

## 5. Cross-References

- RFC-0217 Plugin Packaging
- RFC-0207 Plugin Security
