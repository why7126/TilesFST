import { api } from '@/features/auth/api/auth-api';
import type {
  ListUsersApiV1AdminUsersGetParams,
  UserAdminItem,
  UserCreateRequest,
  UserUpdateRequest,
} from '@/shared/api/generated';

export type UploadProgressHandler = (progress: number) => void;

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

export async function uploadAvatar(file: File, onProgress?: UploadProgressHandler) {
  const response = await api.uploadImageApiV1AdminUploadsPost(
    { file },
    {
      onUploadProgress: (event) => {
        if (!onProgress) return;
        const total = event.total ?? 0;
        if (total <= 0) {
          onProgress(50);
          return;
        }
        onProgress(Math.min(99, Math.max(1, Math.round((event.loaded / total) * 100))));
      },
    },
  );
  return response.data.data!;
}

export type { UserAdminItem };
