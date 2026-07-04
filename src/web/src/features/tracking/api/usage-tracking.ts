import { api } from '@/features/auth/api/auth-api';
import type { UsageEventCreate } from '@/shared/api/generated';

const SESSION_KEY = 'tilesfst_tracking_session_id';
const DEFAULT_CLIENT_TYPE = 'web_admin';
const FORBIDDEN_PROPERTY_KEYS = new Set([
  'authorization',
  'cookie',
  'password',
  'raw_filename',
  'raw_payload',
  'secret',
  'token',
]);

export type UsageTrackingEventName =
  | 'page_view'
  | 'search_submit'
  | 'filter_change'
  | 'detail_view'
  | 'copy_request_id'
  | 'entity_create'
  | 'entity_update'
  | 'entity_delete'
  | 'status_change'
  | 'media_upload'
  | 'login_success'
  | 'login_failed'
  | 'api_error';

export type UsageTrackingProperties = Record<string, unknown>;

interface TrackUsageEventOptions {
  clientType?: string;
  durationMs?: number;
  pagePath?: string;
  requestId?: string | null;
  summary?: string;
}

export function getUsageTrackingSessionId(): string {
  const existing = sessionStorage.getItem(SESSION_KEY);
  if (existing) {
    return existing;
  }
  const next = createSessionId();
  sessionStorage.setItem(SESSION_KEY, next);
  return next;
}

export function sanitizeTrackingProperties(
  properties: UsageTrackingProperties,
): UsageTrackingProperties {
  return Object.entries(properties).reduce<UsageTrackingProperties>((acc, [key, value]) => {
    if (value === undefined || FORBIDDEN_PROPERTY_KEYS.has(key.toLowerCase())) {
      return acc;
    }
    acc[key] = value;
    return acc;
  }, {});
}

export async function trackUsageEvent(
  eventName: UsageTrackingEventName,
  properties: UsageTrackingProperties,
  options: TrackUsageEventOptions = {},
): Promise<void> {
  try {
    const pagePath = options.pagePath ?? getCurrentPagePath();
    const sanitizedProperties = sanitizeTrackingProperties({
      ...properties,
      page_path: properties.page_path ?? pagePath,
    });
    const payload: UsageEventCreate = {
      event_name: eventName,
      properties: sanitizedProperties,
      client_type: options.clientType ?? DEFAULT_CLIENT_TYPE,
      page_path: pagePath,
      request_id: options.requestId ?? undefined,
      session_id: getUsageTrackingSessionId(),
      duration_ms: normalizeDurationMs(options.durationMs),
      summary: options.summary,
    };
    await api.createUsageEventApiV1UsageEventsPost(payload);
  } catch {
    // Tracking must never block the primary user workflow.
  }
}

function normalizeDurationMs(value: number | undefined): number | undefined {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    return undefined;
  }
  return Math.max(0, Math.round(value));
}

function getCurrentPagePath(): string {
  return `${window.location.pathname}${window.location.search}`;
}

function createSessionId(): string {
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
    return `sess_${crypto.randomUUID()}`;
  }
  return `sess_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
}
