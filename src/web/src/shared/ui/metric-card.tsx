import type { ReactNode } from 'react';

import { cn } from '@/shared/lib/cn';

type MetricValue = ReactNode | null | undefined;

export interface MetricCardProps {
  label: ReactNode;
  value?: MetricValue;
  description?: ReactNode;
  loading?: boolean;
  dangerDescription?: boolean;
  placeholder?: ReactNode;
  className?: string;
}

export function MetricCard({
  label,
  value,
  description,
  loading = false,
  dangerDescription = false,
  placeholder = '—',
  className,
}: MetricCardProps) {
  const displayValue = loading || value === null || value === undefined || value === '' ? placeholder : value;

  return (
    <article className={cn('metric-card', className)} aria-busy={loading || undefined}>
      <div className="metric-label">{label}</div>
      <div className="metric-value">{displayValue}</div>
      <div className={cn('metric-desc', dangerDescription && 'danger')}>{description ?? placeholder}</div>
    </article>
  );
}

export interface MetricCardGridProps {
  children: ReactNode;
  ariaLabel: string;
  columns?: 2 | 3 | 4;
  className?: string;
}

const gridColumnClass: Record<NonNullable<MetricCardGridProps['columns']>, string> = {
  2: '!grid-cols-2',
  3: '!grid-cols-3',
  4: '!grid-cols-4',
};

export function MetricCardGrid({ children, ariaLabel, columns = 4, className }: MetricCardGridProps) {
  return (
    <section
      className={cn('summary-grid', gridColumnClass[columns], className)}
      aria-label={ariaLabel}
      data-columns={columns}
    >
      {children}
    </section>
  );
}
