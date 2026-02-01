import type { ContentType } from './common.js';

// Search types
export interface SearchQuery {
  text: string;
  type: 'natural' | 'code' | 'documentation';
  filters?: SearchFilter[];
}

export interface SearchFilter {
  field: string;
  value: string | string[];
  operator: 'equals' | 'contains' | 'startsWith' | 'endsWith';
}

export interface SearchResults {
  query: SearchQuery;
  results: SearchResult[];
  totalCount: number;
  executionTime: number;
  suggestions?: SearchSuggestion[];
}

export interface SearchResult {
  id: string;
  title: string;
  content: string;
  filePath: string;
  type: ContentType;
  score: number;
  highlights: SearchHighlight[];
  context: string;
}

export interface SearchHighlight {
  field: string;
  fragments: string[];
}

export interface SearchSuggestion {
  text: string;
  type: 'correction' | 'completion' | 'related';
  score: number;
}

export interface IndexableContent {
  id: string;
  content: string;
  type: ContentType;
  filePath: string;
  symbols: string[];
  keywords: string[];
  metadata: Record<string, any>;
}

export interface ContentChange {
  id: string;
  type: 'created' | 'updated' | 'deleted';
  content?: IndexableContent;
  timestamp: Date;
}

// Search index entry
export interface IndexEntry {
  id: string;
  content: string;
  type: ContentType;
  filePath: string;
  symbols: string[];
  keywords: string[];
  embedding?: number[];
  lastIndexed: Date;
}

// Search Engine interface
export interface SearchEngine {
  indexContent(content: IndexableContent): Promise<void>;
  search(query: SearchQuery): Promise<SearchResults>;
  suggest(partialQuery: string): Promise<SearchSuggestion[]>;
  updateIndex(changes: ContentChange[]): Promise<void>;
}