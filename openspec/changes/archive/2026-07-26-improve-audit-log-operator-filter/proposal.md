## Why

日志审计页面当前按“操作者”筛选时仍要求输入 `User ID`，而管理员在真实审计和排障中更常使用用户名称或账号识别操作者。直接输入 ID 会让查询链路变长，也容易因为复制或拼写错误导致误判“无日志”。

本 Change 将操作者筛选优化为按用户名称/账号搜索并单选，同时保持后端日志查询继续使用稳定的 `actor_user_id`，兼顾可用性与审计准确性。

## What Changes

- 将 `/admin/logs` 操作者筛选从普通 User ID 输入框改为单选可搜索下拉。
- 下拉候选项只展示账号与用户名称两行，并用账号行区分同名用户。
- 选择操作者后，日志列表仍传 `actor_user_id=<user.id>` 查询，不按显示名称过滤日志。
- 候选搜索优先复用现有 `GET /api/v1/admin/users` 的 `keyword` 查询；如实现确认不足，再新增轻量候选接口并同步 OpenAPI/Orval。
- 补充候选搜索 loading、empty、failed、clear、reset 等交互状态。
- 将 `admin-list` 横切验收纳入本 Change：分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm`、移动端筛选区可用。
- 不改写审计日志事实源，不改变历史日志中的 `actor_user_id` 语义。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `product-usage-logging`: 管理端日志查询 API 与日志审计页面需要明确操作者筛选的用户候选、显示值与 `actor_user_id` 过滤语义。
- `web-client`: 管理端列表页横切一致性需要覆盖 `/admin/logs` 操作者可搜索下拉后的筛选、反馈、分页和移动端布局要求。

## Impact

- **Backend/API:** 优先复用 `GET /api/v1/admin/users` 与 `GET /api/v1/admin/logs?actor_user_id=...`；若新增候选 API，需同步 OpenAPI、Orval、API 文档与权限测试。
- **Web/Admin:** 修改 `/admin/logs` 筛选区，复用或扩展 `SearchableSelect` / Design System 组件，补充前端交互测试。
- **Miniapp:** 无影响。
- **Database/Storage:** 无 schema 和对象存储变更。
- **Security:** 用户候选数据必须走系统管理员鉴权，不暴露密码、Token、敏感备注或非必要用户字段。
- **Testing:** 需覆盖候选搜索、选择、清空、重置、异常态、同名区分、`actor_user_id` 请求参数和 admin-list 横切 AC。
