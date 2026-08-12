export const THEME_MODES = ['system', 'dark_flagship'] as const;

export type ThemeMode = (typeof THEME_MODES)[number];

export const THEME_MODE_LABELS: Record<ThemeMode, string> = {
  system: '跟随系统',
  dark_flagship: '暗色旗舰',
};

export const THEME_STORAGE_KEY = 'tilesfst.theme_mode';

export function isThemeMode(value: unknown): value is ThemeMode {
  return typeof value === 'string' && THEME_MODES.includes(value as ThemeMode);
}

export function normalizeThemeMode(value: unknown): ThemeMode {
  if (value === 'light') return 'system';
  if (value === 'comfort_dark') return 'dark_flagship';
  return isThemeMode(value) ? value : 'system';
}

export function resolveThemeMode(mode: ThemeMode, prefersLight: boolean): 'dark' | 'light' {
  if (mode === 'system') return prefersLight ? 'light' : 'dark';
  return 'dark';
}
