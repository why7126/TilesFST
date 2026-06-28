---
bug_id: BUG-0027-tile-spec-list-ui-inconsistency
status: pending_review
created_at: 2026-06-28 13:20:08
updated_at: 2026-06-28 13:20:08
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 分页 DOM 使用项目内未定义类名，未接入标准分页样式

`TileSpecManagementPage.tsx` 底部分页使用：

```text
pagination-bar
├── pagination-left（共 N 条）
└── pagination-right
    ├── page-btn ‹ ›
    ├── page-indicator（{page} / {totalPages} 文本）
    └── page-size（裸数字 option）
```

用户管理页、品牌管理页（BUG-0002 修复后）、SKU 列表页（BUG-0009 修复后）使用统一结构：

```text
pagination
├── page-summary
└── page-right
    ├── page-buttons
    └── page-size-wrap
```

规格页虽 `import` 了 `user-management.css`（含 `.pagination`、`.page-btn.active`、`.page-size-wrap` 等），但 DOM 类名 `pagination-bar` / `pagination-left` / `page-indicator` **在项目中无任何 CSS 定义**，分页区域落入浏览器默认样式，无法呈现管理端标准分页栏（56px 高度、顶部分割线、激活态金色页码按钮、「每页显示 N 条」文案）。

### 1.2 尺寸名称列 `.size-name` 刻意放大字号与对比度

`tile-spec-management.css`：

```css
.admin-shell .size-name {
  color: var(--admin-text);
  font-size: 13px;
}
```

同表 `.tile-spec-table td` 默认为 12px + `--admin-muted`。该样式直接移植自 REQ-0009 列表原型 HTML（`.size-name`），在无 avatar 辅助的主列场景下，13px 高对比文字相对相邻数值列视觉权重过高，与用户管理页经 avatar + `.user-meta` 平衡后的主列观感不一致。

## 2. 根本原因

### 2.1 CSS Port 实现时以原型 HTML 局部结构为准，未对齐已验收管理端分页黄金参考

REQ-0009 采用 CSS Port（AC-042 要求复用品牌页分页模式）。`add-tile-spec-management` 实现时从 `tile-size-management.html` 移植分页与 `.size-name` 样式，但未参照 BUG-0002 / BUG-0009 已修复的 `UserManagementPage` / `BrandManagementPage` 分页 DOM，导致新页在管理端列表族中视觉分裂。

### 2.2 管理端列表分页仍缺少共享组件或强制复用约束

与 BUG-0002、BUG-0009 根因相同：分页由各页面手写 DOM 完成。新增规格页时 invent 了 `pagination-bar` + `page-indicator` 简化结构，而非复制或抽取已验收分页片段，重复出现同类一致性债务。

### 2.3 REQ-0009 AC-024 语义部分满足但 AC-042 模式复用未达标

分页功能（总数、翻页、每页 20/50/100）在逻辑上可满足 AC-024，但 AC-042 要求「复用 AdminLayout、品牌页启停确认与**分页模式**」。当前 DOM/视觉与用户管理/品牌页不一致，属于对 AC-042 及 Design System 一致性条款的实现缺口。

## 3. 触发条件

满足以下条件时可稳定复现：

1. 以 admin 登录 Web 管理端（local 或 Docker）。
2. 访问 `/admin/tile-specs` 瓷砖规格列表页。
3. 列表存在至少一条规格数据，底部分页区域渲染。
4. 与「用户管理」列表页底部分页并排对比。
5. 观察「尺寸名称」列与同表宽度/长度等列字号差异。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 主要修复面 | Web 管理端规格列表页分页 DOM + `.size-name` 样式 |
| 关联需求 AC | AC-024（分页语义）、AC-042（模式复用）、AC-045（列表原型并排） |

## 5. 后续修复建议

1. 将 `TileSpecManagementPage.tsx` 分页结构对齐 `BrandManagementPage.tsx` / `UserManagementPage.tsx`。
2. 删除 `pagination-bar`、`pagination-left`、`pagination-right`、`page-indicator`；统一 `page-summary` + `page-right` + `page-buttons` + `page-size-wrap`。
3. 调整 `.size-name` 为 12px 或与 `.user-main` 同等视觉层级（若保留 13px 须与产品确认主列规范）。
4. 建议 Change 命名：`fix-tile-spec-list-ui-inconsistency`。
5. 补充 `TileSpecManagementPage.test.tsx`：断言分页 DOM 含 `.pagination`、`.page-buttons`、`.page-size-wrap`，不含 `pagination-bar` / `page-indicator`（参考 `BrandManagementPage.test.tsx`、`TileSkuManagementPage` 修复后测试）。
