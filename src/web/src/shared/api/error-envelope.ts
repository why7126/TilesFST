import axios from 'axios';

export type ApiFieldError = {
  field: string;
  message: string;
  type?: string;
  location?: string[];
};

type ApiErrorEnvelope = {
  message?: unknown;
  data?: {
    errors?: unknown;
  } | null;
  detail?: unknown;
};

function isFieldError(value: unknown): value is ApiFieldError {
  if (!value || typeof value !== 'object') {
    return false;
  }
  const candidate = value as Partial<ApiFieldError>;
  return typeof candidate.field === 'string' && typeof candidate.message === 'string';
}

export function getEnvelopeErrorMessage(error: unknown, fallback: string): string {
  if (!axios.isAxiosError(error)) {
    return fallback;
  }
  const payload = error.response?.data as ApiErrorEnvelope | undefined;
  if (typeof payload?.message === 'string' && payload.message.trim()) {
    return payload.message;
  }
  if (error.message === 'Network Error') {
    return '网络异常，请稍后重试';
  }
  return fallback;
}

export function getEnvelopeFieldErrors(error: unknown): ApiFieldError[] {
  if (!axios.isAxiosError(error)) {
    return [];
  }
  const payload = error.response?.data as ApiErrorEnvelope | undefined;
  const errors = payload?.data?.errors;
  if (!Array.isArray(errors)) {
    return [];
  }
  return errors.filter(isFieldError);
}

export function mapEnvelopeFieldErrors(
  error: unknown,
  visibleFields: readonly string[],
): { fieldErrors: Partial<Record<string, string>>; globalMessages: string[] } {
  const visible = new Set(visibleFields);
  const fieldErrors: Partial<Record<string, string>> = {};
  const globalMessages: string[] = [];

  for (const item of getEnvelopeFieldErrors(error)) {
    if (visible.has(item.field)) {
      fieldErrors[item.field] = item.message;
    } else {
      globalMessages.push(item.message);
    }
  }

  return { fieldErrors, globalMessages };
}
