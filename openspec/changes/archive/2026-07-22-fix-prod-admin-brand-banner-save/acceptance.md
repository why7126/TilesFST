---
created_at: 2026-07-21 15:28:51
updated_at: 2026-07-21 23:04:48
---

# Acceptance: fix-prod-admin-brand-banner-save

## Acceptance Criteria

- 生产或类生产 MySQL `banners` 表包含 `brand_id`，旧表缺列时有幂等迁移或等价 drift 修复路径。
- 管理端可成功新建 `jump_type=BRAND_DETAIL` Banner，并持久化 `brand_id`、`image_source`、`image_object_key`、展示位置、排序和有效期。
- 管理端可成功编辑既有品牌详情 Banner。
- `brand_logo` 与 `custom_upload` 两种图片来源均按规则保存。
- 品牌不存在、品牌未启用、品牌无 Logo、Logo key 不匹配、标题重复等失败场景返回明确错误，不暴露原始 SQL、DSN、MinIO 凭据或内部堆栈。
- 保存成功后，管理端列表、详情和小程序对应轮播查询读取到同一配置。
- 非品牌跳转类型 Banner 保存、上线、下线和删除逻辑不回归。
- 自动化测试覆盖本修复的核心保存、失败和数据库兼容路径。

## Evidence

| 类型 | 结果 |
|---|---|
| MySQL 兼容迁移 | 新增 `mysql_compat_banners_brand_id_v1`：旧 `banners` 表缺 `brand_id` 时补列，补 `idx_banners_status_position`、`idx_banners_sort`、`idx_banners_brand`，无脏品牌引用时补 `fk_banners_brand` |
| API 回归 | `src/backend/tests/test_admin_banners.py` 覆盖品牌详情新增、编辑、`brand_logo`、`custom_upload`、禁用品牌、无 Logo、Logo key 不匹配、重复标题与非品牌逻辑 |
| 展示读取 | `tests/test_miniapp_home.py` focused 回归通过，继续按 `position` 区分首页与品牌列表页轮播 |
| 数据库漂移 | `tests/test_mysql_migrations.py` 与 `tests/test_mysql_schema_drift.py` 通过；默认 SQLite pytest 不依赖本机 MySQL |
| OpenAPI/Orval | 请求/响应 schema 与错误码未变，不需要 Orval |
| 知识库 | 本次属于已有生产 DB drift 治理模式的具体落地，已在 implementation 记录执行与回滚边界，不新增 incident 文档 |
