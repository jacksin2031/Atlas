---
id: ATLAS-PLUGINSPEC-CATALOG-MESSAGES
title: Plugin IPC Messages Catalog
version: \"1.0.0\"
status: active
language: independent
---

# Plugin IPC Messages Catalog

## 1. Purpose

This catalog documents all IPC message types used for inter-plugin communication through the Atlas runtime IPC layer.

## 2. Message Format

All IPC messages use JSON-RPC 2.0 format:

`json
{
  \"jsonrpc\": \"2.0\",
  \"id\": \"unique-request-id\",
  \"method\": \"string\",
  \"params\": { ... },
  \"result\": { ... },
  \"error\": { \"code\": number, \"message\": \"string\", \"data\": { ... } }
}
`

## 3. Request Types

| Method                    | Params Schema                        | Response Schema                  | Description                       |
|---------------------------|--------------------------------------|----------------------------------|-----------------------------------|
| ping                    | {}                                 | { pong: true, timestamp: number } | Health check                   |
| discover                | { query: string, limit: number }   | { results: PluginInfo[] }      | Discover plugins by query         |
| egister                | { service: ServiceDef }            | { registered: true, id: string } | Register a service             |
| consume                 | { service_id: string }             | { instance: ServiceInstance }  | Consume a registered service      |
| invoke                  | { target: string, method: string, params: object } | { result: any } | Invoke a plugin method          |
| subscribe               | { channel: string, filter?: object } | { subscription_id: string } | Subscribe to event channel      |
| unsubscribe             | { subscription_id: string }        | { unsubscribed: true }         | Unsubscribe from channel          |
| stream_open             | { target: string, type: string }   | { stream_id: string }          | Open a bidirectional stream       |
| stream_send             | { stream_id: string, data: any }   | { sent: true }                 | Send data on a stream             |
| stream_close            | { stream_id: string }              | { closed: true }               | Close a stream                    |

## 4. Response Types

| Type      | Success Schema                         | Error Schema                                    |
|-----------|----------------------------------------|-------------------------------------------------|
| Success   | { jsonrpc: \"2.0\", id: string, result: any } | —                                           |
| Error     | —                                      | { jsonrpc: \"2.0\", id: string, error: { code: number, message: string, data: object } } |

## 5. Error Codes

| Code | Name                     | Description                                |
|------|--------------------------|--------------------------------------------|
| -32700 | Parse error            | Invalid JSON-RPC format                    |
| -32600 | Invalid Request        | Request cannot be processed                |
| -32601 | Method Not Found       | Target method does not exist               |
| -32602 | Invalid Params         | Parameters do not match schema             |
| -32603 | Internal Error         | Runtime-internal error                     |
| -32001 | Plugin Not Found       | Target plugin is not loaded                |
| -32002 | Plugin Unavailable     | Target plugin is loading/stopping          |
| -32003 | Permission Denied      | Caller lacks required permissions          |
| -32004 | Rate Limited           | Too many requests from caller              |
| -32005 | Timeout                | Request exceeded timeout                   |
| -32006 | Circuit Breaker Open   | Target service circuit breaker is open     |
| -32007 | Stream Not Found       | Stream ID does not exist                   |

## 6. Event Types

| Event Name             | Payload Schema                                    | Description                        |
|------------------------|---------------------------------------------------|------------------------------------|
| plugin.error         | { plugin_id: string, error: ErrorInfo }         | Plugin encountered an error        |
| plugin.ready         | { plugin_id: string }                           | Plugin is ready to communicate     |
| plugin.stopping      | { plugin_id: string, reason: string }           | Plugin is shutting down            |
| service.registered   | { service_id: string, service_name: string }    | New service registered             |
| service.unavailable  | { service_id: string, reason: string }          | Service became unavailable         |

## 7. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- RFC-0220 Plugin IPC
- RFC-0210 Plugin Events
