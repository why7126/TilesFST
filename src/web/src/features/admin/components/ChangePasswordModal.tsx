import { useCallback, useEffect, useId, useMemo, useState } from 'react';
import axios from 'axios';

import { changePassword } from '@/features/admin/api/password-change-api';
import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { AuthErrorPayload } from '@/features/auth/types/auth.types';

import '../styles/password-change-modal.css';

interface ChangePasswordModalProps {
  open: boolean;
  displayName: string;
  onClose: () => void;
  onSuccess: () => void;
}

function PasswordField({
  id,
  label,
  value,
  onChange,
  placeholder,
  error,
  autoFocus,
}: {
  id: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
  error?: string | null;
  autoFocus?: boolean;
}) {
  const [visible, setVisible] = useState(false);

  return (
    <div className="form-row password-field">
      <label htmlFor={id}>
        <span className="field-label">
          {label} <span className="req-mark">*</span>
        </span>
        <div className="password-input-wrap">
          <input
            id={id}
            className={`input${error ? ' error' : ''}`}
            type={visible ? 'text' : 'password'}
            value={value}
            placeholder={placeholder}
            autoFocus={autoFocus}
            onChange={(event) => onChange(event.target.value)}
          />
          <button
            type="button"
            className="toggle-pass"
            onClick={() => setVisible((current) => !current)}
          >
            {visible ? '隐藏' : '显示'}
          </button>
        </div>
      </label>
      {error ? (
        <div className="error-text" role="alert">
          {error}
        </div>
      ) : null}
    </div>
  );
}

export function mapPasswordChangeApiError(error: unknown): {
  oldPasswordError: string | null;
  newPasswordError: string | null;
} {
  const fallback = getErrorMessage(error, '密码修改失败');
  if (!axios.isAxiosError(error)) {
    return { oldPasswordError: null, newPasswordError: fallback };
  }

  const payload = error.response?.data as AuthErrorPayload | undefined;
  const code = payload?.code;
  const message = payload?.message ?? fallback;

  if (code === 40020) {
    return { oldPasswordError: message, newPasswordError: null };
  }
  if (code === 30060 || code === 40021 || code === 40022 || code === 40023 || code === 42901) {
    return { oldPasswordError: null, newPasswordError: message };
  }

  return { oldPasswordError: null, newPasswordError: message };
}

export function ChangePasswordModal({
  open,
  displayName,
  onClose,
  onSuccess,
}: ChangePasswordModalProps) {
  const titleId = useId();
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [oldPasswordError, setOldPasswordError] = useState<string | null>(null);
  const [newPasswordError, setNewPasswordError] = useState<string | null>(null);
  const [confirmError, setConfirmError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) {
      return;
    }
    setOldPassword('');
    setNewPassword('');
    setConfirmPassword('');
    setOldPasswordError(null);
    setNewPasswordError(null);
    setConfirmError(null);
    setSubmitting(false);
  }, [open]);

  const rules = useMemo(
    () => ({
      length: newPassword.length >= 8 && newPassword.length <= 32,
      charset: /[A-Za-z]/.test(newPassword) && /\d/.test(newPassword),
      different: newPassword.length > 0 && newPassword !== oldPassword,
    }),
    [newPassword, oldPassword],
  );

  const requestClose = useCallback(() => {
    onClose();
  }, [onClose]);

  useEffect(() => {
    if (!open) {
      return;
    }
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        requestClose();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [open, requestClose]);

  const handleSubmit = async () => {
    setOldPasswordError(null);
    setNewPasswordError(null);
    setConfirmError(null);

    if (!rules.length || !rules.charset) {
      setNewPasswordError('新密码不符合安全策略');
      return;
    }
    if (!rules.different) {
      setNewPasswordError('新密码不能与原密码相同');
      return;
    }
    if (newPassword !== confirmPassword) {
      setConfirmError('两次输入的新密码不一致');
      return;
    }

    setSubmitting(true);
    try {
      await changePassword(oldPassword, newPassword);
      onSuccess();
      onClose();
    } catch (err) {
      const mapped = mapPasswordChangeApiError(err);
      setOldPasswordError(mapped.oldPasswordError);
      setNewPasswordError(mapped.newPasswordError);
    } finally {
      setSubmitting(false);
    }
  };

  if (!open) {
    return null;
  }

  return (
    <div className="password-modal-backdrop" role="presentation" onClick={requestClose}>
      <section
        className="modal-card password-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        onClick={(event) => event.stopPropagation()}
      >
        <header className="modal-head">
          <div className="modal-title-wrap">
            <div id={titleId} className="modal-title">
              修改密码
            </div>
            <p className="modal-subtitle">当前账号：{displayName}</p>
          </div>
          <button type="button" className="modal-close" aria-label="关闭" onClick={requestClose}>
            ×
          </button>
        </header>
        <div className="modal-body">
          <p className="password-intro">
            为了账号安全，建议使用 8 位以上并包含字母、数字的密码。修改成功后需要重新登录。
          </p>
          <PasswordField
            id="pwd-old"
            label="原密码"
            value={oldPassword}
            onChange={setOldPassword}
            placeholder="请输入当前登录密码"
            error={oldPasswordError}
            autoFocus
          />
          <PasswordField
            id="pwd-new"
            label="新密码"
            value={newPassword}
            onChange={setNewPassword}
            placeholder="请输入新密码"
            error={newPasswordError}
          />
          <div className="rule-list" aria-label="密码规则">
            <div className={`rule-item${rules.length ? ' ok' : ''}`}>
              <span className="rule-dot" />
              8-32 位字符
            </div>
            <div className={`rule-item${rules.charset ? ' ok' : ''}`}>
              <span className="rule-dot" />
              至少包含字母和数字
            </div>
            <div className={`rule-item${rules.different ? ' ok' : ''}`}>
              <span className="rule-dot" />
              不能与原密码相同
            </div>
          </div>
          <PasswordField
            id="pwd-confirm"
            label="确认新密码"
            value={confirmPassword}
            onChange={setConfirmPassword}
            placeholder="请再次输入新密码"
            error={confirmError}
          />
          <div className="security-tip">
            <span className="security-icon">!</span>
            <span>
              请勿与他人共享密码。保存成功后系统将清理当前登录态，并引导你使用新密码重新登录。
            </span>
          </div>
        </div>
        <footer className="modal-footer">
          <button type="button" className="btn" onClick={requestClose} disabled={submitting}>
            取消
          </button>
          <button
            type="button"
            className="btn primary"
            disabled={submitting}
            onClick={() => void handleSubmit()}
          >
            保存修改
          </button>
        </footer>
      </section>
    </div>
  );
}
