---
bug_id: BUG-0030-banner-list-ui-inconsistency
status: pending_review
created_at: 2026-06-28 16:16:51
updated_at: 2026-06-28 16:16:51
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 表格上方存在原型 port 的 section-head 与 table-toolbar

`BannerManagementPage.tsx` 在 `table-card` 外额外包裹：

```text
section
├── section-head（「Banner 列表」+「共 N 个 Banner」）
└── table-card
    ├── table-toolbar
    │   ├── table-count（「当前显示 X-Y / N」）
    │   └── section-note（删除规则提示）
    ├── table
    └── banner-pagination
```

用户管理页结构为：

```text
section.table-card
├── table
└── pagination（page-summary + page-right）
```

Banner 页多出的 `section-head` 与 `table-toolbar` 直接来自 REQ-0016 列表原型 HTML（`banner-management-list.html`），与用户管理页及 `admin-list-page-consistency.md` 要求的「`table-card` 内无重复 section 标题」冲突。

### 1.2 分页使用自定义 banner-pagination DOM

Banner 页分页结构：

```text
banner-pagination
├── banner-page-left（每页 + select +「X-Y / N」范围）
└── page-buttons（‹ + 最多 5 个页码 + ›）
```

标准管理端分页（用户管理 / 品牌 / 规格修复后）：

```text
pagination
├── page-summary（「共 N 个…」）
└── page-right
    ├── page-buttons（‹ + 当前页 active + ›）
    └── page-size-wrap（「每页显示」+ select）
```

`BannerManagementPage` 已 `import` `user-management.css`，但分页 DOM 使用 `banner-pagination` / `banner-page-left` / `banner-page-size`，样式由 `banner-management.css` 单独定义，未接入 `.pagination`、`.page-summary`、`.page-size-wrap` 等已验收类名。

## 2. 根本原因

### 2.1 CSS Port 以 REQ-0016 原型 HTML 为准，未对齐管理端列表黄金参考

`add-banner-management` 实现时忠实 port 了 `banner-management-list.html` 的 section-head、table-toolbar 与原型分页（含 AC-021 左侧 `1-10 / 32` 式范围），未参照 BUG-0002 / BUG-0009 / BUG-0027 已修复的用户管理页分页模式及 `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 基准要求。

### 2.2 管理端列表分页仍缺少共享组件或强制复用约束

与 BUG-0002、BUG-0009、BUG-0027 相同：分页由各页面手写 DOM。新增 Banner 页时 invent 了 `banner-pagination` + 多页码条 + 双处范围文案（toolbar 与分页左栏重复），而非复制已验收分页片段。

### 2.3 REQ-0016 AC-021 与列表一致性规范存在语义冲突

REQ-0016 AC-021 要求左侧「每页 10/20/50 + `1-10 / 32` 式范围」；`admin-list-page-consistency.md` 要求左侧 `page-summary`「共 N 条/个」。本 BUG 修复以管理端列表一致性规范及用户管理页为基准（同 BUG-0027），需在 `fix-banner-admin-ui` delta spec 中 MODIFIED 消化 AC-021 左侧范围文案要求。

## 3. 触发条件

满足以下条件时可稳定复现：

1. 以 admin 或 employee 登录 Web 管理端（local 或 Docker）。
2. 访问 `/admin/banners` Banner 管理列表页。
3. 观察表格上方「Banner 列表」标题与「当前显示 … / …」行。
4. 观察底部分页区域 DOM 与样式。
5. 与 `/admin/users` 用户管理列表页并排对比。

无需 Banner 数据即可复现结构问题；有数据时分页差异更明显。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 主要修复面 | Web 管理端 Banner 列表页 section-head / table-toolbar / 分页 DOM |
| 关联需求 AC | REQ-0016 AC-021（需 delta 消化）、列表原型 AC-050 |

## 5. 后续修复建议

1. 删除 `section-head` 区块；`table-card` 直接作为列表容器（对齐 `UserManagementPage`）。
2. 删除 `table-toolbar` 及 `table-count`；删除规则提示保留于 disabled 删除按钮 `title`（已实现）。
3. 将 `banner-pagination` 替换为标准 `.pagination` 结构，复制 `UserManagementPage` 分页 JSX 模式。
4. 移除 `banner-management.css` 中 `.banner-pagination`、`.banner-page-left`、`.banner-page-size` 等冗余规则。
5. 建议 Change 命名：`fix-banner-admin-ui`（与 BUG-0031–0036 合并）。
6. SHOULD 补充 `BannerManagementPage` Vitest：断言含 `.pagination`、`.page-summary`、`.page-size-wrap`，不含 `section-head` / `banner-pagination`。
