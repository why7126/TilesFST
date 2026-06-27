import { useEffect, useState } from 'react';

import { createUser, updateUser, uploadAvatar, type UserAdminItem } from '../api/users-api';
import { getErrorMessage } from '@/features/auth/api/auth-api';
import { getUserInitials } from '../lib/user-display';
import { ROLE_FORM_OPTIONS } from '../lib/user-labels';

type AvatarUploadState = 'idle' | 'uploading' | 'uploaded' | 'failed';

interface UserFormModalProps {
  open: boolean;
  mode: 'create' | 'edit';
  user: UserAdminItem | null;
  onClose: () => void;
  onSuccess: (message: string, initialPassword?: string) => void;
}

export function UserFormModal({ open, mode, user, onClose, onSuccess }: UserFormModalProps) {
  const [username, setUsername] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [role, setRole] = useState('store_owner');
  const [avatarKey, setAvatarKey] = useState<string | null>(null);
  const [avatarUrl, setAvatarUrl] = useState<string | null>(null);
  const [avatarUploadState, setAvatarUploadState] = useState<AvatarUploadState>('idle');
  const [avatarUploadProgress, setAvatarUploadProgress] = useState(0);
  const [avatarUploadError, setAvatarUploadError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setError(null);
    setAvatarUploadState('idle');
    setAvatarUploadProgress(0);
    setAvatarUploadError(null);
    if (mode === 'edit' && user) {
      setUsername(user.username);
      setDisplayName(user.display_name ?? '');
      setRole(user.role);
      setAvatarKey(user.avatar_object_key ?? null);
      setAvatarUrl(user.avatar_url ?? null);
    } else {
      setUsername('');
      setDisplayName('');
      setRole('store_owner');
      setAvatarKey(null);
      setAvatarUrl(null);
    }
  }, [open, mode, user]);

  if (!open) return null;

  const initials = getUserInitials(displayName, username);
  const isAvatarUploading = avatarUploadState === 'uploading';

  const handleAvatarChange = async (file: File | undefined) => {
    if (!file) return;
    setError(null);
    setAvatarUploadError(null);
    setAvatarUploadState('uploading');
    setAvatarUploadProgress(8);
    try {
      const result = await uploadAvatar(file, (progress) => {
        setAvatarUploadProgress(progress);
      });
      setAvatarKey(result.object_key);
      setAvatarUrl(result.url);
      setAvatarUploadProgress(100);
      setAvatarUploadState('uploaded');
    } catch (err) {
      const message = getErrorMessage(err, '头像上传失败');
      setAvatarUploadState('failed');
      setAvatarUploadProgress(0);
      setAvatarUploadError(message);
      setError(message);
    }
  };

  const handleSubmit = async () => {
    if (avatarUploadState === 'uploading') {
      setError('头像上传中，请稍后保存');
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      if (mode === 'create') {
        const data = await createUser({
          username: username.trim().toLowerCase(),
          display_name: displayName.trim() || null,
          role,
          avatar_object_key: avatarKey,
        });
        onSuccess('用户已创建', data.initial_password);
      } else if (user) {
        await updateUser(user.id, {
          display_name: displayName.trim() || null,
          role,
          avatar_object_key: avatarKey,
        });
        onSuccess('用户信息已更新');
      }
      onClose();
    } catch (err) {
      setError(getErrorMessage(err, '保存失败'));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div
        className="modal-card"
        role="dialog"
        aria-modal="true"
        aria-labelledby="user-form-title"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-head">
          <span id="user-form-title" className="modal-title">
            {mode === 'create' ? '添加用户' : '编辑用户'}
          </span>
          <button type="button" className="modal-close" aria-label="关闭" onClick={onClose}>
            ×
          </button>
        </div>
        <div className="modal-body">
          <div className="form-row">
            <label className="field-label" htmlFor="um-username">
              用户名
            </label>
            <input
              id="um-username"
              className="input"
              value={username}
              readOnly={mode === 'edit'}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="小写字母开头，4–32 位"
            />
            <div className="form-help">4–32 位，小写字母开头；创建后不可修改。</div>
          </div>
          <div className="form-row">
            <label className="field-label">头像</label>
            <div className="avatar-upload brand-logo-upload">
              <div className="brand-logo-meta">
                <span className="brand-logo-preview">
                  {avatarUrl ? (
                    <img
                      src={avatarUrl}
                      alt=""
                      onError={(event) => {
                        event.currentTarget
                          .closest('.brand-logo-preview')
                          ?.classList.add('is-fallback');
                      }}
                      onLoad={(event) => {
                        event.currentTarget
                          .closest('.brand-logo-preview')
                          ?.classList.remove('is-fallback');
                      }}
                    />
                  ) : null}
                  <span className="brand-logo-fallback">{initials}</span>
                </span>
                <span>
                  <span className="user-main">
                    {avatarUrl ? '已上传头像' : '默认头像'}
                  </span>
                  <span className="user-sub">支持 JPG / PNG / WebP，建议 1:1 图片</span>
                  {isAvatarUploading ? (
                    <span className="brand-logo-status">
                      <span
                        className="brand-logo-progress"
                        role="progressbar"
                        aria-valuemin={0}
                        aria-valuemax={100}
                        aria-valuenow={avatarUploadProgress}
                      >
                        <span
                          className="brand-logo-progress-bar"
                          style={{ width: `${avatarUploadProgress}%` }}
                        />
                      </span>
                      <span className="brand-logo-progress-text">
                        上传中 {avatarUploadProgress}%
                      </span>
                    </span>
                  ) : null}
                  {avatarUploadState === 'uploaded' ? (
                    <span className="brand-logo-upload-success">头像已更新</span>
                  ) : null}
                  {avatarUploadState === 'failed' && avatarUploadError ? (
                    <span className="brand-logo-upload-error" role="alert">
                      {avatarUploadError}
                    </span>
                  ) : null}
                </span>
              </div>
              <label
                className={`btn${isAvatarUploading ? ' disabled' : ''}`}
                aria-disabled={isAvatarUploading}
              >
                {isAvatarUploading ? '上传中' : avatarUrl ? '更换头像' : '更换头像'}
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  disabled={isAvatarUploading}
                  hidden
                  onChange={(e) => {
                    const input = e.currentTarget;
                    void handleAvatarChange(input.files?.[0]).finally(() => {
                      input.value = '';
                    });
                  }}
                />
              </label>
            </div>
          </div>
          <div className="form-row">
            <label className="field-label" htmlFor="um-nickname">
              昵称
            </label>
            <input
              id="um-nickname"
              className="input"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              placeholder="默认为空，可后续修改"
            />
            <div className="form-help">未填写时前台可展示用户名。</div>
          </div>
          <div className="form-row">
            <label className="field-label" htmlFor="um-role">
              角色
            </label>
            <select
              id="um-role"
              className="select"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              {ROLE_FORM_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
          {error ? (
            <p className="form-help" style={{ color: 'var(--admin-danger)' }}>
              {error}
            </p>
          ) : null}
        </div>
        <div className="modal-footer">
          <button type="button" className="btn" onClick={onClose} disabled={submitting}>
            取消
          </button>
          <button
            type="button"
            className="btn primary"
            disabled={submitting || isAvatarUploading}
            onClick={() => void handleSubmit()}
          >
            {mode === 'create' ? '创建用户' : '保存'}
          </button>
        </div>
      </div>
    </div>
  );
}
