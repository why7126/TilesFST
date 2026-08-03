---
bug_id: BUG-0101-thumbnail-optimization-size-regression
review_status: rejected
reviewed_at: 2026-08-02 16:56:28
created_at: 2026-08-02 16:56:28
updated_at: 2026-08-02 16:56:28
review_result: rejected
related_requirement: REQ-0092-brand-certificate-image-thumbnails
---

# BUG Review

## 结论

驳回为 SKU 缩略图回归缺陷，转为需求 `REQ-0092-brand-certificate-image-thumbnails`。

## 评审依据

- 用户确认新上传商品图片的原图与缩略图大小已经不一样，缩略图明显小于原图。
- BUG-0100 的 SKU 商品图片真实缩略图能力当前复核成立，本 BUG 不再作为 SKU 回归缺陷推进。
- 当前新增诉求是品牌图片和证书图片也需要具备类似商品图片的缩略图生成与使用能力，属于尚未覆盖的新能力扩展。

## 后续动作

- 使用 `REQ-0092-brand-certificate-image-thumbnails` 继续需求探索、PRD 生成、评审和 OpenSpec Change。
- 本 BUG 保留在 `plan/` 阶段，状态为 `rejected`，作为需求来源追溯。
