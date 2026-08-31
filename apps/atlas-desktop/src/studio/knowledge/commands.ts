import { commandPaletteService } from "../../services";
import type { CommandPaletteItem } from "../../types";
import { workspaceService } from "../../workspace";
import { knowledgeStudioService } from "./service";
import { useKnowledgeStudioStore } from "./store";

const item=(id:string,label:string,handler:()=>void,shortcut?:string):CommandPaletteItem=>({id,label,handler,shortcut,category:"Knowledge",description:`${label} through Knowledge Runtime`});
const report=(error:unknown)=>useKnowledgeStudioStore.getState().setError(error instanceof Error?error.message:String(error));
const save=()=>void knowledgeStudioService.save().catch(report);
const remove=()=>{const state=useKnowledgeStudioStore.getState();if(state.selectedId&&window.confirm(`Delete '${state.draft.title}' from Knowledge Runtime?`))void knowledgeStudioService.deleteSelected().catch(report);};
export function registerKnowledgeCommands():void{[
  item("knowledge.new","New Knowledge",()=>{if(knowledgeStudioService.newEntry())workspaceService.openPanel("knowledge.editor");},"Ctrl+N"),
  item("knowledge.search","Search Knowledge",()=>workspaceService.openPanel("knowledge.search"),"Ctrl+K"),
  item("knowledge.save","Save Knowledge",save,"Ctrl+S"),item("knowledge.delete","Delete Knowledge",remove,"Delete"),
  item("knowledge.import","Import Knowledge",()=>workspaceService.openPanel("knowledge.import")),item("knowledge.export.json","Export Knowledge as JSON",()=>void knowledgeStudioService.exportFile("json").catch(report)),
  item("knowledge.refresh","Refresh Knowledge",()=>void knowledgeStudioService.initialize()),item("knowledge.focus-search","Focus Knowledge Search",()=>workspaceService.openPanel("knowledge.search"),"Ctrl+F"),
].forEach((command)=>commandPaletteService.register(command));}
const isTextInput=(target:EventTarget|null):boolean=>target instanceof HTMLElement&&(target.isContentEditable||["INPUT","TEXTAREA","SELECT"].includes(target.tagName));
export function installKnowledgeShortcuts():()=>void{const handler=(event:KeyboardEvent)=>{const key=event.key.toLowerCase();if(event.ctrlKey&&key==="s"){save();event.preventDefault();return;}if(isTextInput(event.target))return;const id=event.ctrlKey?({n:"knowledge.new",k:"knowledge.search",f:"knowledge.focus-search"} as Record<string,string>)[key]:key==="delete"?"knowledge.delete":undefined;if(id){commandPaletteService.execute(id);event.preventDefault();}};window.addEventListener("keydown",handler);return()=>window.removeEventListener("keydown",handler);}

