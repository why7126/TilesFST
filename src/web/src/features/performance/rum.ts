import { getWebClientType } from '@/features/auth/api/auth-api';
import { PRODUCT_VERSION } from '@shared/product-version';
import { ingestPerformanceEvents, type PerformanceEventPayload } from './performance-api';

const SAMPLE_RATE = 1;

function pageKey(): string {
  if (typeof window === 'undefined') {
    return 'web/unknown';
  }
  const path = window.location.pathname || '/';
  if (path.startsWith('/admin')) {
    return path.replace(/^\/admin\/?/, 'admin/') || 'admin/dashboard';
  }
  return `catalog${path === '/' ? '/home' : path}`;
}

function appVersion(): string {
  return PRODUCT_VERSION;
}

function networkType(): string | undefined {
  const connection = (navigator as Navigator & { connection?: { effectiveType?: string } }).connection;
  return connection?.effectiveType;
}

function deviceClass(): string {
  const width = window.innerWidth;
  if (width < 640) {
    return 'mobile';
  }
  if (width < 1024) {
    return 'tablet';
  }
  return 'desktop';
}

function sendMetric(metricName: string, durationMs: number): void {
  if (!Number.isFinite(durationMs) || durationMs < 0) {
    return;
  }
  const event: PerformanceEventPayload = {
    client_type: getWebClientType(),
    page_key: pageKey(),
    app_version: appVersion(),
    network_type: networkType(),
    device_class: deviceClass(),
    metric_name: metricName,
    duration_ms: Math.round(durationMs),
    sample_rate: SAMPLE_RATE,
    occurred_at: new Date().toISOString(),
    request_id: createRumRequestId(),
  };
  ingestPerformanceEvents([event]).catch(() => {
    // RUM 上报失败不阻断页面主流程。
  });
}

function createRumRequestId(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return `rum-${crypto.randomUUID()}`;
  }
  return `rum-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

export function installWebRum(): void {
  if (typeof window === 'undefined' || typeof performance === 'undefined') {
    return;
  }

  window.requestAnimationFrame(() => {
    sendMetric('first_content_ready', performance.now());
  });

  window.addEventListener(
    'load',
    () => {
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming | undefined;
      if (navigation) {
        sendMetric('full_load', navigation.loadEventEnd || performance.now());
        sendMetric('dom_content_loaded', navigation.domContentLoadedEventEnd);
        return;
      }
      sendMetric('full_load', performance.now());
    },
    { once: true },
  );
}
