import { useLogStore, useProjectStore } from "../stores";
import type { ProjectDescriptor } from "../types";
import { clearProjectSession, rememberProjectSession, restoreProjectSession } from "../ipc/bridge";
import { projectAssetService } from "./project-assets";

export class ProjectService {

  openProject(project: ProjectDescriptor): void {
    useProjectStore.getState().openProject(project);
    useProjectStore.getState().addRecentProject(project);
    void rememberProjectSession(project.path).then(() => projectAssetService.open(project.path)).catch((error) => useProjectStore.getState().addNotification({
      title: "Project recovery failed", message: error instanceof Error ? error.message : String(error), severity: "error", acknowledged: false,
    }));
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "ProjectService",
      message: `Project opened: ${project.name}`,
    });
  }

  closeProject(): void {
    const current = useProjectStore.getState().currentProject;
    void projectAssetService.close().then(() => clearProjectSession());
    useProjectStore.getState().closeProject();
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "ProjectService",
      message: current ? `Project closed: ${current.name}` : "No project was open",
    });
  }

  async restoreLastProject(): Promise<boolean> {
    const path = await restoreProjectSession();
    if (!path) return false;
    const name = path.split(/[\\/]/).filter(Boolean).at(-1) ?? "Atlas Project";
    const now = Date.now();
    this.openProject({ id: `project-restored-${now}`, name, path, createdAt: now, updatedAt: now, settings: { theme: "system", language: "en", autoSave: true, tabSize: 2 } });
    return true;
  }

  getRecentProjects(): ProjectDescriptor[] {
    return useProjectStore.getState().recentProjects;
  }

  getCurrentProject(): ProjectDescriptor | null {
    return useProjectStore.getState().currentProject;
  }

  addRecentProject(project: ProjectDescriptor): void {
    useProjectStore.getState().addRecentProject(project);
  }

  removeRecentProject(id: string): void {
    useProjectStore.setState((state) => ({
      recentProjects: state.recentProjects.filter((p) => p.id !== id),
    }));
  }
}

export const projectService = new ProjectService();
