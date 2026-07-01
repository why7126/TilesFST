---
title: 业务流程
purpose: 描述生产部署、双数据库初始化与运维流程
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: draft
created_at: 2026-06-28 20:24:46
updated_at: 2026-06-28 20:24:46
note: REQ-0018-production-mysql-deployment
---

# 业务流程

## 1. 与现有系统的差异

```text
变更前（现网 dev/demo）                    变更后（REQ-0018）
────────────────────────────────────────────────────────────────────────────
数据库: SQLite 文件卷 ./data/sqlite/       生产: 外部 MySQL 8.0+（客户实例）
配置: SQLITE_DATABASE_URL 唯一              新增 DATABASE_URL + APP_ENV=production
初始化: schema.sql + migrations.py         MySQL: 独立 baseline（不跑 PRAGMA 迁移链）
Compose: docker-compose.yml（3+1 服务）    新增 docker-compose.prod.yml（无 mysql）
部署文档: 本地/Demo 为主                    增补 VPS 生产 + 外部 MySQL 章节
```

**不变**：MinIO 单桶策略、上传/媒体 URL 规则、API 契约、Web/小程序端代码、本地 SQLite 默认路径。

## 2. 环境选择流程（backend 启动）

```text
读取 APP_ENV、DATABASE_URL、SQLITE_DATABASE_URL
  ↓
APP_ENV == production ?
  ├─ 是 → DATABASE_URL 必须为 MySQL DSN
  │        ├─ 缺失或 SQLite → fail fast（日志 + 退出）
  │        └─ 有效 → 创建 MySQL engine（pool_pre_ping 等）
  └─ 否 → DATABASE_URL 未设置 ?
            ├─ 是 → 使用 SQLITE_DATABASE_URL（SQLite）
            └─ 否 → 按 DATABASE_URL 连接（可选 dev 连远程 MySQL）
  ↓
按 dialect 分支 init_database()
  ├─ SQLite → schema.sql + migrations.py（现状）
  └─ MySQL  → schema.mysql.sql / versioned SQL（新路径）
  ↓
seed_admin_user（空库时）
  ↓
FastAPI 就绪
```

## 3. 生产首次部署流程（VPS）

```text
运维准备
  ├─ 客户 MySQL: 空库、utf8mb4_unicode_ci、账号 DDL+DML、白名单 VPS IP
  ├─ 生成生产 .env（DATABASE_URL、APP_SECRET_KEY、MINIO_*、ADMIN_*）
  └─ VPS: Docker + Compose 已安装
  ↓
git clone / 拉取镜像
  ↓
cp .env.example → .env.prod（按文档填写，非默认密钥）
  ↓
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
  ├─ minio + minio-init → 单桶就绪
  ├─ backend → 连 MySQL 建表 + admin seed
  └─ web → Nginx 反代 API
  ↓
冒烟
  ├─ GET /health（或等价）
  ├─ POST /api/v1/auth/login（管理员）
  ├─ 上传一张图片 + GET /media/{object_key}
  └─ docker restart backend → 数据仍在
  ↓
ADMIN_RESET_PASSWORD_ON_STARTUP 改回 false（若曾启用）
  ↓
交付客户 / 切换 DNS
```

## 4. 本地开发流程（不变）

```text
cp .env.example .env
./scripts/docker-up.sh
  ↓
backend → SQLite ./data/sqlite/
  ↓
pytest / 日常开发（无 MySQL 依赖）
```

## 5. MySQL Schema 初始化流程

```text
backend 启动（MySQL dialect）
  ↓
检查 migration 版本表 / 表是否存在
  ↓
空库 → 执行 schema.mysql.sql（全量 CREATE）
  ↓
已有库 → 按版本执行 forward SQL（本期可为 v1 baseline only）
  ↓
MUST NOT 调用 sqlite_master / PRAGMA 逻辑
  ↓
seed_admin_user（users 表无 ADMIN_USERNAME 时）
```

## 6. 与关联 REQ / 规范差异

| 关联 | 差异说明 |
|---|---|
| REQ-0017 系统设置 | 系统设置页 **不** 在线修改 `DATABASE_URL`；仍为运维 env |
| REQ-0012 对象存储 | MinIO 单桶与 Key 规则不变；生产 Compose 须持久化 MinIO 卷 |
| `rules/database.md` | 从「仅 SQLite」扩展为 dev SQLite + prod MySQL |
| `AGENTS.md` 技术栈 | 归档后更新为双引擎描述 |
| BUG-0005 重启丢登录 | 生产依赖 MySQL 持久化，非 SQLite 文件卷；行为应对齐「DB 持久则会话/用户仍在」 |

## 7. 依赖

| 依赖 | 说明 |
|---|---|
| `app/core/config.py` | `DATABASE_URL`、`APP_ENV` 解析 |
| `app/db/session.py` | 双 dialect engine |
| `app/db/schema.mysql.sql`（或等价） | MySQL baseline DDL |
| `app/db/mysql_migrations/`（或等价） | MySQL forward 迁移 |
| `docker-compose.prod.yml` | 生产编排 |
| `docs/02-deployment.md` | 生产 runbook |
| MySQL driver（pymysql 等） | pyproject + Docker 镜像 |

## 8. 明确不在本期流程

- SQLite `.db` 文件导入 MySQL
- Compose 内 `docker run mysql:8`
- K8s rollout / Helm upgrade
- MySQL 主从切换与自动 failover
