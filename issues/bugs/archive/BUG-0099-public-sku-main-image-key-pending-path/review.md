---
bug_id: BUG-0099-public-sku-main-image-key-pending-path
title: 公开商品主图对象 key 仍停留在 pending 暂存路径
status: done
severity: high
review_result: approved
reviewed_at: 2026-08-01 07:31:13
reviewer: AI
created_at: 2026-08-01 07:31:13
updated_at: 2026-08-01 08:06:26
---

# BUG Review

## 评审结论

批准修复。

该问题属于已绑定并公开展示的商品主图仍长期保留上传暂存路径的生命周期缺陷。`pending` 作为新建 SKU 前的上传暂存目录可以存在，但商品保存、主图绑定或发布后仍引用该路径，会造成对象目录语义错误，并给后续 pending 清理、缩略图派生和公开端访问带来风险。

## 评审清单

- [x] 可复现或根因充分：已确认无 `tile_id` 上传 SKU 图片会生成 `images/default/tiles/pending/...`，SKU 保存时直接写入该 key，发布时不迁移对象。
- [x] 严重等级合理：`high`，公开商品主图长期处于 pending 路径，若后续清理 pending 对象可能导致公开图片丢失。
- [x] 回归验收明确：acceptance.md 已覆盖新建 SKU、编辑 SKU、发布门禁、存量迁移、公开端访问、对象存储安全和回归测试。
- [x] 是否需 hotfix 路径：暂不需要 hotfix；建议作为高优先级常规 BUG 进入 `/bug-opsx` 与 Sprint 规划。若生产环境已经启用 pending 清理或出现公开图片 404，应升级为 hotfix。

## 处理建议

- 后续通过 `/bug-opsx BUG-0099-public-sku-main-image-key-pending-path` 创建 OpenSpec Change。
- 修复应优先在后端 SKU 保存/发布链路补齐暂存对象正式化逻辑，并提供可重入的存量迁移脚本。
- 修复设计必须覆盖同目录缩略图迁移，避免公开商品卡片继续访问 pending 缩略图。
- 修复测试应包含对象存储适配层、数据库引用更新、失败回滚和公开接口回归。
