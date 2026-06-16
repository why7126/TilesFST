import { useEffect, useState } from 'react';

import { createUser, updateUser, uploadAvatar, type UserAdminItem } from '../api/users-api';
import { getErrorMessage } from '@/features/auth/api/auth-api';
import { getUserInitials } from '../lib/user-display';
import { ROLE_FORM_OPTIONS } from '../lib/user-labels';

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
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setError(null);
    if (mode === 'edit' && user) {
      setUsername(user.username);
      setDisplayName(user.display_name ?? '');
      setRole(user.role);
      setAvatarKey(user.avatar_object_key ?? null);
    } else {
      setUsername('');
      setDisplayName('');
      setRole('store_owner');
      setAvatarKey(null);
    }
  }, [open, mode, user]);

  if (!open) return null;

  const handleAvatarChange = async (file: File | undefined) => {
    if (!file) return;
    try {
      const result = await uploadAvatar(file);
      setAvatarKey(result.object_key);
    } catch (err) {
      setError(getErrorMessage(err, '头像上传失败'));
    }
  };

  const handleSubmit = async () => {
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
            <div className="avatar-upload">
              <div className="user-cell">
                <span className="avatar">{getUserInitials(displayName, username)}</span>
                <span>
                  <span className="user-main">默认头像</span>
                  <span className="user-sub">支持 JPG / PNG</span>
                </span>
              </div>
              <label className="btn">
                更换头像
                <input
                  type="file"
                  accept="image/*"
                  hidden
                  onChange={(e) => void handleAvatarChange(e.target.files?.[0])}
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
          <button type="button" className="btn" onClick={onClose}>
            取消
          </button>
          <button type="button" className="btn primary" disabled={submitting} onClick={() => void handleSubmit()}>
            {mode === 'create' ? '创建用户' : '保存'}
          </button>
        </div>
      </div>
    </div>
  );
}
