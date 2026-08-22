import { create } from "zustand";
import type { WorkspaceId } from "./types";

interface WorkspaceState {
  activeWorkspace: WorkspaceId;
  setActiveWorkspace: (workspace: WorkspaceId) => void;
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  activeWorkspace: "workflow",
  setActiveWorkspace: (activeWorkspace) => set({ activeWorkspace }),
}));
