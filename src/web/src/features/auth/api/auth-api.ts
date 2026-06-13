import axios, { type AxiosError } from 'axios';
import { getApi } from '../../../shared/api/generated';
import { clearStoredToken, getStoredToken } from '../utils/auth-token';
import type { AuthErrorPayload } from '../types/auth.types';

export const apiClient = axios.create({
  baseURL: '',
});

apiClient.interceptors.request.use((config) => {
  const token = getStoredToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      handleUnauthorized();
    }
    return Promise.reject(error);
  },
);

export const api = getApi(apiClient);

export function getErrorMessage(error: unknown, fallback: string): string {
  if (axios.isAxiosError(error)) {
    const payload = error.response?.data as AuthErrorPayload | undefined;
    if (payload?.message) {
      return payload.message;
    }
    if (error.message === 'Network Error') {
      return '网络异常，请稍后重试';
    }
  }
  return fallback;
}

export function handleUnauthorized(): void {
  clearStoredToken();
}

export function isUnauthorizedError(error: unknown): boolean {
  return axios.isAxiosError(error) && error.response?.status === 401;
}

export type { AxiosError };
