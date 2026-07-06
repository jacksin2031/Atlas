import { useLogStore, useProjectStore } from "../stores";
import type { ProjectDescriptor } from "../types";

export class ProjectService {

  openProject(project: ProjectDescriptor): void {
    useProjectStore.getState().openProject(project);
    useProjectStore.getState().addRecentProject(project);
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "ProjectService",
      message: `Project opened: ${project.name}`,
    });
  }

  closeProject(): void {
    const current = useProjectStore.getState().currentProject;
    useProjectStore.getState().closeProject();
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "ProjectService",
      message: current ? `Project closed: ${current.name}` : "No project was open",
    });
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

