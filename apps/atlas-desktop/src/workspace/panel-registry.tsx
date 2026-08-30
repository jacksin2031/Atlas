import React from "react";
import { ProjectExplorerPanel, ConsolePanel, ProblemsPanel, OutputPanel } from "../components/panels";
import { WorkflowCanvasView } from "../components/layouts/WorkflowCanvasView";
import { InspectorPanel } from "../components/layouts/InspectorPanel";
import { NodePalette } from "../studio/workflow/components/sidebar/node-palette";
import { VariableManager } from "../studio/workflow/components/variables/variable-manager";
import { DebuggerPanel } from "../studio/workflow/components/toolbar/debugger-panel";
import { ColorPanel, DetectionPanel, OcrPanel, TemplatePanel, TimelinePanel, VisionCanvas, VisionProperties, VisionToolbox } from "../studio/vision";
import { AIContextInspector, AIEditor, AIEventsPanel, AIMemoryPanel, AIMetricsPanel, AIModelBrowser, AIPromptComparisonPanel, AIProviderPanel, AIRequestInspector, AIResponseInspector, AIRetrievalPanel, AISessionsPanel, AIToolsPanel } from "../studio/ai";
import type { PanelDefinition, WorkspaceId } from "./types";

const fill = (Component: React.ComponentType): React.FC => function PanelFill() { return <div className="panel-fill"><Component/></div>; };
export const panelDefinitions: readonly PanelDefinition[] = [
  { id: "shared.project-explorer", title: "Project Explorer", workspace: "shared", component: fill(ProjectExplorerPanel), closable: true, dockable: true, defaultTabset: "workflow-left", icon: "folder" },
  { id: "shared.console", title: "Console", workspace: "shared", component: fill(ConsolePanel), closable: true, dockable: true, defaultTabset: "workflow-bottom" },
  { id: "shared.problems", title: "Problems", workspace: "shared", component: fill(ProblemsPanel), closable: true, dockable: true, defaultTabset: "workflow-bottom" },
  { id: "shared.output", title: "Output", workspace: "shared", component: fill(OutputPanel), closable: true, dockable: true, defaultTabset: "workflow-bottom" },
  { id: "workflow.node-palette", title: "Node Palette", workspace: "workflow", component: fill(NodePalette), closable: true, dockable: true, defaultTabset: "workflow-left", icon: "workflow" },
  { id: "workflow.canvas", title: "Workflow Canvas", workspace: "workflow", component: fill(WorkflowCanvasView), closable: false, dockable: true, defaultTabset: "workflow-center", icon: "workflow" },
  { id: "workflow.properties", title: "Properties", workspace: "workflow", component: fill(InspectorPanel), closable: true, dockable: true, defaultTabset: "workflow-right" },
  { id: "workflow.variables", title: "Variables", workspace: "workflow", component: fill(VariableManager), closable: true, dockable: true, defaultTabset: "workflow-bottom" },
  { id: "workflow.debugger", title: "Debugger", workspace: "workflow", component: fill(DebuggerPanel), closable: true, dockable: true, defaultTabset: "workflow-bottom" },
  { id: "vision.toolbox", title: "Vision Toolbox", workspace: "vision", component: fill(VisionToolbox), closable: false, dockable: true, defaultTabset: "vision-left", icon: "vision" },
  { id: "vision.canvas", title: "Vision Canvas", workspace: "vision", component: fill(VisionCanvas), closable: false, dockable: true, defaultTabset: "vision-center", icon: "vision" },
  { id: "vision.properties", title: "Vision Properties", workspace: "vision", component: fill(VisionProperties), closable: true, dockable: true, defaultTabset: "vision-right" },
  { id: "vision.ocr", title: "OCR", workspace: "vision", component: fill(OcrPanel), closable: true, dockable: true, defaultTabset: "vision-bottom" },
  { id: "vision.detection", title: "Detection", workspace: "vision", component: fill(DetectionPanel), closable: true, dockable: true, defaultTabset: "vision-bottom" },
  { id: "vision.color", title: "Color", workspace: "vision", component: fill(ColorPanel), closable: true, dockable: true, defaultTabset: "vision-bottom" },
  { id: "vision.template", title: "Template", workspace: "vision", component: fill(TemplatePanel), closable: true, dockable: true, defaultTabset: "vision-bottom" },
  { id: "vision.timeline", title: "Timeline", workspace: "vision", component: fill(TimelinePanel), closable: true, dockable: true, defaultTabset: "vision-bottom" },
  { id: "ai.providers", title: "Providers", workspace: "ai", component: fill(AIProviderPanel), closable: false, dockable: true, defaultTabset: "ai-left", icon: "ai" },
  { id: "ai.models", title: "Models", workspace: "ai", component: fill(AIModelBrowser), closable: true, dockable: true, defaultTabset: "ai-left", icon: "ai" },
  { id: "ai.sessions", title: "Sessions", workspace: "ai", component: fill(AISessionsPanel), closable: true, dockable: true, defaultTabset: "ai-left" },
  { id: "ai.editor", title: "AI Playground", workspace: "ai", component: fill(AIEditor), closable: false, dockable: true, defaultTabset: "ai-center", icon: "ai" },
  { id: "ai.context", title: "Context", workspace: "ai", component: fill(AIContextInspector), closable: false, dockable: true, defaultTabset: "ai-right" },
  { id: "ai.request", title: "Request", workspace: "ai", component: fill(AIRequestInspector), closable: true, dockable: true, defaultTabset: "ai-right" },
  { id: "ai.response", title: "Response", workspace: "ai", component: fill(AIResponseInspector), closable: true, dockable: true, defaultTabset: "ai-right" },
  { id: "ai.tools", title: "Tools", workspace: "ai", component: fill(AIToolsPanel), closable: true, dockable: true, defaultTabset: "ai-bottom" },
  { id: "ai.memory", title: "Memory", workspace: "ai", component: fill(AIMemoryPanel), closable: true, dockable: true, defaultTabset: "ai-bottom" },
  { id: "ai.retrieval", title: "Retrieval", workspace: "ai", component: fill(AIRetrievalPanel), closable: true, dockable: true, defaultTabset: "ai-bottom" },
  { id: "ai.metrics", title: "Metrics", workspace: "ai", component: fill(AIMetricsPanel), closable: true, dockable: true, defaultTabset: "ai-bottom" },
  { id: "ai.events", title: "Events", workspace: "ai", component: fill(AIEventsPanel), closable: true, dockable: true, defaultTabset: "ai-bottom" },
  { id: "ai.comparison", title: "Comparison", workspace: "ai", component: fill(AIPromptComparisonPanel), closable: true, dockable: true, defaultTabset: "ai-bottom" },
] as const;

const byId = new Map(panelDefinitions.map((panel) => [panel.id, panel]));
export const getPanelDefinition = (id: string): PanelDefinition | undefined => byId.get(id);
export const getWorkspacePanels = (workspace: WorkspaceId): PanelDefinition[] => panelDefinitions.filter((panel) => panel.workspace === "shared" || panel.workspace === workspace).map((panel) => panel.workspace === "shared" ? { ...panel, defaultTabset: `${workspace}-${panel.id === "shared.project-explorer" ? "left" : "bottom"}` } : panel);
export const getAllowedPanelIds = (workspace: WorkspaceId): ReadonlySet<string> => new Set(getWorkspacePanels(workspace).map((panel) => panel.id));
