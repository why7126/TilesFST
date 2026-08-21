import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { PerformanceRumPage } from './PerformanceRumPage';

const mocks = vi.hoisted(() => ({
  fetchPerformanceFilterOptions: vi.fn(),
  fetchPerformanceSamples: vi.fn(),
  fetchPerformanceSummary: vi.fn(),
  navigate: vi.fn(),
}));

vi.mock('@/features/performance/performance-api', () => ({
  fetchPerformanceFilterOptions: mocks.fetchPerformanceFilterOptions,
  fetchPerformanceSamples: mocks.fetchPerformanceSamples,
  fetchPerformanceSummary: mocks.fetchPerformanceSummary,
}));

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_error: unknown, fallback: string) => fallback,
}));

vi.mock('react-router-dom', () => ({
  useNavigate: () => mocks.navigate,
}));

describe('PerformanceRumPage', () => {
  beforeEach(() => {
    mocks.fetchPerformanceFilterOptions.mockReset();
    mocks.fetchPerformanceSamples.mockReset();
    mocks.fetchPerformanceSummary.mockReset();
    mocks.navigate.mockReset();
    mocks.fetchPerformanceFilterOptions.mockResolvedValue({
      client_types: [
        { value: 'web_admin', label: '管理端 Web' },
        { value: 'web_catalog', label: '店主 Web' },
        { value: 'wechat_miniapp', label: '微信小程序' },
      ],
      app_versions: [{ value: '0.1.0', label: '0.1.0', count: 21 }],
      page_keys: [{ value: 'admin/performance', label: 'admin/performance', count: 21 }],
      device_classes: [{ value: 'desktop', label: 'desktop', count: 21 }],
      network_types: [{ value: 'wifi', label: 'wifi', count: 21 }],
      metrics: [
        { value: 'full_load', label: '完整加载' },
        { value: 'app_launch_ready', label: '小程序启动就绪' },
        { value: 'api_duration', label: '接口请求耗时' },
        { value: 'api_failed_duration', label: '接口失败耗时' },
      ],
    });
    mocks.fetchPerformanceSamples.mockResolvedValue({
      items: [],
      total: 0,
      filters: {},
    });
    mocks.fetchPerformanceSummary.mockResolvedValue({
      items: [],
      slow_pages: [],
      total: 0,
      page: 1,
      page_size: 20,
      total_pages: 1,
      total_events: 0,
      filters: {},
      thresholds: {},
    });
  });

  it('uses admin page title and action conventions', async () => {
    const { container } = render(<PerformanceRumPage />);

    expect(await screen.findByRole('heading', { name: '性能观测' })).toHaveClass('page-title');
    expect(screen.queryByRole('heading', { name: '真实用户性能观测' })).not.toBeInTheDocument();
    const resetButton = screen.getByRole('button', { name: '重置' });
    expect(resetButton.closest('.log-audit-filter-actions')).toBeInTheDocument();
    expect(resetButton.querySelector('svg')).not.toBeInTheDocument();
    expect(screen.getByText('时间范围')).toHaveClass('field-label');
    expect(screen.getByText('端类型')).toHaveClass('field-label');
    expect(screen.getByText('版本号')).toHaveClass('field-label');
    expect(screen.getByText('页面')).toHaveClass('field-label');
    expect(screen.getByText('网络')).toHaveClass('field-label');
    expect(screen.getByText('指标')).toHaveClass('field-label');
    expect(screen.queryByRole('button', { name: '选择设备' })).not.toBeInTheDocument();
    expect(screen.getByText(/浏览器不支持网络类型采集时显示为未知/)).toBeInTheDocument();
    expect(container.querySelector('.filter-hint')).not.toBeInTheDocument();
    expect(screen.queryByText('数据边界')).not.toBeInTheDocument();
    expect(screen.queryByText('页面如何解读')).not.toBeInTheDocument();
    expect(mocks.fetchPerformanceFilterOptions).toHaveBeenCalledWith(expect.objectContaining({
      start_time: expect.any(String),
    }));
  });

  it('navigates to the sample page from performance page aggregates', async () => {
    mocks.fetchPerformanceSummary.mockResolvedValue({
      items: [
        {
          client_type: 'web_admin',
          page_key: 'admin/performance',
          metric_name: 'full_load',
          app_version: '0.1.0',
          network_type: 'wifi',
          device_class: 'desktop',
          sample_count: 21,
          average_ms: 1800,
          max_ms: 3600,
          p50_ms: 1200,
          p75_ms: 1800,
          p95_ms: 3200,
          p99_ms: 3600,
          sample_status: 'ok',
        },
      ],
      slow_pages: [
        {
          client_type: 'web_admin',
          page_key: 'admin/performance',
          metric_name: 'full_load',
          app_version: '0.1.0',
          network_type: 'wifi',
          device_class: 'desktop',
          sample_count: 21,
          average_ms: 1800,
          max_ms: 3600,
          p50_ms: 1200,
          p75_ms: 1800,
          p95_ms: 3200,
          p99_ms: 3600,
          sample_status: 'ok',
        },
      ],
      total: 21,
      page: 1,
      page_size: 20,
      total_pages: 2,
      total_events: 21,
      filters: {},
      thresholds: {},
    });
    render(<PerformanceRumPage />);

    expect(await screen.findByRole('columnheader', { name: '页面' })).toBeInTheDocument();
    expect(screen.getAllByRole('columnheader').map((header) => header.textContent)).toEqual([
      '页面',
      '版本号',
      '端类型',
      '设备',
      '网络',
      '指标',
      '样本',
      'P50',
      'P75',
      'P95',
      'P99',
      '状态',
      '操作',
    ]);
    expect(screen.getByRole('columnheader', { name: '操作' })).toHaveClass('admin-sticky-action-cell');
    expect(screen.getByText('0.1.0')).toBeInTheDocument();
    expect(screen.getByText('wifi')).toBeInTheDocument();
    expect(screen.getByText('desktop')).toBeInTheDocument();
    expect(screen.getByText('共 21 条聚合')).toBeInTheDocument();
    const pageSizeSelect = screen.getByLabelText('每页显示条数');
    expect(pageSizeSelect).toHaveClass('page-size');
    expect(screen.getByRole('option', { name: '20 条' })).toBeInTheDocument();
    expect(pageSizeSelect.closest('.page-right')?.firstElementChild).toHaveClass('page-buttons');
    expect(mocks.fetchPerformanceSummary).toHaveBeenCalledWith(
      expect.objectContaining({
        page: 1,
        page_size: 20,
      }),
    );

    fireEvent.click(screen.getByRole('button', { name: '下一页' }));
    await waitFor(() => expect(mocks.fetchPerformanceSummary).toHaveBeenCalledWith(expect.objectContaining({ page: 2, page_size: 20 })));

    fireEvent.click(screen.getByRole('button', { name: '选择版本号' }));
    fireEvent.click(screen.getByRole('option', { name: '0.1.0' }));
    await waitFor(() => expect(mocks.fetchPerformanceSummary).toHaveBeenCalledWith(expect.objectContaining({
      app_version: '0.1.0',
      page: 1,
    })));

    fireEvent.click(screen.getByRole('button', { name: '查看样本' }));

    expect(mocks.fetchPerformanceSamples).not.toHaveBeenCalled();
    expect(screen.queryByRole('dialog', { name: '样本明细' })).not.toBeInTheDocument();
    expect(mocks.navigate).toHaveBeenCalledWith(expect.stringContaining('/admin/performance/samples?'));
    expect(mocks.navigate.mock.calls[0][0]).toContain('client_type=web_admin');
    expect(mocks.navigate.mock.calls[0][0]).toContain('page_key=admin%2Fperformance');
    expect(mocks.navigate.mock.calls[0][0]).toContain('metric_name=full_load');
    expect(mocks.navigate.mock.calls[0][0]).toContain('app_version=0.1.0');
    expect(mocks.navigate.mock.calls[0][0]).toContain('network_type=wifi');
    expect(mocks.navigate.mock.calls[0][0]).toContain('device_class=desktop');
  });

  it('renders miniapp metric labels and compact performance empty state', async () => {
    const { container } = render(<PerformanceRumPage />);

    expect(await screen.findByText('暂无性能样本')).toHaveClass('performance-table-empty');
    expect(container.querySelector('.performance-table-empty')).toHaveTextContent('暂无性能样本');

    fireEvent.click(screen.getByRole('button', { name: '选择指标' }));
    expect(screen.getByRole('option', { name: '小程序启动就绪' })).toBeInTheDocument();
    expect(screen.getByRole('option', { name: '接口请求耗时' })).toBeInTheDocument();
    expect(screen.getByRole('option', { name: '接口失败耗时' })).toBeInTheDocument();
  });

  it('shows filter option load failures without blocking the aggregate table', async () => {
    mocks.fetchPerformanceFilterOptions.mockRejectedValue(new Error('boom'));

    render(<PerformanceRumPage />);

    expect(await screen.findByText('性能筛选候选值加载失败')).toHaveClass('empty-state');
    expect(screen.getByText('暂无性能样本')).toHaveClass('performance-table-empty');
  });

  it('shows miniapp aggregate metric labels in the table', async () => {
    mocks.fetchPerformanceSummary.mockResolvedValue({
      items: [
        {
          client_type: 'wechat_miniapp',
          page_key: 'app/launch',
          metric_name: 'app_launch_ready',
          app_version: 'v1.1.0',
          network_type: 'wifi',
          device_class: 'miniapp',
          sample_count: 3,
          average_ms: 16,
          max_ms: 38,
          p50_ms: 2,
          p75_ms: 8,
          p95_ms: 38,
          p99_ms: 38,
          sample_status: 'insufficient',
        },
      ],
      slow_pages: [
        {
          client_type: 'wechat_miniapp',
          page_key: 'app/launch',
          metric_name: 'app_launch_ready',
          app_version: 'v1.1.0',
          network_type: 'wifi',
          device_class: 'miniapp',
          sample_count: 3,
          average_ms: 16,
          max_ms: 38,
          p50_ms: 2,
          p75_ms: 8,
          p95_ms: 38,
          p99_ms: 38,
          sample_status: 'insufficient',
        },
      ],
      total: 1,
      page: 1,
      page_size: 20,
      total_pages: 1,
      total_events: 3,
      filters: {},
      thresholds: {},
    });

    render(<PerformanceRumPage />);

    expect(await screen.findByText('微信小程序')).toBeInTheDocument();
    expect(screen.getByText('小程序启动就绪')).toBeInTheDocument();
    expect(screen.getByText('wifi')).toBeInTheDocument();
    expect(screen.getByText('miniapp')).toBeInTheDocument();
  });
});
