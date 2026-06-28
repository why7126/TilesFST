import { api } from '@/features/auth/api/auth-api';
import type {
  ProfileActivityItem,
  ProfileMe,
  ProfilePatchRequest,
} from '@/shared/api/generated';

export type { ProfileActivityItem, ProfileMe };

export async function fetchProfileMe(): Promise<ProfileMe> {
  const response = await api.getProfileMeApiV1ProfileMeGet();
  return response.data.data!;
}

export async function patchProfileMe(payload: ProfilePatchRequest): Promise<ProfileMe> {
  const response = await api.patchProfileMeApiV1ProfileMePatch(payload);
  return response.data.data!;
}

export async function fetchProfileActivities(): Promise<ProfileActivityItem[]> {
  const response = await api.getProfileActivitiesApiV1ProfileMeActivitiesGet();
  return response.data.data ?? [];
}

export { uploadAvatar, type UploadProgressHandler } from './users-api';
