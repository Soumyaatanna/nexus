// Common types used across the system

export interface SourceLocation {
  filePath: string;
  line: number;
  column: number;
  endLine?: number;
  endColumn?: number;
}

export interface Reference {
  id: string;
  location: SourceLocation;
  type: 'definition' | 'usage' | 'import' | 'export';
}

export type NodeType = 
  | 'function' 
  | 'class' 
  | 'interface' 
  | 'variable' 
  | 'import' 
  | 'export' 
  | 'method' 
  | 'property';

export type SymbolType = 
  | 'function' 
  | 'class' 
  | 'interface' 
  | 'variable' 
  | 'method' 
  | 'property' 
  | 'module';

export type DependencyType = 
  | 'import' 
  | 'require' 
  | 'dynamic_import' 
  | 'function_call' 
  | 'inheritance' 
  | 'composition';

export type ContentType = 
  | 'code' 
  | 'documentation' 
  | 'comment' 
  | 'test';

export type SectionType = 
  | 'overview' 
  | 'api' 
  | 'examples' 
  | 'parameters' 
  | 'returns' 
  | 'throws';

export type DocumentationFormat = 
  | 'markdown' 
  | 'html' 
  | 'json' 
  | 'typescript';

export interface WatchHandle {
  id: string;
  path: string;
  active: boolean;
}

// Forward declarations for types defined in other files
export interface ASTNode {
  id: string;
  type: NodeType;
  name?: string;
  location: SourceLocation;
  children: ASTNode[];
  metadata: Record<string, any>;
}

export interface Symbol {
  id: string;
  name: string;
  type: SymbolType;
  location: SourceLocation;
  scope: string;
  references: Reference[];
  documentation?: string;
  signature?: string;
  parameters?: Parameter[];
  returnType?: string;
}

export interface Parameter {
  name: string;
  type: string;
  optional: boolean;
  defaultValue?: string;
  description?: string;
}

export interface Dependency {
  from: string;
  to: string;
  type: DependencyType;
  location: SourceLocation;
  resolved?: boolean;
  external?: boolean;
}