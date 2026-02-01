"""
Example usage of Nexus platform
================================

This example demonstrates how to use Nexus to analyze code, build knowledge graphs,
visualize system flows, and get AI-powered explanations.
"""

import sys
from pathlib import Path

# Add src to path to import nexus
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from nexus import KnowledgeGraph, CodeAnalyzer, Visualizer, AITutor
from nexus.knowledge_graph import NodeType, RelationType
from nexus.ai_tutor import KnowledgeLevel


def example_basic_usage():
    """Basic usage example: Create a simple knowledge graph"""
    print("=" * 60)
    print("Example 1: Basic Knowledge Graph Creation")
    print("=" * 60)
    
    # Create a knowledge graph
    kg = KnowledgeGraph(name="example_system")
    
    # Add some nodes
    kg.add_node("auth_module", NodeType.MODULE, {"name": "authentication", "description": "User authentication"})
    kg.add_node("login_function", NodeType.FUNCTION, {"name": "login", "module": "auth_module"})
    kg.add_node("validate_function", NodeType.FUNCTION, {"name": "validate_token", "module": "auth_module"})
    kg.add_node("user_class", NodeType.CLASS, {"name": "User", "module": "auth_module"})
    
    # Add relationships
    kg.add_edge("auth_module", "login_function", RelationType.USES)
    kg.add_edge("auth_module", "validate_function", RelationType.USES)
    kg.add_edge("login_function", "validate_function", RelationType.CALLS)
    kg.add_edge("login_function", "user_class", RelationType.USES)
    
    # Get statistics
    stats = kg.get_statistics()
    print(f"\nKnowledge Graph Statistics:")
    print(f"  Nodes: {stats['num_nodes']}")
    print(f"  Edges: {stats['num_edges']}")
    print(f"  Node Types: {stats['node_types']}")
    print(f"  Relation Types: {stats['relation_types']}")
    
    return kg


def example_code_analysis():
    """Example: Analyze actual Python code"""
    print("\n" + "=" * 60)
    print("Example 2: Code Analysis")
    print("=" * 60)
    
    # Create a sample Python file to analyze
    sample_code = '''
class Calculator:
    """A simple calculator class"""
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b

def main():
    calc = Calculator()
    result = calc.add(5, 3)
    print(result)
'''
    
    # Write sample code to a temp file
    sample_file = Path("/tmp/sample_calculator.py")
    sample_file.write_text(sample_code)
    
    # Analyze the code
    kg = KnowledgeGraph(name="calculator_analysis")
    analyzer = CodeAnalyzer(kg)
    
    result = analyzer.analyze_file(sample_file)
    
    print(f"\nAnalysis Results:")
    print(f"  Module: {result['module']}")
    print(f"  Classes found: {len(result['classes'])}")
    print(f"  Functions found: {len(result['functions'])}")
    
    # Get metrics
    metrics = analyzer.get_code_metrics()
    print(f"\nCode Metrics:")
    print(f"  Total files analyzed: {metrics['total_files']}")
    print(f"  Knowledge graph nodes: {metrics['knowledge_graph_stats']['num_nodes']}")
    
    return kg


def example_visualization(kg):
    """Example: Visualize the knowledge graph"""
    print("\n" + "=" * 60)
    print("Example 3: Visualization")
    print("=" * 60)
    
    visualizer = Visualizer(kg)
    
    # Generate text report
    report = visualizer.generate_text_report()
    print("\n" + report)
    
    # Note: Visual plots would be generated here but require display
    print("\nVisualization capabilities:")
    print("  - visualize_full_graph(): Complete system overview")
    print("  - visualize_component(): Focus on specific components")
    print("  - visualize_path(): Highlight logic flows between components")


def example_ai_tutor(kg):
    """Example: Use AI tutor for explanations"""
    print("\n" + "=" * 60)
    print("Example 4: AI Tutor")
    print("=" * 60)
    
    # Create tutor with different knowledge levels
    beginner_tutor = AITutor(kg, KnowledgeLevel.BEGINNER)
    advanced_tutor = AITutor(kg, KnowledgeLevel.ADVANCED)
    
    # Get first node for explanation
    nodes = list(kg.graph.nodes())
    if nodes:
        node_id = nodes[0]
        
        print(f"\n--- Beginner Level Explanation ---")
        print(beginner_tutor.explain_node(node_id))
        
        print(f"\n--- Advanced Level Explanation ---")
        print(advanced_tutor.explain_node(node_id))
        
        # Demonstrate debugging suggestions
        if len(nodes) > 1:
            print(f"\n--- Debugging Suggestions ---")
            steps = beginner_tutor.suggest_debugging_steps(node_id, "Function not returning expected value")
            for step in steps:
                print(step)


def example_system_flow(kg):
    """Example: Analyze system flows"""
    print("\n" + "=" * 60)
    print("Example 5: System Flow Analysis")
    print("=" * 60)
    
    tutor = AITutor(kg, KnowledgeLevel.INTERMEDIATE)
    
    # Find paths between nodes
    nodes = list(kg.graph.nodes())
    if len(nodes) >= 2:
        start_node = nodes[0]
        end_node = nodes[-1]
        
        path = kg.find_path(start_node, end_node)
        if path:
            print(f"\nPath found between {start_node} and {end_node}:")
            print(f"  Path length: {len(path)} steps")
            print(f"  Path: {' → '.join(path)}")
            
            # Get AI explanation of the flow
            print(f"\n--- AI Tutor Flow Explanation ---")
            explanation = tutor.explain_system_flow(start_node, end_node)
            print(explanation)
        else:
            print(f"\nNo path found between {start_node} and {end_node}")


def example_persistence():
    """Example: Save and load knowledge graphs"""
    print("\n" + "=" * 60)
    print("Example 6: Persistence")
    print("=" * 60)
    
    # Create and save a knowledge graph
    kg = KnowledgeGraph(name="persistent_example")
    kg.add_node("node1", NodeType.FUNCTION, {"name": "example_function"})
    kg.add_node("node2", NodeType.CLASS, {"name": "ExampleClass"})
    kg.add_edge("node1", "node2", RelationType.USES)
    
    save_path = Path("/tmp/example_graph.nexus")
    kg.save(save_path)
    print(f"\nKnowledge graph saved to: {save_path}")
    
    # Load it back
    loaded_kg = KnowledgeGraph.load(save_path)
    print(f"Knowledge graph loaded successfully")
    print(f"  Nodes: {loaded_kg.graph.number_of_nodes()}")
    print(f"  Edges: {loaded_kg.graph.number_of_edges()}")
    
    return loaded_kg


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Nexus: AI-Powered Cognitive Platform".center(58) + "║")
    print("║" + "  Demonstrating Core Functionality".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    
    # Run examples
    kg1 = example_basic_usage()
    kg2 = example_code_analysis()
    example_visualization(kg1)
    example_ai_tutor(kg1)
    example_system_flow(kg1)
    example_persistence()
    
    print("\n" + "=" * 60)
    print("Examples completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Use 'nexus analyze <path>' to analyze your own codebase")
    print("  2. Use 'nexus visualize <graph>' to visualize knowledge graphs")
    print("  3. Use 'nexus explain <graph> <node>' to get AI explanations")
    print("  4. Check the documentation for more advanced features")
    print()


if __name__ == '__main__':
    main()
