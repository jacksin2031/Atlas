import { describe, expect, it } from "vitest";
import { commandPaletteService } from "../../../services";
import { registerVisionCommands } from "../commands";
import { useVisionDocumentStore } from "../stores";
describe("Vision command routing",()=>{ it("registers unique commands and executes view commands directly",()=>{ registerVisionCommands(); registerVisionCommands(); const commands=commandPaletteService.getAllCommands(); expect(new Set(commands.map((c)=>c.id)).size).toBe(commands.length); const before=useVisionDocumentStore.getState().grid; commandPaletteService.execute("vision.grid"); expect(useVisionDocumentStore.getState().grid).toBe(!before); }); });
