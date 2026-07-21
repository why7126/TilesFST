---
bug_id: BUG-0070-miniapp-sku-detail-duplicate-brand-button
status: draft
lifecycle_stage: plan
severity: medium
created_at: 2026-07-21 08:10:00
updated_at: 2026-07-21 08:13:57
lifecycle:
  captured: 2026-07-21 08:10:00
  generated: 2026-07-21 08:13:57
iteration: null
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: null
related_change: null
source_command: /bug-capture
openspec_changes: []
related_bugs: []
---

```yaml
bug_id: BUG-0070-miniapp-sku-detail-duplicate-brand-button
status: draft
severity: medium
lifecycle_stage: plan
created_at: 2026-07-21 08:10:00
updated_at: 2026-07-21 08:13:57
lifecycle:
  captured: 2026-07-21 08:10:00
  generated: 2026-07-21 08:13:57
iteration: null
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: null
related_change: null
source_command: /bug-capture
openspec_changes: []
related_bugs: []
scope:
  terminal: wechat_miniapp
  page: sku_detail
  component: bottom_action_bar
  issue_type: duplicate_entry
readiness:
  capture: done
  bug: done
  root_cause: todo
  workaround: todo
  acceptance: todo
  review: todo
  trace: done
  next: bug-complete
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
| 2026-07-21 08:13:57 | /bug-generate | 生成 bug.md，状态更新为 draft |
| 2026-07-21 08:10:00 | /bug-capture | 记录小程序商品详情页底部品牌按钮与内容区查看品牌主页入口重复缺陷 |
