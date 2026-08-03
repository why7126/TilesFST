import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { fetchLogDetail, fetchLogs } from '@/features/admin/api/logs-api';
import { fetchUsers } from '@/features/admin/api/users-api';
import { trackUsageEvent } from '@/features/tracking/api/usage-tracking';
import type { LogDetailData, LogListData, UserAdminListData } from '@/shared/api/generated';
import { LogAuditPage } from './LogAuditPage';

vi.mock('@/features/admin/api/logs-api', () => ({
  fetchLogs: vi.fn(),
  fetchLogDetail: vi.fn(),
}));

vi.mock('@/features/admin/api/users-api', () => ({
  fetchUsers: vi.fn(),
}));

vi.mock('@/features/tracking/api/usage-tracking', () => ({
  trackUsageEvent: vi.fn().mockResolvedValue(undefined),
}));

function chooseFilterOption(label: string, optionName: string) {
  fireEvent.click(screen.getByLabelText(label));
  fireEvent.click(screen.getByRole('option', { name: optionName }));
}

const logListData: LogListData = {
  items: [
    {
      id: 'log_1',
      log_type: 'request',
      created_at: '2026-07-02T14:26:18+00:00',
      summary: 'GET /api/v1/admin/logs · 200',
      actor_name: '系统管理员',
      actor_username: 'admin',
      actor_role: 'admin',
      client_type: 'web_admin',
      result: '成功',
      status_code: 200,
      duration_ms: 84,
      request_id: 'req_1234567890abcdef',
      client_request_id: 'web:client-request-abcdef1234567890',
      task_trace_id: 'task_upload_video_abcdef1234567890',
      task_type: 'upload_video',
      task_status: 'success',
      task_duration_ms: 2345,
      task_slowest_span_name: 'storage_put_object',
      method: 'GET',
      path: '/api/v1/admin/logs',
    },
  ],
  total: 1,
  page: 1,
  page_size: 20,
  summary: {
    today_logs: 1286,
    api_errors: 18,
    slow_requests: 27,
    sensitive_ops: 42,
  },
};

const detailData: LogDetailData = {
  log: logListData.items[0],
  basic: {
    title: '基础信息',
    fields: {
      '日志 ID': 'log_1',
      request_id: 'req_1234567890abcdef',
    },
  },
  request: {
    title: '请求信息',
    fields: {
      Method: 'GET',
      Path: '/api/v1/admin/logs',
      'Status Code': 200,
      Duration: '84 ms',
    },
  },
  actor: {
    title: '操作者与客户端',
    fields: {
      操作者: 'admin',
      客户端: 'web_admin',
    },
  },
  context: {
    title: '操作上下文',
    fields: {
      操作摘要: 'GET /api/v1/admin/logs · 200',
    },
  },
  event: {
    title: '埋点属性',
    fields: {
      event_name: '-',
      module: '-',
    },
  },
  request_snapshot: {
    request: {
      method: 'GET',
      path: '/api/v1/admin/logs',
      route_template: '/api/v1/admin/logs',
      route_match_status: 'matched',
      request_id: 'req_1234567890abcdef',
      client_request_id: 'web:client-request-abcdef1234567890',
      trusted_request_id_header: 'x-request-id',
      client_request_id_header: 'x-client-request-id',
    },
    input: {
      query: {
        allowed: { page: '1' },
        ignored_keys: ['debug'],
        redacted_keys: ['token'],
        policy: 'allowlist',
      },
      body_schema_summary: {
        body_type: 'none',
        content_type: null,
        content_length: null,
        stored_raw_body: false,
        fields: [],
      },
      redaction_summary: {
        policy: 'backend_allowlist_and_sensitive_blacklist',
        stored_raw_body: false,
      },
    },
    resource: {
      resource_type: null,
      resource_id: null,
      id_source: 'unidentified',
    },
    response: {
      status_code: 200,
      error_code: null,
      duration_ms: 84,
      result: 'success',
      error_summary: null,
    },
    actor: {
      actor_user_id: 'user_admin',
      actor_username: 'admin',
      actor_role: 'admin',
      client_type: 'web_admin',
      ip_summary: '127.0.*.*',
      user_agent_summary: 'vitest',
    },
    timing: {
      environment: 'test',
      started_at: '2026-07-02T14:26:18+00:00',
      finished_at: '2026-07-02T14:26:18+00:00',
    },
    raw_json: '{\n  "request": {\n    "route_template": "/api/v1/admin/logs"\n  }\n}',
    parse_error: null,
  },
  task_trace: {
    task_trace_id: 'task_upload_video_abcdef1234567890',
    task_type: 'upload_video',
    status: 'success',
    parent_request_id: 'req_1234567890abcdef',
    duration_ms: 2345,
    resource_type: 'media',
    resource_id: 'media_1',
    slowest_span_name: 'storage_put_object',
    error_code: null,
    summary: 'upload_video · success · 2345 ms · slowest=storage_put_object',
    spans: [
      {
        span_name: 'frontend_upload_body_done',
        status: 'success',
        started_at: '2026-07-02T14:26:18+00:00',
        ended_at: '2026-07-02T14:26:18+00:00',
        duration_ms: 0,
        request_id: 'req_1234567890abcdef',
        error_code: null,
        summary: '请求体已到达后端，前端 99% 阶段开始',
        is_slowest: false,
      },
      {
        span_name: 'storage_put_object',
        status: 'success',
        started_at: '2026-07-02T14:26:19+00:00',
        ended_at: '2026-07-02T14:26:21+00:00',
        duration_ms: 1800,
        request_id: 'req_1234567890abcdef',
        error_code: null,
        summary: '对象存储写入完成',
        is_slowest: true,
      },
    ],
  },
  related_task_traces: [
    {
      task_trace_id: 'task_upload_video_abcdef1234567890',
      task_type: 'upload_video',
      status: 'success',
      parent_request_id: 'req_1234567890abcdef',
      duration_ms: 2345,
      resource_type: 'media',
      resource_id: 'media_1',
      slowest_span_name: 'storage_put_object',
      error_code: null,
      summary: 'upload_video · success · 2345 ms · slowest=storage_put_object',
      spans: [
        {
          span_name: 'frontend_upload_body_done',
          status: 'success',
          started_at: '2026-07-02T14:26:18+00:00',
          ended_at: '2026-07-02T14:26:18+00:00',
          duration_ms: 0,
          request_id: 'req_1234567890abcdef',
          error_code: null,
          summary: '请求体已到达后端，前端 99% 阶段开始',
          is_slowest: false,
        },
        {
          span_name: 'storage_put_object',
          status: 'success',
          started_at: '2026-07-02T14:26:19+00:00',
          ended_at: '2026-07-02T14:26:21+00:00',
          duration_ms: 1800,
          request_id: 'req_1234567890abcdef',
          error_code: null,
          summary: '对象存储写入完成',
          is_slowest: true,
        },
      ],
    },
  ],
  metadata_json: '{\n  "path": "/api/v1/admin/logs"\n}',
};

const userListData: UserAdminListData = {
  items: [
    {
      id: 'user_admin',
      username: 'admin',
      display_name: '系统管理员',
      role: 'admin',
      status: 'active',
      created_at: '2026-07-01T00:00:00+00:00',
    },
    {
      id: 'user_operator',
      username: 'operator01',
      display_name: '运营一号',
      role: 'employee',
      status: 'disabled',
      created_at: '2026-07-01T00:00:00+00:00',
    },
  ],
  page: 1,
  page_size: 20,
  total: 2,
  summary: {
    total: 2,
    filtered: 2,
    active_count: 1,
    disabled_count: 1,
  },
};

function setClipboard(value: unknown) {
  Object.defineProperty(navigator, 'clipboard', {
    configurable: true,
    value,
  });
}

describe('LogAuditPage', () => {
  beforeEach(() => {
    vi.useRealTimers();
    vi.mocked(fetchLogs).mockReset();
    vi.mocked(fetchLogDetail).mockReset();
    vi.mocked(fetchUsers).mockReset();
    vi.mocked(trackUsageEvent).mockClear();
    vi.mocked(fetchLogs).mockResolvedValue(logListData);
    vi.mocked(fetchLogDetail).mockResolvedValue(detailData);
    vi.mocked(fetchUsers).mockResolvedValue(userListData);
    setClipboard({
      writeText: vi.fn().mockResolvedValue(undefined),
    });
  });

  it('renders metrics, table and pagination structure', async () => {
    const { container } = render(<LogAuditPage />);

    expect(await screen.findByText('日志审计')).toBeInTheDocument();
    expect(screen.getByText('TODAY LOGS')).toBeInTheDocument();
    expect(screen.getByText('1,286')).toBeInTheDocument();
    expect(screen.queryByText('链路观测')).not.toBeInTheDocument();
    expect(screen.getByText('GET /api/v1/admin/logs · 200')).toBeInTheDocument();

    const summary = screen.getByLabelText('日志摘要');
    const cards = Array.from(summary.querySelectorAll('.metric-card'));
    expect(summary).toHaveClass('summary-grid');
    expect(cards).toHaveLength(4);
    cards.forEach((card) => {
      expect(card.tagName.toLowerCase()).toBe('article');
      expect(card.querySelector('.metric-label')).toBeInTheDocument();
      expect(card.querySelector('.metric-value')).toBeInTheDocument();
      expect(card.querySelector('.metric-desc')).toBeInTheDocument();
    });
    expect(screen.getByText('异常请求')).toHaveClass('metric-desc', 'danger');

    const pagination = container.querySelector('.pagination');
    expect(pagination?.querySelector('.page-summary')).toHaveTextContent('共 1 条日志');
    expect(pagination?.querySelector('.page-right')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-buttons')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-size-wrap')).toBeInTheDocument();
    expect(container.querySelector('th.log-audit-action-cell')).toHaveTextContent('操作');
    expect(container.querySelector('th.log-audit-action-cell')).toHaveClass(
      'admin-sticky-action-cell',
    );
    expect(container.querySelector('td.log-audit-action-cell')).toBeInTheDocument();
    expect(container.querySelector('td.log-audit-action-cell')).toHaveClass(
      'admin-sticky-action-cell',
    );
    expect(screen.queryByRole('button', { name: '查询' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: '重置' }).closest('.log-audit-filter-actions')).toBeInTheDocument();
    expect(screen.getByLabelText('时间范围')).toHaveClass('select');
    expect(screen.getByLabelText('时间范围')).toHaveTextContent('最近1天');
    fireEvent.click(screen.getByLabelText('时间范围'));
    [
      '最近5分钟',
      '最近10分钟',
      '最近30分钟',
      '最近1小时',
      '最近3小时',
      '最近6小时',
      '最近12小时',
      '最近1天',
      '最近2天',
      '最近3天',
      '最近7天',
    ].forEach((label) => {
      expect(screen.getByRole('option', { name: label })).toBeInTheDocument();
    });
    expect(screen.queryByRole('option', { name: '全部时间' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByLabelText('状态 / 结果'));
    expect(screen.getByLabelText('状态 / 结果')).toHaveClass('select');
    expect(screen.getByLabelText('路径 / Request ID')).toHaveAttribute('placeholder', '接口路径或 request_id');
    expect(screen.getByLabelText('Task Trace ID')).toHaveAttribute('placeholder', 'task_upload_video_xxx');
    expect(screen.getByRole('option', { name: '422 参数校验错误' })).toBeInTheDocument();
    expect(screen.getByLabelText('操作者')).toHaveAttribute('role', 'combobox');
    expect(screen.getByLabelText('操作者')).toHaveAttribute('placeholder', '搜索用户名称或账号');
    const filterLabels = Array.from(container.querySelectorAll('.log-audit-filter-grid .field-label')).map((label) => label.textContent);
    expect(filterLabels).toEqual([
      '日志类型',
      '时间范围',
      '状态 / 结果',
      '操作者',
      'Task Trace ID',
      '路径 / Request ID',
    ]);
    expect(screen.queryByPlaceholderText('User ID')).not.toBeInTheDocument();
    expect(screen.queryByLabelText('路径 / request_id / task_trace_id')).not.toBeInTheDocument();
    expect(screen.queryByLabelText('资源 / ID')).not.toBeInTheDocument();
    expect(screen.queryByRole('columnheader', { name: '复制' })).not.toBeInTheDocument();
    const columnHeaders = screen.getAllByRole('columnheader').map((header) => header.textContent);
    expect(columnHeaders).toEqual([
      '时间',
      '类型',
      '事件 / 摘要',
      '操作者',
      '客户端',
      '状态',
      '耗时',
      'request_id',
      'client_request_id',
      'task_trace_id',
      '操作',
    ]);
    expect(screen.queryByRole('columnheader', { name: 'Task Trace' })).not.toBeInTheDocument();
    expect(container.querySelector('.request-id-cell')?.querySelector('.request-copy-action')).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: 'client_request_id' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: 'task_trace_id' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '复制 client_request_id' })).toBeInTheDocument();
    expect(screen.getByText(/web:client/)).toBeInTheDocument();
    const taskTraceCell = container.querySelector('.task-trace-cell');
    const tableRow = taskTraceCell?.closest('tr');
    expect(taskTraceCell?.querySelector('.task-trace-id')).toHaveTextContent(/task_upload/);
    expect(taskTraceCell?.querySelector('.request-copy-action')).toHaveAccessibleName('复制 task_trace_id');
    expect(taskTraceCell?.querySelector('small')).not.toBeInTheDocument();
    expect(screen.getByText(/task_upload/)).toBeInTheDocument();
    expect(within(tableRow as HTMLTableRowElement).queryByText(/storage_put_object/)).not.toBeInTheDocument();
    expect(container.querySelector('.actor-account')).toHaveTextContent('admin');
    expect(container.querySelector('.actor-account')).toHaveAttribute('title', 'admin');
    expect(screen.queryByText('系统管理员')).not.toBeInTheDocument();
    expect(container.querySelector('.log-type')).toHaveClass('type-request');
    expect(container.querySelector('.log-status')).toHaveClass('status-success');
  });

  it('submits filters through backend query params', async () => {
    const beforeChange = Date.now();
    render(<LogAuditPage />);
    await screen.findByText('GET /api/v1/admin/logs · 200');

    chooseFilterOption('时间范围', '最近5分钟');
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({
          start_time: expect.any(String),
          page: 1,
        }),
      );
    });
    const timeRangeQuery = vi.mocked(fetchLogs).mock.calls.at(-1)?.[0];
    expect(new Date(timeRangeQuery?.start_time ?? '').getTime()).toBeGreaterThanOrEqual(beforeChange - 5 * 60 * 1000 - 1000);
    expect(new Date(timeRangeQuery?.start_time ?? '').getTime()).toBeLessThanOrEqual(Date.now() - 5 * 60 * 1000 + 1000);

    fireEvent.change(screen.getByLabelText('路径 / Request ID'), {
      target: { value: 'req_1234567890abcdef' },
    });
    expect(trackUsageEvent).toHaveBeenCalledWith('filter_change', {
      module: 'log_audit',
      entity_type: 'log_query',
      entity_id: 'pathOrRequestId',
      filter_name: 'pathOrRequestId',
      filter_value: 'req_1234567890abcdef',
    });
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({
          path_or_request_id: 'req_1234567890abcdef',
          page: 1,
        }),
      );
    });

    fireEvent.change(screen.getByLabelText('Task Trace ID'), {
      target: { value: 'task_upload_video_abcdef1234567890' },
    });
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({
          task_trace_id: 'task_upload_video_abcdef1234567890',
          page: 1,
        }),
      );
    });

    chooseFilterOption('状态 / 结果', '失败');
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({
          result: 'failed',
          status_code: undefined,
          page: 1,
        }),
      );
    });

    chooseFilterOption('状态 / 结果', '500 服务异常');
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({
          result: undefined,
          status_code: 500,
          page: 1,
        }),
      );
    });

    chooseFilterOption('状态 / 结果', '422 参数校验错误');
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({
          result: undefined,
          status_code: 422,
          page: 1,
        }),
      );
    });

    fireEvent.focus(screen.getByLabelText('操作者'));
    const adminOption = await screen.findByRole('option', { name: /admin/ });
    expect(within(adminOption).getByText('admin')).toBeInTheDocument();
    expect(within(adminOption).getByText('系统管理员')).toBeInTheDocument();
    expect(screen.queryByText('admin / admin / active')).not.toBeInTheDocument();
    fireEvent.click(await screen.findByRole('option', { name: /系统管理员/ }));
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({
          actor_user_id: 'user_admin',
          page: 1,
        }),
      );
    });
    expect(screen.getByLabelText('操作者')).toHaveValue('系统管理员');

    fireEvent.click(screen.getByRole('button', { name: '清空操作者筛选' }));
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({
          actor_user_id: undefined,
          page: 1,
        }),
      );
    });
  });

  it('searches operator candidates and resets actor_user_id with all filters', async () => {
    render(<LogAuditPage />);
    await screen.findByText('GET /api/v1/admin/logs · 200');

    fireEvent.focus(screen.getByLabelText('操作者'));
    fireEvent.change(screen.getByLabelText('操作者'), { target: { value: 'operator' } });

    await waitFor(() => {
      expect(fetchUsers).toHaveBeenCalledWith(
        expect.objectContaining({
          page: 1,
          page_size: 20,
          keyword: 'operator',
        }),
      );
    });

    fireEvent.click(await screen.findByRole('option', { name: /运营一号/ }));
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({ actor_user_id: 'user_operator' }),
      );
    });

    fireEvent.click(screen.getByRole('button', { name: '重置' }));
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({
          actor_user_id: undefined,
          log_type: undefined,
          result: undefined,
          status_code: undefined,
          task_trace_id: undefined,
          page: 1,
        }),
      );
    });
    expect(screen.getByLabelText('操作者')).toHaveValue('');
  });

  it('shows operator candidate empty, failed and duplicate-name account states', async () => {
    vi.mocked(fetchUsers)
      .mockResolvedValueOnce({
        ...userListData,
        items: [
          { ...userListData.items[0], id: 'same_1', username: 'same_a', display_name: '同名用户' },
          { ...userListData.items[1], id: 'same_2', username: 'same_b', display_name: '同名用户' },
        ],
        total: 2,
      })
      .mockResolvedValueOnce({ ...userListData, items: [], total: 0 })
      .mockRejectedValueOnce(new Error('candidate failed'));

    render(<LogAuditPage />);
    await screen.findByText('GET /api/v1/admin/logs · 200');

    fireEvent.focus(screen.getByLabelText('操作者'));
    expect(await screen.findAllByRole('option', { name: /同名用户/ })).toHaveLength(2);
    expect(screen.getByText('same_a')).toBeInTheDocument();
    expect(screen.getByText('same_b')).toBeInTheDocument();
    expect(screen.queryByText('same_a / admin / active')).not.toBeInTheDocument();
    expect(screen.queryByText('same_b / employee / disabled')).not.toBeInTheDocument();

    fireEvent.change(screen.getByLabelText('操作者'), { target: { value: 'missing' } });
    await screen.findByText('无匹配操作者');

    fireEvent.change(screen.getByLabelText('操作者'), { target: { value: 'fail' } });
    expect(await screen.findAllByText('加载操作者候选失败')).toHaveLength(2);
    expect(await screen.findByRole('status')).toHaveTextContent('加载操作者候选失败');
    expect(screen.getByText('GET /api/v1/admin/logs · 200')).toBeInTheDocument();
  });

  it('keeps admin-list feedback stable and avoids native dialogs', async () => {
    const confirmSpy = vi.spyOn(window, 'confirm');
    const alertSpy = vi.spyOn(window, 'alert');
    const { container } = render(<LogAuditPage />);
    await screen.findByText('GET /api/v1/admin/logs · 200');

    fireEvent.click(screen.getByRole('button', { name: '复制 request_id' }));

    expect(await screen.findByRole('status')).toHaveClass('admin-toast');
    expect(document.querySelector('.admin-toast-region')).toBeInTheDocument();
    expect(container.querySelector('.pagination .page-summary')).toBeInTheDocument();
    expect(container.querySelector('.pagination .page-right')).toBeInTheDocument();
    expect(screen.getByLabelText('日志摘要').querySelectorAll('.metric-label')).toHaveLength(4);
    expect(screen.queryByLabelText('链路观测摘要')).not.toBeInTheDocument();
    expect(confirmSpy).not.toHaveBeenCalled();
    expect(alertSpy).not.toHaveBeenCalled();
  });

  it('copies request id with fixed toast feedback', async () => {
    render(<LogAuditPage />);
    await screen.findByText('GET /api/v1/admin/logs · 200');

    fireEvent.click(screen.getByRole('button', { name: '复制 request_id' }));

    await waitFor(() => {
      expect(navigator.clipboard?.writeText).toHaveBeenCalledWith('req_1234567890abcdef');
    });
    expect(trackUsageEvent).toHaveBeenCalledWith('copy_request_id', {
      module: 'log_audit',
      entity_type: 'request_log',
      entity_id: 'req_1234567890abcdef',
      request_id: 'req_1234567890abcdef',
    });
    expect(await screen.findByRole('status')).toHaveTextContent('request_id 已复制');
  });

  it('copies task_trace_id with fixed toast feedback', async () => {
    render(<LogAuditPage />);
    await screen.findByText('GET /api/v1/admin/logs · 200');

    fireEvent.click(screen.getByRole('button', { name: '复制 task_trace_id' }));

    await waitFor(() => {
      expect(navigator.clipboard?.writeText).toHaveBeenCalledWith('task_upload_video_abcdef1234567890');
    });
    expect(trackUsageEvent).toHaveBeenCalledWith('copy_request_id', expect.objectContaining({
      entity_type: 'task_trace',
      task_trace_id: 'task_upload_video_abcdef1234567890',
    }));
    expect(await screen.findByRole('status')).toHaveTextContent('task_trace_id 已复制');
  });

  it('copies parent_request_id with fixed toast feedback', async () => {
    vi.mocked(fetchLogDetail).mockResolvedValueOnce(detailData);
    render(<LogAuditPage />);
    const row = (await screen.findByText('GET /api/v1/admin/logs · 200')).closest('tr');
    expect(row).not.toBeNull();

    fireEvent.click(within(row as HTMLTableRowElement).getByRole('button', { name: '查看' }));
    const drawer = await screen.findByLabelText('日志详情');
    const parentRow = within(drawer).getByText('parent_request_id').closest('div');
    expect(parentRow).not.toBeNull();
    fireEvent.click(within(parentRow as HTMLDivElement).getByRole('button'));

    await waitFor(() => {
      expect(trackUsageEvent).toHaveBeenCalledWith('copy_request_id', expect.objectContaining({
        entity_type: 'parent_request',
        request_id: 'req_1234567890abcdef',
      }));
    });
    expect(await screen.findByRole('status')).toHaveTextContent('parent_request_id 已复制');
  });

  it('copies client_request_id with fixed toast feedback', async () => {
    render(<LogAuditPage />);
    await screen.findByText('GET /api/v1/admin/logs · 200');

    fireEvent.click(screen.getByRole('button', { name: '复制 client_request_id' }));

    await waitFor(() => {
      expect(navigator.clipboard?.writeText).toHaveBeenCalledWith('web:client-request-abcdef1234567890');
    });
    expect(trackUsageEvent).toHaveBeenCalledWith('copy_request_id', expect.objectContaining({
      entity_type: 'client_request',
      client_request_id: 'web:client-request-abcdef1234567890',
    }));
    expect(await screen.findByRole('status')).toHaveTextContent('client_request_id 已复制');
  });

  it('shows manual copy guidance when Clipboard API is unavailable', async () => {
    setClipboard(undefined);
    render(<LogAuditPage />);
    await screen.findByText('GET /api/v1/admin/logs · 200');

    fireEvent.click(screen.getByRole('button', { name: '复制 request_id' }));

    expect(await screen.findByRole('status')).toHaveTextContent('无法自动复制 request_id，请打开日志详情选中文本手动复制');
    expect(trackUsageEvent).not.toHaveBeenCalled();
  });

  it('shows manual copy guidance when Clipboard API rejects writes', async () => {
    setClipboard({
      writeText: vi.fn().mockRejectedValue(new Error('clipboard denied')),
    });
    render(<LogAuditPage />);
    await screen.findByText('GET /api/v1/admin/logs · 200');

    fireEvent.click(screen.getByRole('button', { name: '复制 request_id' }));

    await waitFor(() => {
      expect(navigator.clipboard?.writeText).toHaveBeenCalledWith('req_1234567890abcdef');
    });
    expect(await screen.findByRole('status')).toHaveTextContent('自动复制失败，请打开日志详情选中文本手动复制');
    expect(trackUsageEvent).not.toHaveBeenCalled();
  });

  it('does not render copy action for empty request id rows', async () => {
    vi.mocked(fetchLogs).mockResolvedValueOnce({
      ...logListData,
      items: [{ ...logListData.items[0], request_id: '' }],
    });

    render(<LogAuditPage />);
    await screen.findByText('GET /api/v1/admin/logs · 200');

    expect(screen.queryByRole('button', { name: '复制 request_id' })).not.toBeInTheDocument();
    expect(navigator.clipboard?.writeText).not.toHaveBeenCalled();
  });

  it('opens and closes detail drawer', async () => {
    render(<LogAuditPage />);
    const row = (await screen.findByText('GET /api/v1/admin/logs · 200')).closest('tr');
    expect(row).not.toBeNull();

    fireEvent.click(
      within(row as HTMLTableRowElement).getByRole('button', {
        name: '查看日志详情：GET /api/v1/admin/logs · 200',
      }),
    );

    const drawer = await screen.findByLabelText('日志详情');
    expect(drawer).toBeInTheDocument();
    expect(within(drawer).getByText('Request Snapshot')).toBeInTheDocument();
    expect(within(drawer).getByText('Route Template')).toBeInTheDocument();
    expect(within(drawer).getByText('Trusted Request ID')).toBeInTheDocument();
    expect(within(drawer).getByText('Client Request ID')).toBeInTheDocument();
    expect(within(drawer).getByText('Trusted Response Header')).toBeInTheDocument();
    expect(within(drawer).getAllByLabelText('字段说明：Method')[0]).toHaveAttribute(
      'data-tooltip',
      expect.stringContaining('HTTP 请求方法'),
    );
    expect(within(drawer).getByLabelText('字段说明：Route Template')).toHaveAttribute(
      'data-tooltip',
      expect.stringContaining('路由模板'),
    );
    expect(within(drawer).getAllByLabelText('字段说明：task_trace_id').length).toBeGreaterThan(0);
    expect(within(drawer).getByLabelText('字段说明：parent_request_id')).toHaveAttribute(
      'data-tooltip',
      expect.stringContaining('触发该 Task Trace 的主请求 ID'),
    );
    fireEvent.mouseEnter(within(drawer).getByLabelText('字段说明：parent_request_id'));
    expect(screen.getByRole('tooltip')).toHaveTextContent('触发该 Task Trace 的主请求 ID');
    fireEvent.mouseLeave(within(drawer).getByLabelText('字段说明：parent_request_id'));
    expect(within(drawer).getByText('x-request-id')).toBeInTheDocument();
    expect(within(drawer).getByText('x-client-request-id')).toBeInTheDocument();
    expect(within(drawer).getAllByText('web:client-request-abcdef1234567890').length).toBeGreaterThan(0);
    expect(within(drawer).getAllByText('/api/v1/admin/logs').length).toBeGreaterThan(0);
    expect(within(drawer).getByText('Query Allowlist')).toBeInTheDocument();
    expect(within(drawer).getByText(/"page": "1"/)).toBeInTheDocument();
    expect(within(drawer).getByText('Snapshot JSON')).toBeInTheDocument();
    expect(within(drawer).getByText('Task Trace')).toBeInTheDocument();
    expect(within(drawer).getByText('parent_request_id')).toBeInTheDocument();
    expect(within(drawer).getByText('frontend_upload_body_done')).toBeInTheDocument();
    expect(within(drawer).getByText('storage_put_object')).toBeInTheDocument();
    expect(within(drawer).getByText('耗时最高节点')).toBeInTheDocument();
    expect(screen.getByText('METADATA JSON')).toBeInTheDocument();
    expect(fetchLogDetail).toHaveBeenCalledWith('log_1');
    expect(trackUsageEvent).toHaveBeenCalledWith('detail_view', {
      module: 'log_audit',
      entity_type: 'log',
      entity_id: 'log_1',
      request_id: 'req_1234567890abcdef',
      log_type: 'request',
    }, {
      durationMs: expect.any(Number),
    });

    fireEvent.click(screen.getByRole('button', { name: '关闭' }));
    await waitFor(() => expect(screen.queryByLabelText('日志详情')).not.toBeInTheDocument());
  });

  it('shows request snapshot empty state when detail has no snapshot', async () => {
    vi.mocked(fetchLogDetail).mockResolvedValueOnce({
      ...detailData,
      request_snapshot: null,
    });

    render(<LogAuditPage />);
    const row = (await screen.findByText('GET /api/v1/admin/logs · 200')).closest('tr');
    expect(row).not.toBeNull();

    fireEvent.click(within(row as HTMLTableRowElement).getByRole('button', { name: '查看' }));

    const drawer = await screen.findByLabelText('日志详情');
    expect(within(drawer).getByText('未采集 Request Snapshot')).toBeInTheDocument();
    expect(within(drawer).getByText('METADATA JSON')).toBeInTheDocument();
  });

  it('opens detail drawer from the sticky action column', async () => {
    render(<LogAuditPage />);
    const row = (await screen.findByText('GET /api/v1/admin/logs · 200')).closest('tr');
    expect(row).not.toBeNull();

    fireEvent.click(within(row as HTMLTableRowElement).getByRole('button', { name: '查看' }));

    expect(await screen.findByLabelText('日志详情')).toBeInTheDocument();
    expect(fetchLogDetail).toHaveBeenCalledWith('log_1');
  });
});
