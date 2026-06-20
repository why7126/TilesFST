import { create } from 'zustand';

import { api, getErrorMessage, handleUnauthorized, isUnauthorizedError } from '../api/auth-api';
import type { UserProfile } from '../types/auth.types';
import { clearStoredToken, getStoredToken, setStoredToken } from '../utils/auth-token';
import { clearLoginCredentials } from '../utils/login-credentials';

interface AuthStore {
  user: UserProfile | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (username: string, password: string, rememberMe: boolean) => Promise<void>;
  logout: () => Promise<void>;
  restoreSession: () => Promise<boolean>;
  clearError: () => void;
}

export const useAuthStore = create<AuthStore>((set, get) => ({
  user: null,
  token: getStoredToken(),
  isAuthenticated: false,
  isLoading: false,
  error: null,

  clearError: () => set({ error: null }),

  login: async (username, password, rememberMe) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.loginApiV1AuthLoginPost({
        username,
        password,
        remember_me: rememberMe,
      });
      const data = response.data.data;
      if (!data?.access_token || !data.user) {
        throw new Error('登录响应无效');
      }
      setStoredToken(data.access_token, rememberMe);
      set({
        user: data.user,
        token: data.access_token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      set({
        isLoading: false,
        error: getErrorMessage(error, '账号或密码错误'),
      });
      throw error;
    }
  },

  logout: async () => {
    try {
      if (get().token) {
        await api.logoutApiV1AuthLogoutPost();
      }
    } catch {
      // ignore logout API errors
    } finally {
      clearStoredToken();
      clearLoginCredentials();
      set({ user: null, token: null, isAuthenticated: false, error: null });
    }
  },

  restoreSession: async () => {
    const token = getStoredToken();
    if (!token) {
      set({ isAuthenticated: false, user: null, token: null });
      return false;
    }
    set({ isLoading: true, token });
    try {
      const response = await api.meApiV1AuthMeGet();
      const user = response.data.data;
      if (!user) {
        throw new Error('用户信息无效');
      }
      if (user.role === 'store_owner') {
        clearStoredToken();
        set({ user: null, token: null, isAuthenticated: false, isLoading: false });
        return false;
      }
      set({ user, token, isAuthenticated: true, isLoading: false });
      return true;
    } catch (error) {
      if (isUnauthorizedError(error)) {
        handleUnauthorized();
      }
      set({ user: null, token: null, isAuthenticated: false, isLoading: false });
      return false;
    }
  },
}));
