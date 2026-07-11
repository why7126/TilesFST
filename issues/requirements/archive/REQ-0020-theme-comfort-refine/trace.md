---
requirement_id: REQ-0020-theme-comfort-refine
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-06-30 11:34:04
updated_at: 2026-07-11 20:14:49
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0020-theme-comfort-refine
requirement_name: theme-comfort-refine
requirement_type: Design System / Web 视觉舒适度
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期优先，覆盖登录页、瓷砖 SKU 列表、SKU 表单/弹窗、/design-system
  web_catalog: 品牌展示页允许保留暗色旗舰风；其他店主 Web 页面支持舒适主题
  wechat_miniapp: 待确认
related_requirements:
  - REQ-0000-build-design-system
related_changes:
  - update-theme-comfort-refine
lifecycle:
  captured: 2026-06-30 11:34:04
  generated: 2026-07-11 17:13:53
  completed: 2026-07-11 17:22:09
  reviewed: 2026-07-11 17:33:53
  approved: 2026-07-11 17:33:53
iteration: sprint-006
openspec_changes:
  - change_id: update-theme-comfort-refine
    type: update
    status: archived
    created_at: 2026-07-11 17:38:23
    path: openspec/changes/update-theme-comfort-refine
readiness: Ready
readiness_notes: 已评审通过；已创建 OpenSpec Change update-theme-comfort-refine，后续纳入 Sprint 后方可开发。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - prototype/web/theme-comfort-context.md
  - prototype/web/theme-comfort-matrix.html
  - review.md
expected_openspec_change: update-theme-comfort-refine
theme_decisions:
  modes:
    - system
    - dark_flagship
    - comfort_dark
    - light
  preference_persistence:
    - local
    - account_level
  first_acceptance_matrix:
    - admin_login
    - admin_tile_sku_list
    - admin_tile_sku_form
    - admin_tile_sku_modal
    - design_system
    - web_catalog_comfort_theme
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-form-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-005-retrospective.md
cross_cutting_tags:
  - admin-list
  - admin-form
  - admin-modal
  - media-upload
knowledge_base_gate: Pass
readiness_report:
  readiness: Ready
  knowledge_base_gate: Pass
  added_ac_xcut: 14
  notes: Sprint-005 复盘提示管理端列表 DOM 漂移仍需默认复用 AdminListPage / MetricCard / pagination-window；本 REQ 已将瓷砖 SKU 列表、表单、弹窗与媒体上传状态纳入主题验收矩阵。
```

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-07-11 20:14:40 | lifecycle-stage-migrate | review → archive（/sprint-archive sprint-006） |
| 2026-07-11 20:10:10 | /opsx-archive | Change `update-theme-comfort-refine` 已归档，状态同步完成。 |
| 2026-07-11 18:53:48 | /opsx-apply | Change `update-theme-comfort-refine` apply 完成，待 archive。 |
| 2026-07-11 17:38:23 | `/req-opsx` | 基于 approved 需求创建 OpenSpec Change：update-theme-comfort-refine |
| 2026-07-11 17:34:28 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-11 17:33:53 | `/req-review --approve` | 评审通过；状态更新为 approved，准备迁入 review 阶段 |
| 2026-07-11 17:22:09 | `/req-complete` | 补齐 user-stories、business-flow、acceptance、prototype；写入知识库横切 AC，状态进入 pending_review |
| 2026-07-11 17:13:53 | `/req-generate` | 生成 PRD：明确管理端新增主题切换、品牌展示页可保留暗色旗舰风，舒适度验收覆盖登录页、列表页、表单页、弹窗和 `/design-system` |
| 2026-06-30 11:34:04 | `/capture` | 记录用户反馈主题色太深、长时间观看眼睛疲劳的视觉舒适度优化需求 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0064-theme-selector-sidebar-placement | medium | done | fix-theme-selector-sidebar-placement | 界面主题选择器未放在侧边栏用户头像上方 |
