---
requirement_id: REQ-0014-profile-page
title: 管理后台个人资料页面
terminal: web-admin
version: v1.1
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0004-admin-home
created_at: 2026-06-28 09:56:00
updated_at: 2026-06-28 18:53:00
---

# REQ-0014 管理后台个人资料页面

## 1. 需求背景

TILESFST 管理后台已在 `REQ-0004-admin-home` 中定义侧栏底部用户菜单（个人资料、密码修改、退出登录），其中「个人资料」与「密码修改」当前为占位行为。登录用户需要查看与维护自身基础资料（头像、昵称、联系方式、备注），并在同一页面查看账号安全摘要与近期操作记录。

本需求交付独立路由 `/admin/profile`，视觉与交互继承管理后台暗色旗舰风，与首页、SKU 管理页、用户菜单保持一致。密码修改完整流程由姊妹需求 `REQ-0015-password-change` 以居中弹窗实现；本页仅提供入口并与其共用 modal 触发。

与 `REQ-0005-user-management` 边界：用户管理为管理员编辑**他人**资料；本需求为当前登录用户编辑**自己**资料，API 与 UI 分离。

## 2. 目标用户

| 角色 | 是否可访问 | 说明 |
|---|---:|---|
| 后台管理员（`admin`） | 是 | 可查看并编辑本人资料 |
| 后台运营（`employee`） | 是 | 可查看并编辑本人资料 |
| 前台用户（`store_owner`） | 否 | 不得进入管理端（与现有 RBAC 一致） |

## 3. 范围

### 3.1 本期包含

- 管理端路由与页面：`/admin/profile`。
- 侧栏用户菜单「个人资料」导航至该页；在 profile 页时菜单项高亮。
- 页面布局：Page Head + 左栏个人资料主卡片 + 右栏账号安全卡片与操作记录卡片（对齐 prototype）。
- 字段维护：头像、昵称（`display_name`）、联系邮箱、手机号码、备注说明；用户名只读；所属角色、账号状态仅在账号安全卡片展示。
- 数据库：`users.remark` 列（max 200 字）；`profile_activity_logs` 审计表及读写 service。
- 后端 self-service API：当前用户 profile GET/PATCH、activities GET；头像 upload 权限放宽至 `require_admin_access`。
- 操作记录完整审计：资料更新、头像更新、登录等事件写入审计表；页面展示最近 **5** 条 timeline（v1.1 自 20 条收紧，侧栏卡片轻量预览）。
- 保存成功 inline 提示「资料已更新」（原型 `save-tip` 区域）。
- 「修改密码」打开 `REQ-0015` 弹窗（非独立路由）。
- OpenAPI 变更 + Orval 客户端 regeneration。

### 3.2 本期不包含

- 管理员在用户管理页编辑他人资料（已有能力，不在本 REQ 扩展）。
- 密码修改表单与后端接口（`REQ-0015-password-change`）。
- 忘记密码、短信/邮箱验证码、多因素认证。
- 店主端 / 小程序个人资料。
- 导出操作记录、管理员查看他人操作审计。

## 4. 信息架构

```text
admin-shell
├── sidebar（264px sticky）
│   ├── OPERATIONS / SYSTEM 导航（与现有页一致）
│   └── sidebar-user（展开）
│       ├── 个人资料 ← active on /admin/profile
│       ├── 密码修改 → REQ-0015 modal
│       ├── ─── 分隔线 ───
│       └── 退出登录
└── main-content
    ├── page-head（眉标 SYSTEM / PROFILE、标题、说明、保存修改 CTA）
    └── profile-layout（grid: 1fr + 360px）
        ├── profile-card（基础资料表单 + 身份条 + 重置/保存）
        └── side-stack
            ├── 账号安全卡片
            └── 最近操作记录卡片（timeline）
```

## 5. 数据模型

### 5.1 `users` 表扩展

| 字段 | 类型/约束 | 说明 |
|---|---|---|
| remark | TEXT NULL | 个人工作说明，0–200 字；本期 migration 新增 |

其余字段沿用现有 `users`：`username`、`display_name`、`email`、`phone`、`role`、`status`、`avatar_object_key`、`last_login_at` 等。

### 5.2 `profile_activity_logs` 表（新建）

| 字段 | 类型/约束 | 说明 |
|---|---|---|
| id | TEXT PK | UUID |
| user_id | TEXT NOT NULL FK → users.id | 所属用户 |
| action_type | TEXT NOT NULL | `profile_update` \| `avatar_update` \| `login`（可扩展） |
| summary | TEXT NOT NULL | 展示摘要，如「修改昵称与备注」 |
| metadata | TEXT NULL | JSON，可选（变更字段列表等） |
| created_at | TEXT NOT NULL | ISO 时间 |

**写入时机**：

- 用户 PATCH 保存资料成功 → `profile_update`
- 用户头像 `avatar_object_key` 变更成功 → `avatar_update`
- 用户登录成功 → `login`（可与现有 `login_logs` 双写）

**读取**：按 `user_id` 倒序，默认 limit **5**（v1.1；完整审计仍全量写入表，仅 API/页面展示截断）。

## 6. API 要求（建议路径，实现时对齐 `rules/api.md`）

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| GET | `/api/v1/profile/me` | `require_admin_access` | 返回完整 profile（含 avatar_url、remark、last_login_at 等） |
| PATCH | `/api/v1/profile/me` | `require_admin_access` | 更新 display_name、email、phone、remark、avatar_object_key |
| GET | `/api/v1/profile/me/activities` | `require_admin_access` | 返回最近 **5** 条 activity（v1.1） |
| POST | `/api/v1/uploads`（头像） | `require_admin_access` | 放宽现有 avatar upload（原 `require_system_admin`） |

现有 `GET /api/v1/auth/me` 可保留轻量 session 用途；profile 页以 `/profile/me` 为准。

## 7. 功能要求

### FR-001 页面访问与路由

- MUST 注册路由 `/admin/profile`，受 `ProtectedRoute` 保护（`admin` + `employee`，非 `requireAdmin`）。
- MUST 未登录用户跳转登录页；`store_owner` 跳转 forbidden。

### FR-002 用户菜单入口

- MUST 侧栏底部用户菜单「个人资料」导航至 `/admin/profile`，不再触发占位 toast。
- MUST 当前 pathname 为 `/admin/profile` 时，菜单项「个人资料」高亮。
- MUST 「密码修改」「退出登录」行为不变；退出登录与前两项之间有 0.5px 分隔线。

### FR-003 页面标题区

- MUST 眉标 `SYSTEM / PROFILE`、标题「个人资料」、说明「维护当前登录账号的头像、昵称、联系方式与个人工作说明」。
- MAY 标题区右侧提供「保存修改」主按钮（与卡片内按钮行为一致）。

### FR-004 个人资料主卡片

- MUST 展示身份条：头像、昵称、角色摘要、邮箱、最近登录时间、标签区、「更换头像」按钮。
- MUST 表单字段顺序：用户名（只读）、昵称、联系邮箱、手机号码、备注说明。
- MUST NOT 在基础资料表单内展示所属角色、账号状态（二者仅在 FR-005 账号安全卡片展示；BUG-0022 UX 定稿）。
- MUST 昵称必填，长度 2–32 字符（与 admin 用户管理 `display_name` 一致）。
- MUST 邮箱、手机号格式校验；备注最多 200 字。
- MUST 「重置」恢复进入页面时的服务端数据；「保存修改」提交 PATCH。
- MUST 保存成功后于表单底部 inline 展示「资料已更新」及时间戳（非 toast），对齐 prototype `save-tip`。
- MUST 头像支持 JPG/PNG/WebP，最大 2MB；上传失败展示 inline/字段旁错误文案（与 `UserFormModal` 对齐），保留旧头像。

### FR-005 账号安全卡片

- MUST 展示：登录账号、账号状态、所属角色、最后登录（含 user agent 摘要，如有）。
- MUST 「修改密码」按钮打开 `REQ-0015` 密码修改弹窗（共用组件/hook，非页面跳转）。

### FR-006 操作记录卡片

- MUST 从 `GET /profile/me/activities` 拉取最近 **5** 条（v1.1），timeline 展示：事件标题、时间、摘要；记录数不足 5 时展示实际条数。
- MUST 至少支持展示：资料更新、登录后台、头像更新（与 prototype 示例一致）。
- MUST 无数据时展示空态文案，不报错。

### FR-007 审计写入

- MUST 资料 PATCH 成功写入 `profile_update` 审计记录。
- MUST 头像变更成功写入 `avatar_update` 审计记录。
- MUST 登录成功写入 `login` 审计记录（与 `login_logs` 并存）。

### FR-008 侧栏邮箱展示

- SHOULD 侧栏用户区邮箱改用真实 `email` 字段；无邮箱时 fallback 展示策略在实现阶段与 `getUserEmail` 对齐。

## 8. 校验与异常

| 场景 | 提示 |
|---|---|
| 昵称为空 | 「请输入昵称」 |
| 昵称长度不符 | 「昵称长度为 2–32 个字符」 |
| 邮箱格式错误 | 「请输入正确的邮箱地址」 |
| 手机号格式错误 | 「请输入正确的手机号」 |
| 备注超长 | 「备注说明不能超过 200 字」 |
| 保存成功 | inline「资料已更新」 |
| 头像上传失败 | 展示失败原因，保留旧头像 |
| API 失败 | 表单区或页面级错误提示 |

## 9. UI/UE 约束

- MUST 遵循 `rules/ui-design.md` 工业石材暗色旗舰风；禁止裸 Hex。
- MUST 优先参考 `prototype/web/profile-page.html`；Golden Reference 为 `prototype/images/profile-page.png`。
- MUST 主 CTA「保存修改」为品牌金实底；输入框高度约 38px；卡片 0.5px 边框、3px 圆角、暗色半透明背景。
- MUST 与用户管理/SKU 弹窗表单 Label、弱说明文字风格一致。
- MUST NOT 出现浅色模板、过大圆角或与现有管理页不一致的按钮样式。

原型优先级（OpenSpec design.md 须声明）：

```text
1. prototype/web/profile-page.html
2. prototype/images/profile-page.png
3. prototype/web/profile-page-context.md
4. acceptance.md（req-complete 后）
5. rules/ui-design.md
```

## 10. 关联需求

| REQ | 关系 |
|---|---|
| REQ-0004-admin-home | 父需求；用户菜单占位 → 本页正式实现 |
| REQ-0015-password-change | 姊妹需求；共用修改密码弹窗入口 |
| REQ-0005-user-management | 管理员编辑他人；字段命名对齐，API 独立 |

## 11. 非功能要求

- PATCH 仅允许修改当前登录用户本人数据。
- 头像 upload 须走后端授权与 MinIO（`rules/media.md`、`rules/object-storage.md`）。
- API 变更须同步 OpenAPI 与 Orval。
- 须补充后端 pytest 与前端 vitest（profile 页核心交互、校验、API mock）。

## 12. 修订记录

| 版本 | 时间 | 说明 |
|---|---|---|
| v1.1 | 2026-06-28 18:53:00 | 操作记录展示/API 默认 limit 由 20 调整为 **5**（侧栏卡片信息密度；审计表仍全量写入）。原 BUG-0049 驳回，改需求修订。建议 Change：`fix-profile-activities-display-limit`。 |
| v1 | 2026-06-28 09:59:00 | 初版评审通过；`add-admin-profile-page` 已归档 |

## 13. 状态

| 属性 | 值 |
|---|---|
| requirement_id | REQ-0014-profile-page |
| status | in_sprint |
| priority | P1 |
| terminal | web-admin |
| parent_requirement | REQ-0004-admin-home |
| expected_openspec_change | fix-profile-activities-display-limit |

## 14. 验收方向（req-complete 细化）

- [ ] `/admin/profile` 可访问，prototype PNG 并排视觉一致
- [ ] 字段只读/可编辑规则符合 FR-004
- [ ] 保存 inline 提示、重置、校验符合 §8
- [ ] 操作记录 **5** 条 timeline（v1.1）与审计写入符合 FR-006/FR-007
- [ ] 修改密码打开 REQ-0015 弹窗
- [ ] admin + employee 均可使用；store_owner 不可进入
- [ ] `users.remark` migration 与 `profile_activity_logs` 表存在
