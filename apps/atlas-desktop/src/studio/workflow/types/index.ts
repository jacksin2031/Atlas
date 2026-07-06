// Atlas Workflow Studio - Core Workflow Types
// RFC-0302, RFC-0303, RFC-0307, RFC-0317, RFC-0323 compliant

import type { NodeCategory } from "./node-categories";

// ---------------------------------------------------------------------------
// Node types (RFC-0302 §5.2, RFC-0301 §10)
// ---------------------------------------------------------------------------

export interface WorkflowNodeData {
  id: string;
  type: string;
  label: string;
  description?: string;
  category: NodeCategory;
  inputs: PortDefinition[];
  outputs: PortDefinition[];
  parameters: Record<string, unknown>;
  conditions?: string[];
  actions?: string[];
  triggers?: string[];
  resources?: ResourceRequirement[];
  budget?: ExecutionBudget;
  priority?: number;
  timeout?: string;
  retryPolicy?: RetryPolicy;
  errorHandlers?: ErrorHandlerConfig[];
  recoveryPolicy?: RecoveryPolicy;
  observabilityConfig?: ObservabilityConfig;
  securityContext?: SecurityContext;
  version?: string;
  icon?: string;
  documentationUrl?: string;
  capabilities?: string[];
  // Runtime metadata (populated at execution time)
  executionState?: NodeExecutionState;
  validationState?: ValidationState;
  statusMessage?: string;
}

export interface PortDefinition {
  id: string;
  name: string;
  type: DataType;
  multiple?: boolean;
  description?: string;
  defaultValue?: unknown;
  dynamic?: boolean;
}

export interface ResourceRequirement {
  name: string;
  amount: number;
  unit: string;
}

export interface ExecutionBudget {
  maxDuration?: string;
  maxMemory?: number;
  maxCpu?: number;
  maxCost?: number;
}

export interface RetryPolicy {
  maxRetries: number;
  backoffStrategy: "fixed" | "linear" | "exponential";
  backoffDelay?: string;
}

export interface ErrorHandlerConfig {
  errorType: string;
  strategy: "retry" | "skip" | "compensate" | "abort";
  handlerNodeId?: string;
}

export type RecoveryPolicy = "none" | "checkpoint" | "compensation" | "rollback";

export interface ObservabilityConfig {
  traceEnabled: boolean;
  metricsEnabled: boolean;
  logLevel: "none" | "basic" | "detailed";
}

export interface SecurityContext {
  requiredPermissions: string[];
  isolationLevel: "none" | "process" | "container";
}

// ---------------------------------------------------------------------------
// Data types (RFC-0302 §6.3)
// ---------------------------------------------------------------------------

export type DataType =
  | "string"
  | "integer"
  | "float"
  | "boolean"
  | "array"
  | "object"
  | "null"
  | "duration"
  | "timestamp";

// ---------------------------------------------------------------------------
// Edge types (RFC-0302 §5.3)
// ---------------------------------------------------------------------------

export type EdgeType = "data" | "control" | "condition" | "event" | "resource" | "signal";

export interface WorkflowEdgeData {
  id: string;
  source: string;
  target: string;
  edgeType: EdgeType;
  condition?: string;
  transformation?: string;
  cardinality?: "one-to-one" | "one-to-many" | "many-to-one" | "many-to-many";
  timeout?: string;
  bufferSize?: number;
}

// ---------------------------------------------------------------------------
// Node execution states (RFC-0303 §7.3)
// ---------------------------------------------------------------------------

export type NodeExecutionState =
  | "pending"
  | "ready"
  | "running"
  | "waiting"
  | "completed"
  | "failed"
  | "cancelled"
  | "compensated";

// ---------------------------------------------------------------------------
// Node design-time states (RFC-0301 §11)
// ---------------------------------------------------------------------------

export type NodeDesignState =
  | "draft"
  | "validated"
  | "invalid"
  | "queued"
  | "terminating";

// ---------------------------------------------------------------------------
// Validation states
// ---------------------------------------------------------------------------

export type ValidationState = "valid" | "invalid" | "unchecked";

export interface ValidationResult {
  rule: string;
  severity: "error" | "warning" | "info";
  message: string;
  location?: "node" | "edge" | "workflow";
  nodeId?: string;
}

// ---------------------------------------------------------------------------
// Variable types (RFC-0302 §6)
// ---------------------------------------------------------------------------

export type VariableScope =
  | "workflow"
  | "node"
  | "subgraph"
  | "edge"
  | "environment"
  | "project"
  | "global"
  | "session";

export interface WorkflowVariable {
  id: string;
  name: string;
  type: DataType;
  scope: VariableScope;
  value?: unknown;
  description?: string;
  writable: boolean;
  defaultValue?: unknown;
}

// ---------------------------------------------------------------------------
// Workflow definition (RFC-0302 §5.1)
// ---------------------------------------------------------------------------

export interface WorkflowDefinition {
  id: string;
  version: string;
  name: string;
  description?: string;
  nodes: WorkflowNodeData[];
  edges: WorkflowEdgeData[];
  variables: WorkflowVariable[];
  parameters: Record<string, unknown>;
  metadata: WorkflowMetadata;
}

export interface WorkflowMetadata {
  createdAt: number;
  updatedAt: number;
  createdBy?: string;
  tags?: string[];
}

// ---------------------------------------------------------------------------
// Execution instance (RFC-0303)
// ---------------------------------------------------------------------------

export type WorkflowRunStatus =
  | "created"
  | "initializing"
  | "running"
  | "paused"
  | "completed"
  | "failed"
  | "cancelled"
  | "restarting";

export interface WorkflowRun {
  id: string;
  workflowId: string;
  status: WorkflowRunStatus;
  currentNodeId?: string;
  startedAt?: number;
  completedAt?: number;
  nodeStates: Record<string, NodeExecutionState>;
  variables: Record<string, unknown>;
  errors: ExecutionError[];
  metrics: ExecutionMetrics;
}

export interface ExecutionError {
  nodeId: string;
  errorCode: string;
  message: string;
  timestamp: number;
  stackTrace?: string;
}

export interface ExecutionMetrics {
  totalNodes: number;
  completedNodes: number;
  failedNodes: number;
  duration: number;
  throughput: number;
}

// ---------------------------------------------------------------------------
// Debug types (RFC-0316)
// ---------------------------------------------------------------------------

export type BreakpointType =
  | "node"
  | "edge"
  | "condition"
  | "event"
  | "variable";

export interface Breakpoint {
  id: string;
  type: BreakpointType;
  targetId: string;
  condition?: string;
  enabled: boolean;
  hitCount: number;
}

export interface DebugSession {
  id: string;
  runId: string;
  breakpoints: Breakpoint[];
  currentNodeId?: string;
  executionPath: string[];
  callStack: DebugFrame[];
  history: DebugEvent[];
  startTime: number;
  paused: boolean;
}

export interface DebugFrame {
  nodeId: string;
  functionName?: string;
  timestamp: number;
}

export interface DebugEvent {
  id: string;
  type: "node_enter" | "node_exit" | "edge_traverse" | "variable_change" | "breakpoint_hit" | "error";
  nodeId?: string;
  edgeId?: string;
  variableName?: string;
  timestamp: number;
  data?: Record<string, unknown>;
}

// ---------------------------------------------------------------------------
// Plugin node registration (RFC-0323)
// ---------------------------------------------------------------------------

export interface PluginNodeRegistration {
  nodeId: string;
  typeName: string;
  category: NodeCategory;
  label: string;
  description: string;
  icon?: string;
  inputs: PortDefinition[];
  outputs: PortDefinition[];
  parameters: Record<string, unknown>;
  version: string;
  capabilities: string[];
  documentationUrl?: string;
  pluginId: string;
}

// ---------------------------------------------------------------------------
// Canvas interaction types
// ---------------------------------------------------------------------------

export interface CanvasTransform {
  x: number;
  y: number;
  zoom: number;
}

export interface SelectionState {
  selectedNodeIds: Set<string>;
  selectedEdgeIds: Set<string>;
  draggingNodeId?: string;
  panOrigin?: { x: number; y: number };
}

// ---------------------------------------------------------------------------
// Import/Export formats (RFC-0328)
// ---------------------------------------------------------------------------

export type SerializationFormat = "json" | "yaml" | "canonical" | "exchange" | "checkpoint" | "archive";

export interface ImportExportResult {
  success: boolean;
  workflow?: WorkflowDefinition;
  errors?: ValidationResult[];
  format: SerializationFormat;
  version: string;
}
