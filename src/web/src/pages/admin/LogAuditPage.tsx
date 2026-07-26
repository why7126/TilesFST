import { Copy, RotateCcw, X } from 'lucide-react';
import { useCallback, useEffect, useMemo, useState } from 'react';

import { fetchLogDetail, fetchLogObservability, fetchLogs, type LogObservabilityQuery, type LogQuery } from '@/features/admin/api/logs-api';
import { fetchUsers } from '@/features/admin/api/users-api';
import { AdminToast } from '@/features/admin/components/AdminToast';
import { copyTextToClipboard } from '@/shared/lib/clipboard';
import { getPaginationWindow } from '@/shared/lib/pagination-window';
import '@/features/admin/styles/user-management.css';
import '@/features/admin/styles/log-audit.css';
import { getErrorMessage } from '@/features/auth/api/auth-api';
import { trackUsageEvent } from '@/features/tracking/api/usage-tracking';
import type {
  ListLogsApiV1AdminLogsGetLogType,
  LogDetailData,
  LogDetailSection,
  LogListData,
  LogListItem,
  LogObservabilityData,
  ObservabilityDistributionItem,
  ObservabilityEndpointItem,
  ObservabilitySlowRequestItem,
  ObservabilitySpanItem,
  ObservabilityTaskItem,
  RequestSnapshotData,
  TaskTraceData,
  UserAdminItem,
} from '@/shared/api/generated';
import { MetricCard, MetricCardGrid } from '@/shared/ui/metric-card';
import { SearchableSelect, type SearchableSelectOption } from '@/shared/ui/searchable-select';

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
  taskTraceId: string;
};

const defaultFilters: Filters = {
  logType: ALL_VALUE,
  timeRange: '1d',
  actor: '',
  status: '',
  pathOrRequestId: '',
  taskTraceId: '',
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

const timeRangeOptions = [
  { value: '5m', label: '最近5分钟', minutes: 5 },
  { value: '10m', label: '最近10分钟', minutes: 10 },
  { value: '30m', label: '最近30分钟', minutes: 30 },
  { value: '1h', label: '最近1小时', minutes: 60 },
  { value: '3h', label: '最近3小时', minutes: 60 * 3 },
  { value: '6h', label: '最近6小时', minutes: 60 * 6 },
  { value: '12h', label: '最近12小时', minutes: 60 * 12 },
  { value: '1d', label: '最近1天', minutes: 60 * 24 },
  { value: '2d', label: '最近2天', minutes: 60 * 24 * 2 },
  { value: '3d', label: '最近3天', minutes: 60 * 24 * 3 },
  { value: '7d', label: '最近7天', minutes: 60 * 24 * 7 },
];

function buildQuery(filters: Filters, page: number, pageSize: number): LogQuery {
  const statusFilter = parseStatusFilter(filters.status);
  const pathOrRequestId = filters.pathOrRequestId.trim();
  const taskTraceId = filters.taskTraceId.trim();
  return {
    page,
    page_size: pageSize,
    log_type: filters.logType === ALL_VALUE ? undefined : filters.logType as ListLogsApiV1AdminLogsGetLogType,
    actor_user_id: filters.actor || undefined,
    status_code: statusFilter.status_code,
    result: statusFilter.result,
    path_or_request_id: pathOrRequestId || undefined,
    task_trace_id: taskTraceId || undefined,
    ...timeRangeToParams(filters.timeRange),
  };
}

function buildObservabilityQuery(filters: Filters): LogObservabilityQuery {
  const statusFilter = parseStatusFilter(filters.status);
  const pathOrRequestId = filters.pathOrRequestId.trim();
  const taskTraceId = filters.taskTraceId.trim();
  const timeRange = timeRangeToParams(filters.timeRange);
  return {
    log_type: filters.logType === ALL_VALUE ? undefined : filters.logType as LogObservabilityQuery['log_type'],
    status_code: statusFilter.status_code,
    result: statusFilter.result,
    path_or_request_id: pathOrRequestId || undefined,
    request_id: pathOrRequestId.startsWith('req_') ? pathOrRequestId : undefined,
    task_trace_id: taskTraceId || undefined,
    start_time: timeRange.start_time,
    end_time: timeRange.end_time,
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
  const minutes = timeRangeOptions.find((option) => option.value === value)?.minutes;
  if (!minutes) {
    return {};
  }
  const start = new Date(Date.now() - minutes * 60 * 1000);
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

function shortClientRequestId(value?: string | null) {
  if (!value) {
    return '-';
  }
  if (value.length <= 20) {
    return value;
  }
  return `${value.slice(0, 12)}…${value.slice(-5)}`;
}

function shortTaskTraceId(value?: string | null) {
  if (!value) {
    return '-';
  }
  if (value.length <= 18) {
    return value;
  }
  return `${value.slice(0, 11)}…${value.slice(-5)}`;
}

function getTaskStatusLabel(value?: string | null) {
  if (!value) {
    return '-';
  }
  const labels: Record<string, string> = {
    processing: '处理中',
    success: '成功',
    failed: '失败',
    timeout: '超时',
    cancelled: '已取消',
    skipped: '跳过',
  };
  return labels[value] ?? value;
}

function getActorAccount(item: LogListItem) {
  return item.actor_username?.trim() || item.actor_role?.trim() || 'anonymous';
}

function formatMetric(value?: number) {
  return typeof value === 'number' ? value.toLocaleString('en-US') : '--';
}

function formatPercent(value?: number | null) {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    return '--';
  }
  return `${Math.round(value * 1000) / 10}%`;
}

function maxDistributionCount(items: ObservabilityDistributionItem[]) {
  return Math.max(1, ...items.map((item) => item.count));
}

function isSlowRequestItem(item: ObservabilitySlowRequestItem | ObservabilityTaskItem | ObservabilitySpanItem): item is ObservabilitySlowRequestItem {
  return 'log_id' in item;
}

function isTaskItem(item: ObservabilitySlowRequestItem | ObservabilityTaskItem | ObservabilitySpanItem): item is ObservabilityTaskItem {
  return 'task_trace_id' in item && 'task_type' in item && !('span_name' in item);
}

function isSpanItem(item: ObservabilitySlowRequestItem | ObservabilityTaskItem | ObservabilitySpanItem): item is ObservabilitySpanItem {
  return 'span_name' in item;
}

function getOperatorLabel(user: UserAdminItem) {
  return user.display_name?.trim() || user.username;
}

function getOperatorDescription(user: UserAdminItem) {
  return user.username;
}

function toOperatorOption(user: UserAdminItem): SearchableSelectOption {
  return {
    value: user.id,
    label: getOperatorLabel(user),
    description: getOperatorDescription(user),
  };
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

function renderSnapshotValue(value: unknown) {
  if (value === null || value === undefined || value === '') {
    return '未采集';
  }
  if (typeof value === 'boolean') {
    return value ? '是' : '否';
  }
  if (Array.isArray(value)) {
    return value.length ? value.join(', ') : '无';
  }
  if (typeof value === 'object') {
    return JSON.stringify(value, null, 2);
  }
  return String(value);
}

function getRecord(value: unknown): Record<string, unknown> {
  return value && typeof value === 'object' && !Array.isArray(value) ? value as Record<string, unknown> : {};
}

function SnapshotRows({ rows }: { rows: Array<[string, unknown]> }) {
  return (
    <dl className="snapshot-grid">
      {rows.map(([label, value]) => (
        <div key={label} className="detail-row">
          <dt>{label}</dt>
          <dd>{renderSnapshotValue(value)}</dd>
        </div>
      ))}
    </dl>
  );
}

function BodyFieldList({ fields }: { fields: unknown }) {
  const items = Array.isArray(fields) ? fields.filter((field): field is Record<string, unknown> => typeof field === 'object' && field !== null) : [];
  if (!items.length) {
    return <p className="snapshot-empty">无字段摘要</p>;
  }
  return (
    <ul className="snapshot-field-list">
      {items.map((field, index) => (
        <li key={`${String(field.name ?? 'field')}-${index}`}>
          <span>{renderSnapshotValue(field.name)}</span>
          <code>{renderSnapshotValue(field.type)}</code>
          {field.value !== undefined ? <strong>{renderSnapshotValue(field.value)}</strong> : null}
          {field.redaction ? <em>{renderSnapshotValue(field.redaction)}</em> : null}
        </li>
      ))}
    </ul>
  );
}

function RequestSnapshotSection({ snapshot }: { snapshot?: RequestSnapshotData | null }) {
  if (!snapshot) {
    return (
      <section className="log-detail-section request-snapshot-section">
        <h3>Request Snapshot</h3>
        <p className="snapshot-empty">未采集 Request Snapshot</p>
      </section>
    );
  }
  const query = getRecord(snapshot.input?.query);
  const body = getRecord(snapshot.input?.body_schema_summary);
  const redaction = getRecord(snapshot.input?.redaction_summary);
  return (
    <section className="log-detail-section request-snapshot-section">
      <h3>Request Snapshot</h3>
      {snapshot.parse_error ? <p className="snapshot-warning">{snapshot.parse_error}</p> : null}
      <div className="snapshot-block">
        <h4>请求信息</h4>
        <SnapshotRows rows={[
          ['Method', snapshot.request?.method],
          ['Path', snapshot.request?.path],
          ['Route Template', snapshot.request?.route_template],
          ['Route Match', snapshot.request?.route_match_status],
          ['Trusted Request ID', snapshot.request?.request_id],
          ['Client Request ID', snapshot.request?.client_request_id],
          ['Trusted Response Header', snapshot.request?.trusted_request_id_header],
          ['Client Request Header', snapshot.request?.client_request_id_header],
        ]} />
      </div>
      <div className="snapshot-block">
        <h4>输入摘要</h4>
        <SnapshotRows rows={[
          ['Query Allowlist', query.allowed ?? {}],
          ['Query Ignored', query.ignored_keys ?? []],
          ['Query Redacted', query.redacted_keys ?? []],
          ['Body Type', body.body_type],
          ['Content Type', body.content_type],
          ['Content Length', body.content_length],
          ['Stored Raw Body', body.stored_raw_body],
          ['Policy', redaction.policy],
        ]} />
        <BodyFieldList fields={body.fields} />
      </div>
      <div className="snapshot-block">
        <h4>业务资源</h4>
        <SnapshotRows rows={[
          ['Resource Type', snapshot.resource?.resource_type],
          ['Resource ID', snapshot.resource?.resource_id],
          ['ID Source', snapshot.resource?.id_source],
        ]} />
      </div>
      <div className="snapshot-block">
        <h4>响应结果</h4>
        <SnapshotRows rows={[
          ['Status Code', snapshot.response?.status_code],
          ['Error Code', snapshot.response?.error_code],
          ['Duration', snapshot.response?.duration_ms ? `${snapshot.response.duration_ms} ms` : null],
          ['Result', snapshot.response?.result],
          ['Error Summary', snapshot.response?.error_summary],
        ]} />
      </div>
      <div className="snapshot-block">
        <h4>操作者与客户端</h4>
        <SnapshotRows rows={[
          ['User ID', snapshot.actor?.actor_user_id],
          ['Username', snapshot.actor?.actor_username],
          ['Role', snapshot.actor?.actor_role],
          ['Client Type', snapshot.actor?.client_type],
          ['IP', snapshot.actor?.ip_summary],
          ['User Agent', snapshot.actor?.user_agent_summary],
        ]} />
      </div>
      <div className="snapshot-block">
        <h4>环境与时间</h4>
        <SnapshotRows rows={[
          ['Environment', snapshot.timing?.environment],
          ['Started At', snapshot.timing?.started_at],
          ['Finished At', snapshot.timing?.finished_at],
        ]} />
      </div>
      <details className="snapshot-json">
        <summary>Snapshot JSON</summary>
        <pre>{snapshot.raw_json}</pre>
      </details>
    </section>
  );
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

function DistributionList({ title, items }: { title: string; items?: ObservabilityDistributionItem[] }) {
  const rows = items ?? [];
  const maxCount = maxDistributionCount(rows);
  return (
    <section className="observability-block">
      <h3>{title}</h3>
      {rows.length ? (
        <ul className="observability-bars">
          {rows.map((item) => (
            <li key={`${title}-${item.label}`}>
              <div>
                <span>{item.label || '-'}</span>
                <strong>{formatMetric(item.count)}</strong>
              </div>
              <span className="observability-bar-track" aria-hidden>
                <span style={{ width: `${Math.max(4, Math.round((item.count / maxCount) * 100))}%` }} />
              </span>
            </li>
          ))}
        </ul>
      ) : <p className="observability-empty">暂无数据</p>}
    </section>
  );
}

function EndpointErrorList({ items }: { items: ObservabilityEndpointItem[] }) {
  return (
    <section className="observability-block">
      <h3>错误接口</h3>
      {items.length ? (
        <ul className="observability-list">
          {items.map((item) => (
            <li key={`${item.method}-${item.path}-${item.status_code ?? 'none'}`}>
              <div>
                <strong>{item.method} {item.path}</strong>
                <span>{item.status_code ?? '-'} · {formatPercent(item.error_rate)}</span>
              </div>
              <code>{formatMetric(item.error_count)} / {formatMetric(item.request_count)}</code>
            </li>
          ))}
        </ul>
      ) : <p className="observability-empty">暂无错误接口</p>}
    </section>
  );
}

function TraceResults({ data }: { data: LogObservabilityData['trace_results'] }) {
  const hasQuery = Boolean(data.request_id || data.task_trace_id);
  if (!hasQuery) {
    return null;
  }
  const logIds = data.log_ids ?? [];
  const requestIds = data.request_ids ?? [];
  const taskTraceIds = data.task_trace_ids ?? [];
  return (
    <section className="observability-block trace-results">
      <h3>链路定位</h3>
      {data.reason === 'not_found' ? (
        <p className="observability-empty">未找到匹配链路</p>
      ) : (
        <div className="trace-result-grid">
          <div><span>日志</span><strong>{logIds.length}</strong></div>
          <div><span>Request ID</span><strong>{requestIds.length}</strong></div>
          <div><span>Task Trace</span><strong>{taskTraceIds.length}</strong></div>
        </div>
      )}
    </section>
  );
}

function TaskTraceGroup({
  trace,
  onCopyTaskTraceId,
  onCopyParentRequestId,
  onCopySpanRequestId,
}: {
  trace: TaskTraceData;
  onCopyTaskTraceId: (value?: string | null) => void;
  onCopyParentRequestId: (value?: string | null) => void;
  onCopySpanRequestId: (value?: string | null) => void;
}) {
  const parentRequestId = trace.parent_request_id?.trim();
  return (
    <div className="task-trace-group">
      <div className="task-trace-summary">
        <div>
          <span>task_trace_id</span>
          <button type="button" className="task-copy-button" onClick={() => onCopyTaskTraceId(trace.task_trace_id)}>
            <code>{trace.task_trace_id}</code>
            <Copy size={13} aria-hidden />
          </button>
        </div>
        <div>
          <span>parent_request_id</span>
          {parentRequestId ? (
            <button type="button" className="task-copy-button" onClick={() => onCopyParentRequestId(parentRequestId)}>
              <code>{parentRequestId}</code>
              <Copy size={13} aria-hidden />
            </button>
          ) : (
            <strong>未记录</strong>
          )}
        </div>
        <div><span>任务类型</span><strong>{trace.task_type}</strong></div>
        <div><span>任务状态</span><strong>{getTaskStatusLabel(trace.status)}</strong></div>
        <div><span>总耗时</span><strong>{trace.duration_ms ?? '-'} ms</strong></div>
      </div>
      <ol className="task-trace-timeline">
        {trace.spans.map((span, index) => (
          <li key={`${trace.task_trace_id}-${span.span_name}-${index}`} className={span.is_slowest ? 'slowest' : undefined}>
            <div className="timeline-dot" aria-hidden />
            <div className="timeline-body">
              <div className="timeline-head">
                <strong>{span.span_name}</strong>
                <span>{getTaskStatusLabel(span.status)}</span>
              </div>
              <p>{span.summary}</p>
              <div className="timeline-meta">
                <span>{span.duration_ms ?? '-'} ms</span>
                {span.error_code ? <span>{span.error_code}</span> : null}
                {span.request_id ? (
                  <button type="button" onClick={() => onCopySpanRequestId(span.request_id)}>
                    {shortRequestId(span.request_id)}
                  </button>
                ) : (
                  <span>request_id 未记录</span>
                )}
                {span.is_slowest ? <span>耗时最高节点</span> : null}
              </div>
            </div>
          </li>
        ))}
      </ol>
    </div>
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
  const [operatorOptions, setOperatorOptions] = useState<SearchableSelectOption[]>([]);
  const [selectedOperator, setSelectedOperator] = useState<SearchableSelectOption | null>(null);
  const [operatorLoading, setOperatorLoading] = useState(false);
  const [operatorError, setOperatorError] = useState<string | null>(null);
  const [observability, setObservability] = useState<LogObservabilityData | null>(null);
  const [observabilityLoading, setObservabilityLoading] = useState(true);
  const [observabilityError, setObservabilityError] = useState<string | null>(null);

  const query = useMemo(() => buildQuery(filters, page, pageSize), [filters, page, pageSize]);
  const observabilityQuery = useMemo(() => buildObservabilityQuery(filters), [filters]);
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

  const loadObservability = useCallback(async () => {
    setObservabilityLoading(true);
    setObservabilityError(null);
    try {
      const nextData = await fetchLogObservability(observabilityQuery);
      setObservability(nextData);
    } catch (error) {
      const message = getErrorMessage(error, '加载链路观测失败');
      setObservabilityError(message);
      setNotice(message);
    } finally {
      setObservabilityLoading(false);
    }
  }, [observabilityQuery]);

  useEffect(() => {
    void loadObservability();
  }, [loadObservability]);

  const loadOperatorCandidates = useCallback(async (keyword: string) => {
    setOperatorLoading(true);
    setOperatorError(null);
    try {
      const result = await fetchUsers({
        page: 1,
        page_size: 20,
        keyword: keyword.trim() || undefined,
      });
      const nextOptions = result.items.map(toOperatorOption);
      setOperatorOptions((current) => {
        const selected = selectedOperator ?? current.find((option) => option.value === filters.actor);
        if (!selected || nextOptions.some((option) => option.value === selected.value)) {
          return nextOptions;
        }
        return [selected, ...nextOptions];
      });
    } catch (error) {
      const message = getErrorMessage(error, '加载操作者候选失败');
      setOperatorError(message);
      setNotice(message);
    } finally {
      setOperatorLoading(false);
    }
  }, [filters.actor, selectedOperator]);

  useEffect(() => {
    void loadOperatorCandidates('');
  }, [loadOperatorCandidates]);

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
    setSelectedOperator(null);
    setPage(1);
    void trackUsageEvent('filter_change', {
      module: TRACKING_MODULE,
      entity_type: 'log_query',
      entity_id: 'all',
      filter_name: 'all',
      filter_value: 'reset',
    });
  };

  const updateOperatorFilter = (value: string | null) => {
    const nextValue = value ?? '';
    const nextOperator = operatorOptions.find((option) => option.value === value) ?? null;
    setSelectedOperator(nextOperator);
    updateFilter('actor', nextValue);
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

  const copyClientRequestId = async (value?: string | null) => {
    const result = await copyTextToClipboard(value);
    if (result.status === 'empty') {
      setNotice('当前日志没有 client_request_id');
      return;
    }
    if (result.status === 'unavailable') {
      setNotice('无法自动复制 client_request_id，请打开日志详情选中文本手动复制');
      return;
    }
    if (result.status === 'success') {
      setNotice('client_request_id 已复制');
      void trackUsageEvent('copy_request_id', {
        module: TRACKING_MODULE,
        entity_type: 'client_request',
        entity_id: result.text ?? 'unknown',
        request_id: detail?.log.request_id ?? undefined,
        client_request_id: result.text ?? 'unknown',
      });
      return;
    }
    setNotice('自动复制失败，请打开日志详情选中文本手动复制');
  };

  const copyParentRequestId = async (value?: string | null) => {
    const result = await copyTextToClipboard(value);
    if (result.status === 'empty') {
      setNotice('当前任务没有 parent_request_id');
      return;
    }
    if (result.status === 'unavailable') {
      setNotice('无法自动复制 parent_request_id，请打开日志详情选中文本手动复制');
      return;
    }
    if (result.status === 'success') {
      setNotice('parent_request_id 已复制');
      void trackUsageEvent('copy_request_id', {
        module: TRACKING_MODULE,
        entity_type: 'parent_request',
        entity_id: result.text ?? 'unknown',
        request_id: result.text ?? 'unknown',
        task_trace_id: detail?.task_trace?.task_trace_id ?? undefined,
      });
      return;
    }
    setNotice('自动复制失败，请打开日志详情选中文本手动复制');
  };

  const copyTaskTraceId = async (value?: string | null) => {
    const result = await copyTextToClipboard(value);
    if (result.status === 'empty') {
      setNotice('当前日志没有 task_trace_id');
      return;
    }
    if (result.status === 'unavailable') {
      setNotice('无法自动复制 task_trace_id，请打开日志详情选中文本手动复制');
      return;
    }
    if (result.status === 'success') {
      setNotice('task_trace_id 已复制');
      void trackUsageEvent('copy_request_id', {
        module: TRACKING_MODULE,
        entity_type: 'task_trace',
        entity_id: result.text ?? 'unknown',
        request_id: detail?.log.request_id ?? undefined,
        task_trace_id: result.text ?? 'unknown',
      });
      return;
    }
    setNotice('自动复制失败，请打开日志详情选中文本手动复制');
  };

  const openDetail = (item: LogListItem) => {
    setSelectedId(item.id);
  };

  const openLogDetail = (logId: string) => {
    setSelectedId(logId);
  };

  const filterByTaskTrace = (taskTraceId: string) => {
    updateFilter('taskTraceId', taskTraceId);
  };

  const filterByRequestId = (requestId: string) => {
    updateFilter('pathOrRequestId', requestId);
  };

  const rankingItems = observability?.rankings ?? {};
  const slowRequests = (rankingItems.slow_requests ?? []).filter(isSlowRequestItem);
  const slowTasks = (rankingItems.slow_tasks ?? []).filter(isTaskItem);
  const slowestSpans = (rankingItems.slowest_spans ?? []).filter(isSpanItem);

  return (
    <>
      <AdminToast message={notice} />
      <section className="page-hero log-audit-hero">
        <div>
          <p className="eyebrow">SYSTEM / LOG AUDIT</p>
          <h1 className="page-title">日志审计</h1>
          <p className="page-desc">查询 API 请求日志、产品行为事件与审计操作，通过 request_id 与 task_trace_id 快速定位异常链路。</p>
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

      <section className="table-card log-observability-panel" aria-label="链路观测仪表">
        <header className="observability-header">
          <div>
            <p className="eyebrow">OBSERVABILITY</p>
            <h2>链路观测</h2>
          </div>
          <button className="btn" type="button" onClick={() => void loadObservability()}>
            刷新
          </button>
        </header>
        {observabilityLoading && !observability ? (
          <p className="observability-empty">加载观测数据中...</p>
        ) : observabilityError && !observability ? (
          <p className="observability-empty">{observabilityError}</p>
        ) : observability ? (
          <>
            <MetricCardGrid ariaLabel="链路观测摘要">
              <MetricCard label="TOTAL LOGS" value={formatMetric(observability.summary.total_logs)} description="筛选范围" />
              <MetricCard
                label="API ERROR RATE"
                value={formatPercent(observability.summary.api_error_rate)}
                description={`${formatMetric(observability.summary.api_errors)} 个异常请求`}
                dangerDescription={observability.summary.api_error_rate > 0}
              />
              <MetricCard
                label="TASK SUCCESS"
                value={formatPercent(observability.summary.task_success_rate)}
                description={`${formatMetric(observability.summary.failed_tasks)} 个失败任务`}
                dangerDescription={(observability.summary.failed_tasks ?? 0) > 0}
              />
              <MetricCard
                label="SLOW TASKS"
                value={formatMetric(observability.summary.slow_tasks)}
                description={`超过 ${formatMetric(observability.thresholds.task_duration_ms)}ms`}
                dangerDescription={observability.summary.slow_tasks > 0}
              />
            </MetricCardGrid>
            <div className="observability-grid">
              <DistributionList title="客户端分布" items={observability.distributions.clients} />
              <DistributionList title="任务状态" items={observability.distributions.task_statuses} />
              <DistributionList title="失败原因" items={observability.distributions.failure_reasons} />
              <DistributionList title="行为事件" items={observability.distributions.behavior_events} />
              <EndpointErrorList items={observability.endpoint_errors} />
              <TraceResults data={observability.trace_results} />
            </div>
            <section className="observability-rankings" aria-label="慢链路排行">
              <div className="observability-block">
                <h3>慢请求</h3>
                {slowRequests.length ? (
                  <ul className="observability-list">
                    {slowRequests.map((item) => (
                      <li key={item.log_id}>
                        <div>
                          <strong>{item.method} {item.path}</strong>
                          <span>{item.duration_ms}ms · {item.status_code}</span>
                        </div>
                        <button type="button" onClick={() => openLogDetail(item.log_id)}>查看</button>
                      </li>
                    ))}
                  </ul>
                ) : <p className="observability-empty">暂无慢请求</p>}
              </div>
              <div className="observability-block">
                <h3>慢任务</h3>
                {slowTasks.length ? (
                  <ul className="observability-list">
                    {slowTasks.map((item) => (
                      <li key={item.task_trace_id}>
                        <div>
                          <strong>{item.task_type}</strong>
                          <span>{item.duration_ms ?? '-'}ms · {getTaskStatusLabel(item.status)}</span>
                        </div>
                        <button type="button" onClick={() => filterByTaskTrace(item.task_trace_id)}>筛选</button>
                      </li>
                    ))}
                  </ul>
                ) : <p className="observability-empty">暂无慢任务</p>}
              </div>
              <div className="observability-block">
                <h3>慢节点</h3>
                {slowestSpans.length ? (
                  <ul className="observability-list">
                    {slowestSpans.map((item) => (
                      <li key={`${item.task_trace_id}-${item.span_name}`}>
                        <div>
                          <strong>{item.span_name}</strong>
                          <span>{item.duration_ms ?? '-'}ms · {item.task_type}</span>
                        </div>
                        {item.request_id ? (
                          <button type="button" onClick={() => filterByRequestId(item.request_id ?? '')}>定位</button>
                        ) : (
                          <button type="button" onClick={() => filterByTaskTrace(item.task_trace_id)}>筛选</button>
                        )}
                      </li>
                    ))}
                  </ul>
                ) : <p className="observability-empty">暂无慢节点</p>}
              </div>
            </section>
          </>
        ) : null}
      </section>

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
              {timeRangeOptions.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
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
            <span className="field-label">操作者</span>
            <SearchableSelect
              value={filters.actor || null}
              options={operatorOptions}
              onChange={updateOperatorFilter}
              onSearch={loadOperatorCandidates}
              placeholder="搜索用户名称或账号"
              aria-label="操作者"
              loading={operatorLoading}
              error={operatorError}
              emptyText="无匹配操作者"
              loadingText="加载操作者中..."
              clearable
              clearLabel="清空操作者筛选"
            />
          </label>
          <label>
            <span className="field-label">Task Trace ID</span>
            <input className="input" value={filters.taskTraceId} onChange={(event) => updateFilter('taskTraceId', event.target.value)} placeholder="task_upload_video_xxx" />
          </label>
          <label>
            <span className="field-label">路径 / Request ID</span>
            <input className="input" value={filters.pathOrRequestId} onChange={(event) => updateFilter('pathOrRequestId', event.target.value)} placeholder="接口路径或 request_id" />
          </label>
          <div className="log-audit-filter-actions">
            <button className="btn" type="button" onClick={resetFilters}>
              <RotateCcw size={14} aria-hidden />
              重置
            </button>
          </div>
        </div>
        <p className="filter-hint">默认展示最近1天；路径、request_id 与 task_trace_id 均走后端分页筛选。</p>
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
                <th>Task Trace</th>
                <th>request_id</th>
                <th>client_request_id</th>
                <th className="log-audit-action-cell admin-sticky-action-cell">操作</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={11} className="log-audit-empty">加载日志中...</td></tr>
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
                    <td><span className="actor-account" title={getActorAccount(item)}>{getActorAccount(item)}</span></td>
                    <td>{item.client_type}</td>
                    <td><span className={`log-status ${statusClass(item)}`}>{item.result}</span></td>
                    <td className={item.duration_ms && item.duration_ms >= 1000 ? 'duration danger' : 'duration'}>{item.duration_ms ?? '-'}{item.duration_ms ? 'ms' : ''}</td>
                    <td>
                      <div className="task-trace-cell">
                        <code className="task-trace-id" title={item.task_trace_id?.trim() || undefined}>{shortTaskTraceId(item.task_trace_id?.trim())}</code>
                        {item.task_trace_id?.trim() ? (
                          <button className="request-copy-action" type="button" aria-label="复制 task_trace_id" onClick={() => void copyTaskTraceId(item.task_trace_id)}>
                            <Copy size={13} aria-hidden />
                          </button>
                        ) : null}
                      </div>
                    </td>
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
                    <td>
                      <div className="request-id-cell">
                        <code className="request-id" title={item.client_request_id?.trim() || undefined}>{shortClientRequestId(item.client_request_id?.trim())}</code>
                        {item.client_request_id?.trim() ? (
                          <button className="request-copy-action" type="button" aria-label="复制 client_request_id" onClick={() => void copyClientRequestId(item.client_request_id)}>
                            <Copy size={13} aria-hidden />
                          </button>
                        ) : null}
                      </div>
                    </td>
                    <td className="log-audit-action-cell admin-sticky-action-cell"><button className="log-audit-view-action" type="button" onClick={() => openDetail(item)}>查看</button></td>
                  </tr>
                ))
              ) : (
                <tr><td colSpan={11} className="log-audit-empty">暂无匹配日志</td></tr>
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
                <RequestSnapshotSection snapshot={detail.request_snapshot} />
                {(detail.related_task_traces?.length || detail.task_trace) ? (
                  <section className="log-detail-section task-trace-section">
                    <h3>Task Trace</h3>
                    {(detail.related_task_traces?.length ? detail.related_task_traces : [detail.task_trace!]).map((trace) => (
                      <TaskTraceGroup
                        key={trace.task_trace_id}
                        trace={trace}
                        onCopyTaskTraceId={(value) => void copyTaskTraceId(value)}
                        onCopyParentRequestId={(value) => void copyParentRequestId(value)}
                        onCopySpanRequestId={(value) => void copyRequestId(value)}
                      />
                    ))}
                  </section>
                ) : null}
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
