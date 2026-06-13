/**
 * STONEX Design System — Color Tokens
 * Source: rules/ui-design.md §2 色彩系统
 *
 * Dark theme is the default product theme. Light theme values are reserved
 * for future extension — structure is stable, values may be filled later.
 */

export type ThemeMode = 'dark' | 'light';

/** Semantic color groups used across Web / Miniapp. */
export interface ColorTokens {
  background: {
    /** 页面底色 — global page background */
    page: string;
    /** 表面层 — cards, sidebar, search bar (semantic alias) */
    surface: string;
    /** 次级底色 — cards, sidebar, search box background */
    secondary: string;
    /** 页脚底色 — footer region */
    deep: string;
    /** 轻量浮层 — spec grid cells, hover fills */
    overlay: string;
    /** 徽章/标签弱底色 — "新品" badge */
    badgeNeutral: string;
  };
  text: {
    /** 主文字 — titles, important copy */
    primary: string;
    /** 次文字 — descriptions, subtitles */
    secondary: string;
    /** 弱文字 — labels, placeholders */
    muted: string;
    /** 极弱文字 — counts, tertiary annotations */
    subtle: string;
    /** 导航链接默认态 */
    navLink: string;
    /** 主 CTA / 品牌金文字 */
    brand: string;
    /** 热销语义文字 */
    hotSale: string;
    /** 深色文字 — on gold solid buttons */
    onBrand: string;
  };
  brand: {
    /** 品牌金 — price, primary CTA, active nav underline */
    gold: string;
    /** 金色背景 — badge, filter chip active */
    goldMuted: string;
    /** 金色边框 — inquiry button outline */
    goldBorder: string;
    /** 现货徽章底色 */
    goldBadge: string;
  };
  semantic: {
    /** 热销红 — "热销" badge text */
    hotSale: string;
    /** 热销红背景 */
    hotSaleMuted: string;
    /** 错误/危险 — aligned with hotSale in current palette */
    error: string;
  };
  border: {
    /** 默认分割线 — 0.5px dividers */
    default: string;
    /** 强调分割线 — search bar outer border */
    emphasis: string;
    /** 强边框 — inputs, icon buttons */
    strong: string;
    /** 悬停边框 */
    hover: string;
    /** 聚焦边框 — gold focus ring substitute */
    focus: string;
    /** 筛选标签默认描边 */
    chip: string;
    /** 品牌描边 — active filter chip */
    brand: string;
  };
  interactive: {
    /** 操作图标 hover 填充 */
    accent: string;
  };
}

/** CSS custom property names — colors in globals.css; names kept for TS/Tailwind bridge */
export const colorCssVariables = {
  background: {
    page: '--color-page',
    surface: '--color-surface',
    secondary: '--color-secondary',
    deep: '--color-deep',
    overlay: '--color-bg-overlay',
    badgeNeutral: '--color-bg-badge-neutral',
  },
  text: {
    primary: '--color-text-primary',
    secondary: '--color-text-secondary',
    muted: '--color-text-muted',
    subtle: '--color-text-subtle',
    navLink: '--color-text-nav-link',
    brand: '--color-text-brand',
    hotSale: '--color-text-hot-sale',
    onBrand: '--color-text-on-brand',
  },
  brand: {
    gold: '--color-brand-gold',
    goldMuted: '--color-brand-gold-muted',
    goldBorder: '--color-brand-gold-border',
    goldBadge: '--color-brand-gold-badge',
  },
  semantic: {
    error: '--color-error',
    hotSale: '--color-hot-sale',
    hotSaleMuted: '--color-hot-sale-muted',
  },
  border: {
    default: '--color-border-default',
    emphasis: '--color-border-emphasis',
    strong: '--color-border-strong',
    hover: '--color-border-hover',
    focus: '--color-border-focus',
    chip: '--color-border-chip',
    brand: '--color-border-brand',
  },
  interactive: {
    accent: '--color-accent-subtle',
  },
  shadcn: {
    background: '--background',
    foreground: '--foreground',
    card: '--card',
    cardForeground: '--card-foreground',
    primary: '--primary',
    primaryForeground: '--primary-foreground',
    secondary: '--secondary',
    secondaryForeground: '--secondary-foreground',
    muted: '--muted',
    mutedForeground: '--muted-foreground',
    accent: '--accent',
    accentForeground: '--accent-foreground',
    destructive: '--destructive',
    destructiveForeground: '--destructive-foreground',
    border: '--border',
    input: '--input',
    ring: '--ring',
  },
} as const;

/** Tailwind v4 semantic utility class names */
export const colorTailwindClasses = {
  background: {
    page: 'bg-page',
    surface: 'bg-surface',
    secondary: 'bg-secondary',
    deep: 'bg-deep',
    brandGold: 'bg-brand-gold',
    brandGoldMuted: 'bg-brand-gold-muted',
  },
  text: {
    primary: 'text-primary',
    secondary: 'text-secondary',
    muted: 'text-muted',
    brandGold: 'text-brand-gold',
    error: 'text-error',
    onPage: 'text-page',
  },
  border: {
    default: 'border-default',
    strong: 'border-strong',
    hover: 'border-hover',
    focus: 'border-focus',
    error: 'border-error',
  },
} as const;

/** Dark theme — current STONEX industrial flagship palette */
export const darkColors: ColorTokens = {
  background: {
    page: '#18160F',
    surface: '#211E16',
    secondary: '#211E16',
    deep: '#100F0A',
    overlay: 'rgba(255, 255, 255, 0.04)',
    badgeNeutral: 'rgba(255, 255, 255, 0.07)',
  },
  text: {
    primary: '#EDE8DF',
    secondary: 'rgba(237, 232, 223, 0.5)',
    muted: 'rgba(237, 232, 223, 0.3)',
    subtle: 'rgba(237, 232, 223, 0.25)',
    navLink: 'rgba(237, 232, 223, 0.45)',
    brand: '#C8A055',
    hotSale: '#E07050',
    onBrand: '#18160F',
  },
  brand: {
    gold: '#C8A055',
    goldMuted: 'rgba(200, 160, 85, 0.12)',
    goldBorder: 'rgba(200, 160, 85, 0.5)',
    goldBadge: 'rgba(200, 160, 85, 0.15)',
  },
  semantic: {
    hotSale: '#E07050',
    hotSaleMuted: 'rgba(196, 80, 50, 0.15)',
    error: '#E07050',
  },
  border: {
    default: 'rgba(255, 255, 255, 0.07)',
    emphasis: 'rgba(255, 255, 255, 0.1)',
    strong: 'rgba(255, 255, 255, 0.18)',
    hover: 'rgba(255, 255, 255, 0.28)',
    focus: 'rgba(200, 160, 85, 0.7)',
    chip: 'rgba(255, 255, 255, 0.12)',
    brand: 'rgba(200, 160, 85, 0.5)',
  },
  interactive: {
    accent: 'rgba(255, 255, 255, 0.05)',
  },
};

/**
 * Light theme placeholder — reserved for future extension.
 * Values intentionally mirror structure; replace when light spec is defined.
 */
export const lightColors: ColorTokens = {
  background: {
    page: '#F7F5F0',
    surface: '#FFFFFF',
    secondary: '#FFFFFF',
    deep: '#EDE8DF',
    overlay: 'rgba(24, 22, 15, 0.04)',
    badgeNeutral: 'rgba(24, 22, 15, 0.06)',
  },
  text: {
    primary: '#18160F',
    secondary: 'rgba(24, 22, 15, 0.65)',
    muted: 'rgba(24, 22, 15, 0.45)',
    subtle: 'rgba(24, 22, 15, 0.35)',
    navLink: 'rgba(24, 22, 15, 0.55)',
    brand: '#A8843F',
    hotSale: '#C45A3A',
    onBrand: '#18160F',
  },
  brand: {
    gold: '#A8843F',
    goldMuted: 'rgba(168, 132, 63, 0.12)',
    goldBorder: 'rgba(168, 132, 63, 0.45)',
    goldBadge: 'rgba(168, 132, 63, 0.15)',
  },
  semantic: {
    hotSale: '#C45A3A',
    hotSaleMuted: 'rgba(196, 90, 58, 0.12)',
    error: '#C45A3A',
  },
  border: {
    default: 'rgba(24, 22, 15, 0.08)',
    emphasis: 'rgba(24, 22, 15, 0.12)',
    strong: 'rgba(24, 22, 15, 0.18)',
    hover: 'rgba(24, 22, 15, 0.28)',
    focus: 'rgba(168, 132, 63, 0.65)',
    chip: 'rgba(24, 22, 15, 0.12)',
    brand: 'rgba(168, 132, 63, 0.45)',
  },
  interactive: {
    accent: 'rgba(24, 22, 15, 0.05)',
  },
};

export const colors = {
  dark: darkColors,
  light: lightColors,
} as const satisfies Record<ThemeMode, ColorTokens>;

/** Product default theme — STONEX is dark-first */
export const defaultThemeMode: ThemeMode = 'dark';

export function getColorTokens(mode: ThemeMode = defaultThemeMode): ColorTokens {
  return colors[mode];
}

/** Flatten semantic colors to CSS custom property record for runtime theming */
export function colorsToCssVariables(
  tokens: ColorTokens = getColorTokens(),
): Record<string, string> {
  return {
    [colorCssVariables.background.page]: tokens.background.page,
    [colorCssVariables.background.surface]: tokens.background.surface,
    [colorCssVariables.background.secondary]: tokens.background.secondary,
    [colorCssVariables.background.deep]: tokens.background.deep,
    [colorCssVariables.background.overlay]: tokens.background.overlay,
    [colorCssVariables.background.badgeNeutral]: tokens.background.badgeNeutral,
    [colorCssVariables.text.primary]: tokens.text.primary,
    [colorCssVariables.text.secondary]: tokens.text.secondary,
    [colorCssVariables.text.muted]: tokens.text.muted,
    [colorCssVariables.text.subtle]: tokens.text.subtle,
    [colorCssVariables.text.navLink]: tokens.text.navLink,
    [colorCssVariables.text.brand]: tokens.text.brand,
    [colorCssVariables.text.hotSale]: tokens.text.hotSale,
    [colorCssVariables.text.onBrand]: tokens.text.onBrand,
    [colorCssVariables.brand.gold]: tokens.brand.gold,
    [colorCssVariables.brand.goldMuted]: tokens.brand.goldMuted,
    [colorCssVariables.brand.goldBorder]: tokens.brand.goldBorder,
    [colorCssVariables.brand.goldBadge]: tokens.brand.goldBadge,
    [colorCssVariables.semantic.error]: tokens.semantic.error,
    [colorCssVariables.semantic.hotSale]: tokens.semantic.hotSale,
    [colorCssVariables.semantic.hotSaleMuted]: tokens.semantic.hotSaleMuted,
    [colorCssVariables.border.default]: tokens.border.default,
    [colorCssVariables.border.emphasis]: tokens.border.emphasis,
    [colorCssVariables.border.strong]: tokens.border.strong,
    [colorCssVariables.border.hover]: tokens.border.hover,
    [colorCssVariables.border.focus]: tokens.border.focus,
    [colorCssVariables.border.chip]: tokens.border.chip,
    [colorCssVariables.border.brand]: tokens.border.brand,
    [colorCssVariables.interactive.accent]: tokens.interactive.accent,
    [colorCssVariables.shadcn.background]: tokens.background.page,
    [colorCssVariables.shadcn.foreground]: tokens.text.primary,
    [colorCssVariables.shadcn.card]: tokens.background.secondary,
    [colorCssVariables.shadcn.cardForeground]: tokens.text.primary,
    [colorCssVariables.shadcn.primary]: tokens.brand.gold,
    [colorCssVariables.shadcn.primaryForeground]: tokens.text.onBrand,
    [colorCssVariables.shadcn.secondary]: tokens.background.secondary,
    [colorCssVariables.shadcn.secondaryForeground]: tokens.text.primary,
    [colorCssVariables.shadcn.muted]: tokens.background.secondary,
    [colorCssVariables.shadcn.mutedForeground]: tokens.text.secondary,
    [colorCssVariables.shadcn.accent]: tokens.interactive.accent,
    [colorCssVariables.shadcn.accentForeground]: tokens.text.primary,
    [colorCssVariables.shadcn.destructive]: tokens.semantic.error,
    [colorCssVariables.shadcn.destructiveForeground]: tokens.text.primary,
    [colorCssVariables.shadcn.border]: tokens.border.strong,
    [colorCssVariables.shadcn.input]: tokens.border.strong,
    [colorCssVariables.shadcn.ring]: tokens.border.focus,
  };
}
