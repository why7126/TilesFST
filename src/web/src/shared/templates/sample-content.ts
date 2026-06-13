/**
 * STONEX sample content for page templates — replace with API data in features/
 * Source: rules/ui-design.md §6
 */

import type { LandingPageContent, ListPageContent } from '@shared/templates/types';
import type { SidebarSection } from '@/shared/ui/sidebar';

export const sampleSidebarSections: SidebarSection[] = [
  {
    id: 'texture',
    title: '纹理',
    items: [
      { id: 'marble', label: '大理石', checked: true },
      { id: 'granite', label: '花岗岩' },
      { id: 'slate', label: '板岩' },
    ],
  },
  {
    id: 'color',
    title: '色系',
    items: [
      { id: 'white', label: '白色系' },
      { id: 'gray', label: '灰色系' },
      { id: 'gold', label: '金色系' },
    ],
  },
];

export const sampleLandingContent: LandingPageContent = {
  navLinks: [
    { label: '材质库', href: '/catalog', active: true },
    { label: '工程案例', href: '/cases' },
    { label: '供应商', href: '/suppliers' },
  ],
  eyebrow: 'Industrial Stone Archive',
  heroTitle: '专业石材瓷砖数据库',
  heroDescription:
    '面向高端工程采购与室内设计场景，提供可检索、可比对、可询价的材质档案与供应信息。',
  heroMaterials: [
    { id: 'm1', name: '鱼肚白', spec: '1200×2400', color: 'var(--color-bg-overlay)' },
    { id: 'm2', name: '卡拉拉白', spec: '800×800', color: 'var(--color-brand-gold-muted)' },
    { id: 'm3', name: '深灰岩', spec: '600×1200', color: 'var(--color-border-default)' },
  ],
  stats: [
    { value: '12,480', label: '材质档案' },
    { value: '860', label: '供应商' },
    { value: '2,140', label: '工程案例' },
    { value: '98%', label: '规格覆盖' },
  ],
  dataStrip: [
    { value: '328', label: '本周新增材质' },
    { value: '1,204', label: '现货 SKU' },
    { value: '56', label: '热门色系' },
    { value: '18', label: '今日询价' },
  ],
  filterChips: [
    { id: 'all', label: '全部', active: true },
    { id: 'in-stock', label: '现货' },
    { id: 'new', label: '新品' },
    { id: 'hot', label: '热销' },
  ],
  gridItems: [
    {
      kind: 'featured',
      data: {
        id: 'f1',
        name: '鱼肚白大理石',
        spec: '1200×2400mm · 意大利',
        price: '¥ 680',
        specs: [
          { label: '产地', value: '意大利' },
          { label: '规格', value: '1200×2400' },
          { label: '厚度', value: '9mm' },
          { label: '表面', value: '抛光' },
        ],
        badges: [{ variant: 'inStock', label: '现货' }],
      },
    },
    {
      kind: 'product',
      data: {
        id: 'p1',
        name: '卡拉拉白',
        spec: '800×800mm · 中国',
        price: '¥ 128',
        badges: [{ variant: 'hotSale', label: '热销' }],
      },
    },
    {
      kind: 'product',
      data: {
        id: 'p2',
        name: '爵士白',
        spec: '900×1800mm · 中国',
        price: '¥ 156',
        badges: [{ variant: 'new', label: '新品' }],
      },
    },
  ],
  textures: [
    { id: 't1', name: '暖白', color: 'var(--color-brand-gold-muted)' },
    { id: 't2', name: '米灰', color: 'var(--color-bg-overlay)' },
    { id: 't3', name: '深灰', color: 'var(--color-border-strong)' },
    { id: 't4', name: '玄黑', color: 'var(--color-deep)' },
    { id: 't5', name: '砂金', color: 'var(--color-brand-gold-badge)' },
    { id: 't6', name: '岩灰', color: 'var(--color-border-default)' },
    { id: 't7', name: '雾白', color: 'var(--color-bg-badge-neutral)' },
    { id: 't8', name: '赤棕', color: 'var(--color-hot-sale-muted)' },
  ],
  resultCount: 128,
  sortLabel: '默认排序',
  footerBrand: {
    title: 'STONEX',
    description: '工业石材 · 暗色旗舰风材质数据库，服务工程采购与设计决策。',
  },
  footerColumns: [
    {
      title: '产品',
      links: [
        { label: '材质库', href: '/catalog' },
        { label: 'AI 找砖', href: '/ai' },
      ],
    },
    {
      title: '支持',
      links: [
        { label: '帮助中心', href: '/help' },
        { label: '联系我们', href: '/contact' },
      ],
    },
    {
      title: '公司',
      links: [
        { label: '关于 STONEX', href: '/about' },
        { label: '供应商入驻', href: '/join' },
      ],
    },
  ],
  copyright: '© 2026 STONEX. All rights reserved.',
};

export const sampleListContent: ListPageContent = {
  filterChips: sampleLandingContent.filterChips,
  gridItems: sampleLandingContent.gridItems,
  textures: sampleLandingContent.textures,
  resultCount: sampleLandingContent.resultCount,
  sortLabel: sampleLandingContent.sortLabel,
  page: 1,
  totalPages: 8,
};
