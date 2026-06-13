/**
 * STONEX catalog business types — cross-platform
 * Source: rules/ui-design.md §5.7–5.9
 */

export type ProductBadgeVariant = 'inStock' | 'new' | 'hotSale';

export interface ProductBadge {
  variant: ProductBadgeVariant;
  label: string;
}

export interface ProductCardData {
  id: string;
  name: string;
  spec: string;
  price: string;
  priceUnit?: string;
  imageUrl?: string;
  imageAlt?: string;
  badges?: ProductBadge[];
  href?: string;
  onClick?: () => void;
}

export interface FeaturedSpecItem {
  label: string;
  value: string;
}

export interface FeaturedCardData extends Omit<ProductCardData, 'actions'> {
  specs: [FeaturedSpecItem, FeaturedSpecItem, FeaturedSpecItem, FeaturedSpecItem];
  ctaLabel?: string;
  onCta?: () => void;
  onFavorite?: () => void;
  favoriteLabel?: string;
}

export interface TextureSwatch {
  id: string;
  name: string;
  /** CSS color value — use token-backed values at call site, e.g. var(--color-brand-gold) */
  color: string;
}

export type ProductGridEntry =
  | { kind: 'product'; data: ProductCardData }
  | { kind: 'featured'; data: FeaturedCardData };
