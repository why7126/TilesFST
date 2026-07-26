## Context

- **现状**：`AdminUserMenu`「个人资料」调用 `onPlaceholder` toast；无 `/admin/profile` 路由；`GET /auth/me` 仅返回 5 字段；头像 upload 仅 `require_system_admin`；无 `users.remark`、无 profile 审计表。
- **依赖**：`AdminLayout`、`admin-home.css`、用户管理头像上传模式（`UserFormModal`）、REQ-0015 改密弹窗（可 stub 或同 Sprint 联调）。
- **原型来源**（优先级，OpenSpec / AGENTS 强制）：
  1. `issues/requirements/archive/REQ-0014-profile-page/prototype/web/profile-page.html`
  2. `issues/requirements/archive/REQ-0014-profile-page/prototype/images/profile-page.png`
  3. `issues/requirements/archive/REQ-0014-profile-page/prototype/web/profile-page-context.md`
  4. `issues/requirements/archive/REQ-0014-profile-page/acceptance.md`
  5. `rules/ui-design.md`
  6. `openspec/specs/`

## Conflict Resolution

| 检查项 | HTML | PNG | acceptance / PRD | 决议 |
|--------|------|-----|------------------|------|
| 昵称长度 | 示例「Admin User」 | 同 HTML | 探索拍板 2–32（admin 一致） | 以 acceptance AC-012 为准 |
| 修改密码 | HTML 无 modal | — | 打开 REQ-0015 弹窗 | **MODIFIED** admin-dashboard 用户菜单；profile 页按钮同 hook |
| 保存成功 | inline `save-tip` | 同 HTML | 非 toast | 以 HTML 为准；**不得**用 `.admin-toast` |
| 账号状态只读字段 | 表单内只读 input | 同 HTML | FR-004 | 保留；与用户名/角色并列 |
| 侧栏邮箱 | `admin@tilesfst.com` 样例 | 同 HTML | FR-008 真实 email | 实现用 API `email`；空则 fallback `{username}@tilesfst.com` |
| 操作记录 | 3 条 mock timeline | 同 HTML | 完整审计 API 20 条 | 数据来自 API；视觉对齐 prototype |
| 头像保存时机 | 按钮「更换头像」 | — | business-flow 待定 | **D4**：选择文件 → upload → 立即 PATCH `avatar_object_key` + audit |

## Goals / Non-Goals

**Goals:**

- `/admin/profile` 与 `profile-page.png` 在 1440×1024 并排验收 pass。
- CSS Port：`profile-page.css`（或合并 admin 样式模块），颜色 `var(--color-*)`。
- 完整 profile API + DB migration + audit + Orval + 测试。
- `admin` + `employee` 可编辑本人资料；`store_owner` 403。
- PNG checklist 写入 change `trace.md`。

**Non-Goals:**

- REQ-0015 改密表单、API、成功后 re-login（仅入口）。
- 管理员在用户管理页编辑他人 remark/email/phone（不在本 change 扩展 admin users PATCH）。
- 导出操作记录、管理员查看他人 audit。
- 店主端 / 小程序个人资料。

## Decisions

### D1：CSS Port（与 add-admin-home / user-management 一致）

- **决策**：新增 `src/web/src/features/admin/styles/profile-page.css`，自 `profile-page.html` port profile 专属布局（`.profile-layout`、`.identity-strip`、`.side-stack`、`.timeline` 等）；Shell 复用 `admin-home.css` via `AdminLayout`。
- **理由**：HTML 含完整两列卡片与 timeline；Tailwind 拼装 fidelity 风险高。
- **Token**：禁止裸 Hex；主按钮 `btn primary` 映射 semantic 品牌金。

### D2：API 设计

```text
GET    /api/v1/profile/me              # 完整 profile
PATCH  /api/v1/profile/me              # display_name, email, phone, remark, avatar_object_key
GET    /api/v1/profile/me/activities   # limit=20, desc
```

- 依赖：`require_admin_access`（admin + employee）。
- PATCH MUST NOT 接受 username、role、status。
- 校验：display_name 2–32；email/phone 格式；remark ≤200。
- 错误码：`PROFILE_VALIDATION_ERROR` 等，登记 `api-governance`。

保留轻量 `GET /auth/me` 供 session bootstrap；profile 页加载以 `/profile/me` 为准。

### D3：数据模型

```sql
-- users 扩展
ALTER TABLE users ADD COLUMN remark TEXT NULL;

-- profile_activity_logs
CREATE TABLE profile_activity_logs (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id),
  action_type TEXT NOT NULL,  -- profile_update | avatar_update | login
  summary TEXT NOT NULL,
  metadata TEXT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX idx_profile_activity_logs_user_created ON profile_activity_logs(user_id, created_at DESC);
```

### D4：头像上传与保存

- Upload：`POST /api/v1/uploads` 头像 endpoint 改为 `require_admin_access`（或新增 `/profile/me/avatar` 代理同一 storage 逻辑）。
- 流程：选文件 → upload → PATCH `avatar_object_key` → `avatar_update` audit → 刷新 UI。
- 复用 `UserFormModal` 上传状态机（idle/uploading/uploaded/failed）。

### D5：前端结构

```text
AdminLayout
  └─ ProfilePage (/admin/profile)
       ├─ page-head（SYSTEM / PROFILE）
       ├─ profile-card（身份条 + form-grid + save-tip + actions）
       └─ side-stack（账号安全 + timeline）
AdminUserMenu
  ├─ 个人资料 → navigate('/admin/profile') + active
  └─ 密码修改 → openPasswordChangeModal()  # REQ-0015
```

- 路由：`ProtectedRoute`（非 `requireAdmin`）。
- 改密 modal：若 REQ-0015 未就绪，提供 noop stub + console warning，acceptance 以联调 Sprint 为准。

### D6：审计写入

| 事件 | action_type | 触发点 |
|------|-------------|--------|
| 登录成功 | `login` | `AuthService.login` 成功后 |
| 资料保存 | `profile_update` | PATCH profile 成功 |
| 头像变更 | `avatar_update` | avatar_object_key 变更成功 |

与 `login_logs` 并存；login 场景 summary 如「安全登录成功」。

### D7：保存成功反馈

- inline `.save-tip` 区域展示「资料已更新 · {timestamp}`。
- **MUST NOT** 使用列表页 `.admin-toast-region` 承载保存成功。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| REQ-0015 未交付 | profile 改密入口 stub；Sprint 同包联调 |
| employee 头像 upload 权限变更 | 仅 avatars 前缀；admin users 仍 require_system_admin |
| 审计表增长 | 本期仅展示 20 条；无归档策略 |
| auth/me 与 profile/me 字段不一致 | 文档明确分工；login 后 optional refresh profile |

## Migration Plan

1. Alembic/SQL migration：`remark` + `profile_activity_logs`。
2. 部署 backend → Orval → web。
3. 无需数据 backfill；login 后开始产生 audit。

## Open Questions

- [ ] 改密 modal 与 REQ-0015 是否同 PR（推荐同 Sprint 一次改 AdminUserMenu）
