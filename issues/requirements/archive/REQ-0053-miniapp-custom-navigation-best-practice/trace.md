---
requirement_id: REQ-0053-miniapp-custom-navigation-best-practice
status: done
priority: P1
created_at: 2026-07-19 17:28:06
updated_at: 2026-07-19 21:06:24
lifecycle:
  captured: 2026-07-19 17:28:06
  generated: 2026-07-19 18:09:25
  completed: 2026-07-19 18:41:33
  reviewed: 2026-07-19 18:54:24
  approved: 2026-07-19 18:54:24
iteration: sprint-009
openspec_changes:
  - change_id: add-miniapp-custom-navigation-best-practice
    type: add
    status: archived
related_requirements:
  - REQ-0048-miniapp-global-custom-navigation-bar
  - REQ-0052-miniapp-device-evidence-template
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
cross_cutting_tags: []
lifecycle_stage: archive
readiness: Ready
---

# Trace

```yaml
requirement_id: REQ-0053-miniapp-custom-navigation-best-practice
status: done
priority: P1
created_at: 2026-07-19 17:28:06
updated_at: 2026-07-19 21:06:24
lifecycle:
  captured: 2026-07-19 17:28:06
  generated: 2026-07-19 18:09:25
  completed: 2026-07-19 18:41:33
  reviewed: 2026-07-19 18:54:24
  approved: 2026-07-19 18:54:24
iteration: sprint-009
openspec_changes:
  - change_id: add-miniapp-custom-navigation-best-practice
    type: add
    status: archived
related_requirements:
  - REQ-0048-miniapp-global-custom-navigation-bar
  - REQ-0052-miniapp-device-evidence-template
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
cross_cutting_tags: []
lifecycle_stage: archive
readiness: Ready
```

## 关联需求

| REQ | 关系 | 说明 |
|---|---|---|
| REQ-0048-miniapp-global-custom-navigation-bar | parent | 既有小程序全局自定义导航栏能力沉淀，本文档化其跨页面实现经验与防回归规则 |
| REQ-0052-miniapp-device-evidence-template | related | 截图验收矩阵和真机/DevTools evidence 字段可复用该模板沉淀 |

## Knowledge-base Cross-cutting

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| 无匹配标签 | 本 REQ 为微信小程序导航 best-practice 与验收矩阵治理，不命中管理端列表、表单、弹窗或媒体上传横切标签 | 0 |

最近复盘参考：`docs/knowledge-base/retrospectives/sprint-008-retrospective.md`。与本 REQ 相关的复发预防点为小程序自定义导航建立独立 best-practice，统一状态栏、胶囊避让、返回兜底、页面 offset 和 320/375/430 pt 设备验收矩阵，避免自动化通过被误写成真实设备验收完成。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 21:05:31 | lifecycle-stage-migrate | review → archive（/opsx-archive add-miniapp-custom-navigation-best-practice） |
| 2026-07-19 21:04:33 | /opsx-archive | Change `add-miniapp-custom-navigation-best-practice` 已归档，状态同步完成。 |
| 2026-07-19 21:00:32 | /opsx-apply | Change `add-miniapp-custom-navigation-best-practice` apply 完成，待 archive。 |
| 2026-07-19 19:43:26 | /req-opsx | 创建 OpenSpec Change `add-miniapp-custom-navigation-best-practice`，状态 proposed |
| 2026-07-19 19:22:27 | /sprint-propose sprint-009 | 纳入 sprint-009 正式范围，状态更新为 in_sprint；后续先 /req-opsx |
| 2026-07-19 18:58:03 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-19 18:54:24 | /req-review --approve | 需求评审通过，状态进入 approved，后续可 /req-opsx 或纳入 Sprint |
| 2026-07-19 18:41:33 | /req-complete | 补齐 user-stories、business-flow、acceptance 与 miniapp prototype；Knowledge-base gate 为 N/A；引用 sprint-008 复盘的小程序设备验收与导航 offset 复发模式，状态进入 pending_review |
| 2026-07-19 18:09:25 | /req-generate | 生成 requirement.md，状态进入 draft；明确小程序自定义导航 best-practice 的沉淀范围、状态栏/胶囊/返回/offset 规则和截图验收矩阵 |
| 2026-07-19 17:28:06 | /req-capture | 捕获需求：为小程序自定义导航沉淀 best-practice，明确状态栏、胶囊、返回兜底、页面 offset 和截图验收矩阵 |

- 2026-07-19 21:04:33 workflow-sync：状态同步为 done（Change archived）
