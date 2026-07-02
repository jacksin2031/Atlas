# Runtime Event Catalog

> **Purpose**: Fixed, named events for the Atlas Runtime.  
> **Last Updated**: 2026-06-30  
> **Owner**: Runtime Architecture Board  

---

## Event Catalog

All events use the Common Event Model (RFC-1001).

### Lifecycle Events

| Event ID | Event Name | Category | Priority | Source State | Destination State |
|---|---|---|---|---|---|
| EVENT-0001 | Runtime.Created | lifecycle | 1 | — | Created |
| EVENT-0002 | Runtime.BootStarted | lifecycle | 1 | Created | Initializing |
| EVENT-0003 | Runtime.ServiceRegistered | lifecycle | 2 | Initializing | Initializing |
| EVENT-0004 | Runtime.HealthCheckPassed | lifecycle | 2 | Initializing | Initializing |
| EVENT-0005 | Runtime.Ready | lifecycle | 1 | Initializing | Ready |
| EVENT-0006 | Runtime.Starting | lifecycle | 1 | Ready | Ready |
| EVENT-0007 | Runtime.Running | lifecycle | 1 | Ready | Running |
| EVENT-0008 | Runtime.PauseRequested | lifecycle | 1 | Running | Paused |
| EVENT-0009 | Runtime.Paused | lifecycle | 2 | Running | Paused |
| EVENT-0010 | Runtime.ResumeRequested | lifecycle | 1 | Paused | Paused |
| EVENT-0011 | Runtime.Resumed | lifecycle | 1 | Paused | Running |
| EVENT-0012 | Runtime.ShutdownRequested | lifecycle | 1 | Any | ShuttingDown |
| EVENT-0013 | Runtime.Draining | lifecycle | 2 | ShuttingDown | ShuttingDown |
| EVENT-0014 | Runtime.Terminating | lifecycle | 2 | ShuttingDown | ShuttingDown |
| EVENT-0015 | Runtime.Terminated | lifecycle | 1 | ShuttingDown | Terminated |
| EVENT-0016 | Runtime.Failed | lifecycle | 1 | Any | Failed |
| EVENT-0017 | Runtime.RestartRequested | lifecycle | 1 | Running | ShuttingDown |

### Plugin Events

| Event ID | Event Name | Category | Priority | Description |
|---|---|---|---|---|
| EVENT-0101 | Plugin.Discovered | plugin | 2 | Plugin manifest found |
| EVENT-0102 | Plugin.Loaded | plugin | 2 | Plugin binary loaded into sandbox |
| EVENT-0103 | Plugin.Initialized | plugin | 2 | Plugin initialize() succeeded |
| EVENT-0104 | Plugin.Active | plugin | 1 | Plugin is fully active |
| EVENT-0105 | Plugin.Suspended | plugin | 2 | Plugin paused |
| EVENT-0106 | Plugin.Unloaded | plugin | 2 | Plugin cleanup complete |
| EVENT-0107 | Plugin.CrashDetected | plugin | 1 | Plugin sandbox crashed |
| EVENT-0108 | Plugin.Recovered | plugin | 2 | Plugin recovered from crash |
| EVENT-0109 | Plugin.PermanentlyDisabled | plugin | 1 | Plugin exceeded max retries |

### State Events

| Event ID | Event Name | Category | Priority | Description |
|---|---|---|---|---|
| EVENT-0201 | State.TransactionBegin | state | 2 | Transaction started |
| EVENT-0202 | State.TransactionCommit | state | 2 | Transaction committed |
| EVENT-0203 | State.TransactionRollback | state | 2 | Transaction rolled back |
| EVENT-0204 | State.SnapshotTaken | state | 3 | Snapshot created |
| EVENT-0205 | State.WALFlushed | state | 3 | WAL flushed to disk |

### Resource Events

| Event ID | Event Name | Category | Priority | Description |
|---|---|---|---|---|
| EVENT-0301 | Resource.Allocated | resource | 2 | Resource allocated |
| EVENT-0302 | Resource.Released | resource | 2 | Resource released |
| EVENT-0303 | Resource.Throttled | resource | 2 | Resource throttled |
| EVENT-0304 | Resource.EmergencyCleanup | resource | 1 | Emergency cleanup triggered |

### Health Events

| Event ID | Event Name | Category | Priority | Description |
|---|---|---|---|---|
| EVENT-0401 | Health.HeartbeatMissed | system | 2 | Service heartbeat missed |
| EVENT-0402 | Health.HealthCheckFailed | system | 2 | Service health check failed |
| EVENT-0403 | Health.RecoveryAttempted | system | 2 | Recovery initiated |
| EVENT-0404 | Health.RecoverySuccess | system | 2 | Recovery succeeded |
| EVENT-0405 | Health.RecoveryFailed | system | 1 | Recovery failed |

---

## Event Naming Convention

Format: {Category}.{Action}

| Category | Prefix |
|---|---|
| Lifecycle | Runtime.* |
| Plugin | Plugin.* |
| State | State.* |
| Resource | Resource.* |
| Health | Health.* |
| System | System.* |
