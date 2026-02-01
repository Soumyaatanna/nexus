import type { DatabaseConfig } from '@nexus/shared';
import { Logger } from '@nexus/shared';
import { PostgreSQLConnection } from './postgresql.js';
import { RedisConnection } from './redis.js';

export class ConnectionManager {
  private postgresql?: PostgreSQLConnection;
  private redis?: RedisConnection;
  private logger: Logger;

  constructor(private config: DatabaseConfig) {
    this.logger = new Logger('ConnectionManager');
  }

  async initialize(): Promise<void> {
    this.logger.info('Initializing database connections');

    try {
      // Initialize PostgreSQL
      this.postgresql = new PostgreSQLConnection(this.config.postgresql);
      this.logger.info('PostgreSQL connection initialized');

      // Initialize Redis
      this.redis = new RedisConnection(this.config.redis);
      await this.redis.connect();
      this.logger.info('Redis connection initialized');

      this.logger.info('All database connections initialized successfully');
    } catch (error) {
      this.logger.error('Failed to initialize database connections', error as Error);
      throw error;
    }
  }

  getPostgreSQL(): PostgreSQLConnection {
    if (!this.postgresql) {
      throw new Error('PostgreSQL connection not initialized');
    }
    return this.postgresql;
  }

  getRedis(): RedisConnection {
    if (!this.redis) {
      throw new Error('Redis connection not initialized');
    }
    return this.redis;
  }

  async healthCheck(): Promise<{ postgresql: boolean; redis: boolean }> {
    const results = {
      postgresql: false,
      redis: false
    };

    if (this.postgresql) {
      results.postgresql = await this.postgresql.healthCheck();
    }

    if (this.redis) {
      results.redis = await this.redis.healthCheck();
    }

    return results;
  }

  async close(): Promise<void> {
    this.logger.info('Closing database connections');

    const promises: Promise<void>[] = [];

    if (this.postgresql) {
      promises.push(this.postgresql.close());
    }

    if (this.redis) {
      promises.push(this.redis.disconnect());
    }

    await Promise.all(promises);
    this.logger.info('All database connections closed');
  }
}