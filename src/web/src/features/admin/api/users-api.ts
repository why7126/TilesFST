import { createImageUploadTask } from '@/features/media/media-upload-api';
import type { ImageTaskOptions } from '@/features/media/use-image-upload';
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

export async function uploadAvatar(file: File, onProgress?: UploadProgressHandler, options?: ImageTaskOptions) {
  const update = (value: import('@/features/media/media-upload-controller').UploadSnapshot) => {
    onProgress?.(value.progress); options?.onUpdate?.(value);
  };
  const task = options?.task ?? createImageUploadTask(file, undefined, update, async (signal, progress) => {
    const response = await api.uploadImageApiV1AdminUploadsPost({ file }, {
      signal, onUploadProgress: event => {
        if (event.total && event.total > 0) progress(Math.min(100, event.loaded / event.total * 100));
      },
    });
    return response.data.data!;
  }, 'avatar');
  task.setListener(update); options?.onTask?.(task);
  return task.run();
}

export type { UserAdminItem };
