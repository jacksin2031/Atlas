# Runtime Error Catalog

> Machine-readable error codes for Atlas Runtime  
> Last Updated: 2026-06-30  
> Owner: Runtime Architecture Board  

---

## Severity Levels

| Severity | Meaning | Action |
|---|---|---|
| **Recoverable** | Error can be resolved automatically | Retry, fallback, or self-heal |
| **Warning** | Error does not block execution but indicates degradation | Log, monitor, alert |
| **Fatal** | Error blocks further execution of the component | Rollback, halt, or restart |
| **Critical** | Error threatens system stability or security | Immediate containment, kill process |

---

## Error Code Registry

| Error Code | Category | Severity | Description | Subsystem | Recovery Action |
|---|---|---|---|---|---|
| RT-1001 | Runtime | Fatal | Runtime process failed unexpectedly | Core Runtime | Rollback to last snapshot, terminate |
| RT-1002 | Plugin | Recoverable | Plugin execution exceeded timeout | Plugin Host | Retry with exponential backoff |
| RT-1003 | Workflow | Fatal | Workflow node definition is invalid | Workflow Engine | Halt workflow, notify operator |
| RT-1004 | Vision | Recoverable | Screen capture driver failed | Vision Engine | Cycle capture driver, fallback to alternate |
| RT-1005 | IPC | Recoverable | IPC connection lost between processes | IPC Dispatcher | Re-establish connection, retry |
| RT-1006 | State | Fatal | State data corruption detected | State Manager | Revert to last valid snapshot |
| RT-1007 | Resource | Fatal | System memory exhaustion | Resource Manager | Throttle and retry, emergency cleanup |
| RT-1008 | Manifest | Fatal | Invalid manifest schema | Manifest Parser | Abort boot sequence |
| RT-1009 | Capability | Warning | Required capability unavailable | Capability Registry | Use configured fallback |
| RT-1010 | Hook | Recoverable | Hook execution exceeded timeout | Hook System | Abort hook, log warning |
| RT-1011 | Service | Recoverable | Service process crashed | Service Registry | Restart service adapter |
| RT-1012 | Scheduler | Fatal | Task scheduling deadlock detected | Scheduler | Abort and restart scheduler |
| RT-1013 | Event | Warning | Event queue overflow | Event Bus | Drop lowest-priority events |
| RT-1014 | State | Fatal | Write-Ahead Log full | State Manager | Emergency cleanup, halt writes |
| RT-1015 | Plugin | Fatal | Plugin signature verification failed | Plugin Host | Reject and quarantine plugin |
| RT-1016 | Version | Fatal | Protocol version mismatch | Version Negotiator | Reject connection |
| RT-1017 | Resource | Warning | Memory leak detected in subsystem | Resource Manager | Kill process, restart with limits |
| RT-1018 | Scheduler | Fatal | Thread starvation detected | Scheduler | Emergency dispatch, rebalance |
| RT-1019 | State | Recoverable | Snapshot commit failed | State Manager | Retry commit |
| RT-1020 | Health | Recoverable | Health check timeout | Health Monitor | Probe service directly |
| RT-1021 | Security | Fatal | Permission denied for operation | Security Manager | Log and reject request |
| RT-1022 | Contract | Fatal | Schema validation failed for IPC message | Contract Verifier | Reject message, log error |
| RT-1023 | Event | Warning | Dead Letter Queue full | Event Bus | Drop oldest events |
| RT-1024 | Plugin | Critical | Plugin sandbox escape attempt detected | Plugin Host | Kill sandbox immediately, isolate |
| RT-1025 | Security | Fatal | Cryptographic signature expired | Security Manager | Require re-authentication |
| RT-1026 | Config | Warning | Configuration drift detected | Config Manager | Sync configuration |
| RT-1027 | Service | Fatal | Circular dependency detected | Service Registry | Abort boot sequence |
| RT-1028 | Scheduler | Recoverable | Worker pool exhausted | Scheduler | Scale up workers |
| RT-1029 | Vision | Warning | Frame buffer overflow | Vision Engine | Drop oldest frames |
| RT-1030 | AI | Recoverable | AI model load timeout | AI Engine | Fallback to alternative provider |
| RT-1031 | Runtime | Fatal | Boot sequence exceeded timeout | Core Runtime | Halt, log diagnostics |
| RT-1032 | IPC | Fatal | Maximum message size exceeded | IPC Dispatcher | Drop message, log |
| RT-1033 | Plugin | Recoverable | Plugin unload timeout | Plugin Host | Force terminate plugin |
| RT-1034 | Resource | Warning | Disk I/O latency exceeded threshold | Resource Manager | Throttle I/O operations |
| RT-1035 | State | Recoverable | Snapshot restoration partial failure | State Manager | Retry from previous snapshot |
| RT-1036 | Event | Fatal | Event bus routing loop detected | Event Bus | Break loop, isolate affected channels |
| RT-1037 | Scheduler | Recoverable | Task retry limit exceeded | Scheduler | Mark task failed, escalate |
| RT-1038 | Capability | Fatal | Mandatory capability unavailable at boot | Capability Registry | Halt boot sequence |
| RT-1039 | Security | Critical | Unauthorized IPC message from unknown origin | Security Manager | Drop message, alert operator |
| RT-1040 | Runtime | Fatal | Watchdog detected unresponsive service | Health Monitor | Initiate service recovery |
