import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { DashboardPage } from './DashboardPage';
import { fetchDashboardSummary } from '../../features/admin/api/dashboard-api';
import type { AdminDashboardSummary } from '../../shared/api/generated';

vi.mock('../../features/admin/api/dashboard-api', () => ({
  fetchDashboardSummary: vi.fn(),
}));

const dashboardSummary: AdminDashboardSummary = {
  sku_total: { value: 7, description: '已建档 SKU', visible: true },
  brand_total: { value: 2, description: '有效品牌', visible: true },
  banner_total: { value: 3, description: '有效 Banner', visible: true },
  user_total: { value: 1, description: '后台授权账号', visible: true },
};

describe('DashboardPage', () => {
  beforeEach(() => {
    vi.mocked(fetchDashboardSummary).mockResolvedValue(dashboardSummary);
  });

  it('renders real metrics, quick actions, and recent updates table', async () => {
    render(
      <MemoryRouter>
        <DashboardPage />
      </MemoryRouter>,
    );

    expect(screen.getByText('SKU 总数')).toBeInTheDocument();
    expect(screen.getByText('品牌数量')).toBeInTheDocument();
    expect(screen.getByText('Banner 数量')).toBeInTheDocument();
    expect(screen.getByText('用户数量')).toBeInTheDocument();
    expect(await screen.findByText('7')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.queryByText('12,860')).not.toBeInTheDocument();

    expect(screen.getByText('新增 SKU')).toBeInTheDocument();
    expect(screen.getByText('新增品牌')).toBeInTheDocument();
    expect(screen.getByText('新增类目')).toBeInTheDocument();
    expect(screen.getByText('新增 Banner')).toBeInTheDocument();

    expect(screen.queryByText('导入 SKU')).not.toBeInTheDocument();
    expect(screen.queryByText('价格管理')).not.toBeInTheDocument();

    expect(screen.getByRole('columnheader', { name: '更新时间' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: '类型' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: '名称' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: '操作人' })).toBeInTheDocument();
    expect(screen.getByText('CALACATTA 900×1800')).toBeInTheDocument();
  });

  it('shows loading state before summary is returned', () => {
    vi.mocked(fetchDashboardSummary).mockReturnValue(new Promise(() => undefined));

    render(
      <MemoryRouter>
        <DashboardPage />
      </MemoryRouter>,
    );

    expect(screen.getAllByText('加载中')).toHaveLength(4);
  });

  it('shows error and retry action when summary request fails', async () => {
    vi.mocked(fetchDashboardSummary).mockRejectedValue(new Error('network error'));

    render(
      <MemoryRouter>
        <DashboardPage />
      </MemoryRouter>,
    );

    expect(await screen.findByRole('alert')).toHaveTextContent('数据概览加载失败');
    expect(screen.getByRole('button', { name: '重试' })).toBeInTheDocument();
    expect(screen.queryByText('12,860')).not.toBeInTheDocument();
  });

  it('hides user total when backend marks it invisible', async () => {
    vi.mocked(fetchDashboardSummary).mockResolvedValue({
      ...dashboardSummary,
      user_total: { value: 0, description: '仅系统管理员可见', visible: false },
    });

    render(
      <MemoryRouter>
        <DashboardPage />
      </MemoryRouter>,
    );

    expect(await screen.findByText('—')).toBeInTheDocument();
    expect(screen.getByText('仅系统管理员可见')).toBeInTheDocument();
  });
});
