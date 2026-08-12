import { Activity } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import {
  fetchPerformanceSummary,
  type PerformanceAggregateItem,
  type PerformanceSummaryData,
} from '@/features/performance/performance-api';
import { getErrorMessage } from '@/features/auth/api/auth-api';
import '@/features/admin/styles/user-management.css';
import '@/features/admin/styles/log-audit.css';
import { getPaginationWindow } from '@/shared/lib/pagination-window';
import { AdminFilterSelect } from '@/shared/ui';
import { MetricCard, MetricCardGrid } from '@/shared/ui/metric-card';

const ALL_VALUE = 'all';

const clientOptions = [
  { value: ALL_VALUE, label: '全部端类型' },
  { value: 'web_admin', label: '管理端 Web' },
  { value: 'web_catalog', label: '店主 Web' },
  { value: 'wechat_miniapp', label: '微信小程序' },
];

const metricOptions = [
  { value: ALL_VALUE, label: '全部指标' },
  { value: 'first_content_ready', label: '首屏可用' },
  { value: 'full_load', label: '完整加载' },
  { value: 'first_api_done', label: '首个接口完成' },
];

const timeOptions = [
  { value: '1h', label: '最近1小时', minutes: 60 },
  { value: '6h', label: '最近6小时', minutes: 360 },
  { value: '1d', label: '最近1天', minutes: 1440 },
  { value: '7d', label: '最近7天', minutes: 10080 },
];
const PAGE_SIZE_OPTIONS = [10, 20, 50, 100];

export function PerformanceRumPage() {
  const navigate = useNavigate();
  const [clientType, setClientType] = useState(ALL_VALUE);
  const [metricName, setMetricName] = useState(ALL_VALUE);
  const [timeRange, setTimeRange] = useState('1d');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [data, setData] = useState<PerformanceSummaryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const params = useMemo(() => {
    const minutes = timeOptions.find((option) => option.value === timeRange)?.minutes ?? 1440;
    return {
      client_type: clientType === ALL_VALUE ? undefined : clientType as 'web_admin' | 'web_catalog' | 'wechat_miniapp',
      metric_name: metricName === ALL_VALUE ? undefined : metricName,
      start_time: new Date(Date.now() - minutes * 60 * 1000).toISOString(),
      min_samples: 20,
      page,
      page_size: pageSize,
    };
  }, [clientType, metricName, page, pageSize, timeRange]);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError('');
    fetchPerformanceSummary(params)
      .then((next) => {
        if (active) {
          setData(next);
        }
      })
      .catch((err) => {
        if (active) {
          setError(getErrorMessage(err, '性能观测数据加载失败'));
        }
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [params]);

  const first = data?.items[0];
  const total = data?.total ?? data?.slow_pages.length ?? 0;
  const totalPages = data?.total_pages ?? Math.max(1, Math.ceil(total / pageSize));

  useEffect(() => {
    if (data && page > totalPages) {
      setPage(totalPages);
    }
  }, [data, page, totalPages]);

  return (
    <main className="page-shell sku-page admin-list-page">
      <section className="page-hero log-audit-hero">
        <div>
          <p className="eyebrow">OBSERVABILITY / REAL USER MONITORING</p>
          <h1 className="page-title">性能观测</h1>
          <p className="page-desc">按端类型、页面、版本和网络追踪首屏可用与完整加载体验；浏览器不支持网络类型采集时显示为未知。</p>
        </div>
      </section>

      <MetricCardGrid ariaLabel="性能摘要" columns={4}>
        <MetricCard label="样本量" value={data?.total_events ?? 0} loading={loading} description="当前筛选范围" />
        <MetricCard label="P75 首屏" value={formatMs(first?.p75_ms)} loading={loading} description={first?.page_key ?? '暂无页面'} />
        <MetricCard label="P95 首屏" value={formatMs(first?.p95_ms)} loading={loading} dangerDescription={(first?.p95_ms ?? 0) >= 3000} description="慢页面阈值 3000ms" />
        <MetricCard label="样本状态" value={first ? sampleLabel(first.sample_status) : '无数据'} loading={loading} description="低样本不作趋势结论" />
      </MetricCardGrid>

      <section className="filter-card log-audit-filter" aria-label="性能筛选">
        <div className="log-audit-filter-grid">
          <div>
            <span className="field-label">时间范围</span>
            <AdminFilterSelect value={timeRange} options={timeOptions} onChange={(value) => {
              setTimeRange(value);
              setPage(1);
            }} ariaLabel="选择时间范围" listLabel="时间范围筛选选项" />
          </div>
          <div>
            <span className="field-label">端类型</span>
            <AdminFilterSelect value={clientType} options={clientOptions} onChange={(value) => {
              setClientType(value);
              setPage(1);
            }} ariaLabel="选择端类型" listLabel="端类型筛选选项" />
          </div>
          <div>
            <span className="field-label">指标</span>
            <AdminFilterSelect value={metricName} options={metricOptions} onChange={(value) => {
              setMetricName(value);
              setPage(1);
            }} ariaLabel="选择指标" listLabel="指标筛选选项" />
          </div>
          <div className="log-audit-filter-actions">
            <button type="button" className="btn" onClick={() => {
              setClientType(ALL_VALUE);
              setMetricName(ALL_VALUE);
              setTimeRange('1d');
              setPage(1);
            }}>
              重置
            </button>
          </div>
        </div>
      </section>

      <section className="table-card" aria-label="慢页面排行">
        {error ? <div className="empty-state">{error}</div> : null}
        {!error && !loading && !data?.items.length && total === 0 ? (
          <div className="empty-state">暂无性能样本</div>
        ) : (
          <div className="log-audit-table-wrap">
            <table className="log-audit-table">
              <thead>
                <tr>
                  <th>页面</th>
                  <th>版本号</th>
                  <th>端类型</th>
                  <th>指标</th>
                  <th>样本</th>
                  <th>P50</th>
                  <th>P75</th>
                  <th>P95</th>
                  <th>P99</th>
                  <th>状态</th>
                  <th className="log-audit-action-cell admin-sticky-action-cell">操作</th>
                </tr>
              </thead>
              <tbody>
                {(data?.slow_pages ?? []).map((item) => (
                  <tr key={`${item.client_type}-${item.page_key}-${item.metric_name}-${item.app_version ?? ''}-${item.network_type ?? ''}-${item.device_class ?? ''}`}>
                    <td><span className="log-summary performance-page-key"><span>{item.page_key}</span></span></td>
                    <td>{item.app_version || '版本未知'}</td>
                    <td>{clientLabel(item.client_type)}</td>
                    <td>{metricLabel(item.metric_name)}</td>
                    <td>{item.sample_count}</td>
                    <td>{formatMs(item.p50_ms)}</td>
                    <td>{formatMs(item.p75_ms)}</td>
                    <td className={item.p95_ms >= 3000 ? 'duration danger' : 'duration'}>{formatMs(item.p95_ms)}</td>
                    <td>{formatMs(item.p99_ms)}</td>
                    <td><span className={`log-status ${item.sample_status === 'ok' ? 'status-success' : 'status-warning'}`}>{sampleLabel(item.sample_status)}</span></td>
                    <td className="log-audit-action-cell admin-sticky-action-cell">
                      <button
                        className="log-audit-view-action"
                        type="button"
                        onClick={() => navigate(`/admin/performance/samples?${buildSampleSearchParams(item, params.start_time)}`)}
                      >
                        查看样本
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {loading ? <div className="empty-state"><Activity size={16} /> 加载中...</div> : null}
        {!error && data && total > 0 ? (
          <div className="pagination">
            <div className="page-summary">共 {loading ? '…' : total} 条聚合</div>
            <div className="page-right">
              <div className="page-buttons">
                <button className="page-btn" type="button" disabled={page <= 1} onClick={() => setPage((current) => Math.max(1, current - 1))} aria-label="上一页">‹</button>
                {getPaginationWindow(page, totalPages).map((item) => (
                  <button
                    key={item}
                    className={`page-btn ${item === page ? 'active' : ''}`}
                    type="button"
                    onClick={() => setPage(item)}
                    aria-current={item === page ? 'page' : undefined}
                  >
                    {item}
                  </button>
                ))}
                <button className="page-btn" type="button" disabled={page >= totalPages} onClick={() => setPage((current) => Math.min(totalPages, current + 1))} aria-label="下一页">›</button>
              </div>
              <div className="page-size-wrap">
                <span>每页显示</span>
                <select
                  className="page-size"
                  value={pageSize}
                  onChange={(event) => {
                    setPageSize(Number(event.target.value));
                    setPage(1);
                  }}
                  aria-label="每页显示条数"
                >
                  {PAGE_SIZE_OPTIONS.map((size) => (
                    <option key={size} value={size}>{size} 条</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        ) : null}
      </section>
    </main>
  );
}

function formatMs(value?: number | null) {
  if (value === null || value === undefined) {
    return '—';
  }
  return `${value}ms`;
}

function clientLabel(value: string) {
  return clientOptions.find((option) => option.value === value)?.label ?? value;
}

function metricLabel(value: string) {
  return metricOptions.find((option) => option.value === value)?.label ?? value;
}

function sampleLabel(value: string) {
  return value === 'ok' ? '样本充足' : '样本不足';
}

function buildSampleSearchParams(item: PerformanceAggregateItem, startTime?: string) {
  const searchParams = new URLSearchParams({
    client_type: item.client_type,
    page_key: item.page_key,
    metric_name: item.metric_name,
  });
  if (item.app_version) {
    searchParams.set('app_version', item.app_version);
  }
  if (item.network_type) {
    searchParams.set('network_type', item.network_type);
  }
  if (item.device_class) {
    searchParams.set('device_class', item.device_class);
  }
  if (startTime) {
    searchParams.set('start_time', startTime);
  }
  return searchParams.toString();
}
