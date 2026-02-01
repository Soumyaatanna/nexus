import type { FileChange, AnalysisResult, AnalysisUpdate } from './analysis.js';
import type { DocumentationUpdate } from './documentation.js';
import type { ContentChange } from './search.js';

// Event system types
export interface BaseEvent {
  id: string;
  type: string;
  timestamp: Date;
  source: string;
  metadata?: Record<string, any>;
}

// File system events
export interface FileChangedEvent extends BaseEvent {
  type: 'file.changed';
  payload: {
    changes: FileChange[];
  };
}

export interface FileWatchStartedEvent extends BaseEvent {
  type: 'file.watch.started';
  payload: {
    path: string;
    watchId: string;
  };
}

export interface FileWatchStoppedEvent extends BaseEvent {
  type: 'file.watch.stopped';
  payload: {
    path: string;
    watchId: string;
  };
}

// Analysis events
export interface AnalysisCompletedEvent extends BaseEvent {
  type: 'analysis.completed';
  payload: {
    result: AnalysisResult;
  };
}

export interface AnalysisUpdatedEvent extends BaseEvent {
  type: 'analysis.updated';
  payload: {
    update: AnalysisUpdate;
  };
}

export interface AnalysisFailedEvent extends BaseEvent {
  type: 'analysis.failed';
  payload: {
    filePath: string;
    error: string;
  };
}

// Documentation events
export interface DocumentationGeneratedEvent extends BaseEvent {
  type: 'documentation.generated';
  payload: {
    filePath: string;
    sections: number;
  };
}

export interface DocumentationUpdatedEvent extends BaseEvent {
  type: 'documentation.updated';
  payload: {
    update: DocumentationUpdate;
  };
}

// Search events
export interface IndexUpdatedEvent extends BaseEvent {
  type: 'search.index.updated';
  payload: {
    changes: ContentChange[];
  };
}

export interface SearchQueryEvent extends BaseEvent {
  type: 'search.query';
  payload: {
    query: string;
    resultCount: number;
    executionTime: number;
  };
}

// System events
export interface ServiceStartedEvent extends BaseEvent {
  type: 'service.started';
  payload: {
    serviceName: string;
    version: string;
  };
}

export interface ServiceStoppedEvent extends BaseEvent {
  type: 'service.stopped';
  payload: {
    serviceName: string;
    reason?: string;
  };
}

export interface HealthCheckEvent extends BaseEvent {
  type: 'health.check';
  payload: {
    serviceName: string;
    status: 'healthy' | 'unhealthy' | 'degraded';
    details?: Record<string, any>;
  };
}

// Union type for all events
export type NexusEvent = 
  | FileChangedEvent
  | FileWatchStartedEvent
  | FileWatchStoppedEvent
  | AnalysisCompletedEvent
  | AnalysisUpdatedEvent
  | AnalysisFailedEvent
  | DocumentationGeneratedEvent
  | DocumentationUpdatedEvent
  | IndexUpdatedEvent
  | SearchQueryEvent
  | ServiceStartedEvent
  | ServiceStoppedEvent
  | HealthCheckEvent;

// Event handler type
export type EventHandler<T extends BaseEvent = BaseEvent> = (event: T) => Promise<void> | void;

// Event bus interface
export interface EventBus {
  publish<T extends BaseEvent>(event: T): Promise<void>;
  subscribe<T extends BaseEvent>(eventType: string, handler: EventHandler<T>): string;
  unsubscribe(subscriptionId: string): void;
  getSubscriptions(eventType?: string): string[];
}