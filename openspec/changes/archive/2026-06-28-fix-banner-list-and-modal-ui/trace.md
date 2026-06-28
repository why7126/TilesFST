---
created_at: 2026-06-28 17:46:46
updated_at: 2026-06-28 18:57:34
sprint: sprint-003
change_id: fix-banner-list-and-modal-ui
type: fix
status: archived
related_bug:
  - BUG-0039-banner-list-display-position-column
  - BUG-0040-banner-modal-width-too-narrow
related_requirement: REQ-0016-banner-management
---

# Change 追溯

## PNG / 验收 Checklist

| # | 项 | 参考 | 实现 | 状态 |
|---|-----|------|------|------|
| 1 | 列表第一列仅标题 | BUG-0039 AC-001 | `BannerManagementPage.tsx` | ✓ |
| 2 | 独立「展示位置」列 | BUG-0039 AC-002 | 表头 + `.banner-position` | ✓ |
| 3 | colSpan 9 | BUG-0039 AC-004 | loading/empty rows | ✓ |
| 4 | Banner 弹窗 880px | BUG-0040 AC-001 | `banner-management.css` | ✓ |
| 5 | 与 SKU 弹窗宽度一致 | BUG-0040 AC-002 | 880px + border/shadow/head | ✓ |
| 6 | BUG-0033 滚动无回归 | BUG-0040 AC-003 | flex scroll 保留 | ✓ |
| 7 | 列表 PNG 其余项 | banner-management-list.png | 第一列 delta 已 acceptance 覆盖 | ✓ |
| 8 | 弹窗宽度验收（非 640px PNG） | SKU 弹窗并排 | CSS + Vitest | ✓ |

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 18:57:34 | `/opsx-archive` | Delta spec 合并至 `openspec/specs/web-client/spec.md`；BUG-0039/0040 promote → archive |
| 2026-06-28 18:02:30 | `/opsx-apply` | 列表展示位置列 + 弹窗 880px；Vitest 9 passed；build OK |
| 2026-06-28 18:02:00 | `/sprint-propose` | 纳入 sprint-003 |
| 2026-06-28 17:46:46 | `/bug-opsx` | 自 BUG-0039、BUG-0040 创建 fix change |
