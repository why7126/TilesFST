---
requirement_id: REQ-0082-admin-category-name-special-characters
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-30 22:08:31
updated_at: 2026-07-31 00:05:27
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0082-admin-category-name-special-characters
requirement_name: admin-category-name-special-characters
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
  - REQ-0077-category-name-max-length-15
related_changes:
  - update-admin-category-name-special-characters
lifecycle:
  captured: 2026-07-30 22:08:31
  generated: 2026-07-30 22:11:25
  completed: 2026-07-30 22:14:37
  reviewed: 2026-07-30 22:18:32
  approved: 2026-07-30 22:18:32
iteration: sprint-014
openspec_changes:
  - change_id: update-admin-category-name-special-characters
    type: update
    status: archived
readiness: Ready
readiness_notes: 五件套已补齐，UI 原型策略已提供；后续可进入 /req-review。特殊字符策略按“允许常见可见业务符号、禁止控制字符”收敛，最终实现需在 OpenSpec Change 中同步前后端校验、OpenAPI / Orval、测试与展示回归。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - prototype/web/prototype-context.md
  - prototype/web/admin-category-name-special-characters.html
  - review.md
expected_openspec_change: update-admin-category-name-special-characters
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/retrospectives/sprint-013-retrospective.md
cross_cutting_tags:
  - admin-list
  - admin-modal
  - admin-category
  - validation
knowledge_base_summary: req-complete 命中 admin-list 与 admin-modal；已将列表分页/fixed toast/DS confirm/无 window.confirm 以及弹窗 className/computed width/矮视口滚动转化为 7 条 AC-XCUT。Sprint-013 复盘提示管理端 UI 问题重复出现，后续 apply 前需前置列表与弹窗验收模板。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 00:03:07 | lifecycle-stage-migrate | review → archive（/opsx-archive update-admin-category-name-special-characters） |
| 2026-07-31 00:02:28 | /opsx-archive | Change `update-admin-category-name-special-characters` 已归档，状态同步完成。 |
| 2026-07-30 23:20:55 | /opsx-modify | Change `update-admin-category-name-special-characters` 验收返修已同步，待复验或 archive。 |
| 2026-07-30 23:10:34 | /opsx-apply | Change `update-admin-category-name-special-characters` apply 完成，待 archive。 |
| 2026-07-30 22:55:04 | `/sprint-propose` | 纳入 `sprint-014` 正式范围，关联 Change 可进入 apply 门禁 |
| 2026-07-30 22:21:01 | `/req-opsx` | 创建 OpenSpec Change `update-admin-category-name-special-characters`，状态 proposed |
| 2026-07-30 22:19:02 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-30 22:18:32 | `/req-review --approve` | 需求评审通过，状态更新为 approved，准备迁移 plan → review |
| 2026-07-30 22:14:37 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype/web；写入 admin-list/admin-modal 横切 AC，状态更新为 pending_review |
| 2026-07-30 22:11:25 | `/req-generate` | 生成 requirement.md，状态更新为 draft |
| 2026-07-30 22:08:31 | `/capture` | 记录管理后台瓷砖类目名称命名规则放宽为允许特殊字符，最多 15 个字符不变 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-07-31 00:02:28 workflow-sync：状态同步为 done（Change archived）
