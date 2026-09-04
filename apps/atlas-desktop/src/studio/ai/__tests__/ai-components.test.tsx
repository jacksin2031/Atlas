// @vitest-environment happy-dom

import React, { act } from "react";
import { createRoot } from "react-dom/client";
import { beforeEach, describe, expect, it } from "vitest";
import {
  AIAgentInspector,
  AIContextInspector,
  AIEditor,
  AIModelBrowser,
  AIProviderPanel,
} from "../components";
import { createNormalizedRequest } from "../service";
import { useAIStudioStore } from "../store";
import type { AIModelDescriptor, AIProviderDescriptor } from "../types";

const provider = (connectionState: AIProviderDescriptor["connectionState"] = "disconnected"): AIProviderDescriptor => ({
  providerId: "provider-1", name: "OpenAI", providerType: "openai-compatible", version: "1",
  capabilities: ["chat", "streaming"], health: connectionState === "connected" ? "healthy" : "unhealthy",
  connectionState, enabled: true,
});
const model = (): AIModelDescriptor => ({
  modelId: "model-1", name: "Model", providerId: "provider-1", version: "1",
  capabilities: ["chat", "streaming"], state: "ready",
});

const render = (element: React.ReactNode): string => {
  const container = document.createElement("div");
  document.body.append(container);
  const root = createRoot(container);
  act(() => root.render(element));
  const markup = container.innerHTML;
  act(() => root.unmount());
  container.remove();
  return markup;
};

(globalThis as typeof globalThis & { IS_REACT_ACT_ENVIRONMENT: boolean }).IS_REACT_ACT_ENVIRONMENT = true;

describe("AI Studio resilient rendering", () => {
  beforeEach(() => useAIStudioStore.setState({
    runtimeHealth: "unhealthy", loading: false, mode: "playground", providers: [], models: [],
    selectedProviderId: null, selectedModelId: null, systemPrompt: "", userInput: "test",
    messages: [], contexts: [], memories: [], tools: [], agents: [], events: [], metrics: {},
    lastRequest: null, lastResponse: null, streamContent: "", error: null, running: false,
    streaming: false, startedAt: null,
  }));

  it("renders the Playground when the AI Runtime is unhealthy", () => {
    expect(render(<AIEditor />)).toContain("normalized Runtime response");
  });

  it("renders a controlled empty state for an empty provider list", () => {
    expect(render(<AIProviderPanel />)).toContain("No AI providers discovered");
  });

  it("renders a disconnected provider without crashing", () => {
    useAIStudioStore.setState({ providers: [provider()], selectedProviderId: "provider-1" });
    expect(render(<AIProviderPanel />)).toContain("disconnected");
  });

  it("renders a missing model selection without crashing", () => {
    useAIStudioStore.setState({ providers: [provider()], selectedProviderId: "provider-1", selectedModelId: null });
    expect(render(<AIEditor />)).toContain("Select model");
  });

  it("renders a controlled empty state for an empty model list", () => {
    useAIStudioStore.setState({ providers: [provider()], selectedProviderId: "provider-1", models: [] });
    expect(render(<AIModelBrowser />)).toContain("No models discovered");
  });

  it("renders the Agent Inspector without an unstable Zustand snapshot", () => {
    useAIStudioStore.setState({ mode: "agent", events: [{ eventId: "e1", eventType: "agent_started", timestamp: "2026-09-04T00:00:00Z" }] });
    expect(render(<AIAgentInspector />)).toContain("Agent Started");
  });

  it("visibly marks a stale Knowledge reference and excludes it from inference", () => {
    useAIStudioStore.setState({
      providers: [provider("connected")], models: [model()], selectedProviderId: "provider-1", selectedModelId: "model-1",
      contexts: [{
        id: "knowledge:project-a:deleted", kind: "knowledge", label: "Deleted entry", preview: undefined,
        includedInRequest: false, availability: "missing", unavailableReason: "Knowledge entry is missing or unavailable.",
        metadata: { knowledgeReference: { entryId: "deleted", projectId: "project-a" } },
      }],
    });
    expect(render(<AIContextInspector />)).toContain("Missing / unavailable");
    expect(createNormalizedRequest()?.contextReferences).toEqual([]);
  });

  it("renders the Playground with unhealthy runtime, no providers or models, and stale context", () => {
    useAIStudioStore.setState({ contexts: [{ id: "knowledge:project-a:deleted", kind: "knowledge", label: "Deleted entry", availability: "missing", includedInRequest: false }] });
    const markup = render(<AIEditor />);
    expect(markup).toContain("Select provider");
    expect(markup).toContain("Missing / unavailable");
  });
});
