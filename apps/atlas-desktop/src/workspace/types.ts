import type React from "react";

export type WorkspaceId = "workflow" | "vision" | "ai" | "knowledge" | "marketplace";

export interface PanelDefinition {
  id: string;
  title: string;
  workspace: WorkspaceId | "shared";
  component: React.ComponentType;
  closable: boolean;
  dockable: boolean;
  defaultTabset: string;
  icon?: "workflow" | "vision" | "ai" | "folder";
}
