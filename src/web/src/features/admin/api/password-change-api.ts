import { api } from '@/features/auth/api/auth-api';

export async function changePassword(oldPassword: string, newPassword: string) {
  const response = await api.changePasswordApiV1AdminProfilePasswordPost({
    old_password: oldPassword,
    new_password: newPassword,
  });
  return response.data.data!;
}
