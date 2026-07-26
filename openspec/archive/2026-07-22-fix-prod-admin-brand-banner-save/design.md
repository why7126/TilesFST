---
created_at: 2026-07-21 15:28:51
updated_at: 2026-07-21 15:28:51
---

# Design: fix-prod-admin-brand-banner-save

## Context

品牌详情 Banner 保存链路要求请求包含 `jump_type=BRAND_DETAIL` 与 `brand_id`，服务层校验品牌存在且状态为 `ENABLED`，随后 repository 持久化 `banners.brand_id`。当前 MySQL baseline schema 已包含该字段，但生产既有库可能在能力上线前已创建 `banners` 表，后续 `CREATE TABLE IF NOT EXISTS` 不会执行 `ALTER TABLE`，因此缺列会表现为生产保存失败。

## Approach

1. 先在实现阶段增加可重复执行的 MySQL 兼容修复路径，检测 `banners.brand_id` 是否存在；缺失时补列并按当前查询/约束策略补齐必要索引或外键。
2. 保持 SQLite 与 MySQL schema 语义一致，避免只修生产 DDL 而让本地/demo 漂移。
3. 在 Banner admin service/API 层保留现有业务校验，明确区分业务输入错误与数据库环境错误。
4. 为生产 drift 类错误提供运维友好的日志和管理端可理解错误 envelope；日志不得包含密码、DSN 明文、MinIO 凭据或原始请求敏感内容。
5. 通过测试覆盖合法保存、编辑保存、`brand_logo` 与 `custom_upload` 图片来源、品牌禁用/缺 Logo/key 不匹配、以及 MySQL schema drift/迁移验证。

## Data And Migration

- MySQL 迁移 MUST 对既有 `banners` 表幂等执行。
- `brand_id` 应与当前 SQLAlchemy/SQLite 语义保持 nullable，允许非品牌跳转类型为空。
- 若实现补外键，必须考虑既有脏数据；无法安全补外键时，需在实现记录中说明取舍，并至少保证字段、类型和查询索引满足保存链路。
- 迁移前生产发布流程 SHOULD 要求备份或可回滚证据。

## Error Handling

- 业务校验失败继续返回稳定业务错误，例如品牌不存在/未启用、品牌 Logo 不可用、Logo key 不匹配或标题重复。
- 数据库 schema drift 不应以原始 SQLAlchemy/MySQL 异常透传到前端；实现可以在启动/迁移阶段 fail fast，也可以在 API 层包装为统一错误，但必须保证可定位且不泄密。

## OpenAPI And Orval

若仅修复迁移与既有错误处理，不改变请求/响应 schema，则不需要 Orval。若新增错误码、响应字段或管理端表单错误结构，必须重新导出 OpenAPI 并运行 Orval，同步相关文档和测试。
