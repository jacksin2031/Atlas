// @vitest-environment node
import { readdirSync, readFileSync } from "node:fs";
import { join, relative } from "node:path";
import { describe, expect, it } from "vitest";

function sourceFiles(directory: string): string[] {
  const files: string[] = [];
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) files.push(...sourceFiles(path));
    else if (/\.(?:ts|tsx)$/.test(entry.name)) files.push(path);
  }
  return files;
}

describe("Desktop transport boundary", () => {
  it("keeps Tauri API imports inside the IPC bridge", () => {
    const src = join(process.cwd(), "src");
    const bridge = join(src, "ipc", "bridge.ts");
    const offenders = sourceFiles(src)
      .filter((path) => path !== bridge)
      .filter((path) => /^\s*import[\s\S]*?from\s+["']@tauri-apps\/api\//m.test(readFileSync(path, "utf8")))
      .map((path) => relative(process.cwd(), path).replaceAll("\\", "/"));

    expect(offenders).toEqual([]);
  });
});
