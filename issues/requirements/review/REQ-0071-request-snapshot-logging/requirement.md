---
requirement_id: REQ-0071-request-snapshot-logging
title: API 请求日志统一 Request Snapshot
terminal: multi
version: v1
status: approved
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0024-product-usage-logging
created_at: 2026-07-26 12:56:57
updated_at: 2026-07-26 13:10:46
---

# REQ-0071 API 请求日志统一 Request Snapshot

## 1. 需求背景

当前平台已基于 `REQ-0024-product-usage-logging` 建立产品使用行为埋点与接口请求日志能力，主请求日志已记录 `request_id`、用户、客户端、method、path、状态码、耗时、脱敏 IP、User-Agent、`task_trace_id` 等基础信息。

但现有日志 metadata 主要保存 `query_params` 与 path 摘要，无法稳定还原一次业务请求的输入上下文。排查错误请求、审计敏感操作或分析跨端调用链路时，仍需要在接口参数、业务资源、错误码、响应状态和客户端上下文之间人工拼接信息。

本需求要求在合规脱敏前提下建立统一 Request Snapshot，为前台 Web、后台管理端与微信小程序 API 请求提供一致的请求快照结构，提升审计、排障与后续数据治理能力。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 系统管理员 | 在日志详情中查看完整但已脱敏的请求上下文，判断操作来源与影响对象 |
| 开发 / 运维人员 | 通过 route template、资源 ID、错误码、耗时和客户端信息快速定位接口问题 |
| 企业内部运营人员 | 在授权范围内理解关键业务请求是否成功，以及失败原因摘要 |
| 产品负责人 | 基于一致的请求快照字段评估跨端 API 使用与异常分布 |

## 3. 范围

### 3.1 本期包含

- 建立统一 Request Snapshot 数据结构，覆盖 API 请求的请求侧、响应侧、操作者、客户端、环境与时间信息。
- 在后端请求日志采集链路中生成 Snapshot，并写入请求日志 metadata 或等价结构化字段。
- 为 query 与 body 建立白名单、摘要化、脱敏和截断策略，避免保存原始敏感 body。
- 记录业务资源标识，例如 `resource_type`、`resource_id`、`entity_type`、`entity_id` 或等价字段。
- 在管理端日志详情中展示 Snapshot 分组信息，使用户无需从多个位置拼接请求上下文。
- 明确前台 Web、后台管理端、微信小程序请求的一致字段与差异字段。
- 将 Snapshot 字段纳入后续 API、数据库、测试与安全实现约束。

### 3.2 本期不包含

- 保存完整原始请求体、完整响应体或未脱敏 Header。
- 接入外部 APM、链路追踪、日志平台或消息队列。
- 日志全文检索、复杂 BI、漏斗分析、实时监控大屏。
- 扩展运维级日志，例如 Nginx access log、容器 stdout、数据库慢查询日志。
- 对历史日志进行批量回填。
- 将敏感字段白名单交由前端配置或前端自行裁剪作为安全边界。

## 4. 功能要求

### FR-001 统一 Request Snapshot 结构

- 系统 MUST 为每个可采集 API 请求生成统一 Request Snapshot。
- Snapshot MUST 至少包含：`method`、`path`、`route_template`、`query` 白名单摘要、`body_schema_summary`、业务资源标识、`status_code`、`error_code`、`duration_ms`、操作者、客户端、环境、请求开始时间、响应结束时间。
- Snapshot SHOULD 关联现有 `request_id`、`task_trace_id`、IP 摘要、User-Agent 摘要与日志主记录 ID。
- Snapshot MUST 使用稳定字段名，避免不同终端或不同接口生成互不兼容的 metadata 结构。
- 健康检查、静态资源、Swagger 文档、媒体直出等噪声路由 SHOULD 沿用请求日志排除策略，除非后续配置明确开启。

### FR-002 路由模板与请求路径采集

- 系统 MUST 同时记录实际请求路径 `path` 与路由模板 `route_template`。
- `route_template` SHOULD 表达 FastAPI 路由定义，例如 `/api/v1/admin/products/{product_id}`，用于聚合统计与错误定位。
- 当中间件无法稳定获取 route template 时，系统 MUST 提供降级策略，并在 Snapshot 中标识为 `unknown`、`unmatched` 或等价状态。
- Snapshot MUST NOT 将查询串直接拼接进 `path` 作为唯一请求上下文。

### FR-003 Query 与 Body 摘要策略

- Query 参数 MUST 按接口或通用策略白名单采集；未列入白名单的字段默认忽略或仅记录字段名。
- Body 内容 MUST 仅保存 schema 摘要、字段级类型、字段数量、长度、业务安全字段或脱敏结果。
- 系统 MUST NOT 保存密码、Token、Authorization、Cookie、真实密钥、数据库 DSN、MinIO AccessKey/SecretKey、原始文件名、原始敏感 body。
- 对数组、嵌套对象和大字段，Snapshot MUST 支持长度限制与摘要化展示。
- 对上传、多媒体、登录、认证、系统设置等敏感接口，Snapshot MUST 采用更严格的字段白名单。

### FR-004 业务资源标识

- Snapshot SHOULD 识别并记录请求关联的业务资源，例如产品、品牌、分类、SKU、媒体、用户、系统设置等。
- 资源标识 SHOULD 包含 `resource_type` 与 `resource_id`，或与现有事件字典兼容的 `entity_type` 与 `entity_id`。
- 当资源 ID 来源于 path、query、body 或业务上下文时，系统 SHOULD 标明来源或采用统一提取优先级。
- 无法识别业务资源时，Snapshot MUST 保持字段为空或标识为未识别，不得凭不可靠字符串猜测。

### FR-005 响应结果与错误上下文

- Snapshot MUST 记录响应状态码、业务错误码、耗时与请求结束时间。
- 错误请求 MUST 能关联错误码、状态码、耗时、route template、客户端与操作者。
- Snapshot SHOULD 保存错误消息摘要或错误分类，但不得暴露内部路径、堆栈、SQL、密钥或敏感业务数据。
- 慢请求 SHOULD 可基于 `duration_ms` 与现有日志审计策略被识别和展示。

### FR-006 管理端日志详情展示

- 管理端日志详情 MUST 展示 Request Snapshot，并与现有日志详情抽屉保持一致视觉和权限边界。
- Snapshot 展示 SHOULD 分组为：请求信息、输入摘要、业务资源、响应结果、操作者 / 客户端、环境与时间。
- 详情页 MUST 支持查看结构化 JSON 或等价字段视图，便于复制排障所需信息。
- 当 Snapshot 缺少某些字段时，管理端 MUST 以空态或 `未采集` 展示，不得导致详情页崩溃。
- 日志详情 MUST 仅允许系统管理员或具备等价权限的角色访问。

### FR-007 跨端一致性

- 后台管理端、店主 Web 展示端、微信小程序请求 MUST 使用同一 Snapshot 字段结构。
- `client_type` MUST 能区分 `web_admin`、`web_catalog`、`miniapp`、`backend` 或后续明确的客户端类型。
- 匿名访问场景 SHOULD 记录匿名会话或客户端摘要，但不得采集不必要的个人敏感信息。
- 不同终端无法提供的字段 MUST 保持兼容空值，而不是生成终端专属结构。

### FR-008 安全与合规治理

- Snapshot 采集 MUST 以后端统一脱敏与白名单策略为安全边界。
- 前端脱敏只能作为体验优化，MUST NOT 作为最终安全边界。
- Snapshot 配置与系统审计配置 SHOULD 保持一致，包括日志保留周期、敏感字段脱敏、敏感操作审计等策略。
- 新增字段、白名单或展示项 MUST 在实现阶段补充测试，覆盖敏感字段不落库、错误请求可排障、跨端字段兼容等场景。

## 5. UI 约束

- 管理端展示 MUST 复用现有日志审计详情抽屉、管理端 Shell、shadcn 基础组件和项目 Design System semantic token。
- UI MUST 优先以结构化分组呈现 Snapshot，避免只展示不可读的大段 JSON。
- JSON 展示区域 SHOULD 支持等宽字体、折行、空值提示与复制操作。
- 敏感字段被忽略或脱敏时，UI SHOULD 展示脱敏状态摘要，但不得展示敏感原文。
- 页面不得新增营销式说明页；入口应延续现有日志审计页信息架构。

## 6. 关联需求

| 类型 | 编号 | 关系 |
|---|---|---|
| 父需求 | REQ-0024-product-usage-logging | 在产品使用行为埋点与接口请求日志详情基础上增强请求快照能力 |

## 7. 状态块

```yaml
status: approved
next: /req-opsx REQ-0071
readiness: approved
notes:
  - 已补齐 user-stories、business-flow、acceptance、trace 和 Web 原型策略。
  - 已通过需求评审，可进入 /req-opsx。
```
