---
requirement_id: REQ-0071-request-snapshot-logging
title: API 请求日志统一 Request Snapshot - 业务流程
status: done
owner: product
source: requirement.md
created_at: 2026-07-26 13:02:56
updated_at: 2026-07-26 16:52:07
---

# 业务流程

## 1. 请求快照采集流程

```text
客户端请求
  |
  v
后端统一请求入口 / Middleware
  |
  +-- 生成或读取 request_id
  +-- 识别 client_type、actor、environment
  +-- 捕获 method、path、route_template、开始时间
  |
  v
Snapshot Builder
  |
  +-- query 白名单过滤
  +-- body schema 摘要化
  +-- 敏感字段过滤 / 脱敏 / 截断
  +-- 业务资源标识提取
  |
  v
业务 API 执行
  |
  +-- 成功：记录 status_code、duration、结束时间
  +-- 失败：记录 status_code、error_code、错误摘要、duration、结束时间
  |
  v
请求日志落库
  |
  v
管理端日志详情展示 Request Snapshot
```

## 2. 错误请求排障流程

```text
系统管理员 / 运维人员打开日志审计
  |
  v
通过 request_id、路径、状态码、客户端或时间筛选日志
  |
  v
打开日志详情抽屉
  |
  v
查看 Request Snapshot
  |
  +-- 请求信息：method / path / route_template
  +-- 输入摘要：query whitelist / body schema summary
  +-- 业务资源：resource_type / resource_id
  +-- 响应结果：status_code / error_code / duration
  +-- 操作者与客户端：actor / client_type / environment
  |
  v
复制必要字段进入排障记录或开发定位
```

## 3. 与父需求 REQ-0024 的差异

| 维度 | REQ-0024 已覆盖 | REQ-0071 增强 |
|---|---|---|
| 请求日志基础字段 | `request_id`、method、path、状态码、耗时、操作者、客户端等 | 统一 Snapshot 字段契约，补齐 route template、资源 ID、环境、请求/响应时间 |
| metadata 内容 | query 参数和 path 摘要为主 | query 白名单、body schema 摘要、业务资源、错误上下文和脱敏状态 |
| 日志详情 | 展示基础信息、请求信息、metadata JSON | 结构化展示 Request Snapshot 分组，减少跨字段拼接 |
| 安全策略 | 敏感字段脱敏、请求/响应体截断 | 明确禁止保存敏感原文，后端白名单为安全边界 |
| 跨端一致性 | 支持管理端、店主端、小程序日志方向 | 要求三端使用兼容字段结构和统一 `client_type` |

## 4. 数据边界

- Snapshot 是请求日志事实的一部分，不替代业务审计日志、产品行为事件或外部 APM。
- Snapshot 保存的是可审计摘要，不保存完整原始请求体或完整响应体。
- Snapshot 字段应可被 API 响应、管理端详情和后续 OpenSpec design 复用。
