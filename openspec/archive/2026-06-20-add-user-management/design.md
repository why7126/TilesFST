## Context

- **现状**：`users` 表含 `admin`/`employee`/`store_owner` 与 `active`/`disabled`；无用户管理 API；`admin-nav.ts` 中「用户管理」无 `path`。
- **依赖**：`add-admin-home` 已提供 `AdminLayout`、`AdminSidebar`、`admin-home.css`（待 archive）。
- **原型来源**（优先级，不可省略）：
  1. `issues/requirements/archive/REQ-0005-user-management/prototype/web/user-management-list.html`
  2. `issues/requirements/archive/REQ-0005-user-management/prototype/web/user-management-list.png`
  3. `issues/requirements/archive/REQ-0005-user-management/prototype/web/user-management-modal.html`
  4. `issues/requirements/archive/REQ-0005-user-management/prototype/web/user-management-modal.png`
  5. `prototype/web/*-context.md`
  6. `issues/requirements/archive/REQ-0005-user-management/acceptance.md`
  7. `rules/ui-design.md`
  8. `openspec/specs/`

## Conflict Resolution

| 检查项 | HTML | PNG | acceptance / PRD | 决议 |
|--------|------|-----|------------------|------|
| 页面说明文案 | 含「基础资料」 | 同 HTML | list-context 曾较短 | 以 HTML 为准 |
| 用户名长度 | 辅助文案 4–32 | — | AC-016 4–32 + 格式 | 一致；后端 Pydantic 与前端表单同步校验 |
| 角色产品文案 vs DB enum | 前台/运营/管理员 badge | 同 HTML | `store_owner`/`employee`/`admin` | API 返回 enum；前端映射中文 label |
| 状态「已删除」 | badge.deleted | 同 HTML | `deleted` status | DB CHECK 扩展；登录与 `disabled` 均拒绝 |
| 列表页无弹窗遮罩 | list.html 无 backdrop | list-context §10 | modal 为独立状态页 | 列表路由不渲染弹窗；弹窗为页面内 state |
| `web-client` employee 无权限 | — | — | AC-003 employee 403 | **MODIFIED**「角色权限前端拦截」：用户管理为 admin 专属 |
| auth 管理端 API | 原 spec 仅 admin+employee 进管理端 | — | 用户 API 仅 admin | **ADDED** auth「管理端用户管理 API 访问控制」；不改变 employee 进 dashboard |

## Goals / Non-Goals

**Goals:**

- `/admin/users` 列表 + 弹窗与 list/modal PNG 在 1280×1024 并排验收 pass。
- CSS Port：`user-management.css`（或合并进 admin 样式模块），颜色 `var(--color-*)`。
- 完整 Admin Users API + DB 迁移 + Orval + 测试。
- 仅 `admin` 可管理用户；`employee` 不可见菜单、不可调 API。
- ≥20 项 PNG checklist 写入 change `trace.md`。

**Non-Goals:**

- 用户自助注册、细粒度 RBAC、`login_logs` 写入。
- 个人资料/密码修改（当前用户自助）完整流程。
- 前台店主端用户自助改密/头像。
- 修改 login/me/logout 核心契约（除扩展 me 可选 avatar 外）。

## Decisions

### D1：CSS Port（路径 A，与 add-admin-home 一致）

- **决策**：新增 `src/web/src/features/admin/styles/user-management.css`，自 list/modal HTML port；Shell 复用 `admin-home.css` 的 `.admin-shell`、`.sidebar` 等（通过 `AdminLayout`）。
- **理由**：HTML 含完整筛选网格、指标卡、表格、弹窗样式；Tailwind 拼装 fidelity 风险高。
- **Token 映射**：与 `add-admin-home` design D1 相同（`--page` → `--color-page` 等）。

### D2：产品角色 ↔ 存储枚举

| 产品文案 | `users.role` | 可进管理端 | 用户管理 |
|---|---|---|---|
| 前台用户 | `store_owner` | 否 | — |
| 后台运营 | `employee` | 是 | 不可见/不可操作 |
| 后台管理员 | `admin` | 是 | 全部 |

| 产品文案 | `users.status` | 可登录 |
|---|---|---|
| 正常 | `active` | 是 |
| 已冻结 | `disabled` | 否 |
| 已删除 | `deleted` | 否 |

### D3：API 设计

```text
GET    /api/v1/admin/users              # 分页、keyword、role、status、login_filter + summary
POST   /api/v1/admin/users              # 创建；响应含 initial_password（一次性）
GET    /api/v1/admin/users/{id}
PATCH  /api/v1/admin/users/{id}         # display_name, role, avatar_object_key
POST   /api/v1/admin/users/{id}/reset-password
PATCH  /api/v1/admin/users/{id}/status  # body: { status: active|disabled|deleted }
```

- 依赖：`require_admin`（仅 `role=admin`），区别于现有 `require_admin_user`（admin+employee）。
- 错误码：`USER_USERNAME_TAKEN`、`USER_INVALID_USERNAME`、`USER_CANNOT_DELETE_LOGGED_IN`、`USER_INVALID_STATUS_TRANSITION` 等，登记 `api-governance`。

### D4：用户名与密码

- 用户名：4–32 位；`^[a-z][a-z0-9._-]{3,31}$` + 保留字列表 + 禁止连续 `__|--|..`。
- 初始/重置密码：≥12 位，大小写+数字+特殊字符，排除 O/0/I/l；bcrypt 存储；API 仅创建/重置响应返回一次明文。

### D5：头像存储

- 字段：`users.avatar_object_key`（TEXT NULL）。
- 上传：扩展 `POST /api/v1/admin/uploads`（或专用 `avatars` 前缀），MinIO 单桶 `MINIO_PREFIX_*`；前端不直连未授权 URL。
- 展示：列表/弹窗无头像时用用户名首字母缩写 avatar。

### D6：前端结构

```text
AdminLayout (existing)
  └─ UserManagementPage  (/admin/users)
       ├─ page-hero + 添加用户
       ├─ filter-card
       ├─ summary-grid (4 metrics)
       ├─ table + pagination
       └─ UserFormModal (add/edit)
       └─ ResetPasswordDialog
```

- `admin-nav.ts`：`users` 项 `path: '/admin/users'`；`AdminSidebar` 按 `role===admin` 过滤 SYSTEM 项。
- 路由：`<Route path="users" element={<AdminOnly><UserManagementPage /></AdminOnly>} />` 或等价 guard。

### D7：删除与冻结

- 冻结：`status=disabled`；列表操作「冻结/解冻」。
- 删除：`last_login_at IS NULL` 才允许 → `status=deleted`；已删除行操作列禁用。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| auth spec 与 employee 管理端准入语义冲突 | 新增独立 requirement「管理端用户管理 API」；不缩小 employee 进 dashboard |
| Sprint 002 容量 22 人天偏紧 | 先 archive admin-home；用户管理后端优先再前端 |
| 迁移破坏种子用户 | 迁移脚本 `display_name` 保留；空昵称 COALESCE username |
| 一次性密码泄露 | HTTPS only；日志脱敏；前端复制后关闭不可再看 |

## Migration Plan

1. 执行 schema 迁移（`deleted` status、avatar、nullable display_name）。
2. 部署后端 API；运行 Orval。
3. 发布前端 `/admin/users`。
4. 现有 `active`/`disabled` 用户不受影响；种子 admin 保留。

## 验收 Gate

- 视口：**1280×1024**
- Golden：`user-management-list.png`、`user-management-modal.png`
- Checklist：≥20 项，记录于 `trace.md`
- 命令：`vitest`、`pytest`、`npm run build`、`docker compose build`
