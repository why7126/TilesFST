import { apiClient } from '@/features/auth/api/auth-api';

export type PerformanceClientType = 'web_admin' | 'web_catalog' | 'wechat_miniapp';

export interface PerformanceEventPayload {
  client_type: PerformanceClientType;
  page_key: string;
  app_version?: string;
  network_type?: string;
  device_class?: string;
  metric_name: string;
  duration_ms: number;
  sample_rate: number;
  occurred_at: string;
  request_id?: string;
}

export interface PerformanceAggregateItem {
  client_type: string;
  page_key: string;
  metric_name: string;
  app_version?: string | null;
  network_type?: string | null;
  device_class?: string | null;
  sample_count: number;
  average_ms: number;
  max_ms: number;
  p50_ms: number;
  p75_ms: number;
  p95_ms: number;
  p99_ms: number;
  sample_status: 'ok' | 'insufficient';
}

export interface PerformanceSummaryData {
  items: PerformanceAggregateItem[];
  slow_pages: PerformanceAggregateItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  total_events: number;
  filters: Record<string, string | number | null>;
  thresholds: Record<string, number>;
}

export interface PerformanceSampleItem {
  id: string;
  client_type: string;
  page_key: string;
  metric_name: string;
  duration_ms: number;
  app_version?: string | null;
  network_type?: string | null;
  device_class?: string | null;
  request_id?: string | null;
  occurred_at: string;
  server_received_at: string;
}

export interface PerformanceSampleData {
  items: PerformanceSampleItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  filters: Record<string, string | number | null>;
}

export interface PerformanceFilterOption {
  value: string;
  label: string;
  count?: number | null;
}

export interface PerformanceFilterOptionsData {
  client_types: PerformanceFilterOption[];
  app_versions: PerformanceFilterOption[];
  page_keys: PerformanceFilterOption[];
  device_classes: PerformanceFilterOption[];
  network_types: PerformanceFilterOption[];
  metrics: PerformanceFilterOption[];
}

export interface PerformanceFilterOptionsQuery {
  start_time?: string;
  end_time?: string;
}

export interface PerformanceSummaryQuery {
  client_type?: PerformanceClientType;
  page_key?: string;
  app_version?: string;
  network_type?: string;
  device_class?: string;
  metric_name?: string;
  start_time?: string;
  end_time?: string;
  min_samples?: number;
  page?: number;
  page_size?: number;
  limit?: number;
}

export async function ingestPerformanceEvents(events: PerformanceEventPayload[]): Promise<void> {
  await apiClient.post('/api/v1/performance-events', { events });
}

export async function fetchPerformanceSummary(params: PerformanceSummaryQuery): Promise<PerformanceSummaryData> {
  const response = await apiClient.get('/api/v1/admin/performance-events/summary', { params });
  if (!response.data.data) {
    throw new Error(response.data.message || '性能观测数据为空');
  }
  return response.data.data;
}

export async function fetchPerformanceFilterOptions(
  params: PerformanceFilterOptionsQuery,
): Promise<PerformanceFilterOptionsData> {
  const response = await apiClient.get('/api/v1/admin/performance-events/filter-options', { params });
  if (!response.data.data) {
    throw new Error(response.data.message || '性能筛选候选值为空');
  }
  return response.data.data;
}

export async function fetchPerformanceSamples(params: PerformanceSummaryQuery): Promise<PerformanceSampleData> {
  const response = await apiClient.get('/api/v1/admin/performance-events/samples', { params });
  if (!response.data.data) {
    throw new Error(response.data.message || '性能样本数据为空');
  }
  return response.data.data;
}
