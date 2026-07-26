---
requirement_id: REQ-0071-request-snapshot-logging
title: Request Snapshot 日志详情原型说明
status: approved
owner: product
source: requirement.md
created_at: 2026-07-26 13:02:56
updated_at: 2026-07-26 13:10:46
---

# 原型说明

## 目标

展示管理端日志详情抽屉中 Request Snapshot 的信息分组与空态策略，供后续 `/req-opsx` 设计和 Web 实现参考。

## 页面范围

- 入口沿用现有日志审计页，不新增导航层级。
- 重点展示日志详情抽屉中的 Snapshot 区块。
- 原型不表达真实 API 数据绑定、权限实现、筛选列表和分页行为。

## 信息分组

| 分组 | 字段 |
|---|---|
| 请求信息 | method、path、route_template、request_id |
| 输入摘要 | query whitelist、body schema summary、redaction summary |
| 业务资源 | resource_type、resource_id、id_source |
| 响应结果 | status_code、error_code、duration_ms、error_summary |
| 操作者 / 客户端 | actor、client_type、ip_summary、user_agent_summary |
| 环境与时间 | environment、started_at、finished_at |

## UI 约束

- 复用管理端日志详情抽屉结构和 Design System semantic token。
- Snapshot 优先用结构化字段视图，JSON 作为辅助查看。
- 敏感字段展示脱敏状态或 `ignored`，不得展示敏感原文。
- 字段为空时展示 `未采集`。
- PNG 可在后续设计阶段导出；当前 HTML 为低保真结构原型。
