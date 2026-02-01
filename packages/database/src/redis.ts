import { createClient, RedisClientType } from 'redis';
import type { DatabaseConfig } from '@nexus/shared';
import { Logger } from '@nexus/shared';

export class RedisConnection {
  private client: RedisClientType;
  private logger: Logger;

  constructor(config: DatabaseConfig['redis']) {
    this.logger = new Logger('Redis');
    this.client = createClient({
      socket: {
        host: config.host,
        port: config.port,
      },
      password: config.password,
      database: config.db || 0,
    });

    this.client.on('error', (err) => {
      this.logger.error('Redis client error', err);
    });

    this.client.on('connect', () => {
      this.logger.info('Redis client connected');
    });

    this.client.on('disconnect', () => {
      this.logger.warn('Redis client disconnected');
    });
  }

  async connect(): Promise<void> {
    await this.client.connect();
  }

  async disconnect(): Promise<void> {
    await this.client.disconnect();
    this.logger.info('Redis client disconnected');
  }

  async get(key: string): Promise<string | null> {
    return this.client.get(key);
  }

  async set(key: string, value: string, ttl?: number): Promise<void> {
    if (ttl) {
      await this.client.setEx(key, ttl, value);
    } else {
      await this.client.set(key, value);
    }
  }

  async del(key: string): Promise<number> {
    return this.client.del(key);
  }

  async exists(key: string): Promise<number> {
    return this.client.exists(key);
  }

  async keys(pattern: string): Promise<string[]> {
    return this.client.keys(pattern);
  }

  async hGet(key: string, field: string): Promise<string | undefined> {
    return this.client.hGet(key, field);
  }

  async hSet(key: string, field: string, value: string): Promise<number> {
    return this.client.hSet(key, field, value);
  }

  async hGetAll(key: string): Promise<Record<string, string>> {
    return this.client.hGetAll(key);
  }

  async expire(key: string, seconds: number): Promise<boolean> {
    return this.client.expire(key, seconds);
  }

  async healthCheck(): Promise<boolean> {
    try {
      const result = await this.client.ping();
      return result === 'PONG';
    } catch (error) {
      this.logger.error('Redis health check failed', error as Error);
      return false;
    }
  }
}