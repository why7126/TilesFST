---
requirement_id: REQ-0052-miniapp-device-evidence-template
status: done
priority: P1
created_at: 2026-07-19 17:02:14
updated_at: 2026-07-19 19:06:06
lifecycle:
  captured: 2026-07-19 17:02:14
  generated: 2026-07-19 17:05:33
  completed: 2026-07-19 17:08:59
  reviewed: 2026-07-19 17:15:21
  approved: 2026-07-19 17:15:21
iteration: sprint-009
openspec_changes:
  - change_id: add-miniapp-device-evidence-template
    type: add
    status: archived
related_requirements:
  - REQ-0039-xl-admin-page-layered-acceptance-template
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
cross_cutting_tags: []
lifecycle_stage: archive
---

# Trace

```yaml
requirement_id: REQ-0052-miniapp-device-evidence-template
status: done
priority: P1
created_at: 2026-07-19 17:02:14
updated_at: 2026-07-19 19:06:06
lifecycle:
  captured: 2026-07-19 17:02:14
  generated: 2026-07-19 17:05:33
  completed: 2026-07-19 17:08:59
  reviewed: 2026-07-19 17:15:21
  approved: 2026-07-19 17:15:21
iteration: sprint-009
openspec_changes:
  - change_id: add-miniapp-device-evidence-template
    type: add
    status: archived
related_requirements:
  - REQ-0039-xl-admin-page-layered-acceptance-template
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
cross_cutting_tags: []
lifecycle_stage: archive
```

## 关联需求

| REQ | 关系 | 说明 |
|---|---|---|
| REQ-0039-xl-admin-page-layered-acceptance-template | related | 既有 XL 管理端分层验收模板可作为 evidence 字段、N/A 判定和证据摘要规则参考；本需求面向小程序 DevTools/真机验收单独收敛 |

## Knowledge-base Cross-cutting

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| 无匹配标签 | 本 REQ 为微信小程序设备验收治理模板，不命中管理端列表、表单、弹窗或媒体上传横切标签 | 0 |

最近复盘参考：`docs/knowledge-base/retrospectives/sprint-008-retrospective.md`。与本 REQ 相关的复发预防点为小程序设备验收建立独立 Gate，区分自动化覆盖、DevTools 预览、真机验收与人工 follow-up，避免设备验收散落在 tasks、acceptance、trace 与 Sprint 验收报告中。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 19:05:32 | lifecycle-stage-migrate | review → archive（/opsx-archive add-miniapp-device-evidence-template） |
| 2026-07-19 19:04:22 | /opsx-archive | Change `add-miniapp-device-evidence-template` 已归档，状态同步完成。 |
| 2026-07-19 18:48:23 | /opsx-apply | Change `add-miniapp-device-evidence-template` apply 完成，待 archive。 |
| 2026-07-19 18:11:18 | /req-opsx | 创建 OpenSpec Change `add-miniapp-device-evidence-template`，状态为 proposed |
| 2026-07-19 17:18:31 | /sprint-propose | 纳入 sprint-009，状态进入 in_sprint；后续先 /req-opsx |
| 2026-07-19 17:16:02 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-19 17:15:21 | /req-review --approve | 需求评审通过，状态进入 approved，后续可 /req-opsx 或纳入 Sprint |
| 2026-07-19 17:08:59 | /req-complete | 补齐 user-stories、business-flow 与 acceptance；Knowledge-base gate 为 N/A；引用 sprint-008 复盘设备验收残留经验，状态进入 pending_review |
| 2026-07-19 17:05:33 | /req-generate | 生成 requirement.md，状态进入 draft；明确小程序 DevTools/真机 evidence 模板的范围、字段和证据边界 |
| 2026-07-19 17:02:14 | /req-capture | 捕获需求：为小程序 DevTools/真机验收建立可复用 evidence 模板 |

- 2026-07-19 19:04:22 workflow-sync：状态同步为 done（Change archived）
