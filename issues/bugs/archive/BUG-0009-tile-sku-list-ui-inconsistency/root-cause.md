---
bug_id: BUG-0009-tile-sku-list-ui-inconsistency
status: pending_review
created_at: 2026-06-27 10:18:43
updated_at: 2026-06-27 10:18:43
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 SKU 分页 DOM 复用了 BUG-0002 修复前的品牌页局部结构

`TileSkuManagementPage.tsx` 底部分页使用：

```text
pagination
├── page-left（总数 + 翻页按钮混排）
└── brand-pagination-right
    └── page-size
```

用户管理页（及 BUG-0002 修复后的品牌管理页）使用统一结构：

```text
pagination
├── page-summary
└── page-right
    ├── page-buttons
    └── page-size-wrap
```

SKU 页虽引入 `user-management.css` 中的 `.pagination`、`.page-btn`、`.page-size` 基础样式，但 DOM 结构与 `brand-pagination-right` 类名直接继承自品牌页早期实现，未在 BUG-0002 修复后同步对齐用户管理分页模式。

### 1.2 表格卡片内额外插入 table-head 标题行

`TileSkuManagementPage.tsx` 在 `table-card` 内、`<table>` 之前渲染：

```text
table-head
├── table-title「SKU 列表」
└── table-note「默认按更新时间倒序」
```

该结构：

- 在 `user-management.css`、`tile-sku-management.css` 及 REQ-0006 列表原型 HTML 中**均无对应样式与 DOM 约定**。
- 与页面级 `page-hero`（eyebrow +「瓷砖 SKU」+ 说明文案）形成重复标题层级。
- 用户管理页 `table-card` 直接呈现 `<table>`，无卡片内二级标题。

## 2. 根本原因

### 2.1 CSS Port 实现时未以 UserManagementPage 为分页黄金参考

REQ-0006 采用 CSS Port 策略（AC-050、AC-051），要求复用 admin-home / 品牌管理分页与表格模式。SKU 列表实现时从 v4 HTML 原型与品牌页局部模式组合分页 DOM，未参照 BUG-0002 已验收的用户管理分页结构，导致同类管理端列表页视觉分裂。

### 2.2 管理端列表分页仍缺少共享组件或强制复用约束

与 BUG-0002 根因相同：分页由各页面手写 DOM 完成。新增 SKU 页时复制了已废弃的 `page-left` / `brand-pagination-right` 组合，而非抽取或强制复用 `UserManagementPage` 分页片段。

### 2.3 表格卡片信息架构与原型 context 不一致

`tile-sku-management-list-context.md` §4 信息架构为：

```text
.table-card SKU列表 + 分页
```

§5.4 直接描述表格列结构，§5.5 描述分页左右布局，**未定义**卡片内 `table-head` 标题区。实现时额外添加的「SKU 列表」标题行属于局部臆造，偏离原型与用户管理页既有列表模板。

### 2.4 REQ-0006 AC-019～AC-021 语义满足但 AC-051 一致性未达标

分页功能（总数、翻页、每页条数）在逻辑上可满足 AC-019～AC-021，但 AC-051 要求「复用 AdminLayout、AdminSidebar、**分页与表格模式**」。当前 DOM/视觉与用户管理页不一致，属于对 AC-051 及 Design System 一致性条款的实现缺口。

## 3. 触发条件

满足以下条件时可稳定复现：

1. 以 admin 登录 Web 管理端（local 或 Docker）。
2. 访问 `/admin/tile-skus` 瓷砖 SKU 列表页。
3. 列表存在分页数据，底部分页区域渲染。
4. 与「用户管理」列表页底部分页并排对比。
5. 观察 `table-card` 内表头上方是否出现「SKU 列表」标题行。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 主要修复面 | Web 管理端 SKU 列表页分页 DOM + 表格卡片结构 |
| 关联需求 AC | AC-019～AC-021（分页语义）、AC-051（模式复用）、AC-054（原型并排） |

## 5. 后续修复建议

1. 将 `TileSkuManagementPage.tsx` 分页结构对齐 `UserManagementPage.tsx`（或 BUG-0002 修复后的 `BrandManagementPage.tsx`）。
2. 移除 `table-head` / `table-title` / `table-note` 区块；排序说明可保留在 AC-018 约定的列表行为中，无需重复标题行。
3. 删除或不再使用 `page-left`、`brand-pagination-right` 于 SKU 页；统一 `page-summary` + `page-right`。
4. 建议 Change 命名：`fix-tile-sku-list-ui-inconsistency`。
5. 补充 SKU 列表页 Vitest：断言分页 DOM 不含 `page-left` / `brand-pagination-right`，且 `table-card` 内无 `table-head`（参考 `BrandManagementPage.test.tsx`）。
