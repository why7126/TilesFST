---
requirement_id: REQ-0072-client-request-identity-standard
title: 日志审计请求标识展示 Prototype Context
status: pending_review
owner: product
source: acceptance.md
created_at: 2026-07-26 13:01:32
updated_at: 2026-07-26 13:01:32
---

# Prototype Context

## 目标

本原型用于描述 `REQ-0072` 对既有日志审计列表与详情抽屉的字段补充策略，不代表新增独立页面。

## 页面范围

- 管理端日志审计列表：补充或确认展示 `客户端`、`request_id`、`client_request_id`。
- 日志详情抽屉：分组展示后端可信请求 ID 与客户端请求 ID，并说明二者含义。
- 复制交互：复制后端可信 `request_id` 与可选客户端请求 ID，反馈使用 fixed toast。

## 字段策略

| 字段 | 展示位置 | 说明 |
|---|---|---|
| `client_type` | 列表列、详情基础信息 | 枚举：`web_admin`、`web_catalog`、`wechat_miniapp` |
| `request_id` | 列表列、详情基础信息、复制按钮 | 后端可信请求 ID，排障主入口 |
| `client_request_id` | 详情基础信息；是否入列表待确认 | 客户端生成，辅助关联前端动作 |
| `x-request-id` 响应头 | 详情请求信息 | 后端可信 ID 的响应头承载方式 |

## 交互约束

- 长 ID 在表格中中段截断，Tooltip 或详情展示完整值。
- 复制按钮使用图标按钮，hover 展示 Tooltip。
- 复制成功 / 失败通过 fixed toast 反馈，不推挤页面布局。
- 不新增状态变更类操作，不使用 `window.confirm`。
- 页面样式遵守 Design System semantic token，不新增裸 Hex。

## 待确认

- `client_request_id` 是否进入列表筛选项。
- 小程序 fallback 重试是否复用同一客户端请求 ID。
- 行为事件是否需要动作级 `interaction_id`，该项若超出本需求可后续单独 capture。

## PNG

- PNG Golden Reference：待 OpenSpec design 或 UI 实现阶段导出。
