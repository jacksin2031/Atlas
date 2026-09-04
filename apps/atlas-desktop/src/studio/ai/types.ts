export type AIModelCapability =
  | "chat" | "completion" | "embedding" | "vision" | "audio" | "image"
  | "tool_calling" | "structured_output" | "streaming" | "batch"
  | "fine_tuning" | "rag" | "memory" | "reasoning";

export type AIProviderHealth = "healthy" | "busy" | "degraded" | "unhealthy" | "unknown";
export type AIConnectionState = "connected" | "disconnected" | "connecting" | "error";
export type AIStudioMode = "playground" | "prompt" | "conversation" | "agent" | "memory" | "tools";
export type AIMessageRole = "system" | "user" | "assistant" | "tool";
export type AIContextKind = "prompt" | "vision" | "knowledge" | "memory" | "tool";
export type AIContextAvailability = "available" | "resolving" | "missing" | "unavailable";

export interface AIProviderDescriptor {
  providerId: string;
  name: string;
  providerType: string;
  version: string;
  capabilities: AIModelCapability[];
  health: AIProviderHealth;
  connectionState: AIConnectionState;
  enabled: boolean;
  latencyMs?: number;
}

export interface AIModelDescriptor {
  modelId: string;
  name: string;
  providerId: string;
  version: string;
  capabilities: AIModelCapability[];
  contextWindow?: number;
  modality?: string[];
  state: "created" | "loading" | "ready" | "running" | "unloading" | "unloaded" | "error" | "snapshot";
  requirements?: { gpuMemoryMb?: number; ramMb?: number; cpuCores?: number };
  supportedParameters?: Array<keyof AIInferenceParameters>;
}

export interface AIMessage {
  id: string;
  role: AIMessageRole;
  content: string;
  createdAt: string;
  metadata?: Record<string, unknown>;
}

export interface AIInferenceParameters {
  temperature: number;
  topP: number;
  maxTokens: number;
  stopSequences: string[];
  seed?: number;
  responseFormat?: string;
  reasoning?: string;
  stream: boolean;
  toolChoice?: string;
}

export interface AIContextReference {
  id: string;
  kind: AIContextKind;
  label: string;
  source?: string;
  preview?: string;
  includedInRequest?: boolean;
  availability?: AIContextAvailability;
  unavailableReason?: string;
  metadata?: Record<string, unknown>;
}

export interface AINormalizedRequest {
  requestId: string;
  timestamp: string;
  providerId: string;
  modelId: string;
  messages: AIMessage[];
  parameters: Partial<AIInferenceParameters>;
  tools: string[];
  contextReferences: AIContextReference[];
  attachments: Array<{ id: string; kind: string; label: string; dataUrl?: string; metadata?: Record<string, unknown> }>;
}

export interface AINormalizedResponse {
  requestId: string;
  correlationId?: string;
  providerId: string;
  modelId: string;
  content: string;
  finishReason?: string;
  latencyMs?: number;
  usage?: { inputTokens?: number; outputTokens?: number; totalTokens?: number };
  toolCalls?: AIToolInvocation[];
  metadata?: Record<string, unknown>;
}

export interface AIMemoryItem {
  memoryId: string;
  content: string;
  scope: "session" | "workspace" | "project" | "global";
  createdAt?: string;
  updatedAt?: string;
  source?: string;
  status?: string;
  includedInRequest?: boolean;
  metadata?: Record<string, unknown>;
}

export interface AIToolDescriptor {
  toolId: string;
  name: string;
  description: string;
  provider?: string;
  permissions: Array<"none" | "read_only" | "write" | "execute" | "admin">;
  capabilities: string[];
  enabled: boolean;
  status?: string;
  parameters?: Record<string, unknown>;
}

export interface AIToolInvocation {
  invocationId: string;
  toolId: string;
  arguments: Record<string, unknown>;
  status: "requested" | "permission_check" | "executing" | "completed" | "failed" | "cancelled";
  durationMs?: number;
  result?: unknown;
  error?: string;
}

export interface AIAgentDescriptor {
  agentId: string;
  name: string;
  state: "created" | "ready" | "running" | "paused" | "completed" | "failed" | "stopped";
  capabilities: string[];
  policy?: Record<string, unknown>;
  modelId?: string;
  toolIds: string[];
  memoryScope?: string;
}

export interface AIRuntimeEvent {
  eventId: string;
  eventType: string;
  timestamp: string;
  correlationId?: string;
  source?: string;
  summary?: string;
  metadata?: Record<string, unknown>;
}

/** Event payload emitted by the Python host through Tauri's ai://runtime-event channel. */
export interface AIRuntimeTransportEvent extends AIRuntimeEvent {
  requestId?: string;
  delta?: string;
  response?: AINormalizedResponse;
  error?: string;
  metrics?: AIMetricsSnapshot;
}

export interface AIMetricsSnapshot {
  requestCount?: number;
  successCount?: number;
  failureCount?: number;
  latencyMs?: number;
  firstTokenLatencyMs?: number;
  inputTokens?: number;
  outputTokens?: number;
  totalTokens?: number;
  queueDepth?: number;
  modelLoadTimeMs?: number;
  agentExecutionTimeMs?: number;
  toolExecutionTimeMs?: number;
}

export interface AIRuntimeSnapshot {
  runtimeHealth: AIProviderHealth;
  providers: AIProviderDescriptor[];
  models: AIModelDescriptor[];
  memories: AIMemoryItem[];
  tools: AIToolDescriptor[];
  agents: AIAgentDescriptor[];
  events: AIRuntimeEvent[];
  metrics: AIMetricsSnapshot;
}

export interface AIStudioSession {
  sessionId: string;
  name: string;
  providerId: string | null;
  modelId: string | null;
  createdAt: string;
}

export interface AIPromptDraft {
  name: string;
  description: string;
  systemPrompt: string;
  userTemplate: string;
  variables: Record<string, string>;
  version: string;
  tags: string[];
  metadata: Record<string, string>;
}

export interface AIPromptComparison {
  promptA: string;
  promptB: string;
  responseA: AINormalizedResponse | null;
  responseB: AINormalizedResponse | null;
  errorA?: string;
  errorB?: string;
}
