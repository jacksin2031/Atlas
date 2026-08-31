import { commandPaletteService } from "../../services";
import { useVisionDocumentStore } from "../vision/stores";
import { workspaceService } from "../../workspace";
import type { CommandPaletteItem } from "../../types";
import { aiStudioService } from "./service";
import { useAIStudioStore } from "./store";
import type { AIStudioMode } from "./types";

const item=(id:string,label:string,category:string,handler:()=>void,shortcut?:string):CommandPaletteItem=>({id,label,category,description:`${label} in AI Studio`,handler,shortcut});
const openMode=(mode:AIStudioMode):void=>{useAIStudioStore.getState().setMode(mode);workspaceService.openPanel("ai.editor");};
const selectedProvider=():string|null=>useAIStudioStore.getState().selectedProviderId;

export function registerAICommands():void {
  const commands:CommandPaletteItem[]=[
    item("ai.session.new","New AI Session","AI / Session",()=>useAIStudioStore.getState().newSession(),"Ctrl+N"),
    item("ai.session.open","Open AI Session","AI / Session",()=>useAIStudioStore.getState().setError("Session persistence is not connected to Project Runtime yet.")),
    item("ai.session.save","Save AI Session","AI / Session",()=>useAIStudioStore.getState().setError("Session persistence requires a Project Runtime storage policy and is not available yet."),"Ctrl+S"),
    item("ai.session.clear","Clear AI Session","AI / Session",()=>useAIStudioStore.getState().clearSession()),
    item("ai.refresh","Refresh AI Discovery","AI / Provider",()=>void aiStudioService.refresh()),
    item("ai.provider.connect","Connect AI Provider","AI / Provider",()=>{const id=selectedProvider();if(id)void aiStudioService.providerAction(id,"connect");}),
    item("ai.provider.disconnect","Disconnect AI Provider","AI / Provider",()=>{const id=selectedProvider();if(id)void aiStudioService.providerAction(id,"disconnect");}),
    item("ai.provider.test","Test AI Provider","AI / Provider",()=>{const id=selectedProvider();if(id)void aiStudioService.providerAction(id,"test");}),
    item("ai.provider.configure","Configure AI Provider","AI / Provider",()=>{workspaceService.openPanel("ai.providers");useAIStudioStore.getState().setError("Use Configure in the Providers panel to store the credential in the system vault.");}),
    item("ai.inference.run","Run Inference","AI / Inference",()=>void aiStudioService.run(),"Ctrl+Enter"),
    item("ai.inference.stop","Stop Inference","AI / Inference",()=>void aiStudioService.stop(),"Escape"),
    item("ai.inference.retry","Retry Inference","AI / Inference",()=>void aiStudioService.retry()),
    item("ai.inference.compare","Compare Inference","AI / Inference",()=>{openMode("prompt");useAIStudioStore.getState().setError("Enter Prompt A and Prompt B, then use Compare. Runtime comparison requires the Desktop AI inference bridge.");}),
    item("ai.model.settings","Model Settings","AI / Model",()=>workspaceService.openPanel("ai.models")),
    item("ai.context.image","Add Image Context","AI / Context",openImagePicker),
    item("ai.context.vision","Add Current Vision Frame","AI / Context",addCurrentVisionFrame),
    item("ai.context.knowledge","Add Knowledge Context","AI / Context",()=>{workspaceService.switchWorkspace("knowledge");workspaceService.openPanel("knowledge.search");}),
    item("ai.context.file","Add File Context","AI / Context",()=>useAIStudioStore.getState().setError("File context is not supported by the selected Runtime bridge.")),
    item("ai.context.clear","Clear AI Context","AI / Context",()=>useAIStudioStore.getState().clearContext()),
    item("ai.inspect.request","Inspect AI Request","AI / Debug",()=>workspaceService.openPanel("ai.request")),
    item("ai.inspect.response","Inspect AI Response","AI / Debug",()=>workspaceService.openPanel("ai.response")),
    item("ai.inspect.tools","Inspect Tool Trace","AI / Debug",()=>workspaceService.openPanel("ai.tools")),
    item("ai.inspect.agent","Inspect Agent Trace","AI / Debug",()=>openMode("agent")),
    item("ai.prompt.open","Open Prompt Studio","AI / Editor",()=>openMode("prompt")),item("ai.conversation.open","Open Conversation Studio","AI / Editor",()=>openMode("conversation")),item("ai.memory.open","Open Memory","AI / Editor",()=>workspaceService.openPanel("ai.memory")),item("ai.tools.open","Open Tools","AI / Editor",()=>workspaceService.openPanel("ai.tools")),item("ai.agent.open","Open Agent Inspector","AI / Editor",()=>openMode("agent")),
    item("ai.prompt.save","Save Prompt","AI / Prompt",()=>useAIStudioStore.getState().setError("Prompt persistence requires the Prompt Runtime storage bridge and is not available yet.")),
    item("ai.prompt.duplicate","Duplicate Prompt","AI / Prompt",()=>{const state=useAIStudioStore.getState();state.setPromptField("name",`${state.prompt.name} Copy`);state.setPromptField("version","1.0.0");}),
    item("ai.prompt.compare","Compare Prompts","AI / Prompt",()=>{workspaceService.openPanel("ai.comparison");void aiStudioService.comparePrompts();}),
    item("ai.view.context","Toggle AI Context","AI / View",()=>workspaceService.openPanel("ai.context")),item("ai.view.metrics","Toggle AI Metrics","AI / View",()=>workspaceService.openPanel("ai.metrics")),item("ai.view.memory","Toggle AI Memory","AI / View",()=>workspaceService.openPanel("ai.memory")),item("ai.view.tools","Toggle AI Tools","AI / View",()=>workspaceService.openPanel("ai.tools")),item("ai.view.reset","Reset AI Layout","AI / View",()=>workspaceService.resetActiveLayout()),
  ];
  commands.forEach((command)=>commandPaletteService.register(command));
}

function addCurrentVisionFrame():void {
  const vision=useVisionDocumentStore.getState();const source=vision.source;
  if(!source){useAIStudioStore.getState().setError("Vision Studio has no current frame. Capture or open an image there first.");return;}
  useAIStudioStore.getState().addContext({id:`vision:${source.name}:${vision.revision}`,kind:"vision",label:source.name,source:"Vision Studio",metadata:{width:source.width,height:source.height,sourceKind:source.kind,revision:vision.revision}});
  workspaceService.openPanel("ai.context");
}

function openImagePicker():void {
  const input=document.createElement("input");input.type="file";input.accept="image/*";input.addEventListener("change",()=>{const file=input.files?.[0];if(!file)return;useAIStudioStore.getState().addContext({id:`image:${file.name}:${file.lastModified}`,kind:"vision",label:file.name,source:"Local image",metadata:{mimeType:file.type,sizeBytes:file.size,lastModified:file.lastModified}});workspaceService.openPanel("ai.context");},{once:true});input.click();
}

const isTextInput=(target:EventTarget|null):boolean=>target instanceof HTMLElement&&(target.isContentEditable||["INPUT","TEXTAREA","SELECT"].includes(target.tagName));
export function installAIShortcuts():()=>void {
  const handler=(event:KeyboardEvent):void=>{
    const key=event.key.toLowerCase();
    if(event.ctrlKey&&key==="enter"){commandPaletteService.execute("ai.inference.run");event.preventDefault();return;}
    if(event.key==="Escape"&&useAIStudioStore.getState().running){commandPaletteService.execute("ai.inference.stop");event.preventDefault();return;}
    if(isTextInput(event.target))return;
    const id=event.ctrlKey?({n:"ai.session.new",s:"ai.session.save"} as Record<string,string>)[key]:undefined;
    if(id){commandPaletteService.execute(id);event.preventDefault();}
  };
  window.addEventListener("keydown",handler);return()=>window.removeEventListener("keydown",handler);
}
