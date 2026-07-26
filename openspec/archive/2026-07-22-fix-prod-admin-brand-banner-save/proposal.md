---
created_at: 2026-07-21 15:28:51
updated_at: 2026-07-21 15:28:51
---

# Proposal: fix-prod-admin-brand-banner-save

## Summary

修复 `BUG-0075-prod-admin-brand-banner-save-fails`：生产环境 Web 管理端配置品牌详情跳转 Banner 无法保存。

## Motivation

BUG-0075 已评审通过。现象发生在生产环境管理端，直接阻断品牌类型 Banner 的创建与编辑保存，影响品牌运营位配置、小程序展示入口和品牌主页导流。

本地新库路径中 Banner 模型、API 和测试已覆盖 `jump_type=BRAND_DETAIL`，且 MySQL baseline schema 已声明 `banners.brand_id`。生产失败更可能来自既有 MySQL 表结构漂移：当前初始化依赖 `CREATE TABLE IF NOT EXISTS`，不会自动对已存在的生产 `banners` 表补齐后续字段，保存时可能在写入 `brand_id` 环节触发 SQL 错误。另一个可能分支是品牌未启用、品牌 Logo 缺失或 Logo key 不匹配导致业务校验失败，但该分支也需要明确错误提示和回归覆盖。

## Scope

- 为生产 MySQL 既有 `banners` 表补齐品牌详情跳转所需字段与安全迁移路径，重点覆盖 `brand_id`。
- 为 Banner 保存链路增加 schema drift 检查或启动/发布前可执行的验证证据，避免生产才暴露缺列。
- 保持品牌详情 Banner 业务校验：品牌必须存在且启用，`brand_logo` 来源必须匹配品牌 Logo object key。
- 确保数据库漂移或业务校验失败返回统一、可理解的管理端错误，不泄露原始 SQL、DSN、MinIO 密钥或内部堆栈。
- 补充回归测试，覆盖品牌详情 Banner 新增、编辑、品牌 Logo、自定义上传和典型失败场景。

## Non-Goals

- 不新增 Banner 跳转类型、展示端或展示位置。
- 不放宽品牌启用状态、Logo 引用一致性或上传鉴权规则。
- 不让前端直连对象存储。
- 不导入或修改生产真实客户数据。

## Capabilities

### Modified Capabilities

- `banner-management`: 强化品牌详情 Banner 保存、错误提示和管理端/展示端一致性要求。
- `database`: 要求 MySQL 既有表迁移或漂移检查覆盖 `banners.brand_id` 等品牌 Banner 关键字段。
- `testing`: 要求该修复具备后端 API、MySQL schema drift/迁移和展示读取回归证据。

## Impact

- **api:** 预计仍使用既有 `/api/v1/admin/banners` 创建/编辑接口；如实现新增或修改错误码/响应 schema，必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和错误码文档。
- **database:** 需要 MySQL migration 或等价 schema drift 修复路径；SQLite/MySQL schema 必须保持一致。
- **web/admin:** 管理端品牌详情 Banner 保存应恢复成功，错误提示应可读；如仅依赖后端错误 envelope，不应改 UI 视觉。
- **miniapp:** 保存成功后的品牌详情 Banner 必须继续被小程序对应轮播查询读取，展示端 API 行为不应退化。
- **tests:** 需要新增或更新后端 Banner 测试、MySQL schema drift/迁移验证和必要的 smoke 证据。

## Rollback Plan

若实现阶段的后端代码或迁移导致保存链路异常，可回滚应用镜像到变更前版本。若已对生产 MySQL 执行字段补齐迁移，原则上保留兼容字段；如必须回退数据库变更，需先确认无新增品牌详情 Banner 数据依赖 `brand_id`，并基于发布前备份执行人工回滚。回滚后 BUG-0075 不得关闭，需重新记录生产失败响应与表结构证据。
