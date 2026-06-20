const STORAGE_KEY = 'stonex_login_credentials';

export interface StoredLoginCredentials {
  username: string;
  password: string;
  remember: true;
}

export function saveLoginCredentials(username: string, password: string): void {
  try {
    const payload: StoredLoginCredentials = {
      username,
      password,
      remember: true,
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  } catch {
    // localStorage unavailable — silent degrade
  }
}

export function loadLoginCredentials(): StoredLoginCredentials | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return null;
    }
    const parsed = JSON.parse(raw) as Partial<StoredLoginCredentials>;
    if (parsed.remember !== true || !parsed.username || !parsed.password) {
      clearLoginCredentials();
      return null;
    }
    return {
      username: parsed.username,
      password: parsed.password,
      remember: true,
    };
  } catch {
    clearLoginCredentials();
    return null;
  }
}

export function clearLoginCredentials(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // silent degrade
  }
}
