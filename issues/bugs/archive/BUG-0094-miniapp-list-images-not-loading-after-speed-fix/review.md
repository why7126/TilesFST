---
bug_id: BUG-0094-miniapp-list-images-not-loading-after-speed-fix
status: done
decision: approve
reviewed_at: 2026-07-31 15:28:52
created_at: 2026-07-31 15:28:52
updated_at: 2026-07-31 21:32:14
reviewer: product
severity: high
related_requirement: REQ-0049-miniapp-product-card-component
---

# 评审结论

确认修复，状态推进为 `approved`。

# 评审清单

- [x] 可复现或根因充分：真机证据显示异常图片请求集中在 `/media/thumbnails/default/tiles/pending/<uuid>.jpg`；生产确认公开 SKU 存在 pending 主图引用，原图存在但 thumbnail 不存在。
- [x] 严重等级合理：影响小程序首页与多个商品列表入口的商品图片展示，属于 `BUG-0092` 性能修复后的高影响回归，严重等级 `high` 合理。
- [x] 回归验收明确：acceptance 已覆盖首页/列表图片恢复、pending 主图处理、缩略图同路径命名、历史缩略图回填、数据审计和性能不退化。
- [x] 是否需 hotfix 路径：建议优先进入修复流程；若体验版或生产展示持续受影响，可在 Change 中评估 hotfix 路径，先补齐历史缩略图并避免公开列表返回不可访问缩略图 URL。

# 审核说明

本缺陷已完成 capture、generate、complete，并补充多轮真机与生产确认：

- 生产接口 `cover_image` 均返回 `/media/thumbnails/...`。
- 真机异常请求集中在 `/media/thumbnails/default/tiles/pending/<uuid>.jpg`。
- 生产公开 SKU 主图存在 `images/default/tiles/pending/<uuid>.jpg`。
- 原图对象存在，thumbnail 对象不存在。
- 修复策略确认为补齐缩略图；缩略图与原图同路径存储，通过文件名差异区分，并补全历史缩略图。

# 后续动作

- 允许执行 `/bug-opsx BUG-0094-miniapp-list-images-not-loading-after-speed-fix` 创建 OpenSpec fix Change。
- 允许纳入 Sprint 正式范围。
