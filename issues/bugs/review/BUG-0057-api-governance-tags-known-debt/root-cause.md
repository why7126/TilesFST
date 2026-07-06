---
bug_id: BUG-0057-api-governance-tags-known-debt
title: API governance route tags 历史债清理未闭环根因分析
status: approved
created_at: 2026-07-04 22:27:55
updated_at: 2026-07-04 22:32:37
---

# 直接原因

后端 API route tags 存在两个事实源：

1. `src/backend/app/api/v1/router.py` 在 `include_router(..., tags=[...])` 设置 router-level tags。
2. 多个 route 文件在具体 decorator 上设置 `tags=TAGS`，且 `TAGS` 使用展示名，例如 `["Admin Brands"]`。

FastAPI 生成 OpenAPI 时会合并这两处 tags，导致同一 operation 同时出现技术名与展示名，例如：

```text
["admin-brands", "Admin Brands"]
```

对于 `auth`、`profile`、`uploads` 等模块，router-level tag 与 decorator-level tag 值相同，最终表现为重复 tags，例如：

```text
["auth", "auth"]
```

# 根本原因

API governance 校验覆盖不完整。当前 `scripts/validate-api-standard.py` 主要做源码级启发式检查：确认 route decorator 中是否存在 `response_model`、`tags=`、`summary=`，但没有检查最终 OpenAPI 契约中的 operation tags 是否满足以下约束：

- 每个 operation 仅有一个 tag。
- tag 命名统一，建议为 kebab-case。
- 不允许重复 tag。
- 不允许展示名与技术名双轨并存。

因此，源码层面补齐 `tags=` 后，校验脚本可以通过，但最终 OpenAPI 仍保留重复或不一致 tags。

# 触发条件

满足以下条件时会稳定触发：

1. `router.py` 的 `include_router()` 设置了 `tags=[...]`。
2. 被 include 的 route handler decorator 同时设置了 `tags=...`。
3. 两处 tag 值不同，生成技术名 + 展示名双 tag；两处 tag 值相同，生成重复 tag。

# 缺陷分类

| 维度 | 结论 |
|---|---|
| 类型 | code / governance |
| 位置 | 后端 API route metadata、API governance 校验脚本 |
| 数据库 | 不涉及 |
| 安全 | 不直接涉及鉴权绕过或敏感信息泄露 |
| 前端 | 间接影响 Swagger、管理端接口文档、OpenAPI/Orval 治理体验 |

# 修复方向

建议在后续 `fix-*` Change 中统一处理：

1. 确定 route tag 单一事实源，优先保留一种设置方式。
2. 统一 tags 命名为 kebab-case，例如 `admin-brands`。
3. 扩展 `scripts/validate-api-standard.py`，基于最终 OpenAPI 校验 operation tags。
4. 重新导出 `src/web/openapi.json` 并运行 Orval，确认前端生成物无异常漂移。
