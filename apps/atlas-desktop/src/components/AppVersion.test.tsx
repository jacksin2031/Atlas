// @vitest-environment happy-dom
import React, { act } from "react";
import { createRoot } from "react-dom/client";
import { describe, expect, it, vi } from "vitest";
import { getVersion } from "@tauri-apps/api/app";
import { AppVersion } from "./AppVersion";

vi.mock("@tauri-apps/api/app", () => ({ getVersion: vi.fn() }));
(globalThis as typeof globalThis & { IS_REACT_ACT_ENVIRONMENT: boolean }).IS_REACT_ACT_ENVIRONMENT = true;
async function renderVersion() {
  const container = document.createElement("div"), root = createRoot(container);
  await act(async () => root.render(<AppVersion />));
  const text = container.textContent;
  act(() => root.unmount());
  return text;
}
describe("installed application version", () => {
  it("uses the version returned by the executable", async () => {
    vi.mocked(getVersion).mockResolvedValue("9.8.7-beta");
    expect(await renderVersion()).toBe("Atlas v9.8.7-beta");
  });
  it("does not invent a version when native metadata is unavailable", async () => {
    vi.mocked(getVersion).mockRejectedValue(new Error("IPC unavailable"));
    expect(await renderVersion()).toBe("Atlas · version unavailable");
  });
});
