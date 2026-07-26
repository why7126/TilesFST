## 1. 准备与定位

- [x] 1.1 阅读 `REQ-0010-product-version-display` requirement、acceptance、prototype context
- [x] 1.2 对照 `AdminSidebar.tsx`、`shared/ui/sidebar.tsx`、`LandingPage` / `ListPage`
- [x] 1.3 确认不涉及 API、数据库、Orval、MinIO 变更

## 2. 产品版本常量

- [x] 2.1 新增 `src/shared/product-version.ts`（或等价），导出 `PRODUCT_VERSION = 'v0.0.1'`
- [x] 2.2 配置 Web alias/import 路径，管理端与店主端均可引用

## 3. 共享 UI 组件

- [x] 3.1 新增 `ProductVersionBadge`（或 brand-head 组合组件），semantic token pill 样式
- [x] 3.2 设置 `aria-label`（如「产品版本 {version}」）；MUST NOT 裸 Hex

## 4. 管理端集成

- [x] 4.1 扩展 `AdminSidebar` 顶部：TILESFST + `ProductVersionBadge`
- [x] 4.2 调整 `admin-home.css` brand-head 布局（flex、gap）；导航与用户菜单无回归

## 5. 店主端集成

- [x] 5.1 扩展 `Sidebar` 顶部 brand-head：STONEX（或 prop）+ 同一 badge
- [x] 5.2 确认 `LandingPage` / `ListPage` 经 `CatalogBody` 渲染可见版本

## 6. 测试

- [x] 6.1 Vitest：`AdminSidebar` 渲染含 `PRODUCT_VERSION`（import 常量断言）
- [x] 6.2 Vitest：`Sidebar`（或 brand-head）渲染含同一 `PRODUCT_VERSION`
- [x] 6.3 运行 `cd src/web && pnpm test` 与 `pnpm build`

## 7. 文档与发版检查

- [x] 7.1 更新 release checklist 或 sprint release-note：发版须人工更新 `PRODUCT_VERSION`
- [x] 7.2 1280×1024 并排验收：admin/catalog HTML 原型 + 实现截图（可选 PNG）
- [x] 7.3 更新 `REQ-0010` trace、`openspec/changes/add-product-version-display/trace.md` checklist
