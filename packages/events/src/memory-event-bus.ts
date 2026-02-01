import type { BaseEvent } from '@nexus/types';
import { Logger } from '@nexus/shared';
import { AbstractEventBus } from './event-bus.js';

export class MemoryEventBus extends AbstractEventBus {
  private logger: Logger;

  constructor() {
    super();
    this.logger = new Logger('MemoryEventBus');
  }

  async publish<T extends BaseEvent>(event: T): Promise<void> {
    this.logger.debug(`Publishing event: ${event.type}`, { eventId: event.id });
    
    try {
      await this.notifySubscribers(event);
      this.logger.debug(`Event published successfully: ${event.type}`, { eventId: event.id });
    } catch (error) {
      this.logger.error(`Failed to publish event: ${event.type}`, error as Error, { eventId: event.id });
      throw error;
    }
  }
}