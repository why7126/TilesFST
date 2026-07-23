---
bug_id: BUG-0077-miniapp-category-secondary-name-truncated
status: done
lifecycle_stage: archive
severity: medium
created_at: 2026-07-21 10:25:27
updated_at: 2026-07-22 09:20:43
lifecycle:
  captured: 2026-07-21 10:25:27
  generated: 2026-07-21 14:40:50
  completed: 2026-07-21 14:56:34
  reviewed: 2026-07-21 15:00:29
  approved: 2026-07-21 15:00:29
iteration: sprint-010
related_requirement: REQ-0045-category-list-page
related_bug: null
related_change: fix-miniapp-category-secondary-name-truncated
source_command: /capture
captured_via: capture
classification_rationale: 项目已有微信小程序分类页与二级分类展示能力，二级分类名称超过 4 个字时被省略为省略号属于既有页面展示行为偏差，倾向记录为 BUG。
openspec_changes:
  - change_id: fix-miniapp-category-secondary-name-truncated
    type: fix
    status: archived
related_bugs: []
---

```yaml
bug_id: BUG-0077-miniapp-category-secondary-name-truncated
status: done
severity: medium
lifecycle_stage: review
created_at: 2026-07-21 10:25:27
updated_at: 2026-07-21 15:34:31
lifecycle:
  captured: 2026-07-21 10:25:27
  generated: 2026-07-21 14:40:50
  completed: 2026-07-21 14:56:34
  reviewed: 2026-07-21 15:00:29
  approved: 2026-07-21 15:00:29
iteration: sprint-010
related_requirement: REQ-0045-category-list-page
related_bug: null
related_change: fix-miniapp-category-secondary-name-truncated
source_command: /capture
captured_via: capture
classification_rationale: 项目已有微信小程序分类页与二级分类展示能力，二级分类名称超过 4 个字时被省略为省略号属于既有页面展示行为偏差，倾向记录为 BUG。
openspec_changes:
  - change_id: fix-miniapp-category-secondary-name-truncated
    type: fix
    status: archived
related_bugs: []
scope:
  terminal: miniapp
  page: category
  module: secondary_category
  issue_type: text_truncation
readiness:
  capture: done
  bug: done
  root_cause: done
  workaround: done
  acceptance: done
  review: done
  trace: done
  next: opsx-apply
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| 用户反馈 | `/capture` | 微信小程序分类页二级分类名称超过 4 个字时被省略为 `...` |
| 关联需求 | `REQ-0045-category-list-page` | 分类列表页能力已交付，当前为展示体验偏差 |

## 建议复现要点

| 要点 | 说明 |
|---|---|
| 页面路径 | 确认发生在分类页的二级分类列表、横向导航、筛选入口或其他分类展示区域 |
| 分类样例 | 记录至少 2 个超过 4 个字的二级分类名称，并确认 4 字以内名称是否正常 |
| 设备环境 | 覆盖微信开发者工具、iOS 真机、Android 真机和不同屏幕宽度 |
| 展示规则 | 检查是否由 `text-overflow: ellipsis`、固定宽度、单行限制或组件布局导致 |
| 交互入口 | 确认省略后是否仍可点击进入正确商品列表，避免展示修复引入入口错乱 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 名称可辨识 | 超过 4 个字的二级分类名称在分类页可被用户正常识别 |
| 布局稳定 | 长名称展示不遮挡相邻分类、商品列表、导航栏或页面操作区 |
| 多端适配 | 微信开发者工具、iOS 真机、Android 真机和窄屏设备展示一致可用 |
| 入口正确 | 点击长名称二级分类仍进入对应分类商品列表 |
| 回归覆盖 | 4 字以内、5-8 字、超过 8 字分类名称均有回归验证 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 09:15:15 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-category-secondary-name-truncated） |
| 2026-07-22 09:14:53 | /opsx-archive | Change `fix-miniapp-category-secondary-name-truncated` 已归档，状态同步完成。 |
| 2026-07-21 10:25:27 | /capture | 记录微信小程序分类页二级分类长名称省略缺陷 |
| 2026-07-21 14:40:50 | /bug-generate | 生成缺陷详情 bug.md，状态推进为 draft |
| 2026-07-21 14:56:34 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review |
| 2026-07-21 15:00:29 | /bug-review --approve | 评审通过，状态推进为 approved |
| 2026-07-21 15:01:32 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-21 15:08:00 | /bug-opsx | 创建 OpenSpec Change `fix-miniapp-category-secondary-name-truncated` |
| 2026-07-21 15:28:09 | /sprint-propose sprint-010 | 纳入 sprint-010 正式范围，状态推进为 in_sprint |

- 2026-07-22 09:14:53 workflow-sync：状态同步为 done（Change archived）
