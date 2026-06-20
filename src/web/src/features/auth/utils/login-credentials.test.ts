import { afterEach, describe, expect, it } from 'vitest';

import {
  clearLoginCredentials,
  loadLoginCredentials,
  saveLoginCredentials,
} from './login-credentials';

describe('login-credentials', () => {
  afterEach(() => {
    clearLoginCredentials();
  });

  it('saves and loads credentials', () => {
    saveLoginCredentials('admin', 'secret');
    expect(loadLoginCredentials()).toEqual({
      username: 'admin',
      password: 'secret',
      remember: true,
    });
  });

  it('clears stored credentials', () => {
    saveLoginCredentials('admin', 'secret');
    clearLoginCredentials();
    expect(loadLoginCredentials()).toBeNull();
  });

  it('returns null and clears on corrupted JSON', () => {
    localStorage.setItem('stonex_login_credentials', '{bad json');
    expect(loadLoginCredentials()).toBeNull();
    expect(localStorage.getItem('stonex_login_credentials')).toBeNull();
  });

  it('returns null and clears when remember is not true', () => {
    localStorage.setItem(
      'stonex_login_credentials',
      JSON.stringify({ username: 'admin', password: 'secret', remember: false }),
    );
    expect(loadLoginCredentials()).toBeNull();
    expect(localStorage.getItem('stonex_login_credentials')).toBeNull();
  });
});
