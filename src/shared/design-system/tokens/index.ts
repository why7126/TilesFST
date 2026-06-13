/**
 * STONEX Design System — Token Entry
 * Source: rules/ui-design.md
 *
 * Cross-platform TypeScript tokens for Web (Tailwind v4) and future Miniapp.
 * CSS implementation: src/web/src/styles/globals.css
 */

export {
  type ThemeMode,
  type ColorTokens,
  colorCssVariables,
  colorTailwindClasses,
  darkColors,
  lightColors,
  colors,
  defaultThemeMode,
  getColorTokens,
  colorsToCssVariables,
} from './colors';

export {
  spacingScale,
  layoutSpacing,
  spacing,
  spacingTailwindClasses,
  type SpacingKey,
  type SpacingScaleKey,
  type LayoutSpacingKey,
} from './spacing';

export {
  radius,
  radiusCssVariables,
  radiusTailwindClasses,
  radiusToCssVariables,
  type RadiusKey,
  type RadiusToken,
} from './radius';

export {
  fontFamily,
  fontSize,
  fontWeight,
  lineHeight,
  letterSpacing,
  typographyCssVariables,
  typographyTailwindClasses,
  typographyPresets,
  getTypographyPreset,
  type FontFamilyKey,
  type FontSizeKey,
  type FontWeightKey,
  type LineHeightKey,
  type LetterSpacingKey,
  type TypographyPresetKey,
  type TypographyStyle,
} from './typography';

export {
  shadows,
  shadowThemes,
  shadowTailwindClasses,
  type ShadowKey,
  type ShadowToken,
} from './shadows';

export { generateTokensCss, getFontFamilyTokens } from './css';

export {
  cssVar,
  tailwindSemanticColors,
  tailwindSemanticTextUtilities,
  requiredSemanticClasses,
  default as tailwindConfig,
} from './tailwind.config';

import {
  colorsToCssVariables,
  defaultThemeMode,
  getColorTokens,
  type ThemeMode,
} from './colors';
import { layoutSpacing, spacing, spacingScale } from './spacing';
import { radius, radiusToCssVariables } from './radius';
import {
  fontFamily,
  fontSize,
  fontWeight,
  letterSpacing,
  lineHeight,
  typographyCssVariables,
  typographyPresets,
} from './typography';
import { shadowThemes } from './shadows';

/** Aggregate design tokens for runtime theming */
export interface DesignTokens {
  colors: ReturnType<typeof getColorTokens>;
  radius: typeof radius;
  spacing: typeof spacing;
  spacingScale: typeof spacingScale;
  layoutSpacing: typeof layoutSpacing;
  fontFamily: typeof fontFamily;
  fontSize: typeof fontSize;
  fontWeight: typeof fontWeight;
  lineHeight: typeof lineHeight;
  letterSpacing: typeof letterSpacing;
  typographyPresets: typeof typographyPresets;
  shadows: (typeof shadowThemes)[ThemeMode];
}

/** Resolve full token set for a theme mode */
export function getDesignTokens(mode: ThemeMode = defaultThemeMode): DesignTokens {
  return {
    colors: getColorTokens(mode),
    radius,
    spacing,
    spacingScale,
    layoutSpacing,
    fontFamily,
    fontSize,
    fontWeight,
    lineHeight,
    letterSpacing,
    typographyPresets,
    shadows: shadowThemes[mode],
  };
}

/** Apply theme CSS variables to a DOM element (Web) */
export function applyThemeToElement(
  element: HTMLElement,
  mode: ThemeMode = defaultThemeMode,
): void {
  const cssVars = {
    ...colorsToCssVariables(getColorTokens(mode)),
    ...radiusToCssVariables(),
    [typographyCssVariables.fontBrand]:
      "'Cormorant Garamond', ui-serif, Georgia, 'Times New Roman', serif",
    [typographyCssVariables.trackingBrand]: '0.16em',
  };

  for (const [key, value] of Object.entries(cssVars)) {
    element.style.setProperty(key, value);
  }

  element.dataset.theme = mode;
}

/** Tailwind @theme inline reference — document mapping for codegen */
export const tailwindThemeReference = {
  colors: {
    page: 'var(--color-page)',
    surface: 'var(--color-surface)',
    secondary: 'var(--color-secondary)',
    deep: 'var(--color-deep)',
    'brand-gold': 'var(--color-brand-gold)',
    'brand-gold-muted': 'var(--color-brand-gold-muted)',
    error: 'var(--color-error)',
    'border-default': 'var(--color-border-default)',
    'border-strong': 'var(--color-border-strong)',
    'border-hover': 'var(--color-border-hover)',
    'border-focus': 'var(--color-border-focus)',
  },
  radius: {
    industrial: 'var(--radius-industrial)',
    card: 'var(--radius-card)',
  },
  letterSpacing: {
    brand: 'var(--tracking-brand)',
  },
} as const;
