---
bug_id: BUG-0075-prod-admin-brand-banner-save-fails
status: done
created_at: 2026-07-21 15:21:45
updated_at: 2026-07-22 08:59:18
classification: db/deployment/config
related_requirement: REQ-0062-admin-banner-placement-scope
related_change: fix-prod-admin-brand-banner-save
---

# Root Cause - BUG-0075 生产环境管理端品牌类型 Banner 配置无法保存

## 直接原因

生产环境配置品牌类型 Banner 无法保存，当前高概率直接原因是生产 MySQL `banners` 表结构与当前应用代码期望不一致，尤其是缺少或未正确同步 `brand_id` 字段及相关约束。

当前管理端品牌类型 Banner 保存链路会提交并持久化以下关键字段：

- `jump_type: BRAND_DETAIL`
- `brand_id`
- `image_source`
- `image_object_key`

后端保存时会写入 `banners.brand_id`。本地新库路径已通过 `src/backend/tests/test_admin_banners.py` 中品牌类型 Banner 创建测试，说明当前代码与全新 schema 是匹配的；生产环境失败更符合“生产库由旧版本表结构升级而来，但未执行补列 / 约束同步”的表现。

生产日志仍需最终确认。如果保存接口返回 400 且错误码为 `30052`，则直接原因可能转为品牌业务校验失败；如果返回 500、SQLAlchemy/MySQL 错误或 `Unknown column 'brand_id'`，则可确认数据库结构漂移。

## 根本原因

根本原因是生产数据库结构变更缺少可执行、可验证的 MySQL 迁移闭环：

- MySQL 初始化使用 `schema.mysql.sql` 中的 `CREATE TABLE IF NOT EXISTS`，只会创建缺失表，不会对既有生产表执行 `ALTER TABLE`。
- SQLite 轻量迁移中存在对既有 `banners` 表补 `brand_id` 的逻辑，但该逻辑不适用于生产 MySQL。
- 品牌类型 Banner 能力依赖新增的 `banners.brand_id`，但生产发布前缺少针对目标 MySQL 的 schema drift 检查或显式迁移证据。
- 管理端 Banner 保存接口本地测试覆盖了新库成功路径，但未覆盖“生产旧表结构升级后仍能保存品牌类型 Banner”的兼容验证。

因此，生产库若在品牌类型 Banner 能力上线前已创建 `banners` 表，后续应用版本即使部署了新代码，也可能因为表结构未同步而保存失败。

## 次要可能原因

如果生产表结构已确认一致，则需继续排查以下数据或版本差异：

- 所选品牌不是 `ENABLED` 状态，后端会返回“关联品牌不存在或未启用”。
- 所选品牌没有 `logo_object_key`，但用户选择了“使用品牌 Logo”。
- 前端提交的 `image_object_key` 与生产数据库中的品牌 `logo_object_key` 不一致。
- 生产 Web bundle 与后端镜像版本不一致，导致枚举值或 payload 字段不匹配。
- 同一展示端与展示位置下标题重复，触发唯一性校验。

## 触发条件

满足以下条件时可触发：

1. 生产环境 Web 管理端已部署支持品牌类型 Banner 的前后端代码。
2. 用户在 Banner 管理中选择品牌详情 / 品牌类型跳转。
3. 保存请求 payload 包含 `brand_id`。
4. 生产 MySQL `banners` 表缺少 `brand_id` 字段，或相关外键 / 约束与应用期望不一致。

若表结构一致，则触发条件转为品牌数据不满足后端校验，例如品牌未启用、Logo 为空或 Logo key 不一致。

## 分类

| 分类 | 判断 |
|---|---|
| db | 是。品牌类型 Banner 保存依赖 `banners.brand_id`，生产 MySQL 结构漂移会直接阻断写入 |
| deployment | 是。MySQL 生产发布缺少显式迁移 / drift 校验闭环 |
| config | 可能。若生产前后端版本不一致或部署环境变量指向旧服务，也会出现保存失败 |
| code | 可能。后续可能需要补 MySQL 迁移、错误映射或兼容检查代码 |
| api | 可能。若修复调整错误码或响应契约，需要同步 OpenAPI / Orval |
| security | 否。当前未发现鉴权绕过、密钥、对象存储直连或上传安全放宽问题 |

## 证据

| 位置 | 证据 |
|---|---|
| `src/backend/app/repositories/banner_repository.py` | `create()` / `update()` 均写入 `brand_id` 字段 |
| `src/backend/app/services/banner_admin_service.py` | `BRAND_DETAIL` 要求 `brand_id` 非空、品牌启用，并校验品牌 Logo 引用 |
| `src/backend/app/db/schema.mysql.sql` | 新 schema 已声明 `banners.brand_id` 和 `fk_banners_brand` |
| `src/backend/app/db/session.py` | MySQL 初始化执行 `CREATE TABLE IF NOT EXISTS`，不负责既有表 ALTER |
| `src/backend/tests/test_admin_banners.py` | 新库路径下品牌类型 Banner 创建测试通过 |

## 影响判断

该缺陷发生在生产环境，直接阻断品牌类型 Banner 的保存闭环。它不仅影响运营人员维护 Banner，也会影响小程序品牌导流入口上线。如果根因确认为生产 MySQL schema drift，则属于发布与数据库迁移治理问题，需要在修复中同时补齐生产迁移、drift 检查和回归测试证据。
