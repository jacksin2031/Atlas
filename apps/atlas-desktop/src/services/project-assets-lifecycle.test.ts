// @vitest-environment happy-dom
import { afterEach, describe, expect, it, vi } from "vitest";
import { projectAssetService, restoreProjectAssets } from "./project-assets";
import { loadProjectAssets, saveProjectAssets } from "../ipc/bridge";
import { useAIStudioStore } from "../studio/ai/store";
import { useWorkspaceStore } from "../workspace/store";
import { collectPanelIds, layoutStorageKey, loadWorkspaceLayout } from "../workspace/persistence";
import { cloneDefaultLayout } from "../workspace/layouts";
import { getAllowedPanelIds } from "../workspace/panel-registry";
import type { WorkspaceId } from "../workspace/types";

vi.mock("../ipc/bridge", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../ipc/bridge")>();
  return { ...actual, loadProjectAssets: vi.fn(), saveProjectAssets: vi.fn() };
});
describe("project assets activation safety", () => {
  afterEach(async () => { vi.mocked(saveProjectAssets).mockResolvedValue(undefined); await projectAssetService.close(); vi.resetAllMocks(); });
  it("initializes a fresh project without previous private AI input", async () => {
    useAIStudioStore.setState({ userInput: "private previous project input" });
    vi.mocked(loadProjectAssets).mockResolvedValue(null);
    await projectAssetService.open("C:/Atlas Projects/新專案");
    expect(JSON.stringify(vi.mocked(saveProjectAssets).mock.calls[0]?.[1])).not.toContain("private previous project input");
  });
  it("does not write an unsupported project after load failure", async () => {
    vi.mocked(loadProjectAssets).mockRejectedValue(new Error("FUTURE_SCHEMA"));
    await expect(projectAssetService.open("C:/future")).rejects.toThrow("FUTURE_SCHEMA");
    await projectAssetService.saveNow();
    expect(saveProjectAssets).not.toHaveBeenCalled();
  });
  it("surfaces initialization write failures instead of reporting success", async () => {
    vi.mocked(loadProjectAssets).mockResolvedValue(null);
    vi.mocked(saveProjectAssets).mockRejectedValue(new Error("ACCESS_DENIED"));
    await expect(projectAssetService.open("C:/readonly")).rejects.toThrow("ACCESS_DENIED");
  });
  it("detaches a stopped project so a failed activation cannot write it later", async () => {
    vi.mocked(loadProjectAssets).mockResolvedValue(null);
    await projectAssetService.open("C:/stopped");
    projectAssetService.stop();
    vi.mocked(saveProjectAssets).mockClear();
    await projectAssetService.saveNow();
    expect(saveProjectAssets).not.toHaveBeenCalled();
  });
  it("clears prior project workspace and layouts when initializing", async () => {
    useWorkspaceStore.setState({ activeWorkspace: "ai" });
    localStorage.setItem(layoutStorageKey("ai"), JSON.stringify({ previous: true }));
    vi.mocked(loadProjectAssets).mockResolvedValue(null);
    await projectAssetService.open("C:/fresh-layout");
    expect(useWorkspaceStore.getState().activeWorkspace).toBe("workflow");
    expect(localStorage.getItem(layoutStorageKey("ai"))).toBeNull();
  });
  it("restores all product workspace layouts from project assets", async () => {
    const ids: WorkspaceId[] = ["workflow", "vision", "ai", "knowledge", "marketplace"];
    const layouts = Object.fromEntries(ids.map((id) => [id, { version: 1, workspace: id, layout: cloneDefaultLayout(id) }]));
    vi.mocked(loadProjectAssets).mockResolvedValue({ workspace: { activeWorkspace: "marketplace", layouts } });
    await projectAssetService.open("C:/Atlas Projects/全工作區");
    expect(useWorkspaceStore.getState().activeWorkspace).toBe("marketplace");
    for (const id of ids) {
      expect(localStorage.getItem(layoutStorageKey(id))).not.toBeNull();
      expect(collectPanelIds(loadWorkspaceLayout(id, getAllowedPanelIds(id)))).toContain(collectPanelIds(cloneDefaultLayout(id))[0]);
    }
  });
  it("falls back safely when a restored workspace layout is corrupt", async () => {
    const id: WorkspaceId = "marketplace";
    vi.mocked(loadProjectAssets).mockResolvedValue({ workspace: { activeWorkspace: id, layouts: { [id]: { version: 1, workspace: id, layout: { invalid: true } } } } });
    await projectAssetService.open("C:/Atlas Projects/corrupt-layout");
    expect(collectPanelIds(loadWorkspaceLayout(id, getAllowedPanelIds(id))).length).toBeGreaterThan(0);
  });
  it("rejects malformed execution before changing AI state", () => {
    useAIStudioStore.setState({ userInput: "keep current" });
    expect(() => restoreProjectAssets({ ai: { userInput: "replacement" }, execution: { runs: { broken: { status: "running", errors: null } } } })).toThrow("Invalid restored execution");
    expect(useAIStudioStore.getState().userInput).toBe("keep current");
    expect(() => restoreProjectAssets({ execution: { runs: [] } })).toThrow("Invalid restored execution runs");
  });
});
