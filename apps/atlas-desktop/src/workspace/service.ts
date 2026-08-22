import { Actions, DockLocation, Model } from "flexlayout-react";
import { useWorkspaceStore } from "./store";
import type { PanelDefinition, WorkspaceId } from "./types";

class WorkspaceService {
  private models = new Map<WorkspaceId, Model>();
  private panels = new Map<string, PanelDefinition>();
  private resetHandlers = new Map<WorkspaceId, () => void>();

  registerModel(id: WorkspaceId, model: Model, onReset: () => void): void { this.models.set(id, model); this.resetHandlers.set(id, onReset); }
  registerPanels(panels: readonly PanelDefinition[]): void { panels.forEach((panel) => this.panels.set(panel.id, panel)); }
  switchWorkspace(id: WorkspaceId): void { useWorkspaceStore.getState().setActiveWorkspace(id); }
  resetActiveLayout(): void { this.resetHandlers.get(useWorkspaceStore.getState().activeWorkspace)?.(); }
  openPanel(id: string): void {
    const workspace = useWorkspaceStore.getState().activeWorkspace;
    const model = this.models.get(workspace);
    const panel = this.panels.get(id);
    if (!model || !panel || (panel.workspace !== "shared" && panel.workspace !== workspace)) return;
    const existing = model.getNodeById(id);
    if (existing) { model.doAction(Actions.selectTab(id)); return; }
    const defaultTabset = panel.workspace === "shared" ? `${workspace}-${id === "shared.project-explorer" ? "left" : "bottom"}` : panel.defaultTabset;
    model.doAction(Actions.addNode({ type: "tab", id, component: id, name: panel.title, enableClose: panel.closable, enableRename: false }, defaultTabset, DockLocation.CENTER, -1, true));
  }
  closePanel(id: string): void { this.models.get(useWorkspaceStore.getState().activeWorkspace)?.doAction(Actions.deleteTab(id)); }
}

export const workspaceService = new WorkspaceService();
