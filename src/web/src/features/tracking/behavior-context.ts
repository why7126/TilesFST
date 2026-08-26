const ACTIVE_BEHAVIOR_TTL_MS = 5000;

export type BehaviorContext = {
  behaviorTraceId: string;
  behaviorEventId: string;
  expiresAt: number;
};

let activeBehaviorContext: BehaviorContext | null = null;

export function createBehaviorId(prefix: 'bt' | 'be'): string {
  try {
    if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
      return `${prefix}:${crypto.randomUUID()}`;
    }
  } catch {
    // Fall back below; behavior IDs are correlation aids, not trusted identity.
  }
  return `${prefix}:${Date.now().toString(36)}:${Math.random().toString(36).slice(2, 12)}`;
}

export function setActiveBehaviorContext(behaviorTraceId: string, behaviorEventId: string): BehaviorContext {
  activeBehaviorContext = {
    behaviorTraceId,
    behaviorEventId,
    expiresAt: Date.now() + ACTIVE_BEHAVIOR_TTL_MS,
  };
  return activeBehaviorContext;
}

export function getActiveBehaviorContext(): BehaviorContext | null {
  if (!activeBehaviorContext) {
    return null;
  }
  if (activeBehaviorContext.expiresAt <= Date.now()) {
    activeBehaviorContext = null;
    return null;
  }
  return activeBehaviorContext;
}
