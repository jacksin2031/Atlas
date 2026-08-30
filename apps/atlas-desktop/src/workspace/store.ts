import { create } from "zustand";
import type { WorkspaceId } from "./types";

interface WorkspaceState {
  activeWorkspace: WorkspaceId;
  panelRequest: { id: string; nonce: number } | null;
  setActiveWorkspace: (workspace: WorkspaceId) => void;
  requestPanel: (id: string) => void;
  consumePanelRequest: () => void;
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  activeWorkspace: "workflow",
  panelRequest: null,
  setActiveWorkspace: (activeWorkspace) => set({ activeWorkspace }),
  requestPanel: (id) => set((state) => ({ panelRequest: { id, nonce: (state.panelRequest?.nonce ?? 0) + 1 } })),
  consumePanelRequest: () => set({ panelRequest: null }),
}));
