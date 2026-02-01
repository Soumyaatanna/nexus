"""
Visualizer Module
=================

Visualizes system flows and highlights relevant logic paths.
Generates visual representations of the knowledge graph.
"""

import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path
from typing import List, Optional, Set
from .knowledge_graph import KnowledgeGraph, NodeType, RelationType


class Visualizer:
    """
    Visualizes knowledge graphs and system flows.
    
    Highlights relevant logic paths to reduce complexity and improve understanding.
    """
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        """
        Initialize the visualizer.
        
        Args:
            knowledge_graph: Knowledge graph to visualize
        """
        self.kg = knowledge_graph
        
    def visualize_full_graph(
        self, 
        output_path: Optional[Path] = None,
        figsize: tuple = (12, 8)
    ) -> None:
        """
        Visualize the entire knowledge graph.
        
        Args:
            output_path: Path to save the visualization (if None, displays interactively)
            figsize: Figure size for the plot
        """
        if self.kg.graph.number_of_nodes() == 0:
            print("Knowledge graph is empty. Nothing to visualize.")
            return
        
        plt.figure(figsize=figsize)
        
        # Create layout
        pos = nx.spring_layout(self.kg.graph, k=0.5, iterations=50)
        
        # Color nodes by type
        node_colors = self._get_node_colors()
        
        # Draw the graph
        nx.draw(
            self.kg.graph,
            pos,
            node_color=node_colors,
            with_labels=True,
            node_size=500,
            font_size=8,
            font_weight='bold',
            arrows=True,
            edge_color='gray',
            alpha=0.7
        )
        
        plt.title(f"Knowledge Graph: {self.kg.name}")
        
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def visualize_component(
        self,
        node_id: str,
        depth: int = 2,
        output_path: Optional[Path] = None,
        figsize: tuple = (10, 6)
    ) -> None:
        """
        Visualize a specific component and its neighborhood.
        
        Args:
            node_id: Central node to visualize around
            depth: How many levels of neighbors to include
            output_path: Path to save the visualization
            figsize: Figure size for the plot
        """
        if node_id not in self.kg.graph:
            print(f"Node '{node_id}' not found in knowledge graph.")
            return
        
        # Get subgraph around the node
        nodes = self._get_neighborhood(node_id, depth)
        subgraph = self.kg.graph.subgraph(nodes)
        
        if subgraph.number_of_nodes() == 0:
            print(f"No nodes found in neighborhood of '{node_id}'.")
            return
        
        plt.figure(figsize=figsize)
        
        # Create layout
        pos = nx.spring_layout(subgraph, k=0.5, iterations=50)
        
        # Highlight the central node
        node_colors = []
        for node in subgraph.nodes():
            if node == node_id:
                node_colors.append('red')
            else:
                node_colors.append(self._get_color_for_node(node))
        
        # Draw the graph
        nx.draw(
            subgraph,
            pos,
            node_color=node_colors,
            with_labels=True,
            node_size=700,
            font_size=9,
            font_weight='bold',
            arrows=True,
            edge_color='gray',
            alpha=0.8
        )
        
        plt.title(f"Component View: {node_id}")
        
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Component visualization saved to {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def visualize_path(
        self,
        start_node: str,
        end_node: str,
        output_path: Optional[Path] = None,
        figsize: tuple = (10, 6)
    ) -> None:
        """
        Visualize the path between two nodes, highlighting the logic flow.
        
        Args:
            start_node: Starting node ID
            end_node: Ending node ID
            output_path: Path to save the visualization
            figsize: Figure size for the plot
        """
        path = self.kg.find_path(start_node, end_node)
        
        if not path:
            print(f"No path found between '{start_node}' and '{end_node}'.")
            return
        
        # Get all nodes along the path plus some context
        nodes_to_show = set(path)
        for node in path:
            neighbors = list(self.kg.graph.predecessors(node)) + list(self.kg.graph.successors(node))
            nodes_to_show.update(neighbors[:3])  # Add a few neighbors for context
        
        subgraph = self.kg.graph.subgraph(nodes_to_show)
        
        plt.figure(figsize=figsize)
        
        # Create layout
        pos = nx.spring_layout(subgraph, k=0.5, iterations=50)
        
        # Color nodes: path nodes in red, others in default colors
        node_colors = []
        for node in subgraph.nodes():
            if node in path:
                node_colors.append('red')
            else:
                node_colors.append('lightblue')
        
        # Draw all edges in gray first
        nx.draw_networkx_edges(
            subgraph,
            pos,
            edge_color='gray',
            alpha=0.3,
            arrows=True
        )
        
        # Highlight path edges in red
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(
            subgraph,
            pos,
            edgelist=path_edges,
            edge_color='red',
            width=2,
            alpha=0.8,
            arrows=True
        )
        
        # Draw nodes
        nx.draw_networkx_nodes(
            subgraph,
            pos,
            node_color=node_colors,
            node_size=700,
            alpha=0.8
        )
        
        # Draw labels
        nx.draw_networkx_labels(
            subgraph,
            pos,
            font_size=9,
            font_weight='bold'
        )
        
        plt.title(f"Logic Path: {start_node} → {end_node}")
        plt.axis('off')
        
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Path visualization saved to {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def generate_text_report(self, output_path: Optional[Path] = None) -> str:
        """
        Generate a text report of the knowledge graph structure.
        
        Args:
            output_path: Path to save the report (if None, returns as string)
            
        Returns:
            Text report as string
        """
        stats = self.kg.get_statistics()
        
        report_lines = [
            f"Knowledge Graph Report: {self.kg.name}",
            "=" * 50,
            "",
            "Statistics:",
            f"  Total Nodes: {stats['num_nodes']}",
            f"  Total Edges: {stats['num_edges']}",
            f"  Graph Density: {stats['density']:.4f}",
            "",
            "Node Types:",
        ]
        
        for node_type, count in stats['node_types'].items():
            report_lines.append(f"  {node_type}: {count}")
        
        report_lines.append("")
        report_lines.append("Relation Types:")
        
        for rel_type, count in stats['relation_types'].items():
            report_lines.append(f"  {rel_type}: {count}")
        
        report = "\n".join(report_lines)
        
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(report)
            print(f"Report saved to {output_path}")
        
        return report
    
    def _get_neighborhood(self, node_id: str, depth: int) -> Set[str]:
        """Get all nodes within depth levels from the given node"""
        nodes = {node_id}
        current_level = {node_id}
        
        for _ in range(depth):
            next_level = set()
            for node in current_level:
                # Add predecessors and successors
                next_level.update(self.kg.graph.predecessors(node))
                next_level.update(self.kg.graph.successors(node))
            
            nodes.update(next_level)
            current_level = next_level
        
        return nodes
    
    def _get_node_colors(self) -> List[str]:
        """Get colors for all nodes based on their type"""
        colors = []
        for node_id in self.kg.graph.nodes():
            colors.append(self._get_color_for_node(node_id))
        return colors
    
    def _get_color_for_node(self, node_id: str) -> str:
        """Get color for a specific node based on its type"""
        node_attrs = self.kg.graph.nodes[node_id]
        node_type = node_attrs.get('type', 'unknown')
        
        color_map = {
            NodeType.FUNCTION.value: 'lightblue',
            NodeType.CLASS.value: 'lightgreen',
            NodeType.MODULE.value: 'lightyellow',
            NodeType.VARIABLE.value: 'lightcoral',
            NodeType.DESIGN_DECISION.value: 'plum',
            NodeType.ARCHITECTURE_COMPONENT.value: 'wheat',
        }
        
        return color_map.get(node_type, 'lightgray')
