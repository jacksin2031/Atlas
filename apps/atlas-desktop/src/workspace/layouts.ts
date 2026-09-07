import type { IJsonModel, IJsonTabNode } from "flexlayout-react";
import type { WorkspaceId } from "./types";

const tab = (id: string, name: string, enableClose = true): IJsonTabNode => ({ type: "tab", id, component: id, name, enableClose, enableRename: false });

const global = {
  enableEdgeDock: true,
  enableEdgeDockIndicators: true,
  tabEnableClose: true,
  tabEnableDrag: true,
  tabEnableRename: false,
  tabSetEnableDivide: true,
  tabSetEnableMaximize: true,
  tabSetMinWidth: 120,
  tabSetMinHeight: 80,
  splitterSize: 5,
};

export const DEFAULT_LAYOUTS: Record<WorkspaceId, IJsonModel> = {
  marketplace: {
    global, borders: [], layout: { type: "row", children: [
      { type: "tabset", id: "marketplace-center", weight: 58, enableDeleteWhenEmpty: false, children: [tab("marketplace.browser", "Marketplace", false)] },
      { type: "row", weight: 42, children: [
        { type: "tabset", id: "marketplace-right", weight: 75, children: [tab("marketplace.details", "Plugin Details", false)] },
        { type: "tabset", id: "marketplace-bottom", weight: 25, children: [tab("marketplace.activity", "Package Activity")] },
      ] },
    ] },
  },
  workflow: {
    global,
    borders: [],
    layout: { type: "row", children: [
      { type: "tabset", id: "workflow-left", weight: 18, selected: 1, children: [
        tab("shared.project-explorer", "Project Explorer"), tab("workflow.node-palette", "Node Palette"),
      ]},
      { type: "row", weight: 62, children: [
        { type: "tabset", id: "workflow-center", weight: 72, enableDeleteWhenEmpty: false, children: [tab("workflow.canvas", "Workflow Canvas", false)] },
        { type: "tabset", id: "workflow-bottom", weight: 28, selected: 0, children: [
          tab("workflow.variables", "Variables"), tab("shared.console", "Console"), tab("shared.problems", "Problems"), tab("workflow.debugger", "Debugger"), tab("shared.output", "Output"),
        ]},
      ]},
      { type: "tabset", id: "workflow-right", weight: 20, children: [tab("workflow.properties", "Properties")] },
    ]},
  },
  vision: {
    global,
    borders: [],
    layout: { type: "row", children: [
      { type: "tabset", id: "vision-left", weight: 17, children: [
        tab("vision.toolbox", "Vision Toolbox", false), tab("shared.project-explorer", "Project Explorer"),
      ]},
      { type: "row", weight: 63, children: [
        { type: "tabset", id: "vision-center", weight: 70, enableDeleteWhenEmpty: false, children: [tab("vision.canvas", "Vision Canvas", false)] },
        { type: "tabset", id: "vision-bottom", weight: 30, selected: 0, children: [
          tab("vision.ocr", "OCR"), tab("vision.detection", "Detection"), tab("vision.color", "Color"), tab("vision.template", "Template"), tab("vision.timeline", "Timeline"), tab("shared.console", "Console"), tab("shared.output", "Output"), tab("shared.problems", "Problems"),
        ]},
      ]},
      { type: "tabset", id: "vision-right", weight: 20, children: [tab("vision.properties", "Vision Properties")] },
    ]},
  },
  ai: {
    global,
    borders: [],
    layout: { type: "row", children: [
      { type: "tabset", id: "ai-left", weight: 18, selected: 0, children: [
        tab("ai.providers", "Providers", false), tab("ai.models", "Models"), tab("ai.sessions", "Sessions"),
      ]},
      { type: "row", weight: 62, children: [
        { type: "tabset", id: "ai-center", weight: 70, enableDeleteWhenEmpty: false, children: [tab("ai.editor", "AI Playground", false)] },
        { type: "tabset", id: "ai-bottom", weight: 30, selected: 0, children: [
          tab("shared.console", "Console"), tab("ai.tools", "Tools"), tab("ai.memory", "Memory"), tab("ai.retrieval", "Retrieval"), tab("ai.metrics", "Metrics"), tab("ai.events", "Events"), tab("ai.comparison", "Comparison"), tab("shared.problems", "Problems"),
        ]},
      ]},
      { type: "tabset", id: "ai-right", weight: 20, selected: 0, children: [
        tab("ai.context", "Context", false), tab("ai.request", "Request"), tab("ai.response", "Response"),
      ]},
    ]},
  },
  knowledge: {
    global,
    borders: [],
    layout: { type: "row", children: [
      { type: "tabset", id: "knowledge-left", weight: 20, enableDeleteWhenEmpty: false, children: [
        tab("knowledge.explorer", "Knowledge Explorer", false), tab("shared.project-explorer", "Project Explorer"),
      ]},
      { type: "row", weight: 58, children: [
        { type: "tabset", id: "knowledge-center", weight: 68, enableDeleteWhenEmpty: false, children: [tab("knowledge.editor", "Knowledge Editor", false)] },
        { type: "tabset", id: "knowledge-bottom", weight: 32, selected: 0, children: [
          tab("knowledge.search", "Search"), tab("knowledge.retrieval", "Retrieval"), tab("knowledge.activity", "Activity"), tab("knowledge.health", "Health"), tab("shared.console", "Console"), tab("shared.problems", "Problems"),
        ]},
      ]},
      { type: "tabset", id: "knowledge-right", weight: 22, selected: 0, children: [
        tab("knowledge.metadata", "Metadata & Provenance", false), tab("knowledge.import", "Import"),
      ]},
    ]},
  },
};

export const REQUIRED_PANELS: Record<WorkspaceId, string> = { workflow: "workflow.canvas", vision: "vision.canvas", ai: "ai.editor", knowledge: "knowledge.editor", marketplace: "marketplace.browser" };

export function cloneDefaultLayout(id: WorkspaceId): IJsonModel {
  return structuredClone(DEFAULT_LAYOUTS[id]);
}
