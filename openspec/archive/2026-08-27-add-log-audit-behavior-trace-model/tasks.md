---
change_id: add-log-audit-behavior-trace-model
source_requirement: REQ-0124-log-audit-behavior-trace-model
sprint: sprint-026
created_at: 2026-08-25 22:47:46
updated_at: 2026-08-25 23:20:00
---

# 任务清单

## 1. 数据库与模型

- [x] 1.1 盘点现有 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans` 字段、索引和迁移路径。
- [x] 1.2 为 `usage_events` 增加 `behavior_trace_id`、`behavior_event_id`，同步 SQLite schema、SQLite migration、MySQL baseline、MySQL migration / drift 修复路径。
- [x] 1.3 为 `request_logs` 增加 `behavior_trace_id`、`parent_behavior_event_id`，保持直接 API 调用和历史日志可空兼容。
- [x] 1.4 为 Task Trace 相关结构按需补齐 `behavior_trace_id`、span `request_id` 或等价查询字段，继续保留 `task_traces.parent_request_id` 语义。
- [x] 1.5 补齐 `behavior_trace_id`、`behavior_event_id`、`parent_behavior_event_id`、`request_id`、`parent_request_id`、`task_trace_id`、`created_at` 相关索引或等价查询优化。
- [x] 1.6 更新数据库设计文档，记录字段中文注释、可空约束、索引、SQLite / MySQL 类型映射、旧日志兼容和回滚边界。

## 2. 后端采集与 API

- [x] 2.1 在 usage event 接收路径校验并持久化 `behavior_trace_id` 与 `behavior_event_id`。
- [x] 2.2 在请求日志中间件或统一日志服务中采集 `behavior_trace_id` 与 `parent_behavior_event_id`，直接 API 调用保持为空。
- [x] 2.3 明确 ID 生成方、格式、长度、字符集、幂等策略和可信边界；客户端提供字段不得覆盖服务端可信 `request_id`。
- [x] 2.4 在任务入口继续写入 `task_traces.parent_request_id`，并在界面触发任务中同步或冗余 `behavior_trace_id`。
- [x] 2.5 扩展日志审计查询 API，支持 `behavior_trace_id`、`request_id`、`task_trace_id` 三类入口和链路详情组合。
- [x] 2.6 补齐敏感字段白名单、长度截断、错误摘要脱敏和禁止字段过滤。
- [x] 2.7 同步 OpenAPI、Orval、API 文档与错误码说明；若某内部字段不暴露，记录不需要 Orval 的依据。

## 3. Web 管理端

- [x] 3.1 在前端行为采集和请求封装中透传 `behavior_trace_id` / `behavior_event_id`，并确保埋点失败不阻断主流程。
- [x] 3.2 扩展 `/admin/logs` 查询入口，支持按 `behavior_trace_id`、`request_id`、`task_trace_id` 查询，并保持分页重置语义。
- [x] 3.3 扩展日志详情展示，呈现行为事件、API 请求、任务链路和“流程节点”的关系。
- [x] 3.4 按 `admin-list` gate 保持后端真实分页、长 ID 截断、统一筛选控件或等价 wrapper、fixed toast、空态和权限边界。
- [x] 3.5 确认页面不展示完整请求体、完整响应体、Header、Cookie、Authorization、Token、真实密钥、本机路径或完整内部对象 key。

## 4. 测试与验证

- [x] 4.1 后端测试覆盖界面触发一行为多请求的链路关联。
- [x] 4.2 后端测试覆盖直接 API 调用无行为链路但可通过 `request_id` 进入任务链路。
- [x] 4.3 后端测试覆盖 `task_traces.parent_request_id`、`task_trace_spans` 流程节点和三类 ID 查询。
- [x] 4.4 后端测试覆盖敏感字段脱敏、非法链路字段、旧日志空行为链路兼容和权限拒绝。
- [x] 4.5 数据库测试覆盖 SQLite / MySQL 字段、索引、迁移幂等和 MySQL 目标路径。
- [x] 4.6 前端测试覆盖链路筛选、详情展示、空态、复制 fixed toast、长 ID 截断和分页结构。
- [x] 4.7 运行 OpenSpec 校验、语言校验和受影响测试，并在 Change trace 中记录结果。

## 5. 文档与收尾

- [x] 5.1 更新 `docs/03-api-index.md`、`docs/04-database-design.md` 和相关治理文档或记录不适用原因。
- [x] 5.2 回填 REQ acceptance、Sprint acceptance-report 和 release-note 中 REQ-0124 的验收结论。
- [x] 5.3 归档前确认 `openspec/specs/` delta 可合并，且无 `openspec/changes/archive/` 旧路径残留。
