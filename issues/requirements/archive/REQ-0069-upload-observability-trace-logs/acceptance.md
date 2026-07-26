---
requirement_id: REQ-0069-upload-observability-trace-logs
title: 任务链路追踪与审计日志查看 - 验收标准
status: done
owner: product
created_at: 2026-07-25 11:45:49
updated_at: 2026-07-26 11:56:45
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags:
  - admin-list
  - media-upload
---

# 验收标准

## 功能 AC

- [ ] AC-001 系统 MUST 为每一次可追踪业务任务生成或确认一个 `task_trace_id`，且该 ID 不包含用户原始文件名、手机号、密钥、业务敏感信息或可枚举自增序列。
- [ ] AC-002 后端请求日志、行为事件、审计操作和任务节点 MUST 能通过同一个 `task_trace_id` 关联。
- [ ] AC-003 每个任务节点 MUST 至少记录 `task_trace_id`、`task_type`、`span_name`、`status`、`started_at`、`duration_ms` 或等价结束时间。
- [ ] AC-004 任务节点 SHOULD 记录 `request_id`、`actor_user_id`、`client_type`、`resource_type`、`resource_id`、`error_code`、`summary` 和脱敏 metadata。
- [ ] AC-005 任务状态 MUST 覆盖 `processing`、`success`、`failed`、`timeout`、`cancelled`。
- [ ] AC-006 图片上传、视频上传、文件上传 MUST 作为首批 `task_type` 覆盖。
- [ ] AC-007 上传任务 MUST 至少记录前端选择文件、上传开始、请求体上传完成、后端接收、文件校验、对象存储写入、数据库记录、响应返回、前端完成或失败节点。
- [ ] AC-008 对 `BUG-0085` 的 99% 停留场景，系统 MUST 能统计从“前端请求体上传完成”到“后端响应完成”的耗时，并定位最慢节点。
- [ ] AC-009 上传失败 MUST 关联统一错误码或失败摘要，并能在任务时间线中标识失败节点。
- [ ] AC-010 任务追踪 MUST 不保存 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env` 内容、真实客户数据、内部绝对路径或完整敏感请求体。
- [ ] AC-011 管理端日志审计列表 MUST 支持按 `task_trace_id` 查询相关日志。
- [ ] AC-012 管理端日志审计列表 SHOULD 支持展示任务类型、任务状态、任务耗时或慢节点摘要。
- [ ] AC-013 日志详情 MUST 在存在 `task_trace_id` 时展示任务时间线，包含节点名称、耗时、状态、错误码、关联 `request_id` 和摘要。
- [ ] AC-014 日志详情 MUST 支持复制 `task_trace_id` 和关联 `request_id`，复制成功或失败反馈不得造成页面布局位移。
- [ ] AC-015 没有 `task_trace_id` 的普通日志 MUST 继续按现有日志详情展示，不出现空时间线错误。
- [ ] AC-016 实现阶段 MUST 在 OpenSpec design 中明确数据模型选择：扩展现有日志表、新增 `task_traces` / `task_trace_spans`，或组合方案。
- [ ] AC-017 SQLite demo 与生产 MySQL MUST 保持 schema 兼容，并为 `task_trace_id`、`task_type`、`created_at` 或等价查询字段建立索引。
- [ ] AC-018 若新增或调整日志列表/详情 API 字段，MUST 同步 OpenAPI、Orval、`docs/03-api-index.md`、错误码文档和后端/前端测试。
- [ ] AC-019 任务追踪查询 MUST 仅系统管理员可访问，非系统管理员直链访问 MUST 返回 403 或管理端无权限页。
- [ ] AC-020 任务追踪写入失败时 MUST 有降级策略，不得静默吞掉主业务错误；主业务失败时必须返回明确错误码。
- [ ] AC-021 上传日志 MUST 记录文件大小、媒体类型、业务类型、对象 key 前缀或脱敏对象标识，不得将原始文件名作为对象存储 key。
- [ ] AC-022 视频上传可记录后处理节点；若新增转码、压缩、多清晰度或封面生成增强能力，MUST 另走 OpenSpec Change。
- [ ] AC-023 管理端日志详情的任务时间线 UI MUST 作为独立分组展示，并在 1440x1024 视口下不遮挡基础信息、请求信息和 metadata JSON。
- [ ] AC-024 需求原型策略 MUST 至少提供日志详情时间线 HTML/context；PNG Golden Reference 可在后续设计确认后导出。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 管理端列表页一致性复发类缺陷。

- [ ] AC-XCUT-001 日志审计列表新增 `task_trace_id` 筛选后，分页 DOM MUST 对齐用户管理基准：左侧 `.page-summary`，右侧 `.page-right` 页码 + 每页条数。
- [ ] AC-XCUT-002 日志审计指标摘要 MUST 使用 `.metric-label` / `.metric-value` / `.metric-desc` 结构，不得只复用外层卡片后用裸 `strong` / `span` 承载数值。
- [ ] AC-XCUT-003 查询、复制 `task_trace_id` / `request_id`、打开详情或加载失败反馈 MUST 使用 fixed toast 或等价固定层，不得造成 hero、筛选区或表格纵向位移。
- [ ] AC-XCUT-004 N/A — 本需求首期日志审计列表只查询和查看任务时间线，不包含启停、删除、重置等危险状态变更；若后续新增清理、删除、导出等危险操作，MUST 使用 DS confirm modal。
- [ ] AC-XCUT-005 日志审计列表与详情实现 MUST 不调用 `window.confirm`；本期无确认操作时以静态检查或代码 review 说明 N/A。

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 MinIO 未写入、回显失败、Nginx 413、legacy 双目录类缺陷。

- [ ] AC-XCUT-006 图片、视频、文件上传控件 MUST 保持 `idle → uploading → done / failed` 状态机，且状态变化写入或关联同一 `task_trace_id`。
- [ ] AC-XCUT-007 上传成功后同会话 MUST 即时回显缩略图、文件卡片或媒体结果；失败 MUST 在控件内展示错误，不能只依赖全局 toast。
- [ ] AC-XCUT-008 Docker Web 入口 `http://localhost:3000` MUST 覆盖上传边界文件验收：小文件成功、超限文件返回统一错误码，且不得只验证后端 `:8000`。
- [ ] AC-XCUT-009 上传链路 MUST 继续走后端鉴权和对象存储适配层，禁止前端直连未授权对象存储或写入 legacy `data/uploads/`。
- [ ] AC-XCUT-010 上传变更 MUST 同步有效限制来源，包括前端提示、后端校验、系统设置、Nginx / 代理和对象存储策略；Sprint 010 复盘指出该链路多层配置易漂移。
