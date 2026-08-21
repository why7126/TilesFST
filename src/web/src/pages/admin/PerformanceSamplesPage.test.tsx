import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { PerformanceSamplesPage } from './PerformanceSamplesPage';

const mocks = vi.hoisted(() => ({
  fetchPerformanceSamples: vi.fn(),
  trackUsageEvent: vi.fn(),
}));

vi.mock('@/features/performance/performance-api', () => ({
  fetchPerformanceSamples: mocks.fetchPerformanceSamples,
}));

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_error: unknown, fallback: string) => fallback,
}));

vi.mock('@/features/tracking/api/usage-tracking', () => ({
  trackUsageEvent: mocks.trackUsageEvent,
}));

describe('PerformanceSamplesPage', () => {
  beforeEach(() => {
    mocks.fetchPerformanceSamples.mockReset();
    mocks.trackUsageEvent.mockReset();
    mocks.fetchPerformanceSamples.mockResolvedValue({
      items: [
        {
          id: 'perf-1',
          client_type: 'web_admin',
          page_key: 'admin/performance',
          metric_name: 'full_load',
          duration_ms: 3200,
          app_version: '0.1.0',
          network_type: 'wifi',
          device_class: 'desktop',
          request_id: 'req-safe-1',
          occurred_at: '2026-08-11T00:00:00Z',
          server_received_at: '2026-08-11T00:00:01Z',
        },
      ],
      total: 21,
      page: 1,
      page_size: 20,
      total_pages: 2,
      filters: {},
    });
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value: {
        writeText: vi.fn().mockResolvedValue(undefined),
      },
    });
  });

  it('loads safe samples from URL query in an admin list page', async () => {
    render(
      <MemoryRouter initialEntries={['/admin/performance/samples?client_type=web_admin&page_key=admin%2Fperformance&metric_name=full_load&app_version=0.1.0&network_type=wifi&device_class=desktop&start_time=2026-08-11T00%3A00%3A00.000Z']}>
        <PerformanceSamplesPage />
      </MemoryRouter>,
    );

    expect(await screen.findByRole('heading', { name: '性能样本' })).toHaveClass('page-title');
    expect(screen.getAllByText('页面').some((item) => item.classList.contains('field-label'))).toBe(true);
    expect(screen.getAllByText('admin/performance').length).toBeGreaterThanOrEqual(2);
    expect(screen.getAllByText('版本号').some((item) => item.classList.contains('field-label'))).toBe(true);
    expect(screen.getAllByText('0.1.0').length).toBeGreaterThan(0);
    expect(screen.getByText('共 21 条样本')).toBeInTheDocument();
    expect(screen.getAllByRole('columnheader').map((header) => header.textContent)).toEqual([
      '页面',
      '版本号',
      '端类型',
      '设备',
      '网络',
      '指标',
      '耗时',
      '事件时间',
      '接收时间',
      'request_id',
    ]);
    expect(await screen.findByText('req-safe-1')).toBeInTheDocument();
    expect(screen.getByText('3200ms')).toHaveClass('danger');
    expect(screen.queryByRole('dialog', { name: '样本明细' })).not.toBeInTheDocument();
    expect(screen.queryByText(/Header|Cookie|签名 URL/)).not.toBeInTheDocument();
    expect(screen.queryByText(/仅展示 page_key/)).not.toBeInTheDocument();
    expect(screen.getByLabelText('每页显示条数')).toHaveClass('page-size');

    await waitFor(() => expect(mocks.fetchPerformanceSamples).toHaveBeenCalledWith(expect.objectContaining({
      client_type: 'web_admin',
      page_key: 'admin/performance',
      metric_name: 'full_load',
      app_version: '0.1.0',
      network_type: 'wifi',
      device_class: 'desktop',
      page: 1,
      page_size: 20,
    })));
    expect(mocks.fetchPerformanceSamples.mock.calls[0][0]).not.toHaveProperty('limit');
    expect(mocks.fetchPerformanceSamples.mock.calls[0][0]).not.toHaveProperty('min_samples');

    fireEvent.click(screen.getByRole('button', { name: '复制 request_id' }));
    await waitFor(() => expect(navigator.clipboard.writeText).toHaveBeenCalledWith('req-safe-1'));
    expect(mocks.trackUsageEvent).toHaveBeenCalledWith('copy_request_id', expect.objectContaining({
      module: 'performance_samples',
      request_id: 'req-safe-1',
    }));

    fireEvent.click(screen.getByRole('button', { name: '下一页' }));
    await waitFor(() => expect(mocks.fetchPerformanceSamples).toHaveBeenCalledWith(expect.objectContaining({
      page: 2,
      page_size: 20,
    })));
  });

  it('shows miniapp metric labels in sample context and rows', async () => {
    mocks.fetchPerformanceSamples.mockResolvedValue({
      items: [
        {
          id: 'perf-miniapp-1',
          client_type: 'wechat_miniapp',
          page_key: 'app/launch',
          metric_name: 'app_launch_ready',
          duration_ms: 38,
          app_version: 'v1.1.0',
          network_type: 'wifi',
          device_class: 'miniapp',
          request_id: 'miniapp-rum:safe:abcd1234',
          occurred_at: '2026-08-11T00:00:00Z',
          server_received_at: '2026-08-11T00:00:01Z',
        },
      ],
      total: 1,
      page: 1,
      page_size: 20,
      total_pages: 1,
      filters: {},
    });

    render(
      <MemoryRouter initialEntries={['/admin/performance/samples?client_type=wechat_miniapp&page_key=app%2Flaunch&metric_name=app_launch_ready&app_version=v1.1.0&network_type=wifi&device_class=miniapp']}>
        <PerformanceSamplesPage />
      </MemoryRouter>,
    );

    expect(await screen.findByText('微信小程序')).toBeInTheDocument();
    expect(screen.getAllByText('小程序启动就绪').length).toBeGreaterThanOrEqual(2);
    expect(screen.getAllByText('wifi').length).toBeGreaterThanOrEqual(2);
    expect(screen.getAllByText('miniapp').length).toBeGreaterThanOrEqual(2);
    expect(screen.getByText('miniapp...1234')).toBeInTheDocument();
  });
});
