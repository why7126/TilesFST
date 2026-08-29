import { miniappApiConfig } from '../utils/env';
import { reportPerformanceMetric } from './performance';

const DEFAULT_BASE_URL = miniappApiConfig.apiBaseUrl;
const CLIENT_TYPE = 'wechat_miniapp';
const CLIENT_REQUEST_ID_PREFIX = 'miniapp';
const BEHAVIOR_TRACE_ID_PREFIX = 'bt:miniapp';
const BEHAVIOR_EVENT_ID_PREFIX = 'be:miniapp';

type ApiResponse<T> = {
  code: number;
  message: string;
  data: T;
};

type MiniappRequestOption = WechatMiniprogram.RequestOption & {
  skipPerformanceTracking?: boolean;
  behaviorTraceId?: string;
  behaviorEventId?: string;
};

let activeBehaviorContext: { behaviorTraceId: string; behaviorEventId: string } | null = null;

function baseUrl(): string {
  const app = getApp<{
    globalData?: { apiBaseUrl?: string; apiFallbackBaseUrls?: string[]; environment?: string };
  }>();
  return app.globalData?.apiBaseUrl || DEFAULT_BASE_URL;
}

function baseUrls(): string[] {
  const app = getApp<{
    globalData?: { apiBaseUrl?: string; apiFallbackBaseUrls?: string[]; environment?: string };
  }>();
  const fallbackUrls = app.globalData?.apiFallbackBaseUrls || [];
  return [baseUrl(), ...fallbackUrls].filter(
    (url, index, urls): url is string => Boolean(url) && urls.indexOf(url) === index,
  );
}

function mediaUrl(value: unknown, currentBaseUrl: string): unknown {
  if (typeof value === 'string' && value.indexOf('/media/') === 0) {
    return `${currentBaseUrl}${value}`;
  }
  return value;
}

function normalizeMediaUrls(value: unknown, currentBaseUrl: string): unknown {
  if (Array.isArray(value)) {
    return value.map((item) => normalizeMediaUrls(item, currentBaseUrl));
  }
  if (value && typeof value === 'object') {
    const next: Record<string, unknown> = {};
    Object.keys(value as Record<string, unknown>).forEach((key) => {
      next[key] = normalizeMediaUrls((value as Record<string, unknown>)[key], currentBaseUrl);
    });
    return next;
  }
  return mediaUrl(value, currentBaseUrl);
}

function createClientRequestId(): string | undefined {
  try {
    return `${CLIENT_REQUEST_ID_PREFIX}:${Date.now().toString(36)}:${Math.random().toString(36).slice(2, 10)}`;
  } catch {
    return undefined;
  }
}

function createBehaviorId(prefix: string): string | undefined {
  try {
    return `${prefix}:${Date.now().toString(36)}:${Math.random().toString(36).slice(2, 10)}`;
  } catch {
    return undefined;
  }
}

function setActiveBehaviorContext(behaviorTraceId?: string, behaviorEventId?: string) {
  activeBehaviorContext = behaviorTraceId && behaviorEventId ? { behaviorTraceId, behaviorEventId } : null;
}

function cleanProperties(properties: Record<string, unknown>): Record<string, unknown> {
  const next: Record<string, unknown> = {};
  Object.keys(properties).forEach((key) => {
    const value = properties[key];
    if (value !== undefined && value !== null) {
      next[key] = value;
    }
  });
  return next;
}

function isTelemetryPath(path: string): boolean {
  return path.indexOf('/api/v1/usage-events') === 0 || path.indexOf('/api/v1/performance-events') === 0;
}

export function request<T>(path: string, options: MiniappRequestOption = {}): Promise<T> {
  const { skipPerformanceTracking, behaviorTraceId, behaviorEventId, ...requestOptions } = options;
  const shouldReportPerformance = !skipPerformanceTracking && !isTelemetryPath(path);
  const urls = baseUrls();
  const clientRequestId = createClientRequestId();
  const behaviorContext = activeBehaviorContext;
  const effectiveBehaviorTraceId = behaviorTraceId || behaviorContext?.behaviorTraceId;
  const effectiveBehaviorEventId = behaviorEventId || behaviorContext?.behaviorEventId;
  const attempts: Array<{
    url: string;
    statusCode?: number;
    message?: string;
    errMsg?: string;
  }> = [];

  function tryRequest(index: number): Promise<T> {
    const currentBaseUrl = urls[index] || DEFAULT_BASE_URL;
    const url = `${currentBaseUrl}${path}`;
    const startedAt = Date.now();
    return new Promise((resolve, reject) => {
      wx.request<ApiResponse<T>>({
        ...requestOptions,
        url,
        header: {
          'content-type': 'application/json',
          ...(requestOptions.header || {}),
          'x-client-type': CLIENT_TYPE,
          ...(clientRequestId ? { 'x-client-request-id': clientRequestId } : {}),
          ...(effectiveBehaviorTraceId ? { 'x-behavior-trace-id': effectiveBehaviorTraceId } : {}),
          ...(effectiveBehaviorEventId ? { 'x-behavior-event-id': effectiveBehaviorEventId } : {}),
        },
        success: (res) => {
          const body = res.data;
          if (shouldReportPerformance) {
            reportPerformanceMetric({
              page_key: path,
              metric_name: 'api_duration',
              duration_ms: Date.now() - startedAt,
              device_class: 'miniapp',
              request_id: clientRequestId,
            });
          }
          if (res.statusCode >= 200 && res.statusCode < 300 && body?.code === 0) {
            resolve(normalizeMediaUrls(body.data, currentBaseUrl) as T);
            return;
          }
          attempts.push({
            url,
            statusCode: res.statusCode,
            message: body?.message || `request failed: ${res.statusCode}`,
          });
          if (res.statusCode >= 500 && index + 1 < urls.length) {
            tryRequest(index + 1).then(resolve).catch(reject);
            return;
          }
          const error = new Error(body?.message || `request failed: ${res.statusCode}`) as Error & {
            attempts?: typeof attempts;
          };
          error.attempts = attempts;
          reject(error);
        },
        fail: (error) => {
          if (shouldReportPerformance) {
            reportPerformanceMetric({
              page_key: path,
              metric_name: 'api_failed_duration',
              duration_ms: Date.now() - startedAt,
              device_class: 'miniapp',
              request_id: clientRequestId,
            });
          }
          attempts.push({
            url,
            errMsg: error.errMsg,
          });
          if (index + 1 < urls.length) {
            tryRequest(index + 1).then(resolve).catch(reject);
            return;
          }
          (error as WechatMiniprogram.GeneralCallbackResult & { attempts?: typeof attempts }).attempts =
            attempts;
          reject(error);
        },
      });
    });
  }

  return tryRequest(0);
}

export function track(eventName: string, properties: Record<string, unknown>): void {
  const cleanedProperties = cleanProperties(properties);
  const behaviorTraceId = createBehaviorId(BEHAVIOR_TRACE_ID_PREFIX);
  const behaviorEventId = createBehaviorId(BEHAVIOR_EVENT_ID_PREFIX);
  setActiveBehaviorContext(behaviorTraceId, behaviorEventId);
  request('/api/v1/usage-events', {
    method: 'POST',
    skipPerformanceTracking: true,
    behaviorTraceId,
    behaviorEventId,
    data: {
      event_name: eventName,
      client_type: CLIENT_TYPE,
      page_path: String(cleanedProperties.page_path || ''),
      client_request_id: createClientRequestId(),
      behavior_trace_id: behaviorTraceId,
      behavior_event_id: behaviorEventId,
      properties: {
        ...cleanedProperties,
        client_type: CLIENT_TYPE,
        behavior_trace_id: behaviorTraceId,
        behavior_event_id: behaviorEventId,
      },
    },
  }).catch(() => {
    // 埋点失败不阻断用户浏览、分享或咨询。
  });
}
