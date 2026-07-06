---
bug_id: BUG-0057-api-governance-tags-known-debt
title: API governance route tags 历史债清理未闭环验收标准
status: approved
created_at: 2026-07-04 22:27:55
updated_at: 2026-07-04 22:32:37
---

# 验收标准

## AC-001 route tag 单一事实源

- [ ] 后端 API route tags 仅保留一个事实源。
- [ ] 同一 operation 不再同时出现 router-level tag 与 decorator-level tag 合并后的双 tag。
- [ ] `auth`、`profile`、`uploads` 等路由不再生成重复 tag，例如 `["auth", "auth"]`。

## AC-002 OpenAPI tag 命名统一

- [ ] 最终 OpenAPI 中每个 operation 的 `tags` 数量为 1。
- [ ] tag 使用统一命名体系，建议为 kebab-case，例如 `admin-brands`、`admin-tile-skus`。
- [ ] 不再出现 `Admin Brands`、`Admin Tile SKUs` 等展示名 tag 与技术名 tag 并存。

## AC-003 API governance 校验补强

- [ ] `scripts/validate-api-standard.py` 增加最终 OpenAPI operation tags 校验。
- [ ] 校验覆盖多 tag、重复 tag、非 kebab-case tag。
- [ ] 构造或保留回归测试，证明上述异常会导致校验失败。

## AC-004 OpenAPI / Orval 同步

- [ ] 重新导出 `src/web/openapi.json`。
- [ ] 如生成物变化，运行 Orval 并同步 `src/web/src/shared/api/generated.ts`。
- [ ] 确认管理端接口文档页面的 tag 展示不再受重复/双轨 tags 影响。

## AC-005 回归验证

- [ ] `python scripts/validate-api-standard.py` 通过。
- [ ] OpenAPI operation tags 统计结果满足：多 tag operation 为 0，重复 tag operation 为 0，非 kebab-case tag operation 为 0。
- [ ] 不改变 API 路径、请求参数、响应结构或错误码语义。
