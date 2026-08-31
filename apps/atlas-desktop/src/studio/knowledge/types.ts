export type KnowledgeEntryType = "note" | "document" | "fact" | "observation";
export type KnowledgeHealthState = "unknown" | "available" | "indexing" | "degraded" | "unavailable" | "error";

export interface KnowledgeReference {
  entryId: string;
  projectId: string;
  entryType: KnowledgeEntryType;
  title: string;
  sourceType: string;
}

export interface KnowledgeEntry {
  id: string;
  projectId: string;
  type: KnowledgeEntryType;
  title: string;
  content: string;
  metadata: Record<string, unknown>;
  tags: string[];
  source: Record<string, unknown>;
  provenance: Record<string, unknown>;
  createdAt: string;
  updatedAt: string;
  version: number;
}

export interface KnowledgeDraft {
  id?: string;
  type: KnowledgeEntryType;
  title: string;
  content: string;
  metadataText: string;
  tagsText: string;
  source: Record<string, unknown>;
  provenance: Record<string, unknown>;
}

export interface KnowledgeSearchResult {
  entry: KnowledgeEntry;
  reference: KnowledgeReference;
  excerpt: string;
  score: number;
  matchedTerms: string[];
}

export interface KnowledgeSearchResponse {
  requestId: string;
  query: string;
  method: "lexical";
  candidateCount: number;
  resultCount: number;
  results: KnowledgeSearchResult[];
  filters: { types: string[]; tags: string[] };
  timingMs: number;
}

export interface KnowledgeHealth {
  status: KnowledgeHealthState;
  projectId?: string;
  entryCount: number;
  index?: { method: string; state: string; documentCount: number };
  storage?: { provider: string; location: string };
  uptimeMs?: number;
  timingMs?: number;
}

export interface KnowledgeEvent {
  eventId: string;
  eventType: string;
  projectId: string;
  timestamp: string;
  entryId?: string | null;
  correlationId?: string | null;
  summary: string;
  metadata: Record<string, unknown>;
}

export interface KnowledgeExport {
  format: "json" | "md";
  content: string;
  count: number;
}

