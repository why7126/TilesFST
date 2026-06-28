---
bug_id: BUG-0035-banner-modal-sku-hero-image-no-effect
status: pending_review
created_at: 2026-06-28 16:17:35
updated_at: 2026-06-28 16:17:35
root_cause_type: code
---

# 根因分析

## 1. 直接原因

`BannerFormModal.tsx` 在构建 SKU 下拉选项时，从列表 API 返回的 `item.images[].object_key` 读取 `mainImageKey`：

```tsx
const mainImage = item.images?.find((img) => img.is_main) ?? item.images?.[0];
mainImageKey: mainImage?.object_key ?? null,
mainImageUrl: mainImage?.url ?? item.main_image_url ?? null,
```

「使用 SKU 主图」与 `handleSkuChange` 均以 `sku?.mainImageKey` 为门禁：

```tsx
if (sku?.mainImageKey) {
  setImageKey(sku.mainImageKey);
  setImageUrl(sku.mainImageUrl ?? `/media/${sku.mainImageKey}`);
}
```

后端 `TileSkuAdminService.list_skus` 调用 `to_item(item)` 时 **未** 传 `include_media=True`，列表项 `images` 恒为 `[]`，`mainImageKey` 恒为 `null`。`mainImageUrl` 虽有 `main_image_url` 回退，但无法写入 `imageKey`，预览 `<img>` 不渲染（条件为 `imageUrl` 存在时虽可显示 URL，但 `imageKey` 为空导致保存被拦截）。

结果：点击按钮仅可能切换 `imageSource` 文案，**预览与表单 key 均不更新**；保存时报「请配置 Banner 图片」。

## 2. 根本原因

### 2.1 前后端契约假设错误

前端实现假设 SKU **列表** 响应与 **详情** 响应均含完整 `images[]`（含 `object_key`）。后端设计为列表轻量、详情 `include_media=True` 才加载图库，二者未在 Banner 弹窗集成时对齐。

### 2.2 静默失败路径未处理

当 `mainImageKey` 缺失时，代码无 `else` 分支提示用户，违反 REQ-0016 business-flow「失败时明确提示」及 OpenSpec SKU 详情变体「MUST 默认预览 SKU 主图」。

### 2.3 验收缺口

- `add-banner-management` tasks 7.2 已勾选「主图默认」，但缺少针对「列表 API + object_key 回填」的 Vitest/E2E。
- 后端 pytest 覆盖 Banner 保存时 SKU 主图校验（给定正确 `image_object_key`），未覆盖前端从列表选项解析 key 的路径。

## 3. 触发条件

满足以下条件时可 **100% 稳定复现**：

1. 以 admin 登录 Web 管理端（local 或 Docker）。
2. 打开 Banner 新增/编辑弹窗，`jump_type=SKU_DETAIL`。
3. 选择 **已有主图** 的有效 SKU（`has_main_image=true`）。
4. 点击「使用 SKU 主图」，或依赖选择 SKU 时的自动回填（`image_source=sku_main_image`）。

**编辑模式例外：** 若 Banner 已从后端加载 `image_object_key` + `image_url`，预览可能正常；但再次点击「使用 SKU 主图」切换回 SKU 主图时仍可能失败（同样依赖 `mainImageKey`）。

**非缺陷路径：**

- `jump_type` 非 `SKU_DETAIL` 时不展示「使用 SKU 主图」按钮。
- 自定义上传（`handleCustomUpload`）正常，不依赖 SKU 列表 `images`。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | **code** / frontend-logic + API 契约 |
| 是否接口缺陷 | 部分（列表 API 未提供 Banner 场景所需 `object_key`；详情 API 可用） |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否（`add-banner-management` 初版即存在） |
| 主要修复面 | `BannerFormModal.tsx`；可选 `tile_sku_admin_service.py` 列表增加 `main_image_object_key` |
| 关联需求 | REQ-0016-banner-management（AC-031） |
| 建议 Change | `fix-banner-modal-sku-hero-image`（或与 BUG-0031–0036 合并 `fix-banner-modal-ui`） |

## 5. 后续修复建议

**方案 A（推荐，纯前端）：**

1. 选择 SKU 或点击「使用 SKU 主图」时，调用 `fetchTileSku(id)` 获取含 `images[]` 的详情。
2. 从详情中取 `is_main` 或首张图的 `object_key` / `url` 写入 `imageKey`、`imageUrl`。
3. 无主图时 `setError('该 SKU 无主图，请自定义上传')`。

**方案 B（后端增强）：**

1. 列表 SQL 增加 `main_image_object_key` 子查询（与 `main_image_url` 并列），或 `list_skus` 对 Banner 下拉场景传 `include_media=True`（需评估性能）。
2. 同步 OpenAPI + Orval。

**方案 C（不推荐）：** 从 `main_image_url` 字符串反解析 `object_key`——URL 格式不稳定，易脆。

修复后 MUST 补充 Vitest：mock 列表 `images: []` + 详情含主图，断言点击按钮后 `imageKey` 被设置。
