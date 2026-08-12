import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { PerformanceRumPage } from './PerformanceRumPage';

const mocks = vi.hoisted(() => ({
  fetchPerformanceSamples: vi.fn(),
  fetchPerformanceSummary: vi.fn(),
  navigate: vi.fn(),
}));

vi.mock('@/features/performance/performance-api', () => ({
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
    mocks.fetchPerformanceSamples.mockReset();
    mocks.fetchPerformanceSummary.mockReset();
    mocks.navigate.mockReset();
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
    expect(screen.getByText('指标')).toHaveClass('field-label');
    expect(screen.getByText(/浏览器不支持网络类型采集时显示为未知/)).toBeInTheDocument();
    expect(container.querySelector('.filter-hint')).not.toBeInTheDocument();
    expect(screen.queryByText('数据边界')).not.toBeInTheDocument();
    expect(screen.queryByText('页面如何解读')).not.toBeInTheDocument();
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
    expect(screen.getByRole('columnheader', { name: '版本号' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: '操作' })).toHaveClass('admin-sticky-action-cell');
    expect(screen.getByText('0.1.0')).toBeInTheDocument();
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

    fireEvent.click(screen.getByRole('button', { name: '查看样本' }));

    expect(mocks.fetchPerformanceSamples).not.toHaveBeenCalled();
    expect(screen.queryByRole('dialog', { name: '样本明细' })).not.toBeInTheDocument();
    expect(mocks.navigate).toHaveBeenCalledWith(expect.stringContaining('/admin/performance/samples?'));
    expect(mocks.navigate.mock.calls[0][0]).toContain('client_type=web_admin');
    expect(mocks.navigate.mock.calls[0][0]).toContain('page_key=admin%2Fperformance');
    expect(mocks.navigate.mock.calls[0][0]).toContain('metric_name=full_load');
    expect(mocks.navigate.mock.calls[0][0]).toContain('app_version=0.1.0');
  });
});
