# Capability Catalog

> Machine-readable capability declarations for Atlas Runtime
> Last Updated: 2026-06-30
> Owner: Runtime Architecture Board

---

## Capability Categories

| Category | Description | Examples |
|---|---|---|
| hardware | Physical device capabilities | GPU, Display, CPU |
| software | Installed software capabilities | OCR, AI models, Vector search |
| network | Network connectivity capabilities | Outbound, Inbound, Streaming |
| filesystem | File system access capabilities | Read, Write |
| system | Runtime system capabilities | Plugin host, WASM, Autoscaling |

---

## Permission Model

| Permission | Description | Default Access |
|---|---|---|
| hardware.gpu | Access to GPU resources | Admin only |
| hardware.display | Access to display/screen | Runtime services |
| software.ocr | OCR engine availability | Runtime services |
| software.ai | AI inference capability | Runtime services |
| software.vector | Vector similarity search | Declared in manifest |
| network.outbound | Outbound network access | Declared in manifest |
| network.inbound | Inbound network access | Denied by default |
| network.distributed | Distributed execution | Declared in manifest |
| network.streaming | Real-time streaming | Declared in manifest |
| filesystem.read | File read access | Declared in manifest |
| filesystem.write | File write access | Declared in manifest |
| process.spawn | Child process creation | Denied by default |
| runtime.plugin | Plugin sandbox host | Runtime core |
| runtime.memory | Memory overcommit support | Runtime core |
| runtime.wasm | WebAssembly runtime | Runtime core |
| runtime.cache | Model caching | Runtime core |
| runtime.hotreload | Plugin hot reload | Runtime core |
| runtime.autoscale | Dynamic scaling | Runtime core |
| security.encryption | Encrypted storage | Runtime core |

---

## Capability Registry

| Capability ID | Name | Category | Required Permission | Default Status | Description |
|---|---|---|---|---|---|
| CAP-001 | GPU | hardware | hardware.gpu | Available | Graphics processing unit for acceleration |
| CAP-002 | OCR | software | software.ocr | Available | Optical character recognition engine |
| CAP-003 | AI_INFERENCE | software | software.ai | Available | Local AI model inference capability |
| CAP-004 | PLUGIN_HOST | system | runtime.plugin | Available | Plugin sandbox execution host |
| CAP-005 | REMOTE_EXECUTION | network | network.distributed | Unavailable | Remote distributed task execution |
| CAP-006 | SCREEN_CAPTURE | hardware | hardware.display | Available | Screen capture pipeline |
| CAP-007 | FILESYSTEM_READ | filesystem | filesystem.read | Available | Read workspace files |
| CAP-008 | FILESYSTEM_WRITE | filesystem | filesystem.write | Available | Write workspace files |
| CAP-009 | NETWORK_INBOUND | network | network.inbound | Unavailable | Accept inbound network connections |
| CAP-010 | PROCESS_SPAWN | system | process.spawn | Unavailable | Spawn child processes |
| CAP-011 | MEMORY_OVERCOMMIT | system | runtime.memory | Available | Memory overcommit support |
| CAP-012 | WASM_RUNTIME | system | runtime.wasm | Available | WebAssembly sandbox runtime |
| CAP-013 | VECTOR_SEARCH | software | software.vector | Unavailable | Vector similarity search index |
| CAP-014 | MODEL_CACHE | system | runtime.cache | Available | AI model caching layer |
| CAP-015 | HOT_RELOAD | system | runtime.hotreload | Available | Plugin hot-reload capability |
| CAP-016 | DISTRIBUTED_SCHEDULING | network | network.distributed | Unavailable | Distributed task scheduling |
| CAP-017 | ENCRYPTED_STORAGE | system | security.encryption | Available | Encrypted state storage |
| CAP-018 | REALTIME_STREAMING | network | network.streaming | Available | Real-time event streaming |
| CAP-019 | MULTI_GPU | hardware | hardware.gpu | Unavailable | Multi-GPU parallel processing |
| CAP-020 | AUTOSCALING | system | runtime.autoscale | Available | Dynamic worker pool scaling |

---

## Capability Lifecycle

| Status | Description | Transition |
|---|---|---|
| Discovered | Capability detected during boot | Probed at startup |
| Available | Capability is ready for use | Passed health check |
| Degraded | Capability partially functional | Resource pressure detected |
| Unavailable | Capability not available | Failed probe or removed |

---

## Capability Query Interface
`\ninterface CapabilityCatalog {\n  CapabilityStatus getCapability(string capabilityId);\n  CapabilityList listAvailable();\n  CapabilityList listAll();\n  Subscription subscribeToChanges(CapabilityEventHandler handler);\n}\n`\n
