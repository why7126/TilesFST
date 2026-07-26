## 1. Backend Aggregation API

- [x] 1.1 确认链路观测接口形态：新增 `GET /api/v1/admin/logs/observability` 或扩展现有日志 summary，并在实现 trace 中记录选择理由。
- [x] 1.2 定义管理端链路观测查询参数与响应 Schema，覆盖时间范围、日志类型、客户端、任务类型、接口路径、状态 / 结果、`request_id` 和 `task_trace_id`。
- [x] 1.3 在日志 Service / Repository 中实现统一筛选口径，返回 summary、distributions、rankings 和 trace results。
- [x] 1.4 实现 Task Trace 聚合：任务状态分布、任务成功率、失败任务数、耗时分桶、慢任务排行和最慢 span 排行。
- [x] 1.5 实现请求观测聚合：接口请求量、错误量、错误率、慢请求排行和失败原因分布。
- [x] 1.6 实现客户端与行为事件分布，覆盖 `web_admin`、`web_catalog`、`miniapp`、`backend` 和未识别客户端。
- [x] 1.7 确保聚合接口仅管理员可访问，且所有返回值遵守敏感字段脱敏边界。

## 2. Database And Performance

- [x] 2.1 复核现有 request logs、usage events、audit logs、Task Trace 表结构和索引是否支撑聚合查询。
- [x] 2.2 如需新增索引或聚合字段，同步 SQLite schema、MySQL schema、迁移和数据库文档。
- [x] 2.3 确保聚合查询使用 Repository 或统一数据访问层，不在过滤前将全量日志加载到内存。
- [x] 2.4 明确慢请求、慢任务、默认时间范围、分位值或耗时分桶口径，并写入实现 trace。

## 3. Web Admin UI

- [x] 3.1 在 `/admin/logs` 或等价管理端入口增加链路观测模式，保留日志列表与详情追踪入口。（2026-07-26 已按用户要求从页面移除）
- [x] 3.2 复用管理端 Design System、Admin Shell、筛选、指标卡、表格、分页、详情抽屉和 fixed toast 模式。（2026-07-26 已按用户要求从页面移除观测模块）
- [x] 3.3 实现统一摘要指标、失败原因分布、客户端分布、任务状态分布、慢任务排行、最慢 span 排行、慢请求排行和追踪 ID 查询区。（2026-07-26 已按用户要求从页面移除）
- [x] 3.4 实现筛选联动，确保摘要、分布、排行和明细入口共享同一筛选条件。（2026-07-26 已按用户要求从页面移除观测模块，不再触发观测接口请求）
- [x] 3.5 实现排行项和追踪 ID 下钻，支持打开日志详情、Task Trace 时间线或相关记录集合。（2026-07-26 已按用户要求从页面移除排行下钻）
- [x] 3.6 实现空数据、加载失败、无权限、追踪 ID 未命中状态，并确保聚合失败不破坏基础日志列表查询。（2026-07-26 页面模块已移除；基础日志列表仍保留）

## 4. API Contract, Orval And Docs

- [x] 4.1 同步 OpenAPI response models、summaries、descriptions 和 tags。
- [x] 4.2 执行 Orval 生成 Web client methods 和 types，禁止手工编辑 generated files。
- [x] 4.3 更新 `docs/03-api-index.md`、`docs/04-database-design.md` 和适用错误码文档。
- [x] 4.4 若新增环境变量或系统设置项，同步 `.env.example`、部署文档和系统设置说明。

## 5. Tests And Acceptance

- [x] 5.1 后端测试覆盖聚合摘要、筛选、权限、脱敏、空数据、追踪 ID 命中 / 未命中和 SQLite / MySQL 兼容口径。
- [x] 5.2 前端测试覆盖页面渲染、筛选刷新、复制反馈、无权限、空态和分页结构；2026-07-26 删除页面观测模块后已移除排行下钻和观测加载失败用例。
- [x] 5.3 验证 `admin-list` 横切 AC：指标卡 DOM、分页 DOM、fixed toast、无 `window.confirm`。
- [x] 5.4 运行 1440x1024 与移动端管理端 smoke 或截图验收，覆盖摘要指标、筛选、排行、表格、详情入口和空态。（2026-07-26 已按用户要求移除页面观测模块，此项不再适用）
- [x] 5.5 运行相关后端 pytest、前端 Vitest / Testing Library、OpenSpec validate 和必要 Docker Compose smoke。

## 6. Trace And Workflow

- [x] 6.1 更新 Change trace，记录接口形态、UI 策略、指标口径、测试结果和 known limitations。
- [x] 6.2 同步 REQ / Change / Sprint 状态，确保进入 `/opsx-apply` 前该 Change 已纳入 Sprint 正式范围。
