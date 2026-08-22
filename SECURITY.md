# Security Policy

> **Last Updated**: 2026-07-05
> **Owner**: Atlas Security Team

---

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.10.0-alpha | :white_check_mark: Current |
| < 0.10.0 | :x: Unsupported |

---

## Reporting a Vulnerability

We take the security of Atlas seriously. If you believe you've found a security vulnerability, please report it to us as described below.

### Process

1. **DO NOT** open a public GitHub issue
2. Email security vulnerabilities to: **security@AtlasAutomationStudio.github.io**
3. Include a detailed description of the vulnerability
4. Include steps to reproduce the vulnerability if possible
5. Include potential impact and affected components
6. Allow 72 hours for initial response

### What to Include

- Vulnerability description
- Affected components/runtimes
- Reproduction steps
- Potential impact assessment
- Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 72 hours
- **Initial Assessment**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 7 days
  - High: 14 days
  - Medium: 30 days
  - Low: Next sprint

---

## Disclosure Policy

We follow a coordinated disclosure process:

1. Reporter submits vulnerability details
2. Security team validates and assesses severity
3. Fix is developed and tested
4. Reporter is credited (unless anonymous)
5. Public disclosure after fix is released

---

## Security Measures

### Runtime Security

- **Plugin Sandbox**: Isolated plugin execution environment
- **Permission Model**: Granular access control (10+ permission levels)
- **Capability Negotiation**: Runtime capability verification
- **Event Validation**: Immutable, versioned event schema

### Infrastructure Security

- **Branch Protection**: Required status checks and reviews
- **CODEOWNERS**: Mandatory review from domain experts
- **CI Validation**: Architecture, RFC, and conformance checks
- **Dependency Updates**: Dependabot for automated security patches

---

## Best Practices for Contributors

1. **Never** commit secrets, keys, or credentials
2. **Use** environment variables for sensitive configuration
3. **Follow** the security policy in each runtime
4. **Run** security checks before submitting PRs
5. **Report** suspicious activity immediately

---

## Contact

- **Email**: security@AtlasAutomationStudio.github.io
- **GitHub**: [@AtlasAutomationStudio](https://github.com/AtlasAutomationStudio)
- **Issues**: Use security issue template (private)

---

*This policy is reviewed quarterly by the Atlas Architecture Board.*
