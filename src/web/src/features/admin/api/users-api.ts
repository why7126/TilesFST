import { api } from '@/features/auth/api/auth-api';
import type {
  ListUsersApiV1AdminUsersGetParams,
  UserAdminItem,
  UserCreateRequest,
  UserUpdateRequest,
} from '@/shared/api/generated';

export async function fetchUsers(params: ListUsersApiV1AdminUsersGetParams) {
  const response = await api.listUsersApiV1AdminUsersGet(params);
  return response.data.data!;
}

export async function createUser(payload: UserCreateRequest) {
  const response = await api.createUserApiV1AdminUsersPost(payload);
  return response.data.data!;
}

export async function updateUser(userId: string, payload: UserUpdateRequest) {
  const response = await api.updateUserApiV1AdminUsersUserIdPatch(userId, payload);
  return response.data.data!;
}

export async function resetUserPassword(userId: string) {
  const response = await api.resetPasswordApiV1AdminUsersUserIdResetPasswordPost(userId);
  return response.data.data!.password;
}

export async function updateUserStatus(userId: string, status: string) {
  const response = await api.updateUserStatusApiV1AdminUsersUserIdStatusPatch(userId, {
    status,
  });
  return response.data.data!;
}

export async function uploadAvatar(file: File) {
  const response = await api.uploadImageApiV1AdminUploadsPost({ file });
  return response.data.data!;
}

export type { UserAdminItem };
