# Plugin Trust Levels Catalog

## 1. Purpose

This catalog defines the canonical set of trust levels that classify plugins according to the degree of verification, auditing, and security hardening they have undergone. The trust level determines which sandbox boundaries, permission scopes, and runtime restrictions apply to a plugin instance.

## 2. Stable ID Prefix

All trust level identifiers use the prefix `TRUST-LEVEL-`. This prefix is reserved exclusively for plugin trust classification definitions within the Atlas ecosystem.

## 3. Naming Convention

Trust level identifiers MUST conform to the pattern `TRUST-LEVEL-<CLASSIFICATION>` where `<CLASSIFICATION>` describes the verification depth and organizational authority behind the classification. Classifications MUST use uppercase ASCII letters and hyphens.

## 4. Canonical Trust Level Table

| Stable ID | Name | Verification Depth | Sandbox Scope | Permission Grant |
|---|---|---|---|---|
| `TRUST-LEVEL-UNVERIFIED` | Unverified | No cryptographic verification; the plugin binary is accepted as-is from an untrusted source. | Full sandbox restrictions; all privileged operations are denied. | Minimal; only read-only access to public plugin data is permitted. |
| `TRUST-LEVEL-SIG-VALIDATED` | Signature Validated | The plugin binary is signed with a recognized certificate authority chain; signature verification passes. | Standard sandbox; network access to approved endpoints is permitted. | Extended; access to plugin-scoped data and standard APIs is permitted. |
| `TRUST-LEVEL-SIGNATURE-ROOTED` | Signature Rooted | The plugin signing certificate is rooted in the organization's trusted certificate store; certificate revocation status is checked. | Reduced sandbox; access to internal service endpoints is permitted. | Broad; access to organizational data stores and internal APIs is permitted. |
| `TRUST-LEVEL-AUDITED` | Audited | The plugin source code has been reviewed by a qualified security auditor; audit findings are recorded and all critical findings are resolved. | Minimal sandbox; the plugin MAY operate partially outside the sandbox under monitored conditions. | Elevated; access to sensitive data stores and administrative APIs is permitted under audit logging. |
| `TRUST-LEVEL-ENTERPRISE-APPROVED` | Enterprise Approved | The plugin has received formal approval from the organization's plugin governance board; compliance with organizational security policies is verified. | No sandbox; the plugin operates with full runtime privileges subject to runtime monitoring. | Full; access to all organizational resources and APIs is permitted, subject to RBAC. |
| `TRUST-LEVEL-HARDENED` | Hardened | The plugin has undergone adversarial testing, fuzzing, and penetration testing; known vulnerability databases are checked; the plugin supply chain is verified. | No sandbox with continuous integrity monitoring; any deviation from the verified binary triggers immediate suspension. | Full with integrity guarantees; access to all organizational resources with real-time anomaly detection. |
| `TRUST-LEVEL-CERTIFIED` | Certified | The plugin has achieved third-party certification against a recognized security standard; certification is periodically renewed; the plugin complies with regulatory requirements. | No sandbox with continuous compliance monitoring; compliance violations trigger automated remediation. | Full with regulatory guarantees; access to all organizational resources including regulated data stores. |

## 5. Trust Level Progression Rules

1. A plugin MAY be assigned any trust level at initial installation; the default assignment MUST be `TRUST-LEVEL-UNVERIFIED`.
2. Trust level upgrades MUST follow a monotonic progression; a plugin MUST NOT skip an intermediate trust level without explicit justification recorded in the registry metadata.
3. A plugin that has been demoted from `TRUST-LEVEL-ENTERPRISE-APPROVED` or higher MUST revert to `TRUST-LEVEL-UNVERIFIED` if the demotion reason involves a confirmed security vulnerability.
4. Trust level evaluations MUST be re-run whenever a plugin binary is updated; the new trust level MUST NOT exceed the previous level unless the evaluation explicitly confirms the upgrade.
5. The `PIF-SECURITY-GATE` MUST enforce sandbox and permission boundaries corresponding to the plugin's current trust level at all times.

## 6. Trust Level Evaluation Criteria

Each trust level MUST be evaluated against the following criteria as applicable:

1. Cryptographic signature verification: Applies to `TRUST-LEVEL-SIG-VALIDATED` and above.
2. Certificate chain validation: Applies to `TRUST-LEVEL-SIGNATURE-ROOTED` and above.
3. Source code audit: Applies to `TRUST-LEVEL-AUDITED` and above.
4. Governance board approval: Applies to `TRUST-LEVEL-ENTERPRISE-APPROVED` and above.
5. Adversarial testing: Applies to `TRUST-LEVEL-HARDENED` and above.
6. Third-party certification: Applies to `TRUST-LEVEL-CERTIFIED`.
7. Regulatory compliance verification: Applies to `TRUST-LEVEL-CERTIFIED`.

## 7. Cross-References

- RFC 2119: Key words for use in RFCs to Indicate Requirement Levels.
- Atlas Plugin Security Gate Specification: Defines how `PIF-SECURITY-GATE` enforces trust level policies.
- Atlas Plugin Sandbox Specification: Defines the sandbox configurations mapped to each trust level.
- NIST SP 800-161: Cybersecurity Supply Chain Risk Management Practices for Information Systems and Organizations.

## 8. Usage Guidelines

Plugin publishers SHOULD submit their plugins for the highest trust level achievable given their distribution channel and organizational policies. Runtime operators MUST NOT manually override a trust level without recording the override reason in the registry metadata. Audit trails MUST capture every trust level assignment, upgrade, downgrade, and revocation event. Organizations SHOULD define a trust level policy document that maps business requirements to minimum trust level thresholds for different plugin categories.
