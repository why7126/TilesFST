import * as React from 'react';

import { cn } from '@/shared/lib/cn';

export interface ProductListHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  resultCount: number;
  sortLabel?: string;
}

export function ProductListHeader({
  resultCount,
  sortLabel = '默认排序',
  className,
  ...props
}: ProductListHeaderProps) {
  return (
    <div
      className={cn('flex items-center justify-between border-b border-border-default px-1 pb-4', className)}
      {...props}
    >
      <p className="text-[11px] text-muted">
        共 <span className="text-primary">{resultCount}</span> 个结果
      </p>
      <button type="button" className="text-[11px] text-secondary transition-colors hover:text-primary">
        {sortLabel}
      </button>
    </div>
  );
}
