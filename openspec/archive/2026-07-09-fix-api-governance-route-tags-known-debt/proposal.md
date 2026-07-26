---
created_at: 2026-07-05 07:52:26
updated_at: 2026-07-05 07:52:26
---

# Change: fix-api-governance-route-tags-known-debt

## Why

BUG-0057 暴露出 API governance 的 route tags 历史债没有闭环：`python scripts/validate-api-standard.py` 可以通过，但最终 OpenAPI 中仍存在 operation 多 tag、重复 tag、展示名与技术名双轨并存的问题，例如 `["admin-brands", "Admin Brands"]` 与 `["auth", "auth"]`。

这会削弱 API 标准校验的可信度，污染 Swagger UI / 管理端接口文档的分组展示，并让后续 API 变更难以判断是否引入新的 tag 漂移。

## What Changes

- 统一后端 route tag 的单一事实源，避免 router-level tags 与 decorator-level tags 叠加。
- 统一最终 OpenAPI operation tag 命名为 kebab-case 技术名。
- 扩展 `scripts/validate-api-standard.py`，基于最终 OpenAPI 校验多 tag、重复 tag 与非 kebab-case tag。
- 重新导出 `src/web/openapi.json`，如生成物变化则运行 Orval 并同步生成客户端。
- 增加回归测试，证明 tag 漂移会被治理脚本拦截。

## Impact

- 影响后端 API metadata：route tag 设置方式与最终 OpenAPI tags。
- 影响治理脚本：`scripts/validate-api-standard.py`。
- 影响 OpenAPI/Orval 生成物：`src/web/openapi.json` 与可能的 `src/web/src/shared/api/generated.ts`。
- 不改变 API 路径、请求参数、响应结构、错误码语义或数据库表结构。
- 不新增 Web、小程序或管理端页面能力，仅改善 Swagger / 管理端接口文档的契约元数据质量。

## Rollback Plan

如实现导致 OpenAPI 分组异常，可回滚 route tag 单一事实源改动、恢复治理脚本新增校验，并重新导出 OpenAPI/Orval 生成物。回滚后必须在 BUG trace 中记录 tags 历史债恢复为未闭环状态，并保留人工 OpenAPI tag 检查作为临时规避。
