---
req_id: REQ-0011-admin-sidebar-expand-collapse
status: captured
created_at: 2026-06-27 10:19:43
updated_at: 2026-06-27 10:19:43
recorded_by: product
source: 竞品
priority_hint: P1
parent_requirement: REQ-0010-product-version-display
---

# 一句话

管理端侧边栏支持展开与收起，交互与控件位置参照 SoulKing 参考图（头部右上角 chevron 切换，收起后仅保留图标列）。

# 原始描述

侧边栏支持展开和收起，参照参考图的展开和收起的交互和位置。

参考图（SoulKing 管理端侧边栏）要点：

- **展开态**：完整宽度；头部含 Logo、产品名、版本 badge、副标题；导航项显示图标 + 文案。
- **收起控件**：位于侧边栏**头部右上角**，使用 chevron 图标（展开时指向左 `<`，收起时指向右 `>`）。
- **收起态**：侧边栏收窄为图标列；隐藏产品名、副标题、导航文案；保留 Logo/图标与导航图标；主内容区随宽度变化自适应。
- **过渡**：展开/收起应有平滑宽度过渡动画。
- **选中态**：收起时当前项仍须可识别（图标高亮或 accent 指示）。

# 待澄清

- [ ] 范围：仅管理端侧边栏，还是店主端筛选 Sidebar 一并纳入？
- [ ] 默认态：首次进入默认展开还是收起？是否持久化用户偏好（localStorage）？
- [ ] 收起宽度：图标列目标宽度（如 64px / 72px）？
- [ ] 收起时头部：Logo 是否保留完整方块还是仅图标；版本 badge 是否隐藏？
- [ ] 收起时底部用户菜单：是否折叠为仅头像、移入主内容区，或保持可展开？
- [ ] 小屏响应式（≤1023px）现有布局变更是否与本需求联动？

# 探索结论

（/req-explore + `/req-complete` 已纳入 PRD 与六件套）

- **范围**：仅管理端 `AdminSidebar`；店主端筛选 Sidebar Out。
- **默认态**：expanded；偏好 `localStorage`（`admin-sidebar-collapsed`）。
- **宽度**：264px ↔ 72px；CSS 变量 `--admin-sidebar-width` + 200–250ms transition。
- **收起裁剪**：隐藏产品名/版本/副标题/nav 文案/用户信息；保留 logo 缩略、nav 图标、active accent、avatar 菜单。
- **响应式**：≤1023px 沿用现有 mobile 布局；chevron 隐藏或禁用。
- **依赖**：建议与 REQ-0010 同 Sprint，REQ-0010 优先或并行。
