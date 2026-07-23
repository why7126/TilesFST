---
created_at: 2026-07-21 15:28:51
updated_at: 2026-07-21 23:00:44
---

# Test Plan: fix-prod-admin-brand-banner-save

## Automated Tests

- 后端 Banner API 测试：创建品牌详情 Banner 成功。
- 后端 Banner API 测试：编辑品牌详情 Banner 成功。
- 后端 Banner API 测试：`brand_logo` 图片来源 object key 匹配品牌 Logo 成功。
- 后端 Banner API 测试：`custom_upload` 图片来源使用 Banner 上传 object key 成功。
- 后端 Banner API 测试：品牌不存在、品牌未启用、品牌无 Logo、Logo key 不匹配、标题重复返回稳定业务错误。
- MySQL schema drift/迁移测试：既有 `banners` 表缺 `brand_id` 时可被幂等补齐；重复执行不失败。

## Manual Or Smoke Verification

- 生产或类生产环境执行 migration/drift check 前后表结构对比。
- 管理端保存品牌详情 Banner 并在列表/详情/编辑弹窗回显。
- 小程序对应轮播查询返回已上线且有效期内的品牌详情 Banner。
- 如 API schema 未变，记录不需要 OpenAPI/Orval 的理由；如 schema 变化，记录 OpenAPI/Orval 生成结果。

## Executed

- `uv run ruff check app/db/mysql_migrations.py app/db/session.py tests/test_admin_banners.py ../../tests/test_mysql_migrations.py`
- `uv run pytest tests/test_admin_banners.py ../../tests/test_mysql_migrations.py ../../tests/test_mysql_schema_drift.py ../../tests/test_miniapp_home.py -q`
