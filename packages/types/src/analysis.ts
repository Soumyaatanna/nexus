import type { ASTNode, SourceLocation, Reference, SymbolType, DependencyType, Symbol, Parameter, Dependency } from './common.js';

// Code analysis types
export interface AnalysisResult {
  filePath: string;
  ast: ASTNode;
  symbols: Symbol[];
  dependencies: Dependency[];
  lastModified: Date;
}

export interface ProjectAnalysis {
  projectPath: string;
  files: AnalysisResult[];
  globalSymbols: Symbol[];
  projectDependencies: Dependency[];
  analysisDate: Date;
}

export interface AnalysisUpdate {
  filePath: string;
  changeType: 'created' | 'modified' | 'deleted';
  updatedSymbols: Symbol[];
  updatedDependencies: Dependency[];
  timestamp: Date;
}

export interface CodeStructure {
  filePath: string;
  exports: Symbol[];
  imports: Dependency[];
  classes: Symbol[];
  functions: Symbol[];
  variables: Symbol[];
}

export interface FileChange {
  path: string;
  type: 'created' | 'modified' | 'deleted';
  timestamp: Date;
  content?: string;
}