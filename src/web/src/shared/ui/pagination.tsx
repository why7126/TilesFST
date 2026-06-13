import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-react';
import * as React from 'react';

import { cn } from '@/shared/lib/cn';

import { Button } from './button';

export interface PaginationProps extends React.HTMLAttributes<HTMLElement> {
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  siblingCount?: number;
}

function buildPageRange(page: number, totalPages: number, siblingCount: number): (number | 'ellipsis')[] {
  if (totalPages <= 1) return [1];

  const pages = new Set<number>([1, totalPages, page]);
  for (let i = 1; i <= siblingCount; i += 1) {
    pages.add(Math.max(1, page - i));
    pages.add(Math.min(totalPages, page + i));
  }

  const sorted = [...pages].sort((a, b) => a - b);
  const range: (number | 'ellipsis')[] = [];

  sorted.forEach((value, index) => {
    const prev = sorted[index - 1];
    if (prev !== undefined && value - prev > 1) {
      range.push('ellipsis');
    }
    range.push(value);
  });

  return range;
}

const Pagination = React.forwardRef<HTMLElement, PaginationProps>(
  ({ page, totalPages, onPageChange, siblingCount = 1, className, ...props }, ref) => {
    const items = buildPageRange(page, totalPages, siblingCount);

    return (
      <nav
        ref={ref}
        aria-label="分页"
        className={cn('flex items-center gap-1', className)}
        {...props}
      >
        <Button
          type="button"
          variant="outline"
          size="pagination"
          aria-label="上一页"
          disabled={page <= 1}
          onClick={() => onPageChange(page - 1)}
        >
          <ChevronLeftIcon />
        </Button>

        {items.map((item, index) =>
          item === 'ellipsis' ? (
            <span key={`ellipsis-${index}`} className="px-1 text-muted">
              …
            </span>
          ) : (
            <Button
              key={item}
              type="button"
              variant={item === page ? 'default' : 'outline'}
              size="pagination"
              aria-current={item === page ? 'page' : undefined}
              onClick={() => onPageChange(item)}
            >
              {item}
            </Button>
          ),
        )}

        <Button
          type="button"
          variant="outline"
          size="pagination"
          aria-label="下一页"
          disabled={page >= totalPages}
          onClick={() => onPageChange(page + 1)}
        >
          <ChevronRightIcon />
        </Button>
      </nav>
    );
  },
);
Pagination.displayName = 'Pagination';

export { Pagination };
