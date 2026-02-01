# Nexus - AI-Powered Cognitive Platform

Nexus is an AI-powered cognitive platform that helps developers understand complex software systems, not just write code. It builds a persistent knowledge graph connecting code, architecture, and design decisions. Nexus visualizes system flows and highlights only relevant logic paths to reduce complexity. An adaptive AI tutor explains concepts and debugging steps based on the user's knowledge level, transforming static codebases into living systems that enable deeper understanding.

## Features

### 🧠 Knowledge Graph
- **Persistent Storage**: Build and maintain a persistent knowledge graph that connects code elements, architecture components, and design decisions
- **Relationship Tracking**: Automatically extract and track relationships like function calls, class inheritance, imports, and dependencies
- **Component Discovery**: Search and query the knowledge graph to find specific components or patterns

### 📊 Visualization
- **System Flow Diagrams**: Visualize entire system architecture and component relationships
- **Logic Path Highlighting**: Focus on specific logic paths to reduce cognitive load and complexity
- **Component Views**: Zoom into specific components and their immediate neighborhood
- **Path Visualization**: See the complete flow between any two components in the system

### 🎓 AI Tutor
- **Adaptive Explanations**: Get explanations tailored to your knowledge level (beginner, intermediate, advanced)
- **Contextual Learning**: Understand code elements with context from the knowledge graph
- **Debugging Assistance**: Receive step-by-step debugging suggestions based on system understanding
- **Flow Analysis**: Understand how data and control flow through the system

### 🔍 Code Analysis
- **AST-based Analysis**: Parse and understand Python code structure using Abstract Syntax Trees
- **Automatic Graph Building**: Automatically populate knowledge graphs from source code
- **Dependency Extraction**: Identify and track all dependencies in your codebase
- **Metrics & Statistics**: Get insights into your codebase structure and complexity

## Installation

```bash
# Clone the repository
git clone https://github.com/Soumyaatanna/naxus.git
cd naxus

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Quick Start

### Analyze a Codebase

```bash
# Analyze a single file
nexus analyze path/to/file.py --output my_project.nexus

# Analyze a directory recursively
nexus analyze path/to/project/ --recursive --output my_project.nexus
```

### Visualize the Knowledge Graph

```bash
# Visualize the entire graph
nexus visualize my_project.nexus --output graph.png

# Visualize a specific component
nexus visualize my_project.nexus --mode component --node "module::function" --output component.png

# Visualize the path between two components
nexus visualize my_project.nexus --mode path --node "start_func" --target "end_func" --output path.png
```

### Get AI Explanations

```bash
# Get explanation for a code element
nexus explain my_project.nexus "module::function" --level intermediate

# Adjust knowledge level
nexus explain my_project.nexus "module::Class" --level beginner
```

### Generate Reports

```bash
# Generate a text report
nexus report my_project.nexus --output report.txt
```

## Programmatic Usage

```python
from nexus import KnowledgeGraph, CodeAnalyzer, Visualizer, AITutor
from nexus.knowledge_graph import NodeType, RelationType
from nexus.ai_tutor import KnowledgeLevel

# Create a knowledge graph
kg = KnowledgeGraph(name="my_system")

# Add nodes and edges manually
kg.add_node("auth_module", NodeType.MODULE, {"name": "authentication"})
kg.add_node("login_function", NodeType.FUNCTION, {"name": "login"})
kg.add_edge("auth_module", "login_function", RelationType.USES)

# Analyze code automatically
analyzer = CodeAnalyzer(kg)
analyzer.analyze_directory("path/to/code/", recursive=True)

# Visualize the graph
visualizer = Visualizer(kg)
visualizer.visualize_full_graph(output_path="graph.png")
visualizer.visualize_path("start_node", "end_node", output_path="path.png")

# Get AI tutor explanations
tutor = AITutor(kg, knowledge_level=KnowledgeLevel.INTERMEDIATE)
explanation = tutor.explain_node("module::function")
print(explanation)

# Get debugging suggestions
steps = tutor.suggest_debugging_steps("problematic_function", "Returns None unexpectedly")
for step in steps:
    print(step)

# Save the knowledge graph
kg.save("my_system.nexus")

# Load it later
loaded_kg = KnowledgeGraph.load("my_system.nexus")
```

## Architecture

Nexus is composed of four core modules:

1. **Knowledge Graph** (`knowledge_graph.py`): Core data structure for representing code relationships
2. **Code Analyzer** (`code_analyzer.py`): Analyzes source code and populates the knowledge graph
3. **Visualizer** (`visualizer.py`): Generates visual representations of the knowledge graph
4. **AI Tutor** (`ai_tutor.py`): Provides adaptive explanations and debugging assistance

## Examples

Check out the `examples/` directory for comprehensive examples:

```bash
# Run the demo
python examples/demo.py
```

This demonstrates:
- Creating knowledge graphs
- Analyzing code
- Visualizing systems
- Using the AI tutor
- Persistence

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

### Project Structure

```
naxus/
├── src/nexus/           # Main package
│   ├── __init__.py
│   ├── knowledge_graph.py
│   ├── code_analyzer.py
│   ├── visualizer.py
│   ├── ai_tutor.py
│   └── cli.py
├── tests/               # Test suite
├── examples/            # Example scripts
├── setup.py            # Package configuration
└── requirements.txt    # Dependencies
```

## Use Cases

- **Onboarding**: Help new developers understand complex codebases quickly
- **Code Review**: Visualize impact of changes across the system
- **Debugging**: Trace execution paths and identify problematic flows
- **Refactoring**: Understand dependencies before making changes
- **Documentation**: Generate living documentation that stays in sync with code
- **Learning**: Adaptive explanations help developers learn at their own pace

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Roadmap

- [ ] Support for additional programming languages (JavaScript, Java, Go)
- [ ] Interactive web-based visualization
- [ ] Integration with popular IDEs
- [ ] Machine learning-based code pattern detection
- [ ] Collaborative knowledge graph editing
- [ ] Real-time code change tracking
- [ ] Advanced debugging with execution trace integration
