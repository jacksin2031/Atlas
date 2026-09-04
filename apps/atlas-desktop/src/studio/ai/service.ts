import { cancelAIInference, controlAIProvider, discoverAIRuntime, executeAIInference, listenAIRuntimeEvents } from "../../ipc/bridge";
import { useVisionDocumentStore } from "../vision/stores";
import { createAIMessage, isContextAvailableForRequest, useAIStudioStore, validateAIRequest } from "./store";
import type { AINormalizedRequest, AINormalizedResponse, AIRuntimeSnapshot, AIRuntimeTransportEvent } from "./types";

export interface AIStudioAdapter {
  discover(): Promise<AIRuntimeSnapshot | null>;
  infer(request: AINormalizedRequest): Promise<AINormalizedResponse | null>;
  cancel(requestId: string): Promise<boolean | null>;
  providerAction(providerId: string, action: "connect" | "disconnect" | "refresh" | "test"): Promise<boolean | null>;
}

const runtimeAdapter: AIStudioAdapter = {
  discover: discoverAIRuntime,
  infer: executeAIInference,
  cancel: cancelAIInference,
  providerAction: controlAIProvider,
};

const requestId = (): string => globalThis.crypto?.randomUUID?.() ?? `request-${Date.now()}-${Math.random().toString(36).slice(2,8)}`;
const safeParameters = (model: ReturnType<typeof useAIStudioStore.getState>["models"][number] | undefined, parameters: ReturnType<typeof useAIStudioStore.getState>["parameters"]): Partial<typeof parameters> => {
  const supported = model?.supportedParameters;
  if (!supported) return { temperature:parameters.temperature, topP:parameters.topP, maxTokens:parameters.maxTokens, stopSequences:parameters.stopSequences, stream:parameters.stream };
  return Object.fromEntries(supported.map((key)=>[key,parameters[key]])) as Partial<typeof parameters>;
};
const attachmentDataUrl = (context: ReturnType<typeof useAIStudioStore.getState>["contexts"][number]): string | undefined => {
  if(context.source!=="Vision Studio")return undefined;
  const source=useVisionDocumentStore.getState().source;
  return source?.name===context.label?source.url:undefined;
};
const inspectorRequest = (request: AINormalizedRequest): AINormalizedRequest => ({...request,attachments:request.attachments.map(({dataUrl,...attachment})=>({...attachment,metadata:{...attachment.metadata,transport:dataUrl?"attached":"reference-only"}}))});

export const createNormalizedRequest = (): AINormalizedRequest | null => {
  const state=useAIStudioStore.getState();
  if(!state.selectedProviderId||!state.selectedModelId)return null;
  const contexts=state.contexts.filter(isContextAvailableForRequest);
  const messages=[...(state.systemPrompt.trim()?[createAIMessage("system",state.systemPrompt.trim())]:[]),...state.messages,createAIMessage("user",state.userInput.trim())];
  const model=state.models.find((item)=>item.modelId===state.selectedModelId);
  return {
    requestId:requestId(),timestamp:new Date().toISOString(),providerId:state.selectedProviderId,modelId:state.selectedModelId,messages,
    parameters:safeParameters(model,state.parameters),tools:state.tools.filter((tool)=>tool.enabled).map((tool)=>tool.toolId),contextReferences:contexts,
    attachments:contexts.filter((context)=>context.kind==="vision").map((context)=>({id:context.id,kind:context.kind,label:context.label,dataUrl:attachmentDataUrl(context),metadata:context.metadata})),
  };
};

class AIStudioService {
  private adapter: AIStudioAdapter = runtimeAdapter;

  setAdapter(adapter: AIStudioAdapter): void { this.adapter=adapter; }
  resetAdapter(): void { this.adapter=runtimeAdapter; }

  async connectRuntimeEvents(): Promise<() => void> {
    return listenAIRuntimeEvents((event)=>this.handleRuntimeEvent(event));
  }

  handleRuntimeEvent(event: AIRuntimeTransportEvent): void {
    const state=useAIStudioStore.getState();
    state.addRuntimeEvent({eventId:event.eventId,eventType:event.eventType,timestamp:event.timestamp,correlationId:event.correlationId,source:event.source,summary:event.summary,metadata:event.metadata});
    if(event.metrics)state.setMetrics(event.metrics);
    if(event.requestId&&state.lastRequest?.requestId!==event.requestId)return;
    if(event.eventType==="inference_started"){state.setExecution(true,state.lastRequest?.parameters.stream===true);return;}
    if(event.eventType==="inference_chunk"&&event.delta){state.appendStreamContent(event.delta);return;}
    if(event.eventType==="inference_completed"){
      if(event.response)state.setResponse(event.response);
      state.setExecution(false);return;
    }
    if(event.eventType==="inference_cancelled"){state.setExecution(false);state.setError("Inference cancelled.");return;}
    if(event.eventType==="inference_failed"){state.setExecution(false);state.setError(event.error||event.summary||"Inference failed.");}
  }

  async refresh(): Promise<void> {
    const store=useAIStudioStore.getState();store.setLoading(true);store.setError(null);
    try {
      const snapshot=await this.adapter.discover();
      if(!snapshot){store.setLoading(false);store.setError("AI Runtime unavailable. Start or connect the Desktop AI Runtime bridge, then refresh discovery.");return;}
      store.setDiscovery(snapshot);
    } catch (error) {
      store.setLoading(false);store.setError(this.message(error,"Unable to discover AI Runtime providers."));
    }
  }

  async run(): Promise<void> {
    const current=useAIStudioStore.getState();const validation=validateAIRequest(current);
    if(validation){current.setError(validation);return;}
    const request=createNormalizedRequest();if(!request)return;
    current.setError(null);current.setRequest(inspectorRequest(request));current.setResponse(null);current.setStreamContent("");current.setExecution(true,request.parameters.stream===true);
    current.addMessage(request.messages.at(-1)!);current.setUserInput("");
    try {
      const response=await this.adapter.infer(request);
      const latest=useAIStudioStore.getState();
      if(!response){latest.setExecution(false);latest.setError(latest.error??"AI Runtime unavailable. The normalized request was not submitted.");return;}
      latest.setResponse(response);latest.setStreamContent(response.content);latest.addMessage(createAIMessage("assistant",response.content));latest.setExecution(false);
    } catch(error){const latest=useAIStudioStore.getState();latest.setExecution(false);latest.setError(this.message(error,"Inference failed."));}
  }

  async retry(): Promise<void> {
    const state=useAIStudioStore.getState();const previous=[...state.messages].reverse().find((message)=>message.role==="user");
    if(!previous){state.setError("There is no user message to retry.");return;}
    state.setUserInput(previous.content);await this.run();
  }

  async stop(): Promise<void> {
    const state=useAIStudioStore.getState();const active=state.lastRequest;
    if(!active||!state.running)return;
    try { await this.adapter.cancel(active.requestId); } finally { const latest=useAIStudioStore.getState();latest.setExecution(false);latest.setError("Inference cancelled."); }
  }

  async comparePrompts(): Promise<void> {
    const state=useAIStudioStore.getState();
    if(!state.selectedProviderId||!state.selectedModelId){state.setError("Select a provider and model before comparing prompts.");return;}
    if(!state.prompt.userTemplate.trim()||!state.promptB.trim()){state.setError("Enter both Prompt A and Prompt B before comparing.");return;}
    const build=(content:string):AINormalizedRequest=>{
      const model=state.models.find((item)=>item.modelId===state.selectedModelId);
      const contexts=state.contexts.filter(isContextAvailableForRequest);
      return {requestId:requestId(),timestamp:new Date().toISOString(),providerId:state.selectedProviderId!,modelId:state.selectedModelId!,messages:[...(state.prompt.systemPrompt.trim()?[createAIMessage("system",state.prompt.systemPrompt.trim())]:[]),createAIMessage("user",content)],parameters:safeParameters(model,state.parameters),tools:state.tools.filter((tool)=>tool.enabled).map((tool)=>tool.toolId),contextReferences:contexts,attachments:contexts.filter((context)=>context.kind==="vision").map((context)=>({id:context.id,kind:context.kind,label:context.label,dataUrl:attachmentDataUrl(context),metadata:context.metadata}))};
    };
    const requestA=build(state.prompt.userTemplate),requestB=build(state.promptB);state.setExecution(true);state.setError(null);state.setComparison(null);
    const [a,b]=await Promise.allSettled([this.adapter.infer(requestA),this.adapter.infer(requestB)]);const latest=useAIStudioStore.getState();latest.setExecution(false);
    const responseA=a.status==="fulfilled"?a.value:null,responseB=b.status==="fulfilled"?b.value:null;
    latest.setComparison({promptA:state.prompt.userTemplate,promptB:state.promptB,responseA,responseB,errorA:a.status==="rejected"?this.message(a.reason,"Prompt A failed."):responseA?undefined:"AI Runtime unavailable.",errorB:b.status==="rejected"?this.message(b.reason,"Prompt B failed."):responseB?undefined:"AI Runtime unavailable."});
  }

  async providerAction(providerId: string, action: "connect" | "disconnect" | "refresh" | "test"): Promise<void> {
    const state=useAIStudioStore.getState();state.setError(null);
    try {
      const result=await this.adapter.providerAction(providerId,action);
      if(result===null){state.setError(`Provider ${action} is unavailable through the current Desktop AI bridge.`);return;}
      if(result===false){state.setError(`Provider ${action} reached the Desktop AI bridge but the provider rejected or failed the action.`);return;}
      await this.refresh();
    } catch(error){state.setError(this.message(error,`Provider ${action} failed at the Desktop AI bridge.`));}
  }

  private message(error: unknown, fallback: string): string { return error instanceof Error&&error.message?`${fallback} ${error.message}`:fallback; }
}

export const aiStudioService = new AIStudioService();
