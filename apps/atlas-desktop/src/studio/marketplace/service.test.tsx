// @vitest-environment happy-dom
import React from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { createRoot } from "react-dom/client";
import { act } from "react";
async function render(element: React.ReactNode): Promise<string> { const container = document.createElement("div"); const root = createRoot(container); await act(async () => root.render(element)); const html = container.innerHTML; await act(async () => root.unmount()); return html; }
import { MarketplaceService, registerMarketplaceCommands, useMarketplaceStore, type Snapshot } from "./service";
import { MarketplaceBrowser, MarketplaceDetails, MarketplaceActivity } from "./panels";
import { useNodeRegistryStore } from "../workflow/stores/node-registry-store";
import { commandPaletteService } from "../../services/command-palette";
import { useWorkspaceStore } from "../../workspace/store";
import { cloneDefaultLayout } from "../../workspace/layouts";
import { collectPanelIds, layoutStorageKey } from "../../workspace/persistence";

const manifest = { plugin_id: "test.package", plugin_name: "Test Package", version: "1.0.0", author: "Test", description: "Test package", license: "MIT", entry_point: "bin/workflow.json", permissions: [{ name: "PERM-NETWORK-OUTBOUND", level: "Elevated", required: true }], capabilities: [{ capability: "Workflow", enabled: true }], compatibility: { api_version: "1.0.0" } };
const snapshot = (revision = 1): Snapshot => ({ source: "Local Development Registry", scope: "User", trust: "Development", revision, installed: [], available: [{ manifest, compatible: true }], registrations: [], audit: [] });
beforeEach(() => { useMarketplaceStore.setState({ snapshot: null, selected: null, review: null, view: "Discover", query: "", busy: false, error: null }); useNodeRegistryStore.getState().reset(); });
describe("Marketplace", () => {
  it("renders activity while the initial snapshot is unavailable", async () => { expect(await render(<MarketplaceActivity/>)).toContain("Package activity"); });
  it("shows the selected version digest when another version is installed", async () => {
    const state = snapshot();
    state.available = [{ manifest: { ...manifest, version: "1.1.0" }, compatible: true, digest: "selected-digest" }];
    state.installed = [{ installation: { manifest, digest: "old-digest", enabled: true, approvedPermissions: manifest.permissions, source: "Local", acquiredAt: "2026-09-06" }, health: "healthy" }];
    useMarketplaceStore.setState({ snapshot: state, selected: state.available[0]!.manifest! });
    const html = await render(<MarketplaceDetails/>);
    expect(html).toContain("selected-digest"); expect(html).not.toContain("old-digest");
  });
  it("shows explicit browser backend unavailability", async () => { await new MarketplaceService().refresh(); expect(useMarketplaceStore.getState().error?.code).toBe("MARKETPLACE_UNAVAILABLE"); });
  it("renders actual registry and permission metadata", async () => { useMarketplaceStore.setState({ snapshot: snapshot(), selected: manifest }); const html = await render(<><MarketplaceBrowser/><MarketplaceDetails/></>); expect(html).toContain("Local Development Registry"); expect(html).toContain("PERM-NETWORK-OUTBOUND"); expect(html).toContain("Validate &amp; review package"); expect(html).not.toContain("Verified"); });
  it("renders empty, unavailable and updates states", async () => { useMarketplaceStore.setState({ snapshot: { ...snapshot(), available: [], providerError: { code: "MARKETPLACE_UNAVAILABLE", message: "Registry offline" } }, view: "Updates" }); const html = await render(<MarketplaceBrowser/>); expect(html).toContain("No updates packages"); expect(html).toContain("Registry offline"); });
  it("uses backend search and ignores late responses", async () => {
    const resolvers: ((s: Snapshot) => void)[] = [];
    const request = vi.fn(() => new Promise<Snapshot>((resolve) => resolvers.push(resolve)));
    const service = new MarketplaceService(request as <T>() => Promise<T>);
    const first = service.refresh(); useMarketplaceStore.setState({ query: "new" }); const second = service.refresh();
    resolvers[1]!({ ...snapshot(2), source: "Newest" }); await second; resolvers[0]!(snapshot(1)); await first;
    expect(useMarketplaceStore.getState().snapshot?.source).toBe("Newest"); expect(request).toHaveBeenLastCalledWith("snapshot", { query: "new" });
  });
  it("reconciles only its owned plugin registrations", async () => {
    const reg = { nodeId: "p.node", typeName: "p.echo", label: "Echo", category: "plugin" as const, description: "", inputs: [], outputs: [], parameters: {}, version: "1.0.0", pluginId: "p", capabilities: [] };
    let state = { ...snapshot(), registrations: [reg] };
    const service = new MarketplaceService((async () => state) as <T>() => Promise<T>);
    useNodeRegistryStore.getState().registerNode({ ...reg, nodeId: "other.node", pluginId: "other", typeName: "other.echo" });
    await service.refresh(); await service.refresh(); expect(useNodeRegistryStore.getState().getAllRegistrations()).toHaveLength(2);
    state = { ...snapshot(2), registrations: [] }; await service.refresh(); expect(useNodeRegistryStore.getState().getAllRegistrations().map((r) => r.pluginId)).toEqual(["other"]);
  });
  it("requires explicit mutation and sends exact reviewed grants", async () => {
    const review = { reviewId: "review-exact", manifest, digest: "digest", source: "Local", trust: "Development" };
    const request = vi.fn(async (command: string) => command === "inspect" ? review : snapshot());
    const service = new MarketplaceService(request as <T>(command: string) => Promise<T>);
    await service.inspect(manifest); expect(request).toHaveBeenCalledTimes(1); await service.mutate("install");
    expect(request).toHaveBeenLastCalledWith("install", expect.objectContaining({ reviewId: review.reviewId, approvedPermissions: manifest.permissions, requestId: expect.any(String) }));
  });
  it("surfaces structured errors without fabricating installed state", async () => { const service = new MarketplaceService(async () => { throw { code: "PERMISSION_DENIED", message: "Review required" }; }); await service.mutate("enable", "p"); expect(useMarketplaceStore.getState().snapshot).toBeNull(); expect(useMarketplaceStore.getState().error?.code).toBe("PERMISSION_DENIED"); expect(useMarketplaceStore.getState().busy).toBe(false); });
  it("registers central commands and independent layout", () => { registerMarketplaceCommands(); commandPaletteService.execute("marketplace.installed"); expect(useWorkspaceStore.getState().activeWorkspace).toBe("marketplace"); expect(useMarketplaceStore.getState().view).toBe("Installed"); expect(layoutStorageKey("marketplace")).toBe("atlas.layout.marketplace.v1"); expect(collectPanelIds(cloneDefaultLayout("marketplace"))).toEqual(["marketplace.browser", "marketplace.details", "marketplace.activity"]); });
});
