---
change_id: update-admin-list-column-pagination-consistency-contract
status: archived
type: update
created_at: 2026-08-12 14:48:56
updated_at: 2026-08-12 21:38:05
source_requirement: REQ-0112-admin-list-column-pagination-consistency-contract
source_sprint: sprint-023
impact:
  backend: conditional
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: conditional
capabilities:
  new: []
  modified:
    - design-system
    - testing
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-022-retrospective.md
cross_cutting_tags:
  - admin-list
prototype_strategy:
  html: none
  png: none
  context: issues/requirements/archive/REQ-0112-admin-list-column-pagination-consistency-contract/prototype/web/context.md
---

# Change Trace

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-08-12 21:38:05 | opsx.archive | Change 已归档到 `openspec/archive/2026-08-12-update-admin-list-column-pagination-consistency-contract/`，REQ-0112 验收通过并迁入 archive |
| 2026-08-12 14:55:48 | opsx.apply | 落地管理端列表列展示与分页契约；更新共享模板、代表页样式/测试、knowledge-base 与任务清单 |
| 2026-08-12 14:48:56 | req.opsx | 从 REQ-0112 创建 OpenSpec Change，状态为 proposed |

## UI 证据清单

- [x] UI Contract 已写入 design.md。
- [x] Skeleton 策略已说明：本 Change 不新增独立页面原型，以代表页面契约和测试证据验收。
- [x] 1440×1024 证据：本次未启动浏览器截图；以 Vitest DOM 结构、CSS 源码断言和代表页测试作为等价自动化证据，归档前如需要人工视觉验收再补截图。
- [x] 横向滚动 / 窄屏 sticky 操作列证据：`AdminListPage`、Banner、日志审计和用户管理测试覆盖 sticky action cell、分页 DOM 与 nowrap CSS；`AdminMobileAdaptation.test.ts` 保留日志审计移动/层级断言。
- [x] Mock/API 边界已写入 design.md；本次未改 API、Pydantic Schema、OpenAPI 或 Orval。

## Apply 结果

| 项 | 结论 |
|---|---|
| 代表页盘点 | Banner、日志审计、用户管理均使用后端分页参数和 `page-summary` / `page-right`；Banner 与日志审计已有 sticky action cell，用户管理作为分页基准页保留 sticky action cell。 |
| Web 实现 | `AdminListPage` 增加 `displayMode`、`data-admin-column-display`、nowrap/truncate/multiline exception class；代表页 CSS 明确默认 nowrap 与有效期例外。 |
| API / Orval | N/A，本次未修改接口请求或响应结构。 |
| 测试 | `pnpm --dir src/web test -- admin-list-page UserManagementPage LogAuditPage BannerManagementPage` 通过，62 个 test files、357 个 tests。 |
| 横切 gate | `admin-list` 已覆盖；未新增筛选下拉控件，`admin-filter-dropdown` 保持既有共享组件策略。 |
