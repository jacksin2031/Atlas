import {
  activateKnowledgeProject, createKnowledgeEntry, deleteKnowledgeEntry, exportKnowledge, getKnowledgeStatus, importKnowledgeContent,
  listKnowledgeEntries, listKnowledgeEvents, listenKnowledgeRuntimeEvents, searchKnowledge, updateKnowledgeEntry,
} from "../../ipc/bridge";
import { useProjectStore } from "../../stores";
import { useAIStudioStore } from "../ai";
import { useKnowledgeStudioStore } from "./store";
import type { KnowledgeDraft, KnowledgeEntry, KnowledgeEvent, KnowledgeHealth, KnowledgeReference, KnowledgeSearchResponse } from "./types";

type Raw = Record<string, unknown>;
const record=(value:unknown):Raw=>value&&typeof value==="object"&&!Array.isArray(value)?value as Raw:{};
const stringArray=(value:unknown):string[]=>Array.isArray(value)?value.map(String):[];
const reference=(value:unknown):KnowledgeReference=>{const raw=record(value);return{entryId:String(raw.entry_id??raw.entryId??""),projectId:String(raw.project_id??raw.projectId??""),entryType:String(raw.entry_type??raw.entryType??"note") as KnowledgeReference["entryType"],title:String(raw.title??""),sourceType:String(raw.source_type??raw.sourceType??"unknown")};};
export const normalizeKnowledgeEntry=(value:unknown):KnowledgeEntry=>{const raw=record(value);return{id:String(raw.id??""),projectId:String(raw.project_id??raw.projectId??""),type:String(raw.type??"note") as KnowledgeEntry["type"],title:String(raw.title??""),content:String(raw.content??""),metadata:record(raw.metadata),tags:stringArray(raw.tags),source:record(raw.source),provenance:record(raw.provenance),createdAt:String(raw.created_at??raw.createdAt??""),updatedAt:String(raw.updated_at??raw.updatedAt??""),version:Number(raw.version??1)};};
const normalizeEvent=(value:unknown):KnowledgeEvent=>{const raw=record(value);return{eventId:String(raw.event_id??raw.eventId??""),eventType:String(raw.event_type??raw.eventType??""),projectId:String(raw.project_id??raw.projectId??""),timestamp:String(raw.timestamp??""),entryId:raw.entry_id===null?null:String(raw.entry_id??raw.entryId??""),correlationId:raw.correlation_id===null?null:String(raw.correlation_id??raw.correlationId??""),summary:String(raw.summary??""),metadata:record(raw.metadata)};};
const normalizeSearch=(value:unknown):KnowledgeSearchResponse=>{const raw=record(value);return{requestId:String(raw.request_id??raw.requestId??""),query:String(raw.query??""),method:"lexical",candidateCount:Number(raw.candidate_count??raw.candidateCount??0),resultCount:Number(raw.result_count??raw.resultCount??0),results:(Array.isArray(raw.results)?raw.results:[]).map((item)=>{const row=record(item);return{entry:normalizeKnowledgeEntry(row.entry),reference:reference(row.reference),excerpt:String(row.excerpt??""),score:Number(row.score??0),matchedTerms:stringArray(row.matched_terms??row.matchedTerms)};}),filters:{types:stringArray(record(raw.filters).types),tags:stringArray(record(raw.filters).tags)},timingMs:Number(raw.timing_ms??raw.timingMs??0)};};
const message=(error:unknown):string=>error instanceof Error?error.message:String(error);

export class KnowledgeStudioService {
  private searchSequence=0;
  private refreshTimer:ReturnType<typeof setTimeout>|null=null;

  private scope():{projectId:string;projectPath:string} {
    const project=useProjectStore.getState().currentProject;
    if(!project)throw new Error("Open a Project before using Knowledge Runtime.");
    return{projectId:project.id,projectPath:project.path};
  }

  async activateProject():Promise<void>{await activateKnowledgeProject(this.scope());}

  async initialize():Promise<void>{
    const state=useKnowledgeStudioStore.getState();state.setLoading(true);state.setError(null);
    try{await this.activateProject();await Promise.all([this.refreshStatus(),this.refreshList(),this.refreshEvents()]);}
    catch(error){state.setHealth({status:"unavailable",entryCount:0});state.setError(`Knowledge Runtime unavailable: ${message(error)}`);}
    finally{state.setLoading(false);}
  }

  async refreshStatus():Promise<void>{const raw=record(await getKnowledgeStatus(this.scope()));useKnowledgeStudioStore.getState().setHealth({status:String(raw.status??"error") as KnowledgeHealth["status"],projectId:String(raw.project_id??""),entryCount:Number(raw.entry_count??0),index:{method:String(record(raw.index).method??""),state:String(record(raw.index).state??""),documentCount:Number(record(raw.index).document_count??0)},storage:{provider:String(record(raw.storage).provider??""),location:String(record(raw.storage).location??"")},uptimeMs:Number(raw.uptime_ms??0),timingMs:Number(raw.timing_ms??0)});}
  async refreshList():Promise<void>{const raw=record(await listKnowledgeEntries(this.scope(),{limit:100}));useKnowledgeStudioStore.getState().setEntries((Array.isArray(raw.entries)?raw.entries:[]).map(normalizeKnowledgeEntry));}
  async refreshEvents():Promise<void>{const raw=await listKnowledgeEvents(this.scope(),100);useKnowledgeStudioStore.getState().setEvents((Array.isArray(raw)?raw:[]).map(normalizeEvent));}

  select(entry:KnowledgeEntry|null):boolean{const state=useKnowledgeStudioStore.getState();if(state.dirty&&!window.confirm("Discard unsaved Knowledge Editor changes?"))return false;state.select(entry);return true;}
  newEntry():boolean{return this.select(null);}

  private draftPayload(draft:KnowledgeDraft):Record<string,unknown>{let metadata:unknown;try{metadata=JSON.parse(draft.metadataText||"{}");}catch{throw new Error("Metadata must be valid JSON.");}if(!metadata||typeof metadata!=="object"||Array.isArray(metadata))throw new Error("Metadata must be a JSON object.");return{type:draft.type,title:draft.title.trim(),content:draft.content,metadata,tags:draft.tagsText.split(",").map((tag)=>tag.trim()).filter(Boolean),source:draft.source,provenance:draft.provenance};}
  async save():Promise<KnowledgeEntry>{const state=useKnowledgeStudioStore.getState();const payload=this.draftPayload(state.draft);if(!String(payload.title))throw new Error("Knowledge title is required.");const scope=this.scope(),requestId=`knowledge-save-${crypto.randomUUID()}`;const raw=state.draft.id?await updateKnowledgeEntry(scope,state.draft.id,payload,requestId):await createKnowledgeEntry(scope,payload,requestId);const entry=normalizeKnowledgeEntry(raw);state.markSaved(entry);await Promise.all([this.refreshStatus(),this.refreshEvents()]);return entry;}
  async deleteSelected():Promise<void>{const state=useKnowledgeStudioStore.getState();if(!state.selectedId)return;await deleteKnowledgeEntry(this.scope(),state.selectedId,`knowledge-delete-${crypto.randomUUID()}`);state.removeEntry(state.selectedId);await Promise.all([this.refreshStatus(),this.refreshEvents()]);}

  async search(query=useKnowledgeStudioStore.getState().query):Promise<void>{const state=useKnowledgeStudioStore.getState(),sequence=++this.searchSequence,requestId=`knowledge-search-${crypto.randomUUID()}`;state.setSearching(true);state.setError(null);try{const response=normalizeSearch(await searchKnowledge(this.scope(),{query,limit:25,requestId}));if(sequence===this.searchSequence&&response.requestId===requestId)state.setSearch(response);}catch(error){if(sequence===this.searchSequence)state.setError(message(error));}finally{if(sequence===this.searchSequence)state.setSearching(false);}}

  async importFile(file:File):Promise<void>{const format=(file.name.split(".").pop()??"").toLowerCase();if(!["txt","md","markdown","json","csv"].includes(format))throw new Error("Supported imports are TXT, Markdown, JSON, and CSV.");await importKnowledgeContent(this.scope(),{filename:file.name,format,content:await file.text(),requestId:`knowledge-import-${crypto.randomUUID()}`});await this.initialize();}
  async exportFile(format:"json"|"md"):Promise<void>{const result=record(await exportKnowledge(this.scope(),format));const blob=new Blob([String(result.content??"")],{type:format==="json"?"application/json":"text/markdown"});const link=document.createElement("a");link.href=URL.createObjectURL(blob);link.download=`atlas-knowledge.${format}`;link.click();setTimeout(()=>URL.revokeObjectURL(link.href),0);}
  addToAI(entry:KnowledgeEntry):void{useAIStudioStore.getState().addContext({id:`knowledge:${entry.projectId}:${entry.id}`,kind:"knowledge",label:entry.title,source:String(entry.source.type??"Knowledge Runtime"),preview:entry.content.slice(0,220),includedInRequest:true,metadata:{knowledgeReference:{entryId:entry.id,projectId:entry.projectId,entryType:entry.type,title:entry.title,sourceType:String(entry.source.type??"unknown")},version:entry.version}});}

  async connectRuntimeEvents():Promise<()=>void>{return listenKnowledgeRuntimeEvents((raw)=>{const event=normalizeEvent(raw);const project=useProjectStore.getState().currentProject;if(!project||event.projectId!==project.id)return;useKnowledgeStudioStore.getState().addEvent(event);if(event.eventType.startsWith("entry_")||event.eventType==="import_completed"){if(this.refreshTimer)clearTimeout(this.refreshTimer);this.refreshTimer=setTimeout(()=>{this.refreshTimer=null;void Promise.all([this.refreshList(),this.refreshStatus()]);},50);}});}
}

export const knowledgeStudioService=new KnowledgeStudioService();
