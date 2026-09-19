// @vitest-environment happy-dom
import React, { act } from "react";
import { createRoot } from "react-dom/client";
import { afterEach, expect, it, vi } from "vitest";
import { useProjectStore } from "../../stores";
import { AppLayout } from "./AppLayout";

const mocks = vi.hoisted(() => ({ initialize: vi.fn().mockResolvedValue(undefined) }));
vi.mock("./MenuBar", () => ({ MenuBar: () => null }));
vi.mock("./Toolbar", () => ({ Toolbar: () => null }));
vi.mock("./StatusBar", () => ({ StatusBar: () => null }));
vi.mock("./BetaWelcome", () => ({ BetaWelcome: () => null, BetaHelp: () => null }));
vi.mock("../CommandPalette", () => ({ CommandPalette: () => null }));
vi.mock("../../workspace", () => ({ WorkspaceManager: () => null, useWorkspaceStore: (select: (state: { activeWorkspace: string }) => unknown) => select({ activeWorkspace: "knowledge" }) }));
vi.mock("../../studio/marketplace/service", () => ({ marketplaceService: { connect: async () => () => undefined }, registerMarketplaceCommands: vi.fn() }));
vi.mock("../../studio/vision", () => ({ VisionToolbar: () => null }));
vi.mock("../../studio/vision/commands", () => ({ installVisionShortcuts: vi.fn(), registerVisionCommands: vi.fn() }));
vi.mock("../../studio/vision/services/demo-provider", () => ({ createVisionDemoData: vi.fn(), visionDemoModeEnabled: false }));
vi.mock("../../studio/vision/stores", () => ({ useVisionResultsStore: {}, useVisionTimelineStore: {} }));
vi.mock("../../studio/ai", () => ({ AIToolbar: () => null, aiDemoModeEnabled: false, aiStudioService: { connectRuntimeEvents: async () => () => undefined }, createAIDemoAdapter: vi.fn(), installAIShortcuts: vi.fn(), registerAICommands: vi.fn() }));
vi.mock("../../studio/workflow", () => ({ executorService: { connectRuntimeEvents: async () => () => undefined }, installWorkflowShortcuts: vi.fn(), registerWorkflowCommands: vi.fn() }));
vi.mock("../../studio/knowledge", () => ({ knowledgeStudioService: { initialize: mocks.initialize, activateProject: async () => undefined, connectRuntimeEvents: async () => () => undefined }, installKnowledgeShortcuts: vi.fn(), registerKnowledgeCommands: vi.fn() }));

(globalThis as typeof globalThis & { IS_REACT_ACT_ENVIRONMENT: boolean }).IS_REACT_ACT_ENVIRONMENT = true;
afterEach(() => vi.clearAllMocks());

it("loads the restored Knowledge workspace only after a project is ready, and reloads when projects change", async () => {
  useProjectStore.setState({ currentProject: null });
  const root = createRoot(document.createElement("div"));
  const project = { id: "restored-a", name: "A", path: "C:\\acceptance\\A", createdAt: 0, updatedAt: 0, settings: { theme: "system" as const, language: "en", autoSave: true, tabSize: 2 } };
  try {
    await act(async () => { root.render(<AppLayout />); });
    expect(mocks.initialize).not.toHaveBeenCalled();
    await act(async () => { useProjectStore.setState({ currentProject: project }); });
    expect(mocks.initialize).toHaveBeenCalledTimes(1);
    await act(async () => { useProjectStore.setState({ currentProject: { ...project, id: "restored-b", path: "C:\\acceptance\\B" } }); });
    expect(mocks.initialize).toHaveBeenCalledTimes(2);
    await act(async () => { useProjectStore.setState({ currentProject: null }); });
    expect(mocks.initialize).toHaveBeenCalledTimes(2);
  } finally { await act(async () => { root.unmount(); }); }
});
