import { FormEvent, useId, useState } from 'react';

import { useAuth } from '../hooks/useAuth';

interface LoginFormProps {
  onSuccess: () => void;
}

export function LoginForm({ onSuccess }: LoginFormProps) {
  const { login, isLoading, error, clearError } = useAuth();
  const rememberId = useId();
  const accountId = useId();
  const passwordId = useId();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<{ username?: string; password?: string }>({});

  const submit = async () => {
    clearError();
    const nextErrors: { username?: string; password?: string } = {};
    if (!username.trim()) {
      nextErrors.username = '请输入账号';
    }
    if (!password.trim()) {
      nextErrors.password = '请输入密码';
    }
    setFieldErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) {
      return;
    }

    try {
      await login(username.trim(), password, rememberMe);
      onSuccess();
    } catch {
      // error state handled in store
    }
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    await submit();
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <div className="field">
        <div className="label-row">
          <label htmlFor={accountId} className="field-label">
            账号
          </label>
        </div>
        <input // ds-ok: login CSS port field-input
          id={accountId}
          name="username"
          type="text"
          className="field-input"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              void submit();
            }
          }}
          placeholder="请输入手机号 / 邮箱 / 员工账号"
          aria-invalid={Boolean(fieldErrors.username)}
        />
        {fieldErrors.username ? (
          <p className="field-error" role="alert">
            {fieldErrors.username}
          </p>
        ) : null}
      </div>

      <div className="field">
        <div className="label-row">
          <label htmlFor={passwordId} className="field-label">
            密码
          </label>
        </div>
        <input // ds-ok: login CSS port field-input
          id={passwordId}
          name="password"
          type="password"
          className="field-input"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              void submit();
            }
          }}
          placeholder="请输入登录密码"
          aria-invalid={Boolean(fieldErrors.password)}
        />
        {fieldErrors.password ? (
          <p className="field-error" role="alert">
            {fieldErrors.password}
          </p>
        ) : null}
      </div>

      <div className="form-options">
        <label htmlFor={rememberId} className="check">
          <input // ds-ok: login CSS port checkbox
            id={rememberId}
            type="checkbox"
            className="check-input"
            checked={rememberMe}
            onChange={(event) => setRememberMe(event.target.checked)}
          />
          <span className="box" aria-hidden="true">
            {rememberMe ? '✓' : ''}
          </span>
          记住登录状态
        </label>
      </div>

      {error ? (
        <p className="login-error" role="alert">
          {error}
        </p>
      ) : null}

      <button // ds-ok: login CSS port primary
        type="submit"
        className="primary"
        disabled={isLoading}
        aria-busy={isLoading}
      >
        {isLoading ? '登录中...' : '登录'}
      </button>
    </form>
  );
}
