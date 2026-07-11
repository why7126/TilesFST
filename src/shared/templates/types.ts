/**
 * STONEX page template types — cross-platform
 * Source: rules/ui-design.md §5–§6
 */

import type {
  ProductGridEntry,
  TextureSwatch,
} from '../business/types';

export interface TemplateNavLink {
  label: string;
  href: string;
  active?: boolean;
}

export interface TemplateStatItem {
  value: string;
  label: string;
}

export interface TemplateFilterChip {
  id: string;
  label: string;
  active?: boolean;
}

export interface TemplateHeroMaterial {
  id: string;
  name: string;
  spec: string;
  color: string;
}

export interface TemplateFooterColumn {
  title?: string;
  links: Array<{ label: string; href: string }>;
}

export interface LandingPageContent {
  navLinks: TemplateNavLink[];
  eyebrow: string;
  heroTitle: string;
  heroDescription: string;
  heroMaterials: [TemplateHeroMaterial, TemplateHeroMaterial, TemplateHeroMaterial];
  stats: [TemplateStatItem, TemplateStatItem, TemplateStatItem, TemplateStatItem];
  dataStrip: [TemplateStatItem, TemplateStatItem, TemplateStatItem, TemplateStatItem];
  filterChips: TemplateFilterChip[];
  gridItems: ProductGridEntry[];
  textures?: TextureSwatch[];
  resultCount: number;
  sortLabel?: string;
  footerBrand: { title: string; description: string };
  footerColumns: TemplateFooterColumn[];
  copyright: string;
}

export interface ListPageContent {
  filterChips: TemplateFilterChip[];
  gridItems: ProductGridEntry[];
  textures?: TextureSwatch[];
  resultCount: number;
  sortLabel?: string;
  page: number;
  totalPages: number;
}

export interface DetailPageSpecRow {
  label: string;
  value: string;
}

export interface DetailPageContent {
  name: string;
  spec: string;
  price: string;
  priceUnit?: string;
  imageUrl?: string;
  badges?: Array<{ variant: 'inStock' | 'new' | 'hotSale'; label: string }>;
  description?: string;
  specRows: DetailPageSpecRow[];
  ctaLabel?: string;
}

export interface AdminListMetric<Node = unknown> {
  label: Node;
  value?: Node;
  description?: Node;
  loading?: boolean;
  dangerDescription?: boolean;
}

export interface AdminListFilter<Node = unknown> {
  id: string;
  label?: string;
  control: Node;
  className?: string;
}

export interface AdminListColumn<
  T extends { id: string | number } = { id: string },
  Node = unknown,
> {
  key: string;
  header: string;
  render?: (row: T) => Node;
  stickyAction?: boolean;
  className?: string;
  headerClassName?: string;
}

export interface AdminListPageAction<Node = unknown> {
  id: string;
  label: string;
  control?: Node;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
}

export interface AdminListPaginationState {
  page: number;
  total: number;
  pageSize: number;
  pageSizeOptions?: number[];
  itemLabel?: string;
}

export interface AdminListPageStateContent {
  loadingText?: string;
  emptyText?: string;
  errorText?: string;
  permissionText?: string;
}

export interface AdminListPageContent<
  T extends { id: string | number } = { id: string },
  Node = unknown,
> {
  title: string;
  description?: string;
  eyebrow?: string;
  searchPlaceholder?: string;
  createLabel?: string;
  primaryActionLabel?: string;
  actions?: AdminListPageAction<Node>[];
  metrics?: AdminListMetric<Node>[];
  filters?: AdminListFilter<Node>[];
  columns: AdminListColumn<T, Node>[];
  rows: T[];
  pagination?: AdminListPaginationState;
  state?: AdminListPageStateContent;
}

export interface AdminFormField {
  id: string;
  label: string;
  type?: 'text' | 'textarea' | 'checkbox';
  placeholder?: string;
  defaultValue?: string;
  checked?: boolean;
}

export interface AdminEditPageContent {
  title: string;
  description?: string;
  fields: AdminFormField[];
  submitLabel?: string;
  cancelLabel?: string;
}
