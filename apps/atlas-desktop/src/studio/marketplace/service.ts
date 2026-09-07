import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import { create } from "zustand";
import { useNodeRegistryStore } from "../workflow/stores/node-registry-store";
import type { PluginNodeRegistration } from "../workflow/types";
import { commandPaletteService } from "../../services/command-palette";
import { workspaceService } from "../../workspace/service";

export interface Permission { name: string; level: string; required: boolean }
export interface Manifest {
  plugin_id: string; plugin_name: string; version: string; description: string; author: string; license: string;
  entry_point: string; permissions: Permission[]; capabilities: { capability: string; enabled: boolean }[];
  compatibility: Record<string, string | null>;
}
export interface PackageError { code: string; message: string }
export interface Available { manifest?: Manifest; digest?: string; compatible: boolean; pluginId?: string; version?: string; error?: PackageError }
export interface Installation { manifest: Manifest; digest: string; enabled: boolean; approvedPermissions: Permission[]; source: string; acquiredAt: string }
export interface Installed { installation: Installation; health: string; error?: PackageError; update?: Available }
export interface Snapshot {
  source: string; scope: string; trust: string; available: Available[]; installed: Installed[];
  registrations: PluginNodeRegistration[]; providerError?: PackageError; revision: number;
  audit: { action: string; pluginId: string; requestId: string; timestamp: string; revision: number }[];
}
export interface Review { reviewId: string; manifest: Manifest; digest: string; source: string; trust: string }
export type View = "Discover" | "Installed" | "Updates";
interface MarketplaceState {
  snapshot: Snapshot | null; review: Review | null; selected: Manifest | null; view: View;
  query: string; busy: boolean; error: PackageError | null;
}
export const useMarketplaceStore = create<MarketplaceState>(() => ({ snapshot: null, review: null, selected: null, view: "Discover", query: "", busy: false, error: null }));

export class MarketplaceService {
  private sequence = 0;
  private owners = new Set<string>();
  constructor(private request: <T>(command: string, payload: Record<string, unknown>) => Promise<T> = (command, payload) => {
    if (!("__TAURI_INTERNALS__" in window)) return Promise.reject({ code: "MARKETPLACE_UNAVAILABLE", message: "Marketplace backend unavailable. Run Atlas Desktop to manage plugins." });
    return invoke("marketplace_request", { command, payload });
  }) {}
  private report(error: unknown): void {
    const value = error && typeof error === "object" && "code" in error && "message" in error ? error as PackageError : { code: "MARKETPLACE_UNAVAILABLE", message: error instanceof Error ? error.message : String(error) };
    useMarketplaceStore.setState({ error: value });
  }
  private apply(snapshot: Snapshot): void {
    const current = useMarketplaceStore.getState().snapshot;
    if (current && snapshot.revision < current.revision) return;
    const registry = useNodeRegistryStore.getState();
    for (const owner of this.owners) registry.hotReload(owner);
    for (const registration of snapshot.registrations) registry.registerNode(registration);
    this.owners = new Set(snapshot.registrations.map((r) => r.pluginId));
    useMarketplaceStore.setState({ snapshot });
  }
  async refresh(): Promise<void> {
    const sequence = ++this.sequence;
    try {
      const snapshot = await this.request<Snapshot>("snapshot", { query: useMarketplaceStore.getState().query });
      if (sequence === this.sequence) { this.apply(snapshot); useMarketplaceStore.setState({ error: null }); }
    } catch (error) { if (sequence === this.sequence) this.report(error); }
  }
  async inspect(manifest?: Manifest): Promise<void> {
    if (useMarketplaceStore.getState().busy) return;
    useMarketplaceStore.setState({ busy: true, review: null, selected: manifest ?? null, error: null });
    try {
      const review = await this.request<Review | null>(manifest ? "inspect" : "inspect_local", manifest ? { pluginId: manifest.plugin_id, version: manifest.version } : {});
      useMarketplaceStore.setState({ review, selected: review?.manifest ?? manifest ?? null });
    } catch (error) { this.report(error); }
    finally { useMarketplaceStore.setState({ busy: false }); }
  }
  async mutate(command: "install" | "enable" | "disable" | "uninstall", pluginId?: string): Promise<void> {
    const state = useMarketplaceStore.getState();
    if (state.busy) return;
    ++this.sequence;
    useMarketplaceStore.setState({ busy: true, error: null });
    try {
      const payload = command === "install" ? { reviewId: state.review?.reviewId, approvedPermissions: state.review?.manifest.permissions } : { pluginId };
      const snapshot = await this.request<Snapshot>(command, { ...payload, requestId: crypto.randomUUID() });
      this.apply(snapshot); useMarketplaceStore.setState({ review: null });
    } catch (error) { this.report(error); }
    finally { useMarketplaceStore.setState({ busy: false }); }
  }
  async connect(): Promise<() => void> {
    if (!("__TAURI_INTERNALS__" in window)) { await this.refresh(); return () => undefined; }
    const stop = await listen<{ revision: number }>("plugin://marketplace-changed", ({ payload }) => {
      if (payload.revision > (useMarketplaceStore.getState().snapshot?.revision ?? -1)) void this.refresh();
    });
    await this.refresh(); return stop;
  }
}
export const marketplaceService = new MarketplaceService();
export function openMarketplace(view: View = "Discover"): void { useMarketplaceStore.setState({ view }); workspaceService.switchWorkspace("marketplace"); }
export function registerMarketplaceCommands(): void {
  const commands: [string, string, () => void][] = [
    ["open", "Open Marketplace", () => openMarketplace()],
    ["search", "Search Marketplace", () => { openMarketplace(); workspaceService.openPanel("marketplace.browser"); }],
    ["installed", "Show Installed Plugins", () => openMarketplace("Installed")],
    ["updates", "Check for Plugin Updates", () => { openMarketplace("Updates"); void marketplaceService.refresh(); }],
    ["local", "Install Local Plugin", () => { openMarketplace(); void marketplaceService.inspect(); }],
    ["refresh", "Refresh Marketplace", () => void marketplaceService.refresh()],
  ];
  commands.forEach(([id, label, handler]) => commandPaletteService.register({ id: `marketplace.${id}`, label, category: "Marketplace", handler, description: label }));
}
