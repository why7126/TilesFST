import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { fetchLogDetail, fetchLogs } from '@/features/admin/api/logs-api';
import { trackUsageEvent } from '@/features/tracking/api/usage-tracking';
import type { LogDetailData, LogListData } from '@/shared/api/generated';
import { LogAuditPage } from './LogAuditPage';

vi.mock('@/features/admin/api/logs-api', () => ({
  fetchLogs: vi.fn(),
  fetchLogDetail: vi.fn(),
}));

vi.mock('@/features/tracking/api/usage-tracking', () => ({
  trackUsageEvent: vi.fn().mockResolvedValue(undefined),
}));

const logListData: LogListData = {
  items: [
    {
      id: 'log_1',
      log_type: 'request',
      created_at: '2026-07-02T14:26:18+00:00',
      summary: 'GET /api/v1/admin/logs · 200',
      actor_name: '系统管理员',
      actor_role: 'admin',
      client_type: 'web_admin',
      result: '成功',
      status_code: 200,
      duration_ms: 84,
      request_id: 'req_1234567890abcdef',
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
      操作者: '系统管理员',
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
  metadata_json: '{\n  "path": "/api/v1/admin/logs"\n}',
};

function setClipboard(value: unknown) {
  Object.defineProperty(navigator, 'clipboard', {
    configurable: true,
    value,
  });
}

describe('LogAuditPage', () => {
  beforeEach(() => {
    vi.mocked(fetchLogs).mockReset();
    vi.mocked(fetchLogDetail).mockReset();
    vi.mocked(trackUsageEvent).mockClear();
    vi.mocked(fetchLogs).mockResolvedValue(logListData);
    vi.mocked(fetchLogDetail).mockResolvedValue(detailData);
    setClipboard({
      writeText: vi.fn().mockResolvedValue(undefined),
    });
  });

  it('renders metrics, table and pagination structure', async () => {
    const { container } = render(<LogAuditPage />);

    expect(await screen.findByText('日志审计')).toBeInTheDocument();
    expect(screen.getByText('TODAY LOGS')).toBeInTheDocument();
    expect(screen.getByText('1,286')).toBeInTheDocument();
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
    expect(screen.getByLabelText('状态 / 结果').tagName).toBe('SELECT');
    expect(screen.getByRole('option', { name: '422 参数校验错误' })).toBeInTheDocument();
    expect(screen.queryByLabelText('资源 / ID')).not.toBeInTheDocument();
    expect(screen.queryByRole('columnheader', { name: '复制' })).not.toBeInTheDocument();
    expect(container.querySelector('.request-id-cell')?.querySelector('.request-copy-action')).toBeInTheDocument();
    expect(container.querySelector('.log-type')).toHaveClass('type-request');
    expect(container.querySelector('.log-status')).toHaveClass('status-success');
  });

  it('submits filters through backend query params', async () => {
    render(<LogAuditPage />);
    await screen.findByText('GET /api/v1/admin/logs · 200');

    fireEvent.change(screen.getByLabelText('路径 / request_id'), {
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

    fireEvent.change(screen.getByLabelText('状态 / 结果'), {
      target: { value: 'result:failed' },
    });
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({
          result: 'failed',
          status_code: undefined,
          page: 1,
        }),
      );
    });

    fireEvent.change(screen.getByLabelText('状态 / 结果'), {
      target: { value: 'status:500' },
    });
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({
          result: undefined,
          status_code: 500,
          page: 1,
        }),
      );
    });

    fireEvent.change(screen.getByLabelText('状态 / 结果'), {
      target: { value: 'status:422' },
    });
    await waitFor(() => {
      expect(fetchLogs).toHaveBeenLastCalledWith(
        expect.objectContaining({
          result: undefined,
          status_code: 422,
          page: 1,
        }),
      );
    });
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

    expect(await screen.findByLabelText('日志详情')).toBeInTheDocument();
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

  it('opens detail drawer from the sticky action column', async () => {
    render(<LogAuditPage />);
    const row = (await screen.findByText('GET /api/v1/admin/logs · 200')).closest('tr');
    expect(row).not.toBeNull();

    fireEvent.click(within(row as HTMLTableRowElement).getByRole('button', { name: '查看' }));

    expect(await screen.findByLabelText('日志详情')).toBeInTheDocument();
    expect(fetchLogDetail).toHaveBeenCalledWith('log_1');
  });
});
