// @vitest-environment happy-dom
import React, { act } from "react";
import { createRoot } from "react-dom/client";
import { afterEach, describe, expect, it, vi } from "vitest";
import { MenuBar } from "./MenuBar";

const { execute } = vi.hoisted(() => ({ execute: vi.fn() }));
vi.mock("../../services", () => ({ commandPaletteService: { execute } }));
vi.mock("../../stores", () => ({
  useThemeStore: (select: (state: { resolvedTheme: string }) => unknown) => select({ resolvedTheme: "dark" }),
}));
vi.mock("../../workspace", () => ({
  getWorkspacePanels: () => [],
  useWorkspaceStore: (select: (state: { activeWorkspace: string }) => unknown) => select({ activeWorkspace: "workflow" }),
  workspaceService: {
    openPanel: vi.fn(),
    switchWorkspace: vi.fn(),
    resetActiveLayout: vi.fn(),
  },
}));

const mounted: Array<() => void> = [];
function renderMenu() {
  const container = document.createElement("div");
  document.body.appendChild(container);
  const root = createRoot(container);
  act(() => root.render(<MenuBar onToggleCommandPalette={vi.fn()}/>));
  mounted.push(() => {
    act(() => root.unmount());
    container.remove();
  });
  return container;
}
afterEach(() => {
  while (mounted.length) mounted.pop()?.();
  vi.clearAllMocks();
});

describe("MenuBar keyboard accessibility", () => {
  it("moves ArrowUp from a menu trigger to the last enabled item", async () => {
    const container = renderMenu();
    const file = Array.from(container.querySelectorAll("button")).find((button) => button.textContent === "File");
    expect(file).toBeTruthy();
    act(() => file!.focus());
    act(() => file!.dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowUp", bubbles: true })));
    await act(async () => { await Promise.resolve(); });
    expect(document.activeElement?.textContent).toBe("Exit");
    expect(file!.getAttribute("aria-expanded")).toBe("true");
  });

  it("returns focus to the trigger when Escape closes a menu", async () => {
    const container = renderMenu();
    const file = Array.from(container.querySelectorAll("button")).find((button) => button.textContent === "File")!;
    act(() => file.focus());
    act(() => file.dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowDown", bubbles: true })));
    await act(async () => { await Promise.resolve(); });
    expect(document.activeElement?.getAttribute("role")).toBe("menuitem");

    act(() => document.activeElement!.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true })));
    expect(file.getAttribute("aria-expanded")).toBe("false");
    expect(document.activeElement).toBe(file);
    expect(container.querySelector('[role="menu"]')).toBeNull();
  });
});
