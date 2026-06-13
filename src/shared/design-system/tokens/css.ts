/**
 * Generate CSS custom properties from TypeScript design tokens.
 * Colors: src/web/src/styles/globals.css (canonical Web CSS)
 * Other tokens: tokens.generated.css
 */

import { layoutSpacing, spacingScale } from './spacing';
import { radius, radiusToCssVariables } from './radius';
import {
  fontFamily,
  fontSize,
  fontWeight,
  letterSpacing,
  lineHeight,
  typographyCssVariables,
} from './typography';
import { shadowThemes } from './shadows';

function cssBlock(selector: string, vars: Record<string, string>): string {
  const lines = Object.entries(vars)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => `  ${key}: ${value};`);
  return `${selector} {\n${lines.join('\n')}\n}`;
}

function spacingToCssVariables(): Record<string, string> {
  const vars: Record<string, string> = {};
  for (const [key, value] of Object.entries(spacingScale)) {
    vars[`--spacing-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`] = value;
  }
  for (const [key, value] of Object.entries(layoutSpacing)) {
    vars[`--layout-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`] = value;
  }
  return vars;
}

function typographyToCssVariables(): Record<string, string> {
  const vars: Record<string, string> = {
    [typographyCssVariables.fontBrand]:
      "'Cormorant Garamond', ui-serif, Georgia, 'Times New Roman', serif",
    [typographyCssVariables.trackingBrand]: letterSpacing.brand,
    '--tracking-section': letterSpacing.section,
    '--tracking-eyebrow': letterSpacing.eyebrow,
    '--tracking-badge': letterSpacing.badge,
    '--font-weight-normal': fontWeight.normal,
    '--font-weight-medium': fontWeight.medium,
    '--line-height-body': lineHeight.body,
    '--line-height-caption': lineHeight.caption,
    '--line-height-heading': lineHeight.heading,
    '--line-height-tight': lineHeight.tight,
  };

  for (const [key, value] of Object.entries(fontSize)) {
    vars[`--font-size-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`] = value;
  }

  return vars;
}

function radiusExtendedToCssVariables(): Record<string, string> {
  return {
    ...radiusToCssVariables(),
    '--radius-badge': radius.badge,
    '--radius-chip': radius.chip,
  };
}

function nonColorTokens(): Record<string, string> {
  return {
    ...radiusExtendedToCssVariables(),
    ...spacingToCssVariables(),
    ...typographyToCssVariables(),
    ...shadowThemes.dark,
  };
}

const GENERATED_HEADER = `/**
 * AUTO-GENERATED — do not edit manually.
 * Source: src/shared/design-system/tokens/
 * Colors live in globals.css — regenerate: cd src/web && pnpm sync:tokens
 */`;

/** Generate spacing / radius / typography / shadow CSS variables */
export function generateTokensCss(): string {
  return [GENERATED_HEADER, '', cssBlock(':root', nonColorTokens()), ''].join('\n');
}

/** Resolve font stacks for documentation/codegen */
export function getFontFamilyTokens() {
  return fontFamily;
}
