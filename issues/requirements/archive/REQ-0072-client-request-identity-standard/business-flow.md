---
requirement_id: REQ-0072-client-request-identity-standard
title: 前台后台与小程序统一客户端请求标识规范 - Business Flow
status: done
owner: product
source: requirement.md
created_at: 2026-07-26 13:01:32
updated_at: 2026-07-26 16:53:50
---

# Business Flow

## 1. 总体流程

```text
用户动作
  |
  v
Web 管理端 / Web 前台 / 微信小程序请求封装
  |
  |-- 注入 x-client-type
  |-- 生成并注入 client_request_id 或等价字段
  v
后端 API 入口 / 请求日志 middleware
  |
  |-- 生成可信 request_id
  |-- 校验并记录客户端请求标识
  |-- 记录 client_type、路径、状态码、耗时、操作者
  v
业务处理
  |
  |-- 成功：响应头返回后端可信 x-request-id
  |-- 失败：错误响应和异常日志携带同一后端可信 request_id
  v
日志审计 / 行为事件排查
  |
  |-- 按 request_id 定位服务端请求
  |-- 按 client_request_id 辅助关联前端动作
  |-- 按 client_type 区分 web_admin / web_catalog / wechat_miniapp
```

## 2. Web 管理端流程

```text
管理员在管理端执行查询 / 保存 / 上传 / 复制等操作
  -> 管理端 API client 注入 x-client-type=web_admin
  -> API client 生成客户端请求标识
  -> 后端生成可信 request_id 并写入请求日志
  -> 日志审计展示 web_admin、request_id、client_request_id
```

约束：

- 管理端客户端类型只表达来源，不替代管理员权限。
- 日志审计页展示字段时延续 `REQ-0024` 的列表与详情抽屉结构。

## 3. 店主 Web 前台流程

```text
店主或访客浏览公开商品 / 搜索 / 查看详情
  -> 店主 Web API client 注入 x-client-type=web_catalog
  -> API client 生成客户端请求标识
  -> 后端按公开访问边界处理请求
  -> 请求日志记录 web_catalog 与可信 request_id
```

约束：

- 匿名访问仍只允许查看公开数据。
- 不得因增加客户端类型而暴露管理端日志或内部字段。

## 4. 微信小程序流程

```text
用户在小程序浏览 / 搜索 / 查看 SKU / 上报行为事件
  -> 小程序统一 request 封装注入 x-client-type=wechat_miniapp
  -> request 封装生成客户端请求标识
  -> 普通 API 请求与 usage-events 使用一致客户端类型
  -> 后端请求日志和行为事件均可回溯客户端来源
```

待确认：

- fallback base URL 重试时，是否复用同一个客户端请求标识。
- 同一用户动作触发多个请求时，是否需要动作级关联 ID。

## 5. 与父需求 REQ-0024 的差异

| 项 | REQ-0024 | REQ-0072 |
|---|---|---|
| 主要目标 | 建立请求日志、行为事件、日志审计基础能力 | 统一跨端客户端类型和请求标识规范 |
| 日志字段 | 定义 `request_id`、`client_type` 等观测字段 | 明确后端可信 `request_id` 与客户端请求 ID 的边界 |
| 前端接入 | 管理端日志审计与事件上报为主 | Web 管理端、Web 前台、小程序普通 API 请求均需接入 |
| UI 范围 | 日志审计列表和详情抽屉完整页面 | 在既有日志审计中补充字段展示、复制和筛选策略 |
| 安全重点 | 脱敏、权限、保留周期 | 客户端字段不可替代服务端鉴权和可信链路 ID |

## 6. 异常与降级

| 场景 | 处理原则 |
|---|---|
| 客户端未传 `x-client-type` | 后端采用受控默认值或记录 unknown，具体策略 OpenSpec 阶段确认 |
| 客户端请求标识非法或过长 | 后端忽略或截断并记录安全摘要，不影响可信 `request_id` 生成 |
| 请求封装生成 ID 失败 | 客户端继续发起请求，后端可信 `request_id` 仍可用于排障 |
| 行为事件上报失败 | 不阻断主业务流程，记录可观测错误摘要 |
| 日志审计复制失败 | 使用 fixed toast 提示失败，不引起页面布局位移 |
