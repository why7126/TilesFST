---
purpose: 数据库文档
content: SQLite 表结构、约束、种子数据与迁移说明
source: src/backend/app/db/schema.sql / Sprint 001 auth
update_method: schema 变更时同步更新 schema.sql 与本文件
note: 运行时数据库路径见 SQLITE_DATABASE_URL / .env.example
---

# 数据库设计

## 1. 概述

| 项目 | 说明 |
|---|---|
| 引擎 | SQLite 3 |
| Schema 源 | `src/backend/app/db/schema.sql` |
| 初始化 | 应用启动 `init_database()` 执行 schema |
| ORM | SQLAlchemy 2.x（`src/backend/app/models/`） |
| 对象存储 | MinIO（图片/视频文件，非 SQLite） |

设计原则：结构化业务数据存 SQLite；媒体二进制存 MinIO，SQLite 存元数据与 object_key。

---

## 2. ER 关系（当前）

```text
tile_categories 1 ── * tiles 1 ── * tile_images
brands 1 ── * tiles
tiles 1 ── * tile_videos

users 1 ── * login_logs（预留，本期无写入）

（users 与 tiles 无直接外键，权限通过 JWT role 控制）
```

---

## 3. 表清单

| 表 | Sprint 001 | 说明 |
|---|---|---|
| users | ✓ 使用中 | 认证与角色 |
| login_logs | ✓ 已建表 | 登录审计预留 |
| tile_categories | 桩 | 分类 |
| tiles | SKU 主表 | 瓷砖 SKU（扩展） |
| tile_videos | 已实现 | SKU 关联视频元数据 |
| tile_images | 桩 | 瓷砖图片元数据 |

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

## 7. tiles（SKU 主表）

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| name | TEXT | NOT NULL | SKU 名称 |
| sku_code | TEXT | NOT NULL, UNIQUE | SKU 编码 |
| brand_id | INTEGER | NOT NULL, FK → brands.id | 品牌 |
| category_id | INTEGER | NOT NULL, FK → tile_categories.id | 类目 |
| size | TEXT | NOT NULL | 规格尺寸 |
| surface_finish | TEXT | NOT NULL | 表面工艺 |
| color_family | TEXT | NULL | 主色系 |
| reference_price | REAL | NULL | 参考价格（元） |
| remark | TEXT | NULL | 备注 |
| status | TEXT | NOT NULL | `PUBLISHED` \| `DRAFT` \| `NEEDS_COMPLETION` \| `DISABLED` |
| created_at | TEXT | NOT NULL | ISO8601 UTC |
| updated_at | TEXT | NOT NULL | ISO8601 UTC |

ORM：`src/backend/app/models/tile.py`  
迁移：`src/backend/app/db/migrations.py` → `_ensure_tiles_sku_extended`

---

## 8. tile_images

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| tile_id | INTEGER | NOT NULL, FK → tiles.id | |
| object_key | TEXT | NOT NULL | MinIO 对象键 |
| url | TEXT | NOT NULL | 访问 URL |
| is_main | INTEGER | NOT NULL, DEFAULT 0 | 1=主图 |
| sort_order | INTEGER | NOT NULL, DEFAULT 0 | 排序 |

---

## 9. tile_videos

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

## 10. 媒体资产（规划）

`tile_media` 统一图片/视频/文档表尚未落地，见历史建议。当前上传桩返回 `object_key` + `url`，未持久化到 SQLite。

参考：`rules/media.md`、`docs/06-video-asset-management.md`

---

## 10. 迁移与本地数据

| 场景 | 做法 |
|---|---|
| 本地开发 | `data/sqlite/`（见 `rules/data-management.md`） |
| Docker | 卷挂载 + `SQLITE_DATABASE_URL` |
| Schema 变更 | 修改 `schema.sql` + OpenSpec change；生产需迁移脚本（待引入 Alembic 或等价方案） |

**禁止提交：** 运行时 `.db` 文件、真实客户数据（见 `data/README.md`）

---

## 11. 与 API 的对应

| 表 | 主要 API |
|---|---|
| users | `POST /api/v1/auth/login`、`GET /api/v1/auth/me`、`/api/v1/admin/users` |
| brands | `/api/v1/admin/brands` |
| tile_categories | `/api/v1/admin/tile-categories` |
| tile_categories | `/api/v1/admin/tile-categories` |
| tiles / tile_images / tile_videos | `/api/v1/admin/tile-skus`、`GET /api/v1/tiles`（展示桩） |

索引：`docs/03-api-index.md`

---

## 12. 维护规则

Schema 变更时 MUST：

1. 更新 `src/backend/app/db/schema.sql`
2. 更新 ORM `src/backend/app/models/`
3. 更新本文件
4. 通过 OpenSpec change 进入开发（`rules/database.md`）
