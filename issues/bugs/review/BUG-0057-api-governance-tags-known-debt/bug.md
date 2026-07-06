---
bug_id: BUG-0057-api-governance-tags-known-debt
title: API governance route tags 历史债清理未闭环
severity: medium
status: in_sprint
owner:
discovered_at: 2026-07-04 15:25:45
environment: local
related_requirement:
related_change: fix-api-governance-route-tags-known-debt
created_at: 2026-07-04 22:21:01
updated_at: 2026-07-05 07:52:26
---

# 现象

API governance 的 route tags 历史债清理未闭环。当前代码中没有字面量为 `known-debt` 的 OpenAPI tag，但后端实时 OpenAPI 仍存在 operation tags 重复或双轨并存的问题。

已确认的表现包括：

- `python scripts/validate-api-standard.py` 可以通过。
- 从当前 FastAPI app 导出的 OpenAPI 中，大量 operation 同时包含 router-level tag 与 decorator-level tag，例如 `["admin-brands", "Admin Brands"]`。
- 部分 operation 出现完全重复 tag，例如 `["auth", "auth"]`。
- `src/web/openapi.json` 中 67 个 operation 里有 62 个 operation 存在多 tag；其中 15 个存在重复 tag，47 个包含非 kebab-case tag。

# 复现步骤

1. 执行 API 标准校验：

   ```bash
   python scripts/validate-api-standard.py
   ```

2. 校验脚本返回通过。
3. 从当前 FastAPI app 导出或检查 OpenAPI operation tags。
4. 观察 `/api/v1/admin/brands`、`/api/v1/admin/banners`、`/api/v1/auth/login` 等 operation 的 `tags` 字段。

# 期望 vs 实际

期望：

- API governance 校验脚本不仅检查 route decorator 是否存在 `tags=`，还应检查最终 OpenAPI 中每个 operation 的 tags 是否唯一、规范、无重复。
- OpenAPI operation tag 应统一使用单一命名体系，建议采用 kebab-case，例如 `admin-brands`。
- Swagger、管理端接口文档与 Orval 相关治理视角应避免重复分组或展示名/技术名双轨并存。

实际：

- 现有 `scripts/validate-api-standard.py` 只做源码级启发式检查，未覆盖最终 OpenAPI tag 质量。
- `router.include_router(..., tags=[...])` 与 route decorator `tags=TAGS` 叠加后，最终 OpenAPI 生成多 tag。
- 多个管理端 route 文件使用展示名常量，例如 `TAGS = ["Admin Brands"]`，与 `router.py` 中的 `admin-brands` 并存。

# 影响范围

- API 治理门禁存在盲区：校验通过不代表 OpenAPI tags 已治理干净。
- Swagger UI 与管理端接口文档可能出现重复或不一致分组。
- 后续 API 变更验收会继续携带历史治理噪声，影响判断新增变更是否引入 tag 漂移。
- Orval 方法生成目前未确认受直接影响，但 OpenAPI 契约质量不稳定会增加前后端协作成本。

# 严重等级说明

严重等级评估为 `medium`。

理由：

- 该问题不直接阻断业务接口调用，也不涉及数据损坏、鉴权绕过或数据库变更。
- 但它会削弱 API governance 门禁可信度，并持续影响 Swagger、管理端接口文档和 OpenAPI 契约维护。
- 修复面集中在后端 route tag 单一事实源与校验脚本增强，适合走常规 `fix-*` Change，不需要 hotfix。
