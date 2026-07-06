---
created_at: 2026-07-05 07:52:26
updated_at: 2026-07-05 07:52:26
---

# Design: API governance route tags known-debt 修复

## Bug Analysis Report

**BUG:** `BUG-0057-api-governance-tags-known-debt`

**现象：**

- API 标准校验脚本当前可以通过。
- FastAPI 最终 OpenAPI operation tags 仍出现双轨并存或重复，例如 `["admin-brands", "Admin Brands"]` 与 `["auth", "auth"]`。
- `src/web/openapi.json` 中曾统计到 67 个 operation 里有 62 个存在多 tag，15 个存在重复 tag，47 个包含非 kebab-case tag。

**影响：**

- Swagger UI 和管理端接口文档可能出现重复或不一致分组。
- API governance 校验门禁无法代表最终 OpenAPI tags 已治理完成。
- 后续 API 变更会继续携带历史噪声，增加验收和 Orval 生成物 review 成本。

## Root Cause

后端 API route tags 存在两个事实源：

1. `src/backend/app/api/v1/router.py` 的 `include_router(..., tags=[...])`。
2. 各 route handler decorator 中的 `tags=TAGS`。

FastAPI 会合并 router-level 与 operation-level tags。两处值不同时生成技术名 + 展示名双 tag；两处值相同时生成重复 tag。现有 `scripts/validate-api-standard.py` 主要做源码级启发式检查，没有校验最终 OpenAPI operation tags。

## Fix Strategy

### 1. 单一事实源

实现阶段 MUST 选择一个 route tag 事实源。推荐保留 router include 层的 kebab-case tags，移除 route decorator 中会与之叠加的 `tags=` 参数；如果实现选择 decorator 作为事实源，也 MUST 移除 include 层 tags，且确保最终 OpenAPI 每个 operation 只有一个 tag。

### 2. 命名规范

最终 OpenAPI operation tag MUST 使用 kebab-case 技术名，例如：

- `auth`
- `profile`
- `admin-brands`
- `admin-tile-skus`
- `admin-api-docs`

实现不得继续输出 `Admin Brands`、`Admin Tile SKUs` 等展示名 tag 与技术名 tag 并存。

### 3. 治理脚本增强

`scripts/validate-api-standard.py` MUST 基于最终 OpenAPI schema 校验：

- 每个 operation 的 `tags` 数量为 1。
- 每个 operation 不存在重复 tag。
- 每个 tag 符合 kebab-case 命名。
- 校验失败时输出可定位的 method/path/operationId/tag 列表。

源码级 metadata 检查可保留，但不能作为 tags 治理的唯一证据。

### 4. OpenAPI / Orval 同步

实现阶段 MUST 重新导出 `src/web/openapi.json`。若 OpenAPI tag 变化导致 Orval 生成物变化，MUST 运行 `./scripts/generate-openapi-client.sh` 并提交生成结果。若 Orval 无变化，MUST 在 trace 或验收记录中说明原因。

## Testing

- 运行 `python scripts/validate-api-standard.py`，确认通过。
- 增加或更新脚本测试，覆盖多 tag、重复 tag、非 kebab-case tag 均会失败。
- 统计最终 OpenAPI operation tags，确认多 tag operation、重复 tag operation、非 kebab-case tag operation 均为 0。
- 如 OpenAPI/Orval 生成物变化，执行 Orval 生成并 review diff。

## Non-Goals

- 不改变业务 API 路径、请求参数、响应结构或错误码语义。
- 不新增数据库表或迁移。
- 不新增管理端、店主 Web 或小程序页面能力。
- 不解决统一 422 envelope 等其他 API governance 已知事项。
