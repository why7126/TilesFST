import { HeartIcon, Share2Icon } from 'lucide-react';

import {
  FeaturedCard,
  ProductCard,
  ProductCardAction,
  ProductGrid,
  TextureRow,
} from '@/shared/business';

import { DesignSection, DesignSubSection } from './components';

const gridItems = [
  {
    kind: 'featured' as const,
    data: {
      id: 'f-demo',
      name: '鱼肚白大理石',
      spec: '1200×2400mm · 意大利',
      price: '¥ 680',
      specs: [
        { label: '产地', value: '意大利' },
        { label: '规格', value: '1200×2400' },
        { label: '厚度', value: '9mm' },
        { label: '表面', value: '抛光' },
      ] as [
        { label: string; value: string },
        { label: string; value: string },
        { label: string; value: string },
        { label: string; value: string },
      ],
      badges: [{ variant: 'inStock' as const, label: '现货' }],
      onCta: () => undefined,
      onFavorite: () => undefined,
    },
  },
  {
    kind: 'product' as const,
    data: {
      id: 'p-demo-1',
      name: '卡拉拉白',
      spec: '800×800mm · 中国',
      price: '¥ 128',
      badges: [{ variant: 'hotSale' as const, label: '热销' }],
    },
  },
  {
    kind: 'product' as const,
    data: {
      id: 'p-demo-2',
      name: '爵士白',
      spec: '900×1800mm · 中国',
      price: '¥ 156',
      badges: [{ variant: 'new' as const, label: '新品' }],
    },
  },
];

const textures = [
  { id: 't1', name: '暖白', color: 'var(--color-brand-gold-muted)' },
  { id: 't2', name: '米灰', color: 'var(--color-bg-overlay)' },
  { id: 't3', name: '深灰', color: 'var(--color-border-strong)' },
  { id: 't4', name: '玄黑', color: 'var(--color-deep)' },
  { id: 't5', name: '砂金', color: 'var(--color-brand-gold-badge)' },
  { id: 't6', name: '岩灰', color: 'var(--color-border-default)' },
  { id: 't7', name: '雾白', color: 'var(--color-bg-badge-neutral)' },
  { id: 't8', name: '赤棕', color: 'var(--color-hot-sale-muted)' },
];

const productActions = [
  { id: 'fav', label: '收藏', icon: HeartIcon },
  { id: 'share', label: '分享', icon: Share2Icon },
];

export function BusinessSection() {
  return (
    <DesignSection
      id="business-catalog"
      title="Business Components · 目录业务"
      description="src/web/src/shared/business/ — rules/ui-design.md §5.7–5.9"
    >
      <div className="space-y-10">
        <DesignSubSection title="ProductCard">
          <div className="max-w-xs">
            <ProductCard product={gridItems[1].data} actions={productActions} />
          </div>
        </DesignSubSection>

        <DesignSubSection title="FeaturedCard">
          <FeaturedCard product={gridItems[0].data} />
        </DesignSubSection>

        <DesignSubSection title="ProductCardAction（28×28）">
          <div className="flex gap-2">
            <ProductCardAction icon={HeartIcon} label="收藏" />
            <ProductCardAction icon={Share2Icon} label="分享" />
          </div>
        </DesignSubSection>

        <DesignSubSection title="TextureRow（8 色块）">
          <div className="overflow-hidden rounded-card border border-border-default bg-page">
            <TextureRow items={textures} />
          </div>
        </DesignSubSection>

        <DesignSubSection title="ProductGrid（3 列 + 精选跨 2 列 + 纹理条）">
          <ProductGrid items={gridItems} textures={textures} productActions={productActions} />
        </DesignSubSection>
      </div>
    </DesignSection>
  );
}
