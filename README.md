# Nexus Cognitive Command Center

AI-powered cognitive platform that helps developers understand complex software systems through intelligent code analysis and visualization. Nexus builds a persistent knowledge graph connecting code, architecture, and design decisions while transforming static codebases into intelligent, interactive development environments.

## Overview

Nexus is a microservices-based system that provides:
- **Real-time Code Analysis**: Parse and understand code structure
- **Intelligent Documentation**: Auto-generate API documentation
- **Semantic Search**: Natural language queries across codebase
- **Contextual Assistance**: Smart suggestions and error analysis
- **File Monitoring**: Real-time change detection and processing
- **Knowledge Graph**: Persistent connections between code, architecture, and design decisions
- **System Visualization**: Visual flows highlighting relevant logic paths

## Architecture

The system follows a microservices architecture with event-driven communication:

```
API Gateway → Event Bus → Services → Databases
```

### Core Services
- **File Watcher**: Monitor filesystem changes
- **Code Analyzer**: Parse and analyze source code
- **Documentation Generator**: Create structured documentation
- **Search Engine**: Semantic search with vector embeddings
- **Context Provider**: Intelligent code assistance

### Data Storage
- **PostgreSQL**: Structured data (symbols, dependencies)
- **Redis**: Caching and session management
- **Vector Database**: Semantic search embeddings

## Getting Started

### Prerequisites
- Node.js 18+
- npm 8+
- PostgreSQL
- Redis

### Installation

```bash
# Clone the repository
git clone https://github.com/Soumyaatanna/nexus.git
cd nexus

# Install dependencies
npm install

# Build all packages
npm run build

# Run tests
npm test
```

### Development

```bash
# Start development mode
npm run dev

# Run tests in watch mode
npm run test:watch

# Type checking
npm run type-check
```

## Project Structure

```
nexus/
├── packages/           # Shared packages
│   ├── types/         # TypeScript type definitions
│   ├── shared/        # Shared utilities
│   ├── events/        # Event bus implementation
│   └── database/      # Database connections
├── services/          # Microservices (to be implemented)
├── .kiro/            # Kiro specifications
│   └── specs/        # Requirements, design, and tasks
└── docs/             # Architecture documentation
```

## Documentation

- [Requirements](/.kiro/specs/nexus-cognitive-command-center/requirements.md)
- [Design Document](/.kiro/specs/nexus-cognitive-command-center/design.md)
- [Implementation Tasks](/.kiro/specs/nexus-cognitive-command-center/tasks.md)
- [AWS Architecture](AWS_Architecture_Overview.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License - see LICENSE file for details

## Status

🚧 **In Development** - Core foundation completed, services implementation in progress.

### Completed
- ✅ Project foundation and shared infrastructure
- ✅ TypeScript monorepo setup
- ✅ Shared type definitions
- ✅ Event bus implementation
- ✅ Database connection utilities
- ✅ Testing framework configuration

### In Progress
- 🔄 File Watcher Service
- 🔄 Code Analyzer Service
- 🔄 Documentation Generator Service
- 🔄 Search Engine Service
- 🔄 Context Provider Service
