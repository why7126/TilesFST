import { api } from '@/features/auth/api/auth-api';
import type { ApiDocsData } from '@/shared/api/generated';

export async function fetchApiDocs(): Promise<ApiDocsData> {
  const response = await api.getApiDocsApiV1AdminApiDocsGet();
  if (!response.data.data) {
    throw new Error(response.data.message || '接口文档数据为空');
  }

  return response.data.data;
}
