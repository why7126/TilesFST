import type { UserProfile } from '@/shared/api/generated';
import { api } from '@/features/auth/api/auth-api';

import type { ThemeMode } from './theme';

export async function updateThemePreference(themeMode: ThemeMode): Promise<UserProfile> {
  const response = await api.updateThemePreferenceApiV1AuthMeThemePatch({
    theme_mode: themeMode,
  });
  if (!response.data.data) {
    throw new Error('主题偏好响应无效');
  }
  return response.data.data;
}
