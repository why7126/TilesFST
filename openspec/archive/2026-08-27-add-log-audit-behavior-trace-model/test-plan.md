---
change_id: add-log-audit-behavior-trace-model
source_requirement: REQ-0124-log-audit-behavior-trace-model
sprint: sprint-026
created_at: 2026-08-25 22:47:46
updated_at: 2026-08-25 22:47:46
---

# 测试计划

## 后端

- `pytest` 覆盖 usage event 写入 `behavior_trace_id` / `behavior_event_id`。
- `pytest` 覆盖界面触发同一行为产生多个 request logs，并通过 `behavior_trace_id` 查询。
- `pytest` 覆盖直接 API 调用缺少行为上下文时仍生成 `request_id`，且任务链路通过 `parent_request_id` 可查。
- `pytest` 覆盖日志审计按 `behavior_trace_id`、`request_id`、`task_trace_id` 查询和详情组合。
- `pytest` 覆盖非法/超长链路字段、敏感字段脱敏、旧日志空字段兼容和非 admin 权限拒绝。

## 数据库

- SQLite schema 与 migration 测试覆盖新增字段、可空语义、索引和幂等执行。
- MySQL baseline / migration 或 drift check 测试覆盖新增字段和索引。
- 查询计划或等价测试证明行为链路查询不依赖 metadata JSON 全表扫描作为主路径。

## Web 管理端

- Vitest / Testing Library 覆盖 `/admin/logs` 三类 ID 筛选入口、分页重置和 API 参数。
- 前端测试覆盖详情中的行为事件、请求、任务链路和“流程节点”展示。
- 前端测试覆盖无行为来源空态、长 ID 截断、复制 fixed toast、敏感字段不展示和分页 DOM。

## 文档与生成物

- OpenAPI 生成或校验通过。
- Orval 生成物同步；若没有对外 schema 变化，记录不需要生成的依据。
- 数据库文档与 API 文档同步。
- 运行 `python scripts/validate-openspec-language.py`。
