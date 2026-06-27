import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const createUserMock = vi.hoisted(() => vi.fn());
const updateUserMock = vi.hoisted(() => vi.fn());
const uploadAvatarMock = vi.hoisted(() => vi.fn());

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

vi.mock('../api/users-api', () => ({
  createUser: (...args: unknown[]) => createUserMock(...args),
  updateUser: (...args: unknown[]) => updateUserMock(...args),
  uploadAvatar: (...args: unknown[]) => uploadAvatarMock(...args),
}));

import { UserFormModal } from './UserFormModal';

describe('UserFormModal', () => {
  beforeEach(() => {
    createUserMock.mockReset();
    updateUserMock.mockReset();
    uploadAvatarMock.mockReset();
  });

  it('renders fields in fixed order for create mode', () => {
    render(
      <UserFormModal
        open
        mode="create"
        user={null}
        onClose={vi.fn()}
        onSuccess={vi.fn()}
      />,
    );

    expect(screen.getByText('用户名', { selector: '.field-label' })).toBeInTheDocument();
    expect(screen.getByText('头像', { selector: '.field-label' })).toBeInTheDocument();
    expect(screen.getByText('昵称', { selector: '.field-label' })).toBeInTheDocument();
    expect(screen.getByText('角色', { selector: '.field-label' })).toBeInTheDocument();
    expect(screen.getByLabelText('用户名')).toBeInTheDocument();
  });

  it('uploads avatar with progress and updates preview on create', async () => {
    uploadAvatarMock.mockResolvedValue({
      object_key: 'original/default/avatars/demo.webp',
      url: '/media/original/default/avatars/demo.webp',
    });
    createUserMock.mockResolvedValue({ initial_password: 'TempPass123!' });

    const onSuccess = vi.fn();
    const { container } = render(
      <UserFormModal
        open
        mode="create"
        user={null}
        onClose={vi.fn()}
        onSuccess={onSuccess}
      />,
    );

    expect(container.querySelector('.brand-logo-upload')).toBeInTheDocument();
    expect(screen.getByText('默认头像')).toBeInTheDocument();

    const file = new File(['avatar'], 'avatar.webp', { type: 'image/webp' });
    fireEvent.change(screen.getByLabelText('更换头像'), { target: { files: [file] } });

    await waitFor(() => {
      expect(uploadAvatarMock).toHaveBeenCalledWith(file, expect.any(Function));
    });
    expect(await screen.findByText('已上传头像')).toBeInTheDocument();
    expect(screen.getByText('头像已更新')).toBeInTheDocument();
    expect(container.querySelector('.brand-logo-preview img')?.getAttribute('src')).toBe(
      '/media/original/default/avatars/demo.webp',
    );

    fireEvent.change(screen.getByLabelText('用户名'), { target: { value: 'new_user_01' } });
    fireEvent.click(screen.getByRole('button', { name: '创建用户' }));

    await waitFor(() => {
      expect(createUserMock).toHaveBeenCalledWith(
        expect.objectContaining({
          username: 'new_user_01',
          avatar_object_key: 'original/default/avatars/demo.webp',
        }),
      );
    });
  });

  it('previews existing avatar in edit mode and blocks save while uploading', async () => {
    uploadAvatarMock.mockImplementation(
      () =>
        new Promise(() => {
          /* pending */
        }),
    );

    const { container } = render(
      <UserFormModal
        open
        mode="edit"
        user={{
          id: 'u1',
          username: 'demo_user',
          display_name: '演示',
          role: 'employee',
          status: 'active',
          avatar_object_key: 'original/default/avatars/old.webp',
          avatar_url: '/media/original/default/avatars/old.webp',
          email: null,
          phone: null,
          last_login_at: null,
          created_at: '2026-06-01T00:00:00Z',
        }}
        onClose={vi.fn()}
        onSuccess={vi.fn()}
      />,
    );

    expect(container.querySelector('.brand-logo-preview img')?.getAttribute('src')).toBe(
      '/media/original/default/avatars/old.webp',
    );

    const file = new File(['avatar'], 'avatar.webp', { type: 'image/webp' });
    fireEvent.change(screen.getByLabelText('更换头像'), { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });
    expect(screen.getByRole('button', { name: '保存' })).toBeDisabled();
  });

  it('shows upload error and allows retry', async () => {
    uploadAvatarMock.mockRejectedValueOnce(new Error('network')).mockResolvedValueOnce({
      object_key: 'original/default/avatars/new.webp',
      url: '/media/original/default/avatars/new.webp',
    });

    render(
      <UserFormModal
        open
        mode="create"
        user={null}
        onClose={vi.fn()}
        onSuccess={vi.fn()}
      />,
    );

    const input = screen.getByLabelText('更换头像') as HTMLInputElement;
    fireEvent.change(input, { target: { files: [new File(['a'], 'a.webp', { type: 'image/webp' })] } });

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('头像上传失败');
    });

    fireEvent.change(input, { target: { files: [new File(['b'], 'b.webp', { type: 'image/webp' })] } });

    await waitFor(() => {
      expect(uploadAvatarMock).toHaveBeenCalledTimes(2);
    });
    expect(await screen.findByText('已上传头像')).toBeInTheDocument();
  });
});
