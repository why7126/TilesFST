export const THEME_MODES = ['system', 'dark_flagship', 'comfort_dark', 'light'] as const;

export type ThemeMode = (typeof THEME_MODES)[number];

export const THEME_MODE_LABELS: Record<ThemeMode, string> = {
  system: '系统默认',
  dark_flagship: '暗色旗舰',
  comfort_dark: '舒适暗色',
  light: '浅色',
};

export const THEME_STORAGE_KEY = 'tilesfst.theme_mode';

export function isThemeMode(value: unknown): value is ThemeMode {
  return typeof value === 'string' && THEME_MODES.includes(value as ThemeMode);
}

export function normalizeThemeMode(value: unknown): ThemeMode {
  return isThemeMode(value) ? value : 'system';
}

export function resolveThemeMode(mode: ThemeMode, prefersLight: boolean): 'dark' | 'light' {
  if (mode === 'light') return 'light';
  if (mode === 'system') return prefersLight ? 'light' : 'dark';
  return 'dark';
}
