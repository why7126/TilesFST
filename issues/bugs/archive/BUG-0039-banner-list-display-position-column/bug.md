---
bug_id: BUG-0039-banner-list-display-position-column
title: Banner列表第一列标题与展示位置挤在同一列
severity: medium
status: approved
owner: product
discovered_at: 2026-06-28 17:28:15
environment: local|docker
related_requirement: REQ-0016-banner-management
related_change: null
---

# 缺陷说明

Web 管理端「Banner 管理」列表页（`/admin/banners`）第一列将 **Banner 标题** 与 **展示位置**（`position`，如「首页顶部轮播」「首页中部运营位」）叠放在同一单元格内：标题为主文案（`.banner-main`），展示位置为副文案（`.banner-sub`）。与「展示端」（`display_client`，如 Web 首页 / 小程序首页）已独立成列相比，展示位置信息混杂在 Banner 列中，扫读与列对齐体验差。

实现按 REQ-0016 列表原型 `banner-management-list.html` port：`banner-main` + `banner-sub` 同列是原型既定结构，非运行时异常。本缺陷属于 **UX / 列表信息架构优化**：用户期望第一列仅保留缩略图 + 标题，展示位置单独成列。

# 复现步骤

1. 以 admin 或 employee 登录 Web 管理端（local `5173` 或 Docker `3000`）。
2. 进入「Banner 管理」列表页（侧栏 OPERATIONS → Banner 管理，或 `/admin/banners`）。
3. 确保列表存在至少一条 Banner 数据。
4. 观察表格第一列：缩略图旁是否同时显示标题与展示位置两行文案。
5. 对比「瓷砖 SKU」「用户管理」等列表的列字段划分。
6. 可选：对照 `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-list.html`（原型同样为同列叠放）。

# 期望结果

- 第一列（表头可为「Banner」或「Banner 标题」）**仅**展示缩略图 + Banner 标题。
- 新增独立列「展示位置」，单元格展示 `positionLabel(banner.position)` 文案（如「首页顶部轮播」），与「展示端」列语义区分清晰。
- 空态、加载态 `colSpan` 与表头列数一致。
- 列表其余列（展示端、跳转类型、状态、有效期、排序、更新时间、操作）行为不变。

# 实际结果

- `BannerManagementPage.tsx` 第一列 `<td>` 内：

```tsx
<span className="banner-main">{banner.title}</span>
<span className="banner-sub">{positionLabel(banner.position)}</span>
```

- 表头无「展示位置」列；`banner-management.css` 中 `.banner-sub` 以 11px 弱色叠在标题下方。
- 与 capture.md 及用户反馈一致。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / Banner 列表 | 列结构与信息可读性 |
| API / 数据库 | 无；`position` 字段已存在于列表响应 |
| 权限 / 业务逻辑 | 无 |
| 原型 / 验收 | 与 `banner-management-list.html` / PNG 第一列结构不一致；修复时 acceptance 优先于原型（同 BUG-0030、BUG-0027 模式），`/bug-opsx` 需说明 delta |
| 关联需求 | REQ-0016-banner-management |
| 已归档 Change | `add-banner-management`、`fix-banner-admin-ui`（未覆盖本列结构） |

不影响小程序、店主端、Banner 弹窗或后端接口。

# 严重等级说明

严重程度为 `medium`。

理由：

- 不阻断列表查询、分页、新增、编辑、上下线、删除等核心功能。
- 属于可见管理端 UI / 信息架构问题，影响运营扫读效率。
- 修复面小（`BannerManagementPage.tsx` + 可选 CSS），无数据迁移风险。
- 可与 BUG-0040 等同域 Banner UI 缺陷合并为单一 `fix-*` change。

# 代码线索

| 线索 | 路径 |
|---|---|
| Banner 列表第一列渲染 | `src/web/src/pages/admin/BannerManagementPage.tsx` |
| 展示位置文案 | `src/web/src/features/admin/lib/banner-display.ts` → `positionLabel()` |
| 列表样式 | `src/web/src/features/admin/styles/banner-management.css` → `.banner-main` / `.banner-sub` |
| 列表原型（当前同列叠放） | `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-list.html` |
| 列表 context 列定义 | `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-list-context.md` §8 |
| 页面测试 | `src/web/src/pages/admin/BannerManagementPage.test.tsx` |
