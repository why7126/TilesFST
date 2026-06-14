import * as React from 'react';

import { cn } from '@/shared/lib/cn';
import { Button } from '@/shared/ui/button';

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
      <Button
        type="button"
        variant="link"
        size="sm"
        className="h-auto p-0 text-[11px] text-secondary hover:text-primary"
      >
        {sortLabel}
      </Button>
    </div>
  );
}
