---
bug_id: BUG-0034-banner-modal-link-selector-combined
status: pending_review
created_at: 2026-06-28 16:17:29
updated_at: 2026-06-28 16:17:29
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 SKU / 专题关联目标使用 input + select 双控件

`BannerFormModal.tsx` 在 `jumpType === 'SKU_DETAIL'` 时渲染：

```text
label.banner-form-row
├── input（placeholder="搜索 SKU"，skuKeyword）
└── select（skuId，从 skuOptions 选择）
```

`jumpType === 'TOPIC_PAGE'` 时同理：

```text
label.banner-form-row
├── input（placeholder="搜索专题"，topicKeyword）
└── select（topicId，从 topicOptions 选择）
```

搜索与选择被拆成两个独立 DOM 控件，用户须先在上方输入并按 Enter 触发 API，再在下方 `<select>` 二次选择。

### 1.2 搜索触发与选择逻辑分离

- `loadSkuOptions(keyword)` / `loadTopicOptions(keyword)` 仅在搜索框 `onKeyDown` Enter 时传入 keyword；输入过程中不 debounce、不自动刷新选项。
- `skuKeyword` / `topicKeyword` 与 `skuId` / `topicId` 为独立 state，选中后搜索框仍保留输入内容，与 select 显示值不同步。
- 打开弹窗时 `loadSkuOptions()` / `loadTopicOptions()` 无 keyword，SKU 仅取 `page_size: 20` 前 20 条。

### 1.3 编辑模式已选目标可能无法回显

编辑 Banner 时若已保存的 `sku_id` / `topic_id` 不在默认加载的前 20 条结果中，`<select value={skuId}>` 无对应 `<option>`，浏览器显示空白，用户无法确认当前关联目标。

## 2. 根本原因

### 2.1 `add-banner-management` 以最小实现近似「可搜索」需求

REQ-0016 FR-010 / FR-012 要求关联 SKU / 专题选择器「可搜索」。实现阶段未引入 Combobox 或 SearchableSelect，而是用原生 `input` + `select` 组合快速满足 keyword API 调用，未对齐原型单控件形态与 AC-031 / AC-036 所隐含的「搜索即选」交互。

### 2.2 项目缺少可复用 SearchableSelect / Combobox 组件

`src/web/src/components/ui/` 仅有 Input、Button 等基础 shadcn 件；`shared/ui/` 亦无 SearchableSelect。管理端其他表单（品牌、类目、SKU 弹窗）多为静态 `<select>`，Banner 弹窗为首个需要远程搜索下拉的场景，实现时 invent 了双控件模式而非先抽象共享组件。

### 2.3 原型 fidelity gate 未覆盖选择器交互形态

`add-banner-management` trace checklist #9 / #11 验收项为「SKU 选图 + image_source」「topic 下拉 + topics-api」，标记为 ✓，但未校验「搜索与选择是否在同一控件内」。HTML 原型 `banner-management-modal-{sku-detail|topic-page}.html` 中「关联 SKU / 关联专题」均为 **单个** `<select>`，实现多了一个原型中不存在的独立搜索框，并排验收（trace #16 ○ 待人工复核）未提前拦截。

## 3. 触发条件

满足以下条件时可稳定复现：

1. 以 admin 或 employee 登录 Web 管理端（local `5173` 或 Docker `3000`）。
2. 进入 `/admin/banners`，打开新增或编辑 Banner 弹窗。
3. 将「跳转类型」设为 **「SKU 详情」** 或 **「专题页」**。
4. 观察「关联 SKU」或「关联专题」区域存在两个独立控件。
5. 可选：编辑模式下选择排序靠后、不在默认前 20 条的 SKU/专题，观察 select 是否空白。

无需特殊数据即可复现双控件结构；编辑回显问题需目标不在默认列表前 20 条。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否接口缺陷 | 否（`tile-skus` / `topics` keyword API 已就绪） |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 主要修复面 | `BannerFormModal.tsx` 关联 SKU / 专题选择器；MAY 新增 `shared/ui` SearchableSelect |
| 关联需求 AC | REQ-0016 AC-031（SKU 可搜索）、AC-036（专题可搜索） |

## 5. 后续修复建议

1. 新增或复用 **SearchableSelect / Combobox**（建议 `src/web/src/shared/ui/`，shadcn Command + Popover 或轻量自研），高度 40px，对齐弹窗 `input` / `select` 视觉。
2. SKU / 专题各替换为单控件：输入 debounce 调用 `fetchTileSkus({ keyword })` / `fetchTopics({ keyword })`，选中后在同一控件内展示 label。
3. 编辑模式：打开弹窗时若 `banner.sku_id` / `banner.topic_id` 存在，MUST preload 该实体并 merge 进 options，确保回显。
4. 移除 `skuKeyword` / `topicKeyword` 独立 state 及上方搜索 `input`。
5. 建议 Change：`fix-banner-modal-link-selector-combined`，或与 BUG-0030–0036 合并为 `fix-banner-modal-ui`。
6. SHOULD 补充 `BannerFormModal.test.tsx`：断言 SKU_DETAIL / TOPIC_PAGE 分支仅一个关联选择控件、无独立搜索 input。
