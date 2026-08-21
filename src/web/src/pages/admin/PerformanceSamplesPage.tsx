import { Activity, ArrowLeft, Copy } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import '@/features/admin/styles/user-management.css';
import '@/features/admin/styles/log-audit.css';
import {
  fetchPerformanceSamples,
  type PerformanceClientType,
  type PerformanceSampleData,
  type PerformanceSummaryQuery,
} from '@/features/performance/performance-api';
import { performanceMetricLabel } from '@/features/performance/metric-labels';
import { trackUsageEvent } from '@/features/tracking/api/usage-tracking';
import { copyTextToClipboard } from '@/shared/lib/clipboard';
import { getPaginationWindow } from '@/shared/lib/pagination-window';

const PAGE_SIZE_OPTIONS = [10, 20, 50, 100];
const TRACKING_MODULE = 'performance_samples';

const clientLabels: Record<string, string> = {
  web_admin: '管理端 Web',
  web_catalog: '店主 Web',
  wechat_miniapp: '微信小程序',
};

export function PerformanceSamplesPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [data, setData] = useState<PerformanceSampleData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  const params = useMemo<PerformanceSummaryQuery>(() => {
    const clientType = searchParams.get('client_type') as PerformanceClientType | null;
    return {
      client_type: clientType ?? undefined,
      page_key: searchParams.get('page_key') ?? undefined,
      metric_name: searchParams.get('metric_name') ?? undefined,
      app_version: searchParams.get('app_version') ?? undefined,
      network_type: searchParams.get('network_type') ?? undefined,
      device_class: searchParams.get('device_class') ?? undefined,
      start_time: searchParams.get('start_time') ?? undefined,
      end_time: searchParams.get('end_time') ?? undefined,
      page,
      page_size: pageSize,
    };
  }, [page, pageSize, searchParams]);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError('');
    fetchPerformanceSamples(params)
      .then((next) => {
        if (active) {
          setData(next);
        }
      })
      .catch((err) => {
        if (active) {
          setError(getErrorMessage(err, '性能样本加载失败'));
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

  const total = data?.total ?? 0;
  const totalPages = data?.total_pages ?? Math.max(1, Math.ceil(total / pageSize));
  const pageNumbers = getPaginationWindow(page, totalPages);

  useEffect(() => {
    setPage(1);
  }, [searchParams]);

  useEffect(() => {
    if (data && page > totalPages) {
      setPage(totalPages);
    }
  }, [data, page, totalPages]);

  const copyRequestId = async (value?: string | null) => {
    const result = await copyTextToClipboard(value);
    if (result.status === 'empty') {
      setNotice('当前样本没有 request_id');
      return;
    }
    if (result.status === 'unavailable') {
      setNotice('无法自动复制 request_id，请选中文本手动复制');
      return;
    }
    if (result.status === 'success') {
      setNotice('request_id 已复制');
      void trackUsageEvent('copy_request_id', {
        module: TRACKING_MODULE,
        entity_type: 'performance_event',
        entity_id: result.text ?? 'unknown',
        request_id: result.text ?? 'unknown',
      });
      return;
    }
    setNotice('自动复制失败，请选中文本手动复制');
  };

  return (
    <main className="page-shell sku-page admin-list-page">
      <section className="page-hero log-audit-hero">
        <div>
          <p className="eyebrow">OBSERVABILITY / RUM SAMPLES</p>
          <h1 className="page-title">性能样本</h1>
          <p className="page-desc">查看聚合维度下最近受控性能样本。</p>
        </div>
        <button type="button" className="btn" onClick={() => navigate('/admin/performance')}>
          <ArrowLeft size={14} aria-hidden />
          返回
        </button>
      </section>

      <section className="filter-card log-audit-filter" aria-label="样本上下文">
        <div className="performance-sample-context-grid">
          <ContextItem label="页面" value={params.page_key ?? '未指定'} />
          <ContextItem label="版本号" value={params.app_version ?? '版本未知'} />
          <ContextItem label="端类型" value={clientLabel(params.client_type ?? '')} />
          <ContextItem label="设备" value={params.device_class ?? '设备未知'} />
          <ContextItem label="网络" value={params.network_type ?? '网络未知'} />
          <ContextItem label="指标" value={metricLabel(params.metric_name ?? '')} />
        </div>
      </section>

      <section className="table-card" aria-label="性能样本列表">
        {notice ? <div className="performance-copy-notice" role="status">{notice}</div> : null}
        {error ? <div className="empty-state">{error}</div> : null}
        {loading ? <div className="empty-state"><Activity size={16} /> 加载样本中...</div> : null}
        {!error && !loading && data && !data.items.length ? <div className="empty-state">暂无匹配样本</div> : null}
        {!error && !loading && data?.items.length ? (
          <div className="log-audit-table-wrap">
            <table className="log-audit-table">
              <thead>
                <tr>
                  <th>页面</th>
                  <th>版本号</th>
                  <th>端类型</th>
                  <th>设备</th>
                  <th>网络</th>
                  <th>指标</th>
                  <th>耗时</th>
                  <th>事件时间</th>
                  <th>接收时间</th>
                  <th>request_id</th>
                </tr>
              </thead>
              <tbody>
                {data.items.map((item) => (
                  <tr key={item.id}>
                    <td><span className="log-summary performance-page-key"><span>{item.page_key}</span></span></td>
                    <td>{item.app_version || '版本未知'}</td>
                    <td>{clientLabel(item.client_type)}</td>
                    <td>{item.device_class || '设备未知'}</td>
                    <td>{item.network_type || '网络未知'}</td>
                    <td>{metricLabel(item.metric_name)}</td>
                    <td className={item.duration_ms >= 3000 ? 'duration danger' : 'duration'}>{formatMs(item.duration_ms)}</td>
                    <td>{formatTimestamp(item.occurred_at)}</td>
                    <td>{formatTimestamp(item.server_received_at)}</td>
                    <td>
                      <div className="request-id-cell">
                        <code className="request-id" title={item.request_id?.trim() || undefined}>{shortRequestId(item.request_id?.trim())}</code>
                        {item.request_id?.trim() ? (
                          <button className="request-copy-action" type="button" aria-label="复制 request_id" onClick={() => void copyRequestId(item.request_id)}>
                            <Copy size={13} aria-hidden />
                          </button>
                        ) : null}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}
        {!error && data && total > 0 ? (
          <div className="pagination">
            <div className="page-summary">共 {loading ? '…' : total} 条样本</div>
            <div className="page-right">
              <div className="page-buttons">
                <button type="button" className="page-btn" disabled={page <= 1} onClick={() => setPage((current) => Math.max(1, current - 1))} aria-label="上一页">‹</button>
                {pageNumbers.map((pageNumber) => (
                  <button
                    key={pageNumber}
                    type="button"
                    className={`page-btn${pageNumber === page ? ' active' : ''}`}
                    aria-current={pageNumber === page ? 'page' : undefined}
                    onClick={() => setPage(pageNumber)}
                  >
                    {pageNumber}
                  </button>
                ))}
                <button type="button" className="page-btn" disabled={page >= totalPages} onClick={() => setPage((current) => Math.min(totalPages, current + 1))} aria-label="下一页">›</button>
              </div>
              <div className="page-size-wrap">
                <span>每页显示</span>
                <select
                  className="page-size"
                  value={pageSize}
                  aria-label="每页显示条数"
                  onChange={(event) => {
                    setPageSize(Number(event.target.value));
                    setPage(1);
                  }}
                >
                  {PAGE_SIZE_OPTIONS.map((option) => <option key={option} value={option}>{option} 条</option>)}
                </select>
              </div>
            </div>
          </div>
        ) : null}
      </section>
    </main>
  );
}

function ContextItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <span className="field-label">{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function formatMs(value?: number | null) {
  if (value === null || value === undefined) {
    return '-';
  }
  return `${value}ms`;
}

function formatTimestamp(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString('zh-CN', { hour12: false });
}

function shortRequestId(value?: string | null) {
  if (!value) {
    return '-';
  }
  if (value.length <= 14) {
    return value;
  }
  return `${value.slice(0, 7)}...${value.slice(-4)}`;
}

function clientLabel(value: string) {
  return clientLabels[value] ?? value;
}

function metricLabel(value: string) {
  return performanceMetricLabel(value);
}
