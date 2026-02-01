import type { SourceLocation, Symbol, Dependency } from './common.js';

// Context and assistance types
export interface CodeLocation {
  filePath: string;
  line: number;
  column: number;
  selection?: {
    startLine: number;
    startColumn: number;
    endLine: number;
    endColumn: number;
  };
}

export interface CodeContext {
  location: CodeLocation;
  surroundingCode: string;
  symbols: Symbol[];
  dependencies: Dependency[];
  relatedFunctions: Function[];
  scope: string;
}

export interface Function {
  name: string;
  signature: string;
  location: SourceLocation;
  documentation?: string;
  examples?: string[];
}

export interface Suggestion {
  id: string;
  type: 'completion' | 'refactor' | 'fix' | 'optimization';
  title: string;
  description: string;
  code?: string;
  confidence: number;
  category: string;
}

export interface CodeError {
  message: string;
  location: SourceLocation;
  severity: 'error' | 'warning' | 'info';
  code?: string;
  source: string;
}

export interface ErrorAnalysis {
  error: CodeError;
  possibleCauses: string[];
  suggestedFixes: Suggestion[];
  relatedDocumentation: string[];
}

export interface SessionContext {
  sessionId: string;
  userId?: string;
  startTime: Date;
  lastActivity: Date;
  interactions: Interaction[];
  preferences: UserPreferences;
}

export interface Interaction {
  id: string;
  type: 'query' | 'suggestion' | 'error' | 'completion';
  timestamp: Date;
  input: any;
  output: any;
  context: CodeLocation;
}

export interface UserPreferences {
  language: string;
  theme: 'light' | 'dark';
  suggestionLevel: 'minimal' | 'moderate' | 'comprehensive';
  autoComplete: boolean;
  showDocumentation: boolean;
}

// Context Provider interface
export interface ContextProvider {
  getContext(location: CodeLocation): Promise<CodeContext>;
  provideSuggestions(context: CodeContext): Promise<Suggestion[]>;
  analyzeError(error: CodeError): Promise<ErrorAnalysis>;
  maintainSession(sessionId: string): Promise<SessionContext>;
}