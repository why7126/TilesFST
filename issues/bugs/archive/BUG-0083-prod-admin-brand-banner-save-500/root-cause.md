---
bug_id: BUG-0083-prod-admin-brand-banner-save-500
status: done
created_at: 2026-07-23 11:19:18
updated_at: 2026-07-23 22:59:48
classification: db/deployment/config
related_requirement: REQ-0062-admin-banner-placement-scope
related_bug: BUG-0075-prod-admin-brand-banner-save-fails
related_change: fix-admin-banner-create-schema-drift
---

# Root Cause - BUG-0083 生产环境创建品牌类型 Banner 保存接口返回 500

## 直接原因

生产环境创建品牌类型 Banner 时，`POST /api/v1/admin/banners` 返回 `500 Internal Server Error`。当前高概率直接原因是生产 MySQL `banners` 表结构与当前应用代码期望不一致，导致 Banner 创建 SQL 在写入某个生产缺失字段时抛出未捕获数据库异常。

本次与已归档 `BUG-0075-prod-admin-brand-banner-save-fails` 高度相关，但现象更明确：创建接口直接返回 500。历史修复已增加 MySQL 兼容迁移，用于补齐 `banners.brand_id`、相关索引和 `fk_banners_brand`；但当前 Banner 创建 SQL 会写入的字段不止 `brand_id`，还包括：

- `image_source`
- `sku_gallery_asset_id`
- `topic_id`
- `valid_from`
- `valid_to`
- `remark`
- 以及其他 Banner 基础字段

如果生产旧表缺失的不止 `brand_id`，或生产镜像未执行到兼容迁移，创建品牌类型 Banner 时仍可能触发 `Unknown column`、外键失败、唯一约束失败或数据长度异常，并以未处理 500 暴露给管理端。

最终直接原因仍需以后端生产日志确认。若日志显示 400 / `30052`，则直接原因应转为品牌业务校验失败；但当前用户观测到的是 HTTP 500，因此数据库结构漂移或运行时异常是第一嫌疑。

## 根本原因

根本原因是生产数据库迁移与发布验证闭环仍不足：

- MySQL baseline 使用 `CREATE TABLE IF NOT EXISTS`，不会对既有生产表执行完整 `ALTER TABLE`。
- 当前 MySQL 兼容迁移实现聚焦 `banners.brand_id`，未覆盖 `banners` 表与 `schema.mysql.sql` 的全部字段 drift。
- 本地后端测试覆盖的是新建 schema 成功路径，不能证明旧生产 MySQL 表升级后所有 Banner 字段均已补齐。
- 发布前缺少目标生产库 schema drift 检查结果，未能证明 `banners` 表已与当前 `schema.mysql.sql` 无阻塞差异。
- `BUG-0075` 修复归档后，生产创建品牌类型 Banner 的真实接口回归证据不足，导致残留问题未被拦截。

## 触发条件

满足以下条件时可触发：

1. 生产环境已部署支持品牌类型 Banner 的前后端功能。
2. 用户在管理端新建 Banner，并选择品牌详情或品牌类型跳转。
3. 前端向 `POST /api/v1/admin/banners` 提交 `jump_type=BRAND_DETAIL`、`brand_id`、`image_source`、`image_object_key` 等字段。
4. 生产 `banners` 表缺失当前创建 SQL 需要写入的字段、约束与当前数据不兼容，或后端镜像未执行最新兼容迁移。

若生产表结构完全一致，则触发条件需转为数据或版本差异，例如品牌未启用、品牌 Logo key 不一致、标题重复、Web bundle 与后端版本不一致等。

## 分类

| 分类 | 判断 |
|---|---|
| db | 是。当前第一嫌疑是生产 MySQL `banners` 表字段或约束与应用代码漂移 |
| deployment | 是。生产发布需要证明兼容迁移执行成功和目标库 schema drift 检查通过 |
| config | 可能。生产前后端版本不一致或连接到旧服务也可能导致 payload / schema 漂移 |
| code | 可能。后续修复可能需要扩展 MySQL 兼容迁移覆盖面，并补充数据库异常映射或健康检查 |
| api | 可能。若修复新增稳定错误码或调整响应契约，需要同步 OpenAPI / Orval / docs |
| security | 否。当前未发现鉴权绕过、密钥泄露、对象存储直连或上传安全放宽问题 |

## 证据

| 位置 | 证据 |
|---|---|
| `issues/bugs/archive/BUG-0083-prod-admin-brand-banner-save-500/capture.md` | 用户明确反馈生产 `POST https://tilesfst.wjoyhappy.site/api/v1/admin/banners` 返回 500 |
| `issues/bugs/archive/BUG-0075-prod-admin-brand-banner-save-fails/root-cause.md` | 历史同类缺陷已指向生产 MySQL Banner 表结构漂移 |
| `src/backend/app/repositories/banner_repository.py` | `create()` 会写入 `image_source`、`sku_gallery_asset_id`、`topic_id`、`brand_id` 等字段 |
| `src/backend/app/db/schema.mysql.sql` | 当前 MySQL baseline 声明了完整 Banner 字段、外键、检查约束与索引 |
| `src/backend/app/db/mysql_migrations.py` | 当前兼容迁移只显式补齐 `brand_id`、相关索引和 `fk_banners_brand` |
| 本地验证 | `src/backend/tests/test_admin_banners.py`、`tests/test_mysql_migrations.py`、`tests/test_mysql_schema_drift.py` 通过，说明新库路径正常，但不能替代生产旧表 drift 验证 |

## 影响判断

该缺陷发生在生产环境，直接阻断品牌类型 Banner 创建闭环。它会影响运营人员配置品牌导流 Banner，并可能影响小程序首页轮播或品牌列表页轮播的品牌入口上线。若根因确认为生产 MySQL schema drift，则后续修复不应只处理单个字段，而应补齐完整 Banner 表迁移、目标库 drift 检查、生产接口回归证据和发布前验证门禁。
