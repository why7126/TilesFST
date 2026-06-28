## Why

[BUG-0030-banner-list-ui-inconsistency](issues/bugs/archive/BUG-0030-banner-list-ui-inconsistency/) 至 [BUG-0036-banner-modal-datetime-picker](issues/bugs/archive/BUG-0036-banner-modal-datetime-picker/) 已评审通过，同属 REQ-0016 Banner 管理页 `add-banner-management` 交付后的前端缺口：

1. **BUG-0030**：列表页多余 `section-head` / `table-toolbar`；分页 `banner-pagination` 未对齐用户管理页标准 DOM。
2. **BUG-0031**：弹窗 Banner 图片模块冗余首行来源标题。
3. **BUG-0032**：自定义上传按钮文案「自定义上传 浏览…」，未对齐品牌「选择/更换」模式。
4. **BUG-0033**：弹窗缺滚动/固定头尾；运营备注 textarea 宽度与 placeholder 字号不符。
5. **BUG-0034**：关联 SKU/专题搜索框与下拉框分离，交互不合理。
6. **BUG-0035**（high）：「使用 SKU 主图」无效果——列表 API 无 `object_key`，前端静默失败。
7. **BUG-0036**：原生 `datetime-local` 不可用；有效期需改为单字段区间 DateTime（对齐 modal HTML 原型）。

根据项目规则，已交付能力上的缺陷 MUST 使用 `fix-*` change；七 BUG 共享 `BannerManagementPage` / `BannerFormModal` / `banner-management.css`，合并于本 change。

## What Changes

- **BUG-0030**：移除列表 section 标题与 toolbar 范围行；分页对齐 `UserManagementPage`；MODIFIED 消化 REQ-0016 AC-021 左侧范围文案。
- **BUG-0031**：移除 `banner-upload-title` 首行文案。
- **BUG-0032**：上传按钮动态「选择/更换/上传中」+ `hidden` file input（对齐 `BrandFormModal`）。
- **BUG-0033**：`banner-modal-card` 头尾固定 + body 滚动；port 备注 `textarea` 整行宽度/高度/placeholder。
- **BUG-0034**：SKU/专题改为单一可搜索 Combobox（Popover + Command 或等效 shared 组件）。
- **BUG-0035**：选择 SKU / 点击「使用 SKU 主图」时 fetch SKU 详情取 `object_key`；无主图 inline 错误。
- **BUG-0036**：替换 `datetime-local` 为单字段「有效期」区间控件（`YYYY-MM-DD HH:mm 至 …`）；提交秒策略 `00`/`59`。
- 补充 Vitest；各 BUG acceptance 独立勾选；change `trace.md` 并排验收记录。

## Capabilities

### New Capabilities

（无。）

### Modified Capabilities

- `web-client`：MODIFIED「管理端 Banner 管理页」— 列表分页对齐用户管理；无多余 section 标题。
- `web-client`：MODIFIED「Banner 新增编辑弹窗」— 图片区 UI、布局滚动、可搜索关联选择、SKU 主图回填、有效期 DateTime 区间。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `BannerManagementPage.tsx`、`BannerFormModal.tsx`、`banner-management.css`、可选 `shared/ui` Combobox/DateTime |
| 后端 | BUG-0035 首选纯前端（SKU 详情 API）；MAY 增强列表 `main_image_object_key`（非必须） |
| API / Orval | 默认无；若采用方案 B 则同步 OpenAPI |
| 数据库 | 无 |
| 父需求 | REQ-0016-banner-management |
| 关联 BUG | BUG-0030～0036 |
| 前置 Change | `add-banner-management` |

## Rollback Plan

1. 回滚 `BannerManagementPage.tsx`、`BannerFormModal.tsx`、`banner-management.css` 及新增组件/测试至 fix 前版本。
2. 运行 `cd src/web && pnpm vitest run Banner && pnpm build`。
3. 若已 archive，从 `openspec/specs/web-client/spec.md` 恢复 MODIFIED requirement 前版本。
4. 重新标记 BUG-0030～0036 为未修复。
