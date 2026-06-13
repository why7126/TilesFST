import { describe, expect, it } from 'vitest';

import { clearStoredToken, getStoredToken, setStoredToken } from '../utils/auth-token';

describe('auth-token', () => {
  it('persists token in sessionStorage by default', () => {
    clearStoredToken();
    setStoredToken('session-token', false);
    expect(getStoredToken()).toBe('session-token');
    expect(localStorage.getItem('stonex_auth_token')).toBeNull();
  });

  it('persists token in localStorage when remember me is enabled', () => {
    clearStoredToken();
    setStoredToken('remember-token', true);
    expect(getStoredToken()).toBe('remember-token');
    expect(localStorage.getItem('stonex_auth_token')).toBe('remember-token');
  });
});
