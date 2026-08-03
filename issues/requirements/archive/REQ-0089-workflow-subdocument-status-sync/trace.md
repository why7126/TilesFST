---
requirement_id: REQ-0089-workflow-subdocument-status-sync
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-01 09:40:07
updated_at: 2026-08-01 11:56:22
lifecycle:
  captured: 2026-08-01 09:40:07
  generated: 2026-08-01 09:49:17
  completed: 2026-08-01 09:52:35
  reviewed: 2026-08-01 09:55:21
  approved: 2026-08-01 09:55:21
iteration: sprint-017
openspec_changes:
  - change_id: improve-workflow-subdocument-status-sync
    type: update
    status: archived
related_requirements: []
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0089-workflow-subdocument-status-sync
requirement_name: workflow-subdocument-status-sync
requirement_type: 流程治理 / Workflow Sync / 文档一致性
priority: P1
status: done
owner: product
source: /opsx-explore
target_clients:
  web_admin: 不直接影响运行时；会影响管理端相关 REQ/BUG 文档闭环质量
  web_catalog: 不直接影响运行时；会影响店主端相关 REQ/BUG 文档闭环质量
  wechat_miniapp: 不直接影响运行时；会影响小程序相关 REQ/BUG 文档闭环质量
related_requirements: []
related_changes:
  - improve-workflow-subdocument-status-sync
lifecycle:
  captured: 2026-08-01 09:40:07
  generated: 2026-08-01 09:49:17
  completed: 2026-08-01 09:52:35
  reviewed: 2026-08-01 09:55:21
  approved: 2026-08-01 09:55:21
iteration: sprint-017
openspec_changes:
  - change_id: improve-workflow-subdocument-status-sync
    type: update
    status: archived
readiness: Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance 与 trace；本 REQ 为流程治理 / Workflow Sync / 文档一致性需求，不涉及管理端列表、表单、弹窗或媒体上传 UI 场景，Knowledge-base UI 横切 AC 判定为 N/A。已引用 sprint-016 复盘中关于归档证据缺口、中间态文案残留和 close stale scan 的经验。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
expected_openspec_change: improve-workflow-subdocument-status-sync
knowledge_base_refs:
  - docs/knowledge-base/README.md
  - docs/knowledge-base/retrospectives/sprint-016-retrospective.md
cross_cutting_tags:
  - workflow-sync
  - documentation-governance
  - issue-lifecycle
knowledge_base_summary: sprint-016 复盘显示 Sprint close 前曾出现 acceptance-report 与 release-note 中间态文案残留，且已归档 Change 缺 trace 会阻断 close；本 REQ 将子文档 drift check、验收结果回填、归档证据前移和 close stale scan 纳入验收。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-01 11:46:37 | lifecycle-stage-migrate | review → archive（/opsx-archive improve-workflow-subdocument-status-sync） |
| 2026-08-01 11:45:50 | /opsx-archive | Change `improve-workflow-subdocument-status-sync` 已归档，状态同步完成。 |
| 2026-08-01 11:21:35 | /opsx-apply | Change `improve-workflow-subdocument-status-sync` apply 完成，待 archive。 |
| 2026-08-01 10:34:08 | /sprint-propose sprint-017 | 纳入 Sprint 017 正式范围，关联 Change `improve-workflow-subdocument-status-sync`。 |
| 2026-08-01 10:00:07 | /req-opsx | 创建 OpenSpec Change `improve-workflow-subdocument-status-sync`，类型 update，修改能力 `agent-workflow-tooling`。 |
| 2026-08-01 09:55:59 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-08-01 09:55:21 | /req-review --approve | 评审通过，状态更新为 approved，准备迁入 review 阶段。 |
| 2026-08-01 09:52:35 | /req-complete | 补齐 user-stories、business-flow、acceptance；Knowledge-base gate 判定为 N/A，引用 sprint-016 复盘中的归档证据与中间态文案残留经验，状态更新为 pending_review。 |
| 2026-08-01 09:49:17 | /req-generate | 生成 requirement.md，状态更新为 draft。 |
| 2026-08-01 09:40:07 | /req-capture | 记录 REQ/BUG 子文档状态同步与验收结果回填治理需求。 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-08-01 11:45:50 workflow-sync：状态同步为 done（Change archived）
