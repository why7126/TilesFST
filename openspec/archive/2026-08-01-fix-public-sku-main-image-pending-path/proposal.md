## Why

BUG-0099 已评审通过：公开商品主图已经完成 SKU 绑定并进入店主 Web / 微信小程序公开展示，但大量对象 key 仍长期停留在 `images/default/tiles/pending/...`。`pending` 可作为新建 SKU 前的上传暂存目录存在，但不应成为公开商品主图的长期路径。

当前缺陷会让公开商品素材处于错误的对象生命周期语义中，并给后续 pending 清理、同目录缩略图派生、公开端图片访问和存量数据治理带来风险。一旦引入 pending 清理任务或对象生命周期策略，公开商品主图可能被误删。

## What Changes

- 在 SKU 图片绑定、保存或发布链路中补齐“pending 暂存对象 → SKU 正式对象”的正式化要求。
- 明确公开 SKU 主图不得长期引用 `images/default/tiles/pending/...`。
- 要求正式商品图片 key 可追溯到对应 SKU，例如 `images/default/tiles/{tile_id}/<uuid>.<ext>` 或等价目录。
- 要求同目录缩略图随原图迁移或重新生成，公开商品卡片不得继续派生 pending 缩略图 URL。
- 提供存量公开 SKU pending 主图迁移脚本，支持 dry-run、apply、幂等、对象缺失统计和安全摘要。
- 约束对象迁移必须走后端对象存储适配层，禁止前端直连对象存储或信任前端提交目标路径。

## Rollback Plan

- 若对象正式化逻辑导致 SKU 保存、发布或图片访问异常，可回退本 Change 的后端保存/发布迁移逻辑，保留原 pending 上传与落库行为。
- 回退不得删除已经迁移成功的对象；如需恢复数据库引用，必须依赖迁移脚本输出或审计日志中的原 key / 新 key 映射。
- 若存量迁移 apply 出现异常，应停止后续批次，保留 dry-run / apply 摘要，优先通过对象存在性和数据库引用对账恢复。
- 回退后必须禁用 pending 自动清理任务，直到重新完成对象生命周期修复。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `tile-sku-management`: 补充 SKU 图片暂存对象绑定后的正式化、发布门禁、存量迁移和回归测试要求。
- `object-storage`: 补充 SKU 图片 pending 对象迁移到正式商品目录的对象 key、安全、缩略图和迁移脚本要求。

## Impact

- Backend / Admin API: 影响管理端 SKU 创建、编辑、图片保存和发布流程；可能涉及 `/api/v1/admin/tile-skus`、`PUT /api/v1/admin/tile-skus/{id}`、`POST /api/v1/admin/tile-skus/{id}/publish` 行为。若新增错误码、响应字段或接口参数，必须同步 Pydantic Schema、OpenAPI、Orval 和 `docs/03-api-index.md`。
- Database: 可能更新 `tile_images.object_key` / `url` 的写入语义和存量迁移；通常不要求新增表字段，若引入迁移审计表或字段，必须同步 SQLite/MySQL schema、迁移和 `docs/04-database-design.md`。
- Object Storage / MinIO: 影响图片对象复制、缩略图迁移或生成、对象存在性检查和 pending 清理边界；必须遵守单 Bucket + 标准前缀策略。
- Web Admin: 管理端 SKU 表单、图片上传和发布操作的行为保持可用；如出现迁移失败，需要展示现有统一错误响应。
- Miniapp / Public Web: 公开商品卡片和详情图访问不应回退；公开卡片缩略图 URL 不应继续派生到 pending 目录。
- Tests: 需要补充后端 pytest、对象存储适配测试、存量迁移脚本测试和公开端图片 URL 回归测试。
