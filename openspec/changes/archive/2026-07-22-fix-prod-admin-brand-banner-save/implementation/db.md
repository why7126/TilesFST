---
created_at: 2026-07-21 22:54:52
updated_at: 2026-07-21 23:04:48
---

# DB Implementation - fix-prod-admin-brand-banner-save

## 根因复核

当前仓库未包含真实生产 Network、后端日志或 MySQL 表结构导出；实现按 BUG-0075 root-cause 中的高概率分支处理：旧生产 MySQL 已存在 `banners` 表，`CREATE TABLE IF NOT EXISTS` 不会补齐后续新增的 `brand_id`。若目标环境实际返回 `30052` 等业务错误，应继续核对品牌状态、Logo object key、图片来源和标题唯一性。

## 迁移策略

- SQLite：既有 `_ensure_banner_support` 已可对旧 `banners` 表补 `brand_id INTEGER`，本次不改变 SQLite schema 语义。
- MySQL baseline：`schema.mysql.sql` 已包含 `banners.brand_id BIGINT`、`fk_banners_brand`，本次补 `idx_banners_brand`。
- MySQL 既有表：新增 `mysql_migrations.py`，在 MySQL schema 初始化后执行 `mysql_compat_banners_brand_id_v1`。
- 幂等行为：重复执行会先查 `information_schema`，字段、索引或外键存在时不重复创建。
- 查询索引：既有表会补齐 `idx_banners_status_position(display_client, position, status)`、`idx_banners_sort(sort_order, updated_at)` 和 `idx_banners_brand(brand_id)`，与 baseline 查询路径一致。
- 外键取舍：`brand_id` 可为空；若存在非空 `brand_id` 但找不到对应 `brands.id` 的旧数据，迁移保留字段和索引、跳过外键并记录 warning，避免生产脏数据导致启动失败。

## 生产执行与回滚边界

发布前先备份目标 MySQL，再部署包含本迁移的后端镜像或在类生产环境执行初始化流程。推荐补充运行：

```bash
python scripts/check-mysql-schema-drift.py --database-url "$DATABASE_URL"
```

执行证据只记录命令、环境类型、时间、是否存在 `banners.brand_id`、是否有缺表/缺列；不得记录明文 `DATABASE_URL`、密码、MinIO 凭据或真实客户数据。若需回滚应用，可回退镜像；已补的 nullable `brand_id` 字段和索引原则上保留兼容。只有确认无新增品牌详情 Banner 数据依赖后，才可基于备份人工回滚数据库结构。

## Orval 判定

本次不改变 `/api/v1/admin/banners` 请求/响应 schema，不新增错误码，不需要 OpenAPI/Orval。
