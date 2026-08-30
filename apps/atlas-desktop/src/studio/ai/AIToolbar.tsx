import React from "react";
import { IconButton, ToolbarGroup } from "../../design-system";
import { commandPaletteService } from "../../services";
import { useAIStudioStore } from "./store";

const run=(id:string)=>():void=>commandPaletteService.execute(id);
export const AIToolbar:React.FC=()=>{const running=useAIStudioStore((s)=>s.running);return <div className="ai-toolbar" role="toolbar" aria-label="AI Studio toolbar">
  <ToolbarGroup label="Session"><IconButton icon="add" label="New Session" onClick={run("ai.session.new")}/><IconButton icon="open" label="Open Session" onClick={run("ai.session.open")}/><IconButton icon="save" label="Save Session" onClick={run("ai.session.save")}/><IconButton icon="clear" label="Clear Session" onClick={run("ai.session.clear")}/></ToolbarGroup>
  <ToolbarGroup label="Inference"><IconButton icon="play" label="Run Inference (Ctrl+Enter)" onClick={run("ai.inference.run")} disabled={running}/><IconButton icon="stop" label="Stop Inference (Escape)" onClick={run("ai.inference.stop")} disabled={!running}/><IconButton icon="retry" label="Retry Inference" onClick={run("ai.inference.retry")} disabled={running}/><IconButton icon="duplicate" label="Compare Prompts" onClick={run("ai.inference.compare")}/></ToolbarGroup>
  <ToolbarGroup label="Model"><IconButton icon="ai" label="Select Provider and Model" onClick={run("ai.model.settings")}/><IconButton icon="settings" label="Model Settings" onClick={run("ai.model.settings")}/></ToolbarGroup>
  <ToolbarGroup label="Context"><IconButton icon="image" label="Add Current Vision Frame" onClick={run("ai.context.vision")}/><IconButton icon="open" label="Add Image" onClick={run("ai.context.image")}/><IconButton icon="folder" label="Add Knowledge Context" onClick={run("ai.context.knowledge")}/><IconButton icon="clear" label="Clear Context" onClick={run("ai.context.clear")}/></ToolbarGroup>
  <ToolbarGroup label="Debug"><IconButton icon="inspect" label="Inspect Request" onClick={run("ai.inspect.request")}/><IconButton icon="eye" label="Inspect Response" onClick={run("ai.inspect.response")}/><IconButton icon="tools" label="Tool Trace" onClick={run("ai.inspect.tools")}/><IconButton icon="ai" label="Agent Trace" onClick={run("ai.inspect.agent")}/></ToolbarGroup>
  <ToolbarGroup label="View"><IconButton icon="folder" label="Context Panel" onClick={run("ai.view.context")}/><IconButton icon="metrics" label="Metrics Panel" onClick={run("ai.view.metrics")}/><IconButton icon="memory" label="Memory Panel" onClick={run("ai.view.memory")}/><IconButton icon="tools" label="Tools Panel" onClick={run("ai.view.tools")}/><IconButton icon="fit" label="Reset AI Layout" onClick={run("ai.view.reset")}/></ToolbarGroup>
 </div>;};
