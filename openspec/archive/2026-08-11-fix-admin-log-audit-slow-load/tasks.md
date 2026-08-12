---
change_id: fix-admin-log-audit-slow-load
status: proposed
created_at: 2026-08-11 09:06:06
updated_at: 2026-08-11 23:36:00
---

# 任务清单

- [x] 1. 日志列表查询路径优化
  - [x] 1.1 为 `log_type=request`、`log_type=usage_event`、`log_type=audit` 增加对应单表或等价低成本查询路径
  - [x] 1.2 将时间范围、操作者、client type、状态或结果、request id、Task Trace ID、路径或关键字等筛选条件尽量下推到各日志表子查询
  - [x] 1.3 保持 `items`、`total`、`page`、`page_size`、`created_at DESC` 排序和现有响应字段兼容
  - [x] 1.4 为混合日志分页保留稳定排序和总数语义，避免优化后漏查、重复或顺序漂移
- [x] 2. 摘要指标解耦与前端加载策略
  - [x] 2.1 调整 `today_logs`、`api_errors`、`slow_requests`、`sensitive_ops` 的获取方式，使列表首屏不被全量聚合明显阻塞
  - [x] 2.2 若新增或调整 metrics endpoint、响应 Schema 或查询参数，同步 OpenAPI、Orval 和 API 文档
  - [x] 2.3 管理端日志审计页支持指标独立加载、失败或延迟态，列表数据可先展示
  - [x] 2.4 保持系统管理员权限边界，非管理员不得访问日志列表或指标数据
- [x] 3. SQLite/MySQL 索引、迁移与数据库文档
  - [x] 3.1 补齐 SQLite schema 和 migration 中日志查询常用索引，至少评估 `client_type + created_at`、`result + created_at`、`audit_logs(created_at)`
  - [x] 3.2 补齐 MySQL schema 和兼容 migration 中同等索引，确保命名、字段和排序语义可迁移
  - [x] 3.3 更新 `docs/04-database-design.md` 日志表索引说明
  - [x] 3.4 确认迁移幂等且不破坏既有日志数据
- [x] 4. 测试与性能证据
  - [x] 4.1 增加后端测试覆盖默认首屏、日志类型、时间范围、状态或结果、操作者、request id、Task Trace ID、路径或关键字筛选和分页
  - [x] 4.2 增加查询结果等价测试，覆盖混合日志与单类型日志的排序、总数和分页语义
  - [x] 4.3 增加索引存在性、迁移幂等或查询计划保护测试
  - [x] 4.4 记录 SQLite demo 数据下优化前后响应耗时和 `EXPLAIN QUERY PLAN` 摘要
  - [x] 4.5 记录生产或生产等价 MySQL 的 `EXPLAIN` / 慢查询摘要，若暂不可得需写明原因和剩余风险
- [x] 5. 文档、验收与知识沉淀
  - [x] 5.1 按需更新 `docs/03-api-index.md`、`docs/04-database-design.md`、OpenAPI 和 Orval；若无需 Orval，记录原因
  - [x] 5.2 回填 `BUG-0127` acceptance 的性能、查询计划、索引和回归测试 evidence
  - [x] 5.3 必要时补充 `docs/knowledge-base/incidents/` 或 best practice，沉淀日志审计查询性能经验
  - [x] 5.4 运行 `python scripts/validate-openspec-language.py`
  - [x] 5.5 运行 OpenSpec 校验

## 校验记录

- 2026-08-11：`uv run pytest src/backend/tests/test_product_usage_logging.py` 通过，19 passed；覆盖日志列表、详情、权限、Task Trace、observability、typed source 与索引迁移保护。
- 2026-08-11：`python scripts/validate-openspec-language.py` 通过。
- 2026-08-11：`openspec validate fix-admin-log-audit-slow-load --strict` 通过。
- 2026-08-11：SQLite demo `EXPLAIN QUERY PLAN`：`log_type=request` 且 `client_type + created_at` 条件下命中 `idx_request_logs_client_created`，未出现三表 UNION；此前 BUG 记录的旧统一 UNION 查询曾出现 `USE TEMP B-TREE FOR ORDER BY`。
- 2026-08-11：本 Change 未改变 `/api/v1/admin/logs` response schema；无需运行 Orval。生产或生产等价 MySQL 的 `EXPLAIN` / 慢查询摘要需在具备目标环境连接后补充为发布 evidence。

## 验收返修记录

- 2026-08-11 23:36:00：验收反馈指出本地 MySQL 验证环境未应用 BUG-0127 新增索引，无法作为通过 evidence。已在 `tilesfst` MySQL 8.2.0 验证库执行等价索引补齐，确认 `idx_request_logs_client_created`、`idx_request_logs_result_created`、`idx_usage_events_client_created`、`idx_usage_events_result_created`、`idx_audit_logs_created` 均存在。
- 2026-08-11 23:36:00：重新执行 MySQL `EXPLAIN`。单类型 request / usage_event / audit 查询仅访问对应日志表；混合查询的 request 子查询命中 `idx_request_logs_client_created`，usage_event 子查询命中 `idx_usage_events_client_created`，audit 子查询命中 `idx_audit_logs_created`。当前验证库三张日志表均为 0 行，因此该 evidence 证明 schema/migration 与查询形态，不替代生产真实数据量耗时证据。
