import type { DocumentationFormat, SectionType } from './common.js';
import type { AnalysisResult, AnalysisUpdate } from './analysis.js';

// Documentation types
export interface Documentation {
  filePath: string;
  sections: DocumentationSection[];
  lastGenerated: Date;
  format: DocumentationFormat;
}

export interface DocumentationSection {
  id: string;
  title: string;
  content: string;
  type: SectionType;
  symbols: string[];
  lastUpdated: Date;
}

export interface DocumentationUpdate {
  filePath: string;
  updatedSections: DocumentationSection[];
  timestamp: Date;
}

// Documentation Generator interfaces
export interface DocumentationGenerator {
  generateDocs(analysisResult: AnalysisResult): Promise<Documentation>;
  updateDocs(changes: AnalysisUpdate): Promise<DocumentationUpdate>;
  exportDocs(format: DocumentationFormat): Promise<string>;
}

export interface DocumentationConfig {
  includePrivate: boolean;
  includeTests: boolean;
  outputFormat: DocumentationFormat;
  templatePath?: string;
  customSections?: string[];
}