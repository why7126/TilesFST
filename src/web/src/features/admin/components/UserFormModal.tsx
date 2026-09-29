import { useModalReturnFocus } from './use-modal-return-focus';
import { AuthorizedImage } from '@/features/media/authorized-media';
import { useEffect, useState } from 'react';

import { createUser, updateUser, uploadAvatar, type UserAdminItem } from '../api/users-api';
import { getErrorMessage } from '@/features/auth/api/auth-api';
import { getUserInitials } from '../lib/user-display';
import { ROLE_FORM_OPTIONS } from '../lib/user-labels';

import { useImageUpload } from '@/features/media/use-image-upload';
import { MediaUploadStatus } from '@/features/media/media-upload-status';

interface UserFormModalProps {
  open: boolean;
  mode: 'create' | 'edit';
  user: UserAdminItem | null;
  onClose: () => void;
  onSuccess: (message: string, initialPassword?: string) => void;
}

export function UserFormModal({ open, mode, user, onClose, onSuccess }: UserFormModalProps) {
  useModalReturnFocus(open);
  const [username, setUsername] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [role, setRole] = useState('store_owner');
  const [avatarKey, setAvatarKey] = useState<string | null>(null);
  const [avatarUrl, setAvatarUrl] = useState<string | null>(null);
  const upload = useImageUpload(uploadAvatar);
  const avatarUploadState = upload.snapshot.stage;
  const avatarUploadError = upload.snapshot.error ?? null;
  const [leavePrompt, setLeavePrompt] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setError(null);
    upload.reset(); setLeavePrompt(false);
    if (mode === 'edit' && user) {
      setUsername(user.username);
      setDisplayName(user.display_name ?? '');
      setEmail(user.email ?? '');
      setPhone(user.phone ?? '');
      setRole(user.role);
      setAvatarKey(user.avatar_object_key ?? null);
      setAvatarUrl(user.avatar_url ?? null);
    } else {
      setUsername('');
      setDisplayName('');
      setEmail('');
      setPhone('');
      setRole('store_owner');
      setAvatarKey(null);
      setAvatarUrl(null);
    }
  }, [open, mode, user]);

  if (!open) return null;

  const initials = getUserInitials(displayName, username);
  const isAvatarUploading = upload.busy || submitting;
  const isAvatarError = avatarUploadState === 'failed' && error === avatarUploadError;

  const handleAvatarChange = async (file: File | undefined, retry = false) => {
    if (submitting) return;
    setError(null);
    const result = await upload.start(file, retry);
    if (result) { setAvatarKey(result.object_key); setAvatarUrl(result.thumbnail_url ?? result.url); }
  };
  const cancelUpload = async () => {
    if (submitting) return false;
    if (!await upload.cancel()) return false;
    setAvatarKey(user?.avatar_object_key ?? null); setAvatarUrl(user?.avatar_url ?? null);
    return true;
  };
  const close = () => { if (submitting) return; if (upload.pending || upload.busy) setLeavePrompt(true); else onClose(); };

  const handleSubmit = async () => {
    if (upload.busy || avatarUploadState === 'failed') {
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
          email: email.trim() || null,
          phone: phone.trim() || null,
          role,
          avatar_object_key: avatarKey,
        });
        onSuccess('用户已创建', data.initial_password);
      } else if (user) {
        await updateUser(user.id, {
          display_name: displayName.trim() || null,
          email: email.trim() || null,
          phone: phone.trim() || null,
          role,
          avatar_object_key: avatarKey,
        });
        onSuccess('用户信息已更新');
      }
      upload.saved();
      onClose();
    } catch (err) {
      setError(getErrorMessage(err, '保存失败'));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-backdrop user-form-modal-backdrop" role="presentation">
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
          <button type="button" className="modal-close" aria-label="关闭" onClick={close}>
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
                    <AuthorizedImage file={upload.snapshot.stage === 'failed' ? undefined : upload.file} reference={upload.snapshot.stage !== 'failed' && upload.sessionId ? {resource_type: 'upload_session', resource_id: upload.sessionId, variant: 'display'} : user && avatarKey === user.avatar_object_key ? {resource_type: 'avatar', resource_id: user.id, variant: 'display'} : undefined}
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
                <span className="flex flex-col">
                  <span className="user-main">
                    {avatarUrl ? '已上传头像' : '默认头像'}
                  </span>
                  <span className="user-sub">支持 JPG / PNG / WebP，建议 1:1 图片</span>

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
            <MediaUploadStatus mediaKind="image" stage={avatarUploadState} progress={upload.snapshot.progress}
              fileName={upload.file?.name} error={avatarUploadError} onCancel={() => void cancelUpload()}
              onRetry={upload.snapshot.retryable ? () => void handleAvatarChange(upload.file, true) : undefined} />
            {upload.snapshot.warning ? <p className="text-brand-gold">{upload.snapshot.warning}</p> : null}
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
            <label className="field-label" htmlFor="um-email">
              联系邮箱
            </label>
            <input
              id="um-email"
              className="input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@example.com"
            />
            <div className="form-help">仅作为联系信息，不用于登录。</div>
          </div>
          <div className="form-row">
            <label className="field-label" htmlFor="um-phone">
              手机号码
            </label>
            <input
              id="um-phone"
              className="input"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="+86 138 0000 2026"
            />
            <div className="form-help">允许数字、空格、+、-，不限定国家格式。</div>
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
            <p
              className="form-help"
              role={isAvatarError ? undefined : 'alert'}
              aria-live="polite"
              style={{ color: 'var(--admin-danger)' }}
            >
              {error}
            </p>
          ) : null}
        </div>
        {leavePrompt ? <div role="alertdialog" aria-label="离开上传" className="modal-body">
          <p>离开将取消未保存的头像上传。</p>
          <button type="button" className="btn" onClick={() => setLeavePrompt(false)}>继续编辑</button>
          <button type="button" className="btn" disabled={avatarUploadState === 'cancelling'}
            onClick={() => void cancelUpload().then(ok => { if (ok) onClose(); })}>取消上传并离开</button>
        </div> : null}
        <div className="modal-footer">
          <button type="button" className="btn" onClick={close} disabled={submitting}>
            取消
          </button>
          <button
            type="button"
            className="btn primary"
            disabled={submitting || isAvatarUploading || avatarUploadState === 'failed'}
            onClick={() => void handleSubmit()}
          >
            {mode === 'create' ? '创建用户' : '保存'}
          </button>
        </div>
      </div>
    </div>
  );
}
