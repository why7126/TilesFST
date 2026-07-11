import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { AdminListPage } from './admin-list-page';

const rows = [
  { id: 1, name: '岩境灰', status: '已上架' },
  { id: 2, name: '云脉白', status: '草稿' },
];

const columns = [
  { key: 'name', header: '名称' },
  { key: 'status', header: '状态' },
  {
    key: 'actions',
    header: '操作',
    stickyAction: true,
    render: () => <button type="button">编辑</button>,
  },
];

describe('AdminListPage', () => {
  it('renders title, metrics, filters, list, and pagination in the required order', () => {
    const { container } = render(
      <AdminListPage
        content={{
          title: '管理端列表模板',
          description: '统一管理端列表页契约',
          metrics: [{ label: 'TOTAL', value: 2, description: '全部记录' }],
          filters: [
            {
              id: 'status',
              label: '状态',
              control: <select id="status" aria-label="状态" />,
            },
          ],
          columns,
          rows,
          pagination: { page: 1, total: 2, pageSize: 20, itemLabel: '样例' },
        }}
        onReset={() => undefined}
        onPageChange={() => undefined}
        onPageSizeChange={() => undefined}
      />,
    );

    const sections = Array.from(container.querySelectorAll('[data-admin-list-section]')).map(
      (section) => section.getAttribute('data-admin-list-section'),
    );

    expect(sections).toEqual(['title', 'metrics', 'filters', 'list', 'pagination']);
    expect(container.querySelector('.metric-card .metric-label')).toHaveTextContent('TOTAL');
    expect(screen.queryByRole('button', { name: '查询' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '搜索' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: '重置' })).toBeInTheDocument();
  });

  it('keeps pagination and sticky action column DOM contracts stable', () => {
    const { container } = render(
      <AdminListPage
        content={{
          title: '管理端列表模板',
          columns,
          rows,
          pagination: { page: 1, total: 1, pageSize: 20, itemLabel: '样例' },
        }}
        onPageChange={() => undefined}
        onPageSizeChange={() => undefined}
      />,
    );

    const pagination = container.querySelector('.pagination');
    expect(pagination?.querySelector('.page-summary')).toHaveTextContent('共 1 条样例');
    expect(pagination?.querySelector('.page-right')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-buttons')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-size-wrap')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-btn.active')).toHaveTextContent('1');
    expect(container.querySelector('th.admin-sticky-action-cell')).toBeInTheDocument();
    expect(container.querySelector('td.admin-sticky-action-cell')).toBeInTheDocument();
  });

  it('resets pagination to page 1 when page size changes', () => {
    const onPageChange = vi.fn();
    const onPageSizeChange = vi.fn();

    render(
      <AdminListPage
        content={{
          title: '管理端列表模板',
          columns,
          rows,
          pagination: {
            page: 3,
            total: 120,
            pageSize: 20,
            pageSizeOptions: [20, 50],
            itemLabel: '样例',
          },
        }}
        onPageChange={onPageChange}
        onPageSizeChange={onPageSizeChange}
      />,
    );

    fireEvent.change(screen.getByRole('combobox', { name: '每页显示条数' }), {
      target: { value: '50' },
    });

    expect(onPageSizeChange).toHaveBeenCalledWith(50);
    expect(onPageChange).toHaveBeenCalledWith(1);
  });

  it('renders loading, empty, and error state copy without inserting section headings', () => {
    const { rerender } = render(
      <AdminListPage
        content={{
          title: '管理端列表模板',
          columns,
          rows: [],
          state: { loadingText: '加载中' },
        }}
        loading
      />,
    );

    expect(screen.getByText('加载中')).toBeInTheDocument();

    rerender(
      <AdminListPage
        content={{
          title: '管理端列表模板',
          columns,
          rows: [],
          state: { emptyText: '暂无模板数据' },
        }}
      />,
    );
    expect(screen.getByText('暂无模板数据')).toBeInTheDocument();

    rerender(
      <AdminListPage
        content={{
          title: '管理端列表模板',
          columns,
          rows: [],
          state: { errorText: '模板加载失败' },
        }}
        error="模板加载失败"
      />,
    );
    expect(screen.getByText('模板加载失败')).toBeInTheDocument();
    expect(screen.queryByText('列表')).not.toBeInTheDocument();
  });
});
