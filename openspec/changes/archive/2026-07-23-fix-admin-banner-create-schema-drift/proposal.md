## Why

`BUG-0083-prod-admin-brand-banner-save-500` 记录了生产环境创建品牌类型 Banner 时 `POST /api/v1/admin/banners` 返回 500 的回归/残留缺陷。历史修复已补齐 `banners.brand_id` 的 MySQL 兼容迁移，但当前创建接口还会写入更多 Banner 字段；如果生产旧表存在多字段 drift，仍会在业务请求中暴露未处理数据库异常。

## What Changes

- 扩展生产 MySQL `banners` 兼容迁移，从只补 `brand_id` 扩展为覆盖创建/编辑接口写入的完整 Banner 字段。
- 强化 schema drift 检查与发布证据，要求生产或目标 MySQL 在修复发布前证明 `banners` 无阻塞缺列。
- 保持 Admin Banner API 路径、请求体和成功响应语义不变；错误场景必须返回统一 envelope，不得暴露原始 SQL、DSN、MinIO 凭据或内部堆栈。
- 补充旧 MySQL 表缺列迁移测试、品牌类型 Banner 新增/编辑回归测试和生产等价 smoke 清单。
- 不新增 Banner 类型、不新增展示位置，不放宽品牌状态、Logo 引用、上传鉴权或对象存储策略。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `banner-management`: 强化品牌类型 Banner 保存规则，要求生产既有 MySQL 表具备创建/编辑接口写入的完整 Banner 字段，且缺列不得在 API 中表现为裸 500。
- `database`: 扩展 MySQL 初始化/兼容迁移要求，要求既有 `banners` 表缺失关键字段时可被幂等补齐或在发布前给出可运维阻断。
- `deployment`: 扩展生产 MySQL 前置检查，要求部署/发布文档包含 Banner 表 schema drift 检查与生产 smoke 证据。

## Impact

- 后端：预计修改 `src/backend/app/db/mysql_migrations.py`、可能调整数据库异常映射或启动日志；Admin Banner service/repository 行为保持兼容。
- 数据库：MySQL 兼容迁移补齐既有 `banners` 表缺失字段、必要索引和可安全添加的外键；SQLite schema 不应改变。
- API：`POST /api/v1/admin/banners`、`PUT /api/v1/admin/banners/{id}` 路径和请求/响应结构不变；若新增错误码，需要同步 OpenAPI / Orval / docs。
- 文档：需同步 `docs/04-database-design.md`、`docs/02-deployment.md`，必要时同步 `docs/03-api-index.md` 和错误码文档。
- 测试：需补 MySQL 兼容迁移测试、schema drift 测试、Banner API 品牌类型新增/编辑和失败场景回归。
- 发布：需要目标 MySQL schema drift 检查、迁移执行证据、回滚边界和生产等价 smoke。
