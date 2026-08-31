import React from "react";
import { Icon, IconButton } from "../../design-system";
import { useThemeStore } from "../../stores";
import { useWorkspaceStore, workspaceService } from "../../workspace";

interface ToolbarProps { onToggleCommandPalette: () => void }
export const Toolbar: React.FC<ToolbarProps> = ({ onToggleCommandPalette }) => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme); const active = useWorkspaceStore((s) => s.activeWorkspace);
  return <div className="workspace-toolbar" data-theme={resolvedTheme}><div className="workspace-switcher" role="tablist" aria-label="Atlas workspaces">
    <button role="tab" aria-selected={active === "workflow"} className={active === "workflow" ? "active" : ""} onClick={() => workspaceService.switchWorkspace("workflow")}><Icon name="workflow"/>Workflow</button>
    <button role="tab" aria-selected={active === "vision"} className={active === "vision" ? "active" : ""} onClick={() => workspaceService.switchWorkspace("vision")}><Icon name="vision"/>Vision</button>
    <button role="tab" aria-selected={active === "ai"} className={active === "ai" ? "active" : ""} onClick={() => workspaceService.switchWorkspace("ai")}><Icon name="ai"/>AI</button>
    <button role="tab" aria-selected={active === "knowledge"} className={active === "knowledge" ? "active" : ""} onClick={() => workspaceService.switchWorkspace("knowledge")}><Icon name="folder"/>Knowledge</button>
  </div><div className="toolbar-spacer"/><IconButton icon="command" label="Command Palette (Ctrl+Shift+P)" onClick={onToggleCommandPalette}/></div>;
};
