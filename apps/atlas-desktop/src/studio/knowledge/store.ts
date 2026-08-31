import { create } from "zustand";
import type { KnowledgeDraft, KnowledgeEntry, KnowledgeEvent, KnowledgeHealth, KnowledgeSearchResponse } from "./types";

const emptyDraft = (): KnowledgeDraft => ({ type:"note", title:"", content:"", metadataText:"{}", tagsText:"", source:{type:"user"}, provenance:{} });
const entryDraft = (entry: KnowledgeEntry): KnowledgeDraft => ({ id:entry.id, type:entry.type, title:entry.title, content:entry.content, metadataText:JSON.stringify(entry.metadata,null,2), tagsText:entry.tags.join(", "), source:entry.source, provenance:entry.provenance });

interface KnowledgeStudioState {
  health: KnowledgeHealth;
  entries: KnowledgeEntry[];
  selectedId: string | null;
  draft: KnowledgeDraft;
  dirty: boolean;
  filter: string;
  query: string;
  searching: boolean;
  search: KnowledgeSearchResponse | null;
  events: KnowledgeEvent[];
  loading: boolean;
  error: string | null;
  setHealth: (health: KnowledgeHealth) => void;
  setEntries: (entries: KnowledgeEntry[]) => void;
  select: (entry: KnowledgeEntry | null) => void;
  newDraft: () => void;
  updateDraft: (changes: Partial<KnowledgeDraft>) => void;
  markSaved: (entry: KnowledgeEntry) => void;
  removeEntry: (id: string) => void;
  setFilter: (filter: string) => void;
  setQuery: (query: string) => void;
  setSearching: (searching: boolean) => void;
  setSearch: (search: KnowledgeSearchResponse | null) => void;
  setEvents: (events: KnowledgeEvent[]) => void;
  addEvent: (event: KnowledgeEvent) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useKnowledgeStudioStore = create<KnowledgeStudioState>((set) => ({
  health:{status:"unknown",entryCount:0}, entries:[], selectedId:null, draft:emptyDraft(), dirty:false, filter:"", query:"", searching:false, search:null, events:[], loading:false, error:null,
  setHealth:(health)=>set({health}), setEntries:(entries)=>set({entries}),
  select:(entry)=>set({selectedId:entry?.id??null,draft:entry?entryDraft(entry):emptyDraft(),dirty:false}),
  newDraft:()=>set({selectedId:null,draft:emptyDraft(),dirty:false}),
  updateDraft:(changes)=>set((state)=>({draft:{...state.draft,...changes},dirty:true})),
  markSaved:(entry)=>set((state)=>({entries:[entry,...state.entries.filter((item)=>item.id!==entry.id)],selectedId:entry.id,draft:entryDraft(entry),dirty:false})),
  removeEntry:(id)=>set((state)=>({entries:state.entries.filter((item)=>item.id!==id),selectedId:state.selectedId===id?null:state.selectedId,draft:state.selectedId===id?emptyDraft():state.draft,dirty:state.selectedId===id?false:state.dirty})),
  setFilter:(filter)=>set({filter}), setQuery:(query)=>set({query}), setSearching:(searching)=>set({searching}), setSearch:(search)=>set({search}),
  setEvents:(events)=>set({events}), addEvent:(event)=>set((state)=>({events:[...state.events.filter((item)=>item.eventId!==event.eventId),event].slice(-500)})),
  setLoading:(loading)=>set({loading}), setError:(error)=>set({error}),
}));

