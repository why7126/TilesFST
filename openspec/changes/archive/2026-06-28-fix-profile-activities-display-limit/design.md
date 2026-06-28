## Context

- **REQ**: `REQ-0014-profile-page` v1.1（操作记录展示上限 20→5）
- **Related BUG**: `BUG-0049-profile-recent-activities-limit-five`（**rejected**，改需求修订）
- **Parent change**: `add-admin-profile-page`（已 archive，limit=20）
- **Current code**: `ProfileService.list_activities` → `list_by_user(..., limit=20)`；`ProfilePage` 全量 `map` activities

### 原型优先级（MUST）

```text
1. issues/requirements/archive/REQ-0014-profile-page/acceptance.md AC-024（v1.1 limit 5）
2. issues/requirements/archive/REQ-0014-profile-page/prototype/web/profile-page-context.md（limit 5）
3. issues/requirements/archive/REQ-0014-profile-page/prototype/web/profile-page.html §6（示例 3 条，与 5 条上限一致）
4. issues/requirements/archive/REQ-0014-profile-page/prototype/images/profile-page.png
5. rules/ui-design.md
6. openspec/specs/admin-profile-page/spec.md（归档前为 20，本 change delta 修正为 5）
```

## Conflict Resolution

| 来源 | 原表述 | v1.1 / 本 change | 决议 |
|---|---|---|---|
| `openspec/specs` | limit 20 | limit 5 | **MODIFIED** delta，archive 时合并 |
| `add-admin-profile-page` 实现 | limit=20 | limit=5 | 本 fix 覆盖 |
| prototype HTML | 示例 3 条 | 最多 5 条 | **无冲突** |
| prototype PNG | 少量 timeline 项 | 最多 5 条 | **无冲突** |
| BUG-0049 capture（初稿） | 误以为缺陷 | 需求修订 | 已驳回 |

## Goals / Non-Goals

**Goals:**

- API 与页面 timeline **最多展示 5** 条最近操作记录。
- 审计写入（login / profile_update / avatar_update）不变。
- pytest 覆盖 limit=5 与倒序。

**Non-Goals:**

- 新增 `limit` 查询参数（本期固定 5；business-flow 中 `?limit=5` 为文档示意，路由可不暴露 Query）。
- 「查看更多」、独立审计列表页。
- timeline CSS、卡片布局变更。
- `profile_activity_logs` schema 或写入策略变更。

## Decisions

### D1：后端默认 limit=5（非仅前端 slice）

- **决策**：`ProfileService.list_activities` 与 `ProfileActivityRepository.list_by_user` 默认 `limit=5`。
- **理由**：契约与 UI 一致；减少无效 payload；与 REQ FR-006 / AC-024 对齐。
- **备选**：仅前端 `slice(0,5)` — 拒绝（API 仍返 20，浪费带宽且测试难对齐）。

### D2：不在 API route 暴露 Query limit

- **决策**：`get_profile_activities` 保持无 `limit` 参数，service 层固定 5。
- **理由**：v1.1 无「用户自选条数」需求；最小 diff。
- **备选**：`limit` Query（max 20）— 延后，非本期 scope。

### D3：前端

- **决策**：`ProfilePage` 继续全量渲染 `activities`；依赖 API 返回 ≤5。
- **理由**：`fetchProfileActivities` 无需改 URL；保存/头像后 refresh 仍正确。
- **可选**：vitest mock 6 条断言页面仅 5 条（若 mock 全量则需 slice 测试 — 后端改后 mock ≤5 即可）。

### D4：OpenAPI / Orval

- **决策**：若 OpenAPI summary/description 写明「20 条」则改为「5 条」；无 schema 变更则 Orval **MAY** 跳过（无新参数）。
- **理由**：行为变更非类型变更。

### D5：UI 策略

- **决策**：`--skip-explore`；无 CSS Port / 新组件。
- **理由**：纯数据条数策略调整。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| 用户需查看更早记录 | 本期无「查看更多」；完整记录在 DB，未来可独立审计页 |
| 与 v1 文档残留「20」 | REQ v1.1 已修订；archive 合并 spec |

## Migration Plan

- 无 DB migration；部署 backend 即生效。
- 回滚见 proposal Rollback Plan。

## Open Questions

- 无（v1.1 文档已修订，BUG-0049 已驳回）。
