---
requirement_id: REQ-0098-admin-media-list-thumbnails
created_at: 2026-08-05 09:20:54
updated_at: 2026-08-05 09:20:54
---

# 用户故事

## US-001 运营人员快速浏览 SKU 图片

作为后台运营人员，我希望 SKU 列表优先加载主图缩略图，这样我在翻页或筛选后能更快识别商品，而不用等待原图加载完成。

验收要点：

- SKU 列表项存在主图时，接口返回 `main_image_thumbnail_url`。
- SKU 列表图片优先使用 `main_image_thumbnail_url`。
- 缩略图不可用时，页面能回退到 `main_image_url` 或既有占位。

## US-002 运营人员快速浏览 Banner 图片

作为后台运营人员，我希望 Banner 列表优先加载 Banner 图片缩略图，这样我能快速确认投放图是否正确，而列表不必加载原图。

验收要点：

- Banner 列表项存在图片时，接口返回 `image_thumbnail_url`。
- Banner 图片来源为 SKU、品牌、专题或自定义上传时，缩略图字段与最终 `image_object_key` 一致。
- Banner 列表图片优先使用 `image_thumbnail_url`，失败时不影响行操作。

## US-003 QA 验收图片资源边界

作为 QA，我希望能明确列表、详情、编辑和预览场景分别使用缩略图还是原图，这样我可以设计稳定的回归用例。

验收要点：

- 列表页验证缩略图优先。
- 详情、编辑、放大预览和原文件查看验证原图或原文件保持不变。
- API 字段新增后 OpenAPI、Orval 和前端类型同步。

## US-004 管理员保持列表体验一致

作为后台管理员，我希望 SKU、品牌、证书和 Banner 列表都遵循统一的 image fallback 口径，这样运营人员在不同列表中不会遇到破图、空白或布局抖动。

验收要点：

- 品牌列表继续优先 `logo_thumbnail_url`，缺失时回退原图或首字母占位。
- 证书列表继续优先 `thumbnail_url`，缺失时回退原文件或文件类型占位。
- 图片容器尺寸稳定，加载失败不导致表格布局移动。
