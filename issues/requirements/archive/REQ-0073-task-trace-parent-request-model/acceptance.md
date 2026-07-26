---
requirement_id: REQ-0073-task-trace-parent-request-model
title: Task Trace 主请求与子请求关联模型 - 验收标准
status: done
owner: product
created_at: 2026-07-26 13:03:43
updated_at: 2026-07-26 17:30:55
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags:
  - media-upload
---

# 验收标准

## 功能 AC

- [ ] AC-001 每个由 API 请求触发的 Task Trace MUST 记录触发它的主请求 `request_id`，字段语义为 `parent_request_id`。
- [ ] AC-002 `parent_request_id` MUST 来自后端请求上下文，不得信任前端传入值。
- [ ] AC-003 OpenSpec design MUST 明确 `parent_request_id` 采用独立字段还是 metadata 结构化字段，并说明 SQLite/MySQL 兼容性、索引策略和迁移边界。
- [ ] AC-004 如果新增 `task_traces.parent_request_id` 独立字段，MUST 同步 schema、迁移、Pydantic Schema、Repository、数据库文档和测试。
- [ ] AC-005 如果采用 metadata 结构化字段，MUST 定义稳定 JSON 结构、读取兼容策略和缺失字段兜底，不得依赖临时 key 约定。
- [ ] AC-006 一个主请求触发多个 Task Trace 时，系统 MUST 保留一对多关系，并在日志详情中区分多个任务摘要。
- [ ] AC-007 有请求上下文的 task span MUST 写入当前 `request_id`。
- [ ] AC-008 无直接请求上下文的后端内部 span MAY 继承 `parent_request_id` 或将 `request_id` 标为空，但 MUST 保留 `task_trace_id`、span 顺序、状态和耗时。
- [ ] AC-009 所有任务型接口 MUST 使用同一 `task_trace_id` 串联 request logs、usage events、audit logs、Task Trace 和 task spans。
- [ ] AC-010 后端生成或确认 `task_trace_id` 后，相关响应、日志、审计事件和 span MUST 使用同一个值。
- [ ] AC-011 前端携带 `task_trace_id` 时，后端 MUST 校验格式、权限边界和任务归属；不可信或非法值不得直接落库。
- [ ] AC-012 缺失或非法 `task_trace_id` MUST 不影响主请求日志落库，并应返回或记录明确的可观测错误摘要。
- [ ] AC-013 日志详情 MUST 能从主请求 `request_id` 展示关联 Task Trace 摘要或入口。
- [ ] AC-014 Task Trace 时间线 MUST 展示 span 关联的 `request_id`，并支持定位到对应请求日志详情。
- [ ] AC-015 日志查询能力 SHOULD 支持按 `request_id`、`parent_request_id`、`task_trace_id` 定位同一任务链路。
- [ ] AC-016 当日志缺少 `task_trace_id`、Task Trace 缺少 `parent_request_id` 或 span 缺少 `request_id` 时，API 和页面 MUST 安全兜底，不得展示空状态错误或误导性关联。
- [ ] AC-017 图片、视频、文件上传 MUST 作为首批验证场景，上传主请求 MUST 生成或绑定 `task_trace_id` 并记录 `parent_request_id`。
- [ ] AC-018 上传相关 span MUST 至少覆盖后端接收、文件校验、对象存储写入、数据库落库、响应返回等节点，并尽量写入当前 API 请求 `request_id`。
- [ ] AC-019 `parent_request_id`、`task_trace_id`、span `request_id` 的查询路径 MUST 索引友好，避免以无界 metadata 模糊扫描作为主查询方式。
- [ ] AC-020 历史数据 MAY 不迁移，但新增 API 字段和页面展示 MUST 兼容历史缺失字段。
- [ ] AC-021 任务链路查询 MUST 仅系统管理员可访问，非系统管理员直链访问 MUST 返回 403 或管理端无权限页。
- [ ] AC-022 `request_id`、`parent_request_id`、`task_trace_id` 只用于追踪与定位，不得作为权限判断依据。
- [ ] AC-023 任务追踪数据 MUST 不保存 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env` 内容、真实客户数据、内部绝对路径或完整敏感请求体。
- [ ] AC-024 若新增或调整日志详情 / 任务追踪 API 字段，MUST 同步 OpenAPI、Orval、`docs/03-api-index.md`、错误码文档和后端/前端测试。
- [ ] AC-025 管理端日志详情的 Task Trace 分组 MUST 清晰展示主请求、任务标识、任务状态、span 列表和关联请求；复制或跳转反馈不得造成布局位移。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 MinIO 未写入、回显失败、Nginx 413、legacy 双目录类缺陷；并承接 `docs/knowledge-base/retrospectives/sprint-010-retrospective.md` 对上传链路多层配置漂移的复盘。

- [ ] AC-XCUT-001 图片、视频、文件上传控件 MUST 保持 `idle → uploading → done / failed` 状态机，且上传状态变化 MUST 写入或关联同一 `task_trace_id`。
- [ ] AC-XCUT-002 上传成功后同会话 MUST 即时回显缩略图、文件卡片或媒体结果；失败 MUST 在控件内展示错误，不能只依赖全局 toast。
- [ ] AC-XCUT-003 Docker Web 入口 `http://localhost:3000` MUST 覆盖上传边界文件验收：小文件成功、超限文件返回统一错误码，且不得只验证后端 `:8000`。
- [ ] AC-XCUT-004 上传链路 MUST 继续走后端鉴权和对象存储适配层，禁止前端直连未授权对象存储或写入 legacy `data/uploads/`。
- [ ] AC-XCUT-005 上传变更 MUST 同步有效限制来源，包括前端提示、后端校验、系统设置、Nginx / 代理和对象存储策略；测试应覆盖至少一个边界文件场景。
