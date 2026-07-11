import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { ThemeProvider } from '@/features/theme/ThemeContext';

import { DesignSystemPage } from './DesignSystemPage';

describe('DesignSystemPage', () => {
  it('renders admin list foundation component examples and pagination contracts', () => {
    const { container } = render(
      <ThemeProvider>
        <DesignSystemPage />
      </ThemeProvider>,
    );

    expect(screen.getByLabelText('2 卡指标示例')).toHaveClass('summary-grid', '!grid-cols-2');
    expect(screen.getByLabelText('3 卡指标示例')).toHaveClass('summary-grid', '!grid-cols-3');
    expect(screen.getByLabelText('4 卡指标示例')).toHaveClass('summary-grid', '!grid-cols-4');
    expect(screen.getByText('异常请求')).toHaveClass('metric-desc', 'danger');
    expect(screen.getByText('加载中占位')).toHaveClass('metric-desc');

    const paginationBlocks = Array.from(container.querySelectorAll('.pagination'));
    expect(paginationBlocks.length).toBeGreaterThanOrEqual(4);
    paginationBlocks.slice(0, 3).forEach((pagination) => {
      expect(pagination.querySelector('.page-summary')).toBeInTheDocument();
      expect(pagination.querySelector('.page-right')).toBeInTheDocument();
      expect(pagination.querySelector('.page-buttons')).toBeInTheDocument();
      expect(pagination.querySelector('.page-size-wrap')).toBeInTheDocument();
      expect(pagination.querySelectorAll('.page-btn').length).toBeLessThanOrEqual(5);
    });

    expect(screen.getByText('管理端列表模板')).toBeInTheDocument();
    expect(container.querySelector('#admin-list-page-contract')).toBeInTheDocument();
    expect(container.querySelector('[data-admin-list-section="title"]')).toBeInTheDocument();
    expect(container.querySelector('[data-admin-list-section="metrics"]')).toBeInTheDocument();
    expect(container.querySelector('[data-admin-list-section="filters"]')).toBeInTheDocument();
    expect(container.querySelector('[data-admin-list-section="list"]')).toBeInTheDocument();
    expect(container.querySelector('[data-admin-list-section="pagination"]')).toBeInTheDocument();
    expect(container.querySelector('th.admin-sticky-action-cell')).toBeInTheDocument();
    expect(screen.getByText('/admin/tile-skus')).toBeInTheDocument();
    expect(screen.getByText('/admin/api-docs')).toBeInTheDocument();
    expect(container.querySelector('[data-admin-list-boundary="loading"]')).toBeInTheDocument();
    expect(container.querySelector('[data-admin-list-boundary="empty"]')).toBeInTheDocument();
    expect(container.querySelector('[data-admin-list-boundary="error"]')).toBeInTheDocument();
    expect(container.querySelector('[data-admin-list-boundary="single-page"]')).toBeInTheDocument();
    expect(screen.getByLabelText('主题')).toBeInTheDocument();
  });
});
