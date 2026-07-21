---
review_id: REV-REQ-0062-admin-banner-placement-scope-001
requirement_id: REQ-0062-admin-banner-placement-scope
date: 2026-07-20 18:46:39
participants:
  - product
result: approved
created_at: 2026-07-20 18:46:39
updated_at: 2026-07-20 18:46:39
---

# REQ-0062 需求评审

## 评审结论

通过。`REQ-0062-admin-banner-placement-scope` 定位为 Banner 管理能力的范围收敛需求，目标清晰：管理后台 Banner 展示端仅保留“小程序”，展示位置仅保留“首页轮播”和“品牌列表页轮播”，并明确旧数据删除策略。

本需求与 `REQ-0016-banner-management` 的父子关系清楚，未重建 Banner 数据模型；与 `REQ-0060-brand-list-page` 的关系也已说明，品牌列表页轮播需要独立数据来源，不再长期复用首页轮播。验收标准覆盖管理端 UI、后端枚举校验、旧数据删除、小程序查询分流、API/DB/Orval 同步和测试要求，具备进入 `/req-opsx` 的条件。

## 评审清单

- [x] 范围清晰，In Scope / Out of Scope 明确。
- [x] 验收标准可测试，覆盖功能、数据、API、DB、Orval、Web 管理端、小程序和权限安全。
- [x] 优先级 P1 合理，依赖 Banner 管理父需求和品牌列表页轮播来源已记录。
- [x] UI 类需求已有 `prototype/web/context.md` 与 `prototype/web/prototype.html`，PNG 可后续导出，不阻塞评审。
- [x] Knowledge-base gate 为 Pass，已纳入 `admin-list`、`admin-modal`、`media-upload` 横切 AC。
- [x] 无与现有 REQ 重复未说明；本需求是 `REQ-0016` 的配置范围 refinement。

## 条件通过项

- [ ] 后续 `/req-opsx` 的 design.md MUST 明确最终枚举命名：使用新 `MINIAPP` 展示端，还是沿用兼容 `MINIAPP_HOME` 并只改展示文案。
- [ ] 后续 `/req-opsx` 的 design.md MUST 明确旧数据删除执行方式、删除条件、删除数量记录方式和回滚/备份边界。
- [ ] 后续实现 MUST 同步 SQLite/MySQL schema、Pydantic Schema、OpenAPI、Orval、API 文档和数据库文档。
- [ ] 后续实现 MUST 明确品牌列表页轮播查询来源，确保不再使用首页轮播数据作为兜底。

## 后续动作

1. `/req-opsx REQ-0062-admin-banner-placement-scope`
2. `/sprint-propose` 纳入迭代后再开发
