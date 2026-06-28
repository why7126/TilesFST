---
bug_id: BUG-0039-banner-list-display-position-column
status: pending_review
created_at: 2026-06-28 17:43:07
updated_at: 2026-06-28 17:43:07
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 列表第一列 JSX 叠放标题与展示位置

`BannerManagementPage.tsx` 第一列 `<td>` 在缩略图旁同时渲染：

```tsx
<span className="banner-main">{banner.title}</span>
<span className="banner-sub">{positionLabel(banner.position)}</span>
```

表头仅为「Banner」，无独立「展示位置」列。`banner-management.css` 中 `.banner-sub` 以 11px 弱色副文案叠在标题下方，与「展示端」（`display_client`）已独立成列形成信息层级不一致。

### 1.2 列表列定义忠实 port 原型 HTML

REQ-0016 `banner-management-list.html` 样例行结构为：

```html
<span class="banner-main">意式岩板新品首发</span>
<span class="banner-sub">首页顶部轮播</span>
```

`banner-management-list-context.md` §8 列字段为「Banner、展示端、跳转类型…」，未将 `position` 独立成列。实现按原型 1:1 port，导致展示位置与标题同列。

## 2. 根本原因

### 2.1 原型信息架构将 position 作为 Banner 单元格副标题

产品设计将「展示位置」作为 Banner 行内辅助信息（副标题），而非表格维度字段。运营反馈表明：已有「展示端」列后，「展示位置」作为独立列更易扫读，与 SKU/用户等管理列表「一字段一列」习惯更一致。

### 2.2 列表 port 未纳入后续 UX 反馈迭代

`add-banner-management` 与 `fix-banner-admin-ui` 聚焦分页、弹窗、确认框等缺口，未 revisiting 列表第一列信息架构。`position` 数据已在 API 响应与 `positionLabel()` 工具函数中存在，拆分列无需后端变更。

### 2.3 与现行原型 / OpenSpec 的 delta

修复后第一列结构将与 `banner-management-list.html` / PNG 不一致，属 **acceptance 优先于原型**（同 BUG-0030、BUG-0027）。`/bug-opsx` 须在 delta spec 中 MODIFIED 列表列结构说明。

## 3. 触发条件

满足以下条件可 **100% 稳定复现**：

1. 以 admin 或 employee 登录 Web 管理端。
2. 访问 `/admin/banners`，列表存在至少一条 Banner。
3. 观察第一列：标题与展示位置两行文案同列显示。

无需特定筛选或数据状态。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否（交付即存在；按原型有意实现） |
| 主要修复面 | `BannerManagementPage.tsx` 表头/列；可选精简 `.banner-sub` |
| 建议 Change | `fix-banner-list-display-position-column`（可与 BUG-0040 合并为 `fix-banner-list-and-modal-ui`） |

## 5. 后续修复建议

1. 表头在「Banner」与「展示端」之间（或「Banner」之后）新增 `<th>展示位置</th>`。
2. 第一列 `<td>` 仅保留缩略图 + `banner.title`；新增 `<td>{positionLabel(banner.position)}</td>`。
3. 加载/空态 `colSpan` 由 8 调整为 9。
4. 可选：移除或保留 `.banner-sub`（若不再使用可删 CSS）。
5. SHOULD 补充 Vitest：断言存在「展示位置」表头，第一列不含 `.banner-sub`。
6. `/bug-opsx` delta 说明与 list PNG 第一列结构的 MODIFIED。
