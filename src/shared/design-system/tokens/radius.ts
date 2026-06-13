/**
 * STONEX Design System — Radius Tokens
 * Source: rules/ui-design.md §4 圆角规范
 *
 * Industrial cut aesthetic — near-square corners (1–3px).
 */

export const radius = {
  /** 徽章 / Badge — square label */
  badge: '1px',
  /** 按钮、分页、材质色块、复选框 — industrial default */
  industrial: '2px',
  /** 徽章较大变体 / 筛选标签 */
  chip: '2px',
  /** 产品卡、搜索框 — card-level rounding */
  card: '3px',
  /** shadcn compatibility — maps to industrial */
  sm: '2px',
  /** shadcn compatibility — maps to industrial */
  md: '2px',
  /** shadcn compatibility — maps to card */
  lg: '3px',
  /** shadcn compatibility — maps to card */
  xl: '3px',
  /** 全圆 — reserved, avoid in production UI per design spec */
  full: '9999px',
  none: '0px',
} as const;

/** CSS custom property names — keep in sync with globals.css */
export const radiusCssVariables = {
  industrial: '--radius-industrial',
  card: '--radius-card',
  default: '--radius',
} as const;

/** Tailwind semantic utility class names */
export const radiusTailwindClasses = {
  industrial: 'rounded-industrial',
  card: 'rounded-card',
  badge: 'rounded-[1px]',
  chip: 'rounded-industrial',
  none: 'rounded-none',
} as const;

export type RadiusKey = keyof typeof radius;
export type RadiusToken = (typeof radius)[RadiusKey];

/** Flatten radius tokens to CSS custom property record */
export function radiusToCssVariables(
  tokens: typeof radius = radius,
): Record<string, string> {
  return {
    [radiusCssVariables.industrial]: tokens.industrial,
    [radiusCssVariables.card]: tokens.card,
    [radiusCssVariables.default]: tokens.industrial,
  };
}
