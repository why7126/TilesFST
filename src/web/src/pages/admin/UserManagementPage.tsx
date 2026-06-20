import { useCallback, useEffect, useState } from 'react';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { UserAdminItem, UserAdminListData } from '@/shared/api/generated';

import {
  fetchUsers,
  resetUserPassword,
  updateUserStatus,
} from '@/features/admin/api/users-api';
import { ResetPasswordDialog } from '@/features/admin/components/ResetPasswordDialog';
import { UserFormModal } from '@/features/admin/components/UserFormModal';
import { getUserInitials } from '@/features/admin/lib/user-display';
import {
  LOGIN_FILTER_OPTIONS,
  roleBadgeClass,
  roleLabel,
  ROLE_OPTIONS,
  statusBadgeClass,
  STATUS_OPTIONS,
  statusLabel,
} from '@/features/admin/lib/user-labels';
import '@/features/admin/styles/user-management.css';

function formatLoginTime(value: string | null | undefined): string {
  if (!value) return '从未登录';
  return value.replace('T', ' ').slice(0, 16);
}

function formatDate(value: string): string {
  return value.slice(0, 10);
}

export function UserManagementPage() {
  const [keywordDraft, setKeywordDraft] = useState('');
  const [appliedKeyword, setAppliedKeyword] = useState('');
  const [role, setRole] = useState('');
  const [status, setStatus] = useState('');
  const [loginFilter, setLoginFilter] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [data, setData] = useState<UserAdminListData | null>(null);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState<string | null>(null);

  const [formOpen, setFormOpen] = useState(false);
  const [formMode, setFormMode] = useState<'create' | 'edit'>('create');
  const [editingUser, setEditingUser] = useState<UserAdminItem | null>(null);
  const [resetPassword, setResetPassword] = useState<string | null>(null);

  const loadUsers = useCallback(
    async (overridePage?: number) => {
      const currentPage = overridePage ?? page;
      setLoading(true);
      try {
        const result = await fetchUsers({
          page: currentPage,
          page_size: pageSize,
          keyword: appliedKeyword || undefined,
          role: role || undefined,
          status: status || undefined,
          login_filter: loginFilter || undefined,
        });
        setData(result);
      } catch (err) {
        setNotice(getErrorMessage(err, '加载用户列表失败'));
      } finally {
        setLoading(false);
      }
    },
    [appliedKeyword, role, status, loginFilter, page, pageSize],
  );

  useEffect(() => {
    void loadUsers();
  }, [loadUsers]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const next = keywordDraft.trim();
      setAppliedKeyword(next);
      setPage(1);
    }, 300);
    return () => window.clearTimeout(timer);
  }, [keywordDraft]);

  useEffect(() => {
    if (!notice) return;
    const timer = window.setTimeout(() => setNotice(null), 3200);
    return () => window.clearTimeout(timer);
  }, [notice]);

  const handleKeywordEnter = () => {
    setAppliedKeyword(keywordDraft.trim());
    setPage(1);
  };

  const handleReset = () => {
    setKeywordDraft('');
    setAppliedKeyword('');
    setRole('');
    setStatus('');
    setLoginFilter('');
    setPage(1);
    void fetchUsers({ page: 1, page_size: pageSize }).then(setData).catch((err) => {
      setNotice(getErrorMessage(err, '加载用户列表失败'));
    });
  };

  const openCreate = () => {
    setFormMode('create');
    setEditingUser(null);
    setFormOpen(true);
  };

  const openEdit = (user: UserAdminItem) => {
    setFormMode('edit');
    setEditingUser(user);
    setFormOpen(true);
  };

  const handleFormSuccess = (message: string, initialPassword?: string) => {
    setNotice(message);
    if (initialPassword) {
      setResetPassword(initialPassword);
    }
    void loadUsers();
  };

  const handleResetPassword = async (user: UserAdminItem) => {
    if (!window.confirm(`确认为用户 ${user.username} 重置密码？`)) return;
    try {
      const password = await resetUserPassword(user.id);
      setResetPassword(password);
      setNotice('密码已重置');
    } catch (err) {
      setNotice(getErrorMessage(err, '重置密码失败'));
    }
  };

  const handleFreeze = async (user: UserAdminItem) => {
    const next = user.status === 'disabled' ? 'active' : 'disabled';
    try {
      await updateUserStatus(user.id, next);
      setNotice(next === 'disabled' ? '用户已冻结' : '用户已恢复正常');
      void loadUsers();
    } catch (err) {
      setNotice(getErrorMessage(err, '操作失败'));
    }
  };

  const handleDelete = async (user: UserAdminItem) => {
    if (!window.confirm(`确认删除用户 ${user.username}？`)) return;
    try {
      await updateUserStatus(user.id, 'deleted');
      setNotice('用户已删除');
      void loadUsers();
    } catch (err) {
      setNotice(getErrorMessage(err, '删除失败'));
    }
  };

  const total = data?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));

  return (
    <>
      {notice ? (
        <p className="admin-notice" role="status" aria-live="polite">
          {notice}
        </p>
      ) : null}

      <section className="page-hero">
        <div>
          <p className="eyebrow">SYSTEM / USER MANAGEMENT</p>
          <h1 className="page-title">用户管理</h1>
          <p className="page-desc">
            维护前台用户与后台管理用户，控制后台访问权限、账号状态与基础资料。
          </p>
        </div>
        <button type="button" className="btn primary" onClick={openCreate}>
          ＋ 添加用户
        </button>
      </section>

      <section className="filter-card">
        <div className="filter-grid">
          <label>
            <span className="field-label">关键词</span>
            <input
              className="input"
              placeholder="搜索用户名/昵称"
              value={keywordDraft}
              onChange={(e) => setKeywordDraft(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleKeywordEnter()}
            />
          </label>
          <label>
            <span className="field-label">角色</span>
            <select
              className="select"
              value={role}
              onChange={(e) => {
                setRole(e.target.value);
                setPage(1);
              }}
            >
              {ROLE_OPTIONS.map((opt) => (
                <option key={opt.label} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span className="field-label">状态</span>
            <select
              className="select"
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setPage(1);
              }}
            >
              {STATUS_OPTIONS.map((opt) => (
                <option key={opt.label} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span className="field-label">登录情况</span>
            <select
              className="select"
              value={loginFilter}
              onChange={(e) => {
                setLoginFilter(e.target.value);
                setPage(1);
              }}
            >
              {LOGIN_FILTER_OPTIONS.map((opt) => (
                <option key={opt.label} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </label>
          <button type="button" className="btn" onClick={handleReset}>
            重置
          </button>
        </div>
      </section>

      <section className="summary-grid" aria-label="用户统计">
        <article className="metric-card">
          <div className="metric-label">用户总数</div>
          <div className="metric-value">{data?.summary.total ?? '—'}</div>
          <div className="metric-desc">全部有效用户</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">当前筛选</div>
          <div className="metric-value">{data?.summary.filtered ?? '—'}</div>
          <div className="metric-desc">符合条件用户</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">正常用户</div>
          <div className="metric-value">{data?.summary.active_count ?? '—'}</div>
          <div className="metric-desc">允许登录</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">已冻结</div>
          <div className="metric-value">{data?.summary.disabled_count ?? '—'}</div>
          <div className="metric-desc">禁止登录</div>
        </article>
      </section>

      <section className="table-card" aria-label="用户列表">
        <table className="user-mgmt-table">
          <thead>
            <tr>
              <th>用户</th>
              <th>角色</th>
              <th>状态</th>
              <th>最后登录</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {(data?.items ?? []).map((user) => {
              const isDeleted = user.status === 'deleted';
              const canDelete = !user.last_login_at && !isDeleted;
              return (
                <tr key={user.id}>
                  <td>
                    <div className="user-cell">
                      <span className="avatar">
                        {getUserInitials(user.display_name, user.username)}
                      </span>
                      <div className="user-meta">
                        <span className="user-main">{user.username}</span>
                        <span className="user-sub">
                          {user.display_name?.trim() ? user.display_name : '未设置昵称'}
                        </span>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span className={roleBadgeClass(user.role)}>{roleLabel(user.role)}</span>
                  </td>
                  <td>
                    <span className={statusBadgeClass(user.status)}>
                      {statusLabel(user.status)}
                    </span>
                  </td>
                  <td>{formatLoginTime(user.last_login_at)}</td>
                  <td>{formatDate(user.created_at)}</td>
                  <td>
                    <div className="actions">
                      <button
                        type="button"
                        className={`link-btn${isDeleted ? ' disabled' : ''}`}
                        disabled={isDeleted}
                        onClick={() => openEdit(user)}
                      >
                        编辑
                      </button>
                      <button
                        type="button"
                        className={`link-btn${isDeleted ? ' disabled' : ''}`}
                        disabled={isDeleted}
                        onClick={() => void handleResetPassword(user)}
                      >
                        重置密码
                      </button>
                      <button
                        type="button"
                        className={`link-btn danger${isDeleted ? ' disabled' : ''}`}
                        disabled={isDeleted}
                        onClick={() => void handleFreeze(user)}
                      >
                        {user.status === 'disabled' ? '解冻' : '冻结'}
                      </button>
                      <button
                        type="button"
                        className={`link-btn${canDelete ? ' danger' : ' disabled'}`}
                        disabled={!canDelete}
                        title={canDelete ? undefined : '已登录用户不可删除'}
                        onClick={() => void handleDelete(user)}
                      >
                        删除
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        <div className="pagination">
          <div className="page-summary">共 {loading ? '…' : total} 个用户</div>
          <div className="page-right">
            <div className="page-buttons">
              <button
                type="button"
                className="page-btn"
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
              >
                ‹
              </button>
              <button type="button" className="page-btn active">
                {page}
              </button>
              <button
                type="button"
                className="page-btn"
                disabled={page >= totalPages}
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              >
                ›
              </button>
            </div>
            <div className="page-size-wrap">
              <span>每页显示</span>
              <select
                className="page-size"
                value={pageSize}
                aria-label="每页显示条数"
                onChange={(e) => {
                  setPageSize(Number(e.target.value));
                  setPage(1);
                }}
              >
                <option value={10}>10 条</option>
                <option value={20}>20 条</option>
                <option value={50}>50 条</option>
              </select>
            </div>
          </div>
        </div>
      </section>

      <UserFormModal
        open={formOpen}
        mode={formMode}
        user={editingUser}
        onClose={() => setFormOpen(false)}
        onSuccess={handleFormSuccess}
      />
      <ResetPasswordDialog
        open={Boolean(resetPassword)}
        password={resetPassword}
        onClose={() => setResetPassword(null)}
      />
    </>
  );
}
