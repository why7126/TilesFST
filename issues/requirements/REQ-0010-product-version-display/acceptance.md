---
title: 需求验收标准
purpose: REQ-0010 产品版本号展示验收标准
content: 基于 requirement.md 与 prototype/web/product-version-display-context.md
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-27 10:21:38
updated_at: 2026-06-27 10:21:38
note: REQ-0010-product-version-display
---

# 验收标准

## 1. 版本维护（FR-001）

- [ ] **AC-001** `src/shared/` 存在单一产品版本常量（如 `PRODUCT_VERSION = 'v0.0.1'`），管理端与店主端 MUST 引用同一导出。
- [ ] **AC-002** MUST NOT 从 `package.json`、`pyproject.toml`、FastAPI `version` 或 Git/build 信息读取产品版本。
- [ ] **AC-003** 发版 checklist（或 release note 模板）含「人工更新产品版本常量」检查项。

## 2. 管理端展示（FR-002）

- [ ] **AC-004** 登录后访问 `/admin/dashboard`（及任意 `/admin/*` 经 `AdminLayout` 页面），侧边栏顶部可见产品名 `TILESFST`。
- [ ] **AC-005** 产品名右侧同一行展示版本 pill，文案与 FR-001 常量一致（如 `v0.0.1`）。
- [ ] **AC-006** 版本 pill 垂直居中对齐产品名，布局参照 `prototype/web/images/sidebar-version-reference.png`（SoulKing 参考）。
- [ ] **AC-007** MUST NOT 展示 API / 后端 / OpenAPI 版本号。
- [ ] **AC-008** 导航项、用户菜单、主内容区布局无回归。

## 3. 店主端展示（FR-003）

- [ ] **AC-009** 访问店主端带侧栏页面（如首页 `LandingPage` 或列表 `ListPage`），侧栏**最上方**（筛选区块之上）可见品牌名 + 版本 pill。
- [ ] **AC-010** 版本值 MUST 与管理端一致（同一常量）。
- [ ] **AC-011** 版本 MUST 在侧栏内展示；MUST NOT 仅在 `SiteNav` 顶栏展示而侧栏缺失。
- [ ] **AC-012** 筛选 checkbox 区、商品列表、分页无回归。

## 4. 视觉与无障碍（FR-004）

- [ ] **AC-013** 版本 pill 为小号圆角 badge（约 10–11px），使用 semantic token（`text-muted`/`text-subtle`、`border-border-default` 或 `border-border-chip` 等），TSX/CSS 无裸 Hex。
- [ ] **AC-014** 版本区域具备读屏可感知文本或 `aria-label`（如「产品版本 v0.0.1」）。
- [ ] **AC-015** 1280×1024 下与 `prototype/web/product-version-sidebar-admin.html`、`product-version-sidebar-catalog.html` 并排验收。

## 5. 回归与不回归

- [ ] **AC-016** 登录页、页脚、关于页 **不** 展示产品版本（本期 Out）。
- [ ] **AC-017** 无 API / OpenAPI / Orval / 数据库变更。
- [ ] **AC-018** 微信小程序不涉及。

## 6. 自动化与构建

- [ ] **AC-019** vitest：`AdminSidebar` 渲染含 `PRODUCT_VERSION` 文案。
- [ ] **AC-020** vitest：`Sidebar`（或封装头部组件）渲染含同一 `PRODUCT_VERSION` 文案。
- [ ] **AC-021** 测试通过 import 常量断言，不在测试中 duplicate 硬编码版本字符串。
- [ ] **AC-022** `cd src/web && pnpm test` 与 `pnpm build` 通过。

## 7. OpenSpec 与流程

- [ ] **AC-023** 变更经 OpenSpec `add-product-version-display`（或等价 change-id）进入开发并 archive。
