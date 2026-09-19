// @vitest-environment happy-dom
import React, { act } from "react";
import { createRoot } from "react-dom/client";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { BetaWelcome, RuntimeHealth } from "./BetaWelcome";
import { PanelErrorBoundary } from "../PanelErrorBoundary";
import { useProjectStore } from "../../stores";

vi.mock("../../ipc/bridge", () => ({
  selectProjectDirectory: vi.fn(),
  getBetaSystemInfo: vi.fn().mockRejectedValue(new Error("backend unavailable")),
  exportDiagnostics: vi.fn(),
}));
(globalThis as typeof globalThis & { IS_REACT_ACT_ENVIRONMENT: boolean }).IS_REACT_ACT_ENVIRONMENT = true;
async function render(element: React.ReactNode) {
  const container = document.createElement("div"), root = createRoot(container);
  await act(async () => { root.render(element); });
  const markup = container.innerHTML;
  act(() => root.unmount());
  return markup;
}
describe("Beta first-run resilience", () => {
  beforeEach(() => useProjectStore.setState({ currentProject: null, recentProjects: [], notifications: [] }));
  it("offers project actions and truthful backend failure without fake health", async () => {
    const markup = await render(<BetaWelcome/>);
    expect(markup).toContain("Create Project"); expect(markup).toContain("Open Project");
    expect(markup).toContain("Getting started"); expect(markup).toContain("Runtime health is unavailable");
    expect(markup).not.toContain("healthy</");
  });
  it("displays measured runtime state independently of provider configuration", async () => {
    expect(await render(<RuntimeHealth info={{ version: "test", platform: "windows", architecture: "x86_64", buildType: "test", commit: "unknown", runtimes: [{ name: "AI Runtime", status: "available", detail: "Provider credential not configured" }] }}/>)).toContain("Provider credential not configured");
  });
  it("isolates a failed panel and keeps its sibling usable", async () => {
    const error = vi.spyOn(console, "error").mockImplementation(() => undefined);
    const Broken = (): React.ReactNode => { throw new Error("private runtime payload"); };
    try { const markup = await render(<><PanelErrorBoundary title="Test Studio"><Broken/></PanelErrorBoundary><button>Other panel</button></>); expect(markup).toContain("Test Studio could not be displayed"); expect(markup).toContain("Other panel"); expect(markup).not.toContain("private runtime payload"); } finally { error.mockRestore(); }
  });
});
