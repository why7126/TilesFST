import type { LandingPageContent } from '@shared/templates/types';

import { SearchBar } from '@/shared/ui/search-bar';
import type { SidebarSection } from '@/shared/ui/sidebar';

import { CatalogBody } from './parts/catalog-body';
import { DataStrip } from './parts/data-strip';
import { FilterChips } from './parts/filter-chips';
import { HeroSection } from './parts/hero-section';
import { SiteFooter } from './parts/site-footer';
import { SiteNav } from './parts/site-nav';

export interface LandingPageProps {
  content: LandingPageContent;
  sidebarSections: SidebarSection[];
  page?: number;
  totalPages?: number;
  onPageChange?: (page: number) => void;
  onSearch?: (query: string) => void;
  onAiFindBrick?: () => void;
  onFilterChipClick?: (id: string) => void;
  onHeroPrimary?: () => void;
  onHeroSecondary?: () => void;
}

export function LandingPage({
  content,
  sidebarSections,
  page = 1,
  totalPages = 1,
  onPageChange,
  onSearch,
  onAiFindBrick,
  onFilterChipClick,
  onHeroPrimary,
  onHeroSecondary,
}: LandingPageProps) {
  return (
    <div className="min-h-screen bg-page text-primary">
      <SiteNav links={content.navLinks} />

      <HeroSection
        eyebrow={content.eyebrow}
        title={content.heroTitle}
        description={content.heroDescription}
        materials={content.heroMaterials}
        stats={content.stats}
        onPrimaryAction={onHeroPrimary}
        onSecondaryAction={onHeroSecondary}
      />

      <DataStrip items={content.dataStrip} />

      <div className="bg-page px-7 py-4">
        <SearchBar onSearch={onSearch} onAiFindBrick={onAiFindBrick} />
      </div>

      <FilterChips chips={content.filterChips} onChipClick={onFilterChipClick} />

      <CatalogBody
        sidebarSections={sidebarSections}
        resultCount={content.resultCount}
        sortLabel={content.sortLabel}
        items={content.gridItems}
        textures={content.textures}
        page={page}
        totalPages={totalPages}
        onPageChange={onPageChange}
      />

      <SiteFooter
        brand={content.footerBrand}
        columns={content.footerColumns}
        copyright={content.copyright}
      />
    </div>
  );
}
