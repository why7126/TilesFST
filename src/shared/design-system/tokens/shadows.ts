/**
 * STONEX Design System — Shadow Tokens
 * Source: rules/ui-design.md design principles + openspec design-system
 *
 * Industrial flagship aesthetic avoids heavy shadows and glow effects.
 * Focus states use border-focus, not box-shadow glow.
 * Tokens are defined for API completeness and future subtle elevation needs.
 */

export const shadows = {
  /** Default — no shadow (preferred for industrial UI) */
  none: 'none',
  /** Subtle inset — input/track backgrounds (price slider track feel) */
  insetSubtle: 'inset 0 1px 0 rgba(255, 255, 255, 0.03)',
  /** Minimal elevation — reserved for floating popovers if needed */
  sm: '0 1px 2px rgba(0, 0, 0, 0.24)',
  /** Card elevation — use sparingly; prefer border-default dividers */
  md: '0 2px 8px rgba(0, 0, 0, 0.32)',
  /** Focus ring substitute — prefer border-focus; shadow disabled by default */
  focus: 'none',
} as const;

/** Theme-aware shadow overrides for future light mode */
export const shadowThemes = {
  dark: {
    none: shadows.none,
    insetSubtle: shadows.insetSubtle,
    sm: shadows.sm,
    md: shadows.md,
    focus: shadows.focus,
  },
  light: {
    none: shadows.none,
    insetSubtle: 'inset 0 1px 0 rgba(24, 22, 15, 0.04)',
    sm: '0 1px 2px rgba(24, 22, 15, 0.08)',
    md: '0 2px 8px rgba(24, 22, 15, 0.12)',
    focus: shadows.focus,
  },
} as const;

/** Tailwind utility mappings — project prefers shadow-none in production */
export const shadowTailwindClasses = {
  none: 'shadow-none',
  sm: 'shadow-sm',
  md: 'shadow-md',
} as const;

export type ShadowKey = keyof typeof shadows;
export type ShadowToken = (typeof shadows)[ShadowKey];
