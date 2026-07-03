

## IPC Runtime

The Atlas IPC Runtime (packages/ipc) provides the complete inter-process communication layer. See [IPC_COMPLIANCE_REPORT.md](IPC_COMPLIANCE_REPORT.md) for full RFC traceability.

### Quick Start

cargo check -p atlas-ipc    # Verify compilation
cargo test -p atlas-ipc     # Run 84 tests
# Atlas Workflow Runtime

The Atlas Workflow Runtime transforms declarative workflow definitions into executable runtime graphs.
The architecture is platform-independent. The current reference implementation is written in Python 3.10+.

## Quick Start

See docs/ARCHITECTURE.md for full details.
## Documentation

| Document | Purpose |
|----------|---------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Module structure and design principles |
| [COMPLIANCE_REPORT.md](COMPLIANCE_REPORT.md) | RFC-by-RFC requirement traceability |
| [IMPLEMENTATION_STRATEGY.md](IMPLEMENTATION_STRATEGY.md) | Reference vs. Production distinction and contribution guide |


