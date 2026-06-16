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
| tiles | 桩 | 瓷砖主表 |
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

- 当 `ADMIN_INITIAL_PASSWORD` 已配置且不存在 `username=admin` 时，创建 admin 用户
- 默认用户名：`admin`；显示名：`系统管理员`

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

## 6. tile_categories

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| name | TEXT | NOT NULL, UNIQUE | 分类名称 |

---

## 7. tiles

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | INTEGER | PK AUTOINCREMENT | |
| name | TEXT | NOT NULL | 瓷砖名称 |
| model | TEXT | NOT NULL | 型号 |
| category_id | INTEGER | FK → tile_categories.id | 可空 |
| color | TEXT | NULL | 颜色 |
| size | TEXT | NULL | 规格尺寸 |
| description | TEXT | NULL | 描述 |
| status | TEXT | NOT NULL, DEFAULT `draft` | 上下架状态 |
| created_at | TEXT | DEFAULT CURRENT_TIMESTAMP | |
| updated_at | TEXT | DEFAULT CURRENT_TIMESTAMP | |

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

## 9. 媒体资产（规划）

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
| users | `POST /api/v1/auth/login`、`GET /api/v1/auth/me` |
| tiles / tile_images | `GET /api/v1/tiles`、`POST /api/v1/admin/tiles`（桩） |

索引：`docs/03-api-index.md`

---

## 12. 维护规则

Schema 变更时 MUST：

1. 更新 `src/backend/app/db/schema.sql`
2. 更新 ORM `src/backend/app/models/`
3. 更新本文件
4. 通过 OpenSpec change 进入开发（`rules/database.md`）
