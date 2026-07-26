---
req_id: REQ-0072-client-request-identity-standard
status: captured
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 12:49:31
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0024-product-usage-logging
captured_via: capture
classification_rationale: 当前描述要求统一前端、小程序与后端请求标识规范，属于跨端观测治理增强，因此归类为需求。
---

# 一句话

前台、后台与微信小程序请求需要统一携带客户端类型和请求标识，便于日志归因与链路追踪。

# 原始描述

采纳优化建议：给所有前端/小程序请求统一带 `x-client-type`、`x-request-id` 或前端生成的 `client_request_id`；后端继续生成可信 `request_id` 并返回响应头。

# 背景与关联

- 后端当前可从 `x-client-type` 读取客户端类型，但小程序普通 API 请求未统一携带，容易被归为 `web_catalog`。
- Web Axios 当前只注入 Authorization，未统一生成请求标识。
- 小程序行为事件写入 `wechat_miniapp`，但普通 API 请求日志与行为事件的客户端归因不完全一致。

# 影响范围

- Web 前台/后台：Axios 请求拦截器。
- 微信小程序：统一 request 封装。
- 后端：请求日志 middleware 对 client request id 与可信 request id 的记录和返回。
- 日志审计：列表和详情展示客户端类型、后端 request_id、客户端请求 ID。

# 初步需求要点

- 所有 Web 与小程序 API 请求都应携带明确 `x-client-type`。
- 客户端可生成 `client_request_id` 或 `x-request-id`，后端仍以可信 `request_id` 为主，并在响应头返回。
- 行为事件应尽量携带与主业务请求相关的 request 标识，方便从用户行为跳转到接口请求。
- 客户端类型枚举需要统一，例如 `web_admin`、`web_catalog`、`wechat_miniapp`。

# 待澄清

- [ ] 是否允许客户端传入 `x-request-id` 作为后端最终 request_id，还是保存为独立 `client_request_id`。
- [ ] Web 前台展示端是否已有独立 API client，需要同步接入。
- [ ] 小程序 fallback base URL 重试时同一用户动作是否复用同一个客户端请求 ID。
- [ ] 日志审计页是否需要新增 client_request_id 筛选。

# 建议验收要点

- [ ] 后台 Web 请求日志稳定显示 `web_admin`。
- [ ] 前台 Web 请求日志稳定显示 `web_catalog`。
- [ ] 小程序普通 API 请求日志稳定显示 `wechat_miniapp`。
- [ ] 响应头仍返回后端可信 `x-request-id`。
- [ ] 行为事件与相关业务请求可通过 request 标识进行排查。

# 分类说明（/capture）

该条目是跨端请求标识治理增强，属于 REQ。
