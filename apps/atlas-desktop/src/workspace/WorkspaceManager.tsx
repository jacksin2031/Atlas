import React, { useCallback, useEffect, useState } from "react";
import { ContextMenuBuilder, Layout, Model, showPopupMenu, type TabNode, type TabSetNode, type BorderNode } from "flexlayout-react";
import "flexlayout-react/style/combined.css";
import { EmptyState, Icon } from "../design-system";
import { useThemeStore } from "../stores";
import { getAllowedPanelIds, getPanelDefinition, getWorkspacePanels, panelDefinitions } from "./panel-registry";
import { loadWorkspaceLayout, resetWorkspaceLayout, saveWorkspaceLayout } from "./persistence";
import { useWorkspaceStore } from "./store";
import { workspaceService } from "./service";
import type { WorkspaceId } from "./types";

const createModel = (id: WorkspaceId): Model => Model.fromJson(loadWorkspaceLayout(id, getAllowedPanelIds(id)));
export const WorkspaceManager: React.FC = () => {
  const active = useWorkspaceStore((s) => s.activeWorkspace); const theme = useThemeStore((s) => s.resolvedTheme);
  const [models, setModels] = useState<Record<WorkspaceId, Model>>(() => ({ workflow: createModel("workflow"), vision: createModel("vision") }));
  const reset = useCallback((id: WorkspaceId) => { const model = Model.fromJson(resetWorkspaceLayout(id)); setModels((current) => ({ ...current, [id]: model })); }, []);
  useEffect(() => { workspaceService.registerPanels(panelDefinitions); (Object.keys(models) as WorkspaceId[]).forEach((id) => workspaceService.registerModel(id, models[id], () => reset(id))); }, [models, reset]);
  const factory = useCallback((node: TabNode) => { const definition = getPanelDefinition(node.getComponent() ?? ""); if (!definition) return <EmptyState title="Panel unavailable" description={`The panel '${node.getComponent()}' is not registered.`}/>; return React.createElement(definition.component); }, []);
  const onContextMenu = useCallback((node: TabNode | TabSetNode | BorderNode, event: React.MouseEvent) => { event.preventDefault(); const builder = new ContextMenuBuilder(node).add("maximize").addDivider().add("closeOthers").add("close"); builder.addDivider(); getWorkspacePanels(active).forEach((panel) => builder.addCustom({ key: `open-${panel.id}`, label: `Open ${panel.title}`, onSelect: () => workspaceService.openPanel(panel.id) })); showPopupMenu({ anchor: { x: event.clientX, y: event.clientY }, items: builder.build(), onClose: () => undefined }); }, [active]);
  const model = models[active];
  return <div className={`workspace-manager flexlayout__theme_${theme === "dark" ? "dark" : "light"}`}><Layout key={`${active}-${model.getRootRow()?.getId()}`} model={model} factory={factory} realtimeResize onModelChange={(changed) => saveWorkspaceLayout(active, changed.toJson())} onContextMenu={onContextMenu} supportsPopout={false} onRenderTab={(node, values) => { const icon = getPanelDefinition(node.getComponent() ?? "")?.icon; if (icon) values.leading = <Icon name={icon} size={13}/>; }}/></div>;
};
