---
title: 埋点事件字典
purpose: REQ-0024 人为定义产品使用行为事件、属性与安全边界
content: MVP 事件清单、公共上下文、校验规则与演进流程
source: AI 根据 requirement.md §7 与用户关于人为设计埋点事件属性的确认生成
update_method: 新增事件、属性、客户端覆盖范围或安全策略变更时先更新本文，再同步代码与测试
owner: product
status: draft
created_at: 2026-07-02 13:04:31
updated_at: 2026-07-03 18:10:26
note: REQ-0024-product-usage-logging
---

# 埋点事件字典

## 1. 设计原则

埋点事件和属性 MUST 人为定义。系统可以自动补充上下文，但不得把“所有点击、所有接口、所有 DOM 文案”自动采集后直接当作产品埋点事实源。

```text
需求阶段定义 tracking-events.md
  -> OpenSpec design 确认事件范围
  -> 前端/后端同步事件枚举与 Schema
  -> 后端统一校验与补上下文
  -> 测试覆盖允许事件、非法事件、敏感字段过滤
```

## 2. 公共上下文

后端 MUST 自动补充以下上下文，不信任前端传入的身份字段：

| 字段 | 来源 | 说明 |
|---|---|---|
| `user_id` | 服务端鉴权上下文 | 匿名可为空 |
| `role` | 服务端鉴权上下文 | admin、employee、store_owner、anonymous 等 |
| `client_type` | 服务端推导或受控 Header | web_admin、web_catalog、miniapp、backend |
| `page_path` | 前端上报 + 后端长度校验 | 页面路径，不含敏感 query |
| `request_id` | 后端请求上下文 | 用于串联请求日志 |
| `session_id` | 受控会话标识 | 匿名端待 Sprint 评审确认 |
| `duration_ms` | 前端或服务端计时 | 行为耗时毫秒；页面加载、查询、详情加载、上传、保存等过程型行为 SHOULD 上报；瞬时行为可为空 |
| `timestamp` | 服务端时间 | 统一使用服务端写入时间 |
| `user_agent_summary` | 请求头摘要 | 限制长度 |
| `ip_summary` | 请求来源摘要 | 展示时可脱敏 |

## 3. MVP 事件清单

| event_name | event_category | 触发时机 | 必填属性 | 可选属性 | 禁止属性 |
|---|---|---|---|---|---|
| `page_view` | navigation | 页面加载完成 | `page_path`, `module` | `referrer`, `entry_source` | `token`, `password` |
| `search_submit` | discovery | 用户提交搜索 | `module`, `keyword` | `result_count`, `filters_count` | `token`, `password` |
| `filter_change` | discovery | 筛选条件变化 | `module`, `filter_name`, `filter_value` | `previous_value` | `token`, `password` |
| `detail_view` | inspection | 用户打开详情抽屉或详情页 | `module`, `entity_type`, `entity_id` | `request_id`, `log_type` | `token`, `password` |
| `copy_request_id` | utility | 用户复制 request_id | `module`, `entity_type`, `entity_id`, `request_id` | `log_type` | `token`, `password`, `authorization`, `cookie` |
| `entity_create` | mutation | 新建业务对象成功 | `entity_type`, `entity_id` | `module`, `result` | `raw_payload`, `password` |
| `entity_update` | mutation | 编辑保存成功 | `entity_type`, `entity_id`, `changed_fields` | `module`, `result` | `before_value`, `password` |
| `entity_delete` | mutation | 删除业务对象成功 | `entity_type`, `entity_id` | `module`, `result` | `raw_payload`, `token` |
| `status_change` | mutation | 启停、上下架、冻结等状态变化 | `entity_type`, `entity_id`, `from_status`, `to_status` | `module`, `reason` | `raw_payload`, `token` |
| `media_upload` | media | 媒体上传完成 | `media_type`, `business_type`, `file_size`, `result` | `duration_ms`, `mime_type` | `raw_filename`, `token` |
| `login_success` | auth | 登录成功 | `user_id`, `role` | `client_type` | `password`, `token` |
| `login_failed` | auth | 登录失败 | `username_masked`, `reason` | `client_type` | `password`, `token` |
| `api_error` | reliability | 接口异常 | `request_id`, `path`, `status_code`, `error_code` | `duration_ms`, `module` | `authorization`, `cookie` |

## 3.1 管理端页面覆盖范围

Web 管理端页面浏览事件统一由管理端布局层上报 `page_view`，覆盖所有已登记的 `/admin/*` 业务页面；各页面仍按事件字典单独上报搜索、筛选、详情、复制、创建、更新、删除、状态变化、媒体上传等行为事件。

| route_pattern | module | entity_type | entity_id | page_title |
|---|---|---|---|---|
| `/admin/dashboard` | `dashboard` | `admin_page` | `admin_dashboard` | 数据概览 |
| `/admin/tile-skus` | `tile_sku` | `admin_page` | `admin_tile_skus` | 瓷砖 SKU |
| `/admin/brands` | `brand` | `admin_page` | `admin_brands` | 瓷砖品牌 |
| `/admin/tile-categories` | `tile_category` | `admin_page` | `admin_tile_categories` | 瓷砖类目 |
| `/admin/tile-specs` | `tile_spec` | `admin_page` | `admin_tile_specs` | 瓷砖规格 |
| `/admin/banners` | `banner` | `admin_page` | `admin_banners` | Banner 管理 |
| `/admin/profile` | `profile` | `admin_page` | `admin_profile` | 个人资料 |
| `/admin/users` | `user_management` | `admin_page` | `admin_users` | 用户管理 |
| `/admin/settings/:tab` | `system_settings` | `admin_page` | `admin_settings` | 系统设置 |
| `/admin/logs` | `log_audit` | `admin_page` | `admin_logs` | 日志审计 |
| `/admin/api-docs` | `api_docs` | `admin_page` | `admin_api_docs` | 接口文档 |

## 4. 属性规范

| 属性 | 类型 | 说明 |
|---|---|---|
| `module` | string | 业务模块，如 product、brand、category、system_settings、log_audit |
| `keyword` | string | 搜索词，MUST 做长度限制和敏感字段过滤 |
| `filter_name` | string | 筛选字段名 |
| `filter_value` | string | 筛选值摘要，不保存敏感原值 |
| `entity_type` | string | 业务对象类型，如 tile_sku、brand、category、user、setting |
| `entity_id` | string | 业务对象 ID |
| `changed_fields` | string[] | 字段名列表，不包含变更前后原值 |
| `result` | string | success、failed 或等价受控枚举 |
| `media_type` | string | image、video、document 等受控值 |
| `business_type` | string | brand_logo、sku_image、banner 等业务场景 |
| `file_size` | number | 文件字节数 |
| `username_masked` | string | 脱敏后的用户名 |
| `reason` | string | 失败原因摘要，禁止包含密码、Token |
| `duration_ms` | number | 行为耗时毫秒，作为上报体一等字段保存，非 `properties` 内嵌属性 |

## 5. 校验规则

- MUST 只允许上报本字典中登记的 `event_name`。
- MUST 校验每个事件的必填属性存在且类型正确。
- MUST 拒绝或过滤 `forbidden_properties`。
- MUST 对字符串长度设置上限，避免日志膨胀。
- MUST 对 `metadata` 做 JSON 序列化异常保护。
- MUST 对前端传入的 `user_id`、`role`、`ip` 等身份字段忽略或覆盖。
- SHOULD 记录非法事件上报的错误摘要，但不得阻断主业务流程。

## 6. 演进流程

新增或调整事件时 MUST 依次完成：

1. 更新本文事件字典。
2. 在 OpenSpec design 中说明新增事件的业务价值和数据边界。
3. 更新前端事件枚举或调用封装。
4. 更新后端 Pydantic Schema、枚举或等价校验。
5. 更新单元测试、集成测试和 OpenAPI / Orval 产物。
6. 更新管理端日志筛选或详情展示字段（如涉及）。
