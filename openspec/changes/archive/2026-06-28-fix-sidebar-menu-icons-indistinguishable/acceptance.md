# fix-sidebar-menu-icons-indistinguishable — Acceptance

来源：`issues/bugs/archive/BUG-0021-sidebar-menu-icons-indistinguishable/acceptance.md`

## 语义图标

- [ ] AC-001 各菜单独立 Lucide 语义 icon（home/sku/brand/category/banner/users/settings）
- [ ] AC-002 collapsed 态可仅凭图标识别并正确导航
- [ ] AC-003 expanded 态 icon + 文案无布局回归

## 样式与 a11y

- [ ] AC-004 semantic token / currentColor；移除 CSS 伪元素方块
- [ ] AC-005 employee 角色隐藏用户管理后其余 icon 可区分
- [ ] AC-006 aria-label / aria-hidden 保持

## 回归与范围

- [ ] AC-007 REQ-0011 折叠/localStorage/chevron/≤1023px 无回归
- [ ] AC-008 纯前端，无 API/DB/Orval
- [ ] AC-009 Vitest 图标差异 + collapse 用例通过
- [ ] AC-010 collapsed icon-only 视觉验收记录于 trace.md
