import { createContext, type ReactNode, useContext, useEffect, useMemo, useState } from 'react';

import { useAuthStore } from '@/features/auth/store/auth-store';

import { updateThemePreference } from './theme-api';
import {
  normalizeThemeMode,
  resolveThemeMode,
  THEME_STORAGE_KEY,
  type ThemeMode,
} from './theme';

interface ThemeContextValue {
  mode: ThemeMode;
  resolvedMode: 'dark' | 'light';
  error: string | null;
  setMode: (mode: ThemeMode) => Promise<void>;
  clearError: () => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

function readStoredThemeMode(): ThemeMode {
  if (typeof window === 'undefined') return 'system';
  return normalizeThemeMode(window.localStorage.getItem(THEME_STORAGE_KEY));
}

function writeStoredThemeMode(mode: ThemeMode) {
  window.localStorage.setItem(THEME_STORAGE_KEY, mode);
}

function prefersLightMode(): boolean {
  return typeof window.matchMedia === 'function'
    ? window.matchMedia('(prefers-color-scheme: light)').matches
    : false;
}

function applyTheme(mode: ThemeMode, resolvedMode: 'dark' | 'light') {
  const root = document.documentElement;
  root.dataset.themeMode = mode;
  root.dataset.theme = resolvedMode;
  root.classList.toggle('light', resolvedMode === 'light');
  root.classList.toggle('dark', resolvedMode === 'dark');
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const user = useAuthStore((state) => state.user);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const setUserThemeMode = useAuthStore((state) => state.setUserThemeMode);
  const [mode, setModeState] = useState<ThemeMode>(() => readStoredThemeMode());
  const [prefersLight, setPrefersLight] = useState(() => prefersLightMode());
  const [error, setError] = useState<string | null>(null);
  const resolvedMode = resolveThemeMode(mode, prefersLight);

  useEffect(() => {
    applyTheme(mode, resolvedMode);
  }, [mode, resolvedMode]);

  useEffect(() => {
    if (typeof window.matchMedia !== 'function') {
      return undefined;
    }
    const media = window.matchMedia('(prefers-color-scheme: light)');
    const onChange = () => setPrefersLight(media.matches);
    media.addEventListener('change', onChange);
    return () => media.removeEventListener('change', onChange);
  }, []);

  useEffect(() => {
    const accountMode = normalizeThemeMode(user?.theme_mode);
    if (!isAuthenticated || accountMode === mode) {
      return;
    }
    setModeState(accountMode);
    writeStoredThemeMode(accountMode);
  }, [isAuthenticated, mode, user?.theme_mode]);

  const value = useMemo<ThemeContextValue>(
    () => ({
      mode,
      resolvedMode,
      error,
      clearError: () => setError(null),
      setMode: async (nextMode: ThemeMode) => {
        setModeState(nextMode);
        writeStoredThemeMode(nextMode);
        setError(null);

        if (!isAuthenticated) {
          return;
        }

        setUserThemeMode(nextMode);
        try {
          const updatedUser = await updateThemePreference(nextMode);
          setUserThemeMode(normalizeThemeMode(updatedUser.theme_mode));
        } catch {
          setError('主题已在本机生效，但账号偏好同步失败，请稍后重试。');
        }
      },
    }),
    [error, isAuthenticated, mode, resolvedMode, setUserThemeMode],
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const value = useContext(ThemeContext);
  if (!value) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return value;
}
