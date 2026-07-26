## Why

REQ-0017 要求将 `REQ-0004-admin-home` 侧栏 SYSTEM 分组中的「系统设置」从无效占位落地为完整平台配置能力。当前平台参数分散在 `.env` 与代码常量，管理员无法在 UI 中维护站点信息、媒体限制、安全策略、通知开关与审计策略，且变更无统一留痕。本 change 在 Admin Shell 基座就绪后补齐系统设置（5 分组 Tab + 持久化 + 分 Phase 交付）。

## What Changes

- 新增 `/admin/settings` 路由族（5 Tab 子路由）与 `SystemSettingsPage`（CSS Port 自 v2 设计包 HTML）。
- 侧栏「系统设置」配置 `path`；仅 `admin` 可见；`employee` 隐藏菜单且 API/路由 403。
- SQLite `system_settings` KV 表；`EffectiveSettingsService` runtime merge DB 与 env 默认值。
- 新增 `/api/v1/admin/system-settings/{group}` GET/PATCH/reset 与 audit recent 查询。
- P0：基础信息 + 媒体与存储；P1：安全策略（联动改密/建用户）；P2：`audit_logs` + 审计 Tab；P3：通知开关（无发信引擎）。
- OpenAPI 更新 + Orval；pytest + vitest；HTML/PNG 并排验收 gate。

## Capabilities

### New Capabilities

- `system-settings`：系统设置页 UI、分组 API、`system_settings` 持久化、effective settings、审计写入、Phase 验收 gate。

### Modified Capabilities

- `admin-dashboard`：系统设置可导航；admin 路由 active；employee 不展示菜单；占位场景移除「系统设置」。
- `object-storage`：上传大小/MIME 校验 MUST 读取 effective settings（DB merge env），非仅进程启动 snapshot。
- `auth`：JWT 超时与密码策略 enforcement 读取 effective security settings；可选登录失败锁定（P1b）。
- `user-management`：重置密码/创建用户 MUST 校验 effective 密码策略。
- `web-client`：注册 system-settings 路由；admin-only 守卫；侧栏 nav 按角色过滤。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | system-settings router、service、repository；migration；upload/auth 读 effective settings |
| 前端 Web 管理端 | `SystemSettingsPage`、`system-settings.css` port、admin-nav、Orval |
| 数据库 | `system_settings`；P2 `audit_logs`（与 REQ-0014 统一） |
| API / Orval | **MUST** 重新生成 |
| 测试 | pytest settings/RBAC/effective upload；vitest SystemSettingsPage |
| 关联 REQ | REQ-0012（媒体只读 Key 文案）；REQ-0014/0015（audit 统一、密码联动） |
| Docker | backend + web 镜像重建 |
