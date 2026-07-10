import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { DesignSystemPage } from './DesignSystemPage';

describe('DesignSystemPage', () => {
  it('renders admin list foundation component examples and pagination contracts', () => {
    const { container } = render(<DesignSystemPage />);

    expect(screen.getByLabelText('2 卡指标示例')).toHaveClass('summary-grid', '!grid-cols-2');
    expect(screen.getByLabelText('3 卡指标示例')).toHaveClass('summary-grid', '!grid-cols-3');
    expect(screen.getByLabelText('4 卡指标示例')).toHaveClass('summary-grid', '!grid-cols-4');
    expect(screen.getByText('异常请求')).toHaveClass('metric-desc', 'danger');
    expect(screen.getByText('加载中占位')).toHaveClass('metric-desc');

    const paginationBlocks = Array.from(container.querySelectorAll('.pagination'));
    expect(paginationBlocks).toHaveLength(3);
    paginationBlocks.forEach((pagination) => {
      expect(pagination.querySelector('.page-summary')).toBeInTheDocument();
      expect(pagination.querySelector('.page-right')).toBeInTheDocument();
      expect(pagination.querySelector('.page-buttons')).toBeInTheDocument();
      expect(pagination.querySelector('.page-size-wrap')).toBeInTheDocument();
      expect(pagination.querySelectorAll('.page-btn').length).toBeLessThanOrEqual(5);
    });
  });
});
