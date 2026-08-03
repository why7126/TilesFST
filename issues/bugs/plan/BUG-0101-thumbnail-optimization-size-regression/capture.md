---
bug_id: BUG-0101-thumbnail-optimization-size-regression
status: rejected
created_at: 2026-08-01 11:51:41
updated_at: 2026-08-02 16:56:28
severity_hint: high
environment: backend-media
related_requirement: REQ-0092-brand-certificate-image-thumbnails
related_bug: BUG-0100-thumbnail-size-equals-original
lifecycle_stage: plan
captured_via: capture
classification_rationale: 系统已有 SKU 缩略图生成与优化能力，且 BUG-0100 已针对“缩略图与原图大小一致”完成修复；用户反馈“当前生成的缩略图大小与原图大小优化后一样”，表现为优化后结果仍不符合已交付能力预期，属于既有能力回归或修复未完全生效，因此判定为 BUG。
---

# 现象

SKU 当前生成的缩略图大小在优化后仍与原图大小一样，缩略图没有体现降尺寸、降体积或加载加速效果。

# 复现步骤

1. 上传或选择一个 SKU 原图。
2. 触发当前缩略图生成或优化流程。
3. 获取该 SKU 原图对象与缩略图对象。
4. 对比原图和缩略图的像素尺寸、文件体积、对象 key、MIME Type 与访问 URL。
5. 观察缩略图是否仍与原图大小一致。

# 期望 vs 实际

- 期望：SKU 缩略图在优化后应使用真实派生图，像素尺寸和文件体积应符合缩略图目标约束，列表、卡片和预览场景能实际减少加载成本。
- 实际：缩略图优化后仍与原图大小一样，可能说明缩略图生成、压缩、重生成、对象引用或前端取图链路未正确使用优化结果。

# 影响范围

- 后端 media 模块的 SKU 图片缩略图生成、优化和对象存储写入逻辑。
- 已有 SKU 图片缩略图重生成或迁移流程。
- 管理端、店主 Web 展示端、微信小程序中依赖 SKU 缩略图的列表、卡片、预览加载性能。
- 对象存储容量、流量消耗和移动端首屏体验。

# 初步线索

- 需要复核 BUG-0100 对应修复 `fix-media-thumbnail-generation` 是否只覆盖新增上传，未覆盖优化后重生成或存量对象。
- 需要确认缩略图生成后返回、保存或展示的 URL 是否仍指向原图或 pending/original 对象。
- 需要检查缩略图优化流程是否在某些尺寸、格式或质量参数下跳过 resize/compress。
- 需要确认对象存储中 thumbnail key 对应内容是否真实派生，而不是复制原图内容。

# 建议验收或复现要点

- [ ] 新上传 SKU 图片生成的缩略图像素尺寸小于原图，并符合约定最大宽高。
- [ ] 优化或重生成后的存量 SKU 缩略图不再与原图大小一致。
- [ ] 缩略图文件体积通常小于原图，且格式转换不会异常放大文件。
- [ ] SKU 列表、卡片和预览场景使用缩略图 URL，详情大图仍可使用原图或高清图。
- [ ] 覆盖横图、竖图、大图、小图、透明图、已存在缩略图重生成等测试场景。
- [ ] 与 BUG-0100 的修复结果做回归比对，确认没有再次退化为复制原图。

# 附件

- 暂无。

# 重新分类说明

2026-08-02 用户确认：新上传商品的原图与缩略图大小已经不一样，缩略图明显小于原图，SKU 缩略图回归缺陷不成立。真实诉求是品牌图片和证书图片也需要实现类似商品图片的缩略图能力，因此本 BUG 转为需求 `REQ-0092-brand-certificate-image-thumbnails`，BUG 状态标记为 `rejected`。
