import { render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

const fetchUsersMock = vi.fn();

vi.mock('@/features/admin/api/users-api', () => ({
  fetchUsers: (...args: unknown[]) => fetchUsersMock(...args),
  resetUserPassword: vi.fn(),
  updateUserStatus: vi.fn(),
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
});
