import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { MetricCard, MetricCardGrid } from './metric-card';

describe('MetricCard', () => {
  it('renders content and preserves stable admin metric DOM classes', () => {
    render(<MetricCard label="SKU 总数" value={128} description="全部商品主数据" />);

    const card = screen.getByText('SKU 总数').closest('article');
    expect(card).toHaveClass('metric-card');
    expect(screen.getByText('SKU 总数')).toHaveClass('metric-label');
    expect(screen.getByText('128')).toHaveClass('metric-value');
    expect(screen.getByText('全部商品主数据')).toHaveClass('metric-desc');
  });

  it('renders loading and empty values with a unified placeholder', () => {
    const { rerender } = render(<MetricCard label="EMPTY" value={null} description={null} />);

    expect(screen.getAllByText('—')).toHaveLength(2);

    rerender(<MetricCard label="LOADING" value={100} description="加载中占位" loading />);
    expect(screen.getByText('—')).toHaveClass('metric-value');
    expect(screen.getByText('加载中占位')).toHaveClass('metric-desc');
  });

  it('marks danger descriptions through the existing danger class', () => {
    render(<MetricCard label="API ERRORS" value={7} description="异常请求" dangerDescription />);

    expect(screen.getByText('异常请求')).toHaveClass('metric-desc', 'danger');
  });
});

describe('MetricCardGrid', () => {
  it('renders an accessible summary grid for 2, 3, and 4 card layouts', () => {
    const { rerender } = render(
      <MetricCardGrid ariaLabel="2 卡指标示例" columns={2}>
        <MetricCard label="A" value={1} description="Alpha" />
        <MetricCard label="B" value={2} description="Beta" />
      </MetricCardGrid>,
    );

    expect(screen.getByLabelText('2 卡指标示例')).toHaveClass('summary-grid', '!grid-cols-2');
    expect(screen.getByLabelText('2 卡指标示例')).toHaveAttribute('data-columns', '2');

    rerender(
      <MetricCardGrid ariaLabel="3 卡指标示例" columns={3}>
        <MetricCard label="A" value={1} description="Alpha" />
      </MetricCardGrid>,
    );
    expect(screen.getByLabelText('3 卡指标示例')).toHaveClass('summary-grid', '!grid-cols-3');

    rerender(
      <MetricCardGrid ariaLabel="4 卡指标示例">
        <MetricCard label="A" value={1} description="Alpha" />
      </MetricCardGrid>,
    );
    expect(screen.getByLabelText('4 卡指标示例')).toHaveClass('summary-grid', '!grid-cols-4');
  });
});
