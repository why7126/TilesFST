---
requirement_id: REQ-0077-category-name-max-length-15
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-27 23:56:26
updated_at: 2026-07-28 08:18:07
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0077-category-name-max-length-15
requirement_name: category-name-max-length-15
requirement_type: 管理端 / 类目管理输入规则
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 待评估
  wechat_miniapp: 待评估
related_requirements:
  - REQ-0005-tile-category-management
related_changes:
  - update-category-name-max-length-15
lifecycle:
  captured: 2026-07-27 23:56:26
  generated: 2026-07-28 00:04:27
  completed: 2026-07-28 00:06:52
  reviewed: 2026-07-28 00:13:39
  approved: 2026-07-28 00:13:39
iteration: sprint-013
openspec_changes:
  - change_id: update-category-name-max-length-15
    type: update
    status: archived
readiness: Ready
readiness_notes: 已通过需求评审，可执行 req-opsx；后续实现前需确认 DB 字段约束、OpenAPI/Orval 和展示端回归。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - prototype/web/prototype-context.md
  - prototype/web/category-name-max-length-15.html
  - review.md
expected_openspec_change: update-category-name-max-length-15
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/retrospectives/sprint-012-retrospective.md
cross_cutting_tags:
  - admin-list
  - admin-modal
knowledge_base_summary: 已将列表分页/toast/confirm/指标卡一致性与弹窗 CSS cascade/computed width/矮视口滚动转化为 8 条 AC-XCUT；Sprint-012 复盘提醒后续归档前避免 acceptance 残留 stale 文案。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-28 08:18:07 | lifecycle-stage-migrate | review → archive（/opsx-archive update-category-name-max-length-15） |
| 2026-07-28 08:17:41 | /opsx-archive | Change `update-category-name-max-length-15` 已归档，状态同步完成。 |
| 2026-07-28 08:10:17 | /opsx-apply | Change `update-category-name-max-length-15` apply 完成，待 archive。 |
| 2026-07-28 00:15:03 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-27 23:56:26 | `/capture` | 记录类目名称输入长度上限从 10 个字符放宽到 15 个字符 |
| 2026-07-28 00:04:27 | `/req-generate` | 生成 requirement.md，状态更新为 draft |
| 2026-07-28 00:06:52 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype/web；写入 admin-list/admin-modal 横切 AC，状态更新为 pending_review |
| 2026-07-28 00:13:39 | `/req-review --approve` | 需求评审通过，状态更新为 approved，准备迁移 plan → review |
| 2026-07-28 00:20:23 | `/req-opsx` | 创建 OpenSpec Change `update-category-name-max-length-15`，状态 proposed |
| 2026-07-28 00:24:49 | `/sprint-propose` | 纳入 `sprint-013` 正式范围，关联 Change 可进入 apply 门禁 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
