import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { useAuthStore } from '@/features/auth/store/auth-store';
import type { UserProfile } from '@/shared/api/generated';

import { ThemeProvider, useTheme } from './ThemeContext';
import { ThemeSwitcher } from './ThemeSwitcher';
import { THEME_STORAGE_KEY } from './theme';
import { updateThemePreference } from './theme-api';

vi.mock('./theme-api', () => ({
  updateThemePreference: vi.fn(),
}));

const matchMediaMock = vi.fn().mockReturnValue({
  matches: false,
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
});

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: matchMediaMock,
});

function renderThemeSwitcher() {
  return render(
    <ThemeProvider>
      <ThemeSwitcher />
    </ThemeProvider>,
  );
}

function selectTheme(label: string, valueLabel: string) {
  fireEvent.click(screen.getByLabelText(label));
  fireEvent.click(screen.getByRole('option', { name: valueLabel }));
}

describe('ThemeProvider', () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.removeAttribute('data-theme-mode');
    document.documentElement.removeAttribute('data-theme');
    document.documentElement.className = '';
    useAuthStore.setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    });
    vi.mocked(updateThemePreference).mockReset();
    matchMediaMock.mockClear();
  });

  it('applies local theme mode and writes the first-paint storage key', async () => {
    renderThemeSwitcher();

    selectTheme('界面主题', '暗色旗舰');

    await waitFor(() => {
      expect(document.documentElement.dataset.themeMode).toBe('dark_flagship');
    });
    expect(document.documentElement.dataset.theme).toBe('dark');
    expect(localStorage.getItem(THEME_STORAGE_KEY)).toBe('dark_flagship');
    expect(updateThemePreference).not.toHaveBeenCalled();
  });

  it('normalizes historical local theme modes on initialization', async () => {
    localStorage.setItem(THEME_STORAGE_KEY, 'comfort_dark');

    renderThemeSwitcher();

    await waitFor(() => {
      expect(document.documentElement.dataset.themeMode).toBe('dark_flagship');
    });
    expect(document.documentElement.dataset.theme).toBe('dark');

    localStorage.setItem(THEME_STORAGE_KEY, 'light');
    renderThemeSwitcher();

    await waitFor(() => {
      expect(document.documentElement.dataset.themeMode).toBe('system');
    });
  });

  it('syncs authenticated account preference and keeps local theme active on failure', async () => {
    useAuthStore.setState({
      user: {
        id: '1',
        username: 'admin',
        display_name: 'Admin',
        role: 'admin',
        status: 'active',
        theme_mode: 'system',
      } satisfies UserProfile,
      token: 'token',
      isAuthenticated: true,
      isLoading: false,
      error: null,
    });
    vi.mocked(updateThemePreference).mockRejectedValueOnce(new Error('network'));
    render(
      <ThemeProvider>
        <ThemeSwitcher />
        <ThemeErrorProbe />
      </ThemeProvider>,
    );

    selectTheme('界面主题', '暗色旗舰');

    await waitFor(() => {
      expect(updateThemePreference).toHaveBeenCalledWith('dark_flagship');
    });
    expect(document.documentElement.dataset.themeMode).toBe('dark_flagship');
    expect(screen.getByText('主题已在本机生效，但账号偏好同步失败，请稍后重试。')).toBeInTheDocument();
  });
});

function ThemeErrorProbe() {
  const { error } = useTheme();
  return error ? <p>{error}</p> : null;
}
