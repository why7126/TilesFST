import type { AdminListPageContent } from '@shared/templates/types';

import { Input } from '@/components/ui/input';
import { cn } from '@/shared/lib/cn';
import { Button } from '@/shared/ui/button';

export interface AdminListPageProps<T extends { id: string }> {
  content: AdminListPageContent<T>;
  onCreate?: () => void;
  onSearch?: (value: string) => void;
  onRowClick?: (row: T) => void;
  className?: string;
}

export function AdminListPage<T extends { id: string }>({
  content,
  onCreate,
  onSearch,
  onRowClick,
  className,
}: AdminListPageProps<T>) {
  const { title, description, searchPlaceholder = '搜索…', createLabel = '新建', columns, rows } =
    content;

  return (
    <section className={cn('space-y-6', className)}>
      <div className="flex flex-col gap-4 border-b border-border-default pb-6 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-[22px] font-normal text-primary">{title}</h1>
          {description ? <p className="mt-2 text-[13px] text-secondary">{description}</p> : null}
        </div>
        {onCreate ? (
          <Button size="sm" onClick={onCreate}>
            {createLabel}
          </Button>
        ) : null}
      </div>

      <div className="max-w-md">
        <Input
          placeholder={searchPlaceholder}
          onChange={(event) => onSearch?.(event.target.value)}
        />
      </div>

      <div className="overflow-hidden rounded-card border border-border-default">
        <div
          className="grid border-b border-border-default bg-surface px-4 py-3 text-[11px] font-medium tracking-section text-muted uppercase"
          style={{ gridTemplateColumns: `repeat(${columns.length}, minmax(0, 1fr))` }}
        >
          {columns.map((column) => (
            <span key={column.key}>{column.header}</span>
          ))}
        </div>

        <div className="divide-y divide-border-default bg-page">
          {rows.map((row) => (
            <button
              key={row.id}
              type="button"
              onClick={() => onRowClick?.(row)}
              className="grid w-full px-4 py-3 text-left text-[13px] text-primary transition-colors hover:bg-accent"
              style={{ gridTemplateColumns: `repeat(${columns.length}, minmax(0, 1fr))` }}
            >
              {columns.map((column) => (
                <span key={column.key} className="truncate">
                  {column.render ? column.render(row) : String((row as Record<string, unknown>)[column.key] ?? '')}
                </span>
              ))}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
