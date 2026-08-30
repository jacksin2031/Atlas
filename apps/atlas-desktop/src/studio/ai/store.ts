import { create } from "zustand";
import type {
  AIAgentDescriptor, AIContextReference, AIInferenceParameters, AIMemoryItem, AIMetricsSnapshot,
  AIModelDescriptor, AINormalizedRequest, AINormalizedResponse, AIPromptDraft, AIProviderDescriptor,
  AIRuntimeEvent, AIStudioMode, AIStudioSession, AIToolDescriptor, AIMessage, AIPromptComparison,
} from "./types";

const id = (prefix: string): string => `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
export const createAIMessage = (role: AIMessage["role"], content: string): AIMessage => ({ id: id("message"), role, content, createdAt: new Date().toISOString() });
export const extractPromptVariables = (template: string): string[] => [...new Set([...template.matchAll(/{{\s*([a-zA-Z_][\w.]*)\s*}}/g)].map((match) => match[1]!))];
export const compilePrompt = (template: string, variables: Record<string, string>): { value: string; missing: string[] } => {
  const missing = extractPromptVariables(template).filter((name) => !variables[name]);
  return { value: template.replace(/{{\s*([a-zA-Z_][\w.]*)\s*}}/g, (_, name: string) => variables[name] ?? `{{${name}}}`), missing };
};

interface AIStudioState {
  runtimeHealth: "healthy" | "busy" | "degraded" | "unhealthy" | "unknown";
  loading: boolean; running: boolean; streaming: boolean; startedAt: number | null; streamContent: string; error: string | null;
  mode: AIStudioMode; providers: AIProviderDescriptor[]; models: AIModelDescriptor[];
  selectedProviderId: string | null; selectedModelId: string | null;
  systemPrompt: string; userInput: string; messages: AIMessage[]; parameters: AIInferenceParameters;
  contexts: AIContextReference[]; memories: AIMemoryItem[]; tools: AIToolDescriptor[]; agents: AIAgentDescriptor[];
  events: AIRuntimeEvent[]; metrics: AIMetricsSnapshot; lastRequest: AINormalizedRequest | null; lastResponse: AINormalizedResponse | null;
  sessions: AIStudioSession[]; activeSessionId: string; prompt: AIPromptDraft; promptB: string; comparison: AIPromptComparison | null;
  setMode: (mode: AIStudioMode) => void; setLoading: (loading: boolean) => void; setExecution: (running: boolean, streaming?: boolean) => void;
  setStreamContent: (content: string) => void; appendStreamContent: (content: string) => void; addRuntimeEvent: (event: AIRuntimeEvent) => void; setMetrics: (metrics: AIMetricsSnapshot) => void;
  setError: (error: string | null) => void; setDiscovery: (data: Pick<AIStudioState,"runtimeHealth"|"providers"|"models"|"memories"|"tools"|"agents"|"events"|"metrics">) => void;
  selectProvider: (providerId: string | null) => void; selectModel: (modelId: string | null) => void;
  setSystemPrompt: (value: string) => void; setUserInput: (value: string) => void; setParameter: <K extends keyof AIInferenceParameters>(key: K, value: AIInferenceParameters[K]) => void;
  addMessage: (message: AIMessage) => void; updateMessage: (messageId: string, content: string) => void; deleteMessage: (messageId: string) => void; duplicateMessage: (messageId: string) => void; branchFromMessage: (messageId: string) => void;
  clearConversation: () => void; addContext: (context: AIContextReference) => void; removeContext: (contextId: string) => void; clearContext: () => void;
  setRequest: (request: AINormalizedRequest) => void; setResponse: (response: AINormalizedResponse | null) => void;
  newSession: () => void; clearSession: () => void; setPromptField: <K extends keyof AIPromptDraft>(key: K, value: AIPromptDraft[K]) => void; setPromptB: (value: string) => void; setComparison: (comparison: AIPromptComparison | null) => void;
}

const session = (): AIStudioSession => { const sessionId=id("session"); return { sessionId, name:"Untitled AI Session", providerId:null, modelId:null, createdAt:new Date().toISOString() }; };
const firstSession = session();
const defaultParameters: AIInferenceParameters = { temperature:.7, topP:.9, maxTokens:2048, stopSequences:[], stream:false };
const defaultPrompt: AIPromptDraft = { name:"Untitled Prompt", description:"", systemPrompt:"", userTemplate:"", variables:{}, version:"1.0.0", tags:[], metadata:{} };

export const useAIStudioStore = create<AIStudioState>((set, get) => ({
  runtimeHealth:"unknown", loading:false, running:false, streaming:false, startedAt:null, streamContent:"", error:null, mode:"playground",
  providers:[], models:[], selectedProviderId:null, selectedModelId:null, systemPrompt:"", userInput:"", messages:[], parameters:defaultParameters,
  contexts:[], memories:[], tools:[], agents:[], events:[], metrics:{}, lastRequest:null, lastResponse:null,
  sessions:[firstSession], activeSessionId:firstSession.sessionId, prompt:defaultPrompt, promptB:"", comparison:null,
  setMode:(mode)=>set({mode}), setLoading:(loading)=>set({loading}), setExecution:(running,streaming=false)=>set({running,streaming,startedAt:running?Date.now():null}),
  setStreamContent:(streamContent)=>set({streamContent}), appendStreamContent:(content)=>set((state)=>({streamContent:state.streamContent+content})),
  addRuntimeEvent:(event)=>set((state)=>({events:[...state.events,event].slice(-200)})), setMetrics:(metrics)=>set({metrics}), setError:(error)=>set({error}),
  setDiscovery:(data)=>set((state)=>{
    const providerOk=data.providers.some((provider)=>provider.providerId===state.selectedProviderId);
    const selectedProviderId=providerOk?state.selectedProviderId:data.providers[0]?.providerId??null;
    const providerModels=data.models.filter((model)=>model.providerId===selectedProviderId);
    const modelOk=providerModels.some((model)=>model.modelId===state.selectedModelId);
    return {...data,selectedProviderId,selectedModelId:modelOk?state.selectedModelId:providerModels[0]?.modelId??null,loading:false};
  }),
  selectProvider:(selectedProviderId)=>set((state)=>({selectedProviderId,selectedModelId:state.models.find((model)=>model.providerId===selectedProviderId)?.modelId??null})),
  selectModel:(selectedModelId)=>set({selectedModelId}), setSystemPrompt:(systemPrompt)=>set({systemPrompt}), setUserInput:(userInput)=>set({userInput}),
  setParameter:(key,value)=>set((state)=>({parameters:{...state.parameters,[key]:value}})),
  addMessage:(message)=>set((state)=>({messages:[...state.messages,message]})), updateMessage:(messageId,content)=>set((state)=>({messages:state.messages.map((message)=>message.id===messageId?{...message,content}:message)})),
  deleteMessage:(messageId)=>set((state)=>({messages:state.messages.filter((message)=>message.id!==messageId)})),
  duplicateMessage:(messageId)=>{const message=get().messages.find((item)=>item.id===messageId);if(message)get().addMessage(createAIMessage(message.role,message.content));},
  branchFromMessage:(messageId)=>set((state)=>({messages:state.messages.slice(0,state.messages.findIndex((message)=>message.id===messageId)+1).map((message)=>({...message,id:id("message")})),activeSessionId:id("session")})),
  clearConversation:()=>set({messages:[],userInput:"",lastRequest:null,lastResponse:null,streamContent:"",error:null}),
  addContext:(context)=>set((state)=>state.contexts.some((item)=>item.id===context.id)?state:{contexts:[...state.contexts,context]}), removeContext:(contextId)=>set((state)=>({contexts:state.contexts.filter((item)=>item.id!==contextId)})), clearContext:()=>set({contexts:[]}),
  setRequest:(lastRequest)=>set({lastRequest}), setResponse:(lastResponse)=>set({lastResponse}),
  newSession:()=>set((state)=>{const next=session();return{sessions:[...state.sessions,next],activeSessionId:next.sessionId,messages:[],contexts:[],lastRequest:null,lastResponse:null,streamContent:"",error:null};}),
  clearSession:()=>set({messages:[],contexts:[],systemPrompt:"",userInput:"",lastRequest:null,lastResponse:null,streamContent:"",error:null}),
  setPromptField:(key,value)=>set((state)=>({prompt:{...state.prompt,[key]:value}})), setPromptB:(promptB)=>set({promptB}), setComparison:(comparison)=>set({comparison}),
}));

let cachedModels: AIModelDescriptor[] | null = null;
let cachedProviderId: string | null = null;
let cachedProviderModels: AIModelDescriptor[] = [];
export const selectProviderModels = (state: Pick<AIStudioState,"models"|"selectedProviderId">): AIModelDescriptor[] => {
  if(state.models===cachedModels&&state.selectedProviderId===cachedProviderId)return cachedProviderModels;
  cachedModels=state.models;cachedProviderId=state.selectedProviderId;cachedProviderModels=state.models.filter((model)=>model.providerId===state.selectedProviderId);return cachedProviderModels;
};
export const validateAIRequest = (state: Pick<AIStudioState,"selectedProviderId"|"selectedModelId"|"models"|"userInput"|"contexts">): string | null => {
  if(!state.selectedProviderId)return "Select an AI provider before running inference.";
  if(!state.selectedModelId)return "Select an AI model before running inference.";
  if(!state.userInput.trim())return "Enter a user message before running inference.";
  const model=state.models.find((item)=>item.modelId===state.selectedModelId);
  if(state.contexts.some((context)=>context.kind==="vision")&&!model?.capabilities.includes("vision"))return "The selected model does not support Vision input.";
  return null;
};
