// Centralized logging utility
export interface LogLevel {
  ERROR: 0;
  WARN: 1;
  INFO: 2;
  DEBUG: 3;
}

export const LOG_LEVELS: LogLevel = {
  ERROR: 0,
  WARN: 1,
  INFO: 2,
  DEBUG: 3
} as const;

export type LogLevelType = keyof LogLevel;

export interface LogEntry {
  timestamp: Date;
  level: LogLevelType;
  service: string;
  message: string;
  metadata?: Record<string, any>;
  error?: Error;
}

export class Logger {
  private serviceName: string;
  private logLevel: number;

  constructor(serviceName: string, logLevel: LogLevelType = 'INFO') {
    this.serviceName = serviceName;
    this.logLevel = LOG_LEVELS[logLevel];
  }

  private log(level: LogLevelType, message: string, metadata?: Record<string, any>, error?: Error): void {
    if (LOG_LEVELS[level] > this.logLevel) {
      return;
    }

    const entry: LogEntry = {
      timestamp: new Date(),
      level,
      service: this.serviceName,
      message,
      metadata,
      error
    };

    // In production, this would send to a logging service
    console.log(JSON.stringify(entry, null, 2));
  }

  error(message: string, error?: Error, metadata?: Record<string, any>): void {
    this.log('ERROR', message, metadata, error);
  }

  warn(message: string, metadata?: Record<string, any>): void {
    this.log('WARN', message, metadata);
  }

  info(message: string, metadata?: Record<string, any>): void {
    this.log('INFO', message, metadata);
  }

  debug(message: string, metadata?: Record<string, any>): void {
    this.log('DEBUG', message, metadata);
  }

  setLogLevel(level: LogLevelType): void {
    this.logLevel = LOG_LEVELS[level];
  }
}