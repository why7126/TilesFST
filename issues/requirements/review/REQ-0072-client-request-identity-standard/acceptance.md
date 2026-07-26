---
requirement_id: REQ-0072-client-request-identity-standard
title: 前台后台与小程序统一客户端请求标识规范 - Acceptance
status: pending_review
owner: product
source: requirement.md
created_at: 2026-07-26 13:01:32
updated_at: 2026-07-26 13:01:32
---

# Acceptance

## 功能 AC

- [ ] AC-001 Web 管理端任一受控 API 请求进入后端后，请求日志中的 `client_type` 稳定记录为 `web_admin`。
- [ ] AC-002 店主 Web 前台任一公开业务 API 请求进入后端后，请求日志中的 `client_type` 稳定记录为 `web_catalog`。
- [ ] AC-003 微信小程序普通 API 请求进入后端后，请求日志中的 `client_type` 稳定记录为 `wechat_miniapp`，不得回退为默认 `web_catalog`。
- [ ] AC-004 客户端请求标识使用经确认的统一字段名传递，后端将其保存为独立 `client_request_id` 或 metadata 字段。
- [ ] AC-005 后端每次请求继续生成可信 `request_id`，并在响应头返回 `x-request-id`。
- [ ] AC-006 后端不得默认使用客户端传入的 `x-request-id` 覆盖服务端可信 `request_id`；若读取该请求头，只能按 OpenSpec design 中确认的独立字段策略处理。
- [ ] AC-007 后端对客户端请求标识执行长度、格式或字符集约束；非法值不得污染日志、破坏 JSON metadata 或导致 500。
- [ ] AC-008 错误响应、异常日志和请求日志中的后端可信 `request_id` 保持一致。
- [ ] AC-009 行为事件可携带相关后端 `request_id` 或客户端请求标识，且上报失败不阻断主业务流程。
- [ ] AC-010 后端不信任前端传入的用户身份、角色或权限字段；客户端类型和客户端请求 ID 均不得作为鉴权依据。
- [ ] AC-011 日志审计列表或详情展示客户端类型、后端可信 `request_id` 与客户端请求标识，并能从文案或字段名区分两类 ID。
- [ ] AC-012 日志审计支持复制后端可信 `request_id`；是否支持按 `client_request_id` 筛选在 OpenSpec design 中给出明确结论。
- [ ] AC-013 小程序 fallback base URL 重试时，请求标识复用或重建策略已被文档化，并具备对应验收用例。
- [ ] AC-014 Web 管理端、Web 前台、小程序、后端日志 middleware、日志审计展示的客户端类型枚举一致。
- [ ] AC-015 如新增或调整 API 请求头、响应头、日志字段或查询参数，必须同步 OpenAPI / Orval / docs / tests；若最终设计无需 Orval，需在 Change design 中说明原因。

## 安全 AC

- [ ] AC-SAFE-001 日志不得保存 Authorization Header、Cookie、Token、密码、真实密钥、MinIO AccessKey/SecretKey 或数据库 DSN。
- [ ] AC-SAFE-002 未授权用户不得访问日志审计列表、详情、请求标识字段或复制能力。
- [ ] AC-SAFE-003 客户端字段缺失、伪造或冲突时，不得放宽任何管理端或店主端权限。
- [ ] AC-SAFE-004 日志展示中的长请求 ID 必须避免撑破表格布局，完整值通过复制或详情展示获取。

## 测试与验证 AC

- [ ] AC-TEST-001 后端测试覆盖 `web_admin`、`web_catalog`、`wechat_miniapp` 三类客户端类型解析。
- [ ] AC-TEST-002 后端测试覆盖客户端请求标识非法、缺失、超长时仍生成可信 `request_id` 并返回响应头。
- [ ] AC-TEST-003 Web 管理端测试覆盖请求封装注入客户端类型和客户端请求标识。
- [ ] AC-TEST-004 Web 前台测试或等价 smoke 覆盖公开 API 请求注入 `web_catalog`。
- [ ] AC-TEST-005 小程序静态测试或 request 封装测试覆盖普通 API 请求注入 `wechat_miniapp`。
- [ ] AC-TEST-006 日志审计页面测试覆盖请求标识展示、截断和复制反馈。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 日志审计列表如新增或调整字段，分页 DOM 仍需对齐用户管理基准：左侧 `page-summary`，右侧 `page-right` 页码和每页条数。
- [ ] AC-XCUT-002 日志审计摘要指标卡如受影响，DOM 必须使用 `.metric-label` / `.metric-value` / `.metric-desc`，不得只用裸 `strong` / `span` 承载数值与说明。
- [ ] AC-XCUT-003 请求标识复制成功或失败反馈必须使用 fixed toast，不得使用文档流 notice，不得引起 hero、筛选区或表格纵向位移。
- [ ] AC-XCUT-004 N/A — 本需求不新增启停、冻结、上架/下架、删除、重置密码等状态变更类操作；因此不要求新增 DS confirm modal，但实现中仍不得引入 `window.confirm`。
