import axios from 'axios';
import { describe, expect, it } from 'vitest';

import {
  getEnvelopeErrorMessage,
  getEnvelopeFieldErrors,
  mapEnvelopeFieldErrors,
} from './error-envelope';

function createApiError(data: unknown) {
  return new axios.AxiosError(
    'Request failed',
    'ERR_BAD_REQUEST',
    undefined,
    undefined,
    {
      data,
      status: 422,
      statusText: 'Unprocessable Entity',
      headers: {},
      config: { headers: new axios.AxiosHeaders() },
    },
  );
}

describe('error envelope parser', () => {
  it('prefers unified envelope message for global feedback', () => {
    const error = createApiError({
      code: 40001,
      message: '请求参数无效',
      data: { errors: [] },
    });

    expect(getEnvelopeErrorMessage(error, '保存失败')).toBe('请求参数无效');
  });

  it('maps visible field errors and keeps unmapped errors for global fallback', () => {
    const error = createApiError({
      code: 40001,
      message: '请求参数无效',
      data: {
        errors: [
          { field: 'username', message: '用户名不能为空', type: 'missing', location: ['body', 'username'] },
          { field: 'query.status', message: '状态无效', type: 'enum', location: ['query', 'status'] },
        ],
      },
    });

    expect(getEnvelopeFieldErrors(error)).toHaveLength(2);
    expect(mapEnvelopeFieldErrors(error, ['username'])).toEqual({
      fieldErrors: { username: '用户名不能为空' },
      globalMessages: ['状态无效'],
    });
  });

  it('falls back safely when envelope field details are unavailable', () => {
    const error = createApiError({ detail: [{ msg: 'legacy detail' }] });

    expect(getEnvelopeErrorMessage(error, '保存失败')).toBe('保存失败');
    expect(mapEnvelopeFieldErrors(error, ['username'])).toEqual({
      fieldErrors: {},
      globalMessages: [],
    });
  });
});
