---
bug_id: BUG-0034-banner-modal-link-selector-combined
title: Banner弹窗关联专题/SKU搜索框与下拉框应合并
severity: medium
status: draft
owner: product
discovered_at: 2026-06-28 16:04:18
environment: local|docker
related_requirement: REQ-0016-banner-management
related_change: add-banner-management
---

# 缺陷说明

Web 管理端 Banner 新增/编辑弹窗（`BannerFormModal`）在跳转类型为「SKU 详情」或「专题页」时，关联目标选择区域将 **搜索输入框** 与 **原生下拉框** 拆成两个独立控件，操作割裂，未对齐 REQ-0016 与原型所期望的 **单一可搜索选择器**（Combobox / Select with search）。

根因类型为 **frontend-ui / design fidelity**：

1. `add-banner-management` 实现时以 `input` + `<select>` 组合近似「可搜索」能力，而非单控件 Combobox。
2. 搜索仅在搜索框按 **Enter** 时触发 API（`loadSkuOptions` / `loadTopicOptions`），与下方 `<select>` 选择步骤分离。
3. REQ-0016 原型 `banner-management-modal-{sku-detail|topic-page}.html` 中「关联 SKU / 关联专题」均为 **单个** `<select>`，当前实现多了一个原型中不存在的独立搜索框。

后端 `GET /api/v1/admin/tile-skus`（keyword）与 `GET /api/v1/admin/topics`（keyword）已就绪；属纯前端交互与 UI 一致性问题，非 API 缺失。

# 复现步骤

1. 以 admin 或 employee 登录 Web 管理端（local `5173` 或 Docker `3000`）。
2. 进入「Banner 管理」列表页（`/admin/banners`），点击「+ 新增 Banner」或编辑已有 Banner。
3. 将「跳转类型」设为 **「SKU 详情」** 或 **「专题页」**。
4. 观察「关联 SKU」或「关联专题」字段：上方为 placeholder「搜索 SKU / 搜索专题」的 `input`，下方为「请选择 SKU / 请选择专题」的 `<select>`。
5. 在搜索框输入关键词但不按 Enter：下方下拉选项不变。
6. 按 Enter 后选项刷新，仍需在下方 `<select>` 中二次选择。
7. 可选：对照原型 `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-modal-sku-detail.html` 与 `banner-management-modal-topic-page.html` 中单一选择器结构。

# 期望结果

- 「关联 SKU」「关联专题」各使用 **一个** 可搜索选择控件；输入关键词即筛选候选并在同一控件内完成选择（Combobox 或等效 Select with search）。
- 控件高度 40px，视觉与弹窗其他 `input` / `select` 一致，对齐 REQ-0016 FR-010 / FR-012 与 AC-031 / AC-036。
- 编辑模式下，已保存的 `sku_id` / `topic_id` MUST 正确回显（即使不在默认加载的前 20 条结果中）。
- 布局对齐 prototype 单控件形态，**不得** 出现独立的搜索框 + 下拉框双控件组合。

# 实际结果

- `BannerFormModal.tsx` 在 `jumpType === 'SKU_DETAIL'` 时渲染：
  - `<input placeholder="搜索 SKU">`（`skuKeyword`，Enter 触发 `loadSkuOptions`）
  - `<select>`（`skuId`，从 `skuOptions` 选择）
- `jumpType === 'TOPIC_PAGE'` 时同理：`topicKeyword` + `topicId` 双控件。
- 打开弹窗时默认 `loadSkuOptions()` / `loadTopicOptions()` 无 keyword，仅取前 20 条；编辑时若已选目标不在列表中，select 可能显示空白。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / Banner 弹窗 | `SKU_DETAIL`、`TOPIC_PAGE` 跳转类型的关联目标选择交互 |
| REQ-0016 验收 | AC-031（SKU 可搜索）、AC-036（专题可搜索）体验不达标 |
| 原型 fidelity | 与 `banner-management-modal-sku-detail.html`、`banner-management-modal-topic-page.html` 单控件不一致 |
| 关联缺陷 | BUG-0030~0036 同属 Banner 模块 UI，建议合并为 `fix-banner-modal-ui` 或等价 fix change |

不影响 API、数据库、MinIO、权限边界、Banner 保存逻辑、小程序或店主端。功能上仍可通过双步操作完成配置，但体验差且易误操作。

# 严重等级说明

严重程度为 `medium`。

理由：

- 不阻断 Banner 创建/编辑或跳转目标保存（双控件仍可选中目标）。
- 属于可见 UX 缺陷与 REQ-0016 / 原型 fidelity 问题，影响运营配置效率。
- 编辑模式已选目标可能无法回显，增加误改风险。
- 应在 `add-banner-management` 收尾或独立 fix change 中修复；无需 hotfix。

# 代码线索

| 线索 | 路径 |
|---|---|
| Banner 弹窗双控件（问题点） | `src/web/src/features/admin/components/BannerFormModal.tsx` |
| SKU 列表 API 封装 | `src/web/src/features/admin/api/tile-skus-api.ts` |
| 专题列表 API 封装 | `src/web/src/features/admin/api/topics-api.ts` |
| SKU 详情弹窗原型 | `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-modal-sku-detail.html` |
| 专题页弹窗原型 | `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-modal-topic-page.html` |
| 父 Change | `openspec/changes/add-banner-management` |
| 需求 FR-010 / FR-012 | `issues/requirements/archive/REQ-0016-banner-management/requirement.md` |

**实现提示**：项目当前无现成 Combobox 组件（`src/web/src/components/ui/` 仅基础 shadcn 件）；修复时 MAY 新增 `shared/ui` 可复用 SearchableSelect（shadcn Command + Popover 或轻量自研），并确保编辑模式 preload 已选实体。
