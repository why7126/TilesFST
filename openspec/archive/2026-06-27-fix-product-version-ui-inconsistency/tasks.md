## 1. 准备与定位

- [x] 1.1 阅读 `BUG-0013-product-version-ui-inconsistency` 的 bug.md、root-cause.md、acceptance.md、review.md
- [x] 1.2 对照 REQ-0010 原型 HTML、Golden Reference PNG、用户截图 `screenshots/admin-sidebar-version-actual.png`
- [x] 1.3 对照 `src/web/src/shared/ui/badge.tsx`、`product-version-badge.tsx`、`AdminSidebar.tsx`、`sidebar.tsx`
- [x] 1.4 确认不涉及 API、数据库、Orval、MinIO、`PRODUCT_VERSION` 维护策略变更

## 2. Badge 组件重构

- [x] 2.1 为 `Badge` 新增 `version` variant（或等价），对齐 prototype context §3 + ui-design §8（padding、font-weight 500、tracking-badge、semantic token）
- [x] 2.2 重构 `ProductVersionBadge` 为 thin wrapper 使用该 variant；MUST NOT 裸 Hex
- [x] 2.3 可选：在 `/design-system` 预览区展示 `ProductVersionBadge` 与 Badge variant

## 3. 管理端 brand-head 样式

- [x] 3.1 在 `admin-home.css` 为 `.brand-head` 内版本 pill 增加 scoped 兜底样式（确保 admin shell 下边框/背景/弱化文字可辨识）
- [x] 3.2 确认 `AdminSidebar` brand-head flex/gap 与原型一致；导航与用户菜单无回归

## 4. 店主端一致性

- [x] 4.1 确认店主端 `Sidebar` brand-head 共用重构后的 `ProductVersionBadge`
- [x] 4.2 确认 `LandingPage` / `ListPage` 侧栏顶部 pill 与管理端视觉一致

## 5. 测试

- [x] 5.1 更新 Vitest：`ProductVersionBadge`、`AdminSidebar`、`Sidebar` — 断言 pill 关键 class + `PRODUCT_VERSION` 文案
- [x] 5.2 运行 `cd src/web && pnpm test`
- [x] 5.3 运行 `cd src/web && pnpm build`

## 6. 并排验收与追溯

- [x] 6.1 1280×1024 管理端：实现 vs `product-version-sidebar-admin.html` + Golden Reference PNG 并排验收
- [x] 6.2 1280×1024 店主端：实现 vs `product-version-sidebar-catalog.html` 并排验收
- [x] 6.3 对照 BUG-0013 acceptance AC-001～AC-009 与 REQ-0010 AC-006/AC-013/AC-015，记录于本 change `trace.md`
- [x] 6.4 更新 `BUG-0013-product-version-ui-inconsistency/trace.md` 中 `openspec_changes` 状态
- [x] 6.5 评估是否需 `docs/knowledge-base/incidents/` 沉淀（本缺陷为 UI 一致性，通常不需要）
