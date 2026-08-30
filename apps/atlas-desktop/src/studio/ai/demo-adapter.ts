import type { AIStudioAdapter } from "./service";
import type { AINormalizedRequest, AIRuntimeSnapshot } from "./types";

const now=():string=>new Date().toISOString();
const snapshot=():AIRuntimeSnapshot=>({
  runtimeHealth:"healthy",
  providers:[{providerId:"atlas.demo",name:"Demo Provider",providerType:"development",version:"1.0.0",capabilities:["chat","vision","tool_calling","structured_output","rag","memory"],health:"healthy",connectionState:"connected",enabled:true,latencyMs:0}],
  models:[{modelId:"atlas.demo.chat",name:"Atlas Demo Chat",providerId:"atlas.demo",version:"1.0.0",capabilities:["chat","vision","tool_calling","structured_output","rag","memory"],contextWindow:8192,modality:["text","image"],state:"ready",supportedParameters:["temperature","topP","maxTokens","stopSequences","responseFormat"]}],
  memories:[{memoryId:"demo-memory",content:"Demo memory used to verify Memory debugging UI.",scope:"session",createdAt:now(),source:"Demo Adapter",status:"available",includedInRequest:false}],
  tools:[{toolId:"demo.inspect_context",name:"inspect_context",description:"Development-only schema used to verify the Tool Registry UI.",provider:"Demo Adapter",permissions:["read_only"],capabilities:["search"],enabled:true,status:"healthy",parameters:{type:"object",properties:{section:{type:"string"}}}}],
  agents:[{agentId:"demo-agent",name:"Demo Inspector Agent",state:"ready",capabilities:["vision","tools"],modelId:"atlas.demo.chat",toolIds:["demo.inspect_context"],memoryScope:"session",policy:{mode:"development"}}],
  events:[{eventId:"demo-provider-loaded",eventType:"provider_loaded",timestamp:now(),source:"Demo Adapter",summary:"Demo Provider loaded for development verification."}],
  metrics:{requestCount:0,successCount:0,failureCount:0,queueDepth:0},
});

export const aiDemoModeEnabled=import.meta.env.DEV&&import.meta.env.VITE_ATLAS_AI_DEMO==="true";
export function createAIDemoAdapter():AIStudioAdapter {
  let cancelled=false;
  return {
    discover:async()=>snapshot(),
    infer:async(request:AINormalizedRequest)=>{cancelled=false;const text=request.messages.at(-1)?.content??"";await Promise.resolve();return {requestId:request.requestId,correlationId:`demo:${request.requestId}`,providerId:request.providerId,modelId:request.modelId,content:cancelled?"":"Demo response (development adapter): "+text,finishReason:cancelled?"cancelled":"stop",latencyMs:0,usage:{inputTokens:text.trim()?text.trim().split(/\s+/).length:0,outputTokens:text.trim()?text.trim().split(/\s+/).length+4:4},metadata:{adapter:"demo",production:false}};},
    cancel:async()=>{cancelled=true;return true;},
    providerAction:async()=>true,
  };
}
