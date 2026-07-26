## Context

- **现状**：`AdminUserMenu`「密码修改」→ `onPlaceholder` toast；无改密 API；JWT 无 `token_version`；`users` 表无 `token_version` 列。
- **依赖**：`AdminLayout`、`AdminUserMenu`、`PasswordInput`（login）；`REQ-0014` 共用 modal hook。
- **姊妹 change**：`add-admin-profile-page` 使用 `/api/v1/profile/me`；本 change 改密路径为 `/api/v1/admin/profile/password`（REQ-0015 PRD）。apply 时可合并为同一 `admin_profile` router module，路径保持不变。
- **原型优先级**：
  1. `issues/requirements/archive/REQ-0015-password-change/prototype/web/password-change-modal.html`
  2. `prototype/web/password-change-modal.png`
  3. `prototype/web/password-change-modal-context.md`
  4. `acceptance.md`
  5. `rules/ui-design.md`

## Conflict Resolution

| 检查项 | HTML | PNG | acceptance / PRD | 决议 |
|--------|------|-----|------------------|------|
| 弹窗宽度 | 520px | 同 | AC-002 | 520px |
| 成功反馈 | Toast 文案 | — | FR-004 Toast 非 inline | Toast + logout（非 profile save-tip） |
| API 前缀 | — | — | `/admin/profile/password` vs 0014 `/profile/me` | **并存**；同 router 文件不同 prefix 或子路由 |
| 个人资料 placeholder | HTML 背景为 SKU 页 | — | AC-035 0014 未上线时 placeholder 不变 | apply 0015 时仅改「密码修改」；「个人资料」仍 placeholder 直至 0014 apply |
| 错误码 | — | — | 40020–40023、42901 | apply 时登记 `error-codes.md` |
| 遮罩色 | `rgba(0,0,0,.62)` | PNG | semantic token | port CSS 用 `var(--color-*)` 等价，禁止裸 Hex |

## Goals / Non-Goals

**Goals:**

- 侧栏 +（预留）profile 页入口打开同一弹窗
- 改密 API + token_version 全端失效
- 弱密码 + 限流
- PNG 1440×1024 并排验收

**Non-Goals:**

- 忘记密码、MFA、独立路由
- 管理员 reset-password 变更
- 历史密码 N 代不可重复

## Decisions

### D1：CSS Port

- 新增 `password-change-modal.css`（或 `admin-password-change.css`）自 HTML port
- 弹窗结构：`modal-backdrop` + `modal-card password-modal`（520px）
- 复用 admin 壳层 token；输入 44px；footer 40px

### D2：API

```text
POST /api/v1/admin/profile/password
Body: { old_password, new_password }
Auth: require_admin_access
Success: { success: true }
```

- 副作用：`password_hash` 更新；`token_version += 1`；attempt log
- 错误码：40020–40023、42901

### D3：token_version

```sql
ALTER TABLE users ADD COLUMN token_version INTEGER NOT NULL DEFAULT 0;
```

- JWT payload：`tv: user.token_version`（签发时）
- `decode_access_token` + `get_current_user`：`jwt.tv != user.token_version` → 401
- 登录、改密后 token 含新 `tv`

### D4：限流与弱密码

- 弱密码：静态 frozenset ~50–100 条
- 失败：15min 内 ≥5 次原密码错误 → 42901
- 成功：24h 内 ≥3 次成功改密 → 42901
- 表：`password_change_attempts`（user_id, success, created_at）或复用 audit 表

### D5：前端架构

```text
AdminLayout
  ├── ChangePasswordModalContext (open/close)
  ├── ChangePasswordModal
  └── AdminSidebar → AdminUserMenu.onChangePassword
```

- 成功：`admin-toast-region` Toast → `logout()` → `/admin/login`
- 脏关闭：`window.confirm` 或 DS confirm modal（与项目惯例一致）

### D6：与 add-admin-profile-page 联调

- apply 顺序建议：先 0015 modal + API（菜单入口），或同一 PR 改 `AdminUserMenu` 两项
- `openChangePasswordModal` exported via React context from AdminLayout
- Profile 页 apply 时仅调用 context，不 duplicate modal

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 部署后所有旧 JWT 在改密前仍有效 | 仅改密用户 tv 递增；可接受 |
| 双 change 改 AdminUserMenu 冲突 | sprint-003 同包联调 |
| 限流误伤 | 阈值按 PRD；integration test |

## Open Questions

- [ ] confirm 脏关闭用 `window.confirm` vs 小 confirm modal（实现时与品牌启停 confirm 对齐）
