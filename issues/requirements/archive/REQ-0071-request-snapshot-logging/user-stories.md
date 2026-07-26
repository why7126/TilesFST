---
requirement_id: REQ-0071-request-snapshot-logging
title: API 请求日志统一 Request Snapshot - 用户故事
status: done
owner: product
source: requirement.md
created_at: 2026-07-26 13:02:56
updated_at: 2026-07-26 16:52:07
---

# 用户故事

## US-001 系统管理员查看完整请求快照

作为系统管理员，我希望在日志详情中直接查看一次 API 请求的 Request Snapshot，以便判断请求来源、操作者、影响资源、响应结果和错误上下文。

验收要点：

- 日志详情展示 method、path、route template、status code、error code、duration、request_id、客户端、环境和请求/响应时间。
- 日志详情展示业务资源标识，例如 `resource_type` / `resource_id` 或等价字段。
- Snapshot 缺失字段时展示 `未采集` 或等价空态，不影响详情页加载。

## US-002 开发 / 运维人员定位错误请求

作为开发 / 运维人员，我希望错误请求日志能同时包含路由模板、白名单 query、body schema 摘要、错误码和耗时，以便不查看敏感原文也能定位问题。

验收要点：

- 4xx / 5xx 请求能关联业务错误码、状态码、route template、耗时和客户端类型。
- body 只展示 schema 摘要、字段类型、字段数量、长度或脱敏值。
- 内部路径、堆栈、SQL、密钥、Authorization、Cookie、Token 和密码不进入 Snapshot。

## US-003 产品负责人分析跨端 API 使用

作为产品负责人，我希望前台 Web、后台管理端和微信小程序请求使用一致的 Snapshot 字段，以便后续分析跨端 API 使用与异常分布。

验收要点：

- `client_type` 能稳定区分 `web_admin`、`web_catalog`、`miniapp`、`backend` 或后续明确终端。
- 不同终端无法提供的字段保持兼容空值，而不是生成终端专属 metadata 结构。
- route template 和资源标识可用于后续聚合统计。

## US-004 安全负责人确认日志脱敏边界

作为安全负责人，我希望 Request Snapshot 以后端白名单和脱敏策略为安全边界，以便日志满足审计价值但不保存原始敏感 body。

验收要点：

- query 与 body 字段遵循后端白名单、敏感字段黑名单、长度截断和摘要化规则。
- 上传、登录、认证、系统设置等敏感接口采用更严格白名单。
- 前端传入的身份、敏感字段配置或脱敏结果不得作为最终可信来源。
