export type { LoginData, LoginRequest, UserProfile } from '../../../shared/api/generated';

export interface AuthState {
  user: import('../../../shared/api/generated').UserProfile | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface AuthErrorPayload {
  code?: number;
  message?: string;
}
