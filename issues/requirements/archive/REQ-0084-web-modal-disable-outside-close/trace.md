---
requirement_id: REQ-0084-web-modal-disable-outside-close
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-30 22:53:04
updated_at: 2026-07-31 00:06:42
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0084-web-modal-disable-outside-close
requirement_name: web-modal-disable-outside-close
requirement_type: Web / 弹窗交互策略
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 本期
  wechat_miniapp: 不涉及
related_requirements: []
related_changes:
  - update-web-modal-disable-outside-close
lifecycle:
  captured: 2026-07-30 22:53:04
  generated: 2026-07-30 23:03:32
  completed: 2026-07-30 23:09:16
  reviewed: 2026-07-30 23:18:07
  approved: 2026-07-30 23:18:07
iteration: sprint-014
openspec_changes:
  - change_id: update-web-modal-disable-outside-close
    type: update
    status: archived
readiness: Ready
readiness_notes: 五件套已补齐，UI 类 prototype 策略已提供，admin-modal 与 media-upload 横切 AC 已写入 acceptance.md，待 /req-review 评审。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - prototype/web/context.md
  - prototype/web/modal-disable-outside-close.html
  - review.md
expected_openspec_change: update-web-modal-disable-outside-close
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-013-retrospective.md
cross_cutting_tags:
  - admin-modal
  - media-upload
  - web
  - modal
  - interaction
knowledge_base_gate: Pass
prototype:
  web:
    context: prototype/web/context.md
    html: prototype/web/modal-disable-outside-close.html
    png: 待后续设计或 OpenSpec 阶段按实际组件截图导出
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 00:06:42 | lifecycle-stage-migrate | review → archive（/opsx-archive update-web-modal-disable-outside-close） |
| 2026-07-31 00:06:08 | /opsx-archive | Change `update-web-modal-disable-outside-close` 已归档，状态同步完成。 |
| 2026-07-30 23:50:27 | /opsx-apply | Change `update-web-modal-disable-outside-close` apply 完成，待 archive。 |
| 2026-07-30 23:18:48 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-30 22:53:04 | `/capture` | 记录 Web 端所有弹窗取消点击空白区域自动关闭的交互需求。 |
| 2026-07-30 23:03:32 | `/req-generate` | 生成 requirement.md 草案，状态更新为 draft。 |
| 2026-07-30 23:09:16 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 Web prototype；引用 admin-modal、media-upload 最佳实践和 sprint-013 复盘，状态更新为 pending_review。 |
| 2026-07-30 23:18:07 | `/req-review --approve` | 需求评审通过，状态更新为 approved，准备迁移至 review 阶段。 |
| 2026-07-30 23:25:55 | `/req-opsx` | 创建 OpenSpec Change `update-web-modal-disable-outside-close`，状态为 proposed。 |
| 2026-07-30 23:29:57 | `/req-opsx` | 修正未纳入 Sprint 的 REQ 状态保持 approved；change proposed 追溯不变。 |
| 2026-07-30 23:33:30 | `/sprint-propose sprint-014` | 纳入 Sprint 014 正式范围，状态更新为 in_sprint。 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-07-31 00:05:27 workflow-sync：状态同步为 done（Change archived）
