---
purpose: 数据库文档
content: SQLite 表结构、约束、种子数据与迁移说明
source: src/backend/app/db/schema.sql / Sprint 001 auth
update_method: schema 变更时同步更新 schema.sql 与本文件
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-25 23:20:00
note: 运行时数据库路径见 DATABASE_URL / .env.example
---

# 数据库设计

## 1. 概述

| 项目 | 说明 |
|---|---|
| 引擎 | SQLite 3（本地开发 / demo）；MySQL 8.0+（生产） |
| SQLite Schema 源 | `src/backend/app/db/schema.sql` + `src/backend/app/db/migrations.py` |
| MySQL Schema 源 | `src/backend/app/db/schema.mysql.sql` |
| 初始化 | 应用启动 `init_database()` 按数据库 dialect 执行 schema |
| ORM | SQLAlchemy 2.x（`src/backend/app/models/`） |
| 对象存储 | MinIO（图片/视频文件，非 SQLite） |

设计原则：结构化业务数据在本地 / demo 存 SQLite、生产存 MySQL；媒体二进制存 MinIO，数据库仅保存元数据与 object_key。

### 数据库选择

| 场景 | 配置 | 行为 |
|---|---|---|
| 本地开发 / demo | `APP_ENV!=production` | 使用 SQLite `DATABASE_URL` |
| 非生产外部库验证 | `APP_ENV!=production` 且显式配置 `DATABASE_URL` | 使用 `DATABASE_URL` |
| 生产 | `APP_ENV=production` | 必须配置 MySQL `DATABASE_URL`，否则启动失败 |

生产 MySQL URL 示例：

```text
mysql+pymysql://tiles_user:replace-with-secret@mysql.example.com:3306/tilesfst?charset=utf8mb4
```

---

## 2. ER 关系（当前）

```text
tile_categories 1 ── * tiles 1 ── * tile_images
brands 1 ── * tiles
brands 1 ── * brand_certificates 1 ── * brand_certificate_images
tile_specs 1 ── * tiles
tiles 1 ── * tile_videos

users 1 ── * login_logs（预留，本期无写入）
users 1 ── * profile_activity_logs（Sprint 003）
users 1 ── * system_settings.updated_by（Sprint 003，可选 FK）
users 1 ── * audit_logs.actor_user_id（Sprint 003，可选 FK）
users 1 ── * request_logs.actor_user_id（Sprint 004，可选 FK）
users 1 ── * usage_events.actor_user_id（Sprint 004，可选 FK）
request_logs.request_id ── * usage_events.request_id（逻辑关联，非 FK）
usage_events.behavior_trace_id ── * request_logs.behavior_trace_id（界面行为链路逻辑关联，非 FK）
request_logs.request_id ── * task_traces.parent_request_id（直接 API 或任务入口逻辑关联，非 FK）
task_traces.task_trace_id ── * task_trace_spans.task_trace_id（逻辑关联，非 FK）
task_traces.task_trace_id ── * request_logs / usage_events / audit_logs.task_trace_id（逻辑关联，非 FK）
performance_events.request_id ── request_logs.request_id（逻辑关联，非 FK）

（users 与 tiles 无直接外键，权限通过 JWT role 控制）
```

---

## 3. 表清单

| 表 | Sprint 001 | 说明 |
|---|---|---|
| users | ✓ 使用中 | 认证与角色 |
| login_logs | ✓ 已建表 | 登录审计预留 |
| profile_activity_logs | ✓ Sprint 003 | 个人资料操作审计 |
| system_settings | ✓ Sprint 003 | 系统设置 KV 持久化 |
| audit_logs | ✓ Sprint 003 | 统一审计日志（含 system_settings） |
| request_logs | ✓ Sprint 004 | API 请求日志（REQ-0024） |
| usage_events | ✓ Sprint 004 / Sprint 008 | 产品使用行为埋点事件（REQ-0024）；小程序详情访问、分享、咨询、首页快捷入口、瀑布流与安全降级事件用于热销推荐辅助排序和产品优先级判断 |
| performance_events | ✓ Sprint 022 / REQ-0107 | Web 与微信小程序真实用户页面加载性能事件 |
| task_traces | ✓ Sprint 011 / REQ-0069 | 可追踪业务任务摘要，用于串联上传等长耗时任务 |
| task_trace_spans | ✓ Sprint 011 / REQ-0069 | Task Trace 节点时间线与耗时明细 |
| tile_categories | 桩 | 分类 |
| tile_specs | ✓ Sprint 003 | 瓷砖规格主数据 |
| tiles | SKU 主表 | 瓷砖 SKU（扩展） |
| tile_videos | 已实现 | SKU 关联视频元数据 |
| tile_images | 桩 | 瓷砖图片元数据 |
| brand_certificates | ✓ Sprint 007 | 品牌证书主数据与 legacy 文件元数据 |
| brand_certificate_images | ✓ Sprint 013 | 品牌证书图片列表、主图与排序 |
| banners | ✓ Sprint 003 | Banner 管理 |
| topics | ✓ Sprint 003 | 专题管理 |

MySQL baseline 额外包含 `schema_migrations`，用于记录 baseline 初始化版本。

---

## 4. users（Sprint 001）

管理端账号密码登录。OpenSpec：`openspec/specs/auth/spec.md`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | TEXT | PK | UUID 字符串 |
| username | TEXT | NOT NULL, UNIQUE | 登录名 |
| phone | TEXT | NULL | 预留（多标识登录） |
| email | TEXT | NULL | 预留 |
| password_hash | TEXT | NOT NULL | bcrypt（passlib） |
| display_name | TEXT | NULL | 昵称；空时展示回退 username |
| role | TEXT | NOT NULL, CHECK | `admin` \| `employee` \| `store_owner` |
| status | TEXT | NOT NULL, DEFAULT `active`, CHECK | `active` \| `disabled` \| `deleted` |
| avatar_object_key | TEXT | NULL | MinIO 头像 object_key |
| remark | TEXT | NULL | 个人工作说明（0–200 字，profile self-service） |
| theme_mode | TEXT | NOT NULL, DEFAULT `system`, CHECK | `system` \| `dark_flagship` \| `comfort_dark` \| `light` |
| token_version | INTEGER | NOT NULL, DEFAULT 0 | JWT `tv` 版本；改密后递增使旧 token 失效 |
| last_login_at | TEXT | NULL | ISO8601 UTC |
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

**角色说明**

| role | 用途 |
|---|---|
| admin | 系统管理员；种子用户默认角色 |
| employee | 企业内部员工 |
| store_owner | 店主（预留；管理端 API 拒绝） |

**索引：** `username` UNIQUE（表级约束）

**种子数据：** `src/backend/app/db/seed.py`

- 当 `ADMIN_INITIAL_PASSWORD` 已配置且不存在 `ADMIN_USERNAME` 对应用户时，创建 role 为 `admin` 的默认用户。
- 默认用户名：`admin`；显示名：`系统管理员`。
- 已存在默认管理员时，普通服务重启或重复 seed 不会静默覆盖 `password_hash`。
- 仅当显式设置 `ADMIN_RESET_PASSWORD_ON_STARTUP=true` 时，启动 seed 才会使用 `ADMIN_INITIAL_PASSWORD` 的 bcrypt 哈希更新默认管理员 `password_hash`；该流程不新增字段、不存储明文密码、不改变角色或账号状态。
- `theme_mode` 默认 `system`，由 `PATCH /api/v1/auth/me/theme` 更新；SQLite 与 MySQL baseline 均保留枚举 CHECK，启动迁移为既有 SQLite 库补列。

---

## 5. login_logs（预留）

Sprint 001 仅建表，**无业务写入**。供后续登录审计 change 使用。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | TEXT | PK | UUID |
| user_id | TEXT | FK → users.id, NULL | 用户 ID（失败时可为空） |
| login_identifier | TEXT | NOT NULL | 登录标识（脱敏） |
| result | TEXT | NOT NULL, CHECK | `success` \| `failed` |
| failure_reason | TEXT | NULL | 失败原因 |
| ip | TEXT | NULL | 客户端 IP |
| user_agent | TEXT | NULL | User-Agent |
| created_at | TEXT | NOT NULL | ISO8601 UTC |

ORM：`src/backend/app/models/user.py` → `LoginLog`

---

## 5.1 profile_activity_logs（Sprint 003）

OpenSpec：`openspec/changes/add-admin-profile-page/`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | TEXT | PK | UUID |
| user_id | TEXT | FK → users.id, NOT NULL | 用户 ID |
| action_type | TEXT | NOT NULL | `profile_update` \| `avatar_update` \| `login` |
| summary | TEXT | NOT NULL | 可读中文摘要 |
| metadata | TEXT | NULL | JSON 扩展（可选） |
| created_at | TEXT | NOT NULL | ISO8601 UTC |

索引：`idx_profile_activity_logs_user_created (user_id, created_at DESC)`

ORM：`ProfileActivityLog`；Repository：`profile_activity_repository.py`

---

## 5.2 password_change_attempts（Sprint 003）

OpenSpec：`openspec/changes/add-admin-password-change/`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | TEXT | PK | UUID |
| user_id | TEXT | FK → users.id, NOT NULL | 用户 ID |
| success | INTEGER | NOT NULL | 1 成功 / 0 失败 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |

索引：`idx_password_change_attempts_user_created (user_id, created_at DESC)`

用途：15 分钟内失败 ≥5 次或 24 小时内成功 ≥3 次触发限流（42901）。

ORM：`PasswordChangeAttempt`；Repository：`password_change_repository.py`

---

## 5.3 system_settings（Sprint 003）

OpenSpec：`openspec/changes/add-system-settings/`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| key | TEXT | PK | 点分键，如 `basic.platform_name` |
| value | TEXT | NOT NULL | JSON 或标量字符串 |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_by | TEXT | NULL FK → users.id | 最后修改人 |

读取：`EffectiveSettingsService.get_effective(key)` = DB 覆盖值 ?? env ?? 代码默认。

Repository：`system_settings_repository.py`

---

## 5.4 audit_logs（Sprint 003）

OpenSpec：`openspec/changes/add-system-settings/`（与 REQ-0014 统一目标）

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | TEXT | PK | UUID |
| actor_user_id | TEXT | NULL FK → users.id | 操作人 |
| domain | TEXT | NOT NULL | 如 `system_settings` |
| action_type | TEXT | NOT NULL | 如 `settings_update`、`settings_reset` |
| summary | TEXT | NOT NULL | 人类可读摘要 |
| task_trace_id | TEXT | NULL | 关联 Task Trace，非 FK |
| task_type | TEXT | NULL | 任务类型摘要 |
| metadata | TEXT | NULL | JSON diff |
| created_at | TEXT | NOT NULL | ISO8601 UTC |

索引：`idx_audit_logs_domain_created (domain, created_at DESC)`、`idx_audit_logs_created (created_at DESC)`、`idx_audit_logs_task_trace (task_trace_id, created_at DESC)`

Repository：`audit_log_repository.py`

---

## 5.5 request_logs（Sprint 004 / REQ-0024）

API 请求日志。OpenSpec：`openspec/changes/add-product-usage-logging/`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | TEXT | PK | UUID |
| request_id | TEXT | NOT NULL | 服务端可信请求链路 ID；响应头同步返回 `x-request-id`，不得由客户端覆盖 |
| actor_user_id | TEXT | NULL FK → users.id | 已登录操作人，匿名请求为空 |
| actor_role | TEXT | NULL | `admin` / `employee` / `store_owner` 等 |
| client_type | TEXT | NULL | `web_admin`、`web_catalog`、`wechat_miniapp`、`unknown` |
| client_request_id | TEXT | NULL | 客户端请求标识，来自 `x-client-request-id` 或请求体 `client_request_id`，独立于可信 `request_id` |
| behavior_trace_id | TEXT | NULL | 界面行为链路 ID，来自 `x-behavior-trace-id`；直接 API 调用为空 |
| parent_behavior_event_id | TEXT | NULL | 触发本次请求的行为事件 ID，来自 `x-behavior-event-id`；直接 API 调用为空 |
| method | TEXT | NOT NULL | HTTP Method |
| path | TEXT | NOT NULL | API Path，不含 query |
| status_code | INTEGER | NOT NULL | HTTP 状态码 |
| duration_ms | INTEGER | NOT NULL | 请求耗时毫秒 |
| ip_address_masked | TEXT | NULL | 脱敏 IP |
| user_agent_summary | TEXT | NULL | 截断后的 User-Agent 摘要 |
| summary | TEXT | NOT NULL | 管理端列表可读摘要 |
| error_code | TEXT | NULL | 业务错误码或异常编码 |
| result | TEXT | NOT NULL, CHECK | `success` \| `failed` |
| task_trace_id | TEXT | NULL | 关联 Task Trace，非 FK |
| task_type | TEXT | NULL | 任务类型摘要 |
| metadata | TEXT | NULL | JSON 扩展信息，已做敏感字段过滤；请求日志可包含 `request_snapshot` 结构化请求快照 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |

索引：`idx_request_logs_created`、`idx_request_logs_request_id`、`idx_request_logs_client_request_id`、`idx_request_logs_behavior_trace`、`idx_request_logs_parent_behavior_event`、`idx_request_logs_actor_created`、`idx_request_logs_status_created`、`idx_request_logs_client_created`、`idx_request_logs_result_created`、`idx_request_logs_path_created`、`idx_request_logs_task_trace`

`metadata.request_snapshot` 作为详情展示契约存储统一 Request Snapshot。`client_request_id` 是独立查询列，用于辅助跨端请求归因和日志审计展示；它不作为认证授权依据，也不得覆盖服务端可信 `request_id`。`behavior_trace_id` 用于把一次页面访问、点击或表单提交产生的多个后端请求关联到同一行为链路；`parent_behavior_event_id` 用于从请求日志回指触发请求的单条 `usage_events.behavior_event_id`。直接 API 调用没有界面行为来源时，这两个字段保持 NULL，并继续通过 `request_id` 与任务链路关联。常用筛选依赖 `request_id`、`client_request_id`、`behavior_trace_id`、`parent_behavior_event_id`、`actor_user_id`、`status_code`、`client_type`、`result`、`path`、`created_at`、`task_trace_id` 等索引。REQ-0076 链路观测仪表复用 `request_logs`、`usage_events`、`audit_logs`、`task_traces`、`task_trace_spans` 的时间、状态和 trace 索引进行聚合；BUG-0127 补齐 `client_type + created_at` 与 `result + created_at` 索引用于日志审计列表条件下推和低成本筛选。若后续需要按 `route_template`、`resource_id` 聚合，仍应通过新的 OpenSpec Change 评估冗余列或索引，避免直接依赖 SQLite/MySQL JSON 方言差异。

Repository：`log_repository.py`；Service：`log_service.py`；中间件：`request_logging.py`

---

## 5.6 usage_events（Sprint 004 / REQ-0024）

产品使用行为埋点事件，事件名与属性由产品/研发人为定义并由后端白名单校验。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | TEXT | PK | UUID |
| request_id | TEXT | NULL | 关联 API 请求链路 ID，前端可透传 |
| behavior_trace_id | TEXT | NULL | 一次用户行为链路 ID，用于关联同一页面访问、点击或表单提交触发的多个请求 |
| behavior_event_id | TEXT | NULL | 单条用户行为事件 ID，可被 `request_logs.parent_behavior_event_id` 回指 |
| actor_user_id | TEXT | NULL FK → users.id | 已登录操作人，匿名上报为空 |
| actor_role | TEXT | NULL | 操作人角色 |
| client_type | TEXT | NOT NULL | 客户端类型，默认 `admin_web` |
| event_name | TEXT | NOT NULL | 事件名，如 `page_view`、`media_upload` |
| event_category | TEXT | NOT NULL | 事件分类，如 `navigation`、`entity_operation` |
| page_path | TEXT | NULL | 页面路径 |
| session_id | TEXT | NULL | 前端会话 ID |
| ip_address_masked | TEXT | NULL | 脱敏 IP |
| user_agent_summary | TEXT | NULL | 截断后的 User-Agent 摘要 |
| summary | TEXT | NOT NULL | 管理端列表可读摘要 |
| duration_ms | INTEGER | NULL | 行为耗时毫秒；瞬时行为可为空 |
| result | TEXT | NOT NULL, CHECK | `success` \| `failed` |
| task_trace_id | TEXT | NULL | 关联 Task Trace，非 FK |
| task_type | TEXT | NULL | 任务类型摘要 |
| metadata | TEXT | NULL | JSON 属性快照，禁止 password/token/secret 等敏感字段 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |

索引：`idx_usage_events_created`、`idx_usage_events_event_created`、`idx_usage_events_request_id`、`idx_usage_events_behavior_trace`、`idx_usage_events_behavior_event`、`idx_usage_events_actor_created`、`idx_usage_events_client_created`、`idx_usage_events_result_created`、`idx_usage_events_task_trace`

界面触发的数据链路为：`usage_events.behavior_trace_id -> request_logs.behavior_trace_id -> task_traces.parent_request_id -> task_trace_spans`。前端每次调用 `POST /api/v1/usage-events` 时生成新的 `behavior_trace_id` 与 `behavior_event_id`，并在短时间窗口内通过请求头 `x-behavior-trace-id`、`x-behavior-event-id` 透传给随后触发的 API 请求。

Repository：`log_repository.py`；Service：`log_service.py`

---

## 5.7 performance_events（Sprint 022 / REQ-0107）

真实用户页面加载性能事件。用于采集 Web 管理端、店主展示端与微信小程序在真实用户环境中的首屏、完整加载、应用启动和关键接口耗时。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | TEXT / VARCHAR(64) | PK | UUID |
| client_type | TEXT / VARCHAR(32) | NOT NULL | `web_admin`、`web_catalog`、`wechat_miniapp` |
| page_key | TEXT / VARCHAR(255) | NOT NULL | 页面、路由或接口摘要，不含 query 和敏感参数 |
| metric_name | TEXT / VARCHAR(64) | NOT NULL | 指标名，如 `first_content_ready`、`full_load`、`app_launch_ready`、`api_duration` |
| duration_ms | INTEGER | NOT NULL | 耗时毫秒，0–600000 |
| sample_rate | REAL / DECIMAL(5,4) | NOT NULL | 实际采样率，0–1 |
| app_version | TEXT / VARCHAR(64) | NULL | Web、小程序或后端标记版本 |
| network_type | TEXT / VARCHAR(32) | NULL | 网络类别摘要 |
| device_class | TEXT / VARCHAR(32) | NULL | 设备类别摘要 |
| request_id | TEXT / VARCHAR(64) | NULL | 前端或接口链路 ID，逻辑关联 |
| metadata | TEXT / JSON | NULL | 受控摘要 JSON，不存 Header、Cookie、Authorization、完整请求/响应体、手机号、openid、token 或签名 URL |
| occurred_at | TEXT / DATETIME | NOT NULL | 客户端事件发生时间 |
| created_at | TEXT / DATETIME | NOT NULL | 服务端写入时间 |

索引：`idx_performance_events_created`、`idx_performance_events_client_created`、`idx_performance_events_metric_created`、`idx_performance_events_page_created`、`idx_performance_events_request_id`

Repository：`performance_repository.py`；Service：`performance_service.py`

数据保留：首期不新增自动清理任务。生产环境建议先保留 90 天，后续如需定时归档或清理，由新的 OpenSpec Change 明确保留周期、清理命令与审计记录。

---

## 5.8 task_traces（Sprint 011 / REQ-0069）

可追踪业务任务摘要表。当前首批用于图片、视频、文件上传；REQ-0074 扩展覆盖 SKU 创建、更新、上架、下架等任务型管理操作；后续可扩展导入、导出、发布、同步等任务。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | TEXT | PK | UUID |
| task_trace_id | TEXT | UNIQUE, NOT NULL | 任务链路 ID，格式如 `task_upload_video_xxx` |
| task_type | TEXT | NOT NULL | 任务类型，如 `upload_image`、`upload_video`、`upload_file` |
| status | TEXT | CHECK | `processing` \| `success` \| `failed` \| `timeout` \| `cancelled` \| `skipped` |
| actor_user_id | TEXT | NULL FK → users.id | 发起人 |
| client_type | TEXT | NULL | 客户端类型 |
| parent_request_id | TEXT | NULL | 触发 Task Trace 的后端可信主请求 `request_id`，仅用于追踪定位，不作为权限依据 |
| behavior_trace_id | TEXT | NULL | 任务所属界面行为链路 ID；直接 API 触发时为空 |
| resource_type | TEXT | NULL | 资源类型摘要 |
| resource_id | TEXT | NULL | 资源 ID 摘要 |
| started_at / ended_at | TEXT | NOT NULL / NULL | 任务起止时间 |
| duration_ms | INTEGER | NULL | 聚合耗时 |
| slowest_span_name | TEXT | NULL | 当前耗时最高节点 |
| error_code | TEXT | NULL | 失败错误码 |
| summary | TEXT | NOT NULL | 任务摘要 |
| metadata | TEXT | NULL | 已脱敏 JSON |
| created_at / updated_at | TEXT | NOT NULL | ISO8601 UTC |

索引：`idx_task_traces_task_trace_id`、`idx_task_traces_parent_request_id`、`idx_task_traces_behavior_trace`、`idx_task_traces_type_created`、`idx_task_traces_status_created`

## 5.8 task_trace_spans（Sprint 011 / REQ-0069）

Task Trace 节点时间线。上传首批 span 包含 `frontend_upload_start`、`frontend_upload_body_done`、`api_receive`、`validate_file`、`storage_put_object`、`db_create_media`、`post_process`、`api_response`、`frontend_done/failed`。REQ-0074 的 SKU 保存和状态任务复用同表，不新增存储字段；span 包含 `api_receive`、`input_validate`、`business_persist`、`api_response`，业务失败时记录 `business_process` failed span。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | TEXT | PK | UUID |
| task_trace_id | TEXT | NOT NULL | 任务链路 ID，逻辑关联 `task_traces.task_trace_id` |
| task_type | TEXT | NOT NULL | 任务类型 |
| span_name | TEXT | NOT NULL | 节点名 |
| status | TEXT | CHECK | 节点状态 |
| started_at / ended_at | TEXT | NOT NULL / NULL | 节点起止时间 |
| duration_ms | INTEGER | NULL | 节点耗时 |
| sequence | INTEGER | NOT NULL | 时间线排序 |
| request_id | TEXT | NULL | 关联 HTTP 请求 |
| behavior_trace_id | TEXT | NULL | 节点所属界面行为链路 ID；直接 API 触发时为空 |
| actor_user_id | TEXT | NULL FK → users.id | 操作人 |
| client_type | TEXT | NULL | 客户端 |
| resource_type / resource_id | TEXT | NULL | 资源摘要 |
| error_code | TEXT | NULL | 节点失败错误码 |
| summary | TEXT | NOT NULL | 节点摘要 |
| metadata | TEXT | NULL | 已脱敏 JSON，不保存 Authorization、Cookie、AccessKey、SecretKey、DSN、`.env`、真实客户数据、完整敏感请求体或内部绝对路径 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |

索引：`idx_task_trace_spans_trace_sequence`、`idx_task_trace_spans_request_id`、`idx_task_trace_spans_behavior_trace`、`idx_task_trace_spans_type_created`

---

## 6. tile_categories（Sprint 002）

OpenSpec：`openspec/changes/add-tile-category-management/`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| parent_id | INTEGER | FK → tile_categories.id, NULL | 上级类目 |
| name | TEXT | NOT NULL | 类目名称（max 30） |
| code | TEXT | NOT NULL, UNIQUE | 类目编码（max 32） |
| sort_order | INTEGER | NOT NULL | 排序权重（正整数） |
| level | INTEGER | NOT NULL, CHECK 1–3 | 层级 |
| description | TEXT | NULL | 描述（max 200） |
| status | TEXT | NOT NULL, CHECK | `ENABLED` \| `DISABLED` |
| sku_count | INTEGER | NOT NULL, DEFAULT 0 | 直接绑定 SKU 数 |
| path | TEXT | NOT NULL | 层级路径文本 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

业务约束：自 `limit-admin-tile-categories-to-two-levels` 起，管理端新增类目最多只能创建到二级；自 `update-category-name-max-length-15` 起，管理端类目名称创建 / 更新业务输入上限为 15 个字符；自 `update-admin-category-name-special-characters` 起，管理端类目名称允许中文、英文、数字和常见特殊字符，空格、换行、制表符或不可见控制字符仍由应用层拒绝。SQLite `TEXT`、MySQL `VARCHAR(128)` 与本文档字段容量均已支持至少 15 字符和特殊字符，本变更无需 schema 或 migration。SQLite/MySQL schema 暂保留 `level BETWEEN 1 AND 3` 以兼容历史三级数据，后续历史治理需另走 OpenSpec Change。

ORM：`src/backend/app/models/tile_category.py`  
迁移：`migrations.py` → `_rebuild_tile_categories_table`（兼容旧 id+name 桩表）

---

## 6b. brands（Sprint 002）

OpenSpec：`openspec/changes/add-brand-management/`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| name | TEXT | NOT NULL, UNIQUE | 品牌名称（max 50） |
| sort_order | INTEGER | NOT NULL | 展示排序（正整数） |
| short_name | TEXT | NULL | 简称（max 30） |
| english_name | TEXT | NULL | 英文名（max 80） |
| logo_object_key | TEXT | NULL | MinIO Logo 对象键 |
| description | TEXT | NULL | 介绍（max 500） |
| status | TEXT | NOT NULL, CHECK | `ENABLED` \| `DISABLED` |
| sku_count | INTEGER | NOT NULL, DEFAULT 0 | 关联 SKU 数（本期默认 0） |
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

ORM：`src/backend/app/models/brand.py`  
迁移：`src/backend/app/db/migrations.py` → `_ensure_brands_table`

---

## 6b.1 brand_certificates（Sprint 007 / Sprint 013）

OpenSpec：`openspec/changes/add-brand-certificate-management/`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| brand_id | INTEGER | NOT NULL, FK → brands.id | 所属品牌；一个证书仅关联一个品牌 |
| name | TEXT | NOT NULL | 证书名称 |
| sort_order | INTEGER | NOT NULL, DEFAULT 100 | 展示排序 |
| type | TEXT | NOT NULL, CHECK | `QUALITY` \| `INSPECTION` \| `GREEN_BUILDING` \| `HONOR` \| `OTHER` |
| certificate_no | TEXT | NULL | 证书编号 |
| issuer | TEXT | NULL | 发证机构 |
| file_url | TEXT | NOT NULL | 受控读取 URL，如 `/media/{file_key}` |
| file_key | TEXT | NOT NULL | MinIO object_key |
| file_name | TEXT | NOT NULL | 上传显示文件名 |
| file_mime_type | TEXT | NOT NULL | `image/jpeg` / `image/png` / `image/webp` / `application/pdf` |
| file_size_bytes | INTEGER | NOT NULL, CHECK > 0 | 文件大小 |
| is_permanent | INTEGER | NOT NULL, DEFAULT 0 | 1 长期有效 / 0 有有效期 |
| effective_date | TEXT | NULL | 生效日期，`YYYY-MM-DD` |
| expiry_date | TEXT | NULL | 到期日期，`YYYY-MM-DD` |
| is_visible | INTEGER | NOT NULL, DEFAULT 1 | 是否前台展示 |
| remark | TEXT | NULL | 备注 |
| deleted_at | TEXT | NULL | 软删除时间 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

说明：Sprint 013 起，`file_*` 字段保留为 PDF/文档和旧单文件兼容字段；多图证书的图片列表写入 `brand_certificate_images`。当创建请求只提供图片数组、不提供 legacy `file` 时，后端使用主图回填 `file_*` 字段，保持旧列表与公开端兼容。

索引：`idx_brand_certificates_brand_visible`、`idx_brand_certificates_type_deleted`、SQLite `uq_brand_certificates_brand_name_active`。MySQL baseline 使用 `(brand_id, name, deleted_at)` 唯一键并由 service 层补充未删除证书名称唯一性校验。

Repository：`src/backend/app/repositories/brand_certificate_repository.py`  
迁移：`src/backend/app/db/migrations.py` → `_ensure_brand_certificates_support`

## 6b.2 brand_certificate_images（Sprint 013）

OpenSpec：`openspec/changes/update-certificate-multiple-images-main-image/`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| certificate_id | INTEGER | NOT NULL, FK → brand_certificates.id | 所属证书 |
| file_url | TEXT | NOT NULL | 受控读取 URL，如 `/media/{file_key}` |
| file_key | TEXT | NOT NULL | MinIO object_key |
| file_name | TEXT | NOT NULL | 上传显示文件名 |
| file_mime_type | TEXT | NOT NULL | `image/jpeg` / `image/png` / `image/webp` |
| file_size_bytes | INTEGER | NOT NULL, CHECK > 0 | 图片大小 |
| is_main | INTEGER | NOT NULL, DEFAULT 0 | 1 主图 / 0 非主图 |
| sort_order | INTEGER | NOT NULL, DEFAULT 0 | 图片展示顺序，保存时连续回填 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

索引：`idx_brand_certificate_images_certificate_sort`；SQLite 额外使用 `uq_brand_certificate_images_main` 约束单证书唯一主图。MySQL 由 service 层校验主图唯一性，避免 `(certificate_id, is_main)` 阻止多张非主图。

Repository：`src/backend/app/repositories/brand_certificate_repository.py`  
迁移：`src/backend/app/db/migrations.py` → `_ensure_brand_certificates_support`；MySQL 兼容迁移：`src/backend/app/db/mysql_migrations.py`

---

## 6c. topics（Sprint 003）

OpenSpec：`openspec/changes/add-banner-management/`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| code | TEXT | NOT NULL, UNIQUE | 专题编码 |
| title | TEXT | NOT NULL | 专题标题 |
| status | TEXT | NOT NULL, CHECK | `ENABLED` \| `DISABLED` |
| cover_object_key | TEXT | NULL | 封面 MinIO 键 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

迁移种子 ≥2 条 `ENABLED` 专题。ORM：`src/backend/app/models/topic.py`

---

## 6d. banners（Sprint 003）

OpenSpec：`openspec/changes/add-banner-management/`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| title | TEXT | NOT NULL | Banner 标题 |
| display_client | TEXT | NOT NULL, CHECK | 当前仅支持 `MINIAPP_HOME`；管理端文案显示“小程序” |
| position | TEXT | NOT NULL, CHECK | `MINIAPP_HOME_CAROUSEL` \| `MINIAPP_BRAND_LIST_CAROUSEL` |
| image_object_key | TEXT | NOT NULL | 图片 MinIO 键 |
| image_source | TEXT | NOT NULL | `sku_main_image` \| `sku_gallery_image` \| `custom_upload` \| `topic_cover` \| `brand_logo` |
| sku_gallery_asset_id | INTEGER | FK → tile_images.id | SKU 图库引用 |
| jump_type | TEXT | NOT NULL | `SKU_DETAIL` \| `BRAND_DETAIL` \| `EXTERNAL_LINK` \| `TOPIC_PAGE` \| `NO_JUMP` |
| sku_id | INTEGER | FK → tiles.id | SKU 跳转目标 |
| external_url | TEXT | NULL | HTTPS 外链 |
| topic_id | INTEGER | FK → topics.id | 专题跳转目标 |
| brand_id | INTEGER | FK → brands.id | 品牌详情跳转目标 |
| sort_order | INTEGER | NOT NULL, DEFAULT 100 | 排序 |
| valid_from | TEXT | NULL | 生效开始 |
| valid_to | TEXT | NULL | 生效结束 |
| status | TEXT | NOT NULL, CHECK | `DRAFT` \| `ONLINE` \| `OFFLINE` \| `EXPIRED` |
| remark | TEXT | NULL | 运营备注 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

UNIQUE `(display_client, position, title)`。ORM：`src/backend/app/models/banner.py`  
迁移：SQLite `migrations.py` → `_ensure_banner_support`；MySQL `mysql_migrations.py` → `_ensure_banner_brand_id`，用于对既有生产 `banners` 表幂等补齐创建/编辑写入字段 `image_source`、`sku_gallery_asset_id`、`topic_id`、`brand_id`、`valid_from`、`valid_to`、`remark`，以及 `idx_banners_status_position`、`idx_banners_sort`、`idx_banners_brand`、`idx_banners_topic`、`idx_banners_gallery_asset`。外键 `fk_banners_brand`、`fk_banners_topic`、`fk_banners_gallery_asset` 添加前会检查历史脏引用；存在脏数据时记录跳过原因和计数，不阻断缺列补齐。MySQL 兼容迁移还会检测并重建 `chk_banners_display_client`、`chk_banners_position`、`chk_banners_jump_type`、`chk_banners_image_source`，修复旧生产 CHECK 约束不允许 `MINIAPP_BRAND_LIST_CAROUSEL`、`BRAND_DETAIL` 或 `brand_logo` 的 drift。`update-admin-banner-placement-scope` 执行旧数据清理，删除条件为 `display_client != 'MINIAPP_HOME' OR position NOT IN ('MINIAPP_HOME_CAROUSEL', 'MINIAPP_BRAND_LIST_CAROUSEL')`。该清理仅删除 Banner 业务记录，不物理删除 MinIO 对象或其他业务表中的媒体引用；如需回滚旧 Banner 数据，依赖数据库备份恢复。

---

## 7. tile_specs（规格主数据）

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| width_mm | INTEGER | NOT NULL | 宽度（mm） |
| length_mm | INTEGER | NOT NULL | 长度（mm） |
| unit | TEXT | NOT NULL, DEFAULT 'mm' | 单位 |
| display_name | TEXT | NOT NULL | 展示名，如 `600×600mm` |
| status | TEXT | NOT NULL | `ENABLED` \| `DISABLED` |
| sku_count | INTEGER | NOT NULL, DEFAULT 0 | 绑定 SKU 数 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

UNIQUE `(width_mm, length_mm, unit)`。  
ORM：`src/backend/app/models/tile_spec.py`  
迁移：`src/backend/app/db/migrations.py` → `_ensure_tile_specs_support`

---

## 8. tiles（SKU 主表）

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| name | TEXT | NOT NULL | SKU 名称 |
| sku_code | TEXT | NOT NULL, UNIQUE | SKU 编码 |
| brand_id | INTEGER | NOT NULL, FK → brands.id | 品牌 |
| category_id | INTEGER | NOT NULL, FK → tile_categories.id | 类目 |
| spec_id | INTEGER | NULL, FK → tile_specs.id | 规格（上架前须非空） |
| size | TEXT | NOT NULL | 规格尺寸（与 spec display_name 同步） |
| surface_finish | TEXT | NOT NULL | 表面工艺 |
| color_family | TEXT | NULL | 主色系 |
| reference_price | REAL | NULL | 参考价格（元） |
| remark | TEXT | NULL | 备注 |
| status | TEXT | NOT NULL | `PUBLISHED` \| `DRAFT` \| `NEEDS_COMPLETION` \| `DISABLED` |
| published_at | TEXT | NULL | 最近一次上架/恢复上架时间；下架时可保留历史值，列表响应仅已上架状态展示 |
| recall_pin_sort_order | INTEGER | NOT NULL, DEFAULT 9999, CHECK > 0 | 召回置顶排序值；正整数，`1..9998` 可参与小程序普通商品列表 / 完整搜索 SKU 结果置顶，`9999` 为默认普通商品 |
| recall_pin_starts_at | TEXT | NULL | 召回置顶生效开始时间；空值表示立即可生效 |
| recall_pin_ends_at | TEXT | NULL | 召回置顶生效结束时间；空值表示长期有效 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

ORM：`src/backend/app/models/tile.py`  
迁移：`src/backend/app/db/migrations.py` → `_ensure_tiles_sku_extended`、`_ensure_tile_specs_support`；MySQL 兼容迁移见 `src/backend/app/db/mysql_migrations.py` → `_ensure_tiles_published_at_support`，同时维护召回置顶字段兼容。
索引：`idx_tiles_published_at (published_at)` 用于发布时间查询 / 排序扩展；`idx_tiles_recall_pin (recall_pin_sort_order, recall_pin_starts_at, recall_pin_ends_at)` 用于公开列表召回置顶排序候选筛选；现有管理端 SKU 列表默认排序仍为 `updated_at DESC`。

---

## 9. tile_images

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| tile_id | INTEGER | NOT NULL, FK → tiles.id | |
| object_key | TEXT | NOT NULL | MinIO 对象键 |
| url | TEXT | NOT NULL | 访问 URL |
| is_main | INTEGER | NOT NULL, DEFAULT 0 | 1=主图 |
| sort_order | INTEGER | NOT NULL, DEFAULT 0 | 排序 |

---

## 10. tile_videos

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| tile_id | INTEGER | NOT NULL, FK → tiles.id | |
| object_key | TEXT | NOT NULL | MinIO 对象键 |
| file_name | TEXT | NOT NULL | 原始文件名 |
| file_size_bytes | INTEGER | NULL | 文件大小 |
| duration_seconds | REAL | NULL | 时长（秒） |
| sort_order | INTEGER | NOT NULL, DEFAULT 0 | 排序 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |

---

## 11. miniapp_sku_favorites（小程序 SKU 收藏）

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| client_id | TEXT | NOT NULL | 小程序客户端匿名标识，不存储 token、手机号或微信会话密钥 |
| sku_id | INTEGER | NOT NULL, FK → tiles.id | 收藏的 SKU |
| favorite | INTEGER | NOT NULL, DEFAULT 1, CHECK | 1=收藏，0=取消收藏；用于幂等设置目标状态 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

UNIQUE `(client_id, sku_id)`；索引 `idx_miniapp_sku_favorites_client(client_id, favorite, updated_at)`。
SQLite 迁移：`src/backend/app/db/migrations.py` → `_ensure_miniapp_sku_favorites_support`。
MySQL baseline：`src/backend/app/db/schema.mysql.sql` 中同名表，`client_id` 为 `VARCHAR(128)`，`favorite` 为 `TINYINT`。

---

## 12. 媒体资产（规划）

`tile_media` 统一图片/视频/文档表尚未落地，见历史建议。当前上传桩返回 `object_key` + `url`，图片类额外返回 `thumbnail_url`、`display_url`、`original_url` 等派生 URL；三规格图不新增 SQLite/MySQL 表字段，事实源仍为业务表中的原图 `object_key` / `url`，后端媒体服务按同目录 `.thumb` / `.display` key 规则派生并在缺失时回退原图。若后续改为显式媒体派生关系表，必须通过新的 OpenSpec Change 同步 schema、迁移、API 和测试。

参考：`rules/media.md`、`docs/06-video-asset-management.md`

---

## 13. 迁移与本地数据

| 场景 | 做法 |
|---|---|
| 本地开发 | `data/sqlite/`（见 `rules/data-management.md`） |
| Docker | 卷挂载 + SQLite `DATABASE_URL` |
| 生产 | 外部 MySQL 8.0+ + `DATABASE_URL`，不挂载 SQLite 数据库卷 |
| SQLite Schema 变更 | 修改 `schema.sql` + `migrations.py` + OpenSpec change |
| MySQL Schema 变更 | 修改 `schema.mysql.sql` + versioned migration / `schema_migrations` 记录 + OpenSpec change |

**禁止提交：** 运行时 `.db` 文件、真实客户数据（见 `data/README.md`）

---

## 13.1 SQLite → MySQL 类型映射

| SQLite | MySQL baseline | 说明 |
|---|---|---|
| `INTEGER PRIMARY KEY AUTOINCREMENT` | `BIGINT AUTO_INCREMENT PRIMARY KEY` | 业务自增 ID |
| `TEXT` UUID | `CHAR(36)` | `users`、日志表 ID |
| `TEXT` 短文本 | `VARCHAR(n)` | 名称、状态、对象 Key 等 |
| `TEXT` 长文本 / JSON | `TEXT` | `metadata`、说明、备注 |
| ISO 时间 `TEXT` | `VARCHAR(64)` | 兼容现有 `datetime.now(UTC).isoformat()` 写入 |
| `REAL` | `DOUBLE` | 价格、厚度、视频时长等现有浮点字段 |
| `INTEGER` 布尔 | `TINYINT` | `is_main`、`success` |
| `CHECK` | MySQL 8.0 `CHECK` | 关键枚举保留数据库约束 |

MySQL baseline 保留关键唯一约束与索引：`users.username`、`tiles.sku_code`、`tile_specs(width_mm,length_mm,unit)`、`banners(display_client,position,title)`，以及审计、活动日志与媒体查询路径索引。Banner baseline 与 SQLite 最终态一致：`display_client` 仅允许 `MINIAPP_HOME`，`position` 仅允许 `MINIAPP_HOME_CAROUSEL` 与 `MINIAPP_BRAND_LIST_CAROUSEL`。

## 13.2 初始化与 Seed

- SQLite 路径继续执行 `schema.sql` 后再执行 `migrations.py`，保留 `sqlite_master` / `PRAGMA` 兼容迁移。
- MySQL 路径只执行 `schema.mysql.sql`，不得调用 SQLite introspection 或 SQLite-only DDL。
- MySQL 初始化通过 `schema_migrations(version, applied_at)` 记录 `mysql_baseline_v1`，DDL 使用 `CREATE TABLE IF NOT EXISTS` 保证重复启动幂等；随后执行 MySQL 兼容迁移并记录 `mysql_compat_banners_brand_id_v1`、`mysql_compat_banners_write_fields_v2` 与 `mysql_compat_banners_checks_v3`，覆盖旧生产 `banners` 表缺少品牌详情字段、创建/编辑写入字段以及 CHECK 约束枚举值的 drift 修复。
- 空库首次启动后，默认管理员 seed 继续使用 `ADMIN_USERNAME`、`ADMIN_INITIAL_PASSWORD`、`ADMIN_RESET_PASSWORD_ON_STARTUP`，密码以 bcrypt 哈希保存。

## 13.3 发布前 MySQL 兼容校验

数据库影响发布必须在 `/release-prepare` 中记录目标 MySQL 兼容证据。推荐命令：

```bash
python scripts/check-mysql-schema-drift.py --database-url "$DATABASE_URL"
```

该脚本只读取 `schema.mysql.sql` 和目标 MySQL `information_schema`，不修改业务数据；发现缺表或缺列时返回非 0，发布不得继续。发布证据中只记录命令、目标环境类型、时间和摘要结果，不记录明文 `DATABASE_URL`、密码或生产敏感信息。

## 14. 与 API 的对应

| 表 | 主要 API |
|---|---|
| users | `POST /api/v1/auth/login`、`GET /api/v1/auth/me`、`/api/v1/admin/users` |
| brands | `/api/v1/admin/brands` |
| tile_categories | `/api/v1/admin/tile-categories` |
| tile_specs | `/api/v1/admin/tile-specs` |
| tiles / tile_images / tile_videos | `/api/v1/admin/tile-skus`、`GET /api/v1/tiles`（展示桩）、`/api/v1/miniapp/home`、`/api/v1/miniapp/products`、`/api/v1/miniapp/search*`、`/api/v1/miniapp/skus/{sku_id}` |
| miniapp_sku_favorites | `PUT /api/v1/miniapp/skus/{sku_id}/favorite`、`GET /api/v1/miniapp/skus/{sku_id}` 收藏状态 |
| banners | `/api/v1/admin/banners`、`/api/v1/miniapp/home` |
| brand_certificates | `/api/v1/admin/brand-certificates`、`/api/v1/miniapp/search` 完整搜索证书分区、`/api/v1/miniapp/certificates` 公开证书列表、`/api/v1/miniapp/brands/{brand_id}/certificates` 品牌主页证书 Tab |
| usage_events | `/api/v1/usage-events`；小程序热销推荐读取 `product_detail_view`、`product_share`、`product_contact_click` 聚合计数；REQ-0043 首页样式优化新增瀑布流、快捷入口、收藏视觉和证书 Tab 事件；REQ-0044 新增 SKU 详情、媒体、收藏、分享、品牌、推荐和加载失败事件；REQ-0046 新增搜索浏览、输入、联想、提交、结果、筛选、无结果和历史操作事件；REQ-0047 新增商品列表浏览、曝光、点击、筛选、排序、刷新、加载更多和失败事件 |
| performance_events | `POST /api/v1/performance-events`、`GET /api/v1/admin/performance-events/summary` |

Sprint 008/009 `add-miniapp-home`、`update-miniapp-home-style-optimization`、`add-miniapp-search-component`、`add-miniapp-product-list-component` 与 `add-miniapp-certificate-list-page` 未新增业务表。小程序首页、全部产品瀑布流、搜索、商品列表、品牌证书 Tab 和公开证书列表复用既有 `brands`、`tile_categories`、`tile_specs`、`tiles`、`tile_images`、`brand_certificates`、`banners` 和 `usage_events`：人工配置与发布时间字段优先，行为事件统计作为热销推荐、热门搜索和商品发现效率分析的辅助依据；REQ-0046、REQ-0047 与 REQ-0057 新增事件字典不改变 `usage_events` 表结构。若后续需要高性能搜索索引、排行榜缓存表、商品列表运营插槽、证书运营配置或后台搜索配置中心，必须另走 OpenSpec Change 并同步 SQLite/MySQL schema、迁移、文档和测试。

索引：`docs/03-api-index.md`

---

## 15. 维护规则

Schema 变更时 MUST：

1. 更新 `src/backend/app/db/schema.sql`
2. 更新 ORM `src/backend/app/models/`
3. 更新本文件
4. 通过 OpenSpec change 进入开发（`rules/database.md`）
