/**
 * STONEX Design System — Tailwind Config
 * Source: rules/ui-design.md + src/shared/design-system/tokens/*
 *
 * All theme values reference CSS custom properties — no Hex literals.
 * Runtime values come from tokens.generated.css (sync:tokens).
 */

import type { Config } from 'tailwindcss';
import plugin from 'tailwindcss/plugin';
import { colorCssVariables } from './colors';
import { radiusCssVariables } from './radius';
import { typographyCssVariables } from './typography';

/** Resolve a CSS custom property name to a Tailwind theme value */
export function cssVar(customProperty: string): `var(${string})` {
  return `var(${customProperty})`;
}

/** Background / border semantic colors → bg-*, border-* utilities */
export const tailwindSemanticColors = {
  page: cssVar(colorCssVariables.background.page),
  surface: cssVar(colorCssVariables.background.surface),
  secondary: cssVar(colorCssVariables.background.secondary),
  deep: cssVar(colorCssVariables.background.deep),
  overlay: cssVar(colorCssVariables.background.overlay),
  'brand-gold': cssVar(colorCssVariables.brand.gold),
  'brand-gold-muted': cssVar(colorCssVariables.brand.goldMuted),
  error: cssVar(colorCssVariables.semantic.error),
  'hot-sale': cssVar(colorCssVariables.semantic.hotSale),
  'border-default': cssVar(colorCssVariables.border.default),
  'border-emphasis': cssVar(colorCssVariables.border.emphasis),
  'border-strong': cssVar(colorCssVariables.border.strong),
  'border-hover': cssVar(colorCssVariables.border.hover),
  'border-focus': cssVar(colorCssVariables.border.focus),
  'border-chip': cssVar(colorCssVariables.border.chip),
  'border-brand': cssVar(colorCssVariables.border.brand),
} as const;

/** Text semantic utilities — registered via plugin to avoid shadcn `primary` conflict */
export const tailwindSemanticTextUtilities = {
  '.text-primary': { color: cssVar(colorCssVariables.text.primary) },
  '.text-secondary': { color: cssVar(colorCssVariables.text.secondary) },
  '.text-brand-gold': { color: cssVar(colorCssVariables.brand.gold) },
  '.text-muted': { color: cssVar(colorCssVariables.text.muted) },
  '.text-subtle': { color: cssVar(colorCssVariables.text.subtle) },
} as const;

/** Required semantic token class names (acceptance checklist) */
export const requiredSemanticClasses = [
  'bg-page',
  'bg-surface',
  'text-primary',
  'text-secondary',
  'text-brand-gold',
] as const;

const config = {
  theme: {
    extend: {
      colors: tailwindSemanticColors,
      borderRadius: {
        industrial: cssVar(radiusCssVariables.industrial),
        card: cssVar(radiusCssVariables.card),
        badge: cssVar('--radius-badge'),
        chip: cssVar('--radius-chip'),
      },
      fontFamily: {
        brand: cssVar(typographyCssVariables.fontBrand),
      },
      letterSpacing: {
        brand: cssVar(typographyCssVariables.trackingBrand),
        section: cssVar('--tracking-section'),
        eyebrow: cssVar('--tracking-eyebrow'),
        badge: cssVar('--tracking-badge'),
      },
    },
  },
  plugins: [
    plugin(({ addUtilities }) => {
      addUtilities(tailwindSemanticTextUtilities);
    }),
  ],
} satisfies Config;

export default config;
