---
purpose: fix-admin-list-status-toast-layout OpenSpec 可测试验收项
content: 自 issues/bugs/BUG-0015-admin-list-status-tips-layout-shift/acceptance.md 映射
bug_id: BUG-0015-admin-list-status-tips-layout-shift
status: proposed
created_at: 2026-06-27 12:48:52
updated_at: 2026-06-27 12:48:52
---

# 验收标准

- [ ] 用户/类目/SKU 三页操作反馈使用 fixed toast，列表顶无文档流 `.admin-notice`。
- [ ] 四页 Tips 出现/消失时 hero、指标卡、筛选区、表格、分页纵向位置不变。
- [ ] 四页 toast 视觉、3200ms 自动消失、`aria-live` 行为一致。
- [ ] 品牌页 fixed toast 行为不回归；`BrandManagementPage.test.tsx` 断言 pass。
- [ ] 品牌 Logo 展示、上传进度、启停确认无回归。
- [ ] toast 样式位于共享 CSS（非仅 `brand-management.css`）。
- [ ] 用户/类目/SKU 各至少 1 条 Vitest 覆盖 toast 路径。
- [ ] 无 API、DB、Orval 变更；Web build 通过。
- [ ] 弹窗 inline 错误与 `AdminLayout` 占位 notice 可保持现状。
