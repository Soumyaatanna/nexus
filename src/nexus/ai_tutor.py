"""
AI Tutor Module
===============

Provides adaptive AI tutoring for explaining concepts and debugging steps.
Adjusts explanations based on user's knowledge level.
"""

from typing import Dict, List, Optional
from .knowledge_graph import KnowledgeGraph, NodeType


class KnowledgeLevel:
    """Represents a user's knowledge level"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class AITutor:
    """
    Adaptive AI tutor that explains concepts and debugging steps.
    
    Tailors explanations based on the user's knowledge level and provides
    contextual information from the knowledge graph.
    """
    
    def __init__(self, knowledge_graph: KnowledgeGraph, knowledge_level: str = KnowledgeLevel.INTERMEDIATE):
        """
        Initialize the AI tutor.
        
        Args:
            knowledge_graph: Knowledge graph for contextual information
            knowledge_level: User's knowledge level (beginner/intermediate/advanced)
        """
        self.kg = knowledge_graph
        self.knowledge_level = knowledge_level
        self.conversation_history = []
        
    def explain_node(self, node_id: str) -> str:
        """
        Explain a specific code element from the knowledge graph.
        
        Args:
            node_id: Node identifier to explain
            
        Returns:
            Explanation text tailored to user's knowledge level
        """
        node = self.kg.get_node(node_id)
        
        if not node:
            return f"Node '{node_id}' not found in the knowledge graph."
        
        node_type = node.get('type', 'unknown')
        name = node.get('name', node_id)
        
        # Generate explanation based on knowledge level
        if self.knowledge_level == KnowledgeLevel.BEGINNER:
            explanation = self._explain_for_beginner(node_id, node_type, name, node)
        elif self.knowledge_level == KnowledgeLevel.ADVANCED:
            explanation = self._explain_for_advanced(node_id, node_type, name, node)
        else:
            explanation = self._explain_for_intermediate(node_id, node_type, name, node)
        
        self.conversation_history.append({
            'type': 'explanation',
            'node_id': node_id,
            'response': explanation
        })
        
        return explanation
    
    def explain_relationship(self, source: str, target: str) -> str:
        """
        Explain the relationship between two code elements.
        
        Args:
            source: Source node ID
            target: Target node ID
            
        Returns:
            Explanation of the relationship
        """
        if source not in self.kg.graph or target not in self.kg.graph:
            return "One or both nodes not found in the knowledge graph."
        
        if not self.kg.graph.has_edge(source, target):
            return f"No direct relationship found between '{source}' and '{target}'."
        
        edge_data = self.kg.graph.edges[source, target]
        relation_type = edge_data.get('relation', 'unknown')
        
        source_node = self.kg.get_node(source)
        target_node = self.kg.get_node(target)
        
        source_name = source_node.get('name', source)
        target_name = target_node.get('name', target)
        
        # Build explanation
        if self.knowledge_level == KnowledgeLevel.BEGINNER:
            explanation = (
                f"Let me explain the connection:\n\n"
                f"{source_name} {relation_type} {target_name}\n\n"
                f"This means that {source_name} has a '{relation_type}' relationship with {target_name}. "
                f"In simpler terms, {source_name} depends on or uses {target_name} in some way."
            )
        elif self.knowledge_level == KnowledgeLevel.ADVANCED:
            explanation = (
                f"Relationship Analysis:\n"
                f"Source: {source} (type: {source_node.get('type')})\n"
                f"Target: {target} (type: {target_node.get('type')})\n"
                f"Relation: {relation_type}\n"
                f"Edge Properties: {edge_data}"
            )
        else:
            explanation = (
                f"The relationship between {source_name} and {target_name}:\n\n"
                f"- Type: {relation_type}\n"
                f"- {source_name} ({source_node.get('type')}) {relation_type} {target_name} ({target_node.get('type')})\n"
                f"- This indicates that {source_name} has a dependency or interaction with {target_name}."
            )
        
        self.conversation_history.append({
            'type': 'relationship',
            'source': source,
            'target': target,
            'response': explanation
        })
        
        return explanation
    
    def suggest_debugging_steps(self, node_id: str, issue_description: str = "") -> List[str]:
        """
        Suggest debugging steps for a specific code element.
        
        Args:
            node_id: Node identifier to debug
            issue_description: Optional description of the issue
            
        Returns:
            List of debugging steps
        """
        node = self.kg.get_node(node_id)
        
        if not node:
            return [f"Node '{node_id}' not found. Please verify the identifier."]
        
        node_type = node.get('type', 'unknown')
        steps = []
        
        # General debugging steps
        if self.knowledge_level == KnowledgeLevel.BEGINNER:
            steps.extend([
                f"1. First, let's understand what {node.get('name', node_id)} does",
                "2. Check if the inputs to this component are correct",
                "3. Add print statements to see what's happening",
                "4. Run the code step by step to identify where it breaks"
            ])
        else:
            steps.extend([
                f"1. Review the implementation of {node.get('name', node_id)}",
                "2. Trace the data flow and check input validation",
                "3. Examine dependencies and their states",
                "4. Use a debugger to inspect runtime values"
            ])
        
        # Type-specific steps
        if node_type == NodeType.FUNCTION.value:
            # Get function dependencies
            dependencies = self.kg.get_neighbors(node_id)
            if dependencies:
                steps.append(f"5. Check these dependencies: {', '.join([self.kg.get_node(d).get('name', d) for d in dependencies[:3]])}")
        
        elif node_type == NodeType.CLASS.value:
            # Get class methods
            methods = self.kg.get_neighbors(node_id)
            if methods:
                steps.append(f"5. Review the class methods: {', '.join([self.kg.get_node(m).get('name', m) for m in methods[:3]])}")
        
        # Add issue-specific guidance
        if issue_description:
            steps.append(f"6. Focus on: {issue_description}")
        
        return steps
    
    def explain_system_flow(self, start_node: str, end_node: str) -> str:
        """
        Explain the flow between two components in the system.
        
        Args:
            start_node: Starting node ID
            end_node: Ending node ID
            
        Returns:
            Explanation of the system flow
        """
        path = self.kg.find_path(start_node, end_node)
        
        if not path:
            return f"No flow path found between '{start_node}' and '{end_node}'."
        
        # Build flow explanation
        explanation_parts = [
            f"System Flow from {start_node} to {end_node}:\n",
            f"Path length: {len(path)} steps\n"
        ]
        
        if self.knowledge_level == KnowledgeLevel.BEGINNER:
            explanation_parts.append("\nLet me walk you through this step by step:\n")
            for i, node in enumerate(path, 1):
                node_data = self.kg.get_node(node)
                name = node_data.get('name', node)
                explanation_parts.append(f"{i}. {name}")
        else:
            explanation_parts.append("\nFlow path:\n")
            for i in range(len(path) - 1):
                current = path[i]
                next_node = path[i + 1]
                
                current_data = self.kg.get_node(current)
                next_data = self.kg.get_node(next_node)
                
                edge_data = self.kg.graph.edges[current, next_node]
                relation = edge_data.get('relation', 'connects to')
                
                explanation_parts.append(
                    f"{i+1}. {current_data.get('name', current)} "
                    f"--[{relation}]--> "
                    f"{next_data.get('name', next_node)}"
                )
        
        return "\n".join(explanation_parts)
    
    def set_knowledge_level(self, level: str) -> None:
        """
        Update the user's knowledge level.
        
        Args:
            level: New knowledge level (beginner/intermediate/advanced)
        """
        if level not in [KnowledgeLevel.BEGINNER, KnowledgeLevel.INTERMEDIATE, KnowledgeLevel.ADVANCED]:
            raise ValueError(f"Invalid knowledge level: {level}")
        
        self.knowledge_level = level
        self.conversation_history.append({
            'type': 'level_change',
            'new_level': level
        })
    
    def get_conversation_history(self) -> List[Dict]:
        """
        Get the conversation history.
        
        Returns:
            List of conversation entries
        """
        return self.conversation_history
    
    def _explain_for_beginner(self, node_id: str, node_type: str, name: str, node: Dict) -> str:
        """Generate beginner-level explanation"""
        type_explanations = {
            NodeType.FUNCTION.value: "a function (a reusable piece of code that does a specific task)",
            NodeType.CLASS.value: "a class (a blueprint for creating objects with related data and behavior)",
            NodeType.MODULE.value: "a module (a file containing Python code)",
            NodeType.VARIABLE.value: "a variable (a named container for storing data)",
        }
        
        type_desc = type_explanations.get(node_type, "a code element")
        
        explanation = f"'{name}' is {type_desc}.\n\n"
        
        # Add location info if available
        if 'lineno' in node:
            explanation += f"You can find it at line {node['lineno']} in the code.\n\n"
        
        # Add simple relationship info
        neighbors = list(self.kg.graph.neighbors(node_id))
        if neighbors:
            explanation += f"It connects to {len(neighbors)} other component(s) in the system."
        
        return explanation
    
    def _explain_for_intermediate(self, node_id: str, node_type: str, name: str, node: Dict) -> str:
        """Generate intermediate-level explanation"""
        explanation = f"Component: {name}\nType: {node_type}\n\n"
        
        if 'lineno' in node:
            explanation += f"Location: Line {node['lineno']}\n"
        
        if 'module' in node:
            explanation += f"Module: {node['module']}\n"
        
        # Dependencies
        dependencies = self.kg.get_neighbors(node_id)
        if dependencies:
            explanation += f"\nDependencies ({len(dependencies)}):\n"
            for dep in dependencies[:5]:
                dep_node = self.kg.get_node(dep)
                explanation += f"  - {dep_node.get('name', dep)}\n"
        
        return explanation
    
    def _explain_for_advanced(self, node_id: str, node_type: str, name: str, node: Dict) -> str:
        """Generate advanced-level explanation"""
        explanation = f"Node ID: {node_id}\n"
        explanation += f"Type: {node_type}\n"
        explanation += f"Properties: {node}\n\n"
        
        # Detailed graph analysis
        in_degree = self.kg.graph.in_degree(node_id)
        out_degree = self.kg.graph.out_degree(node_id)
        
        explanation += f"Graph Metrics:\n"
        explanation += f"  In-degree: {in_degree}\n"
        explanation += f"  Out-degree: {out_degree}\n"
        
        # Connected component size
        component = self.kg.get_connected_component(node_id)
        explanation += f"  Connected component size: {len(component)}\n"
        
        return explanation
