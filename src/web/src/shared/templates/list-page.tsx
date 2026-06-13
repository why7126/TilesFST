import type { ListPageContent, TemplateFooterColumn, TemplateNavLink } from '@shared/templates/types';

import { SearchBar } from '@/shared/ui/search-bar';
import type { SidebarSection } from '@/shared/ui/sidebar';

import { CatalogBody } from './parts/catalog-body';
import { FilterChips } from './parts/filter-chips';
import { SiteFooter } from './parts/site-footer';
import { SiteNav } from './parts/site-nav';

export interface ListPageProps {
  content: ListPageContent;
  sidebarSections: SidebarSection[];
  navLinks?: TemplateNavLink[];
  onPageChange?: (page: number) => void;
  onSearch?: (query: string) => void;
  onAiFindBrick?: () => void;
  onFilterChipClick?: (id: string) => void;
  footer?: {
    brand: { title: string; description: string };
    columns: TemplateFooterColumn[];
    copyright: string;
  };
}

const defaultNavLinks = [
  { label: '材质库', href: '/catalog', active: true },
  { label: '工程案例', href: '/cases' },
  { label: '供应商', href: '/suppliers' },
];

export function ListPage({
  content,
  sidebarSections,
  navLinks = defaultNavLinks,
  onPageChange,
  onSearch,
  onAiFindBrick,
  onFilterChipClick,
  footer,
}: ListPageProps) {
  return (
    <div className="min-h-screen bg-page text-primary">
      <SiteNav links={navLinks} />

      <div className="border-b border-border-default bg-page px-7 py-4">
        <SearchBar onSearch={onSearch} onAiFindBrick={onAiFindBrick} />
      </div>

      <FilterChips chips={content.filterChips} onChipClick={onFilterChipClick} />

      <CatalogBody
        sidebarSections={sidebarSections}
        resultCount={content.resultCount}
        sortLabel={content.sortLabel}
        items={content.gridItems}
        textures={content.textures}
        page={content.page}
        totalPages={content.totalPages}
        onPageChange={onPageChange}
      />

      {footer ? (
        <SiteFooter
          brand={footer.brand}
          columns={footer.columns}
          copyright={footer.copyright}
        />
      ) : null}
    </div>
  );
}
