import { useCallback, useEffect, useMemo, useState } from 'react';
import { useOutletContext } from 'react-router-dom';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { ProfileActivityItem, ProfileMe } from '@/shared/api/generated';

import {
  fetchProfileActivities,
  fetchProfileMe,
  patchProfileMe,
  uploadAvatar,
} from '@/features/admin/api/profile-api';
import { getUserInitials } from '@/features/admin/lib/user-display';
import { roleLabel, statusLabel } from '@/features/admin/lib/user-labels';
import '@/features/admin/styles/profile-page.css';

type AvatarUploadState = 'idle' | 'uploading' | 'uploaded' | 'failed';

interface ProfileOutletContext {
  onOpenPasswordChange?: () => void;
  refetchProfileShell?: () => Promise<void>;
}

interface ProfileFormState {
  displayName: string;
  email: string;
  phone: string;
  remark: string;
}

function formatDisplayTimestamp(value: string | null | undefined): string {
  if (!value) {
    return '—';
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  const pad = (num: number) => String(num).padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function activityTitle(actionType: string): string {
  if (actionType === 'profile_update') return '资料更新';
  if (actionType === 'avatar_update') return '头像更新';
  if (actionType === 'login') return '登录后台';
  return actionType;
}

function toFormState(profile: ProfileMe): ProfileFormState {
  return {
    displayName: profile.display_name ?? '',
    email: profile.email ?? '',
    phone: profile.phone ?? '',
    remark: profile.remark ?? '',
  };
}

function validateForm(form: ProfileFormState): string | null {
  const name = form.displayName.trim();
  if (name.length < 2 || name.length > 32) {
    return '昵称长度须为 2–32 个字符';
  }
  if (form.remark.length > 200) {
    return '备注说明不能超过 200 字';
  }
  return null;
}

export function ProfilePage() {
  const context = useOutletContext<ProfileOutletContext | null>();
  const onOpenPasswordChange = context?.onOpenPasswordChange;
  const refetchProfileShell = context?.refetchProfileShell;
  const [profile, setProfile] = useState<ProfileMe | null>(null);
  const [form, setForm] = useState<ProfileFormState>({
    displayName: '',
    email: '',
    phone: '',
    remark: '',
  });
  const [activities, setActivities] = useState<ProfileActivityItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saveTip, setSaveTip] = useState<string | null>(null);
  const [avatarUploadState, setAvatarUploadState] = useState<AvatarUploadState>('idle');
  const [avatarUploadError, setAvatarUploadError] = useState<string | null>(null);

  const loadProfile = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [me, activityItems] = await Promise.all([
        fetchProfileMe(),
        fetchProfileActivities(),
      ]);
      setProfile(me);
      setForm(toFormState(me));
      setActivities(activityItems);
    } catch (err) {
      setError(getErrorMessage(err, '加载个人资料失败'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadProfile();
  }, [loadProfile]);

  const initials = useMemo(
    () => getUserInitials(profile?.display_name, profile?.username),
    [profile?.display_name, profile?.username],
  );

  const handleReset = () => {
    if (!profile) return;
    setForm(toFormState(profile));
    setError(null);
    setSaveTip(null);
  };

  const handleSave = async () => {
    const validationError = validateForm(form);
    if (validationError) {
      setError(validationError);
      return;
    }
    if (avatarUploadState === 'uploading') {
      setError('头像上传中，请稍后保存');
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      const updated = await patchProfileMe({
        display_name: form.displayName.trim(),
        email: form.email.trim() || null,
        phone: form.phone.trim() || null,
        remark: form.remark.trim() || null,
      });
      setProfile(updated);
      setForm(toFormState(updated));
      setSaveTip(`资料已更新 · ${formatDisplayTimestamp(updated.updated_at)}`);
      const activityItems = await fetchProfileActivities();
      setActivities(activityItems);
    } catch (err) {
      setError(getErrorMessage(err, '保存失败'));
    } finally {
      setSubmitting(false);
    }
  };

  const handleAvatarChange = async (file: File | undefined) => {
    if (!file) return;
    setAvatarUploadError(null);
    setAvatarUploadState('uploading');
    try {
      const result = await uploadAvatar(file);
      const updated = await patchProfileMe({ avatar_object_key: result.object_key });
      setProfile(updated);
      setForm(toFormState(updated));
      setAvatarUploadState('uploaded');
      setSaveTip(`资料已更新 · ${formatDisplayTimestamp(updated.updated_at)}`);
      const activityItems = await fetchProfileActivities();
      setActivities(activityItems);
      await refetchProfileShell?.();
    } catch (err) {
      const message = getErrorMessage(err, '头像上传失败');
      setAvatarUploadState('failed');
      setAvatarUploadError(message);
      setError(message);
    }
  };

  if (loading) {
    return <p className="page-desc">加载个人资料…</p>;
  }

  if (!profile) {
    return <p className="profile-error">{error ?? '无法加载个人资料'}</p>;
  }

  const roleText = roleLabel(profile.role);
  const statusText = statusLabel(profile.status);
  const emailDisplay = profile.email?.trim() || `${profile.username}@tilesfst.com`;

  return (
    <>
      <header className="profile-page-head">
        <div>
          <p className="eyebrow">SYSTEM / PROFILE</p>
          <h1 className="page-title">个人资料</h1>
          <p className="page-desc">维护当前登录账号的头像、昵称、联系方式与个人工作说明</p>
        </div>
      </header>

      <section className="profile-layout">
        <article className="profile-card">
          <div className="card-head">
            <div>
              <div className="card-title">基础资料</div>
              <div className="card-desc">用户名与角色由系统分配，仅支持维护个人展示信息</div>
            </div>
            <span className="status on">{profile.status === 'active' ? '账号正常' : statusText}</span>
          </div>
          <div className="profile-body">
            <div className="identity-strip">
              <div className="profile-avatar" aria-hidden={Boolean(profile.avatar_url)}>
                {profile.avatar_url ? (
                  <img src={profile.avatar_url} alt="" />
                ) : (
                  initials
                )}
              </div>
              <div>
                <div className="identity-name">{profile.display_name}</div>
                <div className="identity-meta">
                  {roleText} · {emailDisplay} · 最近登录{' '}
                  {formatDisplayTimestamp(profile.last_login_at)}
                </div>
                <div className="identity-tags">
                  <span className="mini-badge gold">{roleText}</span>
                  <span className="mini-badge">可管理商品资料</span>
                  <span className="mini-badge">安全验证正常</span>
                </div>
              </div>
              <label className={`btn${avatarUploadState === 'uploading' ? ' disabled' : ''}`}>
                {avatarUploadState === 'uploading' ? '上传中' : '更换头像'}
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  hidden
                  disabled={avatarUploadState === 'uploading'}
                  onChange={(event) => {
                    const input = event.currentTarget;
                    void handleAvatarChange(input.files?.[0]).finally(() => {
                      input.value = '';
                    });
                  }}
                />
              </label>
            </div>

            <div className="profile-form-grid">
              <div className="field readonly">
                <label htmlFor="profile-username">用户名 *</label>
                <input id="profile-username" className="input" value={profile.username} readOnly />
              </div>
              <div className="field">
                <label htmlFor="profile-display-name">昵称 *</label>
                <input
                  id="profile-display-name"
                  className="input"
                  value={form.displayName}
                  onChange={(event) =>
                    setForm((current) => ({ ...current, displayName: event.target.value }))
                  }
                />
              </div>
              <div className="field">
                <label htmlFor="profile-email">联系邮箱</label>
                <input
                  id="profile-email"
                  className="input"
                  value={form.email}
                  onChange={(event) =>
                    setForm((current) => ({ ...current, email: event.target.value }))
                  }
                />
              </div>
              <div className="field">
                <label htmlFor="profile-phone">手机号码</label>
                <input
                  id="profile-phone"
                  className="input"
                  value={form.phone}
                  onChange={(event) =>
                    setForm((current) => ({ ...current, phone: event.target.value }))
                  }
                />
              </div>
              <div className="field full">
                <label htmlFor="profile-remark">备注说明</label>
                <textarea
                  id="profile-remark"
                  className="textarea"
                  placeholder="请输入个人工作说明"
                  value={form.remark}
                  onChange={(event) =>
                    setForm((current) => ({ ...current, remark: event.target.value }))
                  }
                />
                <div className="help">最多 200 字；仅后台内部可见。</div>
              </div>
            </div>

            {avatarUploadError ? (
              <p className="profile-error" role="alert">
                {avatarUploadError}
              </p>
            ) : null}
            {error ? (
              <p className="profile-error" role="alert">
                {error}
              </p>
            ) : null}

            <div className="profile-form-actions">
              <div className={`save-tip${saveTip ? '' : ' is-hidden'}`}>{saveTip ?? '占位'}</div>
              <div className="filter-actions">
                <button type="button" className="btn ghost" onClick={handleReset}>
                  重置
                </button>
                <button
                  type="button"
                  className="btn primary"
                  disabled={submitting || avatarUploadState === 'uploading'}
                  onClick={() => void handleSave()}
                >
                  保存修改
                </button>
              </div>
            </div>
          </div>
        </article>

        <div className="side-stack">
          <aside className="side-card">
            <div className="card-title">账号安全</div>
            <div className="card-desc">登录凭证与权限信息由系统统一管理</div>
            <div className="info-list">
              <div className="info-row">
                <span className="info-label">登录账号</span>
                <span className="info-value">{profile.username}</span>
              </div>
              <div className="info-row">
                <span className="info-label">账号状态</span>
                <span className="info-value">
                  <span className="status on">{statusText}</span>
                </span>
              </div>
              <div className="info-row">
                <span className="info-label">所属角色</span>
                <span className="info-value">{roleText}</span>
              </div>
              <div className="info-row">
                <span className="info-label">最后登录</span>
                <span className="info-value">
                  {formatDisplayTimestamp(profile.last_login_at)}
                </span>
              </div>
            </div>
            <button
              type="button"
              className="btn"
              style={{ width: '100%', marginTop: 16 }}
              onClick={() => onOpenPasswordChange?.()}
            >
              修改密码
            </button>
          </aside>

          <aside className="side-card">
            <div className="card-title">最近操作记录</div>
            <div className="card-desc">展示与个人资料相关的审计信息</div>
            {activities.length === 0 ? (
              <p className="timeline-empty">暂无操作记录</p>
            ) : (
              <div className="timeline">
                {activities.map((item) => (
                  <div key={item.id} className="timeline-item">
                    <span className="dot" />
                    <div>
                      <div className="timeline-title">{activityTitle(item.action_type)}</div>
                      <div className="timeline-meta">
                        {formatDisplayTimestamp(item.created_at)} · {item.summary}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </aside>
        </div>
      </section>
    </>
  );
}
