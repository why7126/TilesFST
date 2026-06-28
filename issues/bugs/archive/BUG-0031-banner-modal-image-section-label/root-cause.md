---
bug_id: BUG-0031-banner-modal-image-section-label
status: pending_review
created_at: 2026-06-28 16:20:00
updated_at: 2026-06-28 16:46:00
root_cause_type: design
---

# 根因分析

## 1. 直接原因

`BannerFormModal.tsx` 在 `.banner-upload-box` 内渲染 `.banner-upload-title`（L315–321），根据 `imageSource` 动态显示：

| `imageSource` | 首行文案 |
|---|---|
| `custom_upload`（新增默认，L128） | 「自定义上传」 |
| `sku_main_image`（SKU 详情跳转，经 `clearJumpFieldsForType`） | 「SKU 主图」 |
| `sku_gallery_image` | 「SKU 图库」 |

该首行与字段 Label「Banner 图片*」构成重复标题层，且文案为来源类型标签而非上传状态/上下文信息。

## 2. 根本原因

`add-banner-management` CSS Port 时从 REQ-0016 原型 HTML 保留了 upload 区 `upload-title` / `upload-desc` 结构，但实现时将 `upload-title` 误用为 **图片来源枚举标签**，未对齐：

1. **管理端基准**：`BrandFormModal` Logo 区无来源类型首行，仅 preview + 格式说明 + 按钮。
2. **原型语义**：无跳转态 `upload-title` 为「已上传：{filename}」；SKU 详情态为「SKU图库：{SKU名} · 主图」——均非泛化「自定义上传 / SKU 主图」标签。

产品验收认定该首行对运营无增量信息，应移除。

## 3. 触发条件

打开任意 Banner 新增/编辑弹窗即可 **100% 复现**；切换 `jump_type` 或编辑不同 `image_source` 记录时首行文案变化，但冗余问题均存在。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 修复面 | `src/web/src/features/admin/components/BannerFormModal.tsx`（移除 `banner-upload-title` JSX） |
| 可选清理 | `src/web/src/features/admin/styles/banner-management.css` `.banner-upload-title` |
| 关联修复 | BUG-0032（同 upload 区按钮文案，同 `fix-banner-admin-ui` change） |

## 5. 修复建议

1. 删除 `banner-upload-title` 渲染块；保留 `banner-upload-desc` 帮助文案（尺寸/格式说明） unless 产品要求一并精简。
2. MUST NOT 以其他元素重新渲染「自定义上传 / SKU 主图 / SKU 图库」来源标签。
3. 与 BUG-0032 在 `fix-banner-admin-ui` tasks §3 一并 apply；MUST NOT 回归自定义上传、SKU 主图选择与保存逻辑。
