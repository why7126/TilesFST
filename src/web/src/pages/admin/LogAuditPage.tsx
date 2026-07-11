import { Copy, RotateCcw, X } from 'lucide-react';
import { useCallback, useEffect, useMemo, useState } from 'react';

import { fetchLogDetail, fetchLogs, type LogQuery } from '@/features/admin/api/logs-api';
import { AdminToast } from '@/features/admin/components/AdminToast';
import { copyTextToClipboard } from '@/shared/lib/clipboard';
import { getPaginationWindow } from '@/shared/lib/pagination-window';
import '@/features/admin/styles/user-management.css';
import '@/features/admin/styles/log-audit.css';
import { getErrorMessage } from '@/features/auth/api/auth-api';
import { trackUsageEvent } from '@/features/tracking/api/usage-tracking';
import type { LogDetailData, LogDetailSection, LogListData, LogListItem } from '@/shared/api/generated';
import { MetricCard, MetricCardGrid } from '@/shared/ui/metric-card';

const DEFAULT_PAGE_SIZE = 20;
const PAGE_SIZE_OPTIONS = [10, 20, 50, 100];
const ALL_VALUE = 'all';
const TRACKING_MODULE = 'log_audit';

type Filters = {
  logType: string;
  timeRange: string;
  actor: string;
  status: string;
  pathOrRequestId: string;
};

const defaultFilters: Filters = {
  logType: ALL_VALUE,
  timeRange: '24h',
  actor: '',
  status: '',
  pathOrRequestId: '',
};

const logTypeLabels: Record<string, string> = {
  request: '请求日志',
  usage_event: '行为事件',
  audit: '审计操作',
};

const baseStatusFilterOptions = [
  { value: ALL_VALUE, label: '全部状态' },
  { value: 'result:success', label: '成功' },
  { value: 'result:failed', label: '失败' },
  { value: 'status:200', label: '200 成功' },
  { value: 'status:201', label: '201 已创建' },
  { value: 'status:204', label: '204 无内容' },
  { value: 'status:301', label: '301 永久重定向' },
  { value: 'status:302', label: '302 临时重定向' },
  { value: 'status:304', label: '304 未修改' },
  { value: 'status:400', label: '400 请求错误' },
  { value: 'status:401', label: '401 未认证' },
  { value: 'status:403', label: '403 无权限' },
  { value: 'status:404', label: '404 不存在' },
  { value: 'status:409', label: '409 状态冲突' },
  { value: 'status:422', label: '422 参数校验错误' },
  { value: 'status:429', label: '429 请求过多' },
  { value: 'status:500', label: '500 服务异常' },
  { value: 'status:502', label: '502 网关错误' },
  { value: 'status:503', label: '503 服务不可用' },
  { value: 'status:504', label: '504 网关超时' },
];

function buildQuery(filters: Filters, page: number, pageSize: number): LogQuery {
  const statusFilter = parseStatusFilter(filters.status);
  return {
    page,
    page_size: pageSize,
    log_type: filters.logType === ALL_VALUE ? undefined : filters.logType,
    actor_user_id: filters.actor || undefined,
    status_code: statusFilter.status_code,
    result: statusFilter.result,
    path_or_request_id: filters.pathOrRequestId || undefined,
    ...timeRangeToParams(filters.timeRange),
  };
}

function parseStatusFilter(value: string): Pick<LogQuery, 'status_code' | 'result'> {
  if (!value || value === ALL_VALUE) {
    return {};
  }
  if (value.startsWith('result:')) {
    return { result: value.slice('result:'.length) };
  }
  if (value.startsWith('status:')) {
    const statusCode = Number(value.slice('status:'.length));
    return Number.isFinite(statusCode) ? { status_code: statusCode } : {};
  }
  return {};
}

function timeRangeToParams(value: string): Pick<LogQuery, 'start_time' | 'end_time'> {
  const hours = value === '7d' ? 24 * 7 : value === 'all' ? 0 : 24;
  if (!hours) {
    return {};
  }
  const start = new Date(Date.now() - hours * 60 * 60 * 1000);
  return { start_time: start.toISOString() };
}

function getLogTypeLabel(value: string) {
  return logTypeLabels[value] ?? value;
}

function getStatusFilterOptions(items: LogListItem[] = []) {
  const options = [...baseStatusFilterOptions];
  const existingValues = new Set(options.map((option) => option.value));
  const extraStatusCodes = Array.from(
    new Set(
      items
        .map((item) => item.status_code)
        .filter((statusCode): statusCode is number => typeof statusCode === 'number'),
    ),
  ).sort((a, b) => a - b);

  extraStatusCodes.forEach((statusCode) => {
    const value = `status:${statusCode}`;
    if (!existingValues.has(value)) {
      options.push({ value, label: `${statusCode} 状态码` });
    }
  });
  return options;
}

function formatTime(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

function statusClass(item: LogListItem) {
  const result = item.result.toLowerCase();
  const statusCode = item.status_code ?? 0;
  if (statusCode >= 500 || result.includes('错误') || result.includes('失败') || result.includes('failed')) {
    return 'status-failed status-server-error';
  }
  if (statusCode >= 400 || result.includes('告警') || result.includes('异常')) {
    return 'status-warning status-client-error';
  }
  if ((statusCode >= 200 && statusCode < 400) || result.includes('成功') || result.includes('success')) {
    return 'status-success status-ok';
  }
  return 'status-neutral';
}

function shortRequestId(value?: string | null) {
  if (!value) {
    return '-';
  }
  if (value.length <= 14) {
    return value;
  }
  return `${value.slice(0, 7)}…${value.slice(-4)}`;
}

function formatMetric(value?: number) {
  return typeof value === 'number' ? value.toLocaleString('en-US') : '--';
}

function renderFieldValue(value: unknown) {
  if (Array.isArray(value)) {
    return value.join(', ');
  }
  if (value === null || value === undefined || value === '') {
    return '-';
  }
  return String(value);
}

function nowMs() {
  return typeof performance !== 'undefined' ? performance.now() : Date.now();
}

function elapsedMs(startedAt: number) {
  return Math.max(0, Math.round(nowMs() - startedAt));
}

function DetailSection({ section }: { section: LogDetailSection }) {
  return (
    <section className="log-detail-section">
      <h3>{section.title}</h3>
      <dl>
        {Object.entries(section.fields).map(([key, value]) => (
          <div key={key} className="detail-row">
            <dt>{key}</dt>
            <dd>{renderFieldValue(value)}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}

export function LogAuditPage() {
  const [filters, setFilters] = useState<Filters>(defaultFilters);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(DEFAULT_PAGE_SIZE);
  const [data, setData] = useState<LogListData | null>(null);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<LogDetailData | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const query = useMemo(() => buildQuery(filters, page, pageSize), [filters, page, pageSize]);
  const statusFilterOptions = useMemo(() => getStatusFilterOptions(data?.items), [data?.items]);

  const loadLogs = useCallback(async () => {
    const startedAt = nowMs();
    setLoading(true);
    try {
      const nextData = await fetchLogs(query);
      setData(nextData);
      return elapsedMs(startedAt);
    } catch (error) {
      setNotice(getErrorMessage(error, '加载日志失败'));
      return elapsedMs(startedAt);
    } finally {
      setLoading(false);
    }
  }, [query]);

  useEffect(() => {
    void loadLogs();
  }, [loadLogs]);

  useEffect(() => {
    if (!notice) {
      return;
    }
    const timer = window.setTimeout(() => setNotice(null), 2600);
    return () => window.clearTimeout(timer);
  }, [notice]);

  const total = data?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const pageNumbers = getPaginationWindow(page, totalPages);

  useEffect(() => {
    setPage((current) => Math.min(current, totalPages));
  }, [totalPages]);

  useEffect(() => {
    if (!selectedId) {
      setDetail(null);
      return;
    }
    const startedAt = nowMs();
    setDetailLoading(true);
    fetchLogDetail(selectedId)
      .then((nextDetail) => {
        setDetail(nextDetail);
        void trackUsageEvent('detail_view', {
          module: TRACKING_MODULE,
          entity_type: 'log',
          entity_id: nextDetail.log.id,
          request_id: nextDetail.log.request_id,
          log_type: nextDetail.log.log_type,
        }, {
          durationMs: elapsedMs(startedAt),
        });
      })
      .catch((error) => {
        setNotice(getErrorMessage(error, '加载日志详情失败'));
        setSelectedId(null);
      })
      .finally(() => setDetailLoading(false));
  }, [selectedId]);

  useEffect(() => {
    if (!selectedId) {
      return;
    }
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setSelectedId(null);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [selectedId]);

  const updateFilter = (key: keyof Filters, value: string) => {
    setFilters((current) => ({ ...current, [key]: value }));
    setPage(1);
    void trackUsageEvent('filter_change', {
      module: TRACKING_MODULE,
      entity_type: 'log_query',
      entity_id: key,
      filter_name: key,
      filter_value: value || 'empty',
    });
  };

  const resetFilters = () => {
    setFilters(defaultFilters);
    setPage(1);
    void trackUsageEvent('filter_change', {
      module: TRACKING_MODULE,
      entity_type: 'log_query',
      entity_id: 'all',
      filter_name: 'all',
      filter_value: 'reset',
    });
  };

  const copyRequestId = async (value?: string | null) => {
    const result = await copyTextToClipboard(value);
    if (result.status === 'empty') {
      setNotice('当前日志没有 request_id');
      return;
    }
    if (result.status === 'unavailable') {
      setNotice('无法自动复制 request_id，请打开日志详情选中文本手动复制');
      return;
    }
    if (result.status === 'success') {
      setNotice('request_id 已复制');
      void trackUsageEvent('copy_request_id', {
        module: TRACKING_MODULE,
        entity_type: 'request_log',
        entity_id: result.text ?? 'unknown',
        request_id: result.text ?? 'unknown',
      });
      return;
    }
    setNotice('自动复制失败，请打开日志详情选中文本手动复制');
  };

  const openDetail = (item: LogListItem) => {
    setSelectedId(item.id);
  };

  return (
    <>
      <AdminToast message={notice} />
      <section className="page-hero log-audit-hero">
        <div>
          <p className="eyebrow">SYSTEM / LOG AUDIT</p>
          <h1 className="page-title">日志审计</h1>
          <p className="page-desc">查询 API 请求日志、产品行为事件与审计操作，通过 request_id 快速定位异常链路。</p>
        </div>
        <div className="hero-actions">
          <button className="btn" type="button" onClick={() => void loadLogs()}>
            刷新
          </button>
          <button className="btn primary" type="button" onClick={() => setNotice('审计配置沿用系统设置')}>
            查看审计配置
          </button>
        </div>
      </section>

      <MetricCardGrid ariaLabel="日志摘要">
        <MetricCard label="TODAY LOGS" value={formatMetric(data?.summary.today_logs)} description="今日总量" />
        <MetricCard
          label="API ERRORS"
          value={formatMetric(data?.summary.api_errors)}
          description="异常请求"
          dangerDescription
        />
        <MetricCard
          label="SLOW REQUESTS"
          value={formatMetric(data?.summary.slow_requests)}
          description="超过 1000ms"
          dangerDescription
        />
        <MetricCard label="SENSITIVE OPS" value={formatMetric(data?.summary.sensitive_ops)} description="审计操作" />
      </MetricCardGrid>

      <section className="filter-card log-audit-filter" aria-label="日志筛选">
        <div className="log-audit-filter-grid">
          <label>
            <span className="field-label">日志类型</span>
            <select className="select" value={filters.logType} onChange={(event) => updateFilter('logType', event.target.value)}>
              <option value={ALL_VALUE}>全部日志</option>
              <option value="request">请求日志</option>
              <option value="usage_event">行为事件</option>
              <option value="audit">审计操作</option>
            </select>
          </label>
          <label>
            <span className="field-label">时间范围</span>
            <select className="select" value={filters.timeRange} onChange={(event) => updateFilter('timeRange', event.target.value)}>
              <option value="24h">最近 24 小时</option>
              <option value="7d">最近 7 天</option>
              <option value="all">全部时间</option>
            </select>
          </label>
          <label>
            <span className="field-label">操作者</span>
            <input className="input" value={filters.actor} onChange={(event) => updateFilter('actor', event.target.value)} placeholder="User ID" />
          </label>
          <label>
            <span className="field-label">状态 / 结果</span>
            <select className="select" value={filters.status} onChange={(event) => updateFilter('status', event.target.value)}>
              {statusFilterOptions.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </label>
          <label>
            <span className="field-label">路径 / request_id</span>
            <input className="input" value={filters.pathOrRequestId} onChange={(event) => updateFilter('pathOrRequestId', event.target.value)} placeholder="接口路径或 request_id" />
          </label>
          <div className="log-audit-filter-actions">
            <button className="btn" type="button" onClick={resetFilters}>
              <RotateCcw size={14} aria-hidden />
              重置
            </button>
          </div>
        </div>
        <p className="filter-hint">默认展示最近 24 小时；request_id 与路径均走后端分页筛选。</p>
      </section>

      <section className="table-card" aria-label="日志列表">
        <div className="log-audit-table-wrap">
          <table className="log-audit-table">
            <thead>
              <tr>
                <th>时间</th>
                <th>类型</th>
                <th>事件 / 摘要</th>
                <th>操作者</th>
                <th>客户端</th>
                <th>状态</th>
                <th>耗时</th>
                <th>request_id</th>
                <th className="log-audit-action-cell admin-sticky-action-cell">操作</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={9} className="log-audit-empty">加载日志中...</td></tr>
              ) : (data?.items.length ?? 0) > 0 ? (
                data!.items.map((item) => (
                  <tr key={item.id}>
                    <td>{formatTime(item.created_at)}</td>
                    <td><span className={`log-type type-${item.log_type}`}>{getLogTypeLabel(item.log_type)}</span></td>
                    <td>
                      <button
                        className="log-summary log-summary-button"
                        type="button"
                        aria-label={`查看日志详情：${item.summary}`}
                        onClick={() => openDetail(item)}
                      >
                        <span>{item.summary}</span>
                        <small>{item.method ? `${item.method} ${item.path}` : item.event_name || item.path}</small>
                      </button>
                    </td>
                    <td>{item.actor_name || item.actor_role || 'anonymous'}</td>
                    <td>{item.client_type}</td>
                    <td><span className={`log-status ${statusClass(item)}`}>{item.result}</span></td>
                    <td className={item.duration_ms && item.duration_ms >= 1000 ? 'duration danger' : 'duration'}>{item.duration_ms ?? '-'}{item.duration_ms ? 'ms' : ''}</td>
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
                    <td className="log-audit-action-cell admin-sticky-action-cell"><button className="log-audit-view-action" type="button" onClick={() => openDetail(item)}>查看</button></td>
                  </tr>
                ))
              ) : (
                <tr><td colSpan={9} className="log-audit-empty">暂无匹配日志</td></tr>
              )}
            </tbody>
          </table>
        </div>
        <div className="pagination">
          <div className="page-summary">共 {loading ? '…' : total} 条日志</div>
          <div className="page-right">
            <div className="page-buttons">
              <button type="button" className="page-btn" disabled={page <= 1} onClick={() => setPage((p) => Math.max(1, p - 1))}>‹</button>
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
              <button type="button" className="page-btn" disabled={page >= totalPages} onClick={() => setPage((p) => Math.min(totalPages, p + 1))}>›</button>
            </div>
            <div className="page-size-wrap">
              <span>每页显示</span>
              <select className="page-size" value={pageSize} aria-label="每页显示条数" onChange={(event) => { setPageSize(Number(event.target.value)); setPage(1); }}>
                {PAGE_SIZE_OPTIONS.map((option) => <option key={option} value={option}>{option} 条</option>)}
              </select>
            </div>
          </div>
        </div>
      </section>

      {selectedId ? (
        <div className="log-drawer-layer" role="presentation">
          <button className="log-drawer-backdrop" type="button" aria-label="关闭日志详情" onClick={() => setSelectedId(null)} />
          <aside className="log-drawer" aria-label="日志详情">
            <header className="log-drawer-head">
              <div>
                <p className="eyebrow">LOG DETAIL</p>
                <h2>日志详情</h2>
                <span>{detail?.log.created_at ?? '加载中...'}</span>
              </div>
              <button className="icon-action" type="button" aria-label="关闭" onClick={() => setSelectedId(null)}>
                <X size={16} aria-hidden />
              </button>
            </header>
            {detailLoading || !detail ? (
              <div className="log-drawer-loading">加载详情中...</div>
            ) : (
              <div className="log-drawer-body">
                <DetailSection section={detail.basic} />
                <DetailSection section={detail.request} />
                <DetailSection section={detail.actor} />
                <DetailSection section={detail.context} />
                <DetailSection section={detail.event} />
                <section className="log-detail-section">
                  <h3>METADATA JSON</h3>
                  <pre>{detail.metadata_json}</pre>
                </section>
              </div>
            )}
          </aside>
        </div>
      ) : null}
    </>
  );
}
