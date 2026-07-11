import axios, { type AxiosError } from 'axios';
import { getTilesFSTAPI } from '../../../shared/api/generated';
import { getEnvelopeErrorMessage } from '../../../shared/api/error-envelope';
import { clearStoredToken, getStoredToken } from '../utils/auth-token';

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

export type { AxiosError };
