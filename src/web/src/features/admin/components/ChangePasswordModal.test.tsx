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

function createApiError(code: number, message: string, data: Record<string, unknown> | null = null) {
  return new axios.AxiosError(
    'Request failed',
    undefined,
    undefined,
    undefined,
    {
      status: code === 30060 ? 403 : 400,
      data: { code, message, data },
      statusText: code === 30060 ? 'Forbidden' : 'Bad Request',
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

    expect(await screen.findByText(/新密码需要包含数字/)).toBeInTheDocument();
    expect(fieldContainer('pwd-new')?.querySelector('.error-text')).toHaveTextContent(
      '新密码需要包含数字',
    );
    expect(fieldContainer('pwd-old')?.querySelector('.error-text')).toBeNull();
    expect(changePasswordMock).not.toHaveBeenCalled();
  });

  it('shows API weak password error under new password field', async () => {
    changePasswordMock.mockRejectedValue(createApiError(40022, '新密码过于常见'));
    renderModal();

    fireEvent.change(screen.getByLabelText(/原密码/), { target: { value: 'OldPass123!' } });
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'NewPass4567!' } });
    fireEvent.change(screen.getByLabelText(/确认新密码/), {
      target: { value: 'NewPass4567!' },
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
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'NewPass4567!' } });
    fireEvent.change(screen.getByLabelText(/确认新密码/), {
      target: { value: 'NewPass4567!' },
    });
    fireEvent.click(screen.getByRole('button', { name: '保存修改' }));

    expect(await screen.findByText('原密码错误')).toBeInTheDocument();
    expect(fieldContainer('pwd-old')?.querySelector('.error-text')).toHaveTextContent('原密码错误');
    expect(fieldContainer('pwd-new')?.querySelector('.error-text')).toBeNull();
  });

  it('shows protected account API message under new password field', async () => {
    changePasswordMock.mockRejectedValue(
      createApiError(30060, '系统保底管理员账号不允许执行该操作'),
    );
    renderModal();

    fireEvent.change(screen.getByLabelText(/原密码/), { target: { value: 'OldPass123!' } });
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'NewPass4567!' } });
    fireEvent.change(screen.getByLabelText(/确认新密码/), {
      target: { value: 'NewPass4567!' },
    });
    fireEvent.click(screen.getByRole('button', { name: '保存修改' }));

    expect(await screen.findByText('系统保底管理员账号不允许执行该操作')).toBeInTheDocument();
    expect(fieldContainer('pwd-new')?.querySelector('.error-text')).toHaveTextContent(
      '系统保底管理员账号不允许执行该操作',
    );
    expect(fieldContainer('pwd-old')?.querySelector('.error-text')).toBeNull();
  });

  it('shows validation error when confirm password mismatches', async () => {
    renderModal();
    fireEvent.change(screen.getByLabelText(/原密码/), { target: { value: 'OldPass123!' } });
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'NewPass4567!' } });
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
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'NewPass4567!' } });
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
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'NewPass4567!' } });
    fireEvent.change(screen.getByLabelText(/确认新密码/), {
      target: { value: 'NewPass4567!' },
    });
    fireEvent.click(screen.getByRole('button', { name: '保存修改' }));

    await waitFor(() => {
      expect(changePasswordMock).toHaveBeenCalledWith('OldPass123!', 'NewPass4567!');
    });
    expect(onSuccess).toHaveBeenCalled();
    expect(onClose).toHaveBeenCalled();
  });

  it('renders the simplified password policy rules without legacy complexity hints', () => {
    renderModal();
    expect(screen.getByText('密码至少需要 5 位')).toBeInTheDocument();
    expect(screen.getByText('密码至多 32 位')).toBeInTheDocument();
    expect(screen.getByText('密码需包含英文字符')).toBeInTheDocument();
    expect(screen.getByText('密码需包含数字')).toBeInTheDocument();
    expect(screen.queryByText('8-32 位字符')).not.toBeInTheDocument();
    expect(screen.queryByText(/大写字母/)).not.toBeInTheDocument();
    expect(screen.queryByText(/小写字母/)).not.toBeInTheDocument();
    expect(screen.queryByText(/特殊字符/)).not.toBeInTheDocument();
  });

  it('uses a single password-modal class to avoid modal-card width cascade', () => {
    renderModal();
    const dialog = screen.getByRole('dialog', { name: '修改密码' });
    expect(dialog).toHaveClass('password-modal');
    expect(dialog).not.toHaveClass('modal-card');
  });

  it('maps API policy violation details to concrete new-password messages', async () => {
    changePasswordMock.mockRejectedValue(
      createApiError(40021, '新密码不符合安全策略', {
        violations: ['missing_letter', 'missing_digit'],
        policy: {
          min_length: 5,
          max_length: 32,
          require_letter: true,
          require_digit: true,
        },
      }),
    );
    renderModal();

    fireEvent.change(screen.getByLabelText(/原密码/), { target: { value: 'OldPass123!' } });
    fireEvent.change(screen.getByLabelText(/^新密码/), { target: { value: 'NewPass4567!' } });
    fireEvent.change(screen.getByLabelText(/确认新密码/), {
      target: { value: 'NewPass4567!' },
    });
    fireEvent.click(screen.getByRole('button', { name: '保存修改' }));

    expect(await screen.findByText(/新密码需要包含英文字符/)).toBeInTheDocument();
    expect(fieldContainer('pwd-new')?.querySelector('.error-text')).toHaveTextContent(
      '新密码需要包含数字',
    );
    expect(fieldContainer('pwd-old')?.querySelector('.error-text')).toBeNull();
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
    expect(mapPasswordChangeApiError(createApiError(30060, '系统保底管理员账号不允许执行该操作'))).toEqual({
      oldPasswordError: null,
      newPasswordError: '系统保底管理员账号不允许执行该操作',
    });
    expect(
      mapPasswordChangeApiError(
        createApiError(40021, '新密码不符合安全策略', {
          violations: ['min_length', 'missing_digit'],
          policy: { min_length: 5, max_length: 32 },
        }),
      ),
    ).toEqual({
      oldPasswordError: null,
      newPasswordError: '新密码至少需要 5 位字符；新密码需要包含数字',
    });
  });
});
