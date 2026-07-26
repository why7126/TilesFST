## Why

REQ-0014 要求将 `REQ-0004-admin-home` 侧栏用户菜单中的「个人资料」从占位 toast 落地为完整 self-service 页面。当前登录的 `admin`/`employee` 无法自助维护头像、昵称、联系方式与备注，也无法查看账号安全摘要与操作审计。用户管理（REQ-0005）仅支持管理员编辑**他人**资料，与「编辑自己」场景 API/UI 分离。本 change 在 Admin Shell 基座就绪后补齐个人资料能力，并为 REQ-0015 修改密码弹窗提供 profile 页入口。

## What Changes

- 新增 `/admin/profile` 页面（CSS Port 自 `profile-page.html` / PNG Golden Reference）。
- 侧栏用户菜单「个人资料」导航至该页；pathname 匹配时菜单项高亮；侧栏邮箱优先展示真实 `email`。
- 数据库：`users.remark`（0–200 字）；新建 `profile_activity_logs` 审计表。
- 新增 self-service API：`GET/PATCH /api/v1/profile/me`、`GET /api/v1/profile/me/activities`（最近 20 条）。
- 登录成功写入 `profile_activity_logs`（`login`）；资料 PATCH / 头像变更写入对应 audit。
- 放宽头像 upload：`POST /api/v1/uploads`（avatars）允许 `require_admin_access`（admin + employee）。
- 保存成功 inline「资料已更新」（非 toast）；「修改密码」打开 REQ-0015 弹窗（入口 only，表单/API 归属 REQ-0015）。
- OpenAPI 更新 + Orval；pytest + vitest；PNG 并排验收 gate。

## Capabilities

### New Capabilities

- `admin-profile-page`：个人资料页 UI、self-service profile API、remark 字段、profile 活动审计、PNG 验收 gate。

### Modified Capabilities

- `auth`：用户数据模型扩展 `remark`；登录成功写入 profile 活动审计。
- `admin-dashboard`：用户菜单「个人资料」可导航；profile 页菜单高亮；侧栏邮箱使用真实 email。
- `web-client`：注册 `/admin/profile` 路由；ProfilePage CSS Port；与 REQ-0015 共用改密 modal 入口 hook。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 新 `profile` router、service、repository；migration；login 双写 audit |
| 前端 Web 管理端 | `ProfilePage`、`profile-page.css` port、AdminUserMenu 导航、Orval |
| 数据库 | `users.remark`；`profile_activity_logs` 表 |
| API / Orval | **MUST** 重新生成 |
| MinIO | 头像 upload 权限放宽；沿用单桶 `original/` 前缀 |
| 测试 | pytest profile/activities/RBAC/audit；vitest ProfilePage |
| 关联 REQ | REQ-0015 改密弹窗（入口耦合，实现可并行） |
| Docker | backend + web 镜像重建 |
