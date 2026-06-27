import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

const fetchUsersMock = vi.fn();
const updateUserStatusMock = vi.fn();
const resetUserPasswordMock = vi.fn();

vi.mock('@/features/admin/api/users-api', () => ({
  fetchUsers: (...args: unknown[]) => fetchUsersMock(...args),
  resetUserPassword: (...args: unknown[]) => resetUserPasswordMock(...args),
  updateUserStatus: (...args: unknown[]) => updateUserStatusMock(...args),
}));

vi.mock('@/features/admin/components/UserFormModal', () => ({
  UserFormModal: () => null,
}));

vi.mock('@/features/admin/components/ResetPasswordDialog', () => ({
  ResetPasswordDialog: () => null,
}));

import { UserManagementPage } from './UserManagementPage';

const listPayload = {
  items: [
    {
      id: 'u1',
      username: 'demo_user',
      display_name: '',
      email: 'hidden@example.com',
      role: 'employee',
      status: 'active',
      last_login_at: null,
      created_at: '2026-06-01T00:00:00Z',
    },
  ],
  total: 1,
  page: 1,
  page_size: 10,
  summary: {
    total: 1,
    filtered: 1,
    active_count: 1,
    disabled_count: 0,
  },
};

describe('UserManagementPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders v2 list layout without search button or legacy toolbar copy', async () => {
    fetchUsersMock.mockResolvedValue(listPayload);

    render(<UserManagementPage />);

    await waitFor(() => {
      expect(fetchUsersMock).toHaveBeenCalled();
    });

    expect(screen.queryByRole('button', { name: '搜索' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: '重置' })).toBeInTheDocument();
    expect(screen.getByPlaceholderText('搜索用户名/昵称')).toBeInTheDocument();
    expect(screen.queryByText('用户列表')).not.toBeInTheDocument();
    expect(screen.queryByText(/当前显示/)).not.toBeInTheDocument();
    expect(screen.queryByText(/仅后台管理员可编辑用户/)).not.toBeInTheDocument();
    expect(screen.getByText('共 1 个用户')).toBeInTheDocument();
    expect(screen.getByText('每页显示')).toBeInTheDocument();
    expect(screen.getByText('demo_user')).toBeInTheDocument();
    expect(screen.getByText('未设置昵称')).toBeInTheDocument();
    expect(screen.queryByText('hidden@example.com')).not.toBeInTheDocument();
  });

  it('renders avatar image when avatar_url is present', async () => {
    fetchUsersMock.mockResolvedValue({
      ...listPayload,
      items: [
        {
          ...listPayload.items[0],
          avatar_object_key: 'original/default/avatars/demo.webp',
          avatar_url: '/media/original/default/avatars/demo.webp',
        },
      ],
    });

    const { container } = render(<UserManagementPage />);

    await waitFor(() => {
      expect(fetchUsersMock).toHaveBeenCalled();
    });

    const img = container.querySelector('.avatar img') as HTMLImageElement | null;
    expect(img?.getAttribute('src')).toBe('/media/original/default/avatars/demo.webp');
    expect(container.querySelector('.avatar-fallback')).toBeInTheDocument();
  });

  it('opens freeze confirm dialog before calling updateUserStatus', async () => {
    updateUserStatusMock.mockResolvedValue(undefined);
    fetchUsersMock.mockResolvedValue(listPayload);

    const { container } = render(<UserManagementPage />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '冻结' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '冻结' }));

    const dialog = screen.getByRole('dialog');
    expect(within(dialog).getByText('冻结用户')).toBeInTheDocument();
    expect(
      within(dialog).getByText('确认冻结用户「demo_user」？冻结后该用户将无法登录。'),
    ).toBeInTheDocument();
    expect(updateUserStatusMock).not.toHaveBeenCalled();

    fireEvent.click(within(dialog).getByRole('button', { name: '确认冻结' }));

    await waitFor(() => {
      expect(updateUserStatusMock).toHaveBeenCalledWith('u1', 'disabled');
    });

    expect(container.querySelector('.admin-toast-region')).toBeInTheDocument();
    expect(container.querySelector('.admin-toast')).toHaveTextContent('用户已冻结');
    expect(container.querySelector('.admin-notice')).not.toBeInTheDocument();
  });

  it('does not call updateUserStatus when freeze confirm is cancelled', async () => {
    fetchUsersMock.mockResolvedValue(listPayload);

    render(<UserManagementPage />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '冻结' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '冻结' }));

    const dialog = screen.getByRole('dialog');
    fireEvent.click(within(dialog).getByRole('button', { name: '取消' }));

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
    expect(updateUserStatusMock).not.toHaveBeenCalled();
  });

  it('opens delete confirm modal instead of window.confirm', async () => {
    updateUserStatusMock.mockResolvedValue(undefined);
    fetchUsersMock.mockResolvedValue(listPayload);
    const confirmSpy = vi.spyOn(window, 'confirm');

    render(<UserManagementPage />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '删除' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '删除' }));

    const dialog = screen.getByRole('dialog');
    expect(within(dialog).getByText('删除用户', { selector: '.modal-title' })).toBeInTheDocument();
    expect(confirmSpy).not.toHaveBeenCalled();
    expect(updateUserStatusMock).not.toHaveBeenCalled();

    fireEvent.click(within(dialog).getByRole('button', { name: '删除用户' }));

    await waitFor(() => {
      expect(updateUserStatusMock).toHaveBeenCalledWith('u1', 'deleted');
    });

    confirmSpy.mockRestore();
  });

  it('opens reset password confirm dialog before calling resetUserPassword', async () => {
    resetUserPasswordMock.mockResolvedValue('NewPass123!');
    fetchUsersMock.mockResolvedValue(listPayload);
    const confirmSpy = vi.spyOn(window, 'confirm');

    const { container } = render(<UserManagementPage />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '重置密码' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '重置密码' }));

    const dialog = screen.getByRole('dialog');
    expect(within(dialog).getByText('重置密码', { selector: '.modal-title' })).toBeInTheDocument();
    expect(
      within(dialog).getByText(
        '确认为用户「demo_user」重置密码？重置后将生成新随机密码。',
      ),
    ).toBeInTheDocument();
    expect(confirmSpy).not.toHaveBeenCalled();
    expect(resetUserPasswordMock).not.toHaveBeenCalled();

    fireEvent.click(within(dialog).getByRole('button', { name: '确认重置' }));

    await waitFor(() => {
      expect(resetUserPasswordMock).toHaveBeenCalledWith('u1');
    });

    expect(container.querySelector('.admin-toast')).toHaveTextContent('密码已重置');
    confirmSpy.mockRestore();
  });

  it('does not call resetUserPassword when reset confirm is cancelled', async () => {
    fetchUsersMock.mockResolvedValue(listPayload);
    const confirmSpy = vi.spyOn(window, 'confirm');

    render(<UserManagementPage />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '重置密码' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '重置密码' }));

    const dialog = screen.getByRole('dialog');
    fireEvent.click(within(dialog).getByRole('button', { name: '取消' }));

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
    expect(resetUserPasswordMock).not.toHaveBeenCalled();
    expect(confirmSpy).not.toHaveBeenCalled();
    confirmSpy.mockRestore();
  });
});
