---
change_id: add-production-mysql-deployment
title: 实现任务清单
created_at: 2026-06-29 09:55:35
updated_at: 2026-06-29 16:21:57
source_requirement: REQ-0018-production-mysql-deployment
status: proposed
---

## 1. 数据库配置与依赖

- [x] 1.1 在后端配置中新增 `APP_ENV`、`DATABASE_URL`，保留 `SQLITE_DATABASE_URL` 非生产默认路径
- [x] 1.2 添加 MySQL driver 依赖（如 `pymysql` 或团队确认等价物）并更新 lock / Docker 构建
- [x] 1.3 实现 production `DATABASE_URL` 校验：缺失、SQLite URL、非法 MySQL URL 均 fail fast
- [x] 1.4 确认日志脱敏，启动失败不得输出 MySQL 密码或管理员初始密码

## 2. Dialect-aware Session 与初始化

- [x] 2.1 拆分 SQLite 与 MySQL engine 参数，MySQL 启用 `pool_pre_ping` 和连接池默认值
- [x] 2.2 保留 SQLite `schema.sql` + `migrations.py` 路径，确保 dev/demo 不回归
- [x] 2.3 新增 MySQL 初始化入口（`schema.mysql.sql` 和/或 versioned migration SQL）
- [x] 2.4 MySQL 路径禁止调用 `sqlite_master`、`PRAGMA`、SQLite-only DDL
- [x] 2.5 MySQL 初始化支持幂等或 migration 版本表

## 3. MySQL Baseline DDL 与管理员 Seed

- [x] 3.1 汇总当前 SQLite 最终态表结构，形成 MySQL baseline 表清单
- [x] 3.2 创建 MySQL DDL，覆盖 users、brands、tile_categories、tiles、tile_images、tile_videos、tile_specs、topics、banners、system_settings、audit_logs、profile_activity_logs、password_change_attempts 等实际表
- [x] 3.3 对齐关键唯一约束、索引、外键语义和枚举约束
- [x] 3.4 更新 `implementation/db.md`，记录 SQLite→MySQL 类型映射、索引和约束差异
- [x] 3.5 确认空 MySQL 库首次启动后默认管理员 seed 与 `ADMIN_RESET_PASSWORD_ON_STARTUP` 行为一致

## 4. 生产 Docker Compose 与 MinIO

- [x] 4.1 新增 `docker-compose.prod.yml` 或等价生产 Compose 文件
- [x] 4.2 生产 Compose 包含 backend、web、minio、minio-init，且不包含 mysql 服务
- [x] 4.3 生产 backend 通过 `DATABASE_URL` 连接外部 MySQL，且不挂载 `./data/sqlite`
- [x] 4.4 生产 MinIO 使用持久化 volume、单桶 `MINIO_BUCKET`、非默认 access/secret
- [x] 4.5 确认 Web Nginx 反代 API 与 `/media/`，`client_max_body_size` 与上传限制对齐
- [x] 4.6 新增外部 MySQL + 外部 MinIO 生产 Compose 变体，且只启动 backend、web

## 5. 文档与环境变量同步

- [x] 5.1 更新根目录 `.env.example`，说明 `APP_ENV`、`DATABASE_URL`、`SQLITE_DATABASE_URL` 与生产 MySQL 示例
- [x] 5.2 更新 `src/backend/.env.example` 与 `src/backend/.env.docker`，开发默认仍为 SQLite
- [x] 5.3 更新 `docs/02-deployment.md`，增加 VPS + 外部 MySQL + MinIO 生产部署 runbook
- [x] 5.3a 更新 `docs/02-deployment.md`，增加外部 MySQL + 外部 MinIO 生产部署 runbook
- [x] 5.4 更新 `docs/04-database-design.md`，说明 SQLite dev/demo + MySQL prod 双引擎
- [x] 5.5 更新 `rules/database.md`、`rules/environment.md`、`README.md`
- [x] 5.6 归档前更新 `openspec/project.md` 技术栈描述

## 6. 测试与验证

- [x] 6.1 新增 MySQL 集成测试或 optional pytest marker，覆盖 schema 初始化、管理员 seed、登录或简单 CRUD
- [x] 6.2 如使用 CI，新增 MySQL 8 service container job；如暂不启用 CI，补充 documented manual smoke
- [x] 6.3 运行 SQLite 默认后端测试，确保本地路径不依赖 MySQL
- [x] 6.4 运行生产 Compose 配置校验，确认不包含 mysql 服务且 env 注入正确
- [x] 6.5 完成一次生产类图片上传 + `/media/{object_key}` 读取 smoke

## 7. OpenSpec 与追溯

- [x] 7.1 更新 REQ-0018 trace 的 `openspec_changes` 状态
- [x] 7.2 `/opsx-apply` 完成后运行 Workflow Sync
- [x] 7.3 归档前运行 `openspec validate add-production-mysql-deployment --strict`
- [x] 7.4 归档前确认不需要 Orval；如实现产生 API 契约变更则必须生成 OpenAPI 客户端
