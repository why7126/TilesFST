## Why

`BUG-0074-prod-theme-preference-sync-toast-persistent` 已评审通过。生产环境 Web 管理端切换主题时提示「主题已在本机生效，但账号偏好同步失败，请稍后重试」，且该提示持续存在不会消失。

现有 `web-client` 规格已要求主题切换失败时保留本机视觉选择并展示可恢复错误提示，但没有约束错误提示必须自动消失或可关闭。当前管理端 `AdminLayout` 将主题同步错误写入本地 Toast 状态后缺少清除生命周期，导致错误提示常驻。生产同步失败本身还需要通过 `PATCH /api/v1/auth/me/theme` 的 Network、后端日志、生产 DB 字段和反代链路进一步确认。

需要通过修复 Change 明确：主题偏好同步失败提示必须是可恢复、可消失、可诊断的反馈；账号主题偏好 API 在生产链路中必须保持统一 envelope、鉴权与持久化行为。

## What Changes

- 修改 `web-client` 主题切换与偏好持久化规范：同步失败提示必须自动消失或提供关闭入口，不能常驻页面。
- 要求同步失败时继续保留本机主题即时生效，不得回退当前页面主题或丢失页面状态。
- 要求多次快速切换主题时 Toast 不堆叠、不刷屏、不遮挡主要管理端内容。
- 修改 `auth` 当前用户主题偏好 API 规范：生产环境必须能通过 `PATCH /api/v1/auth/me/theme` 成功保存合法主题，并返回统一 `ApiResponse<UserProfile>` envelope；失败时保持既有鉴权/错误语义且不得写入非法值。
- 要求实现阶段补充前端回归测试和主题偏好 API 回归/生产 smoke 证据。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `web-client`: 强化主题偏好同步失败 Toast 生命周期、可恢复性和回归测试要求。
- `auth`: 强化当前用户主题偏好 API 的生产可用性、统一响应和持久化回归要求。

## Impact

- **web/admin:** 预计修改 `ThemeContext` / `AdminLayout` / `AdminToast` 相关前端状态生命周期，使同步失败提示自动消失或可关闭。
- **api:** 预计不改变接口契约；若排查发现生产接口、响应 envelope 或错误码需要修复，必须同步 OpenAPI、Orval、接口文档和测试。
- **database:** 预计不改变表结构；若生产缺少 `users.theme_mode` 字段或迁移未生效，必须同步 SQLite/MySQL schema、迁移、数据库文档和测试。
- **miniapp:** 不涉及。
- **tests:** 需要补充 Web 前端测试，覆盖同步失败提示自动消失/可关闭、未登录不调用同步接口、多次切换不堆叠；保留或补充后端主题偏好 API 集成测试/生产 smoke。

## Rollback Plan

如修复后主题切换不可用、Toast 不展示、登录态异常或账号偏好保存回退，可回滚前端 Toast 生命周期修改与相关 API/DB 调整。回滚后本机主题切换能力应恢复到修复前状态，但 `BUG-0074` 不得关闭；需要重新分析 Toast 生命周期和生产同步失败根因。
