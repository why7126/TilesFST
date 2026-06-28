import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import '../styles/password-change-modal.css';

const changePasswordMock = vi.hoisted(() => vi.fn());

vi.mock('@/features/admin/api/password-change-api', () => ({
  changePassword: (...args: unknown[]) => changePasswordMock(...args),
}));

import { ChangePasswordModal, mapPasswordChangeApiError } from './ChangePasswordModal';

function renderModal(
  props: Partial<React.ComponentProps<typeof ChangePasswordModal>> = {},
) {
  const defaultProps = {
    open: true,
    displayName: '系统管理员',
    onClose: vi.fn(),
    onSuccess: vi.fn(),
  };
  return render(
    <div className="admin-shell">
      <ChangePasswordModal {...defaultProps} {...props} />
    </div>,
  );
}

function fieldContainer(inputId: string): Element | null {
  return document.getElementById(inputId)?.closest('.password-field') ?? null;
}

function createApiError(code: number, message: string) {
  return new axios.AxiosError(
    'Request failed',
    undefined,
    undefined,
    undefined,
    {
      status: code === 40020 ? 400 : 400,
      data: { code, message },
      statusText: 'Bad Request',
      headers: {},
      config: {} as never,
    },
  );
}

describe('ChangePasswordModal', () => {
  beforeEach(() => {
    changePasswordMock.mockReset();
    changePasswordMock.mockResolvedValue({ success: true });
    vi.spyOn(window, 'confirm');
  });

  it('renders modal fields when open', () => {
    renderModal();
    expect(screen.getByRole('dialog', { name: '修改密码' })).toBeInTheDocument();
    expect(screen.getByLabelText(/^原密码/)).toBeInTheDocument();
    expect(document.getElementById('pwd-new')).toBeInTheDocument();
    expect(screen.getByLabelText(/确认新密码/)).toBeInTheDocument();
  });

  it('shows client validation error under new password field', async () => {
    renderModal();
    fireEvent.change(screen.getByLabelText(/原密码/), { target: { value: 'OldPass123!' } });
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'short' } });
    fireEvent.change(screen.getByLabelText(/确认新密码/), { target: { value: 'short' } });
    fireEvent.click(screen.getByRole('button', { name: '保存修改' }));

    expect(await screen.findByText('新密码不符合安全策略')).toBeInTheDocument();
    expect(fieldContainer('pwd-new')?.querySelector('.error-text')).toHaveTextContent(
      '新密码不符合安全策略',
    );
    expect(fieldContainer('pwd-old')?.querySelector('.error-text')).toBeNull();
    expect(changePasswordMock).not.toHaveBeenCalled();
  });

  it('shows API weak password error under new password field', async () => {
    changePasswordMock.mockRejectedValue(createApiError(40022, '新密码过于常见'));
    renderModal();

    fireEvent.change(screen.getByLabelText(/原密码/), { target: { value: 'OldPass123!' } });
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'NewPass456!' } });
    fireEvent.change(screen.getByLabelText(/确认新密码/), {
      target: { value: 'NewPass456!' },
    });
    fireEvent.click(screen.getByRole('button', { name: '保存修改' }));

    expect(await screen.findByText('新密码过于常见')).toBeInTheDocument();
    expect(fieldContainer('pwd-new')?.querySelector('.error-text')).toHaveTextContent(
      '新密码过于常见',
    );
    expect(fieldContainer('pwd-old')?.querySelector('.error-text')).toBeNull();
  });

  it('shows wrong old password error under old password field', async () => {
    changePasswordMock.mockRejectedValue(createApiError(40020, '原密码错误'));
    renderModal();

    fireEvent.change(screen.getByLabelText(/原密码/), { target: { value: 'WrongPass123!' } });
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'NewPass456!' } });
    fireEvent.change(screen.getByLabelText(/确认新密码/), {
      target: { value: 'NewPass456!' },
    });
    fireEvent.click(screen.getByRole('button', { name: '保存修改' }));

    expect(await screen.findByText('原密码错误')).toBeInTheDocument();
    expect(fieldContainer('pwd-old')?.querySelector('.error-text')).toHaveTextContent('原密码错误');
    expect(fieldContainer('pwd-new')?.querySelector('.error-text')).toBeNull();
  });

  it('shows validation error when confirm password mismatches', async () => {
    renderModal();
    fireEvent.change(screen.getByLabelText(/原密码/), { target: { value: 'OldPass123!' } });
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'NewPass456!' } });
    fireEvent.change(screen.getByLabelText(/确认新密码/), {
      target: { value: 'Different789!' },
    });
    fireEvent.click(screen.getByRole('button', { name: '保存修改' }));

    expect(await screen.findByText('两次输入的新密码不一致')).toBeInTheDocument();
    expect(changePasswordMock).not.toHaveBeenCalled();
  });

  it('keeps toggle inside input wrap for confirm mismatch errors', async () => {
    renderModal();
    fireEvent.change(screen.getByLabelText(/确认新密码/), { target: { value: 'Mismatch123!' } });
    fireEvent.change(screen.getByLabelText(/原密码/), { target: { value: 'OldPass123!' } });
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'NewPass456!' } });
    fireEvent.click(screen.getByRole('button', { name: '保存修改' }));

    await screen.findByText('两次输入的新密码不一致');
    const confirmWrap = document.getElementById('pwd-confirm')?.closest('.password-input-wrap');
    expect(confirmWrap?.querySelector('.toggle-pass')).toBeTruthy();
    expect(confirmWrap?.querySelector('.error-text')).toBeNull();
  });

  it('closes immediately when form is dirty without browser confirm', () => {
    const onClose = vi.fn();
    renderModal({ onClose });
    fireEvent.change(screen.getByLabelText(/原密码/), { target: { value: 'OldPass123!' } });
    fireEvent.click(screen.getByRole('button', { name: '取消' }));

    expect(window.confirm).not.toHaveBeenCalled();
    expect(onClose).toHaveBeenCalled();
  });

  it('submits password change and triggers success callback', async () => {
    const onSuccess = vi.fn();
    const onClose = vi.fn();
    renderModal({ onSuccess, onClose });

    fireEvent.change(screen.getByLabelText(/原密码/), { target: { value: 'OldPass123!' } });
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'NewPass456!' } });
    fireEvent.change(screen.getByLabelText(/确认新密码/), {
      target: { value: 'NewPass456!' },
    });
    fireEvent.click(screen.getByRole('button', { name: '保存修改' }));

    await waitFor(() => {
      expect(changePasswordMock).toHaveBeenCalledWith('OldPass123!', 'NewPass456!');
    });
    expect(onSuccess).toHaveBeenCalled();
    expect(onClose).toHaveBeenCalled();
  });
});

describe('mapPasswordChangeApiError', () => {
  it('routes error codes to the correct field', () => {
    expect(mapPasswordChangeApiError(createApiError(40020, '原密码错误'))).toEqual({
      oldPasswordError: '原密码错误',
      newPasswordError: null,
    });
    expect(mapPasswordChangeApiError(createApiError(40022, '新密码过于常见'))).toEqual({
      oldPasswordError: null,
      newPasswordError: '新密码过于常见',
    });
  });
});
