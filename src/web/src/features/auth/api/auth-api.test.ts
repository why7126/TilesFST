import type { AxiosRequestConfig } from 'axios';
import { beforeEach, describe, expect, it, vi } from 'vitest';

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

  it('uses web_catalog outside admin routes', () => {
    window.history.pushState({}, '', '/tiles');

    expect(getWebClientType()).toBe('web_catalog');
  });

  it('does not throw when client request id generation falls back', () => {
    expect(createClientRequestId()).toMatch(/^web:/);
  });
});
