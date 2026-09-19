import { beforeEach, describe, expect, it, vi } from "vitest";
import { ProjectService } from "./project";
import { projectAssetService } from "./project-assets";
import { clearProjectSession, rememberProjectSession } from "../ipc/bridge";
import { useProjectStore } from "../stores";

vi.mock("./project-assets", () => ({ projectAssetService: { open: vi.fn(), close: vi.fn(), saveNow: vi.fn(), stop: vi.fn(), isOpen: vi.fn() } }));
vi.mock("../ipc/bridge", () => ({ rememberProjectSession: vi.fn(), restoreProjectSession: vi.fn(), clearProjectSession: vi.fn() }));
const project = { id: "test", name: "測試 Project", path: "C:/Atlas Projects/測試", createdAt: 1, updatedAt: 1, settings: { theme: "system" as const, language: "en", autoSave: true, tabSize: 2 } };
describe("project activation", () => {
  beforeEach(() => { vi.resetAllMocks(); useProjectStore.setState({ currentProject: null, recentProjects: [], notifications: [] }); });
  it("does not activate or remember an incompatible project", async () => {
    vi.mocked(projectAssetService.open).mockRejectedValue(new Error("FUTURE_SCHEMA"));
    await expect(new ProjectService().openProject(project)).rejects.toThrow("FUTURE_SCHEMA");
    expect(useProjectStore.getState().currentProject).toBeNull(); expect(rememberProjectSession).not.toHaveBeenCalled(); expect(useProjectStore.getState().recentProjects).toEqual([]);
  });
  it("waits for assets before marking the project open", async () => {
    let finish!: () => void; vi.mocked(projectAssetService.open).mockImplementation(() => new Promise<void>((resolve) => { finish = resolve; }));
    const opened = new ProjectService().openProject(project);
    expect(useProjectStore.getState().currentProject).toBeNull(); finish(); await opened;
    expect(rememberProjectSession).toHaveBeenCalledWith(project.path); expect(useProjectStore.getState().currentProject?.path).toBe(project.path);
  });
  it("keeps the current project active when its pre-switch save fails", async () => {
    useProjectStore.setState({ currentProject: project });
    vi.mocked(projectAssetService.open).mockRejectedValue(new Error("ACCESS_DENIED"));
    vi.mocked(projectAssetService.isOpen).mockReturnValue(true);
    await expect(new ProjectService().openProject({ ...project, path: "C:/another" })).rejects.toThrow("ACCESS_DENIED");
    expect(useProjectStore.getState().currentProject?.path).toBe(project.path);
    expect(projectAssetService.stop).not.toHaveBeenCalled();
  });
  it("keeps project ownership and autosave when clearing the session fails on close", async () => {
    useProjectStore.setState({ currentProject: project });
    vi.mocked(projectAssetService.saveNow).mockResolvedValue(undefined);
    vi.mocked(clearProjectSession).mockRejectedValue(new Error("ACCESS_DENIED"));
    new ProjectService().closeProject();
    await vi.waitFor(() => expect(useProjectStore.getState().notifications.at(-1)?.title).toBe("Project close failed"));
    expect(useProjectStore.getState().currentProject?.path).toBe(project.path);
    expect(projectAssetService.stop).not.toHaveBeenCalled();
  });
  it("saves and clears the session before releasing project ownership", async () => {
    useProjectStore.setState({ currentProject: project });
    vi.mocked(projectAssetService.saveNow).mockResolvedValue(undefined);
    let finish!: () => void;
    vi.mocked(clearProjectSession).mockImplementation(() => new Promise<void>((resolve) => { finish = resolve; }));
    new ProjectService().closeProject();
    await vi.waitFor(() => expect(clearProjectSession).toHaveBeenCalled());
    expect(projectAssetService.stop).not.toHaveBeenCalled();
    expect(useProjectStore.getState().currentProject?.path).toBe(project.path);
    finish();
    await vi.waitFor(() => expect(useProjectStore.getState().currentProject).toBeNull());
    expect(projectAssetService.stop).toHaveBeenCalledOnce();
  });
});
