import { beforeEach, describe, expect, it, vi } from 'vitest';

import { api } from '@/features/auth/api/auth-api';
import {
  getUsageTrackingSessionId,
  sanitizeTrackingProperties,
  trackUsageEvent,
} from './usage-tracking';

vi.mock('@/features/auth/api/auth-api', () => ({
  api: {
    createUsageEventApiV1UsageEventsPost: vi.fn(),
  },
}));

describe('usage tracking', () => {
  beforeEach(() => {
    sessionStorage.clear();
    vi.mocked(api.createUsageEventApiV1UsageEventsPost).mockReset();
    vi.mocked(api.createUsageEventApiV1UsageEventsPost).mockResolvedValue({} as never);
    window.history.replaceState(null, '', '/admin/logs?log_type=request');
  });

  it('keeps a stable session id for the current browser session', () => {
    const first = getUsageTrackingSessionId();
    const second = getUsageTrackingSessionId();

    expect(first).toMatch(/^sess_/);
    expect(second).toBe(first);
  });

  it('removes forbidden and undefined properties before sending', async () => {
    await trackUsageEvent('page_view', {
      module: 'log_audit',
      token: 'secret',
      value: undefined,
    });

    expect(api.createUsageEventApiV1UsageEventsPost).toHaveBeenCalledWith(
      expect.objectContaining({
        event_name: 'page_view',
        page_path: '/admin/logs?log_type=request',
        properties: {
          module: 'log_audit',
          page_path: '/admin/logs?log_type=request',
        },
      }),
    );
  });

  it('does not throw when the tracking request fails', async () => {
    vi.mocked(api.createUsageEventApiV1UsageEventsPost).mockRejectedValue(new Error('network'));

    await expect(
      trackUsageEvent('copy_request_id', {
        module: 'log_audit',
        request_id: 'req_123',
      }),
    ).resolves.toBeUndefined();
  });

  it('sends normalized duration when provided', async () => {
    await trackUsageEvent(
      'search_submit',
      {
        module: 'log_audit',
        keyword: 'request',
      },
      { durationMs: 12.6 },
    );

    expect(api.createUsageEventApiV1UsageEventsPost).toHaveBeenCalledWith(
      expect.objectContaining({
        duration_ms: 13,
      }),
    );
  });

  it('sanitizes forbidden fields case-insensitively', () => {
    expect(
      sanitizeTrackingProperties({
        Authorization: 'Bearer token',
        module: 'log_audit',
      }),
    ).toEqual({ module: 'log_audit' });
  });
});
