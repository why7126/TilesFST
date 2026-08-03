---
bug_id: BUG-0099-public-sku-main-image-key-pending-path
status: done
created_at: 2026-08-01 07:25:02
updated_at: 2026-08-01 08:06:26
---

# 验收标准

## AC-001 新建 SKU 图片绑定后不长期保留 pending key

- GIVEN 管理端新建 SKU 时先上传主图，上传阶段返回 `images/default/tiles/pending/...`
- WHEN 用户保存 SKU 且图片被绑定到新建 SKU
- THEN `tile_images.object_key` 中该主图不应继续使用 `images/default/tiles/pending/...`
- AND 对象 key 应进入可追溯到该 SKU 的正式商品图片目录
- AND `/media/{object_key}` 可正常读取图片

## AC-002 编辑已有 SKU 新增图片使用正式商品目录

- GIVEN 已存在 SKU
- WHEN 用户编辑该 SKU 并上传新增图片
- THEN 上传或保存后的图片 key 应位于该 SKU 的正式商品图片目录
- AND 保存后管理端详情返回的 `images[].object_key` 与数据库一致
- AND 不应出现新增图片仍位于 `images/default/tiles/pending/...`

## AC-003 发布门禁阻止 pending 主图进入公开商品

- GIVEN SKU 已设置主图
- WHEN 用户发布 SKU
- THEN 发布后的公开商品主图不得位于 `images/default/tiles/pending/...`
- AND 如果迁移失败，应阻止发布或回滚到发布前状态，并返回明确错误
- AND 不得出现数据库引用已改但对象不可访问的半成功状态

## AC-004 存量公开商品 pending 主图可安全迁移

- GIVEN 存量公开商品主图位于 `images/default/tiles/pending/...`
- WHEN 执行迁移脚本 dry-run
- THEN 输出待迁移数量、目标 key、缺失对象数量和风险摘要
- AND dry-run 不写数据库、不写对象存储
- WHEN 执行迁移脚本 apply
- THEN 原图、同目录缩略图和数据库引用完成一致迁移
- AND 脚本可重入，重复执行不会重复复制或破坏已迁移数据

## AC-005 公开端图片访问不回退

- GIVEN 商品已经公开
- WHEN 微信小程序商品列表、搜索结果、品牌详情商品 Tab 或商品详情页读取商品主图
- THEN 返回的图片 URL 可访问
- AND 商品卡片缩略图 URL 不再派生到 pending 目录
- AND 原图/缩略图缺失时仍遵循既有 fallback 和占位策略

## AC-006 对象存储安全与目录策略保持一致

- GIVEN 修复涉及对象复制、删除或重命名
- WHEN 后端执行对象迁移
- THEN 所有对象操作必须通过后端对象存储适配层
- AND 不得前端直连对象存储
- AND 不得信任前端提交的目标路径
- AND 不得使用用户原始文件名生成目标 key

## AC-007 回归测试

- MUST 补充后端测试覆盖新建 SKU 上传 pending 图片后保存的 key 正式化。
- MUST 补充后端测试覆盖编辑已有 SKU 新增图片的 key 形态。
- MUST 补充发布流程测试，覆盖 pending 主图迁移成功和失败处理。
- MUST 补充存量迁移或审计脚本测试，覆盖 dry-run、apply、对象缺失、缩略图处理和幂等。
- SHOULD 保留或更新现有 pending 上传前缀测试，确保上传暂存路径本身仍可用于新建前上传场景。
