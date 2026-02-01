# Nexus Quick Reference Guide

## Core Concepts

### Knowledge Graph
The knowledge graph is the central data structure in Nexus. It represents your codebase as a directed graph where:
- **Nodes** represent code elements (functions, classes, modules, etc.)
- **Edges** represent relationships (calls, imports, uses, inherits, etc.)

### Node Types
- `FUNCTION`: A function or method
- `CLASS`: A class definition
- `MODULE`: A Python module (file)
- `VARIABLE`: A variable or constant
- `DESIGN_DECISION`: A documented design decision
- `ARCHITECTURE_COMPONENT`: An architectural component

### Relation Types
- `CALLS`: Function A calls function B
- `INHERITS`: Class A inherits from class B
- `IMPORTS`: Module A imports module B
- `USES`: Component A uses component B
- `IMPLEMENTS`: Class A implements interface B
- `DEPENDS_ON`: Component A depends on component B

## CLI Quick Start

```bash
# Analyze code
nexus analyze src/ --recursive --output project.nexus

# Visualize
nexus visualize project.nexus --output graph.png

# Get explanations
nexus explain project.nexus "node_id" --level intermediate

# Generate report
nexus report project.nexus --output report.txt
```

## Python API Quick Start

```python
from nexus import KnowledgeGraph, CodeAnalyzer, Visualizer, AITutor

# Create and analyze
kg = KnowledgeGraph(name="my_project")
analyzer = CodeAnalyzer(kg)
analyzer.analyze_directory("src/", recursive=True)

# Visualize
visualizer = Visualizer(kg)
visualizer.visualize_full_graph(output_path="graph.png")

# Get AI explanations
tutor = AITutor(kg)
explanation = tutor.explain_node("my_function")
```

See README.md for full documentation.
