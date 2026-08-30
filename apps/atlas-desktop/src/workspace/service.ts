import { Actions, Model } from "flexlayout-react";
import { useWorkspaceStore } from "./store";
import type { PanelDefinition, WorkspaceId } from "./types";

class WorkspaceService {
  private models = new Map<WorkspaceId, Model>();
  private panels = new Map<string, PanelDefinition>();
  private resetHandlers = new Map<WorkspaceId, () => void>();
  private mutationHandlers = new Map<WorkspaceId, () => void>();

  registerModel(id: WorkspaceId, model: Model, onReset: () => void, onMutation: () => void = () => undefined): void { this.models.set(id, model); this.resetHandlers.set(id, onReset); this.mutationHandlers.set(id, onMutation); }
  registerPanels(panels: readonly PanelDefinition[]): void { panels.forEach((panel) => this.panels.set(panel.id, panel)); }
  switchWorkspace(id: WorkspaceId): void { useWorkspaceStore.getState().setActiveWorkspace(id); }
  resetActiveLayout(): void { this.resetHandlers.get(useWorkspaceStore.getState().activeWorkspace)?.(); }
  openPanel(id: string): void {
    useWorkspaceStore.getState().requestPanel(id);
  }
  closePanel(id: string): void { const workspace=useWorkspaceStore.getState().activeWorkspace; this.models.get(workspace)?.doAction(Actions.deleteTab(id)); this.mutationHandlers.get(workspace)?.(); }
}

export const workspaceService = new WorkspaceService();
