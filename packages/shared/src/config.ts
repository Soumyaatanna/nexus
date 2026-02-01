// Configuration management
export interface DatabaseConfig {
  postgresql: {
    host: string;
    port: number;
    database: string;
    username: string;
    password: string;
    ssl?: boolean;
  };
  redis: {
    host: string;
    port: number;
    password?: string;
    db?: number;
  };
  vector: {
    host: string;
    port: number;
    apiKey?: string;
  };
}

export interface ServiceConfig {
  name: string;
  port: number;
  host: string;
  logLevel: 'ERROR' | 'WARN' | 'INFO' | 'DEBUG';
  healthCheckInterval: number;
}

export interface NexusConfig {
  services: {
    fileWatcher: ServiceConfig;
    codeAnalyzer: ServiceConfig;
    documentationGenerator: ServiceConfig;
    searchEngine: ServiceConfig;
    contextProvider: ServiceConfig;
    apiGateway: ServiceConfig;
  };
  database: DatabaseConfig;
  eventBus: {
    type: 'memory' | 'redis' | 'kafka';
    config: Record<string, any>;
  };
  monitoring: {
    enabled: boolean;
    metricsPort: number;
    tracingEndpoint?: string;
  };
}

export function loadConfig(): NexusConfig {
  // In production, this would load from environment variables or config files
  return {
    services: {
      fileWatcher: {
        name: 'file-watcher',
        port: 3001,
        host: 'localhost',
        logLevel: 'INFO',
        healthCheckInterval: 30000
      },
      codeAnalyzer: {
        name: 'code-analyzer',
        port: 3002,
        host: 'localhost',
        logLevel: 'INFO',
        healthCheckInterval: 30000
      },
      documentationGenerator: {
        name: 'documentation-generator',
        port: 3003,
        host: 'localhost',
        logLevel: 'INFO',
        healthCheckInterval: 30000
      },
      searchEngine: {
        name: 'search-engine',
        port: 3004,
        host: 'localhost',
        logLevel: 'INFO',
        healthCheckInterval: 30000
      },
      contextProvider: {
        name: 'context-provider',
        port: 3005,
        host: 'localhost',
        logLevel: 'INFO',
        healthCheckInterval: 30000
      },
      apiGateway: {
        name: 'api-gateway',
        port: 3000,
        host: 'localhost',
        logLevel: 'INFO',
        healthCheckInterval: 30000
      }
    },
    database: {
      postgresql: {
        host: process.env.POSTGRES_HOST || 'localhost',
        port: parseInt(process.env.POSTGRES_PORT || '5432'),
        database: process.env.POSTGRES_DB || 'nexus',
        username: process.env.POSTGRES_USER || 'nexus',
        password: process.env.POSTGRES_PASSWORD || 'nexus'
      },
      redis: {
        host: process.env.REDIS_HOST || 'localhost',
        port: parseInt(process.env.REDIS_PORT || '6379'),
        password: process.env.REDIS_PASSWORD
      },
      vector: {
        host: process.env.VECTOR_DB_HOST || 'localhost',
        port: parseInt(process.env.VECTOR_DB_PORT || '9200'),
        apiKey: process.env.VECTOR_DB_API_KEY
      }
    },
    eventBus: {
      type: 'memory',
      config: {}
    },
    monitoring: {
      enabled: process.env.NODE_ENV === 'production',
      metricsPort: 9090,
      tracingEndpoint: process.env.TRACING_ENDPOINT
    }
  };
}