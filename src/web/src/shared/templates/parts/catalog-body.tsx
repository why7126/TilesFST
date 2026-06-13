import * as React from 'react';

import { cn } from '@/shared/lib/cn';
import { ProductGrid } from '@/shared/business/product-grid';
import type { ProductGridProps } from '@/shared/business/product-grid';
import { Pagination } from '@/shared/ui/pagination';
import { Sidebar, type SidebarSection } from '@/shared/ui/sidebar';

import { ProductListHeader } from './product-list-header';

export interface CatalogBodyProps extends Omit<ProductGridProps, 'className'> {
  sidebarSections: SidebarSection[];
  resultCount: number;
  sortLabel?: string;
  page?: number;
  totalPages?: number;
  onPageChange?: (page: number) => void;
  className?: string;
}

export function CatalogBody({
  sidebarSections,
  resultCount,
  sortLabel,
  page,
  totalPages,
  onPageChange,
  className,
  ...gridProps
}: CatalogBodyProps) {
  return (
    <div className={cn('flex bg-page', className)}>
      <Sidebar sections={sidebarSections} />
      <div className="min-w-0 flex-1 px-7 py-6">
        <ProductListHeader resultCount={resultCount} sortLabel={sortLabel} />
        <div className="mt-4">
          <ProductGrid {...gridProps} />
        </div>
        {page !== undefined && totalPages !== undefined && onPageChange ? (
          <div className="mt-6 flex justify-center">
            <Pagination page={page} totalPages={totalPages} onPageChange={onPageChange} />
          </div>
        ) : null}
      </div>
    </div>
  );
}
