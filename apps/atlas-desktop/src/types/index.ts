// Atlas Desktop Shell - Type Definitions

export type ThemeMode = "dark" | "light" | "system";

export type AppStatus =
  | "created"
  | "initializing"
  | "ready"
  | "running"
  | "shutting_down"
  | "terminated";

export type PanelId =
  | "project-explorer"
  | "runtime-monitor"
  | "output"
  | "console"
  | "logs"
  | "extensions"
  | "settings"
  | "problems"
  | "notifications";

export type DockPosition = "left" | "right" | "bottom" | "center";

export interface PanelInstance {
  id: PanelId;
  title: string;
  visible: boolean;
  position: DockPosition;
  order: number;
  collapsed: boolean;
}

export interface LayoutConfig {
  panels: Record<PanelId, PanelInstance>;
  splitterPositions: Record<string, number>;
  activePanel: PanelId | null;
}

export type LogLevel = "trace" | "debug" | "info" | "warn" | "error";

export interface LogEntry {
  id: string;
  timestamp: number;
  level: LogLevel;
  source: string;
  message: string;
  runtime?: string;
}

export type RuntimeHealth =
  | "healthy"
  | "degraded"
  | "unhealthy"
  | "unknown"
  | "starting"
  | "stopping";

export interface RuntimeInfo {
  name: string;
  status: AppStatus;
  health: RuntimeHealth;
  cpuUsage: number;
  memoryUsage: number;
  uptime: number;
  metrics: RuntimeMetric[];
}

export interface RuntimeMetric {
  name: string;
  value: number;
  unit: string;
  timestamp: number;
}

export type PluginState = "installed" | "available" | "updating" | "error";

export type PluginHealth = "healthy" | "degraded" | "unhealthy" | "unknown";

export interface PluginEntry {
  id: string;
  name: string;
  description: string;
  version: string;
  state: PluginState;
  health: PluginHealth;
  enabled: boolean;
  author: string;
}

export interface ProjectDescriptor {
  id: string;
  name: string;
  path: string;
  createdAt: number;
  updatedAt: number;
  settings: ProjectSettings;
}

export interface ProjectSettings {
  theme: ThemeMode;
  language: string;
  autoSave: boolean;
  tabSize: number;
}

export type NotificationSeverity = "info" | "warning" | "error" | "success";

export interface Notification {
  id: string;
  title: string;
  message: string;
  severity: NotificationSeverity;
  timestamp: number;
  acknowledged: boolean;
}

export interface CommandPaletteItem {
  id: string;
  label: string;
  description: string;
  shortcut?: string;
  category: string;
  handler: () => void;
}

export interface LogFilter {
  level: LogLevel | "all";
  source: string | "all";
  query: string;
}

export interface MessageEnvelope {
  id: string;
  header: MessageHeader;
  payload: unknown;
}

export interface MessageHeader {
  type: string;
  source: string;
  destination: string;
  priority: number;
  timestamp: number;
}


// Workflow Studio panel
export type WorkflowStudioPanelId = 'workflow-studio';

export type ExtendedPanelId = PanelId | WorkflowStudioPanelId;
