import { api } from '@/features/auth/api/auth-api';
import type { ListTopicsApiV1AdminTopicsGetParams } from '@/shared/api/generated';

export async function fetchTopics(params?: ListTopicsApiV1AdminTopicsGetParams) {
  const response = await api.listTopicsApiV1AdminTopicsGet(params);
  return response.data.data!;
}
