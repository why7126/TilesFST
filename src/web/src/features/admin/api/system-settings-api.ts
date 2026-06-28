import { api } from '@/features/auth/api/auth-api';
import type {
  SystemSettingsAuditItem,
  SystemSettingsGroupResponseData,
} from '@/shared/api/generated';

export type SettingsGroup = 'basic' | 'security' | 'media' | 'notification' | 'audit';

export type { SystemSettingsAuditItem };

export async function fetchSettingsGroup(group: SettingsGroup): Promise<SystemSettingsGroupResponseData> {
  const response = await api.getSettingsGroupApiV1AdminSystemSettingsGroupGet(group);
  return response.data.data?.data ?? {};
}

export async function patchSettingsGroup(
  group: SettingsGroup,
  payload: Record<string, unknown>,
): Promise<SystemSettingsGroupResponseData> {
  const response = await api.patchSettingsGroupApiV1AdminSystemSettingsGroupPatch(group, payload);
  return response.data.data?.data ?? {};
}

export async function resetSettingsGroup(group: SettingsGroup): Promise<SystemSettingsGroupResponseData> {
  const response = await api.resetSettingsGroupApiV1AdminSystemSettingsGroupResetPost(group);
  return response.data.data?.data ?? {};
}

export async function fetchRecentAudit(limit = 10): Promise<SystemSettingsAuditItem[]> {
  const response = await api.getRecentAuditApiV1AdminSystemSettingsAuditRecentGet({ limit });
  return response.data.data?.items ?? [];
}
