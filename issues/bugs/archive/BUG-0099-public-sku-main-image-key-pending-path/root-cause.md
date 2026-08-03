---
bug_id: BUG-0099-public-sku-main-image-key-pending-path
status: done
created_at: 2026-08-01 07:25:02
updated_at: 2026-08-01 08:06:26
classification: code-design
---

# 根因分析

## 直接原因

SKU 图片上传接口在没有 `tile_id` 参数时，会将图片对象 key 生成到 `images/default/tiles/pending/...`。这是创建 SKU 前上传图片时的暂存路径。

SKU 创建和编辑保存阶段接收前端提交的 `images[].object_key` 后，直接将该 key 写入 `tile_images.object_key`。当前保存流程没有在业务绑定成功后把 pending 对象迁移到商品自身目录，也没有重写数据库中的对象 key。

SKU 发布阶段只更新商品状态和发布时间，不处理图片对象迁移。因此，创建 SKU 时上传的 pending 主图会原样进入公开商品数据。

## 根本原因

媒体上传链路与 SKU 业务绑定链路之间缺少“暂存对象转正式对象”的生命周期闭环：

- 上传接口已经区分了有 `tile_id` 与无 `tile_id` 的对象路径。
- 业务保存阶段只负责落库引用，没有承担对象迁移或正式化职责。
- 发布阶段只校验主图存在，没有校验主图 key 是否仍处于 pending 目录。
- 现有测试覆盖了 pending 上传前缀和公开图片审计指标，但没有把“公开商品主图不得长期位于 pending”作为保存/发布门禁。

## 触发条件

满足以下条件时容易稳定触发：

1. 管理端处于新建 SKU 模式，SKU 尚无 `tile_id`。
2. 用户先上传 SKU 图片，上传接口使用 `tiles/pending` 资源路径。
3. 用户保存 SKU，并将该图片作为主图。
4. 用户发布 SKU 或该 SKU 进入公开展示范围。

## 缺陷分类

- `code`：保存/发布流程缺少对象迁移、key 重写和引用更新。
- `design`：媒体对象生命周期缺少暂存态到正式态的明确边界和验收门禁。
- `data`：存量 `tile_images.object_key` 中可能已有公开商品主图指向 pending 路径，需要迁移或兼容处理。

## 风险

- 后续如果增加 pending 清理任务，可能误删公开商品主图。
- 公开端缩略图 URL 会沿用 pending 目录，导致对象目录语义继续外泄到公开访问路径。
- 如果只迁移原图而遗漏同目录缩略图，公开商品列表可能出现缩略图 404 或回退原图。
