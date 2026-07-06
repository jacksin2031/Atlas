import { useLogStore, useLayoutStore } from "../stores";
import type { PanelId, DockPosition } from "../types";

export class LayoutService {

  initialize(): void {
    useLayoutStore.getState().loadLayout();
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "LayoutService",
      message: "Layout service initialized",
    });
  }

  setPanelVisible(id: PanelId, visible: boolean): void {
    useLayoutStore.getState().setPanelVisible(id, visible);
  }

  setPanelCollapsed(id: PanelId, collapsed: boolean): void {
    useLayoutStore.getState().setPanelCollapsed(id, collapsed);
  }

  setPanelPosition(id: PanelId, position: DockPosition): void {
    useLayoutStore.getState().setPanelPosition(id, position);
  }

  setActivePanel(id: PanelId): void {
    useLayoutStore.getState().setActivePanel(id);
  }

  resetLayout(): void {
    useLayoutStore.getState().resetLayout();
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "LayoutService",
      message: "Layout reset to defaults",
    });
  }

  saveLayout(): void {
    useLayoutStore.getState().saveLayout();
  }

  getPanelOrder(position: DockPosition): PanelId[] {
    const panels = useLayoutStore.getState().config.panels;
    return Object.values(panels)
      .filter((p) => p.position === position && p.visible)
      .sort((a, b) => a.order - b.order)
      .map((p) => p.id);
  }

  getVisiblePanels(): PanelId[] {
    const panels = useLayoutStore.getState().config.panels;
    return Object.values(panels).filter((p) => p.visible).map((p) => p.id);
  }

  destroy(): void {
    this.saveLayout();
  }
}

export const layoutService = new LayoutService();

