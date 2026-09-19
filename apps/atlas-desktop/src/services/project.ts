import { useLogStore, useProjectStore } from "../stores";
import type { ProjectDescriptor } from "../types";
import { clearProjectSession, rememberProjectSession, restoreProjectSession } from "../ipc/bridge";
import { projectAssetService } from "./project-assets";

export function stableProjectId(projectPath: string): string {
  const normalized = projectPath.replaceAll("\\", "/").replace(/\/+$/, "").toLowerCase();
  let hash = 0xcbf29ce484222325n;
  for (const character of normalized) {
    hash ^= BigInt(character.codePointAt(0) ?? 0);
    hash = BigInt.asUintN(64, hash * 0x100000001b3n);
  }
  return `project-${hash.toString(16).padStart(16, "0")}`;
}

export class ProjectService {
  private opening = false;

  async openProject(project: ProjectDescriptor): Promise<void> {
    if (this.opening) throw new Error("PROJECT_OPEN_IN_PROGRESS");
    this.opening = true;
    project = { ...project, id: stableProjectId(project.path) };
    try {
      await projectAssetService.open(project.path);
      await rememberProjectSession(project.path);
      useProjectStore.getState().openProject(project);
      useProjectStore.getState().addRecentProject(project);
    } catch (error) {
      const current = useProjectStore.getState().currentProject;
      if (current && projectAssetService.isOpen(current.path)) {
        useProjectStore.getState().addNotification({ title: "Project switch failed", message: "The current project remains open. Save its changes successfully before switching projects.", severity: "error", acknowledged: false });
        throw error;
      }
      projectAssetService.stop();
      useProjectStore.getState().closeProject();
      useProjectStore.getState().addNotification({ title: "Project open failed", message: "Check folder permissions and project format compatibility. No project has been opened.", severity: "error", acknowledged: false });
      throw error;
    } finally {
      this.opening = false;
    }
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "ProjectService",
      message: `Project opened: ${project.name}`,
    });
  }

  closeProject(): void {
    const current = useProjectStore.getState().currentProject;
    void projectAssetService.saveNow().then(async () => {
      await clearProjectSession();
      projectAssetService.stop();
      useProjectStore.getState().closeProject();
    }).catch(() => useProjectStore.getState().addNotification({ title: "Project close failed", message: "The project remains open. Check folder access and retry so unsaved changes can be preserved.", severity: "error", acknowledged: false }));
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
    await this.openProject({ id: stableProjectId(path), name, path, createdAt: now, updatedAt: now, settings: { theme: "system", language: "en", autoSave: true, tabSize: 2 } });
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
