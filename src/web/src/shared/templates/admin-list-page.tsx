import type { ReactNode } from 'react';
import type { AdminListColumn, AdminListPageContent } from '@shared/templates/types';

import { Input } from '@/components/ui/input';
import { cn } from '@/shared/lib/cn';
import { MetricCard, MetricCardGrid } from '@/shared/ui/metric-card';

import { getPaginationWindow } from '../lib/pagination-window';

export interface AdminListPageProps<T extends { id: string | number }> {
  content: AdminListPageContent<T, ReactNode>;
  onCreate?: () => void;
  onSearch?: (value: string) => void;
  onReset?: () => void;
  onRowClick?: (row: T) => void;
  onPageChange?: (page: number) => void;
  onPageSizeChange?: (pageSize: number) => void;
  loading?: boolean;
  error?: ReactNode;
  feedback?: ReactNode;
  confirmDialog?: ReactNode;
  className?: string;
  tableClassName?: string;
}

function defaultRenderCell<T extends { id: string | number }>(
  row: T,
  column: AdminListColumn<T, ReactNode>,
) {
  if (column.render) {
    return column.render(row);
  }

  return String((row as Record<string, unknown>)[column.key] ?? '');
}

export function AdminListPage<T extends { id: string | number }>({
  content,
  onCreate,
  onSearch,
  onReset,
  onRowClick,
  onPageChange,
  onPageSizeChange,
  loading = false,
  error,
  feedback,
  confirmDialog,
  className,
  tableClassName,
}: AdminListPageProps<T>) {
  const {
    title,
    description,
    eyebrow,
    searchPlaceholder = '搜索…',
    createLabel = '新建',
    primaryActionLabel,
    actions = [],
    metrics = [],
    filters = [],
    columns,
    rows,
    pagination,
    state,
  } = content;
  const page = pagination?.page ?? 1;
  const pageSize = pagination?.pageSize ?? 20;
  const total = pagination?.total ?? rows.length;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const pageNumbers = getPaginationWindow(page, totalPages);
  const hasFilters = filters.length > 0 || onSearch || onReset;
  const emptyText = state?.emptyText ?? '暂无数据';
  const loadingText = state?.loadingText ?? '数据加载中…';
  const errorText = state?.errorText ?? '加载失败，请稍后重试';
  const permissionText = state?.permissionText ?? '暂无权限查看该列表';

  return (
    <section className={cn('space-y-6', className)} data-admin-list-page>
      {feedback}

      <div className="page-hero" data-admin-list-section="title">
        <div>
          {eyebrow ? <p className="eyebrow">{eyebrow}</p> : null}
          <h1 className="page-title">{title}</h1>
          {description ? <p className="page-desc">{description}</p> : null}
        </div>
        <div className="flex flex-wrap items-center gap-2">
          {actions.map((action) =>
            action.control ? (
              <span key={action.id}>{action.control}</span>
            ) : (
              <button
                key={action.id}
                type="button"
                className={cn(
                  'btn',
                  action.variant === 'primary' && 'primary',
                  action.variant === 'danger' && 'danger',
                )}
                onClick={action.onClick}
              >
                {action.label}
              </button>
            ),
          )}
          {onCreate ? (
            <button type="button" className="btn primary" onClick={onCreate}>
              {primaryActionLabel ?? createLabel}
            </button>
          ) : null}
        </div>
      </div>

      {metrics.length > 0 ? (
        <div data-admin-list-section="metrics">
          <MetricCardGrid ariaLabel={`${title}统计`}>
            {metrics.map((metric, index) => (
              <MetricCard
                key={index}
                label={metric.label}
                value={metric.value}
                description={metric.description}
                loading={metric.loading}
                dangerDescription={metric.dangerDescription}
              />
            ))}
          </MetricCardGrid>
        </div>
      ) : null}

      {hasFilters ? (
        <section className="filter-card" data-admin-list-section="filters">
          <div className="brand-filter-row">
            {onSearch ? (
              <div className="brand-form-item">
                <label htmlFor="admin-list-search">关键词</label>
                <Input
                  id="admin-list-search"
                  className="input"
                  placeholder={searchPlaceholder}
                  onChange={(event) => onSearch(event.target.value)}
                />
              </div>
            ) : null}
            {filters.map((filter) => (
              <div key={filter.id} className={cn('brand-form-item', filter.className)}>
                {filter.label ? <label htmlFor={filter.id}>{filter.label}</label> : null}
                {filter.control}
              </div>
            ))}
            {onReset ? (
              <div className="brand-form-item brand-filter-actions">
                <button type="button" className="btn" onClick={onReset}>
                  重置
                </button>
              </div>
            ) : null}
          </div>
        </section>
      ) : null}

      <section className="table-card" aria-label={`${title}列表`} data-admin-list-section="list">
        <div className="overflow-x-auto">
          <table className={tableClassName}>
            <thead>
              <tr>
                {columns.map((column) => (
                  <th
                    key={column.key}
                    className={cn(
                      column.stickyAction && 'admin-sticky-action-cell',
                      column.headerClassName,
                    )}
                  >
                    {column.header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={columns.length}>{loadingText}</td>
                </tr>
              ) : error ? (
                <tr>
                  <td colSpan={columns.length}>{error || errorText}</td>
                </tr>
              ) : state?.permissionText ? (
                <tr>
                  <td colSpan={columns.length}>{permissionText}</td>
                </tr>
              ) : rows.length === 0 ? (
                <tr>
                  <td colSpan={columns.length}>{emptyText}</td>
                </tr>
              ) : (
                rows.map((row) => (
                  <tr key={row.id} onClick={() => onRowClick?.(row)}>
                    {columns.map((column) => (
                      <td
                        key={column.key}
                        className={cn(
                          column.stickyAction && 'admin-sticky-action-cell',
                          column.className,
                        )}
                      >
                        {defaultRenderCell(row, column)}
                      </td>
                    ))}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {pagination ? (
          <div className="pagination" data-admin-list-section="pagination">
            <div className="page-summary">
              共 {total} 条{pagination.itemLabel ?? '记录'}
            </div>
            <div className="page-right">
              <div className="page-buttons">
                <button
                  type="button"
                  className="page-btn"
                  disabled={page <= 1}
                  onClick={() => onPageChange?.(Math.max(1, page - 1))}
                >
                  ‹
                </button>
                {pageNumbers.map((pageNumber) => (
                  <button
                    key={pageNumber}
                    type="button"
                    className={cn('page-btn', pageNumber === page && 'active')}
                    aria-current={pageNumber === page ? 'page' : undefined}
                    onClick={() => onPageChange?.(pageNumber)}
                  >
                    {pageNumber}
                  </button>
                ))}
                <button
                  type="button"
                  className="page-btn"
                  disabled={page >= totalPages}
                  onClick={() => onPageChange?.(Math.min(totalPages, page + 1))}
                >
                  ›
                </button>
              </div>
              <div className="page-size-wrap">
                <span>每页显示</span>
                <select
                  className="page-size"
                  value={pageSize}
                  aria-label="每页显示条数"
                  onChange={(event) => {
                    onPageSizeChange?.(Number(event.target.value));
                    onPageChange?.(1);
                  }}
                >
                  {(pagination.pageSizeOptions ?? [20, 50, 100]).map((option) => (
                    <option key={option} value={option}>
                      {option} 条
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        ) : null}
      </section>

      {confirmDialog}
    </section>
  );
}
