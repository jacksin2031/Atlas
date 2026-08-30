import { describe, expect, it } from "vitest";
import { assertCredentialFree, interruptRecoverableRuns } from "../../../../services/project-assets";
import type { WorkflowRun } from "../../types";

const run = (status: WorkflowRun["status"]): WorkflowRun => ({
  id: `run-${status}`, workflowId: "workflow", status, nodeStates: {}, variables: {}, errors: [],
  metrics: { totalNodes: 1, completedNodes: 0, failedNodes: 0, duration: 0, throughput: 0 },
});

describe("project asset hardening", () => {
  it("rejects credential-shaped fields but permits token usage metrics", () => {
    expect(() => assertCredentialFree({ provider: { apiKey: "must-not-persist" } })).toThrow(/apiKey/);
    expect(() => assertCredentialFree({ metrics: { inputTokens: 12, totalTokens: 20 } })).not.toThrow();
  });

  it("restores non-terminal workflow runs as explicitly interrupted", () => {
    const restored = interruptRecoverableRuns({ active: run("running"), done: run("completed") });
    expect(restored.active?.status).toBe("interrupted");
    expect(restored.active?.errors.at(-1)?.errorCode).toBe("INTERRUPTED");
    expect(restored.done?.status).toBe("completed");
  });
});
