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

interface PasswordPolicy {
  min_length: number;
  max_length: number;
  require_uppercase: boolean;
  require_lowercase: boolean;
  require_digit: boolean;
  require_special: boolean;
}

const DEFAULT_PASSWORD_POLICY: PasswordPolicy = {
  min_length: 12,
  max_length: 32,
  require_uppercase: true,
  require_lowercase: true,
  require_digit: true,
  require_special: true,
};

const POLICY_MESSAGES: Record<string, (policy: PasswordPolicy) => string> = {
  min_length: (policy) => `新密码至少需要 ${policy.min_length} 位字符`,
  max_length: (policy) => `新密码不能超过 ${policy.max_length} 位字符`,
  missing_uppercase: () => '新密码需要包含大写字母',
  missing_lowercase: () => '新密码需要包含小写字母',
  missing_digit: () => '新密码需要包含数字',
  missing_special: () => '新密码需要包含特殊字符',
  same_as_old: () => '新密码不能与原密码相同',
  weak: () => '新密码过于常见，请更换',
};

function normalizePasswordPolicy(policy?: Partial<PasswordPolicy>): PasswordPolicy {
  return {
    ...DEFAULT_PASSWORD_POLICY,
    ...(policy ?? {}),
  };
}

function collectPolicyViolations(
  newPassword: string,
  oldPassword: string,
  policy = DEFAULT_PASSWORD_POLICY,
): string[] {
  const violations: string[] = [];
  if (newPassword.length < policy.min_length) {
    violations.push('min_length');
  }
  if (newPassword.length > policy.max_length) {
    violations.push('max_length');
  }
  if (policy.require_uppercase && !/[A-Z]/.test(newPassword)) {
    violations.push('missing_uppercase');
  }
  if (policy.require_lowercase && !/[a-z]/.test(newPassword)) {
    violations.push('missing_lowercase');
  }
  if (policy.require_digit && !/\d/.test(newPassword)) {
    violations.push('missing_digit');
  }
  if (policy.require_special && !/[!@#$%^&*\-_=+]/.test(newPassword)) {
    violations.push('missing_special');
  }
  if (newPassword.length > 0 && newPassword === oldPassword) {
    violations.push('same_as_old');
  }
  return violations;
}

function formatPolicyViolations(violations: string[], policy = DEFAULT_PASSWORD_POLICY): string {
  const messages = violations
    .map((violation) => POLICY_MESSAGES[violation]?.(policy))
    .filter((message): message is string => Boolean(message));
  return messages.length > 0 ? messages.join('；') : '新密码不符合安全策略';
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
  const violations = payload?.data?.violations;

  if (code === 40020) {
    return { oldPasswordError: message, newPasswordError: null };
  }
  if (code === 40021 && violations && violations.length > 0) {
    return {
      oldPasswordError: null,
      newPasswordError: formatPolicyViolations(
        violations,
        normalizePasswordPolicy(payload.data?.policy),
      ),
    };
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

  const rules = useMemo(() => {
    const policy = DEFAULT_PASSWORD_POLICY;
    return {
      minLength: newPassword.length >= policy.min_length,
      maxLength: newPassword.length <= policy.max_length,
      uppercase: !policy.require_uppercase || /[A-Z]/.test(newPassword),
      lowercase: !policy.require_lowercase || /[a-z]/.test(newPassword),
      digit: !policy.require_digit || /\d/.test(newPassword),
      special: !policy.require_special || /[!@#$%^&*\-_=+]/.test(newPassword),
      different: newPassword.length > 0 && newPassword !== oldPassword,
    };
  }, [newPassword, oldPassword]);

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

    const localViolations = collectPolicyViolations(newPassword, oldPassword);
    if (localViolations.length > 0) {
      setNewPasswordError(formatPolicyViolations(localViolations));
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
        className="password-modal"
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
            为了账号安全，请使用符合当前安全策略的密码。修改成功后需要重新登录。
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
            <div className={`rule-item${rules.minLength ? ' ok' : ''}`}>
              <span className="rule-dot" />
              至少 {DEFAULT_PASSWORD_POLICY.min_length} 位字符
            </div>
            <div className={`rule-item${rules.maxLength ? ' ok' : ''}`}>
              <span className="rule-dot" />
              不超过 {DEFAULT_PASSWORD_POLICY.max_length} 位字符
            </div>
            <div className={`rule-item${rules.uppercase ? ' ok' : ''}`}>
              <span className="rule-dot" />
              包含大写字母
            </div>
            <div className={`rule-item${rules.lowercase ? ' ok' : ''}`}>
              <span className="rule-dot" />
              包含小写字母
            </div>
            <div className={`rule-item${rules.digit ? ' ok' : ''}`}>
              <span className="rule-dot" />
              包含数字
            </div>
            <div className={`rule-item${rules.special ? ' ok' : ''}`}>
              <span className="rule-dot" />
              包含特殊字符
            </div>
            <div className={`rule-item${rules.different ? ' ok' : ''}`}>
              <span className="rule-dot" />
              不能与原密码相同
            </div>
            <div className="rule-item">
              <span className="rule-dot" />
              避免使用常见弱密码
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
