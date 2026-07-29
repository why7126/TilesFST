---
bug_id: BUG-0086-miniapp-sku-detail-remark-not-shown
status: done
severity: medium
created_at: 2026-07-28 22:24:26
updated_at: 2026-07-29 07:55:20
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-28 22:24:26
  generated: 2026-07-28 22:29:49
  completed: 2026-07-28 22:33:20
  reviewed: 2026-07-28 22:36:32
  approved: 2026-07-28 22:36:32
iteration: sprint-013
openspec_changes:
  - change_id: fix-miniapp-sku-detail-remark-display
    type: fix
    status: archived
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: null
---

# BUG Trace

```yaml
bug_id: BUG-0086-miniapp-sku-detail-remark-not-shown
status: done
severity: medium
created_at: 2026-07-28 22:24:26
updated_at: 2026-07-29 00:09:26
lifecycle_stage: review
lifecycle:
  captured: 2026-07-28 22:24:26
  generated: 2026-07-28 22:29:49
  completed: 2026-07-28 22:33:20
  reviewed: 2026-07-28 22:36:32
  approved: 2026-07-28 22:36:32
iteration: sprint-013
openspec_changes:
  - change_id: fix-miniapp-sku-detail-remark-display
    type: fix
    status: archived
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-29 07:55:10 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-sku-detail-remark-display） |
| 2026-07-29 07:54:54 | /opsx-archive | Change `fix-miniapp-sku-detail-remark-display` 已归档，状态同步完成。 |
| 2026-07-29 00:09:26 | /opsx-apply | 后端备注透传、小程序详情页归一化展示及自动化测试已完成；待补充 DevTools/真机预览证据后可关闭剩余验收。 |
| 2026-07-28 23:04:49 | /opsx-apply | Change `fix-miniapp-sku-detail-remark-display` apply 进行中，待补齐剩余验收。 |
| 2026-07-28 22:51:35 | /sprint-propose | 纳入 `sprint-013` 正式范围，关联 Change `fix-miniapp-sku-detail-remark-display`。 |
| 2026-07-28 22:44:51 | /bug-opsx | 创建 OpenSpec Change `fix-miniapp-sku-detail-remark-display`，状态 proposed。 |
| 2026-07-28 22:37:18 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-28 22:36:32 | /bug-review --approve | 评审通过，确认进入修复流程。 |
| 2026-07-28 22:33:20 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review。 |
| 2026-07-28 22:29:49 | /bug-generate | 生成 bug.md，状态推进为 draft。 |
| 2026-07-28 22:24:26 | /capture | 记录小程序商品详情页备注说明信息没有显示问题，分类为 BUG。 |

- 2026-07-29 07:54:54 workflow-sync：状态同步为 done（Change archived）
