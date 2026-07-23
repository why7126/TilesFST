---
bug_id: BUG-0070-miniapp-sku-detail-duplicate-brand-button
status: done
lifecycle_stage: archive
severity: medium
created_at: 2026-07-21 08:10:00
updated_at: 2026-07-22 08:35:35
lifecycle:
  captured: 2026-07-21 08:10:00
  generated: 2026-07-21 08:13:57
  completed: 2026-07-21 08:16:46
  reviewed: 2026-07-21 08:23:38
  approved: 2026-07-21 08:23:38
iteration: sprint-010
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: null
related_change: fix-miniapp-sku-detail-duplicate-brand-button
source_command: /bug-capture
openspec_changes:
  - change_id: fix-miniapp-sku-detail-duplicate-brand-button
    type: fix
    status: archived
related_bugs: []
---

```yaml
bug_id: BUG-0070-miniapp-sku-detail-duplicate-brand-button
status: done
severity: medium
lifecycle_stage: review
created_at: 2026-07-21 08:10:00
updated_at: 2026-07-21 09:15:27
lifecycle:
  captured: 2026-07-21 08:10:00
  generated: 2026-07-21 08:13:57
  completed: 2026-07-21 08:16:46
  reviewed: 2026-07-21 08:23:38
  approved: 2026-07-21 08:23:38
iteration: sprint-010
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: null
related_change: fix-miniapp-sku-detail-duplicate-brand-button
source_command: /bug-capture
openspec_changes:
  - change_id: fix-miniapp-sku-detail-duplicate-brand-button
    type: fix
    status: archived
related_bugs: []
scope:
  terminal: wechat_miniapp
  page: sku_detail
  component: bottom_action_bar
  issue_type: duplicate_entry
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
| 用户反馈 | `/bug-capture` | 小程序商品详情页底部品牌按钮与内容区“查看品牌主页”入口重复，要求删除底部品牌按钮 |
| REQ | `REQ-0044-miniapp-sku-detail-page` | 微信小程序 SKU 商品详情页已交付能力 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 底部按钮 | SKU 商品详情页底部操作区不再显示品牌按钮 |
| 内容入口 | 内容区“查看品牌主页”入口保留，点击后仍能进入正确品牌主页 |
| 操作区布局 | 删除按钮后底部操作区布局稳定，无空白、错位或点击热区残留 |
| 回归范围 | 商品详情页核心浏览、分享、咨询或其他底部操作入口不受影响 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 08:30:54 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-sku-detail-duplicate-brand-button） |
| 2026-07-22 08:30:37 | /opsx-archive | Change `fix-miniapp-sku-detail-duplicate-brand-button` 已归档，状态同步完成。 |
| 2026-07-21 22:55:54 | /opsx-apply | Change `fix-miniapp-sku-detail-duplicate-brand-button` apply 完成，待 archive。 |
| 2026-07-21 09:15:27 | /sprint-propose | 纳入 sprint-010 正式范围，关联 Change `fix-miniapp-sku-detail-duplicate-brand-button` |
| 2026-07-21 08:35:43 | /bug-opsx | 创建 OpenSpec Change `fix-miniapp-sku-detail-duplicate-brand-button`，状态 proposed |
| 2026-07-21 08:24:14 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-21 08:23:38 | /bug-review --approve | 评审通过，状态更新为 approved，准备由 plan 迁入 review 阶段 |
| 2026-07-21 08:16:46 | /bug-complete | 补齐 root-cause、workaround、acceptance；状态更新为 pending_review |
| 2026-07-21 08:13:57 | /bug-generate | 生成 bug.md，状态更新为 draft |
| 2026-07-21 08:10:00 | /bug-capture | 记录小程序商品详情页底部品牌按钮与内容区查看品牌主页入口重复缺陷 |

- 2026-07-22 08:30:37 workflow-sync：状态同步为 done（Change archived）
