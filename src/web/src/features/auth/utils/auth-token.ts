const TOKEN_KEY = 'stonex_auth_token';
const REMEMBER_KEY = 'stonex_auth_remember';

export function getStoredToken(): string | null {
  return sessionStorage.getItem(TOKEN_KEY) ?? localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token: string, rememberMe: boolean): void {
  clearStoredToken();
  if (rememberMe) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(REMEMBER_KEY, '1');
  } else {
    sessionStorage.setItem(TOKEN_KEY, token);
    sessionStorage.removeItem(REMEMBER_KEY);
  }
}

export function clearStoredToken(): void {
  sessionStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REMEMBER_KEY);
}

export function isRememberMeEnabled(): boolean {
  return localStorage.getItem(REMEMBER_KEY) === '1';
}
