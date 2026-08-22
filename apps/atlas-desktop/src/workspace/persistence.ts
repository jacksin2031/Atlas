import type { IJsonModel } from "flexlayout-react";
import { cloneDefaultLayout, REQUIRED_PANELS } from "./layouts";
import type { WorkspaceId } from "./types";

export const LAYOUT_VERSION = 1;
export const layoutStorageKey = (workspace: WorkspaceId): string => `atlas.layout.${workspace}.v${LAYOUT_VERSION}`;

interface PersistedLayout { version: number; workspace: WorkspaceId; layout: IJsonModel }

export function collectPanelIds(value: unknown): string[] {
  if (!value || typeof value !== "object") return [];
  const node = value as Record<string, unknown>;
  const own = node.type === "tab" && typeof node.component === "string" ? [node.component] : [];
  const children = Array.isArray(node.children) ? node.children.flatMap(collectPanelIds) : [];
  const borders = Array.isArray(node.borders) ? node.borders.flatMap(collectPanelIds) : [];
  const layout = node.layout ? collectPanelIds(node.layout) : [];
  return [...own, ...children, ...borders, ...layout];
}

export function validateLayout(layout: unknown, workspace: WorkspaceId, allowedPanels: ReadonlySet<string>): layout is IJsonModel {
  if (!layout || typeof layout !== "object" || !("layout" in layout)) return false;
  const ids = collectPanelIds(layout);
  if (ids.length === 0 || !ids.includes(REQUIRED_PANELS[workspace])) return false;
  if (new Set(ids).size !== ids.length) return false;
  return ids.every((id) => allowedPanels.has(id));
}

export function loadWorkspaceLayout(workspace: WorkspaceId, allowedPanels: ReadonlySet<string>, storage: Pick<Storage, "getItem"> = localStorage): IJsonModel {
  try {
    const raw = storage.getItem(layoutStorageKey(workspace));
    if (!raw) return cloneDefaultLayout(workspace);
    const parsed = JSON.parse(raw) as PersistedLayout;
    if (parsed.version !== LAYOUT_VERSION || parsed.workspace !== workspace || !validateLayout(parsed.layout, workspace, allowedPanels)) return cloneDefaultLayout(workspace);
    return parsed.layout;
  } catch {
    return cloneDefaultLayout(workspace);
  }
}

export function saveWorkspaceLayout(workspace: WorkspaceId, layout: IJsonModel, storage: Pick<Storage, "setItem"> = localStorage): void {
  try { storage.setItem(layoutStorageKey(workspace), JSON.stringify({ version: LAYOUT_VERSION, workspace, layout } satisfies PersistedLayout)); } catch { /* storage is optional */ }
}

export function resetWorkspaceLayout(workspace: WorkspaceId, storage: Pick<Storage, "removeItem"> = localStorage): IJsonModel {
  try { storage.removeItem(layoutStorageKey(workspace)); } catch { /* storage is optional */ }
  return cloneDefaultLayout(workspace);
}
