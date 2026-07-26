---
change_id: add-production-mysql-deployment
title: 测试计划
created_at: 2026-06-29 09:55:35
updated_at: 2026-06-29 16:25:27
source_requirement: REQ-0018-production-mysql-deployment
status: proposed
---

# 测试计划

## SQLite 回归

- 运行默认后端 pytest，确保未安装 MySQL 时仍使用 SQLite。
- 验证 `./scripts/docker-up.sh` 仍使用 `docker-compose.yml`、SQLite 数据卷与 MinIO。

执行记录：

- `uv run pytest tests/test_database_config.py tests/test_auth.py`：15 passed, 1 skipped。
- `uv run pytest tests/test_system_settings.py tests/test_database_config.py`：15 passed, 1 skipped。
- `uv run pytest tests/test_database_config.py tests/test_auth.py tests/test_admin_brands.py`：35 passed, 1 skipped, 1 failed；失败项为既有媒体 MIME 断言 `test_upload_brand_logo_rejects_invalid_mime`，当前全局配置允许 `image/gif`，测试期望品牌 Logo 拒绝 gif，非本 Change 数据库/部署改动引入。

## MySQL 集成

- 使用 MySQL 8.0+ 测试实例或 CI service container。
- 设置 `APP_ENV=production` 与 MySQL `DATABASE_URL`。
- 覆盖 schema 初始化、二次启动幂等、默认管理员 seed、`POST /api/v1/auth/login`。
- 覆盖一条媒体相关 smoke：上传图片写入 MinIO，再读取 `/media/{object_key}`。

执行记录：

- 已新增 `@pytest.mark.mysql` optional 测试 `tests/test_database_config.py::test_mysql_schema_seed_and_login_when_database_url_is_provided`。未配置 `MYSQL_TEST_DATABASE_URL` 时默认跳过，不提高本地开发门槛。
- `MYSQL_TEST_DATABASE_URL='mysql+pymysql://test:test@127.0.0.1:3306/tilesfst?charset=utf8mb4' uv run python -m pytest tests/test_database_config.py -m mysql`：1 passed, 4 deselected。
- 外部 MySQL + 外部 MinIO 的本地生产类 smoke 已通过：`tilesfst` MySQL schema 初始化、`smoke_admin` seed/login、MinIO 上传与 `/media/{object_key}` 读取均成功。

## 生产 Compose Smoke

- 校验 `docker-compose.prod.yml` 不含 mysql 服务。
- 校验 `docker-compose.prod.external.yml` 仅包含 backend、web，不含 mysql、minio、minio-init。
- 校验 backend 不挂载 `./data/sqlite`。
- 校验 MinIO volume 持久化与单桶初始化。
- 外部 MinIO 场景校验 backend 注入 `MINIO_ENDPOINT`、`MINIO_BUCKET`、`MINIO_SECURE`，且不启动本地 MinIO。
- 校验错误配置 fail fast：缺失 `DATABASE_URL`、SQLite URL、MySQL 不可达。

执行记录：

- `docker compose -f docker-compose.prod.yml config --services`：仅输出 `minio`、`backend`、`minio-init`、`web`。
- `docker compose -f docker-compose.prod.yml config`：backend 环境包含 MySQL `DATABASE_URL`，backend volumes 仅包含 `data/processed` 与 `data/tmp`，MinIO 使用 named volume `minio-data`。
- `docker compose -f docker-compose.prod.external.yml config --services`：仅应输出 `backend`、`web`。
- 外部 MinIO smoke 读取结果：`/media/images/default/brands/logos/398a172d-2b44-4c3c-a3fc-ba46744ed188.webp` 返回 `tilesfst-external-minio-smoke`。
- 重启 `tile-info-platform-backend`、`tile-info-platform-web`、`minio-server` 后再次读取同一 `/media/{object_key}`：200，内容仍为 `tilesfst-external-minio-smoke`。

## 文档与配置校验

- 检查 `.env.example`、`docs/02-deployment.md`、`docs/04-database-design.md`、`rules/database.md`、`rules/environment.md` 与 README 同步。
- 检查文档不包含真实密钥。
