import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: vi.fn(),
}));

vi.mock('../api/users-api', () => ({
  createUser: vi.fn(),
  updateUser: vi.fn(),
  uploadAvatar: vi.fn(),
}));

import { UserFormModal } from './UserFormModal';

describe('UserFormModal', () => {
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
});
