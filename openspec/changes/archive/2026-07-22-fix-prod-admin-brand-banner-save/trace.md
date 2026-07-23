---
created_at: 2026-07-21 15:28:51
updated_at: 2026-07-21 23:00:44
---

# Trace: fix-prod-admin-brand-banner-save

## Source

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| BUG | `BUG-0075-prod-admin-brand-banner-save-fails` | 生产环境 Web 管理端配置品牌类型 Banner 无法保存 |
| Requirement | `REQ-0062-admin-banner-placement-scope` | Banner 展示端/展示位置收敛与品牌列表页轮播能力 |

## Lifecycle

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-07-21 15:28:51 | `/bug-opsx BUG-0075` | 创建 OpenSpec fix Change 草案 |
| 2026-07-21 15:38:16 | `/sprint-propose` | 纳入 `sprint-010` 正式范围 |
| 2026-07-21 23:00:44 | `/opsx-apply fix-prod-admin-brand-banner-save` | 完成 MySQL 兼容迁移、Banner API 回归测试、数据库漂移测试与验收证据 |

## Sprint

| Sprint | 状态 | 说明 |
|---|---|---|
| `sprint-010` | planning | 等待 `/opsx-apply fix-prod-admin-brand-banner-save` |

## Apply Result

| 项 | 结果 |
|---|---|
| 代码 | `src/backend/app/db/mysql_migrations.py`、`src/backend/app/db/session.py`、`src/backend/app/db/schema.mysql.sql` |
| 测试 | `src/backend/tests/test_admin_banners.py`、`tests/test_mysql_migrations.py`、`tests/test_mysql_schema_drift.py`、`tests/test_miniapp_home.py` |
| 文档 | `docs/04-database-design.md`、`openspec/changes/archive/2026-07-22-fix-prod-admin-brand-banner-save/implementation/db.md` |
| Orval | API schema 未变，不需要 |

## Evidence To Collect During Apply

| 证据 | 要求 |
|---|---|
| 生产/类生产 MySQL 表结构 | 证明 `banners.brand_id` 存在或迁移可补齐 |
| API 回归 | 品牌详情 Banner 新增、编辑、失败场景响应 |
| 展示读取 | 管理端列表/详情与小程序轮播查询读取同一配置 |
| 测试结果 | 后端 pytest、MySQL drift/迁移验证、必要的 Orval/OpenAPI 检查 |
