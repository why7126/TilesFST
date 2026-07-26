## Context

- **BUG**: BUG-0030～BUG-0036（severity：medium×3、low×2、high×2）
- **Related REQ**: `REQ-0016-banner-management`
- **Parent Change**: `add-banner-management`
- **Target files**: `BannerManagementPage.tsx`、`BannerFormModal.tsx`、`banner-management.css`；可选 `src/web/src/shared/ui/`

### 原型 / 验收优先级（MUST）

```text
1. issues/bugs/review/BUG-0030～0036/acceptance.md
2. issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-*.html
3. docs/knowledge-base/best-practices/admin-list-page-consistency.md
4. UserManagementPage / BrandFormModal（黄金参考）
5. openspec/changes/add-banner-management/specs/web-client/spec.md
6. rules/ui-design.md
```

## Bug Analysis Report

| ID | 摘要 | 根因类型 |
|---|---|---|
| 0030 | section-head + toolbar + banner-pagination | design / frontend-ui |
| 0031 | banner-upload-title 冗余 | design / frontend-ui |
| 0032 | 按钮文案 + sr-only file input | frontend-ui |
| 0033 | modal 无 scroll；textarea CSS 不完整 | design / frontend-ui |
| 0034 | SKU/专题双控件 | frontend-ui / UX |
| 0035 | list API 无 images[] → mainImageKey null | code / frontend-logic |
| 0036 | datetime-local 不可用 | frontend-ui |

## Goals / Non-Goals

**Goals:**

- 列表分页与 DOM 对齐用户管理（0030）。
- 弹窗图片区、布局、关联选择、SKU 主图、有效期全部按各 BUG acceptance 修复。
- Vitest 覆盖分页 DOM、上传按钮、SKU 主图 fetch、Combobox 结构。
- delta spec MODIFIED 消化 AC-021 分页范围与 AC-031/036 等冲突项。

**Non-Goals:**

- Banner 消费端（店主 Web / 小程序轮播）。
- 专题 CRUD 管理页。
- 重写 `add-banner-management` 后端 Banner CRUD。
- 秒级 DateTime 选择（BUG-0036 acceptance 裁定分钟精度 + 提交秒填充）。

## Decisions

### D1：七 BUG 合并单一 fix change

- **理由**：共享页面/弹窗/CSS；减少重复 PR；各 BUG acceptance 独立勾选。

### D2：列表分页对齐 UserManagementPage（0030）

- 删除 `section-head`、`table-toolbar`/`table-count`。
- 使用 `.pagination` + `page-summary`「共 N 个 Banner」。
- 删除 `.banner-pagination` CSS。

### D3：图片模块对齐 BrandFormModal（0031/0032）

- 移除 `banner-upload-title`。
- `<label className="btn">` + 动态「选择/更换/上传中」+ `<input hidden>`。

### D4：Modal 滚动（0033）

- `banner-modal-card`：`display:flex; flex-direction:column; max-height:92vh`。
- `.modal-body { overflow:auto; flex:1 }`；footer 固定。

### D5：Combobox 实现（0034）

- 新增 `SearchableSelect`（或复用 shadcn Popover+Command）于 `shared/ui/`。
- SKU：`fetchTileSkus({ keyword })` debounce；专题：`fetchTopics({ keyword })`。
- 编辑态：若已选 id 不在默认列表，mount 时 fetch by id 或 prepend 选项。

### D6：SKU 主图（0035）— 方案 A 纯前端

- `handleUseSkuMainImage` / `handleSkuChange`：调用 `fetchTileSku(id)` 取 `images[]`。
- 取 `is_main` 或首张 `object_key` + `url`；无主图 `setError(...)`。
- **不**默认改列表 API（避免 Orval/性能）；若详情 fetch 失败再评估方案 B。

### D7：有效期（0036）

- 单字段「有效期」：`{start} 至 {end}`，各段 `YYYY-MM-DD HH:mm`。
- 实现：Popover 内日期 + 时分 select，或轻量双段 inline picker（非原生 datetime-local）。
- 提交：`valid_from` 秒 `00`，`valid_to` 秒 `59`；空值语义不变。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| Combobox 新组件 scope | 最小 API；Vitest smoke |
| SKU 详情额外请求 | debounce + cache 已选 SKU |
| AC-021 与列表原型冲突 | delta MODIFIED + trace 记录 |

## Test Plan

- Vitest：`BannerManagementPage` 分页 DOM；`BannerFormModal` 按钮文案、SKU 主图 mock、Combobox 单控件。
- 手工：1440 列表 vs 用户管理并排；四套 modal jump_type 冒烟。
- 后端：若改列表 API，补 pytest；否则仅前端 mock 详情 API。
