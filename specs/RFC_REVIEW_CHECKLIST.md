# Atlas RFC Review Checklist

> **Purpose**: Ensure every new or modified RFC meets Atlas specification quality.
> **Related**: [RFC_STYLE_GUIDE.md](RFC_STYLE_GUIDE.md), [RFC_CHANGE_POLICY.md](RFC_CHANGE_POLICY.md), [RFC_VERSIONING_POLICY.md](RFC_VERSIONING_POLICY.md), [RFC_TEMPLATE.md](RFC_TEMPLATE.md)
> **Usage**: Complete this checklist before submitting any RFC for review.
> **Owner**: Atlas Specification Committee
> **Last Updated**: 2026-07-01

---

## Pre-Submission Checklist

### A. Structural Completeness

- [ ] **RFC Header**: All required fields present (RFC#, Title, Status, Category, Owner, Authors, Dates, ADS Version, Spec Version, Normative, Depends On, Supersedes, Superseded By, Related ADR, Related JSON Schema, Related Catalog, Audience, Target Release, Review Cycle, Compatibility, Last Updated)
- [ ] **Normative Status**: Clearly states Normative or Non-Normative
- [ ] **Authority**: Contains Authority section asserting this RFC as the authoritative source
- [ ] **Terminology**: Defines all key terms with exact definitions matching the Atlas Master Glossary
- [ ] **Layer Boundaries**: Contains Responsibilities, Non-Responsibilities, Dependencies, Consumers, Providers, Forbidden Dependencies
- [ ] **Security**: Contains Security section
- [ ] **Performance**: Contains Performance section
- [ ] **Compatibility**: Contains Compatibility section
- [ ] **Compliance**: Contains Compliance section
- [ ] **Future Evolution**: Contains Future Evolution section with 10-year outlook
- [ ] **Runtime Independence**: Contains Runtime Independence section listing all excluded platforms
- [ ] **Acceptance Criteria**: Contains testable acceptance criteria with Verification Method
- [ ] **References**: Contains full References table
- [ ] **Compliance Matrix**: Contains Compliance Matrix table
- [ ] **Revision History**: Contains Revision History table

### B. Language and Style

- [ ] **RFC 2119**: Uses MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, OPTIONAL consistently
- [ ] **No prohibited patterns**: No "should probably", "might want to", "we suggest", "you should"
- [ ] **Active voice**: All sentences use active voice
- [ ] **Present tense**: Requirements use present tense
- [ ] **Third person**: No "you" or "the developer" — use "The implementation"
- [ ] **No tutorials**: No step-by-step implementation guides
- [ ] **No code examples**: No code unless defining a protocol
- [ ] **No implementation advice**: No "use X library" or "consider Y approach"

### C. Cross-References

- [ ] **Workflow Runtime** mention → references RFC-0304
- [ ] **Scheduler** mention → references RFC-0312
- [ ] **Recovery** mention → references RFC-0315
- [ ] **Debugging** mention → references RFC-0316
- [ ] **Validation** mention → references RFC-0317
- [ ] **Versioning** mention → references RFC-0318
- [ ] **Security** mention → references RFC-0319
- [ ] **Performance** mention → references RFC-0320
- [ ] **Observability** mention → references RFC-0321
- [ ] **Extension** mention → references RFC-0322
- [ ] **Plugin Integration** mention → references RFC-0323
- [ ] **Storage** mention → references RFC-0324
- [ ] **AI** mention → references RFC-0325
- [ ] **Vision** mention → references RFC-0326
- [ ] **IPC** mention → references RFC-0327
- [ ] **Serialization** mention → references RFC-0328
- [ ] **Compatibility** mention → references RFC-0329
- [ ] **Compliance** mention → references RFC-0330
- [ ] **Testing** mention → references RFC-0331
- [ ] **Migration** mention → references RFC-0332
- [ ] **SDK** mention → references RFC-0333
- [ ] **No self-references** in Related RFCs header

### D. Diagrams

- [ ] **Consistent naming**: All node names match across diagrams
- [ ] **Unique IDs**: No duplicate node IDs within diagrams
- [ ] **No orphan diagrams**: Every diagram has corresponding text description
- [ ] **Correct syntax**: All Mermaid diagrams render correctly
- [ ] **Appropriate type**: Diagram type matches content (graph, sequence, state, class)

### E. Catalog Alignment

- [ ] **All concepts cataloged**: Every concept introduced exists in catalog/
- [ ] **No undocumented concepts**: No RFC introduces concepts absent from catalog
- [ ] **Catalog references**: Related Catalog field lists all relevant catalog entries
- [ ] **RFC alignment**: Catalog alignment table in the overview RFC is up to date

### F. Acceptance Criteria Quality

- [ ] **Testable**: Every criterion can be verified by a test or analysis
- [ ] **Specific**: Uses "The implementation MUST" not "should" or "could"
- [ ] **Measurable**: Has quantifiable thresholds where applicable
- [ ] **Grouped**: Criteria grouped by domain category
- [ ] **Unique numbering**: AC-01, AC-02, etc. — no gaps or duplicates

### G. ADS Compliance

- [ ] **Constitution reference**: References Atlas AI Constitution
- [ ] **ADR references**: References ADR-0012 (and ADR-0010 if security-related)
- [ ] **No contradictions**: Does not contradict any higher-level RFC
- [ ] **Layer compliance**: Respects layer boundaries defined in the relevant overview RFC
- [ ] **Change Policy Compliance**: Modification follows proposal, review, and approval process
- [ ] **Versioning Compliance**: Version increments follow semver rules

### H. Future-Proofing

- [ ] **Cloud-ready**: Design accommodates cloud deployment
- [ ] **Cluster-ready**: Design accommodates cluster deployment
- [ ] **Distributed-ready**: Design accommodates distributed runtime
- [ ] **Remote-ready**: Design accommodates remote execution
- [ ] **Headless-ready**: Design accommodates headless operation
- [ ] **AI Agent-ready**: Design accommodates AI agent nodes
- [ ] **Multi-engine-ready**: Design accommodates multiple engine implementations

---

## Reviewer Notes

- If any item is marked [NOT APPLICABLE], document why in the reviewer notes.
- Items marked [FAIL] MUST be resolved before the RFC can be accepted.
- Items marked [WARN] SHOULD be resolved but MAY be deferred with committee approval.
- This checklist is a living document. Updates follow the RFC process.
