import { beforeEach, describe, expect, it, vi } from "vitest";

const searchCalls:Array<{request:Record<string,unknown>;resolve:(value:unknown)=>void}>=[];
vi.mock("../../../ipc/bridge",async(importOriginal)=>({
  ...(await importOriginal<typeof import("../../../ipc/bridge")>()),
  activateKnowledgeProject:vi.fn(async()=>undefined),getKnowledgeStatus:vi.fn(),listKnowledgeEntries:vi.fn(),listKnowledgeEvents:vi.fn(),
  createKnowledgeEntry:vi.fn(),updateKnowledgeEntry:vi.fn(),deleteKnowledgeEntry:vi.fn(),importKnowledgeContent:vi.fn(),exportKnowledge:vi.fn(),
  listenKnowledgeRuntimeEvents:vi.fn(async()=>()=>undefined),
  searchKnowledge:vi.fn((_scope:unknown,request:Record<string,unknown>)=>new Promise((resolve)=>searchCalls.push({request,resolve}))),
}));

import { useProjectStore } from "../../../stores";
import { normalizeKnowledgeEntry, knowledgeStudioService } from "../service";
import { useKnowledgeStudioStore } from "../store";

const raw=(id="one")=>({id,project_id:"project-a",type:"fact",title:"Atlas",content:"KRT-1600",metadata:{verified:true},tags:["acceptance"],source:{type:"user"},provenance:{content_hash:"abc"},created_at:"2026-01-01T00:00:00Z",updated_at:"2026-01-02T00:00:00Z",version:2});

describe("Knowledge Studio state",()=>{
  beforeEach(()=>{searchCalls.length=0;useKnowledgeStudioStore.setState({entries:[],selectedId:null,draft:{type:"note",title:"",content:"",metadataText:"{}",tagsText:"",source:{type:"user"},provenance:{}},dirty:false,query:"",search:null,searching:false,error:null});useProjectStore.setState({currentProject:{id:"project-a",name:"A",path:"C:\\atlas-project",createdAt:0,updatedAt:0,settings:{theme:"system",language:"en",autoSave:true,tabSize:2}}});});

  it("normalizes Runtime-owned snake-case contracts",()=>{const entry=normalizeKnowledgeEntry(raw());expect(entry.projectId).toBe("project-a");expect(entry.createdAt).toBe("2026-01-01T00:00:00Z");expect(entry.version).toBe(2);expect(entry.metadata).toEqual({verified:true});});

  it("tracks unsaved editor state separately from saved Runtime state",()=>{const entry=normalizeKnowledgeEntry(raw());const state=useKnowledgeStudioStore.getState();state.select(entry);expect(useKnowledgeStudioStore.getState().dirty).toBe(false);state.updateDraft({content:"changed"});expect(useKnowledgeStudioStore.getState().dirty).toBe(true);state.markSaved({...entry,content:"changed",version:3});expect(useKnowledgeStudioStore.getState().dirty).toBe(false);expect(useKnowledgeStudioStore.getState().draft.content).toBe("changed");});

  it("bounds event history",()=>{const state=useKnowledgeStudioStore.getState();for(let index=0;index<520;index++)state.addEvent({eventId:String(index),eventType:"entry_created",projectId:"project-a",timestamp:new Date().toISOString(),summary:"",metadata:{}});expect(useKnowledgeStudioStore.getState().events).toHaveLength(500);});

  it("prevents a late search response from overwriting the newest query",async()=>{const state=useKnowledgeStudioStore.getState();state.setQuery("first");const first=knowledgeStudioService.search();state.setQuery("second");const second=knowledgeStudioService.search();expect(searchCalls).toHaveLength(2);const secondCall=searchCalls[1]!;const secondRequest=secondCall.request;secondCall.resolve({request_id:secondRequest.requestId,query:"second",method:"lexical",candidate_count:1,result_count:1,results:[{entry:raw("second"),reference:{entry_id:"second",project_id:"project-a",entry_type:"fact",title:"Second",source_type:"user"},excerpt:"second",score:1,matched_terms:["second"]}],filters:{types:[],tags:[]},timing_ms:1});await second;const firstCall=searchCalls[0]!;firstCall.resolve({request_id:firstCall.request.requestId,query:"first",method:"lexical",candidate_count:1,result_count:1,results:[{entry:raw("first"),reference:{entry_id:"first",project_id:"project-a",entry_type:"fact",title:"First",source_type:"user"},excerpt:"first",score:1,matched_terms:["first"]}],filters:{types:[],tags:[]},timing_ms:5});await first;expect(useKnowledgeStudioStore.getState().search?.query).toBe("second");expect(useKnowledgeStudioStore.getState().search?.results[0]!.entry.id).toBe("second");});
});
