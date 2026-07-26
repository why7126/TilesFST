## Why

当前 Web 管理端已覆盖登录、Dashboard、SKU、品牌、Banner、类目、规格、用户、日志、接口文档、个人资料和系统设置等页面，但移动端响应式策略分散在各页面 CSS 与组件中。`REQ-0027` 已评审并纳入 `sprint-010`，需要把“手机与小屏平板基础可用”的范围、断点、横切验收和测试矩阵固化为 OpenSpec Change，避免后续实现只修单点页面而遗漏 Shell、列表、弹窗和上传控件的共性问题。

## What Changes

- 明确 Web 管理端 `/admin/*` 已实现页面在 `375x812`、`390x844`、`768x1024` 和 `1440x1024` 视口下的基础可用要求。
- 补充 Admin Shell、Sidebar、内容区、列表筛选、表格、分页、表单弹窗、日志抽屉、设置页、个人资料页、登录页和无权限页的移动端验收契约。
- 将 `REQ-0027` 的 knowledge-base 横切 AC 落入设计与任务：`admin-list`、`admin-form`、`admin-modal`、`media-upload`。
- 约束实现阶段不得扩大到店主 Web、微信小程序、API、数据库、Orval、Docker Compose、MinIO 或媒体后端链路。
- 要求实现阶段补充 Playwright 或等价浏览器 smoke 验收记录，并保留桌面回归视口。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `admin-dashboard`: 补充管理端 Shell 与 Sidebar 在手机/小屏平板视口下的基础可用契约。
- `web-client`: 补充 Web 管理端已实现页面的移动端列表、分页、弹窗、表单、上传控件和 smoke 验收契约。

## Impact

- Web：影响 `src/web/src/` 下管理端布局、页面样式、共享管理端 UI/业务组件与前端 smoke 测试。
- 管理端：影响 `/admin/*` 当前已实现页面的移动端基础可用性与验收矩阵。
- API：不影响；本 Change 不新增或修改请求、响应、错误码、OpenAPI 或 Orval。
- 数据库：不影响；不新增表、字段、迁移或 Pydantic Schema。
- 小程序：不影响。
- 媒体/对象存储：仅验收已有上传控件在移动端的展示状态，不修改 MinIO、Nginx、上传大小限制或后端链路。
- Docker Compose：默认不需要验证；若实现阶段触及代理、上传或部署配置，必须拆分或补充独立门禁。
