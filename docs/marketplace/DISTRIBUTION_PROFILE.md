# Atlas local distribution profile v1

This profile implements the local development scope permitted by Sprint 17 using the existing PluginManifest, PluginManager, PluginProvider/PluginFactory, semantic version, dependency, capability, lifecycle and health contracts. It specializes the ZIP/signature requirements of RFC-0213, RFC-0216 and RFC-0217. It does not claim the production certificate authority, revocation or public registry infrastructure described by those RFCs.

## Package and trust

An `.atlas-plugin` is a ZIP containing canonical `manifest.json`, `checksum.sha256`, `signature.sig` and the manifest's `bin/` entrypoint. Archives are read into bounded memory and never extracted. ZIP paths must be relative, unique under case folding, and free of traversal, backslashes, drive syntax, control characters, reserved devices and link entries. Packages and total expanded content are capped at 8 MiB, archives at 128 entries, and programs at 32 nodes.

`checksum.sha256` is the UTF-8 concatenation of `lowercase_sha256`, two spaces, the path, and LF for every content file except checksum/signature files, ordered lexicographically by path. The Ed25519 signature covers SHA-256 of all entries except `signature.sig`, sorted by path. Each entry is framed as big-endian u64 UTF-8 path length, path bytes, big-endian u64 content length, content bytes. `signature.sig` is `Ed25519:` followed by base64 of the 64-byte signature. A registry listing also pins the SHA-256 of the whole ZIP.

Desktop embeds the development public key so losing the registry directory cannot replace trust or prevent installed-package recovery. The reproducible fixture signing seed is intentionally public. UI trust text explicitly says Development; no production certification badge is issued.

## Execution boundary

`atlas.safe-workflow.v1` is the constrained provider's entrypoint format, not another manifest schema. It declares platform/architecture support and owner-prefixed node types with one input and one output. Its operations are echo, constant, prefix, uppercase, lowercase and controlled failure/permission-denial probes. Unsupported executable formats and operations are rejected before installation. Node output is produced by a concrete Rust Plugin instance managed by PluginManager, never by React or a package-specific host branch.

No native libraries, Python modules, JavaScript, shell commands or arbitrary binary code are loaded. Isolation comes from an interpreter with no privileged host API, bounded package content and a finite operation set; it is not an OS process sandbox. Permission review records the exact canonical permission objects for the inspected bytes. Approval does not expose files, network, credentials, Input, AI, Knowledge or Vision. Privileged operations remain denied even with declared grants. Input arm and emergency-stop state remain owned by the existing Input Runtime.

## Transactions and recovery

User-scoped package storage resides at Tauri app-data `plugins/v1`, shared across projects. PackageStore is a backend filesystem adapter using immutable digest-named ZIPs, an exclusive process lock, atomic staging writes and one atomically replaced `installed.json` commit record. The existing generic StorageProvider does not expose durable rename/locking primitives, so it is not used to simulate these guarantees.

Install/update validates bytes and exact permission review, resolves dependencies, stages a blob, starts the existing Plugin Runtime to check activation, synchronizes owned Workflow registrations, and commits installed state. New installs finish disabled; updates preserve enabled state. Failures restore the old package/runtime and send a newer registration revision to undo any partial host synchronization. A process interruption before the commit recovers the old record; after commit it recovers the new one. A host that cannot acknowledge rollback produces an explicit recovery error and must restart. Uninstall commits absence before deleting the blob.

Startup revalidates each committed package and manifest, restores enabled packages in dependency order, and reports corrupt/unavailable packages without registering their nodes. Only UUID staging files and unreferenced digest-named package files in the dedicated store are cleaned; unrelated files are preserved. Cleanup is best effort and retries at startup. Files referenced by the commit record are never treated as orphans.

Required dependencies must already be installed, version-compatible and enabled for activation. There is no silent dependency download or permission grant. Updates must be newer by canonical semantic ordering and preserve contributed node types; schema migration and arbitrary downgrade are unsupported. Package identity/version cannot be reassigned to different bytes. Multiple package owners remain separate during registration and removal.

## Desktop integration and limits

Marketplace uses WorkspaceManager, FlexLayout, the panel registry, design-system controls, central commands and workspace persistence. Zustand holds presentation state, not installation authority. Tauri exposes discovery/review/lifecycle requests; package execution is available only through the existing Workflow host bridge. Python receives owner metadata and routes invocation back to Rust. Missing nodes remain serialized and visible; validation rejects execution safely.

Acquisition is a bounded local file read, so cancellation occurs by cancelling the picker or declining review before mutation. There is no remote download queue. Provider failures affect discovery; committed installations remain manageable. The lifecycle mutex serializes execution and mutation. Structured errors carry codes, and the latest 100 audit entries retain request correlation and provenance. Existing PluginManager lifecycle/event/health components continue to operate.

Production registry service, private publisher keys, certificate/revocation policy, remote authentication, native-code isolation, privileged capability brokers, dependency acquisition and node schema migration are outside this local profile. They require separate implementation and acceptance before being advertised.
