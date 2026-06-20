import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it } from 'vitest';

import { DashboardPage } from './DashboardPage';

describe('DashboardPage', () => {
  it('renders four metrics, four quick actions, and recent updates table', () => {
    render(
      <MemoryRouter>
        <DashboardPage />
      </MemoryRouter>,
    );

    expect(screen.getByText('SKU 总数')).toBeInTheDocument();
    expect(screen.getByText('品牌数量')).toBeInTheDocument();
    expect(screen.getByText('Banner 数量')).toBeInTheDocument();
    expect(screen.getByText('用户数量')).toBeInTheDocument();

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
});
