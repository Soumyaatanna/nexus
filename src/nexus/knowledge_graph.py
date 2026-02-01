"""
Knowledge Graph Module
======================

Builds and maintains a persistent knowledge graph connecting:
- Code elements (functions, classes, modules)
- Architecture components
- Design decisions
"""

import networkx as nx
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum


class NodeType(Enum):
    """Types of nodes in the knowledge graph"""
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"
    VARIABLE = "variable"
    DESIGN_DECISION = "design_decision"
    ARCHITECTURE_COMPONENT = "architecture_component"


class RelationType(Enum):
    """Types of relationships in the knowledge graph"""
    CALLS = "calls"
    INHERITS = "inherits"
    IMPORTS = "imports"
    USES = "uses"
    IMPLEMENTS = "implements"
    DEPENDS_ON = "depends_on"
    DOCUMENTS = "documents"


class KnowledgeGraph:
    """
    Persistent knowledge graph for connecting code, architecture, and design decisions.
    
    This class provides the foundation for building a living system that understands
    the codebase structure, relationships, and design decisions.
    """
    
    def __init__(self, name: str = "default"):
        """
        Initialize a new knowledge graph.
        
        Args:
            name: Name identifier for this knowledge graph
        """
        self.name = name
        self.graph = nx.DiGraph()
        self._node_counter = 0
        
    def add_node(
        self, 
        node_id: str,
        node_type: NodeType,
        properties: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add a node to the knowledge graph.
        
        Args:
            node_id: Unique identifier for the node
            node_type: Type of the node
            properties: Additional properties/metadata
            
        Returns:
            The node_id that was added
        """
        props = properties or {}
        props['type'] = node_type.value
        self.graph.add_node(node_id, **props)
        return node_id
    
    def add_edge(
        self,
        source: str,
        target: str,
        relation_type: RelationType,
        properties: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, str]:
        """
        Add an edge (relationship) between two nodes.
        
        Args:
            source: Source node ID
            target: Target node ID
            relation_type: Type of relationship
            properties: Additional properties/metadata
            
        Returns:
            Tuple of (source, target) node IDs
        """
        props = properties or {}
        props['relation'] = relation_type.value
        self.graph.add_edge(source, target, **props)
        return (source, target)
    
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a node and its properties.
        
        Args:
            node_id: Node identifier
            
        Returns:
            Dictionary of node properties or None if not found
        """
        if node_id in self.graph:
            return dict(self.graph.nodes[node_id])
        return None
    
    def get_neighbors(
        self, 
        node_id: str, 
        relation_type: Optional[RelationType] = None
    ) -> List[str]:
        """
        Get neighboring nodes connected to the given node.
        
        Args:
            node_id: Node identifier
            relation_type: Filter by specific relation type
            
        Returns:
            List of neighboring node IDs
        """
        if node_id not in self.graph:
            return []
        
        neighbors = []
        for neighbor in self.graph.neighbors(node_id):
            edge_data = self.graph.edges[node_id, neighbor]
            if relation_type is None or edge_data.get('relation') == relation_type.value:
                neighbors.append(neighbor)
        
        return neighbors
    
    def find_path(self, source: str, target: str) -> Optional[List[str]]:
        """
        Find a path between two nodes in the graph.
        
        Args:
            source: Source node ID
            target: Target node ID
            
        Returns:
            List of node IDs forming the path, or None if no path exists
        """
        try:
            return nx.shortest_path(self.graph, source, target)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None
    
    def get_connected_component(self, node_id: str) -> Set[str]:
        """
        Get all nodes in the connected component containing the given node.
        
        Args:
            node_id: Node identifier
            
        Returns:
            Set of node IDs in the same connected component
        """
        if node_id not in self.graph:
            return set()
        
        # For directed graphs, use weakly connected components
        undirected = self.graph.to_undirected()
        for component in nx.connected_components(undirected):
            if node_id in component:
                return component
        return set()
    
    def search_nodes(
        self, 
        node_type: Optional[NodeType] = None,
        **filters
    ) -> List[str]:
        """
        Search for nodes matching criteria.
        
        Args:
            node_type: Filter by node type
            **filters: Additional property filters
            
        Returns:
            List of matching node IDs
        """
        results = []
        for node_id, attrs in self.graph.nodes(data=True):
            if node_type and attrs.get('type') != node_type.value:
                continue
            
            match = True
            for key, value in filters.items():
                if attrs.get(key) != value:
                    match = False
                    break
            
            if match:
                results.append(node_id)
        
        return results
    
    def save(self, filepath: Path) -> None:
        """
        Save the knowledge graph to disk.
        
        Args:
            filepath: Path to save the graph
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'name': self.name,
            'graph': self.graph,
            'node_counter': self._node_counter
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    @classmethod
    def load(cls, filepath: Path) -> 'KnowledgeGraph':
        """
        Load a knowledge graph from disk.
        
        Args:
            filepath: Path to load the graph from
            
        Returns:
            Loaded KnowledgeGraph instance
        """
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        kg = cls(name=data['name'])
        kg.graph = data['graph']
        kg._node_counter = data['node_counter']
        
        return kg
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge graph.
        
        Returns:
            Dictionary with graph statistics
        """
        return {
            'num_nodes': self.graph.number_of_nodes(),
            'num_edges': self.graph.number_of_edges(),
            'node_types': self._count_node_types(),
            'relation_types': self._count_relation_types(),
            'density': nx.density(self.graph),
        }
    
    def _count_node_types(self) -> Dict[str, int]:
        """Count nodes by type"""
        counts = {}
        for _, attrs in self.graph.nodes(data=True):
            node_type = attrs.get('type', 'unknown')
            counts[node_type] = counts.get(node_type, 0) + 1
        return counts
    
    def _count_relation_types(self) -> Dict[str, int]:
        """Count edges by relation type"""
        counts = {}
        for _, _, attrs in self.graph.edges(data=True):
            rel_type = attrs.get('relation', 'unknown')
            counts[rel_type] = counts.get(rel_type, 0) + 1
        return counts
