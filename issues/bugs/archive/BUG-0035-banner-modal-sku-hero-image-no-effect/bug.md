---
bug_id: BUG-0035-banner-modal-sku-hero-image-no-effect
title: Banner弹窗点击使用SKU主图无任何效果
severity: high
status: draft
owner: product
discovered_at: 2026-06-28 16:04:18
environment: local|docker
related_requirement: REQ-0016-banner-management
related_change: add-banner-management
---

# 缺陷说明

Web 管理端 Banner 新增/编辑弹窗（`BannerFormModal`）在跳转类型为 **SKU 详情**（`jump_type=SKU_DETAIL`）时，「Banner 图片」模块的 **「使用 SKU 主图」** 按钮点击后无法回填 SKU 主图预览，也无法写入表单 `image_object_key`，且无 loading 或错误提示。

根因类型为 **frontend-functional**（数据映射缺口）：

1. 弹窗通过 `fetchTileSkus`（列表 API）加载 SKU 下拉选项，并从 `item.images[].object_key` 解析 `mainImageKey`。
2. 后端 `list_skus` 调用 `to_item(item)` 时 **未** 传 `include_media=True`，列表响应中 `images` 恒为 `[]`，仅 `main_image_url` 有值。
3. 「使用 SKU 主图」与 `handleSkuChange` 均以 `sku?.mainImageKey` 为门禁；`mainImageKey` 为 `null` 时 **静默跳过**，仅可能切换 `imageSource` 文案，预览区不变。
4. 保存时若 `imageKey` 为空，前端拦截「请配置 Banner 图片」，**SKU 详情类 Banner 无法以 SKU 主图来源完成创建**。

该行为违背 REQ-0016 AC-031（选择 SKU 后默认预览 SKU 主图）及 OpenSpec `add-banner-management` SKU 详情变体场景。

# 复现步骤

1. 以 admin 登录 Web 管理端（local `5173` 或 Docker `3000`）。
2. 进入「Banner 管理」（`/admin/banners`），点击「+ 新增 Banner」打开弹窗。
3. 将 **跳转类型** 设为「SKU 详情」。
4. 在 **关联 SKU** 下拉中选择一条 **已有主图** 的有效 SKU。
5. 在 **Banner 图片** 区域点击 **「使用 SKU 主图」**。
6. 观察图片预览区、`image_source` 文案及保存行为。
7. 可选：编辑已关联 SKU 的 Banner，重复步骤 5–6。

# 期望结果

- 选择 SKU 后（`image_source=sku_main_image`），**默认** 预览该 SKU 主图，并写入 `image_object_key` 与预览 URL。
- 点击「使用 SKU 主图」后，预览区显示所选 SKU 主图；`image_source` 为 `sku_main_image`；`sku_gallery_asset_id` 清空。
- SKU 无主图或无法解析主图 `object_key` 时，给出 **明确错误提示**（如「该 SKU 无主图，请自定义上传」），不得静默无响应。
- 保存 SKU 详情 Banner 时，后端 `_validate_sku_image` 校验通过（`image_object_key` 与 SKU 主图 key 一致）。

# 实际结果

- 点击「使用 SKU 主图」后，预览区 **无变化**；`imageKey` 仍为空。
- 选择 SKU 时同样无法自动回填主图（`handleSkuChange` 依赖空的 `mainImageKey`）。
- 无 loading、无错误 toast/inline 提示。
- 尝试保存时提示「请配置 Banner 图片」，功能链路阻断。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / Banner 弹窗 | `jump_type=SKU_DETAIL` 的新增与编辑；SKU 主图来源不可用 |
| REQ-0016 验收 | AC-031、business-flow §8「默认 image_source = sku_main_image，预览 SKU 主图」未满足 |
| 关联 Change | `add-banner-management`（tasks 7.2 已勾选，实现未打通） |
| 关联缺陷 | BUG-0032/0031（同弹窗图片区 UI，可同 change 修复但本 BUG 为功能阻断） |
| 后端 / API / DB | 无变更需求；`get_sku_main_image_key` 与保存校验逻辑正常 |
| 小程序 / 店主端 | 无直接影响（管理端配置能力缺失） |

# 严重等级说明

严重程度为 `high`。

理由：

- **功能阻断**：SKU 详情类 Banner 无法按需求使用 SKU 主图作为 Banner 图，核心业务流程不可用。
- **静默失败**：用户无反馈，易误判为按钮失效或系统故障。
- **非数据损坏**：不涉及错误写入或安全风险；修复面主要为前端（可选辅以列表 API 字段扩展）。

建议在 `add-banner-management` 收尾或独立 `fix-banner-modal-sku-hero-image` 中修复；可与 BUG-0031–0036 合并为 `fix-banner-modal-ui`，但本项 MUST 单独验收 AC-031。

# 代码线索

| 线索 | 路径 |
|---|---|
| Banner 弹窗（问题点） | `src/web/src/features/admin/components/BannerFormModal.tsx` |
| SKU 列表 API（`images` 为空） | `src/backend/app/services/tile_sku_admin_service.py` → `list_skus` / `to_item` |
| SKU 详情 API（含完整 `images`） | `get_sku` → `to_item(..., include_media=True)` |
| Banner 保存 SKU 主图校验 | `src/backend/app/services/banner_admin_service.py` → `_validate_sku_image` |
| 父 Change / OpenSpec | `openspec/changes/add-banner-management` |
| REQ-0016 验收 | `issues/requirements/archive/REQ-0016-banner-management/acceptance.md` AC-031 |
