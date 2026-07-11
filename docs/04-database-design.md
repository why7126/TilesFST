---
purpose: 数据库文档
content: SQLite 表结构、约束、种子数据与迁移说明
source: src/backend/app/db/schema.sql / Sprint 001 auth
update_method: schema 变更时同步更新 schema.sql 与本文件
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-11 18:51:16
note: 运行时数据库路径见 DATABASE_URL / SQLITE_DATABASE_URL / .env.example
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
| 本地开发 / demo | `APP_ENV!=production` 且 `DATABASE_URL` 为空 | 使用 `SQLITE_DATABASE_URL` |
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
tile_specs 1 ── * tiles
tiles 1 ── * tile_videos

users 1 ── * login_logs（预留，本期无写入）
users 1 ── * profile_activity_logs（Sprint 003）
users 1 ── * system_settings.updated_by（Sprint 003，可选 FK）
users 1 ── * audit_logs.actor_user_id（Sprint 003，可选 FK）
users 1 ── * request_logs.actor_user_id（Sprint 004，可选 FK）
users 1 ── * usage_events.actor_user_id（Sprint 004，可选 FK）
request_logs.request_id ── * usage_events.request_id（逻辑关联，非 FK）

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
| usage_events | ✓ Sprint 004 | 产品使用行为埋点事件（REQ-0024） |
| tile_categories | 桩 | 分类 |
| tile_specs | ✓ Sprint 003 | 瓷砖规格主数据 |
| tiles | SKU 主表 | 瓷砖 SKU（扩展） |
| tile_videos | 已实现 | SKU 关联视频元数据 |
| tile_images | 桩 | 瓷砖图片元数据 |
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
| metadata | TEXT | NULL | JSON diff |
| created_at | TEXT | NOT NULL | ISO8601 UTC |

索引：`idx_audit_logs_domain_created (domain, created_at DESC)`

Repository：`audit_log_repository.py`

---

## 5.5 request_logs（Sprint 004 / REQ-0024）

API 请求日志。OpenSpec：`openspec/changes/add-product-usage-logging/`

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | TEXT | PK | UUID |
| request_id | TEXT | NOT NULL | 请求链路 ID；响应头同步返回 `x-request-id` |
| actor_user_id | TEXT | NULL FK → users.id | 已登录操作人，匿名请求为空 |
| actor_role | TEXT | NULL | `admin` / `employee` / `store_owner` 等 |
| client_type | TEXT | NULL | `admin_web`、`storefront_web`、`mini_program`、`api` |
| method | TEXT | NOT NULL | HTTP Method |
| path | TEXT | NOT NULL | API Path，不含 query |
| status_code | INTEGER | NOT NULL | HTTP 状态码 |
| duration_ms | INTEGER | NOT NULL | 请求耗时毫秒 |
| ip_address_masked | TEXT | NULL | 脱敏 IP |
| user_agent_summary | TEXT | NULL | 截断后的 User-Agent 摘要 |
| summary | TEXT | NOT NULL | 管理端列表可读摘要 |
| error_code | TEXT | NULL | 业务错误码或异常编码 |
| result | TEXT | NOT NULL, CHECK | `success` \| `failed` |
| metadata | TEXT | NULL | JSON 扩展信息，已做敏感字段过滤 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |

索引：`idx_request_logs_created`、`idx_request_logs_request_id`、`idx_request_logs_actor_created`、`idx_request_logs_status_created`、`idx_request_logs_path_created`

Repository：`log_repository.py`；Service：`log_service.py`；中间件：`request_logging.py`

---

## 5.6 usage_events（Sprint 004 / REQ-0024）

产品使用行为埋点事件，事件名与属性由产品/研发人为定义并由后端白名单校验。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | TEXT | PK | UUID |
| request_id | TEXT | NULL | 关联 API 请求链路 ID，前端可透传 |
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
| metadata | TEXT | NULL | JSON 属性快照，禁止 password/token/secret 等敏感字段 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |

索引：`idx_usage_events_created`、`idx_usage_events_event_created`、`idx_usage_events_request_id`、`idx_usage_events_actor_created`

Repository：`log_repository.py`；Service：`log_service.py`

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
| display_client | TEXT | NOT NULL | `WEB_HOME` \| `MINIAPP_HOME` \| `TOPIC` |
| position | TEXT | NOT NULL | 展示位置（与 display_client 组合校验） |
| image_object_key | TEXT | NOT NULL | 图片 MinIO 键 |
| image_source | TEXT | NOT NULL | `sku_main_image` \| `sku_gallery_image` \| `custom_upload` \| `topic_cover` |
| sku_gallery_asset_id | INTEGER | FK → tile_images.id | SKU 图库引用 |
| jump_type | TEXT | NOT NULL | `SKU_DETAIL` \| `EXTERNAL_LINK` \| `TOPIC_PAGE` \| `NO_JUMP` |
| sku_id | INTEGER | FK → tiles.id | SKU 跳转目标 |
| external_url | TEXT | NULL | HTTPS 外链 |
| topic_id | INTEGER | FK → topics.id | 专题跳转目标 |
| sort_order | INTEGER | NOT NULL, DEFAULT 100 | 排序 |
| valid_from | TEXT | NULL | 生效开始 |
| valid_to | TEXT | NULL | 生效结束 |
| status | TEXT | NOT NULL, CHECK | `DRAFT` \| `ONLINE` \| `OFFLINE` \| `EXPIRED` |
| remark | TEXT | NULL | 运营备注 |
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

UNIQUE `(display_client, position, title)`。ORM：`src/backend/app/models/banner.py`  
迁移：`migrations.py` → `_ensure_banner_support`

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
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

ORM：`src/backend/app/models/tile.py`  
迁移：`src/backend/app/db/migrations.py` → `_ensure_tiles_sku_extended`、`_ensure_tile_specs_support`

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

## 11. 媒体资产（规划）

`tile_media` 统一图片/视频/文档表尚未落地，见历史建议。当前上传桩返回 `object_key` + `url`，未持久化到 SQLite。

参考：`rules/media.md`、`docs/06-video-asset-management.md`

---

## 12. 迁移与本地数据

| 场景 | 做法 |
|---|---|
| 本地开发 | `data/sqlite/`（见 `rules/data-management.md`） |
| Docker | 卷挂载 + `SQLITE_DATABASE_URL` |
| 生产 | 外部 MySQL 8.0+ + `DATABASE_URL`，不挂载 SQLite 数据库卷 |
| SQLite Schema 变更 | 修改 `schema.sql` + `migrations.py` + OpenSpec change |
| MySQL Schema 变更 | 修改 `schema.mysql.sql` + versioned migration / `schema_migrations` 记录 + OpenSpec change |

**禁止提交：** 运行时 `.db` 文件、真实客户数据（见 `data/README.md`）

---

## 12.1 SQLite → MySQL 类型映射

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

MySQL baseline 保留关键唯一约束与索引：`users.username`、`tiles.sku_code`、`tile_specs(width_mm,length_mm,unit)`、`banners(display_client,position,title)`，以及审计、活动日志与媒体查询路径索引。

## 12.2 初始化与 Seed

- SQLite 路径继续执行 `schema.sql` 后再执行 `migrations.py`，保留 `sqlite_master` / `PRAGMA` 兼容迁移。
- MySQL 路径只执行 `schema.mysql.sql`，不得调用 SQLite introspection 或 SQLite-only DDL。
- MySQL 初始化通过 `schema_migrations(version, applied_at)` 记录 `mysql_baseline_v1`，DDL 使用 `CREATE TABLE IF NOT EXISTS` 保证重复启动幂等。
- 空库首次启动后，默认管理员 seed 继续使用 `ADMIN_USERNAME`、`ADMIN_INITIAL_PASSWORD`、`ADMIN_RESET_PASSWORD_ON_STARTUP`，密码以 bcrypt 哈希保存。

## 13. 与 API 的对应

| 表 | 主要 API |
|---|---|
| users | `POST /api/v1/auth/login`、`GET /api/v1/auth/me`、`/api/v1/admin/users` |
| brands | `/api/v1/admin/brands` |
| tile_categories | `/api/v1/admin/tile-categories` |
| tile_specs | `/api/v1/admin/tile-specs` |
| tiles / tile_images / tile_videos | `/api/v1/admin/tile-skus`、`GET /api/v1/tiles`（展示桩） |

索引：`docs/03-api-index.md`

---

## 14. 维护规则

Schema 变更时 MUST：

1. 更新 `src/backend/app/db/schema.sql`
2. 更新 ORM `src/backend/app/models/`
3. 更新本文件
4. 通过 OpenSpec change 进入开发（`rules/database.md`）
