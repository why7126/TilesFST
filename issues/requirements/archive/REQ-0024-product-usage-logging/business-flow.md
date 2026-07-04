---
title: 业务流程
purpose: REQ-0024 产品使用日志与埋点业务流程
content: 描述请求日志、行为事件、管理端查询、脱敏与保留周期闭环
source: AI 根据 requirement.md、capture.md 与知识库横切规则生成，项目团队确认
update_method: 数据模型、接口、原型或安全策略变更时同步更新
owner: product
status: draft
created_at: 2026-07-02 13:04:31
updated_at: 2026-07-02 13:04:31
note: REQ-0024-product-usage-logging
---

# 业务流程

## 1. 总览

```text
用户页面行为 / API 请求 / 后端关键操作
  -> 生成或透传 request_id
  -> 请求日志中间件 / 行为事件上报 / 业务审计写入
  -> 事件字典校验、字段脱敏、长度截断
  -> 关系型数据库存储（SQLite demo / MySQL production）
  -> 管理端 GET /api/v1/admin/logs
  -> 日志审计列表、筛选、分页、详情抽屉
  -> 排障、审计、产品使用分析
```

## 2. 请求日志采集流程

1. 客户端发起 API 请求。
2. 后端统一中间件读取或生成 `request_id`。
3. 鉴权完成后补充 `actor_user_id`、`actor_role`、`client_type`。
4. 请求结束后记录 method、path、status_code、duration_ms、request_id、summary、created_at。
5. 若发生异常，记录 error_code、错误摘要和脱敏后的 metadata。
6. 默认跳过健康检查、静态资源、Swagger 文档、媒体直出等噪声路由。
7. 通过 Repository 写入关系型数据库，SQL MUST 参数化。

## 3. 行为事件采集流程

1. 产品、研发、测试在 `tracking-events.md` 中定义事件字典。
2. 前端或后端业务代码只允许上报字典中的 `event_name`。
3. 上报时携带必填业务属性和可选属性，不携带身份可信字段。
4. 后端校验事件名、必填属性、字段类型、长度与禁止属性。
5. 后端自动补充 user_id、role、client_type、page_path、request_id、session_id、timestamp、user_agent/ip 摘要。
6. 上报失败时不阻断主业务流程，但 SHOULD 记录可观测错误摘要。

## 4. 管理端查询流程

```text
系统管理员打开 SYSTEM / 日志审计
  -> 页面加载指标摘要和第一页日志
  -> 使用日志类型、时间、操作者、路径/事件名、状态码、request_id 筛选
  -> 后端按索引字段查询并返回分页结构
  -> 列表展示摘要、耗时、状态、操作者和 request_id
  -> 点击详情
  -> 抽屉展示基础信息、请求信息、行为上下文、错误摘要、metadata
```

约束：

- 普通员工、店主端和匿名用户 MUST NOT 访问日志查询与详情。
- 管理端列表 MUST 使用现有 AdminListPage 或等价列表骨架。
- 复制 request_id、查询失败、详情加载失败等反馈 MUST 使用 fixed toast 或等价固定层。

## 5. 脱敏与安全流程

```text
原始上下文
  -> 禁止字段过滤
  -> 敏感字段脱敏
  -> 长度截断
  -> metadata JSON 序列化
  -> 数据库存储
  -> 管理端展示脱敏结果
```

禁止采集或展示：

- 密码、Token、Authorization Header、Cookie。
- MinIO AccessKey / SecretKey、数据库 DSN、真实密钥。
- 未经白名单确认的完整请求体或完整响应体。
- 真实客户数据导出的运行时日志文件。

## 6. 保留周期与清理流程

1. 系统设置中的审计保留天数为默认策略来源。
2. 如果请求日志和行为事件需要独立保留周期，OpenSpec design MUST 说明新增配置项。
3. 查询 MUST 按时间倒序分页，禁止一次性全量加载后内存过滤。
4. 本期可先定义清理策略和后续任务；实现阶段至少预留按 `created_at` 清理的 Repository 能力或脚本规划。

## 7. 与现有能力差异

| 项目 | 现有能力 | REQ-0024 新增闭环 |
|---|---|---|
| `audit_logs` | 单点业务审计与设置操作留痕 | 统一纳入请求日志、行为事件、审计操作的查询模型 |
| REQ-0017 系统设置 | 配置审计策略、保留天数、脱敏开关 | 查询和查看日志数据本身 |
| API 错误处理 | 返回统一错误响应 | 通过 request_id、错误摘要和详情帮助排障 |
| 前端行为 | 页面自身交互 | 按事件字典采集关键行为事件 |

## 8. 待 Sprint 评审确认

- 店主 Web 展示端与微信小程序是否纳入本期实现，还是仅完成设计与后端扩展点。
- 日志模型采用扩展 `audit_logs`，还是新增 `request_logs` / `usage_events`。
- 是否新增独立日志保留周期配置。
- 是否需要手动清理入口；批量导出不在本期范围。
