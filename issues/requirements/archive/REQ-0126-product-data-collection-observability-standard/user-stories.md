---
requirement_id: REQ-0126-product-data-collection-observability-standard
title: 建立通用产品数据采集与链路观测规范 - 用户故事
created_at: 2026-08-26 10:20:20
updated_at: 2026-08-26 10:23:12
---

# 用户故事

## US-001 产品设计阶段明确采集范围

作为产品负责人，我希望在新产品或新模块设计阶段就能引用统一的数据采集规范，以便明确哪些页面访问、业务点击、搜索筛选、详情查看、保存删除、上传分享等行为必须采集，避免上线后才补埋点。

验收要点：

- 规范覆盖 Web 管理端、店主端、小程序、App 和后端 API。
- 规范明确“所有可命名业务行为必须采集，纯 UI 噪音可排除”的口径。
- 规范列出可采集行为、可排除行为和 N/A 记录要求。

## US-002 后端统一记录所有业务 API 请求

作为后端开发，我希望所有业务 API 请求都按统一规则写入 `request_logs`，以便任何接口异常都能通过服务端可信 `request_id` 排障。

验收要点：

- 规范要求所有业务 API 请求 MUST 写入 `request_logs`。
- 规范列出健康检查、静态资源、OpenAPI 文档资源、预检 OPTIONS、内部探活等可排除项。
- 规范明确请求日志写入失败不得阻断主业务响应。

## US-003 前端和客户端统一透传行为链路

作为 Web、小程序或 App 开发，我希望有统一的行为事件 helper / SDK 规则，以便生成 `behavior_trace_id`、`behavior_event_id` 并在行为触发的 API 请求中透传。

验收要点：

- 规范定义 `behavior_trace_id`、`behavior_event_id` 和 `parent_behavior_event_id` 的语义。
- 规范明确行为采集失败不阻断主业务流程。
- 规范明确小程序、店主端、App 和 Web 管理端均需遵守同一链路模型。

## US-004 直接 API 调用保持独立排障入口

作为外部 API 调用方或运维人员，我希望直接 API 调用不需要伪造行为事件，也能从 `request_logs.request_id` 进入任务链路和流程节点。

验收要点：

- 规范明确直接 API 调用允许 `behavior_trace_id` 为空。
- 规范明确直接 API 调用不强制写入 `usage_events`。
- 规范明确直接 API 调用通过 `request_logs.request_id -> task_traces.parent_request_id -> task_trace_spans` 排障。

## US-005 任务类接口按分级策略接入 Task Trace

作为研发和 QA，我希望知道哪些接口必须拆 Task Trace，哪些普通接口只保留 request log 即可，以便平衡排障价值和开发成本。

验收要点：

- 规范采用 Task Trace 分级覆盖策略。
- 长耗时、多步骤、批量、异步、导入导出、上传 / 对象存储、第三方依赖、失败需定位节点和高风险写操作 MUST 接入 Task Trace。
- 普通简单写操作 MAY 只保留 request log，并需说明不接入 Task Trace 的理由。

## US-006 数据留存和脱敏边界可执行

作为安全和运维负责人，我希望规范明确日志、行为事件、任务链路和聚合数据的默认保留周期，以及敏感字段禁止采集规则，以便控制数据库成本和隐私风险。

验收要点：

- `request_logs` 默认保留 90 天。
- `usage_events` 明细默认保留 180 天。
- `task_traces` / `task_trace_spans` 默认保留 90 天。
- 聚合数据默认保留 1 年。
- 规范明确超期删除或匿名化，不允许无限期保留明细。
- 规范禁止采集 Authorization、Cookie、Token、真实密钥、完整请求体、完整响应体、本机路径、完整内部对象 key 和真实客户敏感数据。

## US-007 后续需求和 Change 可引用规范验收

作为 AI Agent、研发负责人和评审者，我希望该规范能作为后续 REQ、BUG、OpenSpec Change 和 Sprint 验收的事实依据，以便新产品从开发阶段就接入数据采集和链路观测。

验收要点：

- 规范提供新产品接入清单。
- 规范明确 API、DB、OpenAPI/Orval、测试和文档同步要求。
- 后续观测类、日志类、上传类、批量任务类需求可引用该规范作为验收依据。
