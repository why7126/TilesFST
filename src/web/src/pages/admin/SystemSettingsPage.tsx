import { useCallback, useEffect, useMemo, useState } from 'react';
import { Navigate, useNavigate, useParams } from 'react-router-dom';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import { AdminToast } from '@/features/admin/components/AdminToast';
import {
  fetchRecentAudit,
  fetchSettingsGroup,
  patchSettingsGroup,
  resetSettingsGroup,
  type SettingsGroup,
  type SystemSettingsAuditItem,
} from '@/features/admin/api/system-settings-api';
import '@/features/admin/styles/system-settings.css';

const SETTINGS_TABS: Array<{
  id: SettingsGroup;
  label: string;
  desc: string;
  panelTitle: string;
}> = [
  { id: 'basic', label: '基础信息', desc: '平台名称、语言、时区', panelTitle: '基础信息配置' },
  { id: 'security', label: '安全策略', desc: '密码、登录锁定、会话', panelTitle: '安全策略配置' },
  { id: 'media', label: '媒体与存储', desc: '上传限制与格式策略', panelTitle: '媒体与存储配置' },
  { id: 'notification', label: '通知设置', desc: '账号、SKU、容量预警', panelTitle: '通知设置' },
  { id: 'audit', label: '审计配置', desc: '日志保留与敏感记录', panelTitle: '审计配置' },
];

const GROUP_LABELS: Record<SettingsGroup, string> = {
  basic: '基础信息',
  security: '安全策略',
  media: '媒体与存储',
  notification: '通知设置',
  audit: '审计配置',
};

const VALID_TABS = new Set<string>(SETTINGS_TABS.map((t) => t.id));

const IMAGE_MIME_OPTIONS = [
  { label: 'JPG', value: 'image/jpeg' },
  { label: 'PNG', value: 'image/png' },
  { label: 'WebP', value: 'image/webp' },
  { label: 'GIF', value: 'image/gif' },
  { label: 'SVG', value: 'image/svg+xml' },
  { label: 'BMP', value: 'image/bmp' },
  { label: 'TIFF', value: 'image/tiff' },
  { label: 'HEIC', value: 'image/heic' },
];

const VIDEO_MIME_OPTIONS = [
  { label: 'MP4', value: 'video/mp4' },
  { label: 'MOV', value: 'video/quicktime' },
  { label: 'AVI', value: 'video/x-msvideo' },
  { label: 'WebM', value: 'video/webm' },
  { label: 'MKV', value: 'video/x-matroska' },
  { label: 'MPEG', value: 'video/mpeg' },
  { label: '3GP', value: 'video/3gpp' },
];

type ConfirmDialog =
  | { kind: 'reset' }
  | { kind: 'tab-switch'; nextTab: SettingsGroup };

function formatShortDate(value: string | undefined): string {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

function Toggle({
  checked,
  onChange,
  label,
}: {
  checked: boolean;
  onChange: (value: boolean) => void;
  label: string;
}) {
  return (
    <div className="settings-toggle-row">
      <span className="settings-toggle-label">{label}</span>
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        className={`settings-toggle${checked ? '' : ' off'}`}
        onClick={() => onChange(!checked)}
      />
    </div>
  );
}

function SettingsFooter({
  onCancel,
  onReset,
  onSave,
  saving,
}: {
  onCancel: () => void;
  onReset: () => void;
  onSave: () => void;
  saving: boolean;
}) {
  return (
    <div className="settings-panel-footer">
      <div className="settings-audit-tip">修改系统设置会记录到审计日志。</div>
      <div className="settings-footer-actions">
        <button type="button" className="settings-btn" onClick={onCancel} disabled={saving}>
          取消
        </button>
        <button type="button" className="settings-btn" onClick={onReset} disabled={saving}>
          恢复默认
        </button>
        <button type="button" className="settings-btn primary" onClick={onSave} disabled={saving}>
          {saving ? '保存中…' : '保存设置'}
        </button>
      </div>
    </div>
  );
}

export function SystemSettingsPage() {
  const { tab } = useParams<{ tab?: string }>();
  const navigate = useNavigate();
  const activeTab = (VALID_TABS.has(tab ?? '') ? tab : 'basic') as SettingsGroup;

  const [snapshot, setSnapshot] = useState<Record<string, unknown>>({});
  const [form, setForm] = useState<Record<string, unknown>>({});
  const [auditItems, setAuditItems] = useState<SystemSettingsAuditItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [toast, setToast] = useState<string | null>(null);
  const [confirmDialog, setConfirmDialog] = useState<ConfirmDialog | null>(null);
  const [templateModal, setTemplateModal] = useState<{ title: string; description: string } | null>(
    null,
  );

  const tabMeta = SETTINGS_TABS.find((t) => t.id === activeTab)!;

  const loadGroup = useCallback(async (group: SettingsGroup) => {
    setLoading(true);
    setError(null);
    setToast(null);
    try {
      const data = await fetchSettingsGroup(group);
      setSnapshot(data);
      setForm(data);
      if (group === 'audit') {
        const recent = await fetchRecentAudit(10);
        setAuditItems(recent);
      }
    } catch (err) {
      setError(getErrorMessage(err, '加载系统设置失败'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadGroup(activeTab);
  }, [activeTab, loadGroup]);

  const dirty = useMemo(
    () => JSON.stringify(snapshot) !== JSON.stringify(form),
    [snapshot, form],
  );

  const updateField = (key: string, value: unknown) => {
    setForm((prev) => ({ ...prev, [key]: value }));
    setToast(null);
  };

  const handleTabChange = (nextTab: SettingsGroup) => {
    if (nextTab === activeTab) return;
    if (dirty) {
      setConfirmDialog({ kind: 'tab-switch', nextTab });
      return;
    }
    navigate(`/admin/settings/${nextTab}`);
  };

  const handleCancel = () => {
    setForm(snapshot);
    setToast(null);
    setError(null);
  };

  const executeReset = async () => {
    setSaving(true);
    setError(null);
    try {
      const data = await resetSettingsGroup(activeTab);
      setSnapshot(data);
      setForm(data);
      setToast('已恢复默认配置');
      if (activeTab === 'audit') {
        const recent = await fetchRecentAudit(10);
        setAuditItems(recent);
      }
    } catch (err) {
      setError(getErrorMessage(err, '恢复默认失败'));
    } finally {
      setSaving(false);
    }
  };

  const handleReset = () => {
    setConfirmDialog({ kind: 'reset' });
  };

  const handleConfirmDialog = async () => {
    if (!confirmDialog) return;
    if (confirmDialog.kind === 'tab-switch') {
      const nextTab = confirmDialog.nextTab;
      setConfirmDialog(null);
      navigate(`/admin/settings/${nextTab}`);
      return;
    }
    setConfirmDialog(null);
    await executeReset();
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    setToast(null);
    try {
      const patch: Record<string, unknown> = {};
      for (const key of Object.keys(form)) {
        if (key in snapshot && form[key] !== snapshot[key]) {
          patch[key] = form[key];
        }
      }
      const data = await patchSettingsGroup(activeTab, patch);
      setSnapshot(data);
      setForm(data);
      setToast('设置已保存并立即生效');
    } catch (err) {
      setError(getErrorMessage(err, '保存失败'));
    } finally {
      setSaving(false);
    }
  };

  const toggleMime = (field: 'allowed_image_types' | 'allowed_video_types', mime: string) => {
    const raw = String(form[field] ?? '');
    const current = new Set(raw.split(',').map((s) => s.trim()).filter(Boolean));
    if (current.has(mime)) {
      current.delete(mime);
    } else {
      current.add(mime);
    }
    updateField(field, Array.from(current).join(','));
  };

  if (!tab) {
    return <Navigate to="/admin/settings/basic" replace />;
  }

  if (!VALID_TABS.has(tab)) {
    return <Navigate to="/admin/settings/basic" replace />;
  }

  const renderBasicTab = () => (
    <>
      <section className="settings-section-card">
        <div className="settings-section-head">
          <div>
            <h2 className="settings-section-title">基础信息</h2>
            <p className="settings-section-desc">
              用于维护平台对外显示名称、后台默认语言、时区、首页公告与系统联系信息。
            </p>
          </div>
          <span className="settings-status">已完成</span>
        </div>
        <div className="settings-form-grid">
          <label>
            <span className="settings-field-label">
              平台名称<span className="required">*</span>
            </span>
            <input
              className="settings-input"
              value={String(form.platform_name ?? '')}
              onChange={(e) => updateField('platform_name', e.target.value)}
            />
          </label>
          <label>
            <span className="settings-field-label">
              管理端默认语言<span className="required">*</span>
            </span>
            <select
              className="settings-select"
              value={String(form.default_language ?? 'zh-CN')}
              onChange={(e) => updateField('default_language', e.target.value)}
            >
              <option value="zh-CN">简体中文</option>
              <option value="en">English</option>
            </select>
          </label>
          <label>
            <span className="settings-field-label">
              默认时区<span className="required">*</span>
            </span>
            <select
              className="settings-select"
              value={String(form.default_timezone ?? 'Asia/Shanghai')}
              onChange={(e) => updateField('default_timezone', e.target.value)}
            >
              <option value="Asia/Shanghai">Asia/Shanghai</option>
              <option value="UTC">UTC</option>
            </select>
          </label>
          <label>
            <span className="settings-field-label">数据刷新周期</span>
            <select
              className="settings-select"
              value={String(form.data_refresh_minutes ?? 15)}
              onChange={(e) => updateField('data_refresh_minutes', Number(e.target.value))}
            >
              {[5, 15, 30, 60].map((m) => (
                <option key={m} value={m}>
                  {m} 分钟
                </option>
              ))}
            </select>
          </label>
          <label>
            <span className="settings-field-label">客服邮箱</span>
            <input
              className="settings-input"
              value={String(form.support_email ?? '')}
              onChange={(e) => updateField('support_email', e.target.value)}
            />
          </label>
          <label>
            <span className="settings-field-label">系统维护窗口</span>
            <input
              className="settings-input"
              value={String(form.maintenance_window ?? '')}
              onChange={(e) => updateField('maintenance_window', e.target.value)}
            />
          </label>
          <label style={{ gridColumn: '1 / -1' }}>
            <span className="settings-field-label">系统公告</span>
            <textarea
              className="settings-textarea"
              value={String(form.system_announcement ?? '')}
              onChange={(e) => updateField('system_announcement', e.target.value)}
            />
          </label>
        </div>
      </section>
      <section className="settings-section-card">
        <div className="settings-section-head">
          <div>
            <h2 className="settings-section-title">首页显示配置</h2>
            <p className="settings-section-desc">控制后台首页与列表页默认展示口径。</p>
          </div>
          <span className="settings-status">启用中</span>
        </div>
        <div className="settings-form-grid">
          <div>
            <span className="settings-field-label">显示数据概览</span>
            <Toggle
              label="后台首页展示核心指标卡"
              checked={Boolean(form.show_dashboard_metrics)}
              onChange={(v) => updateField('show_dashboard_metrics', v)}
            />
          </div>
          <div>
            <span className="settings-field-label">展示维护公告</span>
            <Toggle
              label="登录后展示顶部公告提醒"
              checked={Boolean(form.show_maintenance_notice)}
              onChange={(v) => updateField('show_maintenance_notice', v)}
            />
          </div>
        </div>
      </section>
    </>
  );

  const renderMediaTab = () => {
    const imageTypes = new Set(
      String(form.allowed_image_types ?? '')
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean),
    );
    const videoTypes = new Set(
      String(form.allowed_video_types ?? '')
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean),
    );

    return (
      <>
        <section className="settings-section-card">
          <div className="settings-section-head">
            <div>
              <h2 className="settings-section-title">上传限制</h2>
              <p className="settings-section-desc">
                作用于 SKU 图库、Banner 图片、视频素材等媒体文件上传校验。
              </p>
            </div>
            <span className="settings-status">已启用</span>
          </div>
          <div className="settings-form-grid">
            <label>
              <span className="settings-field-label">
                图片最大尺寸 (MB)<span className="required">*</span>
              </span>
              <select
                className="settings-select"
                value={String(form.max_image_size_mb ?? 20)}
                onChange={(e) => updateField('max_image_size_mb', Number(e.target.value))}
              >
                {[5, 10, 20, 50, 100].map((mb) => (
                  <option key={mb} value={mb}>
                    {mb} MB
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span className="settings-field-label">
                视频最大尺寸 (MB)<span className="required">*</span>
              </span>
              <select
                className="settings-select"
                value={String(form.max_video_size_mb ?? 500)}
                onChange={(e) => updateField('max_video_size_mb', Number(e.target.value))}
              >
                {[50, 100, 200, 500, 1000].map((mb) => (
                  <option key={mb} value={mb}>
                    {mb} MB
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span className="settings-field-label">
                文档最大尺寸 (MB)<span className="required">*</span>
              </span>
              <select
                className="settings-select"
                value={String(form.max_file_size_mb ?? 25)}
                onChange={(e) => updateField('max_file_size_mb', Number(e.target.value))}
              >
                {[10, 20, 25, 50, 100, 200].map((mb) => (
                  <option key={mb} value={mb}>
                    {mb} MB
                  </option>
                ))}
              </select>
            </label>
            <div>
              <span className="settings-field-label">支持图片格式</span>
              <div className="settings-chips">
                {IMAGE_MIME_OPTIONS.map((opt) => (
                  <button
                    key={opt.value}
                    type="button"
                    className={`settings-chip${imageTypes.has(opt.value) ? ' active' : ''}`}
                    onClick={() => toggleMime('allowed_image_types', opt.value)}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <span className="settings-field-label">支持视频格式</span>
              <div className="settings-chips">
                {VIDEO_MIME_OPTIONS.map((opt) => (
                  <button
                    key={opt.value}
                    type="button"
                    className={`settings-chip${videoTypes.has(opt.value) ? ' active' : ''}`}
                    onClick={() => toggleMime('allowed_video_types', opt.value)}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </section>
        <section className="settings-section-card">
          <div className="settings-section-head">
            <div>
              <h2 className="settings-section-title">对象存储策略</h2>
              <p className="settings-section-desc">
                当前采用项目级桶与语义前缀目录结构，对齐 REQ-0012 Object Key 规范。
              </p>
            </div>
            <span className="settings-status warn">只读策略</span>
          </div>
          <div className="settings-form-grid">
            <label>
              <span className="settings-field-label">默认存储桶</span>
              <div className="settings-readonly">{String(form.minio_bucket ?? '')}</div>
            </label>
            <label>
              <span className="settings-field-label">Key 生成规则</span>
              <div className="settings-readonly">{String(form.object_key_rule ?? '')}</div>
            </label>
            <div style={{ gridColumn: '1 / -1' }}>
              <span className="settings-field-label">上传区域示意</span>
              <div className="settings-mock-upload">
                拖拽上传图片 / 视频
                <br />
                系统根据业务模块自动生成存储目录
              </div>
              <p className="settings-form-help">
                桶名与 Key 规则来自运行时环境配置，不可在线修改。
              </p>
            </div>
          </div>
        </section>
      </>
    );
  };

  const renderSecurityTab = () => (
    <>
      <section className="settings-section-card">
        <div className="settings-section-head">
          <div>
            <h2 className="settings-section-title">密码策略</h2>
            <p className="settings-section-desc">作用于用户改密、管理员重置密码与随机密码生成。</p>
          </div>
          <span className="settings-status">已启用</span>
        </div>
        <div className="settings-form-grid">
          <label>
            <span className="settings-field-label">密码最小长度</span>
            <input
              type="number"
              className="settings-input"
              min={5}
              max={32}
              value={Number(form.password_min_length ?? 5)}
              onChange={(e) => updateField('password_min_length', Number(e.target.value))}
            />
          </label>
          <label>
            <span className="settings-field-label">密码有效期（天，0=不过期）</span>
            <input
              type="number"
              className="settings-input"
              min={0}
              value={Number(form.password_expiry_days ?? 0)}
              onChange={(e) => updateField('password_expiry_days', Number(e.target.value))}
            />
          </label>
          <div>
            <span className="settings-field-label">须含大写字母</span>
            <Toggle
              label="启用大写字母校验"
              checked={Boolean(form.require_uppercase)}
              onChange={(v) => updateField('require_uppercase', v)}
            />
          </div>
          <div>
            <span className="settings-field-label">须含小写字母</span>
            <Toggle
              label="启用小写字母校验"
              checked={Boolean(form.require_lowercase)}
              onChange={(v) => updateField('require_lowercase', v)}
            />
          </div>
          <div>
            <span className="settings-field-label">须含数字</span>
            <Toggle
              label="启用数字校验"
              checked={Boolean(form.require_digit)}
              onChange={(v) => updateField('require_digit', v)}
            />
          </div>
          <div>
            <span className="settings-field-label">须含特殊字符</span>
            <Toggle
              label="启用特殊字符校验"
              checked={Boolean(form.require_special)}
              onChange={(v) => updateField('require_special', v)}
            />
          </div>
        </div>
      </section>
      <section className="settings-section-card">
        <div className="settings-section-head">
          <div>
            <h2 className="settings-section-title">会话与登录</h2>
            <p className="settings-section-desc">JWT 会话超时对新签发的 Token 生效。</p>
          </div>
        </div>
        <div className="settings-form-grid">
          <label>
            <span className="settings-field-label">会话超时时长（分钟）</span>
            <input
              type="number"
              className="settings-input"
              min={15}
              max={1440}
              value={Number(form.jwt_access_token_expire_minutes ?? 120)}
              onChange={(e) => updateField('jwt_access_token_expire_minutes', Number(e.target.value))}
            />
          </label>
          <div>
            <span className="settings-field-label">首次登录强制改密</span>
            <Toggle
              label="新用户首次登录须修改密码"
              checked={Boolean(form.must_change_password_on_first_login)}
              onChange={(v) => updateField('must_change_password_on_first_login', v)}
            />
          </div>
          <div>
            <span className="settings-field-label">登录失败锁定</span>
            <Toggle
              label="启用连续失败锁定（P1b 预留）"
              checked={Boolean(form.login_lock_enabled)}
              onChange={(v) => updateField('login_lock_enabled', v)}
            />
          </div>
          <label>
            <span className="settings-field-label">失败次数阈值</span>
            <input
              type="number"
              className="settings-input"
              min={3}
              max={20}
              value={Number(form.login_failure_threshold ?? 5)}
              onChange={(e) => updateField('login_failure_threshold', Number(e.target.value))}
            />
          </label>
          <label>
            <span className="settings-field-label">锁定时长（分钟）</span>
            <input
              type="number"
              className="settings-input"
              min={5}
              max={1440}
              value={Number(form.login_lock_minutes ?? 15)}
              onChange={(e) => updateField('login_lock_minutes', Number(e.target.value))}
            />
          </label>
        </div>
      </section>
    </>
  );

  const renderNotificationTab = () => {
    const templates = (form.templates as Array<{ id: string; title: string; description: string }>) ?? [];
    return (
      <>
        <section className="settings-section-card">
          <div className="settings-section-head">
            <div>
              <h2 className="settings-section-title">通知开关</h2>
              <p className="settings-section-desc">仅持久化开关与阈值，不触发真实发信。</p>
            </div>
          </div>
          <div className="settings-form-grid">
            <div>
              <span className="settings-field-label">账号冻结通知</span>
              <Toggle
                label="账号被禁用时发送通知（占位）"
                checked={Boolean(form.account_freeze_notify)}
                onChange={(v) => updateField('account_freeze_notify', v)}
              />
            </div>
            <div>
              <span className="settings-field-label">SKU 待处理提醒</span>
              <Toggle
                label="SKU 待完善时提醒运营"
                checked={Boolean(form.sku_pending_notify)}
                onChange={(v) => updateField('sku_pending_notify', v)}
              />
            </div>
            <div>
              <span className="settings-field-label">存储容量预警</span>
              <Toggle
                label="容量超阈值时预警"
                checked={Boolean(form.storage_capacity_warn)}
                onChange={(v) => updateField('storage_capacity_warn', v)}
              />
            </div>
            <label>
              <span className="settings-field-label">容量预警阈值 (%)</span>
              <input
                type="number"
                className="settings-input"
                min={50}
                max={95}
                value={Number(form.storage_capacity_threshold_pct ?? 80)}
                onChange={(e) => updateField('storage_capacity_threshold_pct', Number(e.target.value))}
              />
            </label>
          </div>
        </section>
        <section className="settings-section-card">
          <div className="settings-section-head">
            <div>
              <h2 className="settings-section-title">通知模板</h2>
              <p className="settings-section-desc">模板只读，可查看占位文案。</p>
            </div>
            <span className="settings-status warn">只读</span>
          </div>
          {templates.map((tpl) => (
            <div key={tpl.id} className="settings-template-row">
              <div>
                <div className="settings-template-title">{tpl.title}</div>
                <div className="settings-template-desc">{tpl.description}</div>
              </div>
              <button
                type="button"
                className="settings-btn"
                onClick={() => setTemplateModal({ title: tpl.title, description: tpl.description })}
              >
                查看
              </button>
            </div>
          ))}
        </section>
      </>
    );
  };

  const renderAuditTab = () => (
    <>
      <section className="settings-section-card">
        <div className="settings-section-head">
          <div>
            <h2 className="settings-section-title">审计范围</h2>
            <p className="settings-section-desc">{String(form.scope_description ?? '')}</p>
          </div>
          <span className="settings-status warn">只读</span>
        </div>
      </section>
      <section className="settings-section-card">
        <div className="settings-section-head">
          <div>
            <h2 className="settings-section-title">审计策略</h2>
            <p className="settings-section-desc">配置日志保留、导出权限与敏感字段脱敏。</p>
          </div>
        </div>
        <div className="settings-form-grid">
          <label>
            <span className="settings-field-label">操作日志保留天数</span>
            <input
              type="number"
              className="settings-input"
              min={30}
              max={3650}
              value={Number(form.retention_days ?? 365)}
              onChange={(e) => updateField('retention_days', Number(e.target.value))}
            />
          </label>
          <div>
            <span className="settings-field-label">允许导出审计日志</span>
            <Toggle
              label="管理员可导出审计记录"
              checked={Boolean(form.allow_export)}
              onChange={(v) => updateField('allow_export', v)}
            />
          </div>
          <div>
            <span className="settings-field-label">敏感操作强制记录</span>
            <Toggle
              label="密码重置等操作强制审计"
              checked={Boolean(form.force_sensitive_audit)}
              onChange={(v) => updateField('force_sensitive_audit', v)}
            />
          </div>
          <div>
            <span className="settings-field-label">敏感字段脱敏展示</span>
            <Toggle
              label="审计列表脱敏手机号/邮箱"
              checked={Boolean(form.mask_sensitive_fields)}
              onChange={(v) => updateField('mask_sensitive_fields', v)}
            />
          </div>
        </div>
      </section>
      <section className="settings-section-card">
        <div className="settings-section-head">
          <div>
            <h2 className="settings-section-title">最近变更记录</h2>
            <p className="settings-section-desc">来自 audit_logs（domain=system_settings）</p>
          </div>
        </div>
        <table className="settings-mini-table">
          <tbody>
            {auditItems.length === 0 ? (
              <tr>
                <td colSpan={2}>暂无变更记录</td>
              </tr>
            ) : (
              auditItems.map((item) => (
                <tr key={item.id}>
                  <td>
                    {item.actor_display_name ?? '系统'} · {formatShortDate(item.created_at)}
                  </td>
                  <td>{item.summary}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </>
  );

  const renderTabContent = () => {
    if (loading) {
      return <p className="settings-form-help">加载中…</p>;
    }
    switch (activeTab) {
      case 'basic':
        return renderBasicTab();
      case 'media':
        return renderMediaTab();
      case 'security':
        return renderSecurityTab();
      case 'notification':
        return renderNotificationTab();
      case 'audit':
        return renderAuditTab();
      default:
        return null;
    }
  };

  return (
    <div className="settings-content-inner">
      <AdminToast message={toast} />
      <section className="settings-page-hero">
        <div>
          <p className="eyebrow">SYSTEM / SYSTEM SETTINGS</p>
          <h1 className="page-title">系统设置 · {GROUP_LABELS[activeTab]}</h1>
          <p className="page-desc">
            按设置分组维护平台配置，保存后立即生效（策略类无需重启）。
          </p>
        </div>
        <div className="settings-hero-actions">
          {dirty ? <span className="settings-mini-badge">有未保存修改</span> : null}
        </div>
      </section>

      <section className="settings-summary-grid">
        <article className="settings-metric-card">
          <div className="settings-metric-label">当前分组</div>
          <div className="settings-metric-value">{GROUP_LABELS[activeTab]}</div>
          <div className="settings-metric-desc">独立配置页面</div>
        </article>
        <article className="settings-metric-card">
          <div className="settings-metric-label">配置状态</div>
          <div className="settings-metric-value">{dirty ? '草稿' : '已同步'}</div>
          <div className="settings-metric-desc">{dirty ? '有未保存修改' : '与服务器一致'}</div>
        </article>
        <article className="settings-metric-card">
          <div className="settings-metric-label">分组数量</div>
          <div className="settings-metric-value">5</div>
          <div className="settings-metric-desc">基础 / 安全 / 媒体 / 通知 / 审计</div>
        </article>
        <article className="settings-metric-card">
          <div className="settings-metric-label">发布状态</div>
          <div className="settings-metric-value">即时</div>
          <div className="settings-metric-desc">保存后立即生效</div>
        </article>
      </section>

      {error ? <div className="settings-error-tip">{error}</div> : null}

      <section className="settings-layout">
        <aside className="settings-nav" aria-label="设置分组">
          <p className="settings-nav-title">SETTING GROUPS</p>
          {SETTINGS_TABS.map((item) => (
            <button
              key={item.id}
              type="button"
              className={`setting-tab${item.id === activeTab ? ' active' : ''}`}
              onClick={() => handleTabChange(item.id)}
            >
              <span>
                <span className="tab-title">{item.label}</span>
                <span className="tab-desc">{item.desc}</span>
              </span>
              <span className={`dot${item.id === 'security' || item.id === 'audit' ? ' warn' : ''}`} />
            </button>
          ))}
        </aside>

        <div className="settings-panel">
          <div className="settings-panel-head">
            <div className="settings-panel-title">{tabMeta.panelTitle}</div>
            <div className="settings-panel-note">自动保存未开启</div>
          </div>
          <div className="settings-panel-body">{renderTabContent()}</div>
          <SettingsFooter
            onCancel={handleCancel}
            onReset={handleReset}
            onSave={() => void handleSave()}
            saving={saving}
          />
        </div>
      </section>

      {confirmDialog ? (
        <div
          role="dialog"
          aria-modal="true"
          className="modal-backdrop"
          onClick={() => setConfirmDialog(null)}
        >
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <h3 className="settings-section-title">
              {confirmDialog.kind === 'reset' ? '恢复默认配置' : '放弃未保存修改'}
            </h3>
            <p className="settings-section-desc" style={{ marginTop: 12 }}>
              {confirmDialog.kind === 'reset'
                ? '确定恢复该分组为默认配置吗？此操作不可撤销。'
                : '有未保存的修改，确定放弃并切换分组吗？'}
            </p>
            <div className="settings-footer-actions" style={{ marginTop: 16 }}>
              <button type="button" className="settings-btn" onClick={() => setConfirmDialog(null)}>
                取消
              </button>
              <button
                type="button"
                className="settings-btn primary"
                onClick={() => void handleConfirmDialog()}
              >
                确认
              </button>
            </div>
          </div>
        </div>
      ) : null}

      {templateModal ? (
        <div
          role="dialog"
          aria-modal="true"
          className="modal-backdrop"
          onClick={() => setTemplateModal(null)}
        >
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <h3 className="settings-section-title">{templateModal.title}</h3>
            <p className="settings-section-desc" style={{ marginTop: 12 }}>
              {templateModal.description}
            </p>
            <p className="settings-form-help" style={{ marginTop: 12 }}>
              此为通知模板占位，本期不发送真实邮件或短信。
            </p>
            <div className="settings-footer-actions" style={{ marginTop: 16 }}>
              <button type="button" className="settings-btn primary" onClick={() => setTemplateModal(null)}>
                关闭
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
