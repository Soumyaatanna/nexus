"""
CLI Module
==========

Command-line interface for interacting with Nexus.
"""

import argparse
import sys
from pathlib import Path
from .knowledge_graph import KnowledgeGraph
from .code_analyzer import CodeAnalyzer
from .visualizer import Visualizer
from .ai_tutor import AITutor, KnowledgeLevel


def main():
    """Main entry point for the Nexus CLI"""
    parser = argparse.ArgumentParser(
        description="Nexus - AI-Powered Cognitive Platform for Understanding Software Systems"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a codebase')
    analyze_parser.add_argument('path', type=str, help='Path to code file or directory')
    analyze_parser.add_argument('--output', '-o', type=str, help='Output path for knowledge graph')
    analyze_parser.add_argument('--recursive', '-r', action='store_true', help='Analyze directory recursively')
    
    # Visualize command
    viz_parser = subparsers.add_parser('visualize', help='Visualize knowledge graph')
    viz_parser.add_argument('graph', type=str, help='Path to knowledge graph file')
    viz_parser.add_argument('--output', '-o', type=str, help='Output path for visualization')
    viz_parser.add_argument('--mode', choices=['full', 'component', 'path'], default='full',
                           help='Visualization mode')
    viz_parser.add_argument('--node', type=str, help='Node ID for component/path visualization')
    viz_parser.add_argument('--target', type=str, help='Target node ID for path visualization')
    
    # Explain command
    explain_parser = subparsers.add_parser('explain', help='Get AI tutor explanations')
    explain_parser.add_argument('graph', type=str, help='Path to knowledge graph file')
    explain_parser.add_argument('node', type=str, help='Node ID to explain')
    explain_parser.add_argument('--level', choices=['beginner', 'intermediate', 'advanced'],
                               default='intermediate', help='Knowledge level')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate knowledge graph report')
    report_parser.add_argument('graph', type=str, help='Path to knowledge graph file')
    report_parser.add_argument('--output', '-o', type=str, help='Output path for report')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        if args.command == 'analyze':
            return cmd_analyze(args)
        elif args.command == 'visualize':
            return cmd_visualize(args)
        elif args.command == 'explain':
            return cmd_explain(args)
        elif args.command == 'report':
            return cmd_report(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def cmd_analyze(args):
    """Handle analyze command"""
    path = Path(args.path)
    
    if not path.exists():
        print(f"Error: Path '{path}' does not exist", file=sys.stderr)
        return 1
    
    print(f"Analyzing: {path}")
    
    # Create knowledge graph
    kg = KnowledgeGraph(name=path.name)
    analyzer = CodeAnalyzer(kg)
    
    # Analyze
    if path.is_file():
        result = analyzer.analyze_file(path)
    else:
        result = analyzer.analyze_directory(path, recursive=args.recursive)
    
    if 'error' in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1
    
    # Print results
    metrics = analyzer.get_code_metrics()
    print(f"\nAnalysis complete!")
    print(f"Files analyzed: {metrics['total_files']}")
    print(f"Nodes in graph: {metrics['knowledge_graph_stats']['num_nodes']}")
    print(f"Edges in graph: {metrics['knowledge_graph_stats']['num_edges']}")
    
    # Save knowledge graph
    output_path = args.output or f"{path.name}.nexus"
    kg.save(output_path)
    print(f"\nKnowledge graph saved to: {output_path}")
    
    return 0


def cmd_visualize(args):
    """Handle visualize command"""
    graph_path = Path(args.graph)
    
    if not graph_path.exists():
        print(f"Error: Knowledge graph '{graph_path}' does not exist", file=sys.stderr)
        return 1
    
    print(f"Loading knowledge graph: {graph_path}")
    kg = KnowledgeGraph.load(graph_path)
    
    visualizer = Visualizer(kg)
    
    if args.mode == 'full':
        print("Generating full graph visualization...")
        visualizer.visualize_full_graph(output_path=args.output)
    
    elif args.mode == 'component':
        if not args.node:
            print("Error: --node is required for component visualization", file=sys.stderr)
            return 1
        print(f"Generating component visualization for: {args.node}")
        visualizer.visualize_component(args.node, output_path=args.output)
    
    elif args.mode == 'path':
        if not args.node or not args.target:
            print("Error: --node and --target are required for path visualization", file=sys.stderr)
            return 1
        print(f"Generating path visualization: {args.node} → {args.target}")
        visualizer.visualize_path(args.node, args.target, output_path=args.output)
    
    return 0


def cmd_explain(args):
    """Handle explain command"""
    graph_path = Path(args.graph)
    
    if not graph_path.exists():
        print(f"Error: Knowledge graph '{graph_path}' does not exist", file=sys.stderr)
        return 1
    
    print(f"Loading knowledge graph: {graph_path}")
    kg = KnowledgeGraph.load(graph_path)
    
    tutor = AITutor(kg, knowledge_level=args.level)
    
    print(f"\nExplanation for '{args.node}':")
    print("-" * 50)
    explanation = tutor.explain_node(args.node)
    print(explanation)
    
    return 0


def cmd_report(args):
    """Handle report command"""
    graph_path = Path(args.graph)
    
    if not graph_path.exists():
        print(f"Error: Knowledge graph '{graph_path}' does not exist", file=sys.stderr)
        return 1
    
    print(f"Loading knowledge graph: {graph_path}")
    kg = KnowledgeGraph.load(graph_path)
    
    visualizer = Visualizer(kg)
    report = visualizer.generate_text_report(output_path=args.output)
    
    if not args.output:
        print("\n" + report)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
