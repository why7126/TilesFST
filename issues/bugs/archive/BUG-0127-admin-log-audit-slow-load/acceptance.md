---
bug_id: BUG-0127-admin-log-audit-slow-load
acceptance_status: passed
created_at: 2026-08-11 08:50:48
updated_at: 2026-08-12 00:15:15
severity: medium
related_requirement:
related_bug:
source_change: fix-admin-log-audit-slow-load
source_sprint: sprint-022
---

# 验收标准

## 回归验收

### AC-001 默认首屏列表响应达到目标性能

**Given** 日志表中存在接近生产规模的数据量  
**When** 系统管理员打开管理后台“日志审计”页面并使用默认时间范围  
**Then** `/api/v1/admin/logs` 列表接口应在目标响应时间内返回列表数据  
**And** 列表首屏不应被摘要指标聚合明显阻塞  
**And** 响应结构应保持兼容，除非 OpenSpec Change 明确调整前后端契约。

### AC-002 常用筛选条件语义保持一致

**Given** 管理员按日志类型、时间范围、状态、操作者、路径 / Request ID 或 Task Trace ID 查询日志  
**When** 后端执行优化后的列表查询  
**Then** 返回的 `items`、`total`、分页参数和排序顺序应与当前业务语义一致  
**And** `created_at DESC` 排序在三类日志混合结果中保持稳定  
**And** 权限边界仍只允许系统管理员访问日志审计接口。

### AC-003 指定日志类型避免无必要三表扫描

**Given** 查询参数指定 `log_type=request`、`usage_event` 或 `audit`  
**When** 后端构造日志列表查询  
**Then** 查询应优先落到对应单表或等价低成本路径  
**And** 不应继续无条件扫描另外两类日志表  
**And** 对应筛选字段应尽量下推到单表查询条件。

### AC-004 摘要指标不再拖慢列表首屏

**Given** 页面需要展示 `today_logs`、`api_errors`、`slow_requests`、`sensitive_ops`  
**When** 日志列表接口加载首屏数据  
**Then** 摘要指标应通过缓存、独立接口、异步加载或低成本聚合策略获取  
**And** 摘要失败或延迟不应阻断列表数据展示  
**And** 指标口径变化必须在 API 文档和测试中明确。

### AC-005 SQLite 与 MySQL 索引和迁移保持一致

**Given** 修复涉及日志表索引或查询字段  
**When** 更新 SQLite schema、SQLite migration、MySQL schema 或 MySQL compatibility migration  
**Then** `request_logs`、`usage_events`、`audit_logs` 的常用筛选索引应在两类数据库中保持一致  
**And** 数据库设计文档应同步说明新增或调整的索引  
**And** 迁移应幂等，不破坏既有日志数据。

### AC-006 测试覆盖性能回归风险

**Given** 日志审计查询已完成优化  
**When** 运行后端测试和必要的前端测试  
**Then** 应覆盖列表筛选、分页、摘要指标和日志详情入口的既有功能  
**And** 应补充查询结果等价、索引存在性或查询计划保护测试  
**And** 应记录 SQLite 本地/demo 与 MySQL 生产等价环境下的验证方式。

## 验收返修证据

- 2026-08-11：`uv run pytest src/backend/tests/test_product_usage_logging.py` 通过，19 passed。
- 2026-08-11：`python scripts/validate-openspec-language.py` 通过。
- 2026-08-11：`openspec validate fix-admin-log-audit-slow-load --strict` 通过。
- 2026-08-11：SQLite demo `EXPLAIN QUERY PLAN` 显示 `log_type=request` 且 `client_type + created_at` 条件下命中 `idx_request_logs_client_created`，未生成三表 UNION。
- 2026-08-11 23:36:00：MySQL 8.2.0 验证库 `tilesfst` 已补齐 `idx_request_logs_client_created`、`idx_request_logs_result_created`、`idx_usage_events_client_created`、`idx_usage_events_result_created`、`idx_audit_logs_created`。
- 2026-08-11 23:36:00：MySQL 单类型 `request` / `usage_event` / `audit` 查询的 `EXPLAIN` 均只访问对应日志表；混合日志 `EXPLAIN` 中 request 子查询命中 `idx_request_logs_client_created`，usage_event 子查询命中 `idx_usage_events_client_created`，audit 子查询命中 `idx_audit_logs_created`。
- 剩余风险：当前 MySQL 验证库 `request_logs` / `usage_events` / `audit_logs` 均为 0 行，上述 evidence 证明 schema/migration 与查询形态，不替代真实生产数据量下的响应耗时或慢查询量化证据。
- API response schema 未变化；无需 Orval。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 00:15:15
accepted_by: workflow-sync
source_change: fix-admin-log-audit-slow-load
source_sprint: sprint-022
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

