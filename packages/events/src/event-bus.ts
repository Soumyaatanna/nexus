import type { BaseEvent, EventBus, EventHandler } from '@nexus/types';

export abstract class AbstractEventBus implements EventBus {
  protected subscriptions = new Map<string, Map<string, EventHandler>>();

  abstract publish<T extends BaseEvent>(event: T): Promise<void>;

  subscribe<T extends BaseEvent>(eventType: string, handler: EventHandler<T>): string {
    const subscriptionId = `${eventType}-${Date.now()}-${Math.random()}`;
    
    if (!this.subscriptions.has(eventType)) {
      this.subscriptions.set(eventType, new Map());
    }
    
    this.subscriptions.get(eventType)!.set(subscriptionId, handler as EventHandler);
    return subscriptionId;
  }

  unsubscribe(subscriptionId: string): void {
    for (const [eventType, handlers] of this.subscriptions) {
      if (handlers.has(subscriptionId)) {
        handlers.delete(subscriptionId);
        if (handlers.size === 0) {
          this.subscriptions.delete(eventType);
        }
        return;
      }
    }
  }

  getSubscriptions(eventType?: string): string[] {
    if (eventType) {
      const handlers = this.subscriptions.get(eventType);
      return handlers ? Array.from(handlers.keys()) : [];
    }
    
    const allSubscriptions: string[] = [];
    for (const handlers of this.subscriptions.values()) {
      allSubscriptions.push(...handlers.keys());
    }
    return allSubscriptions;
  }

  protected async notifySubscribers<T extends BaseEvent>(event: T): Promise<void> {
    const handlers = this.subscriptions.get(event.type);
    if (!handlers) return;

    const promises = Array.from(handlers.values()).map(handler => {
      try {
        return Promise.resolve(handler(event));
      } catch (error) {
        console.error(`Error in event handler for ${event.type}:`, error);
        return Promise.resolve();
      }
    });

    await Promise.allSettled(promises);
  }
}