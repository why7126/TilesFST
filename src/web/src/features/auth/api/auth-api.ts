import axios, { type AxiosError } from 'axios';
import { getTilesFSTAPI } from '../../../shared/api/generated';
import { getEnvelopeErrorMessage } from '../../../shared/api/error-envelope';
import { clearStoredToken, getStoredToken } from '../utils/auth-token';

const CLIENT_REQUEST_ID_PREFIX = 'web';

export const apiClient = axios.create({
  baseURL: '',
});

apiClient.interceptors.request.use((config) => {
  const token = getStoredToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  config.headers['x-client-type'] = getWebClientType();
  const clientRequestId = createClientRequestId();
  if (clientRequestId) {
    config.headers['x-client-request-id'] = clientRequestId;
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

export const api = getTilesFSTAPI(apiClient);

export function getErrorMessage(error: unknown, fallback: string): string {
  return getEnvelopeErrorMessage(error, fallback);
}

export function handleUnauthorized(): void {
  clearStoredToken();
}

export function isUnauthorizedError(error: unknown): boolean {
  return axios.isAxiosError(error) && error.response?.status === 401;
}

export function getWebClientType(): 'web_admin' | 'web_catalog' {
  if (typeof window !== 'undefined' && window.location.pathname.startsWith('/admin')) {
    return 'web_admin';
  }
  return 'web_catalog';
}

export function createClientRequestId(): string | undefined {
  try {
    if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
      return `${CLIENT_REQUEST_ID_PREFIX}:${crypto.randomUUID()}`;
    }
    return `${CLIENT_REQUEST_ID_PREFIX}:${Date.now().toString(36)}:${Math.random().toString(36).slice(2, 10)}`;
  } catch {
    return undefined;
  }
}

export type { AxiosError };
