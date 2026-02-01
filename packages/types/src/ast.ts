import type { NodeType, SourceLocation } from './common.js';

// Abstract Syntax Tree representation
export interface ASTNode {
  id: string;
  type: NodeType;
  name?: string;
  location: SourceLocation;
  children: ASTNode[];
  metadata: Record<string, any>;
}

export interface ParseResult {
  success: boolean;
  ast?: ASTNode;
  errors: ParseError[];
  warnings: ParseWarning[];
}

export interface ParseError {
  message: string;
  location: SourceLocation;
  severity: 'error' | 'warning';
}

export interface ParseWarning {
  message: string;
  location: SourceLocation;
  type: 'deprecated' | 'unused' | 'style';
}