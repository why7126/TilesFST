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
  data?: {
    violations?: string[];
    policy?: Partial<{
      min_length: number;
      max_length: number;
      require_uppercase: boolean;
      require_lowercase: boolean;
      require_digit: boolean;
      require_special: boolean;
    }>;
  } | null;
}
