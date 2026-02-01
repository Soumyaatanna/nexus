"""
Code Analyzer Module
====================

Analyzes codebases to extract structure, dependencies, and relationships.
Populates the knowledge graph with code understanding.
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Optional, Set
from .knowledge_graph import KnowledgeGraph, NodeType, RelationType


class CodeAnalyzer:
    """
    Analyzes source code and builds knowledge graph representation.
    
    Currently supports Python code analysis with AST parsing.
    """
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        """
        Initialize the code analyzer.
        
        Args:
            knowledge_graph: Knowledge graph to populate with analysis results
        """
        self.kg = knowledge_graph
        self.analyzed_files = set()
        
    def analyze_file(self, filepath: Path) -> Dict[str, any]:
        """
        Analyze a single Python file.
        
        Args:
            filepath: Path to the Python file
            
        Returns:
            Dictionary with analysis results
        """
        filepath = Path(filepath)
        
        if not filepath.exists() or filepath.suffix != '.py':
            return {'error': 'Invalid file path or not a Python file'}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                source = f.read()
                tree = ast.parse(source)
            except SyntaxError as e:
                return {'error': f'Syntax error: {e}'}
        
        module_id = str(filepath)
        self.kg.add_node(
            module_id,
            NodeType.MODULE,
            {'name': filepath.name, 'path': str(filepath)}
        )
        
        results = {
            'module': module_id,
            'classes': [],
            'functions': [],
            'imports': []
        }
        
        # Analyze module contents
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_id = f"{module_id}::{node.name}"
                self.kg.add_node(
                    class_id,
                    NodeType.CLASS,
                    {
                        'name': node.name,
                        'lineno': node.lineno,
                        'module': module_id
                    }
                )
                self.kg.add_edge(module_id, class_id, RelationType.USES)
                results['classes'].append(class_id)
                
                # Analyze class methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_id = f"{class_id}.{item.name}"
                        self.kg.add_node(
                            method_id,
                            NodeType.FUNCTION,
                            {
                                'name': item.name,
                                'lineno': item.lineno,
                                'class': class_id
                            }
                        )
                        self.kg.add_edge(class_id, method_id, RelationType.USES)
                        
            elif isinstance(node, ast.FunctionDef):
                # Only top-level functions (not methods)
                if self._is_top_level(node, tree):
                    func_id = f"{module_id}::{node.name}"
                    self.kg.add_node(
                        func_id,
                        NodeType.FUNCTION,
                        {
                            'name': node.name,
                            'lineno': node.lineno,
                            'module': module_id
                        }
                    )
                    self.kg.add_edge(module_id, func_id, RelationType.USES)
                    results['functions'].append(func_id)
                    
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    import_id = f"import::{alias.name}"
                    self.kg.add_node(
                        import_id,
                        NodeType.MODULE,
                        {'name': alias.name, 'type_detail': 'import'}
                    )
                    self.kg.add_edge(module_id, import_id, RelationType.IMPORTS)
                    results['imports'].append(alias.name)
                    
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    import_id = f"import::{node.module}"
                    self.kg.add_node(
                        import_id,
                        NodeType.MODULE,
                        {'name': node.module, 'type_detail': 'import'}
                    )
                    self.kg.add_edge(module_id, import_id, RelationType.IMPORTS)
                    results['imports'].append(node.module)
        
        self.analyzed_files.add(str(filepath))
        return results
    
    def analyze_directory(self, directory: Path, recursive: bool = True) -> Dict[str, any]:
        """
        Analyze all Python files in a directory.
        
        Args:
            directory: Path to the directory
            recursive: Whether to analyze subdirectories recursively
            
        Returns:
            Dictionary with analysis summary
        """
        directory = Path(directory)
        
        if not directory.is_dir():
            return {'error': 'Invalid directory path'}
        
        results = {
            'analyzed_files': [],
            'total_modules': 0,
            'total_classes': 0,
            'total_functions': 0
        }
        
        pattern = '**/*.py' if recursive else '*.py'
        for filepath in directory.glob(pattern):
            if filepath.is_file():
                file_result = self.analyze_file(filepath)
                if 'error' not in file_result:
                    results['analyzed_files'].append(str(filepath))
                    results['total_modules'] += 1
                    results['total_classes'] += len(file_result.get('classes', []))
                    results['total_functions'] += len(file_result.get('functions', []))
        
        return results
    
    def extract_dependencies(self, node_id: str) -> List[str]:
        """
        Extract all dependencies for a given code element.
        
        Args:
            node_id: Node identifier in the knowledge graph
            
        Returns:
            List of dependency node IDs
        """
        dependencies = []
        
        # Get direct imports
        imports = self.kg.get_neighbors(node_id, RelationType.IMPORTS)
        dependencies.extend(imports)
        
        # Get used components
        uses = self.kg.get_neighbors(node_id, RelationType.USES)
        dependencies.extend(uses)
        
        return dependencies
    
    def find_call_chain(self, start_func: str, end_func: str) -> Optional[List[str]]:
        """
        Find the call chain between two functions.
        
        Args:
            start_func: Starting function node ID
            end_func: Ending function node ID
            
        Returns:
            List of node IDs forming the call chain, or None if no chain exists
        """
        return self.kg.find_path(start_func, end_func)
    
    def _is_top_level(self, node: ast.FunctionDef, tree: ast.Module) -> bool:
        """Check if a function is defined at module level"""
        for item in tree.body:
            if item is node:
                return True
        return False
    
    def get_code_metrics(self) -> Dict[str, any]:
        """
        Get code metrics from the analyzed codebase.
        
        Returns:
            Dictionary with various code metrics
        """
        stats = self.kg.get_statistics()
        
        return {
            'total_files': len(self.analyzed_files),
            'knowledge_graph_stats': stats,
            'analyzed_files': list(self.analyzed_files)
        }
