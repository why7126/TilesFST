import { useAuthStore } from '../store/auth-store';

export function useAuth() {
  const user = useAuthStore((state) => state.user);
  const token = useAuthStore((state) => state.token);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isLoading = useAuthStore((state) => state.isLoading);
  const error = useAuthStore((state) => state.error);
  const login = useAuthStore((state) => state.login);
  const logout = useAuthStore((state) => state.logout);
  const restoreSession = useAuthStore((state) => state.restoreSession);
  const clearError = useAuthStore((state) => state.clearError);

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    restoreSession,
    clearError,
    isAdmin: user?.role === 'admin',
  };
}
