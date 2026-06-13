/**
 * STONEX Design System — Typography Tokens
 * Source: rules/ui-design.md §3 字体系统
 */

/** Font family stacks */
export const fontFamily = {
  /** 正文与 UI — system sans-serif via CSS variable */
  sans: 'var(--font-sans, ui-sans-serif, system-ui, sans-serif)',
  /** STONEX Logo / 品牌名 — Cormorant Garamond */
  brand:
    "var(--font-brand, 'Cormorant Garamond', ui-serif, Georgia, 'Times New Roman', serif)",
  /** 等宽 — code, data tables (reserved) */
  mono: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
} as const;

/** Font size scale — semantic hierarchy */
export const fontSize = {
  /** 标签 / 眉标 — category labels, spec annotations (9–10px) */
  label: '9px',
  labelMd: '10px',
  /** 辅助文字 — specs, captions (11–12px) */
  caption: '11px',
  captionMd: '12px',
  /** 普通标题 — card names, nav (13–16px) */
  headingSm: '13px',
  headingMd: '15px',
  headingLg: '16px',
  /** 正文 — descriptions (13px, line-height 1.8) */
  body: '13px',
  /** 卡片标题 — featured card names (18–20px) */
  cardTitle: '18px',
  cardTitleLg: '20px',
  /** 页面标题 — section headings */
  pageTitle: '22px',
  /** 数据统计数字 — hero / data strip */
  stat: '20px',
  statLg: '22px',
  /** 价格 — product card price row */
  price: '15px',
  priceUnit: '10px',
  /** 超大标题 — Hero main title */
  hero: '38px',
  /** 侧边栏区块标题 */
  sidebarSection: '10px',
  /** 筛选标签字号 */
  filterChip: '11px',
  /** 徽章字号 */
  badge: '9px',
} as const;

/** Font weight scale */
export const fontWeight = {
  normal: '400',
  medium: '500',
} as const;

/** Line height scale */
export const lineHeight = {
  /** 正文默认 — ui-design §3 */
  body: '1.8',
  /** 规格说明 — product card spec text */
  caption: '1.5',
  /** 紧凑 — labels, badges */
  tight: '1.2',
  /** 标题 — page/hero headings */
  heading: '1.3',
  none: '1',
} as const;

/** Letter spacing — tracking scale */
export const letterSpacing = {
  /** 普通正文 */
  normal: '0',
  /** 徽章 — ui-design §8 */
  badge: '0.04em',
  /** 区块标签 / 侧边栏标题 — ui-design §3 */
  section: '0.12em',
  /** Logo / 品牌名 */
  brand: '0.16em',
  /** 眉标 eyebrow */
  eyebrow: '0.18em',
} as const;

/** CSS custom property names */
export const typographyCssVariables = {
  fontBrand: '--font-brand',
  trackingBrand: '--tracking-brand',
} as const;

/** Tailwind semantic utility class names */
export const typographyTailwindClasses = {
  fontBrand: 'font-brand',
  trackingBrand: 'tracking-brand',
  trackingSection: 'tracking-[0.12em]',
  trackingEyebrow: 'tracking-[0.18em]',
  trackingBadge: 'tracking-[0.04em]',
  textHero: 'text-[38px]',
  textPageTitle: 'text-[22px]',
  textBody: 'text-[13px]',
  textCaption: 'text-[11px]',
  textLabel: 'text-[9px]',
  leadingBody: 'leading-[1.8]',
  leadingCaption: 'leading-[1.5]',
} as const;

/** Composite typography presets — use in components for consistency */
export const typographyPresets = {
  hero: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.hero,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.heading,
    letterSpacing: letterSpacing.normal,
  },
  pageTitle: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.pageTitle,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.heading,
    letterSpacing: letterSpacing.normal,
  },
  cardTitle: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.cardTitle,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.heading,
    letterSpacing: letterSpacing.normal,
  },
  heading: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.headingSm,
    fontWeight: fontWeight.medium,
    lineHeight: lineHeight.heading,
    letterSpacing: letterSpacing.normal,
  },
  body: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.body,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.body,
    letterSpacing: letterSpacing.normal,
  },
  caption: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.caption,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.caption,
    letterSpacing: letterSpacing.normal,
  },
  eyebrow: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.labelMd,
    fontWeight: fontWeight.medium,
    lineHeight: lineHeight.tight,
    letterSpacing: letterSpacing.eyebrow,
  },
  brandLogo: {
    fontFamily: fontFamily.brand,
    fontSize: fontSize.pageTitle,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.none,
    letterSpacing: letterSpacing.brand,
  },
  badge: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.badge,
    fontWeight: fontWeight.medium,
    lineHeight: lineHeight.tight,
    letterSpacing: letterSpacing.badge,
  },
  stat: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.statLg,
    fontWeight: fontWeight.medium,
    lineHeight: lineHeight.none,
    letterSpacing: letterSpacing.normal,
  },
  price: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.price,
    fontWeight: fontWeight.medium,
    lineHeight: lineHeight.none,
    letterSpacing: letterSpacing.normal,
  },
} as const;

export type FontFamilyKey = keyof typeof fontFamily;
export type FontSizeKey = keyof typeof fontSize;
export type FontWeightKey = keyof typeof fontWeight;
export type LineHeightKey = keyof typeof lineHeight;
export type LetterSpacingKey = keyof typeof letterSpacing;
export type TypographyPresetKey = keyof typeof typographyPresets;

/** CSS properties object for inline styles or CSS-in-JS */
export type TypographyStyle = {
  fontFamily: string;
  fontSize: string;
  fontWeight: string;
  lineHeight: string;
  letterSpacing: string;
};

export function getTypographyPreset(
  preset: TypographyPresetKey,
): TypographyStyle {
  return typographyPresets[preset];
}
