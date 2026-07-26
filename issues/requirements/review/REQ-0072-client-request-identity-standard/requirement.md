---
requirement_id: REQ-0072-client-request-identity-standard
title: 前台后台与小程序统一客户端请求标识规范
terminal: multi
version: v1
status: approved
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0024-product-usage-logging
created_at: 2026-07-26 12:57:10
updated_at: 2026-07-26 13:10:48
---

# REQ-0072 前台后台与小程序统一客户端请求标识规范

## 1. 需求背景

`REQ-0024-product-usage-logging` 已建立产品使用行为埋点与接口请求日志详情能力，后端请求日志中已经包含 `request_id`、`client_type` 等关键观测字段。但当前跨端请求归因仍存在不一致：

- Web 管理端与店主 Web 前台的 Axios 请求尚未统一注入客户端类型与客户端请求标识。
- 微信小程序普通 API 请求未统一携带明确客户端类型，容易在后端日志中被归为默认 Web 前台来源。
- 微信小程序行为事件可记录 `wechat_miniapp`，但普通 API 请求日志与行为事件之间缺少稳定的客户端请求标识关联。
- 后端可信 `request_id` 与前端生成的请求标识边界需要明确，避免把客户端可伪造字段误作为服务端可信链路 ID。

本需求用于补齐“客户端请求身份”治理规范，让 Web 管理端、Web 前台、小程序和后端日志在客户端类型、请求标识、响应头返回与日志审计展示上形成一致闭环。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 系统管理员 | 在日志审计中准确识别请求来自管理端、店主 Web 前台还是微信小程序 |
| 开发 / 运维人员 | 通过后端可信 `request_id` 与客户端请求 ID 快速排查跨端问题 |
| 测试人员 | 能稳定验证不同端普通 API 请求的客户端归因，不依赖偶然默认值 |
| 产品负责人 | 在行为事件与接口请求日志之间建立可追溯关系，支持后续使用分析与问题复盘 |

## 3. 范围

### 3.1 本期包含

- Web 管理端与店主 Web 前台 API 请求统一携带客户端类型。
- 微信小程序普通 API 请求统一携带客户端类型。
- 客户端生成并携带独立的客户端请求标识，用于辅助排查同一用户动作触发的前端请求。
- 后端继续生成可信 `request_id`，并在响应头返回。
- 后端请求日志记录客户端类型、后端可信 `request_id` 与客户端请求标识。
- 日志审计列表或详情支持展示客户端类型、后端可信 `request_id` 与客户端请求标识。
- 行为事件尽量携带相关请求标识，便于从用户行为跳转到接口请求排查。
- 统一客户端类型枚举与字段命名，避免 Web、小程序、后端各自定义。

### 3.2 本期不包含

- 不引入分布式链路追踪平台、OpenTelemetry、Jaeger 或外部 APM。
- 不要求客户端传入字段成为后端最终可信 `request_id`。
- 不新增真实用户画像、漏斗分析、实时大屏或复杂 BI 能力。
- 不要求保存完整请求体、响应体、Authorization Header、Cookie 或敏感业务字段。
- 不调整日志保留周期、日志清理策略或存储分表策略。
- 不改变现有认证授权边界，不允许未授权访问日志审计。
- 不要求小程序 fallback base URL 重试策略在本阶段完全定稿，重试标识复用规则可在 `/req-complete` 阶段继续确认。

## 4. 功能要求

### FR-001 客户端类型统一

- MUST 定义统一 `client_type` 枚举，至少包含 `web_admin`、`web_catalog`、`wechat_miniapp`。
- Web 管理端 API 请求 MUST 携带明确客户端类型，后端日志应稳定记录为 `web_admin`。
- 店主 Web 前台 API 请求 MUST 携带明确客户端类型，后端日志应稳定记录为 `web_catalog`。
- 微信小程序普通 API 请求 MUST 携带明确客户端类型，后端日志应稳定记录为 `wechat_miniapp`。
- 后端 MUST 对未知或缺失客户端类型采用安全默认值或受控降级策略，并在 OpenSpec 阶段明确规则。
- 客户端类型不得用于替代认证授权判断；权限仍以服务端鉴权与角色校验为准。

### FR-002 客户端请求标识

- 客户端 SHOULD 为每次 API 请求生成独立客户端请求标识。
- 客户端请求标识字段 SHOULD 使用 `x-client-request-id`、`client_request_id` 或经 OpenSpec 确认的等价命名。
- 后端 MUST 将客户端请求标识保存为独立字段或 metadata，不得默认覆盖后端可信 `request_id`。
- 后端 MUST 限制客户端请求标识长度、字符集或格式，避免日志污染、超长字段和控制字符注入。
- 同一用户动作触发多个 API 请求时，客户端 MAY 复用同一个动作级关联标识；最终策略在 `/req-complete` 或 OpenSpec design 中确认。

### FR-003 后端可信 request_id

- 后端 MUST 继续为每个 API 请求生成服务端可信 `request_id`。
- 后端 MUST 在响应头返回可信 `request_id`，便于客户端错误提示、排障截图和日志检索。
- 后端 MAY 读取客户端传入的 `x-request-id`，但不得在未确认安全策略前将其作为最终可信 `request_id`。
- 日志审计中 MUST 能区分后端可信 `request_id` 与客户端请求标识。
- 错误响应、异常日志与请求日志中的后端可信 `request_id` MUST 保持一致。

### FR-004 跨端请求封装接入

- Web 端 SHOULD 在统一 Axios client 或等价请求封装中注入客户端类型与客户端请求标识。
- 若管理端与店主 Web 前台使用不同 API client，MUST 分别接入，不得只覆盖其中一端。
- 微信小程序 SHOULD 在统一 request 封装中注入客户端类型与客户端请求标识。
- 小程序 fallback base URL 重试时是否复用同一个客户端请求标识 MUST 在后续需求完善阶段确认，并形成可测试规则。
- 请求标识生成失败不应阻断主业务请求，但 SHOULD 采用受控降级并保留后端可信 `request_id`。

### FR-005 行为事件关联

- 行为事件 SHOULD 携带与当前用户动作或相关业务请求有关的请求标识。
- 对可明确关联主业务请求的行为事件，SHOULD 至少记录后端可信 `request_id` 或客户端请求标识之一。
- 行为事件上报失败不得阻断主业务流程。
- 后端不得信任前端传入的用户身份、角色或权限字段；行为事件通用上下文仍由服务端补充或校验。

### FR-006 日志审计展示与查询

- 日志审计列表或详情 MUST 展示客户端类型、后端可信 `request_id` 与客户端请求标识。
- 日志详情 MUST 明确字段含义，避免把客户端请求标识误读为服务端可信链路 ID。
- 日志审计 SHOULD 支持按后端可信 `request_id` 查询或复制。
- 是否新增 `client_request_id` 筛选项待 `/req-complete` 阶段确认。
- 日志审计访问 MUST 保持系统管理员权限边界，未授权用户不得查看请求标识与日志详情。

## 5. UI 约束

- 管理端日志审计新增字段展示时 MUST 继承现有管理端暗色旗舰风与列表/详情抽屉模式。
- Web UI 变更 MUST 使用 Design System semantic token class，不得新增裸 Hex 颜色。
- 请求标识复制操作 SHOULD 复用现有表格操作按钮、图标按钮、Tooltip 或等价组件。
- `request_id` 与客户端请求标识字段较长时，列表中 SHOULD 采用截断展示、复制完整值、详情中展示完整值的方式，避免撑破表格布局。
- 小程序端不要求新增可见页面；若展示请求 ID 用于错误反馈，文案需简短且不暴露敏感信息。

## 6. 关联需求与文档

| 关联项 | 关系 |
|---|---|
| `REQ-0024-product-usage-logging` | 父需求；提供产品使用行为埋点、接口请求日志与日志审计基础能力 |
| `rules/security.md` | 约束客户端字段不得替代服务端鉴权、不得记录敏感 Header 或密钥 |
| `rules/coding.md` | 约束 Web、小程序、后端请求封装与分层实现位置 |
| `docs/03-api-index.md` | 后续如涉及接口或响应头说明，需评估同步 |
| `docs/standards/api-governance.md` | 后续如固化请求头规范，需评估同步 |

## 7. 状态块

```yaml
status: approved
readiness: Ready
next_step: /req-opsx REQ-0072-client-request-identity-standard
expected_openspec_change: standardize-client-request-identity
needs_prototype: false
needs_api_change: true
needs_database_change: likely
needs_orval: likely
needs_docker_validation: false
knowledge_base_gate: Pass
cross_cutting_tags:
  - admin-list
```

## 8. 待完善项

- 确认客户端请求标识最终字段名：`x-client-request-id`、`client_request_id`、`x-request-id` 或组合策略。
- 确认是否允许客户端传入 `x-request-id`，以及是否仅作为客户端请求标识保存。
- 确认 Web 管理端与店主 Web 前台是否存在独立 API client，分别列入实现范围。
- 确认小程序 fallback base URL 重试时同一用户动作是否复用同一个客户端请求 ID。
- 确认日志审计页是否新增 `client_request_id` 筛选项。
