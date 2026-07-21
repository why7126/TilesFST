---
bug_id: BUG-0068-miniapp-home-device-acceptance-followup
status: done
lifecycle_stage: archive
severity: high
created_at: 2026-07-19 17:27:51
updated_at: 2026-07-19 21:40:59
lifecycle:
  captured: 2026-07-19 17:27:51
  generated: 2026-07-19 17:35:07
  completed: 2026-07-19 17:36:58
  reviewed: 2026-07-19 17:41:40
  approved: 2026-07-19 17:41:40
iteration: sprint-009
related_requirement: REQ-0041-miniapp-home
related_bug: BUG-0065-miniapp-home-preview-deviation
related_change: null
source_sprint: sprint-008
source_command: /bug-capture
openspec_changes:
  - change_id: fix-miniapp-home-device-acceptance
    type: fix
    status: archived
related_bugs: []
captured_via: bug-capture
classification_rationale: Sprint 008 已交付能力仍存在微信开发者工具/真机验收残留，影响首页预览、适配和避让验收闭环，属于已交付能力的验收缺陷 follow-up。
---

```yaml
bug_id: BUG-0068-miniapp-home-device-acceptance-followup
status: done
severity: high
lifecycle_stage: review
created_at: 2026-07-19 17:27:51
updated_at: 2026-07-19 18:14:29
lifecycle:
  captured: 2026-07-19 17:27:51
  generated: 2026-07-19 17:35:07
  completed: 2026-07-19 17:36:58
  reviewed: 2026-07-19 17:41:40
  approved: 2026-07-19 17:41:40
iteration: sprint-009
related_requirement: REQ-0041-miniapp-home
related_bug: BUG-0065-miniapp-home-preview-deviation
related_change: null
source_sprint: sprint-008
source_command: /bug-capture
openspec_changes:
  - change_id: fix-miniapp-home-device-acceptance
    type: fix
    status: archived
related_bugs: []
scope:
  terminal: wechat_miniapp
  page: home
  acceptance_gap:
    - 微信开发者工具真实首页预览
    - 真机或等效设备验收
    - 320-430 pt 逻辑宽度
    - 微信原生胶囊避让
    - fixed header 与底部 TabBar 内容不遮挡
readiness:
  capture: done
  bug: in_sprint
  root_cause: done
  workaround: done
  acceptance: done
  review: done
  trace: done
  next: /bug-opsx BUG-0068-miniapp-home-device-acceptance-followup
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| Sprint | `sprint-008` | 强制关闭时保留小程序首页 DevTools / 真机验收人工 follow-up 风险 |
| REQ | `REQ-0041-miniapp-home` | 微信小程序首页原始需求与 320-430 pt 首页验收要求 |
| BUG | `BUG-0065-miniapp-home-preview-deviation` | 首页运行入口修复已归档，但 trace 记录仍需人工预览与视口验收 |
| 文档 | `iterations/archive/sprint-008/acceptance-report.md` | 验收报告明确不得把自动化与静态检查表述为真实设备验收已完成 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 首页真实预览 | 微信开发者工具打开 `pages/index/index` 后，品牌导航、搜索、Banner、快捷入口和推荐模块正常展示 |
| 320-430 pt | 320、375、390、430 pt 及区间内常见宽度没有横向滚动、不可读文本或卡片挤压 |
| 胶囊避让 | 自定义导航栏不进入微信原生分享 / 关闭胶囊区域，不手绘模拟胶囊 |
| 内容不遮挡 | fixed header、状态栏、底部 TabBar 和安全区不会遮挡首页关键内容或点击目标 |
| evidence | 补充 DevTools / 真机截图或验收记录，明确设备、宽度、时间和结论 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 21:40:27 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-home-device-acceptance） |
| 2026-07-19 21:38:23 | /opsx-archive | Change `fix-miniapp-home-device-acceptance` 已归档，状态同步完成。 |
| 2026-07-19 21:17:08 | /opsx-apply | Change `fix-miniapp-home-device-acceptance` apply 完成，待 archive。 |
| 2026-07-19 18:14:29 | /bug-opsx | 创建 OpenSpec Change `fix-miniapp-home-device-acceptance`，状态 proposed |
| 2026-07-19 17:45:33 | /sprint-propose | 纳入 sprint-009 正式范围，容量估算更新为 11.0/30.0 人天 |
| 2026-07-19 17:42:30 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-19 17:41:40 | /bug-review --approve | 评审通过，状态更新为 approved，准备迁入 review 阶段 |
| 2026-07-19 17:36:58 | /bug-complete | 补齐 root-cause、workaround、acceptance；状态更新为 pending_review |
| 2026-07-19 17:35:07 | /bug-generate | 生成 bug.md，状态更新为 draft |
| 2026-07-19 17:27:51 | /bug-capture | 为 Sprint 008 遗留的小程序首页 DevTools / 真机验收建立 follow-up BUG |

- 2026-07-19 21:38:23 workflow-sync：状态同步为 done（Change archived）
