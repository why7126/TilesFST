import { beforeEach, describe, expect, it, vi } from 'vitest';
import { PRODUCT_VERSION } from '@shared/product-version';

const ingestPerformanceEvents = vi.fn();

vi.mock('@/features/auth/api/auth-api', () => ({
  getWebClientType: () => 'web_admin',
}));

vi.mock('./performance-api', () => ({
  ingestPerformanceEvents,
}));

describe('installWebRum', () => {
  beforeEach(() => {
    vi.resetModules();
    ingestPerformanceEvents.mockReset();
    ingestPerformanceEvents.mockResolvedValue(undefined);
    Object.defineProperty(window, 'innerWidth', { configurable: true, value: 1280 });
    window.requestAnimationFrame = (callback: FrameRequestCallback) => {
      callback(16);
      return 1;
    };
    vi.spyOn(performance, 'now').mockReturnValue(123.4);
    vi.spyOn(performance, 'getEntriesByType').mockReturnValue([
      {
        loadEventEnd: 987.6,
        domContentLoadedEventEnd: 456.7,
      } as PerformanceNavigationTiming,
    ]);
    window.history.pushState({}, '', '/admin/performance');
  });

  it('reports first content and load metrics without blocking the page', async () => {
    const { installWebRum } = await import('./rum');

    installWebRum();
    window.dispatchEvent(new Event('load'));

    expect(ingestPerformanceEvents).toHaveBeenCalledTimes(3);
    expect(ingestPerformanceEvents).toHaveBeenCalledWith([
      expect.objectContaining({
        client_type: 'web_admin',
        page_key: 'admin/performance',
        metric_name: 'first_content_ready',
        app_version: PRODUCT_VERSION,
        duration_ms: 123,
        device_class: 'desktop',
        request_id: expect.stringMatching(/^rum-/),
        sample_rate: 1,
      }),
    ]);
    expect(ingestPerformanceEvents).toHaveBeenCalledWith([
      expect.objectContaining({ metric_name: 'full_load', duration_ms: 988 }),
    ]);
    expect(ingestPerformanceEvents).toHaveBeenCalledWith([
      expect.objectContaining({ metric_name: 'dom_content_loaded', duration_ms: 457 }),
    ]);
  });

  it('swallows reporting failures', async () => {
    ingestPerformanceEvents.mockRejectedValueOnce(new Error('network down'));
    const { installWebRum } = await import('./rum');

    expect(() => installWebRum()).not.toThrow();
  });
});
