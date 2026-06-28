---
bug_id: BUG-0031-banner-modal-image-section-label
title: Banner弹窗图片模块首行自定义上传/SKU主图文案冗余
severity: low
status: draft
owner: product
discovered_at: 2026-06-28 16:04:18
environment: local|docker
related_requirement: REQ-0016-banner-management
related_change: add-banner-management
related_bug: BUG-0032-banner-modal-upload-button-label
---

# 缺陷说明

Web 管理端 Banner 新增/编辑弹窗（`BannerFormModal`）「Banner 图片」模块首行存在「自定义上传 / SKU 主图 / SKU 图库」类来源说明文案（`.banner-upload-title`），与 REQ-0016 弹窗原型及同类上传区（如品牌 Logo）不一致；该首行对运营无增量信息，与字段 Label「Banner 图片*」形成重复标题层。

根因类型为 **frontend-ui**：

1. `add-banner-management` 实现时在 upload box 内根据 `imageSource` 动态渲染来源类型标题（「自定义上传」「SKU 主图」「SKU 图库」）。
2. 新增模式默认 `imageSource = 'custom_upload'`（L128），打开弹窗即 100% 显示「自定义上传」。
3. 切换跳转类型为 SKU 详情时，`clearJumpFieldsForType` 将 `imageSource` 设为 `'sku_main_image'`，首行变为「SKU 主图」。
4. 品牌 `BrandFormModal` Logo 区无此类来源标题行，仅展示 preview + 格式说明 + 操作按钮。

上传与保存功能正常，属纯 UI/文案冗余，非功能阻断。

# 复现步骤

1. 以 admin 或 employee 登录 Web 管理端（local `5173` 或 Docker `3000`）。
2. 进入「Banner 管理」列表页（`/admin/banners`）。
3. 点击「+ 新增 Banner」打开弹窗；在「Banner 图片」模块观察 upload box 右侧首行文案 → 显示 **「自定义上传」**。
4. 将「跳转类型」切换为 **SKU 详情** → 首行变为 **「SKU 主图」**。
5. 可选：编辑已有 `image_source = sku_gallery_image` 的 Banner → 首行显示 **「SKU 图库」**。
6. 对比「瓷砖品牌」新增/编辑弹窗 Logo 上传区（无「自定义上传」类首行标题）。

# 期望结果

- 「Banner 图片*」字段 Label 之下 **直接** 展示预览区、格式/操作说明（若保留）与上传/选择按钮（如「使用 SKU 主图」）。
- MUST NOT 渲染独立的 `.banner-upload-title` 来源类型首行（「自定义上传 / SKU 主图 / SKU 图库」）。
- 与管理端上传区一致性基准（`BrandFormModal`）对齐：无重复标题层。

# 实际结果

- `BannerFormModal.tsx` L315–321 渲染 `banner-upload-title`，按 `imageSource` 显示来源类型文案。
- 下方 `banner-upload-desc` 仍保留帮助说明（与首行叠加后视觉更冗余）。
- 与 REQ-0016 原型差异：无跳转原型 `upload-title` 为「已上传：filename」状态文案；SKU 详情原型为「SKU图库：{SKU名} · 主图」上下文文案——均 **不是** 当前实现的泛化来源标签。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / Banner 弹窗 | 新增与编辑模式下，各 `jump_type` 的图片模块首行冗余文案 |
| 管理端 UI 一致性 | 未对齐 `BrandFormModal` 及 REQ-0016 弹窗 upload 区信息层级 |
| 关联需求 | REQ-0016-banner-management（`add-banner-management` 弹窗实现） |
| 关联缺陷 | BUG-0032（同 upload 区按钮文案，建议同 change 修复） |

不影响 API、数据库、MinIO 上传链路、权限边界、小程序或店主端。

# 严重等级说明

严重程度为 `low`。

理由：

- 不阻断 Banner 创建/编辑或图片上传保存。
- 主要为视觉冗余与管理端 UI 一致性问题。
- 修复面小（移除或不再渲染 `banner-upload-title`；可选清理 `banner-management.css` 对应样式）。
- 建议与 BUG-0032 合并为 `fix-banner-admin-ui`（或同类 `fix-banner-modal-*` change）一并修复。

# 代码线索

| 线索 | 路径 |
|---|---|
| Banner 弹窗 upload title（问题点） | `src/web/src/features/admin/components/BannerFormModal.tsx` L315–321 |
| 默认 imageSource | 同上 L128（`'custom_upload'`） |
| jump_type 切换 imageSource | `src/web/src/features/admin/lib/banner-display.ts` `clearJumpFieldsForType` |
| upload 区样式 | `src/web/src/features/admin/styles/banner-management.css` `.banner-upload-title` |
| 品牌 Logo 上传基准 | `src/web/src/features/admin/components/BrandFormModal.tsx` |
| 父 Change | `openspec/changes/add-banner-management` |
| REQ-0016 原型 | `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-modal-*.html` |
