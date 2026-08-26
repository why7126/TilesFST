import type { AxiosRequestConfig } from 'axios';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { setActiveBehaviorContext } from '@/features/tracking/behavior-context';
import { apiClient, createClientRequestId, getWebClientType } from './auth-api';

vi.mock('../utils/auth-token', () => ({
  clearStoredToken: vi.fn(),
  getStoredToken: vi.fn(() => 'token-123'),
}));

describe('auth api client request identity', () => {
  beforeEach(() => {
    window.history.pushState({}, '', '/admin/logs');
  });

  it('injects web_admin identity headers without overriding authorization', async () => {
    let captured: AxiosRequestConfig | null = null;

    await apiClient.get('/api/v1/admin/logs', {
      adapter: async (config) => {
        captured = config;
        return {
          data: { code: 0, message: 'ok', data: {} },
          status: 200,
          statusText: 'OK',
          headers: {},
          config,
        };
      },
    });

    expect(captured).toBeTruthy();
    const headers = captured!.headers as Record<string, string>;
    expect(headers.Authorization).toBe('Bearer token-123');
    expect(headers['x-client-type']).toBe('web_admin');
    expect(headers['x-client-request-id']).toMatch(/^web:/);
  });

  it('passes the active behavior trace headers when a UI event triggered the request', async () => {
    let captured: AxiosRequestConfig | null = null;
    setActiveBehaviorContext('bt:axios-behavior-001', 'be:axios-event-001');

    await apiClient.get('/api/v1/admin/logs', {
      adapter: async (config) => {
        captured = config;
        return {
          data: { code: 0, message: 'ok', data: {} },
          status: 200,
          statusText: 'OK',
          headers: {},
          config,
        };
      },
    });

    const headers = captured!.headers as Record<string, string>;
    expect(headers['x-behavior-trace-id']).toBe('bt:axios-behavior-001');
    expect(headers['x-behavior-event-id']).toBe('be:axios-event-001');
  });

  it('uses web_catalog outside admin routes', () => {
    window.history.pushState({}, '', '/tiles');

    expect(getWebClientType()).toBe('web_catalog');
  });

  it('does not throw when client request id generation falls back', () => {
    expect(createClientRequestId()).toMatch(/^web:/);
  });
});
