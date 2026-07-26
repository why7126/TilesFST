---
change_id: fix-banner-admin-ui
requirement_id: REQ-0016-banner-management
type: fix
status: archived
created_at: 2026-06-28 16:20:00
updated_at: 2026-06-28 16:35:00
---

# Change Trace — fix-banner-admin-ui

## 1. 关联

| 项 | 值 |
|---|---|
| REQ | REQ-0016-banner-management |
| 父 Change | add-banner-management |
| BUG | BUG-0030、BUG-0031、BUG-0032、BUG-0033、BUG-0034、BUG-0035、BUG-0036 |
| 类型 | fix（列表 + 弹窗 UI/UX） |

## 2. Delta Spec

| 能力 | 变更 |
|---|---|
| web-client | MODIFIED「管理端 Banner 管理页」「Banner 新增编辑弹窗」 |

## 3. 验收 Checklist（apply 后勾选）

| # | 项 | 基准 | 实现 | 状态 |
|---|---|---|---|---|
| 1 | 列表无 section-head / toolbar 范围行 | UserManagementPage | BannerManagementPage | ✓ |
| 2 | 列表标准分页 DOM | user-management.css | `.pagination` | ✓ |
| 3 | 图片区无首行标题 + 选择/更换按钮 | BrandFormModal | BannerFormModal | ✓ |
| 4 | 弹窗 scroll + 备注整行 | modal HTML | banner-management.css | ✓ |
| 5 | SKU/专题 Combobox 单控件 | BUG-0034 AC | SearchableSelect | ✓ |
| 6 | SKU 主图回填 | BUG-0035 AC | fetchTileSku | ✓ |
| 7 | 有效期单字段区间 | modal HTML | BannerValidityField | ✓ |
| 8 | Vitest + 1440 并排 | trace | 7 tests pass + build | ✓ |

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 16:20:00 | `/bug-opsx` | 合并 BUG-0030～0036 创建 change |
| 2026-06-28 16:30:00 | `/opsx-apply` | 列表/弹窗 UI 修复、SearchableSelect、Vitest |
| 2026-06-28 16:35:00 | `/opsx-archive` | 归档；delta 已前向合并至 `add-banner-management/specs/web-client/spec.md`（主 spec 尚无 Banner 条目） |

## 5. 实现摘要

| 文件 | 变更 |
|---|---|
| `BannerManagementPage.tsx` | 标准分页；移除 section-head / table-toolbar |
| `BannerFormModal.tsx` | Combobox、SKU 主图 fetch、有效期区间、上传按钮 |
| `BannerValidityField.tsx` | 新增有效期区间控件 |
| `searchable-select.tsx` | 新增可搜索下拉 |
| `banner-display.ts` | `extractSkuMainImage` |
| `banner-management.css` | modal scroll、备注、Combobox 样式；删除旧分页 CSS |
| `*.test.tsx` | BannerManagementPage、BannerFormModal、extractSkuMainImage |
