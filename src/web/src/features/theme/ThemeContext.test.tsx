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

    fireEvent.change(screen.getByLabelText('界面主题'), {
      target: { value: 'comfort_dark' },
    });

    await waitFor(() => {
      expect(document.documentElement.dataset.themeMode).toBe('comfort_dark');
    });
    expect(document.documentElement.dataset.theme).toBe('dark');
    expect(localStorage.getItem(THEME_STORAGE_KEY)).toBe('comfort_dark');
    expect(updateThemePreference).not.toHaveBeenCalled();
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

    fireEvent.change(screen.getByLabelText('界面主题'), {
      target: { value: 'light' },
    });

    await waitFor(() => {
      expect(updateThemePreference).toHaveBeenCalledWith('light');
    });
    expect(document.documentElement.dataset.themeMode).toBe('light');
    expect(screen.getByText('主题已在本机生效，但账号偏好同步失败，请稍后重试。')).toBeInTheDocument();
  });
});

function ThemeErrorProbe() {
  const { error } = useTheme();
  return error ? <p>{error}</p> : null;
}
