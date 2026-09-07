# Local Development Registry

This is a real, repository-owned development package source for Atlas Marketplace acceptance. It is not a production marketplace or a publisher certification service.

Rebuild its signed ZIP packages from the repository root:

```powershell
cargo +stable-x86_64-pc-windows-msvc run -p atlas-plugin --example build_acceptance_registry -- marketplace/local-development
```

The example uses the deliberately public development signing seed `[17; 32]`. Anyone can reproduce this key: a matching signature establishes consistency with this development profile, not publisher identity, safety, or production trust. Desktop pins the corresponding public key at build time. Never reuse this key for production.

| Package | Purpose |
| --- | --- |
| Echo 1.0.0 | Returns the incoming typed value |
| Echo 1.1.0 | Returns `ATLAS_MARKETPLACE_1710` to distinguish updated execution |
| Echo 1.2.0 | Requests an additional outbound-network permission, requiring a new exact review |
| failure 1.0.0 | Returns a controlled execution error |
| denied 1.0.0 | Attempts an undeclared privileged operation; backend denies it |
| unhealthy 1.0.0 | Fails runtime activation; installation rolls back |

Installations are initially disabled. Enable Echo and import `sample-workflow-marketplace.json` in Workflow to execute it through Tauri, Python Workflow Runtime, PluginBridge and the Rust PluginManager. The package supplies the operation; the workflow stores only its type, owner, ports and graph configuration.

The implementation profile, signature framing, limits and isolation boundary are documented in [DISTRIBUTION_PROFILE.md](../../docs/marketplace/DISTRIBUTION_PROFILE.md).
