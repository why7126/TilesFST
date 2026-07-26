---
note: workflow-sync — workflow-sync 自动同步 — 6/6 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-012
title: Sprint 012 API 请求日志 Request Snapshot 与客户端请求身份增强
status: completed
lifecycle_stage: archive
created_at: 2026-07-26 15:15:24
updated_at: 2026-07-26 17:42:08
---

# Sprint 012 API 请求日志 Request Snapshot 与客户端请求身份增强

## 1. 目标

- 建立统一 Request Snapshot，让 API 请求日志能够还原 method、path、route template、query 白名单、body schema 摘要、资源 ID、状态码、错误码、耗时、操作者、客户端、环境和请求/响应时间。
- 在不保存原始敏感 body 的前提下，补齐可审计、可排障的请求输入上下文。
- 扩展管理端日志详情抽屉，按结构化分组展示 Snapshot，并保留 JSON 辅助视图、空态和脱敏状态。
- 统一 Web 管理端、店主 Web 前台和微信小程序普通 API 请求的 `client_type` 与客户端请求标识注入策略。
- 明确后端可信 `request_id` 与客户端请求标识边界，日志审计中可区分、展示和复制两类 ID。
- 将 Task Trace 从上传链路扩展到保存 SKU、批量操作、导入导出、媒体处理、异步任务和复杂查询等任务型接口，形成首批接入清单、统一 helper 和复杂任务追踪标识反馈。
- 同步后端 API、SQLite/MySQL schema 或 metadata、OpenAPI/Orval、API/数据库文档与测试。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0071-request-snapshot-logging | API 请求日志统一 Request Snapshot | done | 5.0 人天 | archived `update-request-snapshot-logging`（2026-07-26 16:54:03） |
| REQ | REQ-0072-client-request-identity-standard | 前台后台与小程序统一客户端请求标识规范 | done | 5.0 人天 | archived `standardize-client-request-identity`（2026-07-26 15:48:23） |
| REQ | REQ-0073-task-trace-parent-request-model | Task Trace 主请求与子请求关联模型 | done | 3.0 人天 | archived `fix-task-trace-parent-request-model`（2026-07-26 17:18:10） |
| REQ | REQ-0074-task-trace-coverage-expansion | 任务型接口 Task Trace 覆盖扩展 | done | 5.0 人天 | archived `update-task-trace-coverage-expansion`（2026-07-26 15:57:22） |
| REQ | REQ-0075-audit-log-task-trace-linking | 审计操作日志补齐任务链路关联字段 | done | 3.0 人天 | archived `link-audit-logs-to-task-trace`（2026-07-26 17:12:37） |
| REQ | REQ-0076-observability-dashboard | 日志审计与链路观测仪表 | done | 5.0 人天 | archived `add-observability-dashboard`（2026-07-26 16:56:31） |

BUG：无 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：已回填 6 个范围项关联 Change；6 archived，0 applied，0 in_progress，0 proposed。所有已纳入范围项均已关联 Change；执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 指标 | 值 |
|---|---:|
| 开发 | 2 |
| 测试 | 1 |
| 容量 | 30 人天 |
| 估算 | 26.0 人天 |
| 容量占用 | 86.67% |
| fix 缓冲 | 4.0 人天 / 13.33% |

容量门禁：通过。当前范围包含 REQ-0071、REQ-0072、REQ-0073、REQ-0074、REQ-0075 与 REQ-0076，占用 26.0 / 30 人天，容量占用 86.67%，低于容量上限；fix 缓冲 4.0 人天 / 13.33%，低于 30% 建议值但未触发容量硬阻断。apply 时仍需控制范围，不纳入外部 APM、历史回填、全文检索、完整原始请求/响应体保存、复杂 BI、外部分布式链路追踪平台、全量历史接口覆盖或新增导入导出业务能力。

## 4. 里程碑

| 阶段 | 目标日期 | 交付物 |
|---|---|---|
| 契约设计落地 | 2026-07-29 18:00:00 | Request Snapshot Schema、route template 降级策略、query/body 白名单与脱敏策略 |
| 后端与数据库实现 | 2026-08-01 18:00:00 | Snapshot builder、日志服务/仓储、SQLite/MySQL schema 或 metadata 兼容、日志详情 API |
| 跨端请求身份实现 | 2026-08-03 18:00:00 | Web 管理端、店主 Web、小程序请求封装注入 `client_type` 与客户端请求标识 |
| 管理端实现 | 2026-08-05 18:00:00 | 日志详情抽屉 Snapshot 分组、请求身份字段展示、JSON 辅助视图、空态与脱敏状态 |
| 验收收尾 | 2026-08-08 18:00:00 | OpenAPI/Orval/docs/tests 同步，pytest/Vitest/OpenSpec 校验记录 |

## 5. 风险

| 风险 | 影响 | 应对 |
|---|---|---|
| FastAPI middleware 获取 route template 时机不稳定 | 聚合统计和排障字段可能为空 | 实现明确降级枚举，测试覆盖 matched / unmatched 路由 |
| Snapshot 字段过多导致 metadata 膨胀 | 日志详情变慢或存储成本上升 | body 仅保存 schema 摘要、长度和安全字段；长字段截断 |
| SQLite 与 MySQL JSON 行为差异 | 本地通过但生产查询或展示异常 | 查询字段优先索引列；JSON 用于详情展示，生产字段需说明索引或不索引理由 |
| 敏感字段漏记 | 审计日志暴露密钥、Cookie、Token 或内部路径 | 后端黑名单、白名单、脱敏和截断为最终安全边界，测试覆盖敏感字段不落库 |
| 管理端只展示 JSON | 管理员仍需人工拼接排障信息 | 详情抽屉必须结构化展示 Snapshot，JSON 只作辅助 |
| 客户端请求标识与可信 `request_id` 边界混淆 | 排障时误信任可伪造客户端字段 | 后端继续生成可信 `request_id`，客户端 ID 独立存储和展示，字段命名与文案必须区分 |
| 三端请求封装遗漏 | 日志中 `client_type` 仍回退为默认值 | Web 管理端、店主 Web、小程序分别补测试或 smoke，覆盖 `web_admin`、`web_catalog`、`wechat_miniapp` |
| 长请求 ID 撑破日志列表 | 管理端表格和移动端布局回归 | 列表单行截断、详情完整展示、复制走 fixed toast，按 admin-list gate 回归 |

## 6. 知识库承接

- 承接 sprint-010 复盘行动：生产 smoke 在 apply 中段落盘，不等 archive 才补证据。
- 承接 sprint-010 复盘行动 A-003：容量超过 100% 时必须列出可移出项；本 Sprint 当前容量 33.33%，无超载。
- 承接 sprint-010 复盘行动 A-004：涉及生产 DB/API drift 的变更应前置 smoke evidence stub。
- 承接 sprint-010 复盘中“生产 DB/API drift”经验：SQLite demo 与 MySQL production schema 必须同步验证。
- 承接 sprint-010 复盘中“Admin UI smoke matrix”经验：日志详情抽屉需验证桌面和移动端可滚动、可关闭、无崩溃。
- 承接 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`：日志审计列表新增请求身份字段后，分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm` 和移动端不溢出约束必须保持一致。

## 7. 横切预防清单

| 检查项 | 要求 |
|---|---|
| knowledge-base gate | REQ-0072 命中 `admin-list`，日志审计列表变更必须承接列表页一致性最佳实践 |
| api-contract | 日志详情 API 新增 Snapshot 字段必须同步 OpenAPI / Orval |
| database | SQLite demo 与 MySQL production schema 或 metadata 兼容策略必须写入 docs |
| security | Snapshot 不得保存 Authorization、Cookie、密码、Token、密钥、DSN、MinIO secret、内部路径、原始文件名或原始敏感 body |
| admin-log-detail | 日志详情抽屉必须展示 Snapshot 分组、JSON 辅助视图、空态和 metadata 解析失败兜底 |
| client-request-identity | 三端普通 API 请求必须统一 `client_type` 和客户端请求标识；服务端可信 `request_id` 不得被客户端覆盖 |
| task-trace-coverage | 首批任务型接口清单必须至少评估保存 SKU、批量操作、导入导出、媒体处理、异步任务和复杂查询六类场景，并标注接入优先级、任务类型、关键步骤、预期 span 和未纳入原因 |
| complex-task-feedback | 管理端复杂任务成功、失败、处理中或部分成功反馈应展示或支持复制 `task_trace_id`；无 trace 时保持旧交互，不显示空错误态 |
| admin-list | 请求 ID 长字段单行截断、完整复制、fixed toast、分页 DOM 与指标卡 DOM 必须保持一致 |
| testing | 后端覆盖 route template、query/body 摘要、敏感字段不落库、错误请求上下文；前端覆盖 Snapshot 展示和空态 |

## 8. 依赖

```text
REQ-0071-request-snapshot-logging
└── update-request-snapshot-logging
    ├── product-usage-logging spec delta
    ├── Request Snapshot Schema / builder
    ├── route_template 获取与降级
    ├── query/body 白名单、摘要、脱敏、截断
    ├── request_logs metadata 或结构化字段兼容
    ├── 管理端日志详情 API 与抽屉展示
    ├── OpenAPI / Orval / docs 同步
    └── backend pytest / frontend Vitest / OpenSpec 校验

REQ-0072-client-request-identity-standard
└── standardize-client-request-identity
    ├── product-usage-logging / web-client / api-governance spec delta
    ├── 后端可信 request_id 与独立 client_request_id 边界
    ├── Web 管理端、店主 Web 与小程序 request 封装注入
    ├── 日志审计列表/详情请求身份字段展示与复制反馈
    ├── SQLite/MySQL schema、OpenAPI、Orval、docs/tests 同步
    └── admin-list 横切 AC 与小程序 fallback 重试标识策略

REQ-0074-task-trace-coverage-expansion
└── update-task-trace-coverage-expansion
    ├── product-usage-logging spec delta
    ├── 首批任务型接口候选清单与优先级
    ├── Task Trace helper / service / repository 扩展
    ├── 同步、异步、批量任务 span 接入
    ├── 管理端复杂任务追踪标识反馈
    ├── API / DB / OpenAPI / Orval / docs 同步
    └── backend pytest / Web Vitest / smoke evidence stub
```

## 9. 发布计划

本 Sprint 适合作为平台日志治理增强发布。若实现阶段只扩展日志详情响应和 metadata，不改变公开业务 API 行为，可随管理端和后端版本一并发布；若新增数据库字段或索引，必须同步 SQLite/MySQL migration、备份/回滚边界和生产 smoke。REQ-0072 预计会新增或调整跨端请求头、响应头说明、日志字段和日志审计展示，必须同步 OpenAPI、Orval、`docs/03-api-index.md`、`docs/04-database-design.md`、API governance 文档和后端/前端/小程序测试。REQ-0074 预计会扩展 Task Trace helper、任务型接口 span 写入、管理端复杂任务反馈与日志审计详情，若新增响应字段或存储字段，必须同步 OpenAPI、Orval、SQLite/MySQL schema、数据库/API 文档和测试。REQ-0075 预计会补齐 audit log 与 Task Trace 的关联字段、敏感审计写入点接入清单和 audit 类型日志详情联动；若新增 `audit_logs` 字段、索引或响应字段，必须同步 SQLite/MySQL schema、OpenAPI、Orval、数据库/API 文档和测试。若新增错误码，必须同步错误码文档。该 Sprint 不包含外部 APM、日志全文检索、历史日志回填、完整请求/响应体保存、复杂 BI、全量历史接口覆盖、新增导入导出业务能力、全量审计历史补写或外部分布式链路追踪平台。

## 10. 关联文档

| 类型 | 路径 |
|---|---|
| REQ | `issues/requirements/archive/REQ-0071-request-snapshot-logging/` |
| REQ | `issues/requirements/archive/REQ-0072-client-request-identity-standard/` |
| REQ | `issues/requirements/archive/REQ-0073-task-trace-parent-request-model/` |
| REQ | `issues/requirements/archive/REQ-0074-task-trace-coverage-expansion/` |
| REQ | `issues/requirements/archive/REQ-0075-audit-log-task-trace-linking/` |
| REQ | `issues/requirements/archive/REQ-0076-observability-dashboard/` |
| Change | `openspec/archive/2026-07-26-update-request-snapshot-logging/` |
| Change | `openspec/archive/2026-07-26-standardize-client-request-identity/` |
| Change | `openspec/archive/2026-07-26-fix-task-trace-parent-request-model/` |
| Change | `openspec/archive/2026-07-26-update-task-trace-coverage-expansion/` |
| Change | `openspec/archive/2026-07-26-link-audit-logs-to-task-trace/` |
| Change | `openspec/archive/2026-07-26-add-observability-dashboard/` |
| 复盘 | `docs/knowledge-base/retrospectives/sprint-010-retrospective.md` |
| 复盘 | `docs/knowledge-base/retrospectives/sprint-012-retrospective.md` |
| 最佳实践 | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-26 17:42:08 | /sprint-exps | 生成 sprint-012 复盘并回链至 knowledge-base |
| 2026-07-26 17:36:09 | /sprint-archive | 6/6 Change 已归档，Sprint change → archive；AI usage post-command hook 已刷新为 actual（command_run_count=1，warning_count=0） |
| 2026-07-26 15:40:00 | /sprint-propose | REQ-0075 改纳入 sprint-012，关联 link-audit-logs-to-task-trace |
| 2026-07-26 15:34:18 | /sprint-propose | REQ-0074 改纳入 sprint-012，关联 update-task-trace-coverage-expansion |
| 2026-07-26 15:17:24 | /sprint-propose | 纳入 REQ-0072 与 standardize-client-request-identity |
| 2026-07-26 15:15:24 | /sprint-propose | 创建 sprint-012，纳入 REQ-0071 与 update-request-snapshot-logging |
