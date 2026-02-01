import { Pool, PoolClient } from 'pg';
import type { DatabaseConfig } from '@nexus/shared';
import { Logger } from '@nexus/shared';

export class PostgreSQLConnection {
  private pool: Pool;
  private logger: Logger;

  constructor(config: DatabaseConfig['postgresql']) {
    this.logger = new Logger('PostgreSQL');
    this.pool = new Pool({
      host: config.host,
      port: config.port,
      database: config.database,
      user: config.username,
      password: config.password,
      ssl: config.ssl,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });

    this.pool.on('error', (err) => {
      this.logger.error('PostgreSQL pool error', err);
    });
  }

  async getClient(): Promise<PoolClient> {
    return this.pool.connect();
  }

  async query(text: string, params?: any[]): Promise<any> {
    const client = await this.getClient();
    try {
      const result = await client.query(text, params);
      return result.rows;
    } finally {
      client.release();
    }
  }

  async transaction<T>(callback: (client: PoolClient) => Promise<T>): Promise<T> {
    const client = await this.getClient();
    try {
      await client.query('BEGIN');
      const result = await callback(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  async close(): Promise<void> {
    await this.pool.end();
    this.logger.info('PostgreSQL connection pool closed');
  }

  async healthCheck(): Promise<boolean> {
    try {
      await this.query('SELECT 1');
      return true;
    } catch (error) {
      this.logger.error('PostgreSQL health check failed', error as Error);
      return false;
    }
  }
}